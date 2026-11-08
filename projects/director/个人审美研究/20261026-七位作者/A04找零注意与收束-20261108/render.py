from pathlib import Path
from hashlib import sha256
import json
import os
import shutil
import subprocess
from PIL import Image, ImageDraw

HERE=Path(__file__).resolve().parent
REFERENCE=HERE.parent/'原创找零-20261106/v3/找零.mp4'
LOCAL_FFMPEG=HERE.parent.parent/'研究媒体工具/imageio-ffmpeg/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
FFMPEG=os.environ.get('FFMPEG') or (str(LOCAL_FFMPEG) if LOCAL_FFMPEG.is_file() else shutil.which('ffmpeg'))
W,H,S,FPS,COUNT=768,512,2,24,192

def smooth(t,a,b):
    u=max(0,min(1,(t-a)/(b-a)));return u*u*(3-2*u)
def lerp(a,b,u):return a+(b-a)*u
def draw_frame(tm, v):
    im=Image.new('RGB',(W*S,H*S),'#ece6d3');d=ImageDraw.Draw(im)
    def poly(p,c):d.polygon([(int(x*S),int(y*S)) for x,y in p],fill=c)
    def line(p,c,w=2):d.line([(int(x*S),int(y*S)) for x,y in p],fill=c,width=int(w*S),joint='curve')
    def ellipse(box,c):d.ellipse(tuple(int(z*S) for z in box),fill=c)
    def rr(box,c,r=5):d.rounded_rectangle(tuple(int(z*S) for z in box),radius=r*S,fill=c)
    # Original flat colour illustration; no copied bitmap or third-party asset.
    poly([(250,90),(768,64),(768,360),(250,360)],'#c0d3cd')
    for k in range(12):
        y=250+k*8;line([(260,y),(760,y-4)],'#a6c3c0',1)
    poly([(510,250),(705,250),(677,278),(540,278)],'#627d89');line([(616,170),(616,250)],'#627d89',3)
    poly([(620,180),(665,239),(620,239)],'#ede7d9')
    for x in [290,330,730]:line([(x,150),(x,320)],'#93adaa',3)
    rr((40,65,290,390),'#788b89',3);rr((61,90,270,330),'#d3d6bc',2)
    # Boat pictogram and clerk's ledger establish a ticket window without explanatory dialogue.
    rr((77,107,124,148),'#e9e1c8',2);poly([(83,131),(117,131),(109,140),(91,140)],'#526c80');line([(100,113),(100,132)],'#526c80',2)
    # Clerk: grown adult, dark coat, face turned toward the transaction.
    poly([(144,221),(221,219),(266,365),(112,365)],'#46536b');poly([(174,222),(190,248),(203,219)],'#e8d7c5')
    ellipse((148,143,217,225),'#e3c0a7');ellipse((143,134,210,180),'#4c626b');poly([(176,136),(216,162),(207,184),(195,157)],'#4c626b')
    gaze_hand=smooth(tm,0.75,1.25)*(1-smooth(tm,3.2,3.65)) if v>=4 else 0
    gaze_ledger=smooth(tm,5.2,5.9) if v==5 else 0
    line([(199,184),(209,187)],'#394b59',2)
    if gaze_hand or gaze_ledger:
        ex=205+3*gaze_hand-4*gaze_ledger
        ey=187+2*gaze_hand+4*gaze_ledger
        ellipse((ex-1.8,ey-1.8,ex+1.8,ey+1.8),'#242b37')
    line([(206,205),(213,202)],'#9a776c',2)
    # Traveler: different shape/colour, face and gaze oriented toward the open palm.
    poly([(593,235),(660,233),(727,402),(561,404)],'#b8c7d5');poly([(601,236),(623,264),(653,237)],'#eee4cd')
    ellipse((586,155,652,238),'#e8c9b0');poly([(584,181),(589,147),(635,142),(661,167),(648,199),(640,164),(601,165)],'#76667b')
    line([(589,198),(600,200)],'#4b4a64',2)
    if gaze_hand:
        ex=596-3*gaze_hand
        ey=200+3*gaze_hand
        ellipse((ex-1.8,ey-1.8,ex+1.8,ey+1.8),'#283446')
    line([(588,219),(601,221)],'#a57c76',2)
    # Counter and book remain behind both hands.
    poly([(72,355),(550,355),(595,382),(58,382)],'#9c7776');poly([(58,382),(595,382),(595,474),(58,474)],'#686878')
    poly([(108,350),(215,341),(234,357),(123,369)],'#ebe1c6');line([(167,347),(179,363)],'#b09b88',2)
    # Fixed giving motion. Fingers open at release; forearm remains attached to clerk.
    give=smooth(tm,0.5,1.7);ret=smooth(tm,3.8,5.2)
    gx=lerp(330,437,give)*(1-ret)+330*ret;gy=lerp(262,225,give)*(1-ret)+262*ret
    at_book=smooth(tm,5.25,6.55) if v==5 else 0
    gx=lerp(gx,188,at_book)
    gy=lerp(gy,347,at_book)
    elbow=(lerp(278,216,at_book),lerp(285,300,at_book))
    palm=(gx-18+25*at_book,gy+7-21*at_book)
    line([(226,258),elbow,palm],'#46536b',26)
    line([palm,(gx,gy)],'#e3c0a7',17)
    ellipse((gx-6,gy-8,gx+15,gy+8),'#e3c0a7')
    opening=smooth(tm,1.85,2.08)
    if at_book:
        for finger in range(3):
            x=gx-8+finger*6
            line([(x,gy-1),(x-5,gy+5+4*at_book)],'#e3c0a7',4)
    else:
        line([(gx+7,gy-2),(gx+17,gy-10-8*opening)],'#e3c0a7',6)
    # V1: receiver starts too late. V2: arrive before fall. V3 also parents coin to the receiving hand after contact.
    ready=smooth(tm,1.8 if v==1 else 0.85,2.8 if v==1 else 1.65)
    back=smooth(tm,3.1,4.6)
    hx=lerp(645,480,ready)+95*back;hy=lerp(407,335,ready)+40*back
    line([(636,274),(615,354),(hx+49,hy+14)],'#b8c7d5',31);line([(hx+49,hy+14),(hx+18,hy+3)],'#e8c9b0',18)
    ellipse((hx-23,hy-10,hx+26,hy+10),'#e8c9b0')
    for z in range(3):line([(hx-15+z*7,hy-4),(hx-27+z*7,hy-16)],'#e8c9b0',5)
    # Coin has one release/fall path across versions.
    if tm<2:
        cx,cy=gx+7,gy+14
    elif tm<2.45:
        u=(tm-2)/.45;cx=lerp(444,470,u);cy=239+81*u*u
    else:
        cx,cy=470,320
        if v>=3:cx+=hx-480;cy+=hy-335
    ellipse((cx-11,cy-11,cx+11,cy+11),'#d0a157');ellipse((cx-6,cy-7,cx+6,cy+5),'#edd08b');line([(cx-4,cy),(cx+4,cy)],'#ae7d4d',2)
    if v>=3 and tm>=2.45:
        close=smooth(tm,2.45,2.65)
        for z in range(2):line([(hx-13+z*10,hy-3),(hx-15+z*10,hy-6-12*close)],'#e8c9b0',6)
    line([(40,477),(740,477)],'#b9b0aa',1)
    return im.resize((W,H),Image.Resampling.LANCZOS)

