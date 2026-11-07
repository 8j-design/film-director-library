from pathlib import Path
import hashlib
import json
import math
import subprocess
from PIL import Image, ImageDraw

here = Path(__file__).resolve().parent
ff = here.parent.parent / '研究媒体工具/imageio-ffmpeg/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
W, H, FPS, N, CUT = 640, 360, 24, 72, 36
views = {'A': (0, 0, 900, 506), 'B': (171, 113, 801, 467), 'C': (65, 113, 695, 467)}

def frame(i, mode):
    src = Image.new('RGB', (900, 506), '#698893')
    d = ImageDraw.Draw(src)
    d.polygon([(0, 330), (185, 254), (400, 310), (590, 278), (900, 334), (900, 506), (0, 506)], fill='#83774e')
    d.polygon([(0, 378), (305, 325), (570, 360), (900, 319), (900, 506), (0, 506)], fill='#aa9253')
    for x, y, r in [(680, 180, 120), (625, 158, 90), (680, 106, 82), (752, 209, 74), (549, 216, 83)]:
        d.ellipse((x-r, y-r, x+r, y+r), fill='#bbc4bb')
    for x, y, r in [(673, 168, 99), (622, 146, 70), (682, 99, 68), (752, 200, 57), (544, 207, 66)]:
        d.ellipse((x-r, y-r, x+r, y+r), fill='#d2cfb5')
    for k in range(270):
        x=(k*97)%900
        y=345+(k*43)%162
        h=5+(k*11)%10
        d.line((x,y,x-4,y-h), fill=('#b6a365','#7b7247','#c4ab6a')[k%3], width=1)
    # Same target pose, motion, terrain and moment of reveal in all versions.
    px, foot = 570 + round(2*math.sin(i/5)), 379
    d.line([(px-1,foot),(px+4,foot-9),(px+7,foot-15),(px+14,foot-20)], fill='#303f43', width=4)
    d.line([(px+4,foot-9),(px+9,foot)], fill='#303f43', width=3)
    d.line([(px+12,foot-18),(px+6,foot-11)], fill='#36434a', width=2)
    d.ellipse((px+12,foot-26,px+19,foot-19), fill='#28343c')
    d.line([(px+13,foot-19),(px+7,foot-21),(px-1,foot-22-(i%7)//4)], fill='#e0bd7b', width=2)
    if i < CUT:
        # Dark foreground crosses the actor, then leaves the frame at the edit.
        end = 705 + round(13*math.sin(i/6))
        d.polygon([(0,0),(end-120,0),(end,305),(end-18,429),(end-72,506),(0,506)], fill='#303b3c')
        for k in range(24):
            x=21+k*25
            d.polygon([(x,345),(x+14,335),(x+23,350),(x+10,360)], outline='#46514e')
    window = views[mode] if i >= CUT else views['A']
    return src.crop(window).resize((W,H), Image.Resampling.LANCZOS)

def encode(name):
    dest=here/f'{name}.mp4'
    assert not dest.exists()
    cmd=[str(ff),'-v','error','-f','rawvideo','-pixel_format','rgb24','-video_size',f'{W}x{H}',
         '-framerate',str(FPS),'-i','-','-an','-c:v','libx264','-pix_fmt','yuv420p','-movflags','+faststart',str(dest)]
    p=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    for i in range(N):
        p.stdin.write(frame(i,name).tobytes())
    p.stdin.close()
    assert p.wait()==0
    out=subprocess.check_output([str(ff),'-v','error','-i',str(dest),'-f','rawvideo','-pix_fmt','rgb24','-'])
    assert len(out)==W*H*3*N
    return dest,out

if __name__=='__main__':
    sheet=Image.new('RGB',(960,606),'#1a232c'); pen=ImageDraw.Draw(sheet)
    labels={'A':'A - same scale','B':'B - matched zoom','C':'C - displaced zoom'}
    report={}
    for y,mode in enumerate(views):
        dest,data=encode(mode)
        report[mode]={'decoded_frames':N,'sha256':hashlib.sha256(dest.read_bytes()).hexdigest()}
        for x,i in enumerate((35,36,52)):
            offset=i*W*H*3
            thumb=Image.frombytes('RGB',(W,H),data[offset:offset+W*H*3]).resize((320,180))
            sheet.paste(thumb,(x*320,y*202+20))
            pen.text((x*320+8,y*202+5), f'{labels[mode]} | frame {i}',fill='white')
    sheet.save(here/'decoded-contact.png')
    (here/'metadata.json').write_text(json.dumps({'fps':FPS,'reveal_frame':CUT,'frames':N,'audio':False,'views':views,'variants':report},indent=2)+'\n',encoding='utf-8')
