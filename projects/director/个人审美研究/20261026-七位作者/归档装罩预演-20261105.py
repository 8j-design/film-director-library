from pathlib import Path
import json,hashlib,sys,importlib.util,zipfile
task=Path(__file__).resolve().parent;source=task/'原创装罩动作-20261105';repo=task.parent/'影视资料库建库-20261020/repo'
sys.path.insert(0,str(repo/'tools'))
from publish_archive import GitHub,PREFIX
spec=importlib.util.spec_from_file_location('existing_helper',task/'publish_media.py');helper=importlib.util.module_from_spec(spec);spec.loader.exec_module(helper)
verification=json.loads((source/'encoded-verification.json').read_text(encoding='utf-8'))
for row in verification:row['selected_images_review']='all listed decoded images actually inspected; not continuous playback'
(source/'encoded-verification.json').write_text(json.dumps(verification,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
files=[source/n for n in ['执行大纲.md','实看与回原作复核.md','render_blocking.py','verify_encoded.py','encoded-verification.json']]
for v in range(1,5):
    meta=source/f'v{v}/metadata.json';j=json.loads(meta.read_text(encoding='utf-8'));j['actual_review_status']='see encoded-verification.json and 实看与回原作复核.md; selected images reviewed, not continuous playback';meta.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    files.extend([source/f'v{v}/assembly.mp4',meta]);files.extend(sorted((source/f'v{v}/decoded').glob('board*.png')))
items=[{'path':p.relative_to(source).as_posix(),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files]
manifest=source/'asset-manifest.json';manifest.write_text(json.dumps({'scope':'original code-native silent motion blocking V1-V4; no reference media/pixels; contact causality only, rotation partly occluded, anatomy and full scene unverified','files':items},ensure_ascii=False,indent=2)+'\n',encoding='utf-8');files.append(manifest)
archive=task/'lantern-assembly-blocking-v1-v4-20261105.zip';assert not archive.exists()
with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED) as z:
    for p in files:z.write(p,'lantern-assembly-blocking/'+p.relative_to(source).as_posix())
with zipfile.ZipFile(archive) as z:
    for p in files:assert z.read('lantern-assembly-blocking/'+p.relative_to(source).as_posix())==p.read_bytes()
digest=hashlib.sha256(archive.read_bytes()).hexdigest();c=GitHub();target=c.check_target()
found=[r for r in c.request(PREFIX+'/releases?per_page=100') if r['tag_name']=='research-2026-11-05-paperbird-lantern'];assert len(found)==1;release=found[0]
assets=c.request(PREFIX+f"/releases/{release['id']}/assets?per_page=100");assert not any(x['name']==archive.name for x in assets)
asset=helper.upload(c,release,archive);asset=c.request(PREFIX+f"/releases/assets/{asset['id']}")
assert asset['state']=='uploaded' and asset['size']==archive.stat().st_size and asset.get('digest')=='sha256:'+digest
addition='新增8秒无声装罩几何预演V1—V4附件：保留失败与遮挡修订，四版完整解码/选点实看。V4接触后点亮较清楚，旋转仍部分遮挡；非真实装配或人物风格动画，前后选择及声音未完成。'
if addition not in (release.get('body') or ''):c.request(PREFIX+f"/releases/{release['id']}",'PATCH',{'body':(release.get('body') or '')+'\n\n'+addition})
receipt={'repository':target['repository'],'private':target['private'],'release_url':release['html_url'],'asset_url':asset['browser_download_url'],'asset_id':asset['id'],'bytes':asset['size'],'sha256':digest,'server_sha256_verified':True,'files':len(files),'scope':json.loads(manifest.read_text(encoding='utf-8'))['scope']}
(task/'装罩预演媒体回执-20261105.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(receipt,ensure_ascii=False))
