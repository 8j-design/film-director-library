from pathlib import Path
import sys,json,hashlib,importlib.util,zipfile
t=Path(__file__).resolve().parent;r=t.parent/'影视资料库建库-20261020/repo';source=t/'原创动态点到即止-20261103'
sys.path.insert(0,str(r/'tools'));from publish_archive import GitHub,PREFIX
spec=importlib.util.spec_from_file_location('media_helper',t/'publish_media.py');helper=importlib.util.module_from_spec(spec);spec.loader.exec_module(helper)
files=sorted(p for p in source.iterdir() if p.is_file() and p.suffix in ['.md','.py','.json','.jpg','.mp4'] and p.name!='asset-manifest.json')
assert len([p for p in files if p.suffix=='.mp4'])==6
manifest={'scope':'original 2D contact timing rough animatics V1-V6, keypose boards, scripts and actual failures/review; no third-party media; not polished action/sound validation','files':[{'name':p.name,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files]}
(source/'asset-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');files.append(source/'asset-manifest.json')
archive=t/'original-contact-animatic-20261103.zip'
with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED) as z:
 for p in files:z.write(p,source.name+'/'+p.name)
digest=hashlib.sha256(archive.read_bytes()).hexdigest();c=GitHub();target=c.check_target();head=c.request(PREFIX+'/git/ref/heads/main')['object']['sha']
tag='research-2026-11-03-original-contact-animatic';found=[x for x in c.request(PREFIX+'/releases?per_page=100') if x['tag_name']==tag];assert len(found)<=1
rel=found[0] if found else c.request(PREFIX+'/releases','POST',{'tag_name':tag,'target_commitish':head,'name':'原创动作粗版：点到即止六轮及失败复核','body':'私有研究阶段。六个8秒二维粗版、关键姿态图版、制作脚本及实际复核。保留剑线穿脸、再次交叉与提前接触等失败；V5/V6仅为短剑尖端相触停留对照。步态重心、招架、连续播放和听声未验收。无第三方原媒体。','draft':True,'prerelease':False})
assets=c.request(PREFIX+f"/releases/{rel['id']}/assets?per_page=100");same=[x for x in assets if x['name']==archive.name];assert len(same)<=1
asset=same[0] if same else helper.upload(c,rel,archive);asset=c.request(PREFIX+f"/releases/assets/{asset['id']}")
assert asset['state']=='uploaded' and asset['size']==archive.stat().st_size and asset.get('digest')=='sha256:'+digest
if rel['draft']:rel=c.request(PREFIX+f"/releases/{rel['id']}",'PATCH',{'draft':False})
asset=c.request(PREFIX+f"/releases/assets/{asset['id']}");assert asset['size']==archive.stat().st_size and asset['digest']=='sha256:'+digest
result={'repository':target['repository'],'private':target['private'],'release_url':rel['html_url'],'asset_url':asset['browser_download_url'],'bytes':asset['size'],'sha256':digest,'server_sha256_verified':True,'files':len(files),'scope':manifest['scope']}
(t/'原创点到即止媒体回执-20261103.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(result,ensure_ascii=False))
