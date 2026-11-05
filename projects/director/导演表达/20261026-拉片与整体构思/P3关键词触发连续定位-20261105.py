from pathlib import Path
import subprocess,json
from PIL import Image,ImageDraw
r=Path('C:/Users/scvfv/Documents/ChatGPT/导演/新工作/拉片方法与创作能力研究-20261025/本地参考/M-P3-20261102')
o=r/'关键词触发1740-1762-20261105';o.mkdir(exist_ok=True)
f=Path('C:/Users/scvfv/Documents/ChatGPT/导演/新工作/研究媒体工具/imageio-ffmpeg/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe')
times=[1740+i*.5 for i in range(45)]
for start in range(0,len(times),12):
 b=Image.new('RGB',(1920,1536),'#111111');d=ImageDraw.Draw(b)
 for j,t in enumerate(times[start:start+12]):
  p=o/f'{t:.1f}.png';assert not p.exists()
  subprocess.run([str(f),'-hide_banner','-loglevel','error','-ss',str(t),'-i',str(r/'原发布7672707839571283242.mp4'),'-frames:v','1','-vf','scale=640:360',str(p)],check=True)
  x=j%3*640;y=j//3*384;b.paste(Image.open(p),(x,y+24));d.text((x+8,y+5),f'nominal {t:.1f} not exact PTS',fill='white')
 b.save(o/f'board{start//12+1}.png')
(o/'metadata.json').write_text(json.dumps({'source':'https://www.douyin.com/video/7672707839571283242','times':times,'boundary':'half-second grid; not all source frames or listening'},ensure_ascii=False,indent=2),encoding='utf-8')
print({'positions':45,'boards':4})
