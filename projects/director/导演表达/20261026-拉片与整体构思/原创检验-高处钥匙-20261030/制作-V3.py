from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import math, subprocess, json, sys

ROOT=Path(__file__).parent
FF=Path('C:/Users/scvfv/Documents/ChatGPT/导演/新工作/研究媒体工具/imageio-ffmpeg/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe')
W,H,FPS=960,640,12
BG='#172738'; DECK='#82909c'; BLUE='#6cb6d6'; RED='#ef8d74'; GOLD='#ffe38b'
def mix(a,b,u):
    u=max(0,min(1,u)); return a+(b-a)*u
def lerp(a,b,u): return tuple(mix(x,y,u) for x,y in zip(a,b))
def smooth(u):
    u=max(0,min(1,u)); return u*u*(3-2*u)
def line(d,pts,col,w): d.line(pts,fill=col,width=w,joint='curve')
def dot(d,p,r,c,outline=None): d.ellipse((p[0]-r,p[1]-r,p[0]+r,p[1]+r),fill=c,outline=outline,width=2)
def limb(d,a,b,col,w,bend=1):
    dx,dy=b[0]-a[0],b[1]-a[1]; dist=math.hypot(dx,dy) or 1
    m=((a[0]+b[0])/2-bend*dy/dist*13,(a[1]+b[1])/2+bend*dx/dist*13)
    line(d,[a,m,b],col,w); dot(d,m,w/2,col); return m
def eye(d,head,target,r):
    dx,dy=target[0]-head[0],target[1]-head[1]; n=math.hypot(dx,dy) or 1
    p=(head[0]+dx/n*r*.56,head[1]+dy/n*r*.40)
    dot(d,p,3,'#152536')
def facing(d,head,target,r,color):
    dx,dy=target[0]-head[0],target[1]-head[1]; n=math.hypot(dx,dy) or 1
    ux,uy=dx/n,dy/n; px,py=-uy,ux
    dot(d,head,r,color)
    # Nose contour and visible white/pupil provide an actual directional silhouette.
    tip=(head[0]+ux*r*1.22,head[1]+uy*r*1.22)
    b=(head[0]+ux*r*.78,head[1]+uy*r*.78)
    d.polygon([(b[0]+px*5,b[1]+py*5),tip,(b[0]-px*5,b[1]-py*5)],fill=color)
    ep=(head[0]+ux*r*.46,head[1]+uy*r*.46)
    dot(d,ep,5.5,'#f1eee0');dot(d,(ep[0]+ux*2,ep[1]+uy*2),3.2,'#122333')
def key(d,p,scale=1):
    x,y=p; r=5*scale
    d.ellipse((x-r,y-r,x+r,y+r),outline=GOLD,width=max(2,int(3*scale)))
    line(d,[(x,y+r),(x,y+17*scale),(x+7*scale,y+17*scale)],GOLD,max(2,int(3*scale)))
    line(d,[(x+4*scale,y+12*scale),(x+4*scale,y+17*scale)],GOLD,max(2,int(3*scale)))

def state(t,v):
    if v==3:
        if t<3: x=700
        elif t<5: x=mix(700,568,smooth((t-3)/2))
        elif t<9.1: x=568
        else: x=mix(568,1010,smooth((t-9.1)/3.7))
        rest=(x-15,238)
        if t<5: ch=rest
        elif t<5.5: ch=lerp(rest,(535,236),smooth((t-5)/.5))
        elif t<5.9: ch=(535,236)
        elif t<6.3: ch=lerp((535,236),(555,240),smooth((t-5.9)/.4))
        elif t<6.9: ch=(555,240)
        elif t<7.6: ch=lerp((555,240),(520,224),smooth((t-6.9)/.7))
        else: ch=(520,224)
        if t<7.6: kp=(520,224)
        elif t<8.8: kp=(520,224-26*smooth((t-7.6)/1.2));ch=kp
        elif t<9.1: kp=lerp((520,198),(548,214),smooth((t-8.8)/.3));ch=kp
        else: kp=(x-20,214);ch=kp
        return x,ch,kp,t>=7.6,8.8,9.1,16
    # Main timing is stable except V2's added contact / removal dwell.
    grab=7.0 if v==1 else 7.0
    release=7.1 if v==1 else 8.2
    exit_start=7.2 if v==1 else 8.5
    end=14 if v==1 else 16
    if t<2.8: x=700
    elif t<4.8: x=mix(700,610,smooth((t-2.8)/2))
    elif t<5.5: x=mix(610,596,math.sin((t-4.8)/.7*math.pi))
    elif t<6.8: x=mix(610,568,smooth((t-5.5)/1.3))
    elif t<exit_start: x=568
    else: x=mix(568,936 if v==1 else 1010,smooth((t-exit_start)/3.7))
    reach=smooth((t-6.4)/.6)
    ch=lerp((x-9,237),(520,224),reach) if t<exit_start else (x-20,214)
    if t<grab: kp=(520,224)
    elif t<release:
        # V1 transfers at almost one frame; V2 holds contact then visibly lifts free.
        u=smooth((t-grab)/(release-grab)); kp=(520,224-26*u); ch=kp
    elif t<exit_start:
        kp=(520,198) if v==1 else lerp((520,198),(548,214),smooth((t-release)/(exit_start-release)))
        ch=kp
    else: kp=(x-20,214); ch=kp
    has=t>=grab
    return x,ch,kp,has,release,exit_start,end

