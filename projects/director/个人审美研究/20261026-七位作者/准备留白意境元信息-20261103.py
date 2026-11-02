from pathlib import Path
import json,csv,io
t=Path(__file__).resolve().parent;r=t/'本地参考/A07-留白意境-20261103'
ids=['7680508700536163618','7683850938414550335','7688320625382804755','7687561226544631091','7690529645023857966']
titles=['凤栖玉人旁','往事流转在你眼眸','如果你的游戏有这种画质','国风才是最x的','这就是古人笔下的东方美学吗']
dur=[34.07,35.60,35.57,30.03,35.43];dims=[(1930,1080),(1930,1080),(2532,1080),(1930,1080),(1930,1080)]
rows=[]
for n,(vid,title,d,dim) in enumerate(zip(ids,titles,dur,dims),1):
 p=r/f'第{n}集{vid}-采样1-0-None/采样元信息.json';j=json.loads(p.read_text(encoding='utf-8'))
 assert all((p.parent/f'table{k}.jpg').is_file() for k in [1,2,3])
 rows.append(dict(episode=n,video_id=vid,url=f'https://www.douyin.com/video/{vid}',title=title,duration_rounded_seconds=d,download_dimensions=list(dim),nominal_samples=j['frames'],boards_actually_viewed=3,sha256=j['sha256'],bytes=j['bytes'],boundary='1-second FFmpeg grid samples/15 contact sheets actually inspected; not source-frame PTS, continuous motion, final fraction or audio verification'))
assert sum(x['nominal_samples'] for x in rows)==171
(t/'A07-留白意境五集实读元信息-20261103.json').write_text(json.dumps({'collection':'https://www.douyin.com/collection/7681638452602406950/1','observed_total':5,'actually_inspected_boards':15,'nominal_samples':171,'third_party_media_local_only':True,'episodes':rows},ensure_ascii=False,indent=2),encoding='utf-8')
b=io.StringIO(newline='');w=csv.DictWriter(b,fieldnames=['episode','video_id','title','url','duration_rounded_seconds','nominal_samples','boards_actually_viewed','boundary'],lineterminator='\n');w.writeheader();w.writerows({k:row[k] for k in w.fieldnames} for row in rows);(t/'A07-留白意境五集覆盖-20261103.csv').write_bytes(b.getvalue().encode('utf-8'))
s=(t/'publish_A07_ferry-20261031.py').read_text(encoding='utf-8')
s=s.replace('four original keyframes','three original wide-shot keyframes').replace('A07-渡口短笺-20261031','A07-渡口远景-20261103').replace('A07-渡口短笺四版原创与回原作检验-20261031.md','A07-渡口远景三轮与经典留白反检-20261103.md').replace("{'V1-渡口短笺.png','V2-渡口短笺.png','V3-渡口短笺.png','V4-近景递笺.png','prompts.md','review.md'}","{'V5-渡口远景.png','V6-人物缩小失败.png','V7-整体拉远.png','prompts.md','review.md'}").replace('four original static keyframes','three original static wide-shot keyframes').replace('len(files)==7','len(files)==6').replace('a07-ferry-keyframes-20261031.zip','a07-ferry-wide-20261103.zip').replace('research-2026-10-31-a07-ferry-keyframes','research-2026-11-03-a07-ferry-wide').replace('A07研究：渡口短笺四张原创关键帧与图后修订','A07研究：渡口远景三轮尺度修正与经典反检').replace('四张原创静态图、完整实际提示词、原参考/同系列对照及失败说明','三张原创静态远景图、完整实际提示词、五集原参考对照及微缩人失败说明').replace('A07-渡口短笺媒体回执-20261031.json','A07-渡口远景媒体回执-20261103.json').replace('four original stills','three original wide-shot stills')
(t/'publish_A07_wide-20261103.py').write_text(s,encoding='utf-8')
print(json.dumps({'episodes':len(rows),'samples':171,'boards_inspected':15},ensure_ascii=False))
