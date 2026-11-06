from pathlib import Path
import json,subprocess,re,hashlib,sys
from PIL import Image,ImageDraw,ImageOps
t=Path(__file__).resolve().parent;source=t/'本地参考/M飞屋P2-20261106/M飞屋P2-7632623213981322536.mp4';out=t/'本地参考/M飞屋P2-20261106/连续动作与误认-20261107';out.mkdir(exist_ok=True)
ff=t.parent/'研究媒体工具/imageio-ffmpeg/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
choices={'balloon':(1030,1035,1),'dog-grid':(1110,1124,6),'dog-reveal':(1119,1121,1),'dog-enter':(1121,1126,1)}
label=sys.argv[1];start,end,stride=choices[label];d=out/label;d.mkdir()
vf=f'select=gte(t\\,{start})*lt(t\\,{end})'+(f'*not(mod(n\\,{stride}))' if stride!=1 else '')+',showinfo'
r=subprocess.run([str(ff),'-hide_banner','-loglevel','info','-ss',str(max(0,start-2)),'-copyts','-i',str(source),'-vf',vf,'-vsync','0',str(d/'frame%04d.png')],capture_output=True,text=True,check=True)
pts=[float(x) for x in re.findall(r'pts_time:([\d.]+)',r.stderr)];frames=sorted(d.glob('frame*.png'));assert len(frames)==len(pts)>0
for s in range(0,len(frames),16):
    batch=frames[s:s+16];b=Image.new('RGB',(1920,294*((len(batch)+3)//4)),'#202020');dr=ImageDraw.Draw(b)
    for k,f in enumerate(batch):
        im=ImageOps.contain(Image.open(f),(480,270));x=k%4*480;y=k//4*294;b.paste(im,(x,y+24));dr.text((x+4,y+4),f'{label} sourcePTS {pts[s+k]:.6f}s',fill='white')
    b.save(d/f'board{s//16+1}.png')
j={'label':label,'source_url':'https://www.douyin.com/video/7632623213981322536','source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'selection':'all decoded source frames' if stride==1 else 'every sixth decoded source frame','source_pts_seconds':pts,'frames':len(frames),'boards':(len(frames)+15)//16,'all_boards_actually_viewed':False,'full_audio_listened':False,'full_audiovisual':False,'series_complete':False};(d/'metadata.json').write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print({k:v for k,v in j.items() if k!='source_pts_seconds'})
