"""Publish this private library's archive using existing system Git credentials.

Never prints credentials, accepts tokens on the command line, or stores secrets.
GitHub REST API: https://docs.github.com/en/rest/releases/assets
"""
import argparse
import base64
import hashlib
import http.client
import json
import os
from pathlib import Path
import ssl
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request

REPO = Path(__file__).resolve().parents[1]
TASK = REPO.parent
OWNER = '8j-design'
NAME = 'film-director-library'
PREFIX = f'/repos/{OWNER}/{NAME}'
TAG = 'archive-2026-10-20'

class GitHubError(RuntimeError):
    def __init__(self, status, method, path):
        self.status = status
        super().__init__(f'GitHub HTTP {status} for {method} {path}')

def git(*args):
    return subprocess.check_output(['git', '-c', f'safe.directory={REPO.as_posix()}', *args], cwd=REPO).decode('utf-8').strip()

def credentials():
    env = dict(os.environ, GIT_TERMINAL_PROMPT='0', GCM_INTERACTIVE='never')
    result = subprocess.run(
        ['git', '-c', 'credential.interactive=never', 'credential', 'fill'],
        input=f'protocol=https\nhost=github.com\nusername={OWNER}\n\n',
        text=True, capture_output=True, cwd=REPO, env=env, timeout=30)
    if result.returncode:
        raise RuntimeError('System GitHub credential unavailable; complete official login first.')
    fields = dict(line.split('=', 1) for line in result.stdout.splitlines() if '=' in line)
    if not fields.get('password'):
        raise RuntimeError('System credential did not return an access credential.')
    return fields['password']

def sha256(path):
    result = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024*1024), b''):
            result.update(block)
    return result.hexdigest()

