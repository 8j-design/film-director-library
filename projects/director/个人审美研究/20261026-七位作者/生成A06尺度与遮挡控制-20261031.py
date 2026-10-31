"""Original procedural composition study; no reference pixels or generative model."""
from pathlib import Path
from PIL import Image, ImageDraw
import math, subprocess, json, hashlib
task=Path(__file__).resolve().parent
root=task if task.name=='A06-风口灯标-20261031' else task/'原创试验'/'A06-风口灯标-20261031'
root.mkdir(parents=True,exist_ok=True)
ff='C:/Users/scvfv/Documents/ChatGPT/导演/新工作/研究媒体工具/imageio-ffmpeg/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
W,H,FPS,SECONDS=960,540,12,8
def frame(v,t):
    im=Image.new('RGB',(W,H),'#a4b5b5');d=ImageDraw.Draw(im)
    d.polygon([(0,240),(180,170),(420,230),(630,200),(960,290),(960,540),(0,540)],fill='#63776c')
    d.polygon([(0,370),(210,340),(530,385),(960,350),(960,540),(0,540)],fill='#829e8c' if v in [5,6] else '#45594f')
    # Monumental cloud mass is shared; no physical cloud simulation is claimed.
    for cx,cy,rx,ry in [(280,60,420,235),(600,90,340,190),(370,175,260,200),(75,180,210,150)]:
        d.ellipse((cx-rx,cy-ry,cx+rx,cy+ry),fill='#394d50')
    d.ellipse((425,70,865,375),fill='#a4b5b5')
    # Figure is 26px high in every version and frame.
    x,y=700,451
    if v==3:d.ellipse((x-33,y-47,x+33,y+12),fill='#b8c9bd')
    if v==4:d.polygon([(415,433),(680,400),(960,418),(960,472),(700,478),(515,468)],fill='#829e8c')
    d.polygon([(0,539),(465,469),(675,464),(960,500),(960,540)],fill='#566c60')
    d.polygon([(0,539),(440,477),(665,463),(615,475),(0,540)],fill='#a3b9b0')
    scale=2 if v==6 else 1
    def pt(dx,dy):return (x+dx*scale,y+dy*scale)
    d.ellipse((*pt(-3,-26),*pt(3,-20)),fill='#182d32')
    d.polygon([pt(-4,-20),pt(4,-20),pt(7,-4),pt(-7,-4)],fill='#182d32')
    d.line([pt(-3,-5),pt(-5,0)],fill='#182d32',width=2*scale)
    d.line([pt(3,-5),pt(5,0)],fill='#182d32',width=2*scale)
    sway=math.sin(t*math.pi)*4
    d.polygon([pt(-2,-19),pt(-21,-21+sway),pt(-16,-15+sway)],fill='#9c604a')
    # Same moving foreground ribbon, V2+ only raised 80px.
    edge=435+28*math.sin(t*math.pi/4)
    shift=0 if v==1 else -80
    pts=[(0,130),(260,150),(500,270),(730,edge+shift),(960,edge-20+shift),(960,0),(0,0)]
    d.polygon(pts,fill='#263c40')
    # Direction marks remain schematic, not realistic vegetation.
    for gx in range(40,940,55):
        gy=495+(gx*13)%35
        d.line([(gx,gy),(gx-13,gy-8+sway)],fill='#8ba18a',width=1)
    d.text((20,18),f'V{v} | {t:04.1f}s | original geometry study / no sound',fill='#f0e8cc')
    return im
report=json.loads((root/'编码与控制条件.json').read_text(encoding='utf-8'))['outputs'] if (root/'编码与控制条件.json').exists() else []
for v in [1,2,3,4,5,6]:
    path=root/f'V{v}.mp4'
    if path.exists() and any(r['version']==v for r in report):continue
    proc=subprocess.Popen([ff,'-y','-hide_banner','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-an','-c:v','libx264','-pix_fmt','yuv420p','-crf','20',str(path)],stdin=subprocess.PIPE)
    for i in range(FPS*SECONDS):proc.stdin.write(frame(v,i/FPS).tobytes())
    proc.stdin.close();assert proc.wait()==0
    board=Image.new('RGB',(960,4*285),'#17262b');bd=ImageDraw.Draw(board)
    for j,t in enumerate([0,2,4,6]):
        still=frame(v,t);still.thumbnail((480,270));xx=(j%2)*480;yy=(j//2)*285
        board.paste(still,(xx,yy+15));bd.text((xx+6,yy+2),f'V{v} {t}s',fill='white')
    # compact 2x2 board, unused bottom removed
    board.crop((0,0,960,570)).save(root/f'V{v}-contact.png')
    report.append({'version':v,'bytes':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'frames':96,'fps':FPS,'duration_seconds':SECONDS})
(root/'编码与控制条件.json').write_text(json.dumps({'shared':'960x540; V1-5 26px person; V6 52px; same camera, timing, cloud, path and scarf; no source pixels','versions':{'1':'foreground crosses figure','2':'foreground raised 80px only','3':'V2 plus compact bright ellipse behind figure','4':'V2 plus broad angled lighter field replacing V3 ellipse','5':'after seeing V1-4: lighten entire existing middle ground plane instead of an added floating patch','6':'after revisiting source at 56s: V5 person geometry uniformly scaled 2x around feet; not a blanket tiny-figure rule'},'outputs':report},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False))
