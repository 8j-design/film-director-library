from pathlib import Path
import subprocess,json
from PIL import Image,ImageDraw
a=Path(__file__).resolve().parent;r=a/'本地参考/Mei练习67-20261105';ff=a.parent/'研究媒体工具/imageio-ffmpeg/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
p=r/'练习6逐帧/full-last-decoded151.png'
assert not p.exists()
subprocess.run([str(ff),'-hide_banner','-loglevel','error','-i',str(r/'练习6-7701738751680122139.mp4'),'-vf',r'select=eq(n\,151)','-vsync','0','-frames:v','1',str(p)],check=True)
assert p.exists()
out=r/'练习7转场';out.mkdir(exist_ok=True)
times=sorted(set([7+i/8 for i in range(17)]+[12.75+i/8 for i in range(9)]+[14.75+i/8 for i in range(9)]+[17.25+i/8 for i in range(17)]))
for start in range(0,len(times),12):
    batch=times[start:start+12];im=Image.new('RGB',(1440,294*((len(batch)+2)//3)),'#222');d=ImageDraw.Draw(im)
    for j,t in enumerate(batch):
        p=out/f'{t:g}.png';assert not p.exists()
        subprocess.run([str(ff),'-hide_banner','-loglevel','error','-ss',str(t),'-i',str(r/'练习7-7702285485346934079.mp4'),'-frames:v','1','-vf','scale=480:270',str(p)],check=True)
        x=j%3*480;y=j//3*294;im.paste(Image.open(p),(x,y+24));d.text((x+5,y+3),f'{t:g}s nominal',fill='white')
    im.save(out/f'board{start//12+1}.png')
(out/'positions.json').write_text(json.dumps({'nominal_seconds':times,'count':len(times),'generated_not_viewed':True,'limits':'selective transition intervals; not audio or whole-clip continuous viewing'},ensure_ascii=False,indent=2),encoding='utf-8')
print({'positions':len(times),'boards':(len(times)+11)//12,'last_source_frame_exists':True})