def render(t,v):
    im=Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(im)
    # High structure: uninterrupted long drop, raised deck, base below frame edge.
    for y in (120,350,570): line(d,[(0,y),(W,y)],'#203449',1)
    for x in (575,870):
        d.rectangle((x,260,x+15,640),fill='#435565')
    line(d,[(590,600),(870,310)],'#354a5d',9)
    deck_end=930 if v==1 else 960
    d.rectangle((540,260,deck_end,278),fill=DECK)
    line(d,[(540,260),(deck_end,260)],'#d2d8da',3)
    for y in range(270,640,40): line(d,[(420,y),(470,y)],'#abb9bb',8)
    line(d,[(420,235),(420,640)],'#6b8796',10);line(d,[(470,235),(470,640)],'#6b8796',10)
    # Hook is outside the deck edge; neither hand crosses through the platform.
    line(d,[(556,260),(556,193),(520,193),(520,210)],'#bdc7c6',5)
    d.arc((514,203,526,217),0,180,fill='#bdc7c6',width=4)
    # Simple far-side access gate and clear passage.
    line(d,[(884,155),(884,260)],'#718592',7)
    d.rectangle((882,145,936,155),fill='#718592')
    x,ch,kp,has,release,es,end=state(t,v)
    # Adult stays supported; after loss, free hand returns, body descends a rung.
    retreat=smooth((t-(11.5 if v==3 else es+.8))/1.0)
    # V2 rejects V1's simultaneous sliding descent: stay on the same holds.
    descend=smooth((t-(es+2.0))/1.0)*40 if v==1 else 0
    hip=(441,427+descend); shoulder=(448,351+descend); head=(440,318+descend)
    left=(420,(310 if v==1 else 292)+descend)
    # Foot contact occurs on rung centers and shifts only after regrip.
    lf=(420,510+descend);rf=(470,470+descend)
    limb(d,hip,lf,BLUE,16,-1);limb(d,hip,rf,BLUE,16,1)
    line(d,[(414,lf[1]),(435,lf[1])],'#b9e1e8',8)
    line(d,[(459,rf[1]),(479,rf[1])],'#b9e1e8',8)
    d.polygon([(421,350+descend),(464,350+descend),(458,429+descend),(426,429+descend)],fill=BLUE)
    limb(d,(425,358+descend),left,BLUE,13,1)
    dot(d,left,7,'#d8e3df');line(d,[(416,left[1]-5),(424,left[1]-5),(424,left[1]+4)],'#203449',2)
    reach=smooth((t-.6)/1.4)
    free=lerp((470,392),(510,249) if v==1 else (500,260),reach)
    free=lerp(free,(470,333),retreat); free=(free[0],free[1]+descend)
    limb(d,shoulder,free,BLUE,13,-1);dot(d,free,6,'#d8e3df')
    if retreat<.8:
        line(d,[(free[0]-2,free[1]-4),(free[0]+6,free[1]-9)],'#d8e3df',3)
    else:
        line(d,[(466,free[1]-5),(474,free[1]-5),(474,free[1]+5)],'#203449',2)
    target=(520,224) if t<es else (x,200)
    if v==3:
        target=kp if t<11.2 else free
        head=(440+3*smooth((t-9)/1.5),318+6*smooth((t-11.2)/.5))
        facing(d,head,target,25,BLUE)
    else:
        dot(d,head,23,BLUE);eye(d,head,target,23)
    # Small figure can step across the upper platform without using a supporting hand.
    walk=((3<t<5) or t>es) if v==3 else ((2.8<t<4.8) or (5.5<t<6.8) or t>es)
    stride=math.sin(t*11)*10 if walk else 0
    head2=(x,184); hip2=(x,228)
    limb(d,hip2,(x-10+stride,257),RED,10,-1)
    limb(d,hip2,(x+10-stride,257),RED,10,1)
    d.polygon([(x-12,203),(x+12,203),(x+13,231),(x-13,231)],fill=RED)
    # Before takeover, a probing hand pauses toward key while gaze alternates down / target.
    other=(x+15,234)
    limb(d,(x+10,208),other,RED,8,1)
    if t<6.4 and v!=3: ch=(x-17,233)
    limb(d,(x-10,208),ch,RED,8,-1);dot(d,ch,5,'#ffcab2')
    dot(d,head2,16,RED)
    if t<1.4: look=(440,318)
    elif t<2.3: look=(520,224)
    elif t<3: look=(440,318)
    elif t<es: look=(520,224)
    else: look=(936,210)
    if v==3:
        if t<1.8: look=(500,260)
        elif t<5.9: look=(520,224)
        elif t<6.9: look=(500,260)
        elif t<es: look=kp
        else: look=(1010,184)
        # Downward checking lowers the head; target-facing raises/leans it forward.
        check=t<1.8 or 5.9<=t<6.9
        head2=(x-3,189) if check else ((x-4,181) if t<es else (x+3,182))
        facing(d,head2,look,20,RED)
    else: eye(d,head2,look,16)
    # Key overlays gripping hand so ownership can be followed.
    key(d,kp,1 if v==1 else 1.6)
    # Minimal presentation label and time; no action/meaning subtitles.
    d.text((22,20),f'HIGH KEY / V{v} / silent action rough',fill='#b6c7d0')
    d.text((22,40),f'{t:04.1f}s',fill='#8298a8')
    return im