class GitHub:
    def __init__(self):
        self.secret = credentials()

    def headers(self):
        return {'Authorization': 'Bearer ' + self.secret,
                'Accept': 'application/vnd.github+json',
                'User-Agent': 'film-director-library-backup',
                'X-GitHub-Api-Version': '2026-03-10'}

    def request(self, path, method='GET', body=None):
        if not (path == '/user' or path.startswith(PREFIX + '/') or path == PREFIX):
            raise RuntimeError('Request outside the designated repository blocked.')
        data = None if body is None else json.dumps(body, ensure_ascii=False).encode('utf-8')
        headers = self.headers()
        if data is not None:
            headers['Content-Type'] = 'application/json'
        req = urllib.request.Request('https://api.github.com' + path, data=data,
                                     headers=headers, method=method)
        try:
            with urllib.request.urlopen(req, timeout=35) as response:
                return json.load(response)
        except urllib.error.HTTPError as error:
            raise GitHubError(error.code, method, path) from None
        except urllib.error.URLError as error:
            raise RuntimeError(f'GitHub transport error: {error.reason}') from None

    def check_target(self):
        account = self.request('/user')
        repository = self.request(PREFIX)
        if account.get('login', '').lower() != OWNER:
            raise RuntimeError('Logged-in account does not match the authorized owner.')
        if repository.get('full_name', '').lower() != f'{OWNER}/{NAME}' or not repository.get('private'):
            raise RuntimeError('Target repository identity or private visibility mismatch.')
        if not repository.get('permissions', {}).get('push'):
            raise RuntimeError('Current connection lacks push permission.')
        return {'account': account['login'], 'repository': repository['html_url'],
                'private': True, 'can_push': True}

    def verify_tree(self):
        head = git('rev-parse', 'HEAD')
        remote = self.request(PREFIX + '/git/ref/heads/main')['object']['sha']
        raw = subprocess.check_output(['git', '-c', f'safe.directory={REPO.as_posix()}', 'ls-tree', '-rz', 'HEAD'], cwd=REPO)
        expected = {}
        for entry in raw.split(b'\0'):
            if entry:
                meta, path = entry.split(b'\t', 1)
                _mode, kind, oid = meta.decode('ascii').split()
                if kind == 'blob':
                    expected[path.decode('utf-8')] = oid
        tree = self.request(PREFIX + f'/git/trees/{remote}?recursive=1')
        actual = {entry['path']: entry['sha'] for entry in tree['tree'] if entry['type'] == 'blob'}
        if tree.get('truncated') or actual != expected:
            raise RuntimeError('Remote file tree failed the full local-object comparison.')
        return {'commit': remote, 'source_commit': head, 'files': len(expected), 'all_git_blobs_match': True}

    def sync_text(self):
        """API fallback: preserve remote history and refuse unrecorded remote edits."""
        source = git('rev-parse', 'HEAD')
        raw = subprocess.check_output(['git', '-c', f'safe.directory={REPO.as_posix()}',
                                       'ls-tree', '-rz', 'HEAD'], cwd=REPO)
        expected, contents = {}, {}
        for entry in raw.split(b'\0'):
            if not entry:
                continue
            meta, path = entry.split(b'\t',1)
            mode, kind, oid = meta.decode('ascii').split()
            if kind != 'blob' or mode != '100644':
                raise RuntimeError('Only committed ordinary text files are allowed in this sync.')
            name = path.decode('utf-8')
            content = subprocess.check_output(['git','-c',f'safe.directory={REPO.as_posix()}',
                                               'cat-file','blob',oid],cwd=REPO)
            expected[name] = oid
            contents[name] = content.decode('utf-8')
        receipt_path = TASK/'远端提交回执.json'
        try:
            parent = self.request(PREFIX+'/git/ref/heads/main')['object']['sha']
        except GitHubError as error:
            if error.status not in (404,409):
                raise
            try:
                self.request(PREFIX+'/commits?per_page=1')
            except GitHubError as empty:
                if empty.status != 409:
                    raise
            else:
                raise RuntimeError('Repository has history but main is absent; no bootstrap performed.')
            created = self.request(PREFIX+'/contents/README.md','PUT',{
                'message':'初始化私有影视资料库入口',
                'content':base64.b64encode(contents['README.md'].encode('utf-8')).decode('ascii'),
                'branch':'main'})
            parent = created['commit']['sha']
        old = self.request(PREFIX+f'/git/trees/{parent}?recursive=1')
        old_files = {e['path']:e['sha'] for e in old['tree'] if e['type']=='blob'}
        if old.get('truncated'):
            raise RuntimeError('Remote tree was truncated; no update performed.')
        if old_files != expected:
            known = json.loads(receipt_path.read_text(encoding='utf-8')) if receipt_path.exists() else {}
            is_bootstrap = old_files == {'README.md':expected['README.md']}
            if not is_bootstrap and known.get('remote_commit') != parent:
                raise RuntimeError('Remote changed outside the recorded sync; review instead of overwriting.')
            tree = self.request(PREFIX+'/git/trees','POST',{
                'base_tree':old['sha'],
                'tree':[{'path':p,'mode':'100644','type':'blob','content':contents[p]} for p in sorted(contents)]})
            commit = self.request(PREFIX+'/git/commits','POST',{
                'message':'同步导演研究、可见聊天、影视方法、分类与归库流程',
                'tree':tree['sha'],'parents':[parent]})
            self.request(PREFIX+'/git/refs/heads/main','PATCH',{'sha':commit['sha'],'force':False})
        verified = self.verify_tree()
        receipt = dict(verified,remote_commit=verified['commit'],
                       repository=f'https://github.com/{OWNER}/{NAME}',
                       method='GitHub REST Git database; fast-forward only; all blob hashes compared')
        receipt_path.write_text(json.dumps(receipt,ensure_ascii=False,indent=2),encoding='utf-8')
        return receipt

    def upload(self, release, path):
        base = release['upload_url'].split('{', 1)[0]
        url = urllib.parse.urlsplit(base)
        if url.scheme != 'https' or url.hostname != 'uploads.github.com':
            raise RuntimeError('Unexpected release upload host.')
        route = url.path + '?' + urllib.parse.urlencode({'name': path.name})
        connection = http.client.HTTPSConnection(url.hostname, timeout=90,
                                                 context=ssl.create_default_context())
        headers = self.headers()
        headers.update({'Content-Type': 'application/zip', 'Content-Length': str(path.stat().st_size)})
        connection.putrequest('POST', route)
        for name, value in headers.items():
            connection.putheader(name, value)
        connection.endheaders()
        sent = 0
        next_report = 32 * 1024 * 1024
        with path.open('rb') as stream:
            for block in iter(lambda: stream.read(1024 * 1024), b''):
                connection.send(block)
                sent += len(block)
                if sent >= next_report:
                    print(json.dumps({'upload_bytes_sent': sent, 'total': path.stat().st_size}), flush=True)
                    next_report += 32 * 1024 * 1024
        response = connection.getresponse()
        if response.status != 201:
            status = response.status
            response.read()
            connection.close()
            raise RuntimeError(f'Archive upload returned HTTP {status}; no asset was deleted.')
        result = json.load(response)
        connection.close()
        return result

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['check', 'sync', 'verify', 'publish'])
    args = parser.parse_args()
    client = GitHub()
    target = client.check_target()
    if args.action == 'check':
        print(json.dumps(target, ensure_ascii=False))
        return
    if args.action == 'sync':
        print(json.dumps(client.sync_text(),ensure_ascii=False))
        return
    verified = client.verify_tree()
    if args.action == 'verify':
        print(json.dumps(dict(target, **verified), ensure_ascii=False))
        return
    path = TASK / 'director-project-2026-10-20.zip'
    manifest = json.loads((REPO/'archives/2026-10-20/manifest.json').read_text(encoding='utf-8-sig'))
    expected = manifest['archive']
    digest = sha256(path)
    if path.stat().st_size != expected['bytes'] or digest != expected['sha256']:
        raise RuntimeError('Archive no longer matches the previously verified manifest.')
    releases = client.request(PREFIX + '/releases?per_page=100')
    found = [r for r in releases if r['tag_name'] == TAG]
    if len(found) > 1:
        raise RuntimeError('Multiple matching releases require review.')
    release = found[0] if found else client.request(PREFIX + '/releases', 'POST', {
        'tag_name': TAG, 'target_commitish': verified['commit'],
        'name': '导演项目与个人影视资料库：2026-10-20源档案',
        'body': f'私有研究档案，592个源文件。\nZIP字节数：{path.stat().st_size}\nSHA-256：{digest}\n范围和排除项见仓库archives/2026-10-20/manifest.json。',
        'draft': True, 'prerelease': False})
    assets = client.request(PREFIX + f"/releases/{release['id']}/assets?per_page=100")
    matching = [asset for asset in assets if asset['name'] == path.name]
    asset = matching[0] if matching else client.upload(release, path)
    asset = client.request(PREFIX + f"/releases/assets/{asset['id']}")
    if asset.get('state') != 'uploaded' or asset.get('size') != path.stat().st_size:
        raise RuntimeError('Remote archive state or length did not verify; draft preserved.')
    if asset.get('digest') != 'sha256:' + digest:
        raise RuntimeError('GitHub server SHA-256 did not match; draft preserved for review.')
    if release['draft']:
        release = client.request(PREFIX + f"/releases/{release['id']}", 'PATCH', {'draft': False})
        asset = client.request(PREFIX + f"/releases/assets/{asset['id']}")
    result = dict(target, **verified, release_url=release['html_url'],
                  asset_id=asset['id'], asset_url=asset['browser_download_url'],
                  asset_bytes=asset['size'], asset_sha256=digest,
                  server_sha256_verified=True, release_published=not release['draft'])
    (TASK/'发布回执.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False))

if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        # Error messages contain only controlled status/path information, not response headers or credentials.
        print(str(error) if isinstance(error,RuntimeError) else type(error).__name__, file=sys.stderr)
        raise SystemExit(1)
