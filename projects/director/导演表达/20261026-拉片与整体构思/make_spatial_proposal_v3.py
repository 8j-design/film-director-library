"""Original geometric blocking diagram; no reference-image editing or film simulation."""
from pathlib import Path
import math, json, csv, html
from PIL import Image, ImageDraw, ImageFont
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'空间验证V3';OUT.mkdir(exist_ok=True)
FIXED=[('固定工作台',(0.4,3.7,2.4,4.5)),('包架',(0.15,4.5,2.3,4.8)),('矮凳初位',(4.19,3.69,4.51,4.01)),('门外展示架',(5.02,-1.7,5.32,-.5)),('伞暂位',(5.05,-.4,5.3,-.15)),('柜台',(4.6,0.7,5.4,2.4)),('寄物处',(4.6,2.7,5.2,3.4)),('架收回备选位',(4.6,3.7,5.3,4.5))]
def table(cx,cy,angle):
    c,s=math.cos(angle),math.sin(angle)
    return [(cx+x*c-y*s,cy+x*s+y*c) for x,y in [(-1,-.425),(1,-.425),(1,.425),(-1,.425)]]
def rect(r):
    x,y,X,Y=r;return [(x,y),(X,y),(X,Y),(x,Y)]
def overlap(a,b):
    for p in (a,b):
        for i in range(4):
            x,y=p[i];X,Y=p[(i+1)%4];axis=(-(Y-y),X-x)
            aa=[q[0]*axis[0]+q[1]*axis[1] for q in a];bb=[q[0]*axis[0]+q[1]*axis[1] for q in b]
            if max(aa)<=min(bb)+1e-8 or max(bb)<=min(aa)+1e-8:return False
    return True
KEYS=[(1.4,2.525,0),(3.1,2.525,0),(3.1,2.525,math.pi/2),(3.85,2.525,math.pi/2),(3.85,-1.6,math.pi/2),(3.85,-1.6,0),(1.4,-1.2,0)]
poses=[]
for i in range(len(KEYS)-1):
    a,b=KEYS[i:i+2]
    for j in range(41):
        t=j/40;poses.append(tuple(a[k]*(1-t)+b[k]*t for k in range(3)))
def check(door):
    walls=[(-.12,-.12,3.85-door/2,.12),(3.85+door/2,-.12,5.52,.12),(-.12,0,0,4.92),(5.4,0,5.52,4.92),(0,4.8,5.4,4.92)]
    hits=[]
    for i,pose in enumerate(poses):
        poly=table(*pose)
        for name,r in FIXED+[(f'墙{j}',r) for j,r in enumerate(walls)]:
            if overlap(poly,rect(r)):hits.append({'sample':i,'obstacle':name,'pose':[round(x,4) for x in pose]})
    return {'door_width_m':door,'sample_count':len(poses),'collision_count':len(hits),'first_hits':hits[:5]}
