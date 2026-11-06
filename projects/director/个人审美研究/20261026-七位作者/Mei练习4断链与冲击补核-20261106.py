from pathlib import Path
import subprocess,json
from PIL import Image,ImageDraw
t=Path(__file__).resolve().parent;r=t/'本地参考/Mei练习4-20261106';src=r/'Mei练习4-7694136610048183593.mp4';ff=t.parent/'研究媒体工具/imageio-ffmpeg/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe';out=r/'断链与末端连续补核';out.mkdir(exist_ok=True);records=[]
for name,start in [('break',50),('impact',56)]:
    assert not list(out.glob(name+'[0-9]*.png'))
    subprocess.run([str(ff),'-hide_banner','-loglevel','error','-ss',str(start),'-i',str(src),'-t','2','-an','-vf','scale=480:270','-fps_mode','passthrough',str(out/(name+'%03d.png'))],check=True);files=sorted(out.glob(name+'[0-9]*.png'));assert len(files)==60
    for s in range(0,len(files),16):
        batch=files[s:s+16];b=Image.new('RGB',(1920,294*((len(batch)+3)//4)),'#202020');d=ImageDraw.Draw(b)
        for k,p in enumerate(batch):b.paste(Image.open(p),(k%4*480,k//4*294+24));d.text((k%4*480+8,k//4*294+5),f'{name} decoded {s+k}, ~{start+(s+k)/30:.3f}s',fill='white')
        b.save(out/f'{name}-board{s//16+1}.png')
    records.append({'label':name,'start_nominal':start,'duration':2,'decoded_frames':60,'boards_generated':4})
times=[4.5,14.5,21.5,24.5,35.5,38.5,40.5,44.5]
for s in range(0,len(times),4):
    batch=times[s:s+4];b=Image.new('RGB',(2048,600*((len(batch)+1)//2)),'#202020');d=ImageDraw.Draw(b)
    for k,z in enumerate(batch):
        p=out/f'context{z:g}.png';assert not p.exists();subprocess.run([str(ff),'-hide_banner','-loglevel','error','-ss',str(z),'-i',str(src),'-frames:v','1',str(p)],check=True);b.paste(Image.open(p),(k%2*1024,k//2*600+24));d.text((k%2*1024+8,k//2*600+5),f'nominal {z:g}s / source-sized',fill='white')
    b.save(out/f'context-board{s//4+1}.png')
(out/'metadata.json').write_text(json.dumps({'intervals':records,'full_context_positions':times,'full_context_boards':2,'boundary':'generated only until viewed; intervals source-rate decoded, absolute time nominal seek + 30fps estimate; sound not listened'},ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print({'consecutive_frames':120,'context_images':8,'boards_generated':10})
