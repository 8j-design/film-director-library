from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageChops
import json, hashlib, sys

OUT = Path(__file__).resolve().parent
VERSION = sys.argv[1] if len(sys.argv)>1 else 'v1'
REVISION = VERSION in ('v2','v3')
if REVISION:
    OUT=OUT/VERSION
    OUT.mkdir(exist_ok=True)
FONT = 'C:/Windows/Fonts/msyh.ttc'
BG = '#d9dedb'
INK = '#273d46'

def scene(n, keyword_size):
    im = Image.new('RGB', (960, 540), BG)
    d = ImageDraw.Draw(im)
    def txt(x,y,s,size=22,fill=INK):
        d.text((x,y),s,font=ImageFont.truetype(FONT,size),fill=fill)
    def person(x,y,scale=1,look=False,color='#758a93',direction=1):
        r=int(26*scale)
        d.ellipse((x-r,y-r,x+r,y+r),fill='#cdb8a0',outline=INK,width=2)
        d.polygon([(x-r,y+r),(x+r,y+r),(x+int(45*scale),y+int(140*scale)),(x-int(40*scale),y+int(140*scale))],fill=color)
        ex=x+int((10 if look else 3)*scale)*direction
        d.ellipse((ex-3,y-3,ex+3,y+3),fill=INK)
        if REVISION:
            nx=x+direction*r
            d.polygon([(nx,y-7),(nx+direction*int(9*scale),y+5),(nx,y+10)],fill='#cdb8a0',outline=INK)
            if color=='#a5877b':
                d.line((x-r,y+r,x+r,y+r),fill='#b9d4cb',width=max(3,int(8*scale)))
    if n==0:
        d.rectangle((0,0,960,540),fill='#354850')
        d.rounded_rectangle((295,35,665,510),radius=20,fill='#edece5',outline='#1b2d36',width=7)
        txt(335,68,'未知联系人',27)
        d.line((320,118,640,118),fill='#c4ccc7',width=2)
        txt(325,160,'你的第三张画，',29)
        txt(325,205,'今天换了颜色。',29)
        txt(325,340,'你怎么知道？',26)
        txt(325,440,'未发送',17,fill='#7c8a8b')
        if REVISION:
            d.polygon([(610,540),(695,540),(660,445),(615,455)],fill='#a5877b')
            d.rounded_rectangle((612,421,655,478),radius=13,fill='#cdb8a0',outline=INK,width=2)
            d.line((616,482,667,469),fill='#b9d4cb',width=8)
    elif n==1:
        d.rectangle((0,0,960,70),fill=INK)
        d.rectangle((135,115,775,380),fill='#eee9d5',outline=INK,width=3)
        txt(170,135,'城市艺术周',22)
        # In the A/B pair, this font size is the sole rendered difference.
        txt(170,190,'在线画展',keyword_size)
        txt(170,280,'周三更新  /  作品与生活',19)
        d.line((40,0,40,540),fill='#8e9b9b',width=16)
        d.polygon([(710,0),(760,0),(750,160),(720,160)],outline=INK,width=5)
        d.ellipse((703,130,770,192),outline=INK,width=8)
        person(855,382,.8,REVISION,color='#a5877b' if REVISION else '#758a93',direction=-1 if REVISION else 1)
        d.rectangle((0,470,960,540),fill='#8e9c9c')
    elif n==2:
        d.rectangle((70,55,575,440),fill='#a7b8b6',outline=INK,width=5)
        d.line((325,55,325,440),fill=INK,width=5)
        person(650,235,1.25,True,color='#a5877b')
        d.line((680,360,760,348),fill=INK,width=16)
        d.rectangle((739,305,785,365),fill='#edece5',outline=INK,width=3)
        d.rectangle((0,455,960,540),fill='#8c9999')
        if VERSION=='v3':
            # A common insert replaces the ambiguous crowd inference.
            d.rectangle((0,0,960,540),fill='#354850')
            d.rounded_rectangle((230,25,730,520),radius=20,fill='#edece5',outline=INK,width=7)
            txt(260,48,'城市艺术周 / 在线画展',26)
            txt(260,104,'小禾 · 第3幅',28)
            d.rectangle((275,162,685,365),fill='#cfd8b8',outline=INK,width=2)
            d.ellipse((350,193,430,273),fill='#d09b78')
            d.polygon([(490,330),(600,182),(646,330)],fill='#768db4')
            txt(260,389,'今天 10:16 更新',25)
            txt(260,448,'公开作品',21)
            d.polygon([(650,540),(780,540),(730,465),(675,478)],fill='#a5877b')
            d.line((675,496,736,487),fill='#b9d4cb',width=8)
    else:
        d.rectangle((80,55,885,340),fill='#a7b8b6',outline=INK,width=6)
        for x in [120,420,750]:
            d.line((x,0,x,500),fill='#809392',width=8)
        person(235,228,1.2,False,color='#a5877b')
        person(510,230,1.15,False,color='#7b859a')
        person(785,198,1.25,False,color='#737f74')
        d.rectangle((455,275,560,340),fill='#d2cfbc',outline=INK,width=3)
        d.rectangle((0,480,960,540),fill='#8c9999')
        if VERSION=='v3':
            d.rectangle((0,0,960,540),fill='#a7b8b6')
            d.rectangle((60,45,520,420),outline=INK,width=5)
            person(670,210,1.7,True,color='#a5877b')
            d.line((700,380,775,368),fill=INK,width=14)
            d.rectangle((750,318,802,382),fill='#edece5',outline=INK,width=3)
            txt(95,465,'',20)
    return im

frames = {}
for variant,size in [('A',12),('B',42)]:
    frames[variant]=[scene(n,size) for n in range(4)]
    for n,im in enumerate(frames[variant]):
        im.save(OUT/f'{variant}-{n+1}.png')
    frames[variant][0].save(OUT/f'{variant}.gif',save_all=True,append_images=frames[variant][1:],duration=[3000]*4,loop=0,optimize=False)

sheet=Image.new('RGB',(960,1180),'#f6f4ec')
sd=ImageDraw.Draw(sheet)
for row,v in enumerate(['A','B']):
    sd.text((10,row*590+10),v,font=ImageFont.truetype(FONT,24),fill=INK)
    for j,im in enumerate(frames[v]):
        x=(j%2)*480;y=row*590+40+(j//2)*270
        sheet.paste(im.resize((480,270)),(x,y))
sheet.save(OUT/'两版分镜.png')

checks = {'dimensions':[960,540], 'durations_ms':[3000]*4,'sound':'none','scope':'schematic original animatic, not final art or audience validation','differences':[]}
for n in range(4):
    diff=ImageChops.difference(frames['A'][n],frames['B'][n])
    checks['differences'].append({'shot':n+1,'bbox':diff.getbbox()})
assert all(checks['differences'][n]['bbox'] is None for n in [0,2,3])
b=checks['differences'][1]['bbox']
assert b and b[0]>=170 and b[1]>=190 and b[2]<=390 and b[3]<=255
checks['sha256']={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(OUT.glob('*.gif'))}
(OUT/'变量与媒体核对.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(checks,ensure_ascii=False))
