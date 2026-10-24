from pathlib import Path
import json,hashlib,shutil,re,zipfile
R=Path(__file__).resolve().parent;REPO=R.parent/'影视资料库建库-20261020/repo';DEST=REPO/'projects/director/美术研究/20261024-五组补强与作品检验'
TAG='research-2026-10-24-five-art-groups';RELEASE='https://github.com/8j-design/film-director-library/releases/tag/'+TAG;DL='https://github.com/8j-design/film-director-library/releases/download/'+TAG+'/'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
sources={
 'color-light-images.json':R/'agents/reference_images/color_light/image_manifest.json',
 'exhibition-images.json':R/'reference_images/exhibition/image_manifest.json',
 'body-images.json':R/'reference_images/body/image_manifest.json',
 'motion-images.json':R/'reference_images/motion/manifest.json',
 'exhibition-viewing-calculation.json':R/'reference_images/exhibition/viewing_geometry.json'}
(R/'sources').mkdir(exist_ok=True)
for name,p in sources.items():shutil.copyfile(p,R/'sources'/name)
deliver=R/'deliverable-assets';deliver.mkdir(exist_ok=True);shutil.copyfile(R/'artwork/v3/base-0192.png',deliver/'folds-v3-preview.png')
files=[]
for p in R.iterdir():
 if p.is_file() and p.suffix in ['.md','.py','.csv','.json'] and p.name not in ['媒体清单.json','媒体发布回执.json','归库完成回执.json']:files.append(p)
for folder in ['agents','artwork','verification','sources']:
 for p in (R/folder).rglob('*'):
  if not p.is_file() or p.suffix=='.blend1':continue
  if folder=='agents' and p.parent!=R/'agents':continue
  if folder=='agents' and p.suffix!='.md':continue
  files.append(p)
files=sorted(set(files));records=[{'path':str(p.relative_to(R)).replace('\\','/'),'bytes':p.stat().st_size,'sha256':sha(p)} for p in files]
archive=R/'five-art-groups-original-work-2026-10-24.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p,row in zip(files,records):z.write(p,row['path'])
 z.writestr('archive-file-manifest.json',json.dumps({'files':records,'exclusions':'Third-party reference image files and website/PDF caches excluded; own reports and source metadata included','scope':'Limited research/test, not complete mastery or audience acceptance'},ensure_ascii=False,indent=2))
with zipfile.ZipFile(archive) as z:
 assert z.testzip() is None
 assert not any(n.startswith('reference_images/') or '/reference_images/' in n for n in z.namelist())
assets=[archive,R/'artwork/v3/folds-of-air.mp4',R/'artwork/v3/folds-animation.blend',R/'verification/versions-contact.png',R/'verification/motion-contact.png',R/'verification/controls-contact.png',deliver/'folds-v3-preview.png']
manifest={'archive':{'name':archive.name,'bytes':archive.stat().st_size,'sha256':sha(archive),'files_without_internal_manifest':len(records)},'release_assets':[{'local_path':str(p.relative_to(R)).replace('\\','/'),'name':p.name,'bytes':p.stat().st_size,'sha256':sha(p)} for p in assets],'rights':'Original work/scripts/reports only; no third-party raw art, film, audio or site cache','release_url':RELEASE,'evidence_scope':'Native source/reopen and actual render/video decode; no complete viewing/audience/physical venue acceptance'}
(R/'媒体清单.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
common={'artwork/v3/folds-of-air.mp4':'folds-of-air.mp4','artwork/v3/folds-animation.blend':'folds-animation.blend','verification/versions-contact.png':'versions-contact.png','verification/motion-contact.png':'motion-contact.png','verification/controls-contact.png':'controls-contact.png'}
def repo_text(text):
 # Absolute local-reference links remain plain provenance notes, not broken GitHub navigation.
 text=re.sub(r'\[([^\]]+)\]\((?:C:/|C:\\)[^)]+\)',r'\1（本地参考证据；原URL及指纹见sources/）',text)
 def link(m):
  bang,label,path=m.groups()
  if path in common:return bang+'['+label+']('+DL+common[path]+')'
  if path.startswith(('artwork/','verification/')) and Path(path).suffix in ['.png','.mp4','.blend']:
   return '['+label+'；媒体包内 '+path+']('+RELEASE+')'
  return m.group(0)
 return re.sub(r'(!?)\[([^\]]+)\]\(([^)]+)\)',link,text)
DEST.mkdir(parents=True,exist_ok=True)
text_files=[p for p in files if p.suffix in ['.md','.py','.csv','.json'] and 'artwork' not in p.relative_to(R).parts and 'decoded-small' not in p.parts and 'gallery-before-distance-correction' not in p.parts]
for p in text_files:
 target=DEST/p.relative_to(R);target.parent.mkdir(parents=True,exist_ok=True)
 t=p.read_text(encoding='utf-8');target.write_text(repo_text(t) if p.suffix=='.md' else t,encoding='utf-8')
(DEST/'媒体清单.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
# Keep small JSON render receipts alongside their original paths.
for p in (R/'artwork').rglob('*.json'):
 target=DEST/p.relative_to(R);target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,target)
readme=DEST/'README.md';t=readme.read_text(encoding='utf-8');t+='\n[完整原创媒体与源文件私有Release]('+RELEASE+')。第三方原图/网页不在媒体包；此仓库正文配合包内文件阅读，媒体验证以回执为准。\n';readme.write_text(t,encoding='utf-8')
print(json.dumps({'archive':manifest['archive'],'text_files_copied':len(text_files),'release_assets':len(assets)},ensure_ascii=False))
