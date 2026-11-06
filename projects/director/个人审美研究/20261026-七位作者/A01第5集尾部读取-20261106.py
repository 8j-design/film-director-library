from pathlib import Path
import subprocess,json,re,hashlib
from PIL import Image,ImageDraw,ImageOps
t=Path(__file__).resolve().parent;src=t/'A01-猫咪节奏研究-20261030/reference-7681139704313466089.mp4';out=t/'本地参考/A01第5集尾部-20261106';out.mkdir(exist_ok=True)
ff=t.parent/'研究媒体工具/imageio-ffmpeg/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
choices={'tail-sampling':r'gte(t\,18.6)*not(mod(n\,6))','tail-boundary':r'gte(t\,29.8)','left-entry':r'gte(t\,23.4)*lt(t\,24.6)','right-exit':r'gte(t\,21.4)*lt(t\,22.4)'}
import sys
label=sys.argv[1];d=out/label;d.mkdir();p=subprocess.run([str(ff),'-hide_banner','-loglevel','info','-i',str(src),'-vf','select='+choices[label]+',showinfo','-vsync','0',str(d/'frame%04d.png')],capture_output=True,text=True,check=True)
pts=[float(v) for v in re.findall(r'pts_time:([\d.]+)',p.stderr)];frames=sorted(d.glob('frame*.png'));assert len(pts)==len(frames)>0
for s in range(0,len(frames),16):
    batch=frames[s:s+16];b=Image.new('RGB',(1920,294*((len(batch)+3)//4)),'#202020');dr=ImageDraw.Draw(b)
    for k,f in enumerate(batch):
        im=ImageOps.contain(Image.open(f),(480,270));x=k%4*480;y=k//4*294;b.paste(im,(x,y+24));dr.text((x+5,y+5),f'{label} PTS {pts[s+k]:.6f}s',fill='white')
    b.save(d/f'board{s//16+1}.png')
meta={'source_url':'https://www.douyin.com/video/7681139704313466089','source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'scope':label,'source_pts_seconds':pts,'frames':len(frames),'boards':(len(frames)+15)//16,'all_boards_actually_viewed':False,'full_audio_listened':False,'full_audiovisual':False,'series_complete':False}
(d/'metadata.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print({k:v for k,v in meta.items() if k!='source_pts_seconds'})
