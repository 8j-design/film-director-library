from pathlib import Path
import sys,math,subprocess,json,hashlib
from PIL import Image,ImageDraw
t=Path(__file__).resolve().parent;v=int(sys.argv[1]);assert v in [1,2,3];out=t/f'v{v}';out.mkdir();frames=out/'frames';frames.mkdir()
ff=t.parents[1]/'研究媒体工具/imageio-ffmpeg/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
W,H=768,512;S=2
def smooth(t,a,b):
    u=max(0,min(1,(t-a)/(b-a)));return u*u*(3-2*u)
def lerp(a,b,u):return a+(b-a)*u
def draw_frame(tm):
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
    line([(199,184),(209,187)],'#394b59',2);line([(206,205),(213,202)],'#9a776c',2)
    # Traveler: different shape/colour, face and gaze oriented toward the open palm.
    poly([(593,235),(660,233),(727,402),(561,404)],'#b8c7d5');poly([(601,236),(623,264),(653,237)],'#eee4cd')
    ellipse((586,155,652,238),'#e8c9b0');poly([(584,181),(589,147),(635,142),(661,167),(648,199),(640,164),(601,165)],'#76667b')
    line([(589,198),(600,200)],'#4b4a64',2);line([(588,219),(601,221)],'#a57c76',2)
    # Counter and book remain behind both hands.
    poly([(72,355),(550,355),(595,382),(58,382)],'#9c7776');poly([(58,382),(595,382),(595,474),(58,474)],'#686878')
    poly([(108,350),(215,341),(234,357),(123,369)],'#ebe1c6');line([(167,347),(179,363)],'#b09b88',2)
    # Fixed giving motion. Fingers open at release; forearm remains attached to clerk.
    give=smooth(tm,0.5,1.7);ret=smooth(tm,3.8,5.2)
    gx=lerp(330,437,give)*(1-ret)+330*ret;gy=lerp(262,225,give)*(1-ret)+262*ret
    line([(226,258),(278,285),(gx-18,gy+7)],'#46536b',26);line([(gx-18,gy+7),(gx,gy)],'#e3c0a7',17)
    ellipse((gx-6,gy-8,gx+15,gy+8),'#e3c0a7')
    opening=smooth(tm,1.85,2.08)
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
        if v==3:cx+=hx-480;cy+=hy-335
    ellipse((cx-11,cy-11,cx+11,cy+11),'#d0a157');ellipse((cx-6,cy-7,cx+6,cy+5),'#edd08b');line([(cx-4,cy),(cx+4,cy)],'#ae7d4d',2)
    if v==3 and tm>=2.45:
        close=smooth(tm,2.45,2.65)
        for z in range(2):line([(hx-13+z*10,hy-3),(hx-15+z*10,hy-6-12*close)],'#e8c9b0',6)
    line([(40,477),(740,477)],'#b9b0aa',1)
    return im.resize((W,H),Image.Resampling.LANCZOS)
for n in range(192):draw_frame(n/24).save(frames/f'{n:04d}.png')
subprocess.run([str(ff),'-hide_banner','-loglevel','error','-framerate','24','-i',str(frames/'%04d.png'),'-c:v','libx264','-crf','20','-pix_fmt','yuv420p',str(out/'找零.mp4')],check=True)
# Read back encoded output, not just the pre-encoding images.
check=out/'decoded';check.mkdir();subprocess.run([str(ff),'-hide_banner','-loglevel','error','-i',str(out/'找零.mp4'),'-vsync','0',str(check/'%04d.png')],check=True)
files=sorted(check.glob('*.png'));assert len(files)==192
times=[0,1.5,2,2.42,2.65,3.5,4.6,7.9];board=Image.new('RGB',(1536,536*4),'#202020');dd=ImageDraw.Draw(board)
for k,z in enumerate(times):
    idx=round(z*24);x=k%2*768;y=k//2*536;board.paste(Image.open(files[idx]),(x,y+24));dd.text((x+7,y+5),f'V{v} decoded frame {idx}, {idx/24:.3f}s',fill='white')
board.save(out/'关键时刻.png')
j={'version':v,'duration_seconds':8,'fps':24,'dimensions':[W,H],'decoded_frames':len(files),'selected_decoded_frames':[round(z*24) for z in times],'selected_board_actually_viewed':False,'audio':False,'art_origin':'original code-drawn flat illustration, not extracted from reference','full_audiovisual_verified':False,'sha256':hashlib.sha256((out/'找零.mp4').read_bytes()).hexdigest()}
(out/'metadata.json').write_text(json.dumps(j,ensure_ascii=False,indent=2),encoding='utf-8');print(j)
