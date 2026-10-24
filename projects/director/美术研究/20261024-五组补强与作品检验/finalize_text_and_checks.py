from pathlib import Path
import json,re,csv,hashlib
R=Path(__file__).resolve().parent
changed=[]
for p in R.rglob('*'):
 if p.is_file() and p.suffix in ['.md','.json','.csv'] and 'source_pages' not in p.parts:
  t=p.read_text(encoding='utf-8');n=t.replace('徐哲龙','许喆隆')
  if p.name=='五组资料大纲.md':n=n.replace('只读正文/图段，未看转台/源模型','正文与图注文字，未看图/转台/源模型')
  if n!=t:p.write_text(n,encoding='utf-8');changed.append(str(p.relative_to(R)))
p=R/'agents'/'body_costume.md';t=p.read_text(encoding='utf-8')
if 'B13' not in t:
 t+='\n## 终审核名与新增直接访谈 B13\n\n原稿误将Zhelong Xu中文写成另一名字，经[Maxon 2024-10-29直接访谈](https://www.maxon.net/zh/article/3d-artist-zhelong-xu-on-using-zbrush-for-ipad-to-create-mythical-icons)核定为**许喆隆**，主控已统一本批正文和元数据。主控实际读身份字段及创作过程段：先纸/平板草图，再初雕轮廓和层次，喜欢后才继续高分辨率与纹理。两三小时是作者自述该阶段的工作方式，不是通用完成时限；未实看本页图，也未安装/使用ZBrush。工具厂商访谈的赞誉/营销措辞不作为独立审美或兼容性证据。\n'
 p.write_text(t,encoding='utf-8')
# Source navigation deliberately does not re-label every linked page as read.
reports=[R/'agents'/'color_light.md',R/'agents'/'exhibition_perception.md',R/'agents'/'body_costume.md',R/'R36-运动影像研读与转用.md']
rows=[]
for p in reports:
 section=''
 for line in p.read_text(encoding='utf-8').splitlines():
  if line.startswith('#'):section=line.lstrip('# ').strip()
  for label,url in re.findall(r'\[([^\]]+)\]\((https?://[^\s)]+)\)',line):
   rows.append({'url':url,'label':label,'report':str(p.relative_to(R)).replace('\\','/'),'section':section,'reading_status':'见报告该处精确范围；此表含入口、失败、文字及看图，不统一计深研','context':re.sub(r'\[([^\]]+)\]\([^)]+\)',r'\1',line)[:480]})
with (R/'来源导航.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
result={'corrections':changed,'source_navigation_link_occurrences':len(rows),'distinct_page_links':len({r['url'] for r in rows}),'not_a_read_count':True,'video_sha256':hashlib.sha256((R/'artwork/v3/folds-of-air.mp4').read_bytes()).hexdigest()}
(R/'文本与来源核对.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False))
