from pathlib import Path
import subprocess,json,re,hashlib,sys
from PIL import Image,ImageDraw,ImageOps
t=Path(__file__).resolve().parent;root=t/'本地参考/A07-宸阙观古-20261104';out=t/'本地参考/A07宸阙转接-20261106';out.mkdir(exist_ok=True)
ff=t.parent/'研究媒体工具/imageio-ffmpeg/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
choices={'E4-state':('E4-7669749149704719668.mp4',2.5,5.5),'E5-cloth':('E5-7679031394835713299.mp4',17,22),'E4-before':('E4-7669749149704719668.mp4',0,2.5),'E4-after':('E4-7669749149704719668.mp4',5.5,7.5),'E5-before':('E5-7679031394835713299.mp4',15.5,17),'E5-after':('E5-7679031394835713299.mp4',22,23),'E1-grid':('E1-7662002359173778724.mp4',0,24),'E1-tail':('E1-7662002359173778724.mp4',22,24),'E1-jump':('E1-7662002359173778724.mp4',5.2,7.4)}
choices.update({'E2-tail':('E2-7663828587891428671.mp4',40,42),'E3-tail':('E3-7669002333358984490.mp4',28,29),'E4-tail':('E4-7669749149704719668.mp4',31,33),'E5-tail':('E5-7679031394835713299.mp4',33,34)})
choices.update({'E2-pipa':('E2-7663828587891428671.mp4',14,17),'E3-pipa':('E3-7669002333358984490.mp4',21,24.5)})
choices.update({'E5-late23':('E5-7679031394835713299.mp4',23,26),'E5-late26':('E5-7679031394835713299.mp4',26,29),'E5-late29':('E5-7679031394835713299.mp4',29,33)})
choices.update({'E5-early0':('E5-7679031394835713299.mp4',0,17)})
choices.update({'E4-dance7':('E4-7669749149704719668.mp4',7.5,15.5),'E4-dance15':('E4-7669749149704719668.mp4',15.5,23.5),'E4-late23':('E4-7669749149704719668.mp4',23.5,31)})
label=sys.argv[1];name,start,end=choices[label];src=root/name;d=out/label;d.mkdir()
vf=f'select=gte(t\\,{start})*lt(t\\,{end}),showinfo'
if label=='E1-grid':vf=f'select=gte(t\\,{start})*lt(t\\,{end})*not(mod(n\\,6)),showinfo'
p=subprocess.run([str(ff),'-hide_banner','-loglevel','info','-i',str(src),'-vf',vf,'-vsync','0',str(d/'frame%04d.png')],capture_output=True,text=True,check=True)
pts=[float(v) for v in re.findall(r'pts_time:([\d.]+)',p.stderr)];frames=sorted(d.glob('frame*.png'));assert len(frames)==len(pts)>0;dim=Image.open(frames[0]).size
for s in range(0,len(frames),16):
    batch=frames[s:s+16];b=Image.new('RGB',(1920,230*((len(batch)+3)//4)),'#202020');dr=ImageDraw.Draw(b)
    for k,f in enumerate(batch):
        im=ImageOps.contain(Image.open(f),(480,206));x=k%4*480;y=k//4*230;b.paste(im,(x+(480-im.width)//2,y+24));dr.text((x+4,y+4),f'{label} sourcePTS {pts[s+k]:.6f}s',fill='white')
    b.save(d/f'board{s//16+1}.png')
vid=src.stem.split('-')[-1];j={'label':label,'selection':'every sixth decoded frame' if label=='E1-grid' else 'all decoded source frames in interval','source_url':f'https://www.douyin.com/video/{vid}','source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'source_dimensions':dim,'interval_seconds':[start,end],'source_pts_seconds':pts,'frames':len(frames),'boards':(len(frames)+15)//16,'all_boards_actually_viewed':False,'full_audio_listened':False,'full_audiovisual':False,'series_complete':False}
(d/'metadata.json').write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print({k:v for k,v in j.items() if k!='source_pts_seconds'})
