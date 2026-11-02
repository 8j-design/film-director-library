from pathlib import Path
import shutil, subprocess, hashlib, json
from PIL import Image, ImageDraw
root=Path(__file__).resolve().parent/'本地参考'/'M-P3-20261102'
root.mkdir(parents=True,exist_ok=True)
src=root/'原发布7672707839571283242.mp4'
if not src.exists(): shutil.copy2('C:/Users/scvfv/Downloads/download (14).mp4',src)
ff='C:/Users/scvfv/Documents/ChatGPT/导演/新工作/研究媒体工具/imageio-ffmpeg/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
positions=list(range(2180,2256,5))+[2256]
for t in positions:
    subprocess.run([ff,'-hide_banner','-loglevel','error','-ss',str(t),'-i',str(src),'-frames:v','1',str(root/f't{t}.png')],check=True)
for start in range(0,len(positions),4):
    batch=positions[start:start+4]; board=Image.new('RGB',(1280,len(batch)*390),'#202020');d=ImageDraw.Draw(board)
    for j,t in enumerate(batch):
        im=Image.open(root/f't{t}.png').convert('RGB');im.thumbnail((1275,360))
        board.paste(im,((1280-im.width)//2,j*390+24));d.text((8,j*390+4),f'nominal {t//60:02}:{t%60:02} / {t}s',fill='white')
    board.save(root/f'table{start//4+1}.png')
meta={'url':'https://www.douyin.com/video/7672707839571283242','source_bytes':src.stat().st_size,'sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'positions_seconds':positions,'boundary':'FFmpeg nominal seeks; actual visual reading recorded separately; no full AV claim'}
(root/'source-media.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(meta,ensure_ascii=False))
