from pathlib import Path
import json, subprocess, math
from PIL import Image, ImageDraw, ImageChops

HERE=Path(__file__).resolve().parent
FF=HERE.parent.parent/'研究媒体工具/imageio-ffmpeg/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
W,H,FPS,N,CUT=640,360,24,192,72

def letter(d,x,y,s=1):
    x,y=int(x),int(y);w,h=int(38*s),int(24*s)
    d.rectangle((x,y,x+w,y+h),fill='#e8d8ab',outline='#807564',width=1)
    d.line([(x,y),(x+w//2,y+h//2),(x+w,y)],fill='#807564',width=1)
    d.rectangle((x+w-8,y+3,x+w-4,y+7),fill='#a75b47')

def frame(n,variant):
    im=Image.new('RGB',(W,H),'#283e4c');d=ImageDraw.Draw(im)
    if n<CUT:
        d.rectangle((0,120,W,H),fill='#5f7378')
        d.polygon([(0,230),(640,200),(640,300),(0,335)],fill='#a47e58')
        letter(d,248,212,3)
        d.rectangle((389,99,415,230),fill='#bba88d')
        d.ellipse((374,215,417,237),fill='#bba88d')
        return im
    d.polygon([(0,260),(640,260),(640,360),(0,360)],fill='#53636a')
    d.rectangle((45,40,176,257),fill='#172a39',outline='#789397',width=3)
    d.rectangle((210,42,602,233),fill='#334c58',outline='#182e3c',width=4)
    for y in (90,138,186,234):d.line((210,y,602,y),fill='#a47e58',width=5)
    if variant!='A':
        for row in range(4):
            for col in range(10):
                letter(d,216+38*col,63+48*row,.85)
    d.rectangle((324,260,592,276),fill='#a47e58')
    for x in (340,575):d.line((x,277,x,344),fill='#80634c',width=8)
    letter(d,430,240,1)
    t=(n-CUT)/FPS;x=105+min(t/3.5,1)*190
    d.ellipse((x-11,199,x+11,222),fill='#c0ac91')
    d.polygon([(x-13,222),(x+14,222),(x+20,279),(x-18,279)],fill='#d19557')
    sway=math.sin(t*7)*7 if t<3.5 else 0
    d.line((x-7,278,x-10+sway,325),fill='#172a39',width=8)
    d.line((x+8,278,x+13-sway,325),fill='#172a39',width=8)
    d.line((x+10,234,x+30,254),fill='#c0ac91',width=7)
    letter(d,x+22,244,.7)
    return im

def run():
    raws={};meta={}
    for v in ('A','B'):
        frames=[frame(n,v) for n in range(N)];out=HERE/f'{v}.mp4'
        subprocess.run([str(FF),'-hide_banner','-loglevel','error','-n','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-an','-c:v','libx264','-crf','17','-pix_fmt','yuv420p','-movflags','+faststart',str(out)],input=b''.join(f.tobytes() for f in frames),check=True)
        raws[v]=subprocess.check_output([str(FF),'-hide_banner','-loglevel','error','-i',str(out),'-f','rawvideo','-pix_fmt','rgb24','-'])
        assert len(raws[v])==N*W*H*3
        meta[v]={'frames':N,'seconds':N/FPS,'audio':False,'additional_shelf_letters':0 if v=='A' else 40}
    assert all(frame(n,'A').tobytes()==frame(n,'B').tobytes() for n in range(CUT))
    boxes=[ImageChops.difference(frame(n,'A'),frame(n,'B')).getbbox() for n in range(CUT,N)]
    board=Image.new('RGB',(W*2,(H+22)*3),'#19242c');d=ImageDraw.Draw(board)
    for col,v in enumerate(('A','B')):
        for row,n in enumerate((71,84,180)):
            stride=W*H*3;im=Image.frombytes('RGB',(W,H),raws[v][n*stride:(n+1)*stride])
            board.paste(im,(col*W,row*(H+22)));d.text((col*W+8,row*(H+22)+H+3),f'{v} frame {n} / {n/FPS:.2f}s',fill='white')
    board.save(HERE/'decoded-comparison.png')
    (HERE/'verification.json').write_text(json.dumps({'outputs':meta,'precut_exact_match':True,'difference_bounds':sorted(set(boxes)),'cut_frame':CUT,'observer_feedback':False,'decoded_frames_checked_by_code':N},indent=2),encoding='utf-8')

if __name__=='__main__':run()
