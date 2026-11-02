from pathlib import Path
import shutil, subprocess, json, hashlib
from PIL import Image, ImageDraw
root=Path(__file__).resolve().parent/'本地参考'/'A07-少女心事第3集-20261031'
root.mkdir(parents=True,exist_ok=True)
src=root/'原发布7692750596880747776.mp4'
if not src.exists(): shutil.copy2(Path('C:/Users/scvfv/Downloads/download (13).mp4'),src)
ff='C:/Users/scvfv/Documents/ChatGPT/导演/新工作/研究媒体工具/imageio-ffmpeg/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
subprocess.run([ff,'-hide_banner','-loglevel','error','-i',str(src),'-vf','fps=1','-frames:v','49',str(root/'f%03d.png')],check=True)
frames=sorted(root.glob('f*.png'))
for start in range(0,len(frames),10):
    rows=(min(10,len(frames)-start)+1)//2
    board=Image.new('RGB',(1000,rows*305),'#202020'); d=ImageDraw.Draw(board)
    for j,p in enumerate(frames[start:start+10]):
        im=Image.open(p).convert('RGB'); im.thumbnail((495,280))
        x=(j%2)*500;y=(j//2)*305
        board.paste(im,(x+(495-im.width)//2,y+22));d.text((x+7,y+3),f'nominal {start+j}s / fps=1',fill='white')
    board.save(root/f'table{start//10+1}.png')
meta={'url':'https://www.douyin.com/video/7692750596880747776','title':'少女心事第3集：雨天未必有我忧郁','page_publication':'2026-10-04 18:01','duration_dom':49.333333,'nominal_samples':len(frames),'boards':len(list(root.glob('table*.png'))),'source_bytes':src.stat().st_size,'sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'boundary':'nominal fps output; not exact source PTS; actual viewing recorded separately; no continuous AV claim'}
(root/'source-media.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(meta,ensure_ascii=False))
