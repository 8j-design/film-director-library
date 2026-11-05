from pathlib import Path
import subprocess,json
from PIL import Image,ImageDraw
t=Path(__file__).resolve().parent;r=t/'本地参考/Mei阿米拉-20261106';src=r/'Mei阿米拉-7672920482366180642.mp4';ff=t.parent/'研究媒体工具/imageio-ffmpeg/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe';out=r/'刀击连续与转接补核';out.mkdir(exist_ok=True)
cmd=[str(ff),'-hide_banner','-loglevel','error','-ss','38','-i',str(src),'-t','2.5','-an','-vf','scale=480:270','-fps_mode','passthrough',str(out/'contact%03d.png')]
assert not list(out.glob('contact*.png'));subprocess.run(cmd,check=True);files=sorted(out.glob('contact*.png'));assert len(files)==75
for s in range(0,len(files),16):
    batch=files[s:s+16];b=Image.new('RGB',(1920,294*((len(batch)+3)//4)),'#202020');d=ImageDraw.Draw(b)
    for k,p in enumerate(batch):b.paste(Image.open(p),(k%4*480,k//4*294+24));d.text((k%4*480+8,k//4*294+5),f'decoded {s+k}, ~{38+(s+k)/30:.3f}s',fill='white')
    b.save(out/f'contact-board{s//16+1}.png')
times=[28.5,29.5,33.5,34.5,40.6,44.5,45.5,46.5,49.5,50.5,51.5,52.5,53.5,58.5,59.5,70.5,71.5,72.5,73.5,75.5,76.5,77.5,78.5,79.5]
for s in range(0,len(times),8):
    batch=times[s:s+8];b=Image.new('RGB',(1920,564*((len(batch)+1)//2)),'#202020');d=ImageDraw.Draw(b)
    for k,z in enumerate(batch):
        p=out/f'extra{z:g}.png';assert not p.exists();subprocess.run([str(ff),'-hide_banner','-loglevel','error','-ss',str(z),'-i',str(src),'-frames:v','1','-vf','scale=960:540',str(p)],check=True);b.paste(Image.open(p),(k%2*960,k//2*564+24));d.text((k%2*960+8,k//2*564+5),f'nominal {z:g}s / seek',fill='white')
    b.save(out/f'extra-board{s//8+1}.png')
j={'contact_start_nominal':38,'duration_seconds':2.5,'decoded_frames':75,'source_fps_reported':30,'contact_boards':5,'extra_nominal_positions':times,'extra_boards':3,'boundary':'source-rate consecutive decoded interval, start seek nominal not exact PTS; generated only until viewed; no claim of sound listening'}
(out/'metadata.json').write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(j)