def make(v):
    folder=ROOT/f'V{v}-frames';folder.mkdir(exist_ok=True)
    dur=14 if v==1 else 16
    for i in range(dur*FPS): render(i/FPS,v).save(folder/f'{i:04}.png')
    subprocess.run([str(FF),'-y','-loglevel','error','-framerate',str(FPS),'-i',str(folder/'%04d.png'),'-c:v','libx264','-pix_fmt','yuv420p','-movflags','+faststart',str(ROOT/f'V{v}.mp4')],check=True)
    # Decode from encoded mp4, not from the source PNG sequence.
    dec=ROOT/f'V{v}-decoded';dec.mkdir(exist_ok=True)
    times=[0,1.8,3.8,5.1,6.6,7.0,7.3,7.8,8.2,8.6,10,12,13.5] if v==1 else ([0,2.3,5.6,6.5,7.4,8.3,10.2,11.6,14] if v==3 else [0,1.8,3.8,5.1,6.6,7,7.3,7.8,8.2,8.6,10,12,14,15.5])
    frames=[]
    font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',18)
    for j,tm in enumerate(times):
        out=dec/f'{tm:04.1f}s.png'
        subprocess.run([str(FF),'-y','-loglevel','error','-ss',str(tm),'-i',str(ROOT/f'V{v}.mp4'),'-frames:v','1',str(out)],check=True)
        small=Image.open(out).resize((480,320)); sd=ImageDraw.Draw(small)
        sd.rectangle((0,0,65,25),fill='#111111');sd.text((5,2),f'{tm:.1f}s',font=font,fill='white')
        frames.append(small)
    sheet=Image.new('RGB',(480*3,345*math.ceil(len(frames)/3)),'#101b26')
    for j,im in enumerate(frames): sheet.paste(im,((j%3)*480,(j//3)*345))
    sheet.save(ROOT/f'V{v}-decoded-contact.png')
    (ROOT/f'V{v}-technical.json').write_text(json.dumps({'fps':FPS,'frames':dur*FPS,'duration_seconds':dur,'size':[W,H],'silent':True,'decoded_times':times,'scope':'technical properties, not artistic validation'},indent=2),encoding='utf-8')
if __name__=='__main__': make(int(sys.argv[1]))
