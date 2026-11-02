from pathlib import Path
import subprocess,re,json,sys,hashlib
from PIL import Image,ImageDraw
root=Path(__file__).resolve().parent/'本地参考/A07-清的小剧场-20261102'
name=sys.argv[1];stride=float(sys.argv[2]) if len(sys.argv)>2 else .5
start=float(sys.argv[3]) if len(sys.argv)>3 else 0
end=float(sys.argv[4]) if len(sys.argv)>4 else None
src=root/name;out=root/(src.stem+('-半秒采样' if stride==.5 and not start and end is None else f'-采样{stride:g}-{start:g}-{end}'));out.mkdir(exist_ok=True)
assert not list(out.glob('s*.png'))
ff=Path(__file__).resolve().parents[1]/'研究媒体工具/imageio-ffmpeg/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
sel=f',select=gte(t\\,{start})'+(f'*lt(t\\,{end})' if end is not None else '') if start or end is not None else ''
cmd=[str(ff),'-hide_banner','-i',str(src),'-vf',f'fps=1/{stride}{sel},showinfo,scale=480:-2','-fps_mode','passthrough',str(out/'s%03d.png')]
r=subprocess.run(cmd,capture_output=True,text=True,check=True)
pts=[float(t) for t in re.findall(r'pts_time:([\d.]+)',r.stderr)]
frames=sorted(out.glob('s*.png'));assert len(pts)==len(frames)
for start in range(0,len(frames),12):
 batch=frames[start:start+12];wide=Image.open(batch[0]).width>Image.open(batch[0]).height;cellh=170 if wide else 410
 board=Image.new('RGB',(1200,((len(batch)+3)//4)*cellh),'#202020');d=ImageDraw.Draw(board)
 for j,p in enumerate(batch):
  im=Image.open(p).convert('RGB');im.thumbnail((294,cellh-30));x=j%4*300;y=j//4*cellh
  board.paste(im,(x+(294-im.width)//2,y+25));d.text((x+4,y+4),f'sample {pts[start+j]:.3f}s',fill='white')
 board.save(out/f'table{start//12+1}.jpg',quality=93)
meta={'source':name,'bytes':src.stat().st_size,'sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'selection':f'FFmpeg fps sampling every {stride}s; output grid time, not guaranteed original source PTS','sample_times':pts,'frames':len(frames),'boards':(len(frames)+11)//12,'boundary':'Must actually inspect boards; neither continuous source frame coverage nor sound listening'}
(out/'采样元信息.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf-8')
print(r.stderr[:1000]);print(json.dumps(meta,ensure_ascii=False))
