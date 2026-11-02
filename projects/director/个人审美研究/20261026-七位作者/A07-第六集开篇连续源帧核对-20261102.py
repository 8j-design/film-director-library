from pathlib import Path
import subprocess,re,json,argparse
from PIL import Image,ImageDraw
root=Path(__file__).resolve().parent/'本地参考/A07-少女心事第6集-20261031'
parser=argparse.ArgumentParser();parser.add_argument('--start',type=float,default=0);parser.add_argument('--end',type=float,default=4);args=parser.parse_args()
assert 0<=args.start<args.end<=40.066667
out=root/('开篇连续源帧-20261102' if args.start==0 and args.end==4 else f'连续源帧{args.start:g}-{args.end:g}-20261102');out.mkdir(exist_ok=True)
ff='C:/Users/scvfv/Documents/ChatGPT/导演/新工作/研究媒体工具/imageio-ffmpeg/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
# No stride: decode every source frame in [start,end). Image scaling is for review only.
assert not list(out.glob('s*.png')),'Existing output must not be overwritten'
filt=f'select=gte(t\\,{args.start})*lt(t\\,{args.end}),showinfo,scale=640:-2'
r=subprocess.run([ff,'-hide_banner','-i',str(root/'原发布7695724385688210703.mp4'),'-vf',filt,'-fps_mode','passthrough',str(out/'s%03d.png')],capture_output=True,text=True,check=True)
pts=[float(v) for v in re.findall(r'pts_time:([\d.]+)',r.stderr)]
frames=sorted(out.glob('s*.png'));assert len(pts)==len(frames)
for start in range(0,len(frames),16):
 batch=frames[start:start+16];board=Image.new('RGB',(1280,((len(batch)+3)//4)*205),'#202020');d=ImageDraw.Draw(board)
 for j,p in enumerate(batch):
  im=Image.open(p).convert('RGB');im.thumbnail((316,178));x=j%4*320;y=j//4*205
  board.paste(im,(x+(316-im.width)//2,y+24));d.text((x+4,y+4),f'PTS {pts[start+j]:.6f}',fill='white')
 board.save(out/f'table{start//16+1}.png')
(out/'source-pts.json').write_text(json.dumps({'source_video_id':'7695724385688210703','source_pts_seconds':pts,'source_frames':len(frames),'selection':f'all decoded source frames where {args.start} <= PTS < {args.end}; no frame stride','boundary':'scaled review boards must actually be read; no sound or whole-clip AV claim'},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'source_frames':len(frames),'boards':(len(frames)+15)//16,'first_pts':pts[0],'last_pts':pts[-1]},ensure_ascii=False))
