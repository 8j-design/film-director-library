from pathlib import Path
import json,hashlib,sys,importlib.util,zipfile
from PIL import Image
t=Path(__file__).resolve().parent;repo=t.parent/'影视资料库建库-20261020/repo';sys.path.insert(0,str(repo/'tools'))
from publish_archive import GitHub,PREFIX
spec=importlib.util.spec_from_file_location('existing_helper',t/'publish_media.py');helper=importlib.util.module_from_spec(spec);spec.loader.exec_module(helper)
r=t/'原创灯给谁-20261106';p=r/'prompts.json';j=json.loads(p.read_text(encoding='utf-8'));j['v3']=json.loads((r/'v3-prompt.json').read_text(encoding='utf-8'));p.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
names={'v1.png','v2.png','v3.png','prompts.json','执行与验收.md','V1-V2实看.md','V3实看与回原作反检.md'};files=sorted(p for p in r.iterdir() if p.name in names);assert {p.name for p in files}==names;items=[]
for p in files:
    row={'name':p.name,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
    if p.suffix=='.png':
        with Image.open(p) as im:row.update(width=im.width,height=im.height);im.verify()
    items.append(row)
scope='Original six-panel Lamp for whom V1-V3, two actual revisions and return-to-source review; V2 unintended fifth-panel darkening retained; static stills, no motion/sound/physics/user acceptance claim; no third-party media'
(r/'asset-manifest.json').write_text(json.dumps({'scope':scope,'files':items},ensure_ascii=False,indent=2)+'\n',encoding='utf-8');files.append(r/'asset-manifest.json')
archive=t/'lamp-choice-v1-v3-20261106.zip'
if not archive.exists():
    with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED) as z:
        for p in files:z.write(p,'lamp-choice-v1-v3/'+p.name)
with zipfile.ZipFile(archive) as z:
    assert set(z.namelist())=={'lamp-choice-v1-v3/'+p.name for p in files}
    for p in files:assert z.read('lamp-choice-v1-v3/'+p.name)==p.read_bytes()
digest=hashlib.sha256(archive.read_bytes()).hexdigest();c=GitHub();target=c.check_target();assert target['private'];tag='research-2026-11-06-lamp-choice'
found=[v for v in c.request(PREFIX+'/releases?per_page=100') if v['tag_name']==tag];assert len(found)<=1
release=found[0] if found else c.request(PREFIX+'/releases','POST',{'tag_name':tag,'target_commitish':c.request(PREFIX+'/git/ref/heads/main')['object']['sha'],'name':'灯给谁：原创选择后果三版（2026-11-06）','body':'私有原创研究。六格由照面具转为照共同缝帆，V1因果偏弱、V2误暗第五格、V3恢复工作照明。三图、完整提示词与回M/Mei原作反检，静态图不冒称连续动作/声音/成片或用户验收。旧纸鸟与装罩附件不覆盖，无第三方媒体。','draft':True,'prerelease':False})
assets=c.request(PREFIX+f"/releases/{release['id']}/assets?per_page=100");same=[a for a in assets if a['name']==archive.name];assert len(same)<=1
asset=same[0] if same else helper.upload(c,release,archive);asset=c.request(PREFIX+f"/releases/assets/{asset['id']}")
assert asset['state']=='uploaded' and asset['size']==archive.stat().st_size and asset.get('digest')=='sha256:'+digest
if release['draft']:release=c.request(PREFIX+f"/releases/{release['id']}",'PATCH',{'draft':False})
asset=c.request(PREFIX+f"/releases/assets/{asset['id']}");assert asset['size']==archive.stat().st_size and asset.get('digest')=='sha256:'+digest
result={'repository':target['repository'],'private':target['private'],'release_url':release['html_url'],'asset_url':asset['browser_download_url'],'asset_id':asset['id'],'bytes':asset['size'],'sha256':digest,'server_sha256_verified':True,'files':len(files),'contents':items,'scope':scope}
(t/'灯给谁媒体回执-20261106.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:v for k,v in result.items() if k!='contents'},ensure_ascii=False))
