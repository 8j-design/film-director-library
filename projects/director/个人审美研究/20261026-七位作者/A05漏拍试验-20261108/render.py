from pathlib import Path
from hashlib import sha256
from math import sin, cos, pi, exp
import json
import os
import shutil
import subprocess
import wave

import numpy as np
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
LOCAL = HERE.parent.parent/'研究媒体工具/imageio-ffmpeg/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
FFMPEG = os.getenv('FFMPEG') or (str(LOCAL) if LOCAL.is_file() else shutil.which('ffmpeg'))
W, H, FPS, FRAMES = 640, 360, 24, 96
RATE = 48000
BEATS = (15, 33, 51, 69, 87)
SKIP = 51
INSERT = range(48, 62)
BG = Image.new('RGB', (W,H), '#222737')
sky = ImageDraw.Draw(BG)
sky.rectangle((0,216,640,360),fill='#403d48')
sky.polygon([(0,216),(640,216),(640,246),(0,286)],fill='#524854')
for x in (28,144,249,391,507,618):
    sky.line([(x,42),(x,219)],fill='#34343e',width=8)
sky.line([(0,77),(156,107),(317,116),(498,95),(640,55)],fill='#a47966',width=2)
for x,y in [(52,86),(129,102),(220,111),(314,116),(406,106),(507,92),(595,69)]:
    sky.rounded_rectangle((x-7,y-1,x+7,y+22),radius=5,fill='#e6ad73')
    sky.line((x-4,y+5,x+4,y+5),fill='#fae1a2',width=2)
for x,y in [(46,186),(120,189),(162,185),(342,196),(370,185),(585,181),(610,194)]:
    sky.ellipse((x-10,y-32,x+10,y-12),fill='#424255')
    sky.rounded_rectangle((x-13,y-12,x+13,y+41),radius=9,fill='#3b3b4b')
sky.ellipse((117,259,414,325),fill='#6b514f')
sky.ellipse((420,271,580,306),fill='#51464d')

def dancer(d,i):
    sway=13*sin(2*pi*i/42)
    x=255+sway
    tilt=17*sin(2*pi*i/48)
    d.ellipse((x-49,281,x+55,297),fill='#584246')
    d.polygon([(x-20,172),(x+20,170),(x+39+tilt,237),(x+82+tilt,282),(x+15,291),(x-66-tilt,274),(x-41,217)],fill='#a75062')
    d.polygon([(x-20,171),(x+20,171),(x+21,223),(x+65+tilt,270),(x+14,282),(x-29,246)],fill='#db785e')
    d.line((x-11,189,x-39,258,x-22,275),fill='#f0a17d',width=4)
    d.polygon([(x-19,153),(x-47-tilt,128),(x-66-tilt,106),(x-59-tilt,99),(x-33,121),(x-5,137)],fill='#e8ba90')
    d.polygon([(x+13,155),(x+35,130),(x+65+tilt,123),(x+70+tilt,131),(x+39,146),(x+23,163)],fill='#f0c5a0')
    d.ellipse((x-23,111,x+17,155),fill='#453243')
    d.ellipse((x-14,119,x+20,151),fill='#f0c5a0')
    d.polygon([(x-22,127),(x+20,117),(x+8,107),(x-15,109)],fill='#594052')
    d.arc((x+2,132,x+14,143),10,130,fill='#884851',width=2)

def drummer(d,i,skip):
    x,y=(491,218)
    d.polygon([(x-44,y+14),(x+30,y+8),(x+46,y+58),(x-32,y+57)],fill='#5d7e79')
    d.ellipse((x-27,y-50,x+27,y+4),fill='#e4ae7c')
    d.polygon([(x-33,y-26),(x-29,y-54),(x+15,y-62),(x+32,y-44),(x+31,y-24),(x+18,y-40),(x-22,y-35)],fill='#343345')
    gazing=skip and 47<=i<58
    gaze=-11 if gazing else 3
    d.ellipse((x-9+gaze,y-24,x-5+gaze,y-20),fill='#252737')
    d.ellipse((x+7+gaze,y-24,x+11+gaze,y-20),fill='#252737')
    if gazing:
        d.line((x-11,y-13,x+1,y-13),fill='#72465a',width=2)
    d.rounded_rectangle((x-42,y+45,x+42,y+89),radius=9,fill='#936966')
    d.ellipse((x-42,y+35,x+42,y+61),fill='#d4a986',outline='#574758',width=3)
    nearest=min(BEATS,key=lambda hit:abs(hit-i))
    distance=abs(nearest-i)
    can_strike=not (skip and nearest==SKIP)
    drop=(1-distance/5) if can_strike and distance<5 else 0
    elbow=(x+33,y+25)
    hand=(x-3,y+10+22*drop) if not gazing else (x+11,y+12)
    d.line((elbow,hand),fill='#efb891',width=8)
    tip=(hand[0]-22,hand[1]+12)
    d.line((hand,tip),fill='#f4d398',width=4)

