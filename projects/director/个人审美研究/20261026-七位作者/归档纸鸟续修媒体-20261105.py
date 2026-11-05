from pathlib import Path
import json,hashlib,sys,importlib.util,zipfile
from PIL import Image
task=Path(__file__).resolve().parent;repo=task.parent/'影视资料库建库-20261020/repo'
sys.path.insert(0,str(repo/'tools'))
from publish_archive import GitHub,PREFIX
spec=importlib.util.spec_from_file_location('existing_helper',task/'publish_media.py');helper=importlib.util.module_from_spec(spec);spec.loader.exec_module(helper)
source=task/'原创纸鸟与灯-20261105/修灯续修';names={'v4.png','v5.png','prompts.json','V4-V5因果与材质复核.md'}
files=sorted(p for p in source.iterdir() if p.name in names);assert {p.name for p in files}==names
items=[]
for p in files:
    row={'name':p.name,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
    if p.suffix=='.png':
        with Image.open(p) as im:row.update(width=im.width,height=im.height);im.verify()
    items.append(row)
scope='original V4/V5 still storyboards from V2 branch, two actual edit prompts and causal/texture review; no third-party media; no motion or sound claim'
(source/'asset-manifest.json').write_text(json.dumps({'scope':scope,'files':items},ensure_ascii=False,indent=2),encoding='utf-8');files.append(source/'asset-manifest.json')
archive=task/'paperbird-cause-v4-v5-20261105.zip'
if not archive.exists():
    with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED) as z:
        for p in files:z.write(p,'paperbird-cause-v4-v5/'+p.name)
with zipfile.ZipFile(archive) as z:
    assert set(z.namelist())=={'paperbird-cause-v4-v5/'+p.name for p in files}
    for p in files:assert z.read('paperbird-cause-v4-v5/'+p.name)==p.read_bytes()
digest=hashlib.sha256(archive.read_bytes()).hexdigest();c=GitHub();target=c.check_target()
found=[r for r in c.request(PREFIX+'/releases?per_page=100') if r['tag_name']=='research-2026-11-05-paperbird-lantern'];assert len(found)==1;release=found[0]
assets=c.request(PREFIX+f"/releases/{release['id']}/assets?per_page=100");same=[x for x in assets if x['name']==archive.name];assert len(same)<=1
asset=same[0] if same else helper.upload(c,release,archive);asset=c.request(PREFIX+f"/releases/assets/{asset['id']}")
assert asset['state']=='uploaded' and asset['size']==archive.stat().st_size and asset.get('digest')=='sha256:'+digest
addition='补充V4—V5附件：V2分支补备用完整灯罩，V5恢复干涩线色；装罩/递灯连续动作、声音及V3面具支线合并仍未验证。旧V1—V3附件不变。'
if addition not in (release.get('body') or ''):release=c.request(PREFIX+f"/releases/{release['id']}",'PATCH',{'body':(release.get('body') or '')+'\n\n'+addition})
r={'repository':target['repository'],'private':target['private'],'release_url':release['html_url'],'asset_url':asset['browser_download_url'],'asset_id':asset['id'],'bytes':asset['size'],'sha256':digest,'server_sha256_verified':True,'files':len(files),'contents':items,'scope':scope}
(task/'纸鸟与灯V4-V5媒体回执-20261105.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps({k:v for k,v in r.items() if k!='contents'},ensure_ascii=False))
