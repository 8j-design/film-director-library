from pathlib import Path
import subprocess,json,re,hashlib
from PIL import Image,ImageDraw
t=Path(__file__).resolve().parent; ff=t.parent/'研究媒体工具/imageio-ffmpeg/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
out=t/'本地参考/A04补核-20261106';out.mkdir(exist_ok=True)
scopes=[]
for name,src,start,end,crop,scale in [('fruit',t/'本地参考/A04-双子生日-20261030/原发布7695004107710450984.mp4',20.2,20.8,(0,480,500,980),(500,500)),('fifty-tail',t/'本地参考/A04-同画师第50集-20261030/原发布7502400928919915802.mp4',32,34,None,(288,402))]:
    d=out/name;d.mkdir();filt=f'select=gte(t\\,{start})*lt(t\\,{end}),showinfo'
    r=subprocess.run([str(ff),'-hide_banner','-loglevel','info','-i',str(src),'-vf',filt,'-vsync','0',str(d/'frame%04d.png')],capture_output=True,text=True,check=True)
    pts=[float(x) for x in re.findall(r'pts_time:([\d.]+)',r.stderr)];frames=sorted(d.glob('frame*.png'));assert len(pts)==len(frames)>0
    for s in range(0,len(frames),16):
        batch=frames[s:s+16];w,h=scale;b=Image.new('RGB',(w*4,(h+25)*((len(batch)+3)//4)),'#202020');draw=ImageDraw.Draw(b)
        for k,p in enumerate(batch):
            im=Image.open(p)
            if crop:im=im.crop(crop)
            im=im.resize(scale);x=k%4*w;y=k//4*(h+25);b.paste(im,(x,y+25));draw.text((x+5,y+5),f'source PTS {pts[s+k]:.6f}',fill='white')
        b.save(d/f'board{s//16+1}.png')
    scopes.append({'name':name,'source_filename':src.name,'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'selected_interval':[start,end],'source_pts_seconds':pts,'decoded_frames':len(frames),'boards':(len(frames)+15)//16,'crop':crop,'all_boards_actually_viewed':False})
src=t/'本地参考/A04-同画师第50集-20261030/原发布7502400928919915802.mp4'
for z in [28.5,30,33.3]:subprocess.run([str(ff),'-hide_banner','-loglevel','error','-ss',str(z),'-i',str(src),'-frames:v','1',str(out/f'fifty-full{z:g}.png')],check=True)
(out/'metadata.json').write_text(json.dumps({'scopes':scopes,'full_context_nominal_positions':[28.5,30,33.3],'generated_only_until_viewed':True,'audio_actually_listened':False},ensure_ascii=False,indent=2),encoding='utf-8')
print([{k:v for k,v in s.items() if k not in ['source_pts_seconds']} for s in scopes])
