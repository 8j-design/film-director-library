from pathlib import Path
import json
t=Path(__file__).resolve().parent;root=t/'本地参考/A07-剑气长歌-20261103'
ids=['7637842246393466122','7641126288408857894','7664555231040113971','7668645774279904538','7670496024552688947','7678285140388269375','7682370643907661090','7687193937836018980','7695354122026945834']
streams={2:list(range(0,76,5)),4:list(range(0,76,5)),7:list(range(0,81,5)),8:[0,5.603054,11.048243,16.600806,22.118105,27.698897,33.302648,40.271566,45.271566,50.271566,55.271566,60.271566,65.271566,70.271566,75.271566,80.271566,83.977133],9:sorted([0,5,80]+[40.003074+5*k for k in range(8)]+[10.54824+5*k for k in range(7)])}
durations={2:77.625,4:75.79,7:83.569,8:85.288,9:80.04};rows=[]
for n,vid in enumerate(ids,1):
 row={'episode':n,'video_id':vid,'source':'https://www.douyin.com/video/'+vid}
 if n in streams:row.update(mode='browser streamed actual images; approximate metadata times with paint delay possible',duration=durations[n],positions=streams[n],count=len(streams[n]),local_media=False)
 else:
  src=root/f'第{n}集{vid}.mp4';metas=list(root.glob(src.stem+'*/采样元信息.json'));assert len(metas)==1
  row.update(mode='local original publication; sampled boards actually inspected',sampling=json.loads(metas[0].read_text(encoding='utf-8')),all_boards_viewed=True,local_media=True)
 rows.append(row)
assert sum(len(v) for v in streams.values())==84
result={'collection':'https://www.douyin.com/collection/7677828369890674714/1','date':'2026-11-03','entries':rows,'local_sample_frames':193,'local_boards_viewed':18,'stream_positions':84,'limits':'Not continuous whole viewing. Audio not listened. Excluded frozen stream9 10-35s attempts and duplicate stream8 0.066s. All source files local only; no model throughput/cost verification.'}
(t/'A07-剑气长歌九集实读元信息-20261103.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps({'entries':len(rows),'stream_positions':84,'sampled':193},ensure_ascii=False))
