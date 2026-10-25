from pathlib import Path
import csv,shutil
R=Path(__file__).resolve().parent;A=R/'agents';snap=A/'audit-start-snapshots';snap.mkdir(exist_ok=True)
for name in ['award_benchmarks.csv','art44_audit.csv']:
 if not (snap/name).exists():shutil.copy2(A/name,snap/name)
def load(p):return list(csv.DictReader(p.open(encoding='utf-8-sig')))
def save(p,rows):
 with p.open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
rows=load(A/'award_benchmarks.csv')
for row in rows:
 if row['id']=='B19':
  row['actual_read_scope']='初核读作者多像技术笔记实质选段；本批接续已取得NFB完整公开源并作全片范围103幅静帧覆盖，主控/子agent实际看图，详见pas_visual_analysis.md；不是正常速度完整视听'
  row['unverified_scope']='未正常速度连续观看或实听；未确认原胶片放映体验；103幅不是19512帧全部实看，不以静帧推音乐/精确运动效果'
  row['legal_fullfilm_route']='NFB公开匿名播放器明示未加密HLS完整217段已合法获取，仅本地研究；来源/版本/哈希见official_film_materials.md'
  row['read_date']='2026-10-24—2026-10-25接续'
save(A/'award_benchmarks.csv',rows)
rows=load(A/'art44_audit.csv')
for row in rows:row['本轮重新读取外部原文范围']='初次审计未新增外部重读；此后本批研究/制作增量见44组本轮复验增量.csv及主总结，不以空白表示后续未做'
save(A/'art44_audit.csv',rows)
p=A/'art44_audit.md';t=p.read_text(encoding='utf-8');note='> 接续口径（2026-10-25）：本稿逐题判断是初次审计基线，后续实际研究/制作增量见主目录《44组本轮复验增量.csv》《复验结果与研究总结.md》。例如R21所记Sprite未取是当时状态；本批后续已取得公开成片并看全片范围及关键窗口图，完整Style Guide仍未取得。各题“未新增外部重读”仅指审计动作，不覆盖其后工作。原始CSV快照保存在audit-start-snapshots/。\n\n'
if not t.startswith('> 接续口径'):p.write_text(note+t,encoding='utf-8')
p=A/'award_benchmarks.md';t=p.read_text(encoding='utf-8');note='> 接续实作补充（2026-10-25）：下文获取/未看图状态记录初核时点。B19随后已取得NFB完整公开源，完成全片范围103幅静帧及关键原图核看，见pas_visual_analysis.md；仍未正常速度完整视听。CSV B19已更新并保留初核快照。Sprite和8项华语制作正文另列，不能将各表行数相加为独立深研影片数。\n\n'
if not t.startswith('> 接续实作补充'):p.write_text(note+t,encoding='utf-8')
print('TABLE_CONTINUATION_FIXED')
