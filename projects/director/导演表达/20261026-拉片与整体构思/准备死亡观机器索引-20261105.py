from pathlib import Path
root=Path(__file__).resolve().parent
s=(root/'M-P3分段机器语音-20261104.py').read_text(encoding='utf-8')
s=s.replace('<=2256','<=1337').replace("'M-P3-20261102'","'M寻梦飞屋死亡观-20261105'").replace('20261104','20261105').replace('7672707839571283242','7653391978796813594')
p=root/'M寻梦飞屋分段机器语音-20261105.py';assert not p.exists();p.write_text(s,encoding='utf-8')
