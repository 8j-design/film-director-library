from pathlib import Path
import subprocess,json,re
from PIL import Image,ImageDraw
t=Path(__file__).resolve().parent; src=t/'本地参考/A04-双子生日-20261030/原发布7695004107710450984.mp4';ff=t.parent/'研究媒体工具/imageio-ffmpeg/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
d=t/'本地参考/A04补核-20261106/红果19-21.2';d.mkdir()
r=subprocess.run([str(ff),'-hide_banner','-loglevel','info','-i',str(src),'-vf','select=gte(t\\,19)*lt(t\\,21.2),showinfo','-vsync','0',str(d/'frame%04d.png')],capture_output=True,text=True,check=True)
pts=[float(x) for x in re.findall(r'pts_time:([\d.]+)',r.stderr)];frames=sorted(d.glob('frame*.png'));assert len(pts)==len(frames)
for s in range(0,len(frames),12):
    batch=frames[s:s+12];board=Image.new('RGB',(1800,625*((len(batch)+3)//4)),'#202020');draw=ImageDraw.Draw(board)
    for k,p in enumerate(batch):
        # Preserve both hands, falling object and the gap between them; full source images remain alongside crops.
        im=Image.open(p).crop((0,200,600,1000)).resize((450,600));x=k%4*450;y=k//4*625;board.paste(im,(x,y+25));draw.text((x+4,y+4),f'source PTS {pts[s+k]:.6f}',fill='white')
    board.save(d/f'board{s//12+1}.png')
j={'source':'https://www.douyin.com/video/7695004107710450984','interval':[19,21.2],'source_pts_seconds':pts,'frames_generated':len(frames),'boards_generated':(len(frames)+11)//12,'crop':[0,200,600,1000],'generated_only_not_read_claim':True,'full_audio_listened':False}
(d/'metadata.json').write_text(json.dumps(j,ensure_ascii=False,indent=2),encoding='utf-8');print({k:v for k,v in j.items() if k!='source_pts_seconds'})