def frame(i,version):
    image=BG.copy()
    d=ImageDraw.Draw(image)
    dancer(d,i)
    drummer(d,i,version!=0)
    if version==2 and i in INSERT:
        image=image.crop((340,147,640,316)).resize((W,H),Image.Resampling.LANCZOS)
    return image

def synth(skip):
    total=np.zeros(FRAMES*RATE//FPS,dtype=np.float64)
    t=np.arange(round(RATE*.13))/RATE
    hit=np.exp(-t*36)*(np.sin(2*pi*97*t)+.34*np.sin(2*pi*174*t))
    for beat in BEATS:
        if skip and beat==SKIP:
            continue
        n=beat*RATE//FPS
        total[n:n+len(hit)] += hit
    return np.rint(total*14500).astype('<i2')

def wav(path,pcm):
    with wave.open(str(path),'wb') as file:
        file.setnchannels(1)
        file.setsampwidth(2)
        file.setframerate(RATE)
        file.writeframes(pcm.tobytes())

def ff(*args,data=None):
    return subprocess.check_output([FFMPEG,'-v','error',*map(str,args)],input=data)

def framehash(path):
    lines=ff('-i',path,'-map','0:v:0','-f','framemd5','-').decode().splitlines()
    return [s.rsplit(',',1)[-1].strip() for s in lines if not s.startswith('#')]

def audiodata(path):
    return ff('-i',path,'-map','0:a:0','-c:a','pcm_s16le','-f','s16le','-')

assert FFMPEG
board=Image.new('RGB',(1120,710),'#252737')
label=ImageDraw.Draw(board)
row_names=('01 All strikes', '02 Missed strike, wide shot', '03 Same missed strike, reaction insert')
points=(45,51,57,69)
files=[]
for v, name in enumerate(('01-all-strikes','02-missed-wide','03-missed-insert')):
    audio=HERE/f'{name}.wav'
    wav(audio,synth(v!=0))
    output=HERE/f'{name}.mp4'
    pictures=[]
    for i in range(FRAMES):
        im=frame(i,v)
        pictures.append(im.tobytes())
    ff('-y','-f','rawvideo','-pix_fmt','rgb24','-video_size',f'{W}x{H}','-framerate',FPS,'-i','-','-i',audio,
       '-c:v','libx264','-crf','16','-pix_fmt','yuv420p','-c:a','aac','-b:a','96k','-movflags','+faststart',output,
       data=b''.join(pictures))
    audio.unlink()
    decoded=ff('-i',output,'-map','0:v:0','-pix_fmt','rgb24','-f','rawvideo','-')
    stride=W*H*3
    assert len(decoded)==FRAMES*stride
    for j,i in enumerate(points):
        im=Image.frombytes('RGB',(W,H),decoded[i*stride:(i+1)*stride])
        board.paste(im.resize((280,158),Image.Resampling.LANCZOS),(j*280,v*230))
        label.text((j*280+7,v*230+163),f'frame {i} / {i/FPS:.3f} s',fill='#f0dbc1')
    label.text((7,v*230+193),row_names[v],fill='#f0dbc1')
    files.append(output)
board.save(HERE/'comparison.png')
decoded_frames=[framehash(path) for path in files]
assert [len(v) for v in decoded_frames]==[FRAMES]*3
pcm=[audiodata(path) for path in files]
assert pcm[1]==pcm[2]
offset=SKIP*RATE//FPS
peaks=[int(np.max(np.abs(np.frombuffer(row,dtype='<i2')[offset:offset+RATE//10].astype(np.int32)))) for row in pcm]
assert peaks[0]>3000 and peaks[1]<120 and peaks[2]<120
raw_diff_ab=[i for i in range(FRAMES) if frame(i,0).tobytes()!=frame(i,1).tobytes()]
raw_diff_bc=[i for i in range(FRAMES) if frame(i,1).tobytes()!=frame(i,2).tobytes()]
assert all(47<=i<58 for i in raw_diff_ab) and raw_diff_ab
assert raw_diff_bc==list(INSERT)
(HERE/'verification.json').write_text(json.dumps({'fps':FPS,'frames':FRAMES,'strike_frames':BEATS,
    'omission_frame':SKIP,'b_c_decoded_pcm_identical':pcm[1]==pcm[2],
    'omission_window_peak_pcm16':peaks,'unencoded_ab_frame_diffs':raw_diff_ab,
    'unencoded_bc_frame_diffs':raw_diff_bc,'file_sha256':{p.name:sha256(p.read_bytes()).hexdigest() for p in files},
    'audience_test':False},indent=2)+'\n',encoding='utf-8')
