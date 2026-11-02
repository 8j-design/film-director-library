from pathlib import Path
import subprocess
from PIL import Image,ImageDraw
root=Path(__file__).resolve().parent/'本地参考'/'M-P3-20261102';out=root/'结论缺句';out.mkdir(exist_ok=True)
ff='C:/Users/scvfv/Documents/ChatGPT/导演/新工作/研究媒体工具/imageio-ffmpeg/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
subprocess.run([ff,'-hide_banner','-loglevel','error','-ss','2180','-i',str(root/'原发布7672707839571283242.mp4'),'-t','36','-vf','fps=1,crop=1920:150:0:930,scale=1280:100',str(out/'s%03d.png')],check=True)
frames=sorted(out.glob('s*.png'))
for start in range(0,len(frames),12):
    batch=frames[start:start+12];im=Image.new('RGB',(1280,125*len(batch)),'#202020');d=ImageDraw.Draw(im)
    for j,p in enumerate(batch):
        t=2180+start+j;im.paste(Image.open(p),(0,j*125+23));d.text((8,j*125+3),f'nominal {t//60}:{t%60:02} / subtitle strip only',fill='white')
    im.save(out/f'board{start//12+1}.png')
print({'strips':len(frames),'start_nominal':2180,'end_nominal':2215,'not_exact_source_pts':True})
tail=out/'tail';tail.mkdir(exist_ok=True)
result=subprocess.run([ff,'-hide_banner','-loglevel','info','-copyts','-ss','2256','-i',str(root/'原发布7672707839571283242.mp4'),'-vf','showinfo','-fps_mode','passthrough',str(tail/'f%03d.png')],check=True,capture_output=True,text=True)
(tail/'decode-log.txt').write_text(result.stderr,encoding='utf-8')
last=sorted(tail.glob('f*.png'));board=Image.new('RGB',(1280,((len(last)+1)//2)*390),'#202020');d=ImageDraw.Draw(board)
for j,p in enumerate(last):
    im=Image.open(p);im.thumbnail((635,355));x=(j%2)*640;y=(j//2)*390;board.paste(im,(x,y+25));d.text((x+8,y+4),f'last source frame {j+1}',fill='white')
board.save(tail/'board.png');print({'tail_decoded_frames':len(last)})
