from pathlib import Path
import subprocess,json,re,hashlib
from PIL import Image,ImageDraw,ImageOps
t=Path(__file__).resolve().parent;r=t/'A01-猫咪节奏研究-20261030';out=t/'本地参考/A01猫近景-20261106';out.mkdir(exist_ok=True);ff=t.parent/'研究媒体工具/imageio-ffmpeg/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
meta=out/'metadata.json';scopes=json.loads(meta.read_text(encoding='utf-8'))['scopes'] if meta.exists() else []
for label,vid,start,end in [('pose5',7681139704313466089,16,18),('pose3',7682994627658468841,19,21.5),('pose5-exit',7681139704313466089,18,18.6)]:
    src=r/f'reference-{vid}.mp4';d=out/label
    if d.exists():
        assert any(s['label']==label for s in scopes)
        continue
    d.mkdir()
    filt=f'select=gte(t\\,{start})*lt(t\\,{end}),showinfo'
    p=subprocess.run([str(ff),'-hide_banner','-loglevel','info','-i',str(src),'-vf',filt,'-vsync','0',str(d/'frame%04d.png')],capture_output=True,text=True,check=True)
    pts=[float(x) for x in re.findall(r'pts_time:([\d.]+)',p.stderr)];frames=sorted(d.glob('frame*.png'));assert len(pts)==len(frames)>0
    dimensions=Image.open(frames[0]).size
    for s in range(0,len(frames),16):
        batch=frames[s:s+16];b=Image.new('RGB',(1920,294*((len(batch)+3)//4)),'#202020');draw=ImageDraw.Draw(b)
        for k,f in enumerate(batch):
            im=ImageOps.contain(Image.open(f),(480,270));x=k%4*480;y=k//4*294;b.paste(im,(x+(480-im.width)//2,y+24+(270-im.height)//2));draw.text((x+5,y+5),f'{label} source {pts[s+k]:.6f}s',fill='white')
        b.save(d/f'board{s//16+1}.png')
    scopes.append({'label':label,'source_url':f'https://www.douyin.com/video/{vid}','source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'dimensions':dimensions,'interval_seconds':[start,end],'source_pts_seconds':pts,'decoded_frames':len(frames),'boards_generated':(len(frames)+15)//16,'all_boards_actually_viewed':False})
(out/'metadata.json').write_text(json.dumps({'scopes':scopes,'full_audio_listened':False,'series_complete':False},ensure_ascii=False,indent=2),encoding='utf-8');print([{k:v for k,v in s.items() if k!='source_pts_seconds'} for s in scopes])