result={'scope':'离散采样的桌面平面占地；含墙厚；不含人、抬高、倾斜、接触或消防/建筑规范检验','table_m':[2,.85],'v1':check(.75),'v2':check(1.1),'hypothetical':True,'state_limits':'架收回备选位保守预留为障碍；凳与袋仅记录初始/交接位置，桌下状态涉及高度未验；一袋上限是台词约定'}
(OUT/'空间几何核对.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
W,H=1160,980
im=Image.new('RGB',(W,H),'#f6f3ec');d=ImageDraw.Draw(im)
fontpath='C:/Windows/Fonts/msyh.ttc'
F=lambda size:ImageFont.truetype(fontpath,size)
d.text((28,20),'《借桌》空间提案 V3',font=F(32),fill='#232a2f')
d.text((28,66),'虚构平面 / 米为单位 / 原创布局草案 / 不是实地勘景',font=F(19),fill='#525e62')
S=103;OX=54;OY=355
xy=lambda p:(OX+p[0]*S,OY+p[1]*S)
def box(r,fill,outline='#45535a',width=2):
    x,y,X,Y=r;d.rectangle([xy((x,y)),xy((X,Y))],fill=fill,outline=outline,width=width)
def text(p,t,size=18,fill='#26353c'):d.text(xy(p),t,font=F(size),fill=fill)
box((0,0,5.4,4.8),'#ffffff')
# Opening, and storefront window represented as architectural diagram marks.
d.line([xy((3.3,0)),xy((4.4,0))],fill='#f6f3ec',width=10)
d.line([xy((.5,0)),xy((3.05,0))],fill='#64a6b4',width=9)
text((.5,.12),'橱窗',15);text((3.35,.12),'门 1.10m',15)
for name,r in FIXED:
    box(r,'#d9d8d1');text((r[0]+.03,r[1]+.04),name,11)
text((4.18,3.4),'凳旁→凳上',12)
def poly(pose,color,label=None):
    pts=[xy(p) for p in table(*pose)];d.polygon(pts,fill=color,outline='#293b44',width=2)
    if label:text((pose[0]-.7,pose[1]-.11),label,16)
poly(KEYS[0],'#e0bc83','① 店内长桌')
poly(KEYS[-1],'#b6d9ce','② 室外活动')
poly(KEYS[3],'#e5e9eb')
text((3.49,1.65),'竖向',15);text((3.49,1.91),'通过',15)
centers=[xy((p[0],p[1])) for p in KEYS]
d.line(centers,fill='#b46c39',width=4)
for p in centers:d.ellipse((p[0]-4,p[1]-4,p[0]+4,p[1]+4),fill='#b46c39')
text((.4,-2.55),'街边活动区（未设完整街道）',17)
text((.4,-2.2),'灰箱：提前还桌后使用',15)
box((.45,-.7,1.25,-.25),'#d8dfe3');box((1.5,-.7,2.3,-.25),'#d8dfe3')
text((.6,-.65),'箱',15);text((1.68,-.65),'箱',15)
text((.3,4.95),'室内 5.4 × 4.8m；图示按统一比例',17)
panelx=660
notes=[('图在检验什么',24),('长桌移动、转向和门口占地。',18),('初设门宽0.75m，小于桌短边。',18),('V2门宽1.10m，桌转90°后出门。',18),('',18),('状态变化另列',24),('绿色：借出后的室外桌位。',18),('灰箱：提前还桌后的书箱位置。',18),('寄袋：地面→凳面→领走。',18),('凳子最终归桌下，高度未验。',18),('',18),('仍未检验',24),('搬运者身体、手和脚的通路；',18),('真实抬高/倾斜、门扇和门槛；',18),('人物视线、镜头遮挡和表演；',18),('真实场地与业务流程。',18),('',18),('结果范围',24),(f'每版{len(poses)}个离散桌位采样。',18),(f'V1碰撞记录：{result["v1"]["collision_count"]}',18),(f'V2碰撞记录：{result["v2"]["collision_count"]}',18),('零碰撞仅指本模型采样。',18),('不等于全程可搬、场面成立。',18)]
y=137
for s,size in notes:
    d.text((panelx,y),s,font=F(size),fill='#33444a');y+=36 if size==24 else 28
im.save(OUT/'借桌-空间提案V3.png')
# Authoring geometry also exported as an SVG; text labels retain editable text.
parts=['<svg xmlns="http://www.w3.org/2000/svg" width="800" height="900" viewBox="-0.5 -3 7 8.5">','<style>text{font-family:"Microsoft YaHei",sans-serif;font-size:.16px;fill:#26353c}</style>','<rect x="-.5" y="-3" width="7" height="8.5" fill="#f6f3ec"/>','<rect x="0" y="0" width="5.4" height="4.8" fill="white" stroke="#45535a" stroke-width=".025"/>']
for name,r in FIXED:
    x,y,X,Y=r;parts.append(f'<rect x="{x}" y="{y}" width="{X-x}" height="{Y-y}" fill="#d9d8d1" stroke="#45535a" stroke-width=".02"/><text x="{x+.03}" y="{y+.25}">{html.escape(name)}</text>')
for pose,color in [(KEYS[0],'#e0bc83'),(KEYS[-1],'#b6d9ce'),(KEYS[3],'#e5e9eb')]:
    pts=' '.join(f'{x},{y}' for x,y in table(*pose));parts.append(f'<polygon points="{pts}" fill="{color}" stroke="#293b44" stroke-width=".02"/>')
parts += ['<line x1="3.3" y1="0" x2="4.4" y2="0" stroke="#f6f3ec" stroke-width=".12"/>','<text x=".1" y="-2.6">《借桌》虚构空间 V2 / 不是勘景 / 单位m</text>','<text x="3.3" y=".25">门1.10m</text>','<text x=".1" y="5.2">完整范围与未检验项见PNG和JSON；未包含搬运者身体</text>','</svg>']
(OUT/'借桌-空间提案V3.svg').write_text('\n'.join(parts),encoding='utf-8')
durations=[32,28,34,28,38,32,30,48,36,44,22,20,40,36]
with (OUT/'全片时长草案.csv').open('w',encoding='utf-8-sig',newline='') as f:
    wr=csv.writer(f);wr.writerow(['unit','start_seconds','duration_seconds','end_seconds','status'])
    t=0
    for i,dur in enumerate(durations,1):wr.writerow([i,t,dur,t+dur,'规划预算，未朗读实测']);t+=dur
assert t==468
print(json.dumps(result,ensure_ascii=False))
