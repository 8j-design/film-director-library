from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import random,json
out=Path(__file__).resolve().parent/'tests/A02-雨后候车-20261027'
out.mkdir(parents=True,exist_ok=True)
W,H=640,420
pal=['#f7c979','#e6aac0','#b48bb4','#77658e','#f3dbab']
def scene(mode):
    im=Image.new('RGB',(W,H),'#252537');d=ImageDraw.Draw(im)
    d.rectangle((0,0,W,235),fill='#34344c')
    d.rectangle((35,60,333,236),fill='#62516a');d.rectangle((344,25,605,236),fill='#4c425b')
    d.polygon([(0,235),(640,235),(640,420),(0,420)],fill='#2b293b')
    d.polygon([(0,252),(640,233),(640,253),(0,276)],fill='#71647c')
    for x in [60,119,178,237,370,429,488,547]:
        for y in [88,146,199]:
            d.rectangle((x,y,x+28,y+24),fill='#282b3b')
    d.rectangle((178,146,206,170),fill='#e3b66c')
    d.rectangle((488,88,516,112),fill='#bd90b2')
    d.polygon([(410,230),(455,226),(455,242),(410,247)],fill='#282837')
    d.line((400,133,400,241),fill='#b6a0b0',width=3)
    d.rectangle((397,126,460,135),fill='#d7b477')
    # A puddle with separate banks and stable dark interruptions.
    d.polygon([(40,307),(280,271),(595,293),(559,386),(193,407),(42,369)],fill='#433147')
    if mode=='A':
        pass
    elif mode in ('E','F'):
        layer=Image.new('RGB',(W,H),'#433147');ld=ImageDraw.Draw(layer)
        mask=Image.new('L',(W,H),0);md=ImageDraw.Draw(mask)
        md.polygon([(40,307),(280,271),(595,293),(559,386),(193,407),(42,369)],fill=255)
        r=random.Random(72)
        for _ in range(1200):
            x=r.randrange(40,596);y=r.randrange(272,408)
            bright=abs(x-192)<10+(y-272)*.17
            pink=abs(x-502)<6+(y-272)*.12
            if not bright and not pink and r.random()<.45:continue
            color=r.choice(pal[:2]) if bright else ('#b48bb4' if pink else r.choice(['#776080','#806485','#5e526e']))
            rx=2+(y-272)/20;ry=.7+(y-272)/150
            ld.ellipse((x-rx,y-ry,x+rx,y+ry),outline=color,width=1)
        im.paste(layer,(0,0),mask);d=ImageDraw.Draw(im)
        if mode=='F':
            # Broken, low-contrast wet/dry transition, distinct from bright ripples.
            for j in range(45):
                x=55+j*11;y=306-(x-40)*.16 if x<280 else 271+(x-280)*.07
                d.line((x,y,x+7,y-1),fill='#594958',width=2)
            d.line((42,369,193,407,559,386),fill='#514052',width=2)
            # Dark occlusion below the human, interrupted by water marks.
            for yy in range(285,351,7):
                xx=301+(yy-285)*.05
                d.line((xx-4,yy,xx+8,yy),fill='#252537',width=2)
    elif mode=='B':
        r=random.Random(72)
        for _ in range(1100):
            x=r.randrange(W);y=r.randrange(H)
            d.ellipse((x-4,y-2,x+4,y+2),outline=r.choice(pal),width=1)
    else:
        r=random.Random(72)
        # Form-aware surface marks; brighter broken reflection aligned below window.
        n=580 if mode=='C' else 300
        for _ in range(n):
            x=r.randrange(43,590);y=r.randrange(278,404)
            if not (70+(404-y)*.3 < x < 570):continue
            bright=abs(x-(190+(y-280)*.23))<15+(y-275)*.17
            color=r.choice(pal[:2]) if bright else r.choice(['#776080','#806485','#5e526e'])
            if mode=='D' and not bright and r.random()<.6:continue
            rx=3+(y-275)/20;ry=.7+(y-275)/120
            d.ellipse((x-rx,y-ry,x+rx,y+ry),outline=color,width=1)
        for _ in range(100):
            x=r.randrange(40,605);y=r.randrange(40,230)
            if 333<x<344:continue
            d.line((x,y,x,y+3),fill='#7b627c',width=1)
    # Foreground human/umbrella added last, unchanged across controls.
    d.ellipse((295,198,306,210),fill='#bca5a9')
    d.polygon([(293,211),(307,211),(314,242),(289,243)],fill='#202332')
    d.line((295,242,292,260),fill='#171b2c',width=4);d.line((307,242,313,259),fill='#171b2c',width=4)
    d.pieslice((264,175,337,215),180,360,fill='#392d4a',outline='#b194a7',width=2)
    d.line((301,194,301,225),fill='#b194a7',width=2)
    if mode=='F':
        d.ellipse((283,256,317,263),fill='#1d2030')
        d.line((306,216,302,225),fill='#bca5a9',width=3)
        d.arc((299,222,307,232),0,180,fill='#b194a7',width=2)
        d.rectangle((410,154,438,180),fill='#c6acaf')
        d.line((415,160,432,160),fill='#4c425b',width=2)
        d.line((415,167,428,167),fill='#4c425b',width=2)
    return im
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',20)
labels={'A':'A | Palette only','B':'B | Uniform bright marks','C':'C | Surface marks, high density','D':'D | Selective reflection, first revision'}
ims=[]
for k in labels:
    im=scene(k);im.save(out/(k+'.png'));ims.append(im)
board=Image.new('RGB',(1280,912),'#11141c');draw=ImageDraw.Draw(board)
for idx,k in enumerate(labels):
    x=(idx%2)*640;y=(idx//2)*456
    draw.text((x+14,y+8),labels[k],font=font,fill='white')
    board.paste(ims[idx],(x,y+36))
board.save(out/'comparison.png')
scene('E').save(out/'E.png')
scene('F').save(out/'F.png')
metrics={}
for k,im in list(zip(labels,ims))+[('E',scene('E')),('F',scene('F'))]:
    pixels=list(im.crop((40,278,590,404)).get_flattened_data())
    metrics[k]={'rectangle_roi_pixels':len(pixels),'bright_pixels':sum(.2126*r+.7152*g+.0722*b>155 for r,g,b in pixels),'dark_pixels':sum(.2126*r+.7152*g+.0722*b<70 for r,g,b in pixels)}
(out/'pixel-check.json').write_text(json.dumps(metrics,indent=2),encoding='utf-8')
print(out)
print(json.dumps(metrics))
