from pathlib import Path
import subprocess,json
from PIL import Image,ImageDraw
t=Path(__file__).resolve().parent;r=t/'本地参考/Mei思凡-20261106';src=r/'Mei思凡-7405853931789651263.mp4';ff=t.parent/'研究媒体工具/imageio-ffmpeg/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
out=r/'转接与排比补核';out.mkdir(exist_ok=True);intervals=[]
for begin,end in [(10,11.5),(31.5,36.5)]:
    d=out/f'连续{begin:g}-{end:g}';d.mkdir();filt=f'select=gte(t\\,{begin})*lt(t\\,{end}),scale=480:270'
    subprocess.run([str(ff),'-hide_banner','-loglevel','error','-i',str(src),'-vf',filt,'-vsync','0',str(d/'frame%04d.png')],check=True)
    frames=sorted(d.glob('frame*.png'));assert frames
    for s in range(0,len(frames),16):
        batch=frames[s:s+16];board=Image.new('RGB',(1920,292*((len(batch)+3)//4)),'#202020');draw=ImageDraw.Draw(board)
        for k,p in enumerate(batch):
            x=k%4*480;y=k//4*292;board.paste(Image.open(p),(x,y+22));draw.text((x+5,y+4),f'interval {begin:g}-{end:g}s decoded #{s+k}',fill='white')
        board.save(d/f'board{s//16+1}.png')
    intervals.append({'start_seconds':begin,'end_seconds_exclusive':end,'decoded_frames':len(frames),'boards_generated':(len(frames)+15)//16,'folder':d.name})
times=[6.5,10.5,11.5,15.5,20.5,24.5,26.5,29.5,31.5,33.5,35.5,38.5,39.5]
for s in range(0,len(times),6):
    batch=times[s:s+6];board=Image.new('RGB',(1920,564*((len(batch)+1)//2)),'#202020');draw=ImageDraw.Draw(board)
    for k,z in enumerate(batch):
        dest=out/f'context{z:g}.png';assert not dest.exists()
        subprocess.run([str(ff),'-hide_banner','-loglevel','error','-ss',str(z),'-i',str(src),'-frames:v','1','-vf','scale=960:540',str(dest)],check=True);assert dest.exists()
        x=k%2*960;y=k//2*564;board.paste(Image.open(dest),(x,y+24));draw.text((x+5,y+4),f'nominal {z:g}s; seek not exact PTS',fill='white')
    board.save(out/f'context-board{s//6+1}.png')
j={'intervals':intervals,'context_positions':times,'context_boards_generated':3,'generated_not_yet_viewed':True,'boundary':'all decoded source frames in selected intervals; baked black bars preserved; not audio or full AV'}
(out/'metadata.json').write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(j)
