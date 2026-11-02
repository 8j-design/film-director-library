from pathlib import Path
import subprocess,re,json
from PIL import Image,ImageDraw
root=Path(__file__).resolve().parent/'本地参考/A07-少女心事第3集-20261031'
out=root/'开伞源帧';out.mkdir(exist_ok=True)
ff='C:/Users/scvfv/Documents/ChatGPT/导演/新工作/研究媒体工具/imageio-ffmpeg/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
filt=r'select=between(t\,19\,22)*not(mod(n\,3)),showinfo'
r=subprocess.run([ff,'-hide_banner','-i',str(root/'原发布7692750596880747776.mp4'),'-vf',filt,'-vsync','0',str(out/'s%03d.png')],capture_output=True,text=True,check=True)
pts=[float(v) for v in re.findall(r'pts_time:([\d.]+)',r.stderr)]
frames=sorted(out.glob('s*.png'));assert len(pts)==len(frames)
for start in range(0,len(frames),10):
    rows=(min(10,len(frames)-start)+1)//2
    board=Image.new('RGB',(1000,rows*305),'#202020');d=ImageDraw.Draw(board)
    for j,p in enumerate(frames[start:start+10]):
        im=Image.open(p).convert('RGB');im.thumbnail((495,280));x=j%2*500;y=j//2*305
        board.paste(im,(x+(495-im.width)//2,y+22));d.text((x+7,y+3),f'source PTS {pts[start+j]:.6f}s',fill='white')
    board.save(out/f'table{start//10+1}.png')
meta={'source_video_id':'7692750596880747776','source_pts_seconds':pts,'selected_frames':len(frames),'selection':'19<=source PTS<=22; every third source frame by n modulo 3','boundary':'sparse source-frame reread, no sound; actual viewing recorded separately'}
(out/'source-pts.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'frames':len(frames),'boards':len(list(out.glob('table*.png'))),'pts_first':pts[0],'pts_last':pts[-1]},ensure_ascii=False))
