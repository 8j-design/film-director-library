"""Original schematic blocking experiment, not a character-art generator."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json
import math

TASK = Path(__file__).resolve().parent
BATCH = TASK
MEDIA = TASK / 'rendered'
BATCH.mkdir(parents=True, exist_ok=True)
MEDIA.mkdir(exist_ok=True)
FONT = 'C:/Windows/Fonts/msyh.ttc'
SPEC = {
    'duration':10, 'fps':8, 'canvas':[900,520],
    'variants':{
        'X':{'withdraw':3.0,'door_gaze':False,'label':'X · 同步起动'},
        'Y':{'withdraw':4.7,'door_gaze':False,'label':'Y · 错开起动'},
        'Z':{'withdraw':4.7,'door_gaze':True,'label':'Y′ · 同时序，注视门口'},
    },
    'paper':[443,273,97,25], 'chen_block':[3.0,4.0],
    'reach':[0.5,2.0], 'withdraw_duration':1.3,
    'purpose':'比较同一清桌动作中的反应相位与注视目标；不预设优胜版本',
}
(BATCH/'scene.json').write_text(json.dumps(SPEC,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def phase(t,a,b):
    u=max(0,min(1,(t-a)/(b-a)))
    return u*u*(3-2*u)

def mix(a,b,u):
    return [a[0]+(b[0]-a[0])*u,a[1]+(b[1]-a[1])*u]

def state(t,key):
    v=SPEC['variants'][key]
    reach=phase(t,*SPEC['reach'])
    withdraw=phase(t,v['withdraw'],v['withdraw']+SPEC['withdraw_duration'])
    hand=mix([633,340],[535,278],reach*(1-withdraw))
    block=mix([303,346],[473,284],phase(t,*SPEC['chen_block']))
    # Gaze targets are displayed as eye direction, never as intent labels.
    chen_gaze=hand if 1.4<t<6.3 else [401,282]
    meng_gaze=[830,200] if v['door_gaze'] else ([470,282] if t<4 else [310,177])
    return {'t':round(t,3),'variant':key,'chen_hand':block,'meng_hand':hand,
            'chen_gaze':chen_gaze,'meng_gaze':meng_gaze,'paper':SPEC['paper']}

def paint(t,key,review=False):
    im=Image.new('RGB',(900,520),'#f4f1e9')
    d=ImageDraw.Draw(im)
    ft=ImageFont.truetype(FONT,19)
    small=ImageFont.truetype(FONT,15)
    line='#363d42'; c='#486674'; m='#916548'
    d.line((50,434,850,434),fill='#c6c5bd',width=2)
    d.rectangle((780,100,848,434),outline='#babbb5',width=2)
    d.ellipse((789,263,795,269),fill='#aaa99f')
    # Work surface and paper are unchanged in all versions.
    d.polygon([(350,300),(569,300),(600,316),(330,316)],fill='#bcb7a9',outline=line)
    d.line((350,316,350,434),fill=line,width=8)
    d.line((578,316,578,434),fill=line,width=8)
    d.rectangle((365,284,431,291),fill='#6d7c73')
    d.line((373,287,427,287),fill='#e4e5d7',width=1)
    paper=SPEC['paper']
    d.polygon([(443,273),(537,273),(540,298),(447,298)],fill='#ece3c6',outline=line)
    d.arc((455,276,509,300),185,335,fill='#9b8a69',width=2)
    s=state(t,key)

    def elbow_for(shoulder,hand,length=90,side=-1):
        dx,dy=hand[0]-shoulder[0],hand[1]-shoulder[1]
        dist=max(0.001,math.hypot(dx,dy))
        assert dist < length*2, 'Target outside schematic arm reach'
        h=math.sqrt(length*length-dist*dist/4)
        return [shoulder[0]+dx/2-side*dy/dist*h,shoulder[1]+dy/2+side*dx/dist*h]

    def person(x,col,active,other,elbow,gaze,who):
        # The neutral figures are spatial markers, not approved character designs.
        d.line((x-15,355,x-28,430),fill=col,width=14)
        d.line((x+15,355,x+27,430),fill=col,width=14)
        d.line((x-35,430,x-7,430),fill=line,width=5)
        d.line((x+17,430,x+42,430),fill=line,width=5)
        d.rounded_rectangle((x-30,239,x+30,359),radius=18,fill=col)
        d.line((x,225,x,244),fill=col,width=17)
        d.ellipse((x-34,146,x+34,226),fill='#dfc8a6',outline=line,width=2)
        for ex in (x-13,x+13):
            ey=184
            d.ellipse((ex-9,ey-7,ex+9,ey+7),fill='#fffdf7',outline=line,width=1)
            dx,dy=gaze[0]-x,gaze[1]-184
            length=max(1,math.hypot(dx,dy))
            px,py=ex+5*dx/length,ey+3*dy/length
            d.ellipse((px-3,py-3,px+3,py+3),fill=line)
        d.line((x-8,210,x+8,210),fill=line,width=2)
        active_shoulder=[x+20 if who=='陈' else x-20,250]
        other_shoulder=[x-20 if who=='陈' else x+20,250]
        bend=1 if who=='陈' else -1
        other_elbow=elbow_for(other_shoulder,other[1],80,bend)
        elbow=elbow_for(active_shoulder,active,90,bend)
        d.line([other_shoulder,other_elbow,other[1]],fill=col,width=13,joint='curve')
        if who=='孟':
            ox,oy=other[1]
            for shift in (6,3,0):
                d.polygon([(ox-17,oy-17+shift),(ox+28,oy-17+shift),(ox+33,oy+6+shift),(ox-12,oy+6+shift)],fill='#f2e9d2',outline=line)
        d.ellipse((other[1][0]-9,other[1][1]-7,other[1][0]+9,other[1][1]+7),fill='#dfc8a6',outline=line)
        d.line([active_shoulder,elbow,active],fill=col,width=13,joint='curve')
        # A flat hand on paper must read differently from the reaching hand.
        if who=='陈':
            d.rounded_rectangle((active[0]-20,active[1]-9,active[0]+18,active[1]+9),radius=4,fill='#dfc8a6',outline=line,width=2)
            for offset in (-12,-5,2,9):
                d.line((active[0]+offset,active[1]-7,active[0]+offset,active[1]-1),fill='#9b866a',width=1)
        else:
            hx,hy=active
            d.polygon([(hx+18,hy+8),(hx-10,hy+7),(hx-13,hy+2),(hx-7,hy-3),(hx+9,hy-3),(hx+14,hy-11),(hx+19,hy-9)],fill='#dfc8a6',outline=line)
            d.line((hx-9,hy+2,hx+9,hy+2),fill=line,width=2)
        d.text((x-9,271),who,font=ft,fill='#f6f0e5')
        if review:
            d.line((x,184,*gaze),fill=col,width=2)
            d.ellipse((gaze[0]-4,gaze[1]-4,gaze[0]+4,gaze[1]+4),outline=col,width=2)

    person(309,c,s['chen_hand'],([355,260],[394,287]),[405,292],s['chen_gaze'],'陈')
    person(650,m,s['meng_hand'],([693,295],[691,349]),[559,283],s['meng_gaze'],'孟')
    if review:
        d.text((35,25),SPEC['variants'][key]['label'],font=ft,fill=line)
        d.text((35,56),f'{t:.2f} s  ·  审查层：注视线可见',font=small,fill=line)
        d.text((37,474),'固定机位 / 纸样不移动 / 无对白与音乐',font=small,fill=line)
    return im

trace={key:[state(i/8,key) for i in range(81)] for key in SPEC['variants']}
(BATCH/'event-trace.json').write_text(json.dumps(trace,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

# A contact sheet has diagnostic marks; the motion previews deliberately do not.
times=[2.5,3.5,4.25,5.5]
board=Image.new('RGB',(1800,885),'#f4f1e9')
bd=ImageDraw.Draw(board)
for row,key in enumerate(SPEC['variants']):
    for col,t in enumerate(times):
        frame=paint(t,key,True).resize((450,260),Image.Resampling.LANCZOS)
        board.paste(frame,(col*450,row*295))
    bd.text((24,row*295+262),SPEC['variants'][key]['label'],font=ImageFont.truetype(FONT,20),fill='#363d42')
board.save(MEDIA/'pose-comparison.png')
watch=Image.new('RGB',(1800,885),'#f4f1e9')
wd=ImageDraw.Draw(watch)
for row,key in enumerate(SPEC['variants']):
    for col,t in enumerate(times):
        watch.paste(paint(t,key,False).resize((450,260),Image.Resampling.LANCZOS),(col*450,row*295))
        wd.text((col*450+12,row*295+262),f'{"Y′" if key=="Z" else key}   {t:.2f} s',font=ImageFont.truetype(FONT,20),fill='#363d42')
watch.save(MEDIA/'pose-view.png')
for key in SPEC['variants']:
    frames=[paint(i/8,key).resize((720,416),Image.Resampling.LANCZOS).convert('P',palette=Image.Palette.ADAPTIVE,colors=128) for i in range(80)]
    # GIF stores centiseconds: alternate 120/130 ms so 8 fps totals 10 seconds.
    durations=[120 if i%2==0 else 130 for i in range(80)]
    frames[0].save(MEDIA/f'blocking-{key}.gif',save_all=True,append_images=frames[1:],duration=durations,loop=1,optimize=True)

print('Rendered schematic frames and GIFs to', MEDIA)
