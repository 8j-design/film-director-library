"""原创几何示意；同一绘图指令生成SVG与PNG，不编辑第三方图片。"""
from pathlib import Path
import math, json, hashlib
from PIL import Image, ImageDraw

ROOT=Path(__file__).resolve().parent
W,H=720,960
C={'sky':'#9ed5d7','wall':'#489aac','dark':'#215b78','light':'#a9dfdb',
   'tile':'#75c5cb','line':'#327d97','gold':'#dcc27b','floor':'#8ebdb6',
   'door':'#f5e8bd','person':'#b94f31','shadow':'#295f75'}

def scene(version):
    image=Image.new('RGB',(W,H),C['sky']);d=ImageDraw.Draw(image)
    svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">']
    def poly(points,fill):
        d.polygon(points,fill=fill)
        svg.append('<polygon points="'+' '.join(f'{x:.2f},{y:.2f}' for x,y in points)+f'" fill="{fill}"/>')
    def line(points,color,width=1):
        d.line(points,fill=color,width=width)
        svg.append('<polyline points="'+' '.join(f'{x:.2f},{y:.2f}' for x,y in points)+f'" fill="none" stroke="{color}" stroke-width="{width}"/>')
    def rect(box,fill):
        x,y,a,b=box;poly([(x,y),(a,y),(a,b),(x,b)],fill)
    def oval(box,fill):
        d.ellipse(box,fill=fill);x,y,a,b=box
        svg.append(f'<ellipse cx="{(x+a)/2}" cy="{(y+b)/2}" rx="{(a-x)/2}" ry="{(b-y)/2}" fill="{fill}"/>')
    def arch(cx,top,width,bottom,fill):
        half=width/2;shoulder=top+width*.52
        pts=[(cx-half,bottom),(cx-half,shoulder)]
        for i in range(17):
            t=i/16;pts.append((cx-half+half*t,top+(shoulder-top)*(1-t)**1.7))
        for i in range(1,17):
            t=i/16;pts.append((cx+half*t,top+(shoulder-top)*t**1.7))
        pts.append((cx+half,bottom));poly(pts,fill)
    def motif(cx,cy,size):
        radius=size*.39
        star=[]
        for n in range(16):
            r=radius if n%2==0 else radius*.52
            angle=math.pi*n/8
            star.append((cx+math.cos(angle)*r,cy+math.sin(angle)*r))
        line(star+[star[0]],C['line'],2)
        k=size*.085;poly([(cx,cy-k),(cx+k,cy),(cx,cy+k),(cx-k,cy)],C['gold'])
    def field(box,size):
        x,y,a,b=box
        for cy in range(y+size//2,b-size//3,size):
            for cx in range(x+size//2,a-size//3,size):motif(cx,cy,size)

    # 所有版本固定的主体、人物、光影和相机
    rect((44,70,676,750),C['wall'])
    rect((65,96,195,730),C['tile']);rect((525,96,655,730),C['tile'])
    rect((207,96,513,730),C['light'])
    arch(360,139,282,750,C['dark'])
    arch(360,184,222,748,C['tile'])
    rect((292,442,428,748),C['light'])
    arch(360,450,112,748,C['gold'])
    arch(360,470,84,748,C['door'])
    # 每个版本的图案只画在同样的墙面分区；V1/V2变化仅是分区的单元步长
    zones=[(70,105,188,342),(70,363,188,718),(532,105,650,342),(532,363,650,718),
           (216,106,504,133),(260,365,460,430)]
    sizes=[34]*len(zones) if version==1 else [100,34,100,34,34,62]
    for zone,size in zip(zones,sizes):field(zone,size)
    for xx in [57,199,211,509,521,663]:line([(xx,90),(xx,740)],C['dark'],3)
    for yy in [348,356]:line([(65,yy),(195,yy)],C['dark'],3);line([(525,yy),(655,yy)],C['dark'],3)
    # 固定遮挡/投影形状；并非物理光照模拟
    poly([(44,70),(676,70),(676,450),(485,247),(460,281),(240,70)],C['shadow'])
    rect((0,751,720,960),C['floor'])
    poly([(318,751),(402,751),(570,960),(100,960)],C['light'])
    for y in [790,850,925]:line([(0,y),(720,y)],C['line'],2)
    for x in range(-800,1500,160):line([(360,746),(x,960)],C['line'],2)
    # V1/V2图后审查：门周本已安静，真正竞争人物的是满地放射网格。
    # V3仅覆盖中央行走带的网格，人物本身、投影和建筑保持不动。
    if version>=3:
        poly([(326,752),(395,752),(480,960),(207,960)],C['light'])
    poly([(370,814),(465,856),(480,860),(373,822)],C['shadow'])
    oval((350,767,367,785),C['gold'])
    poly([(351,784),(366,784),(380,825),(360,838),(345,819)],C['person'])
    line([(352,818),(350,848)],C['dark'],5);line([(367,823),(381,844)],C['dark'],5)
    line([(351,792),(337,804)],C['dark'],4)
    # 底部前景遮挡固定，提供近/中/远层
    poly([(0,890),(75,850),(120,960),(0,960)],C['dark'])
    poly([(720,875),(663,837),(604,960),(720,960)],C['dark'])
    svg.append('</svg>')
    (ROOT/f'V{version}.svg').write_text('\n'.join(svg),encoding='utf-8')
    image.save(ROOT/f'V{version}.png')
    return image

if __name__=='__main__':
    import sys
    versions=[int(v) for v in sys.argv[1:]] or [1,2]
    images=[scene(v) for v in versions]
    sheet=Image.new('RGB',(360*len(images),510),'#eeeeea');sd=ImageDraw.Draw(sheet)
    for i,(v,img) in enumerate(zip(versions,images)):
        sheet.paste(img.resize((360,480),Image.Resampling.LANCZOS),(i*360,30))
        sd.text((i*360+12,9),f'V{v} / original controlled study',fill='#172c3a')
    sheet.save(ROOT/('compare-'+''.join(map(str,versions))+'.png'))
    payload={'medium':'original code-native geometric space study; not source artwork edit','size':[W,H],
             'palette':C,'invariants':['architecture','figure','camera','light shape','palette'],
             'V1':'same 34px repeat in every wall zone','V2':'zone repeat steps 100,34,100,34,34,62',
             'V3':'central floor quiet-zone mask after V1/V2 review; no change to door',
             'versions_rendered':versions}
    (ROOT/'parameters.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'rendered':versions,'directory':str(ROOT)},ensure_ascii=False))
