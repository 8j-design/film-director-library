from pathlib import Path
import argparse,shutil,subprocess,json,hashlib,math
from PIL import Image,ImageDraw
p=argparse.ArgumentParser();p.add_argument('episode',type=int);p.add_argument('video_id');p.add_argument('download');p.add_argument('duration',type=float);args=p.parse_args()
assert args.video_id.isdigit() and 1<=args.episode<=13
root=Path(__file__).resolve().parent/'本地参考'/f'A07-少女心事第{args.episode}集-20261102';root.mkdir(parents=True,exist_ok=True)
src=root/f'原发布{args.video_id}.mp4'
if not src.exists():shutil.copy2(args.download,src)
ff='C:/Users/scvfv/Documents/ChatGPT/导演/新工作/研究媒体工具/imageio-ffmpeg/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
count=math.floor(args.duration)
subprocess.run([ff,'-hide_banner','-loglevel','error','-i',str(src),'-vf','fps=1','-frames:v',str(count),str(root/'f%03d.png')],check=True)
frames=sorted(root.glob('f*.png'))
for start in range(0,len(frames),10):
    batch=frames[start:start+10];board=Image.new('RGB',(1000,((len(batch)+1)//2)*305),'#202020');d=ImageDraw.Draw(board)
    for j,frame in enumerate(batch):
        im=Image.open(frame).convert('RGB');im.thumbnail((495,280));x=(j%2)*500;y=(j//2)*305
        board.paste(im,(x+(495-im.width)//2,y+22));d.text((x+7,y+3),f'nominal {start+j}s / fps=1',fill='white')
    board.save(root/f'table{start//10+1}.png')
meta={'url':f'https://www.douyin.com/video/{args.video_id}','episode':args.episode,'duration_dom':args.duration,'source_bytes':src.stat().st_size,'sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'nominal_samples':len(frames),'boundary':'actual boards must be viewed separately; nominal fps samples, not complete AV'}
(root/'source-media.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(meta,ensure_ascii=False))
