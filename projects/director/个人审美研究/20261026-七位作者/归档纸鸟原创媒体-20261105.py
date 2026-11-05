from pathlib import Path
import json,hashlib,sys,importlib.util,zipfile
from PIL import Image
task=Path(__file__).resolve().parent
repo=task.parent/'影视资料库建库-20261020/repo'
sys.path.insert(0,str(repo/'tools'))
from publish_archive import GitHub,PREFIX
spec=importlib.util.spec_from_file_location('existing_helper',task/'publish_media.py');helper=importlib.util.module_from_spec(spec);spec.loader.exec_module(helper)
source=task/'原创纸鸟与灯-20261105'
names={'v1.png','v2.png','v3.png','prompts.json','三版实看与回参考复核.md'}
files=sorted(p for p in source.iterdir() if p.name in names);assert {p.name for p in files}==names
items=[]
for p in files:
    row={'name':p.name,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
    if p.suffix=='.png':
        with Image.open(p) as im:row.update(width=im.width,height=im.height);im.verify()
    items.append(row)
manifest={'scope':'original static 6-panel storyboards V1/V2/V3, prompt set and critical review; V3 texture drift not passed; no third-party media or original source URLs','files':items,'animation':False,'sound':False}
(source/'asset-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
files.append(source/'asset-manifest.json')
archive=task/'paperbird-lantern-20261105.zip'
if not archive.exists():
    with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED) as z:
        for p in files:z.write(p,source.name+'/'+p.name)
with zipfile.ZipFile(archive) as z:
    assert set(z.namelist())=={source.name+'/'+p.name for p in files}
    for p in files:assert z.read(source.name+'/'+p.name)==p.read_bytes()
digest=hashlib.sha256(archive.read_bytes()).hexdigest()
c=GitHub();target=c.check_target();head=c.request(PREFIX+'/git/ref/heads/main')['object']['sha']
tag='research-2026-11-05-paperbird-lantern'
found=[r for r in c.request(PREFIX+'/releases?per_page=100') if r['tag_name']==tag];assert len(found)<=1
release=found[0] if found else c.request(PREFIX+'/releases','POST',{'tag_name':tag,'target_commitish':head,'name':'纸鸟与灯：三版静态分镜与失败复核','body':'原创六格分镜三版、完整提示词与实际复核。V2修双向视线；V3留面具但整图材质漂移未通过。灯罩修理因果、连续动作和声音待验证。无第三方原媒体。','draft':True,'prerelease':False})
assets=c.request(PREFIX+f"/releases/{release['id']}/assets?per_page=100");same=[x for x in assets if x['name']==archive.name];assert len(same)<=1
asset=same[0] if same else helper.upload(c,release,archive)
asset=c.request(PREFIX+f"/releases/assets/{asset['id']}")
assert asset['state']=='uploaded' and asset['size']==archive.stat().st_size and asset.get('digest')=='sha256:'+digest
if release['draft']:release=c.request(PREFIX+f"/releases/{release['id']}",'PATCH',{'draft':False})
asset=c.request(PREFIX+f"/releases/assets/{asset['id']}")
assert asset['size']==archive.stat().st_size and asset.get('digest')=='sha256:'+digest
result={'repository':target['repository'],'private':target['private'],'release_url':release['html_url'],'asset_url':asset['browser_download_url'],'asset_id':asset['id'],'bytes':asset['size'],'sha256':digest,'server_sha256_verified':True,'files':len(files),'contents':items,'scope':manifest['scope']}
(task/'纸鸟与灯媒体回执-20261105.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k!='contents'},ensure_ascii=False))
