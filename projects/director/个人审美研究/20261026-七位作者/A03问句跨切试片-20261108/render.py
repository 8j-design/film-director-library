from pathlib import Path
import os, shutil
import subprocess
import json
from PIL import Image, ImageDraw, ImageChops

HERE=Path(__file__).resolve().parent
LOCAL_FFMPEG=HERE.parent.parent/'研究媒体工具/imageio-ffmpeg/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
FFMPEG=os.environ.get('FFMPEG') or (str(LOCAL_FFMPEG) if LOCAL_FFMPEG.is_file() else shutil.which('ffmpeg'))
WIDTH,HEIGHT,FPS=480,270,30
CUT=43
COUNT=90

def figure(draw,x,y,scale,color):
    head=round(10*scale)
    draw.ellipse((x-head,y-head,x+head,y+head),fill=color)
    draw.polygon([(x-head,y+head),(x+head,y+head),(x+2*head,y+6*head),(x-2*head,y+6*head)],fill=color)

def frame(i,carry):
    before=i<CUT
    image=Image.new('RGB',(WIDTH,HEIGHT),'#697184' if before else '#729db2')
    draw=ImageDraw.Draw(image)
    if before:
        draw.polygon([(0,66),(480,82),(480,270),(0,270)],fill='#ad8d70')
        draw.polygon([(0,78),(168,113),(120,269),(0,269)],fill='#654a4f')
        draw.polygon([(480,82),(328,113),(375,269),(480,269)],fill='#725355')
        draw.polygon([(99,35),(395,50),(343,94),(149,84)],fill='#d0a46e')
        figure(draw,223,148,0.78,'#292f45')
        draw.ellipse((259,194,278,213),fill='#453b4a')
        draw.polygon([(189,216),(258,197),(272,214),(201,231)],fill='#57485b')
    else:
        draw.polygon([(0,66),(480,100),(480,121),(0,86)],fill='#d0a46e')
        reveal=min(i-CUT,26)
        figure(draw,240,16+3*reveal,2.1,'#403d59')
        draw.polygon([(224,116+3*reveal),(247,128+3*reveal),(236,147+3*reveal)],fill='#c5a173')
    if 27<=i<CUT+carry:
        draw.rectangle((155,230,325,253),fill='#241d29')
        draw.text((169,235),'Where are you taking her?',fill='white')
    return image

def render():
    assert FFMPEG, 'Set FFMPEG or put it on PATH.'
    variants=(0,2,8)
    board=Image.new('RGB',(WIDTH*3,292*4),'#19212c')
    labels=ImageDraw.Draw(board)
    base=[frame(i,0) for i in range(COUNT)]
    changes={}
    stride=WIDTH*HEIGHT*3
    for column,carry in enumerate(variants):
        frames=[frame(i,carry) for i in range(COUNT)]
        boxes={i:ImageChops.difference(base[i],frames[i]).getbbox() for i in range(COUNT)}
        changed=[i for i,b in boxes.items() if b is not None]
        assert changed==list(range(CUT,CUT+carry))
        assert all(boxes[i]==(155,230,326,254) for i in changed)
        filename=HERE/f'carry-{carry:02d}.mp4'
        subprocess.run([str(FFMPEG),'-hide_banner','-loglevel','error','-y','-f','rawvideo','-pix_fmt','rgb24','-video_size','480x270','-framerate',str(FPS),'-i','-','-c:v','libx264','-pix_fmt','yuv420p','-movflags','+faststart',str(filename)],input=b''.join(im.tobytes() for im in frames),check=True)
        decoded=subprocess.check_output([str(FFMPEG),'-hide_banner','-loglevel','error','-i',str(filename),'-f','rawvideo','-pix_fmt','rgb24','-'])
        assert len(decoded)==COUNT*stride
        for row,i in enumerate((42,43,45,51)):
            offset=i*stride
            board.paste(Image.frombytes('RGB',(WIDTH,HEIGHT),decoded[offset:offset+stride]),(column*WIDTH,row*292))
            labels.text((column*WIDTH+8,row*292+275),f'carry {carry} | frame {i}',fill='white')
        changes[str(carry)]=changed
    board.save(HERE/'decoded-contact.png')
    (HERE/'metadata.json').write_text(json.dumps({'fps':FPS,'frames_each':COUNT,'zero_based_cut_frame':CUT,'changed_unencoded_frames_by_carry':changes,'audio':False,'observer_test':False},indent=2)+'\n',encoding='utf-8',newline='\n')

if __name__=='__main__':
    render()
