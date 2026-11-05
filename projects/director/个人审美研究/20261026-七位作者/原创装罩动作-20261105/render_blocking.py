"""Original geometric motion blocking. No reference image pixels are used or edited."""
from pathlib import Path
import math,json,subprocess,hashlib,sys
from PIL import Image,ImageDraw,ImageFont
root=Path(__file__).resolve().parent
version=int(sys.argv[1]);assert version in [1,2,3,4]
out=root/f'v{version}';out.mkdir(exist_ok=True)
W,H,FPS,N=960,540,24,192
ff=root.parents[1]/'研究媒体工具/imageio-ffmpeg/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
font=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',20);small=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',16)
def lerp(a,b,u):return a+(b-a)*u
def smooth(t,a,b):
    u=max(0,min(1,(t-a)/(b-a)));return u*u*(3-2*u)
def pose(t):
    if t<1.2:old=(480,lerp(390,190,smooth(t,.4,1.2)))
    elif t<2:old=(lerp(480,220,smooth(t,1.2,2)),190)
    else:old=(220,lerp(190,420,smooth(t,2,2.4)))
    if t<3.2:new=(780,lerp(420,190,smooth(t,2.4,3.2)))
    elif t<4.3:new=(lerp(780,480,smooth(t,3.2,4.3)),190)
    else:new=(480,lerp(190,390,smooth(t,4.3,5.4)))
    # Hand endpoints follow glass during carrying; later withdraw to expose its seat.
    left=(old[0]-58,old[1]-72) if t<2.4 else (lerp(162,390,smooth(t,2.4,3)),lerp(348,398,smooth(t,2.4,3)))
    if version>=2 and t>6.15:
        target=(422,411) if version==2 else ((448,395) if version==3 else (448,375))
        left=(lerp(390,target[0],smooth(t,6.15,6.5)),lerp(398,target[1],smooth(t,6.15,6.5)))
    right=(new[0]+58,new[1]-72)
    if t>5.8:right=(lerp(538,850,smooth(t,5.8,6.4)),lerp(318,435,smooth(t,5.8,6.4)))
    light=smooth(t,6.6,7.15)
    return old,new,left,right,light
def glass(d,x,bottom,cracked=False):
    contour='#81978e';width=2
    pts=[(x-35,bottom-134),(x+35,bottom-134),(x+47,bottom-106),(x+54,bottom-66),(x+49,bottom-20),(x+35,bottom),(x-35,bottom),(x-49,bottom-20),(x-54,bottom-66),(x-47,bottom-106)]
    d.polygon(pts,fill='#d2d9c5');d.line(pts+[pts[0]],fill=contour,width=width,joint='curve')
    d.arc((x-35,bottom-141,x+35,bottom-127),0,360,fill=contour,width=width)
    d.line([(x-26,bottom-115),(x-36,bottom-80),(x-32,bottom-35)],fill='#f6f2db',width=5)
    if cracked:
        d.line([(x-22,bottom-121),(x+6,bottom-88),(x-12,bottom-67),(x+24,bottom-32),(x+11,bottom-5)],fill='#535c55',width=3)
        d.line([(x+6,bottom-88),(x+31,bottom-102)],fill='#535c55',width=2)
def hand(d,start,end,color,side):
    x,y=end;d.line([start,(lerp(start[0],x,.55),lerp(start[1],y,.45)),(x+side*19,y+10)],fill=color,width=42,joint='curve')
    d.ellipse((x-21,y-16,x+21,y+17),fill='#cc9b76',outline='#5a453a',width=2)
    # A thumb/jaw embraces the rim. This schematic does not prove human finger anatomy.
    d.arc((x-21,y-13,x+21,y+13),70,290 if side<0 else 230,fill='#73513e',width=3)