def ffmpeg(*args,data=None):
    return subprocess.check_output([FFMPEG,'-v','error',*map(str,args)],input=data)

def samples(path,points):
    select='select='+ '+'.join(r'eq(n\,'+str(i)+')' for i in points)
    rgb=ffmpeg('-i',path,'-vf',select,'-fps_mode','passthrough','-pix_fmt','rgb24','-f','rawvideo','-')
    stride=W*H*3
    assert len(rgb)==len(points)*stride
    return [Image.frombytes('RGB',(W,H),rgb[j*stride:(j+1)*stride]) for j in range(len(points))]

def main():
    assert FFMPEG and REFERENCE.is_file()
    before=[draw_frame(i/FPS,3).tobytes() for i in range(COUNT)]
    files=[REFERENCE]
    versions={}
    for v in (4,5):
        next_path=HERE/f'v{v}-ferry-change.mp4'
        frames=[draw_frame(i/FPS,v).tobytes() for i in range(COUNT)]
        if v==4:
            changes=[i for i in range(COUNT) if frames[i]!=before[i]]
            assert changes and all(.75<i/FPS<3.65 for i in changes)
        else:
            changes=[i for i in range(COUNT) if frames[i]!=before[i]]
            assert changes and all(i/FPS>5.2 for i in changes)
        before=frames
        ffmpeg('-y','-f','rawvideo','-pix_fmt','rgb24','-video_size',f'{W}x{H}','-framerate',FPS,'-i','-',
               '-c:v','libx264','-crf',20,'-pix_fmt','yuv420p','-movflags','+faststart',next_path,data=b''.join(frames))
        decoded=ffmpeg('-i',next_path,'-map','0:v:0','-f','framemd5','-').decode()
        assert sum(not line.startswith('#') for line in decoded.splitlines())==COUNT
        versions[str(v)]={'diff_from_previous_unencoded_frames':changes,'frames':COUNT,
                          'sha256':sha256(next_path.read_bytes()).hexdigest()}
        files.append(next_path)
    points=[28,57,95,151,178]
    size=(320,220)
    board=Image.new('RGB',(size[0]*len(points),size[1]*len(files)),'#283346')
    label=ImageDraw.Draw(board)
    for row,path in enumerate(files):
        for col,im in enumerate(samples(path,points)):
            board.paste(im.resize((320,192),Image.Resampling.LANCZOS),(col*320,row*220))
            label.text((col*320+8,row*220+197),f'V{row+3} | frame {points[col]} | {points[col]/FPS:.2f}s',fill='#f4e2c3')
    board.save(HERE/'comparison.png')
    (HERE/'verification.json').write_text(json.dumps({'points':points,'duration_s':COUNT/FPS,'fps':FPS,
        'reference_sha256':sha256(REFERENCE.read_bytes()).hexdigest(),'new_versions':versions,'audio':False,
        'audience_test':False},indent=2)+'\n',encoding='utf-8')

if __name__=='__main__':
    main()
