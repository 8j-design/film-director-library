from pathlib import Path
import json,csv,io
t=Path(__file__).resolve().parent
p=t/'M-P5分批位置-20261103.json';j=json.loads(p.read_text(encoding='utf-8'));assert j['count']==505
j.update(final_tail_positions=[2744.560339],count=506,last_actual=2744.560339,unread_tail_seconds=0.272971,next='final 0.272971 seconds, audio, sampling gaps and remaining obscured clauses; cross-episode comparison',remote_status='pending 20261104 receipt; previous remote covered 505 plus 11 separate reinspections')
p.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
p=t/'逐集覆盖台账-20261026.csv';rows=list(csv.DictReader(io.StringIO(p.read_text(encoding='utf-8-sig'))));found=0
for row in rows:
 if row['video_id']=='7689055016908246323':
  row['status']='506名义画面/字幕位置；另11无遮挡重读；声音/间隙/末0.273秒未完'
  row['latest_reading_range']='20261104整合上次真实尾点2744.560339/2744.83331，黑底细红线；506主位置，11无遮挡重读另记。原生进度条只验证实际呈现位置，不称连续覆盖尾1.6秒。末0.272971秒、完整声音、间隙与跨集待核。';found+=1
assert found==1
b=io.StringIO(newline='');ww=csv.DictWriter(b,fieldnames=list(rows[0]),lineterminator='\n');ww.writeheader();ww.writerows(rows);p.write_text(b.getvalue(),encoding='utf-8',newline='\n')
print(json.dumps({'count':506,'last_actual':2744.560339,'remaining_tail':0.272971},ensure_ascii=False))
