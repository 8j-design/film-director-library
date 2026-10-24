"""Publish only this batch's original work to the already authorized private film library."""
from pathlib import Path
import hashlib,json,sys,http.client,ssl,urllib.parse,mimetypes
TASK=Path(__file__).resolve().parent;REPO=TASK.parent/'影视资料库建库-20261020/repo'
sys.path.insert(0,str(REPO/'tools'))
from publish_archive import GitHub,PREFIX
TAG='research-2026-10-24-five-art-groups'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def upload(c,release,path):
 base=urllib.parse.urlsplit(release['upload_url'].split('{',1)[0])
 if base.scheme!='https' or base.hostname!='uploads.github.com':raise RuntimeError('Unexpected upload host.')
 route=base.path+'?'+urllib.parse.urlencode({'name':path.name})
 conn=http.client.HTTPSConnection(base.hostname,timeout=90,context=ssl.create_default_context())
 headers=c.headers();headers.update({'Content-Type':mimetypes.guess_type(path.name)[0] or 'application/octet-stream','Content-Length':str(path.stat().st_size)})
 conn.putrequest('POST',route)
 for k,v in headers.items():conn.putheader(k,v)
 conn.endheaders()
 with path.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):conn.send(b)
 response=conn.getresponse();data=response.read();status=response.status;conn.close()
 if status!=201:raise RuntimeError('Media upload returned HTTP '+str(status)+'; nothing overwritten.')
 return json.loads(data)
def main():
 manifest=json.loads((TASK/'媒体清单.json').read_text(encoding='utf-8'))
 c=GitHub();target=c.check_target();verified=c.verify_tree()
 releases=[r for r in c.request(PREFIX+'/releases?per_page=100') if r['tag_name']==TAG]
 if len(releases)>1:raise RuntimeError('Multiple matching releases; stopped.')
 release=releases[0] if releases else c.request(PREFIX+'/releases','POST',{'tag_name':TAG,'target_commitish':verified['commit'],'name':'五组美术补强：原创空衣三维试作、控制与检验（2026-10-24）','body':'私有研究过程。包含三版工程、两段16秒静音中间/修订输出、固定帧色光控制、展示修正及真实解码证据。完整源在ZIP；下方另有预览与V3工程。第三方参考图/网页不包含。有限试作不等于五组全部掌握。','draft':True,'prerelease':False})
 receipts=[]
 existing=c.request(PREFIX+f"/releases/{release['id']}/assets?per_page=100")
 for item in manifest['release_assets']:
  path=TASK/item['local_path'];digest=sha(path)
  if digest!=item['sha256'] or path.stat().st_size!=item['bytes']:raise RuntimeError('Local media changed: '+path.name)
  found=[a for a in existing if a['name']==path.name]
  if len(found)>1:raise RuntimeError('Duplicate assets; stopped.')
  asset=found[0] if found else upload(c,release,path)
  asset=c.request(PREFIX+f"/releases/assets/{asset['id']}")
  if asset.get('state')!='uploaded' or asset.get('size')!=item['bytes'] or asset.get('digest')!='sha256:'+digest:raise RuntimeError('Media checksum/length mismatch; existing asset preserved: '+path.name)
  receipts.append({'name':path.name,'asset_id':asset['id'],'url':asset['browser_download_url'],'bytes':asset['size'],'sha256':digest,'server_sha256_verified':True})
 if release['draft']:release=c.request(PREFIX+f"/releases/{release['id']}",'PATCH',{'draft':False})
 for row in receipts:
  final=c.request(PREFIX+f"/releases/assets/{row['asset_id']}")
  if final.get('size')!=row['bytes'] or final.get('digest')!='sha256:'+row['sha256']:raise RuntimeError('Final verification mismatch.')
 result=dict(target,**verified,release_url=release['html_url'],release_published=not release['draft'],assets=receipts,all_server_sha256_verified=True)
 (TASK/'媒体发布回执.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(json.dumps({'release_url':result['release_url'],'private':target,'assets':len(receipts),'all_server_sha256_verified':True},ensure_ascii=False))
if __name__=='__main__':
 try:main()
 except Exception as e:
  print(str(e) if isinstance(e,RuntimeError) else type(e).__name__,file=sys.stderr);raise SystemExit(1)
