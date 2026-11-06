from pathlib import Path
import subprocess,json
from PIL import Image,ImageDraw
t=Path(__file__).resolve().parent; r=t/'本地参考/M-P3-20261102';src=r/'原发布7672707839571283242.mp4';ff=t.parent/'研究媒体工具/imageio-ffmpeg/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
d=r/'插片1980-2002-20261106';d.mkdir();times=list(range(1980,2003));times=sorted(set(times))
for z in times:
    p=d/f'full{z:g}.png';subprocess.run([str(ff),'-hide_banner','-loglevel','error','-ss',str(z),'-i',str(src),'-frames:v','1',str(p)],check=True)
for s in range(0,len(times),8):
    batch=times[s:s+8];b=Image.new('RGB',(1920,190*len(batch)),'#202020');draw=ImageDraw.Draw(b)
    for k,z in enumerate(batch):
        im=Image.open(d/f'full{z:g}.png');assert im.size==(1920,1080);im=im.crop((0,920,1920,1080));b.paste(im,(0,k*190+30));draw.text((5,k*190+6),f'nominal source {z:g}s; seek not exact subtitle PTS',fill='white')
    b.save(d/f'sub-board{s//8+1}.png')
contexts=[1981,1985,1989,1993,1997,2001]
for s in range(0,len(contexts),4):
    batch=contexts[s:s+4];b=Image.new('RGB',(1920,564*((len(batch)+1)//2)),'#202020');draw=ImageDraw.Draw(b)
    for k,z in enumerate(batch):
        im=Image.open(d/f'full{z:g}.png').resize((960,540));x=k%2*960;y=k//2*564;b.paste(im,(x,y+24));draw.text((x+5,y+4),f'nominal {z:g}s',fill='white')
    b.save(d/f'context-board{s//4+1}.png')
j={'source_url':'https://www.douyin.com/video/7672707839571283242','subtitle_nominal_positions':times,'context_positions':contexts,'subtitle_boards_generated':(len(times)+7)//8,'context_boards_generated':2,'all_boards_actually_viewed':False,'full_audio_listened':False,'machine_index_used_for_location_only':True}
(d/'metadata.json').write_text(json.dumps(j,ensure_ascii=False,indent=2),encoding='utf-8');print({'positions':len(times),'sub_boards':j['subtitle_boards_generated'],'context_boards':2})
