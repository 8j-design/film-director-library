"""Publish only four original keyframes and their actual prompts/review to existing private library."""
from pathlib import Path
import sys,json,hashlib,importlib.util,zipfile,shutil
from PIL import Image
task=Path(__file__).resolve().parent
repo=task.parent/'影视资料库建库-20261020/repo'
sys.path.insert(0,str(repo/'tools'))
from publish_archive import GitHub,PREFIX
spec=importlib.util.spec_from_file_location('existing_media_helper',task/'publish_media.py')
helper=importlib.util.module_from_spec(spec);spec.loader.exec_module(helper)
source=task/'原创试验'/'A07-渡口短笺-20261031'
shutil.copy2(task/'A07-渡口短笺四版原创与回原作检验-20261031.md',source/'review.md')
base=sorted(p for p in source.iterdir() if p.is_file() and p.name!='asset-manifest.json')
assert {p.name for p in base}=={'V1-渡口短笺.png','V2-渡口短笺.png','V3-渡口短笺.png','V4-近景递笺.png','prompts.md','review.md'}
items=[]
for p in base:
    row={'name':p.name,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
    if p.suffix=='.png':
        with Image.open(p) as im: row.update(width=im.width,height=im.height,mode=im.mode);im.verify()
    items.append(row)
(source/'asset-manifest.json').write_text(json.dumps({'scope':'four original static keyframes, built-in image_gen, actual prompts/review; no third-party media; no continuous motion/sound claim','files':items},ensure_ascii=False,indent=2),encoding='utf-8')
files=sorted(p for p in source.iterdir() if p.is_file());assert len(files)==7
archive=task/'a07-ferry-keyframes-20261031.zip'
with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED) as z:
    for p in files:z.write(p,source.name+'/'+p.name)
digest=hashlib.sha256(archive.read_bytes()).hexdigest()
c=GitHub();target=c.check_target()
head=c.request(PREFIX+'/git/ref/heads/main')['object']['sha']
tag='research-2026-10-31-a07-ferry-keyframes'
found=[r for r in c.request(PREFIX+'/releases?per_page=100') if r['tag_name']==tag];assert len(found)<=1
release=found[0] if found else c.request(PREFIX+'/releases','POST',{'tag_name':tag,'target_commitish':head,'name':'A07研究：渡口短笺四张原创关键帧与图后修订','body':'私有阶段研究。四张原创静态图、完整实际提示词、原参考/同系列对照及失败说明。非连续动画，不称声画、身份或手部跨帧通过；没有第三方原媒体。','draft':True,'prerelease':False})
assets=c.request(PREFIX+f"/releases/{release['id']}/assets?per_page=100")
same=[a for a in assets if a['name']==archive.name];assert len(same)<=1
asset=same[0] if same else helper.upload(c,release,archive)
asset=c.request(PREFIX+f"/releases/assets/{asset['id']}")
assert asset['state']=='uploaded' and asset['size']==archive.stat().st_size and asset.get('digest')=='sha256:'+digest
if release['draft']:release=c.request(PREFIX+f"/releases/{release['id']}",'PATCH',{'draft':False})
asset=c.request(PREFIX+f"/releases/assets/{asset['id']}")
assert asset['size']==archive.stat().st_size and asset['digest']=='sha256:'+digest
result={'repository':target['repository'],'private':target['private'],'release_url':release['html_url'],'asset_url':asset['browser_download_url'],'asset_id':asset['id'],'bytes':asset['size'],'sha256':digest,'server_sha256_verified':True,'files':len(files),'scope':'four original stills, prompt set, actual review and manifest; no third-party media; no animation claim','contents':[{'name':p.name,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files]}
(task/'A07-渡口短笺媒体回执-20261031.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k!='contents'},ensure_ascii=False))