def frame(t):
    im=Image.new('RGB',(W,H),'#ded8c1');d=ImageDraw.Draw(im)
    d.rectangle((0,0,W,430),fill='#bdc1ad');d.rectangle((0,430,W,H),fill='#9f8060')
    d.line((0,430,W,430),fill='#4b4b3c',width=4)
    for x in [100,300,600,870]:d.line((x,435,x+40,540),fill='#b39570',width=2)
    old,new,left,right,light=pose(t)
    # Open assembly jig is deliberately simplified; cap/hood mechanism is outside this test.
    d.rounded_rectangle((392,385,568,435),14,fill='#545748',outline='#343d35',width=4)
    d.rectangle((414,379,546,390),fill='#3f463c');d.rectangle((476,357,484,384),fill='#453d32')
    d.line([(399,382),(399,241)],fill='#525a4a',width=9);d.line([(561,382),(561,241)],fill='#525a4a',width=9)
    if light:
        r=int(17+45*light);d.ellipse((480-r,340-r,480+r,340+r),fill='#d5b875')
    glass(d,*old,True);glass(d,*new)
    if light:
        d.polygon([(480,319-16*light),(466,357),(480,369),(494,357)],fill='#eeb94e')
        d.polygon([(480,335),(473,358),(480,364),(486,358)],fill='#fff0b1')
    d.ellipse((408,399,436,427),fill='#67624e',outline='#354137',width=3)
    angle=lerp(-.9,.9,smooth(t,6.4,6.7)) if version>=2 else -.9
    d.line([(422-10*math.cos(angle),413-10*math.sin(angle)),(422+10*math.cos(angle),413+10*math.sin(angle))],fill='#ddd0a1',width=3)
    left_anchor=(15,lerp(446,300,smooth(t,6.15,6.5))) if version==4 else (15,446)
    hand(d,left_anchor,left,'#526d68',-1);hand(d,(945,446),right,'#ae8242',1)
    if version>=3 and t>6.15:
        u=smooth(t,6.15,6.5)
        d.line([(left[0]-12,left[1]+10),(lerp(left[0]-12,430,u),lerp(left[1]+10,419,u))],fill='#cc9b76',width=9)
    # Header is audit information outside the image action area, not a caption explaining causality.
    d.rectangle((0,0,W,47),fill='#2f3833');d.text((16,10),f'原创装罩预演 V{version}    {t:04.2f}s / 8.00s    固定机位 · 简化支架 · 无声',font=font,fill='#f1ecd4')
    d.text((16,505),'模型动作测试；非真实装配、热安全、人物表演或连续看片验证',font=small,fill='#ede3c7')
    return im
video=out/'assembly.mp4';assert not video.exists()
proc=subprocess.Popen([str(ff),'-hide_banner','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-an','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p',str(video)],stdin=subprocess.PIPE)
for i in range(N):proc.stdin.write(frame(i/FPS).tobytes())
proc.stdin.close();assert proc.wait()==0
times=[0,.8,1.6,2.4,3.2,4,4.6,5.2,5.4,5.8,6.2,6.5,6.7,7.2,7.95]
for start in range(0,len(times),6):
    batch=times[start:start+6];board=Image.new('RGB',(1440,426*((len(batch)+1)//2)),'#292e2b')
    for k,t in enumerate(batch):
        im=frame(t);im.save(out/f'frame{t:g}.png');board.paste(im.resize((720,405)),(k%2*720,k//2*426+21));ImageDraw.Draw(board).text((k%2*720+8,k//2*426+2),f'{t:g}s',fill='white')
    board.save(out/f'board{start//6+1}.png')
events={'old_glass_depart':.4,'old_glass_on_table':2.4,'spare_lift':2.4,'spare_horizontal_over_lamp':4.3,'spare_seated':5.4,'right_hand_release_begin':5.8,'right_hand_clear':6.4,'knob_action':None if version==1 else [6.4,6.7],'flame_begin':6.6,'flame_established':7.15}
meta={'version':version,'construction':'original geometric shapes rendered by Python/Pillow; no input image edits','duration_seconds':8,'fps':FPS,'frames':N,'dimensions':[W,H],'audio':False,'actual_review_status':'generated, not yet reviewed','review_times':times,'events':events,'scope':'contact path and temporal causality only; open jig is not exact V5 hood mechanism','source_code':str(Path(__file__).resolve()),'bytes':video.stat().st_size,'sha256':hashlib.sha256(video.read_bytes()).hexdigest()}
(out/'metadata.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(meta,ensure_ascii=False))
