from pathlib import Path
from PIL import Image,ImageDraw
import math,subprocess,json,hashlib
HERE=Path(__file__).resolve().parent
FF=HERE.parent.parent/'研究媒体工具/imageio-ffmpeg/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
W,H,FPS=640,360,24
def scene(n,rev=False):
    im=Image.new('RGB',(1280,720),'#21333b');d=ImageDraw.Draw(im)
    for y in range(720):
        c=int(29+y/35);d.line((0,y,1280,y),fill=(c,c+20,c+25))
    for x in (90,1120):
        d.rectangle((x,100,x+30,720),fill='#31434b');d.arc((x-90,80,x+150,360),180,360,fill='#657679',width=8)
    d.rectangle((50,600,1230,620),fill='#657679')
    for x in range(0,1280,65):d.line((x,660,x+45,650),fill='#536973',width=2)
    d.polygon([(180,460),(1050,460),(950,330),(280,330)],fill='#8c806a')
    for row in range(5):
        for col in range(15):
            x=210+col*53+row*6;y=348+row*23
            d.polygon([(x,y),(x+65,y-3),(x+78,y+22),(x+8,y+26)],fill=('#c0c5b5' if (row+col)%3 else '#9faeac'),outline='#718885')
            d.line((x,y,x+39,y+12,x+65,y-3),fill='#718885',width=1)
    for x in (245,975):d.rectangle((x,455,x+12,600),fill='#806d53')
    d.rectangle((397,484,840,499),fill='#8d7153')
    for x in (410,824):d.rectangle((x,498,x+10,580),fill='#806d53')
    if rev:
        d.rectangle((100,220,260,270),fill='#b2baaa',outline='#1d3139',width=3)
        d.text((114,233),'WAITING / 07',fill='#21333b',stroke_width=1)
    # Focal envelope lies on roof, a seal and clipped corner distinguish it.
    d.polygon([(609,386),(684,386),(690,413),(611,416)],fill='#e4d9ad',outline='#746c5d')
    d.line((609,386,651,405,684,386),fill='#746c5d',width=2)
    if rev!=2:d.ellipse((646,397,655,406),fill='#b56848')
    if rev:d.ellipse((617,397,631,411),fill='#c46f47',outline='#edd9ae',width=2)
    dy=math.sin(n/FPS*2)*1.2
    d.ellipse((629,347+dy,687,389+dy),fill='#367888',outline='#84a9ae',width=2)
    d.polygon([(630,369+dy),(610,390+dy),(645,385+dy)],fill='#2a5869')
    d.ellipse((669,335+dy,698,363+dy),fill='#4a8c9b')
    d.polygon([(694,347+dy),(711,352+dy),(695,356+dy)],fill='#d2b179')
    d.ellipse((686,343+dy,690,347+dy),fill='#101e23')
    for x in (652,676):
        d.line((x,384+dy,x-1,401),fill='#262b29',width=3);d.line((x-7,403,x+5,401),fill='#262b29',width=2)
    return im
BOXES={'close':(565,320,765,433),'mid':(380,235,1020,595),'wide':(0,0,1280,720)}
ORDERS={'B':['close','mid','wide'],'A':['wide','close','mid'],'C':['close','wide','mid'],'D':['close','wide','mid'],'E':['close','wide','mid']}
def frame(n,v):return scene(n%96,2 if v=='E' else int(v=='D')).crop(BOXES[ORDERS[v][n//96]]).resize((W,H),Image.Resampling.LANCZOS)
def main():
    meta={};board=Image.new('RGB',(W*5,(H+24)*3),'#18272f');d=ImageDraw.Draw(board)
    for col,(v,order) in enumerate(ORDERS.items()):
        out=HERE/f'{v}.mp4'
        if not out.exists():
            p=subprocess.Popen([str(FF),'-hide_banner','-loglevel','error','-n','-f','rawvideo','-pix_fmt','rgb24','-s','640x360','-r','24','-i','-','-an','-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(out)],stdin=subprocess.PIPE)
            for n in range(288):p.stdin.write(frame(n,v).tobytes())
            p.stdin.close();assert p.wait()==0
        decoded=subprocess.check_output([str(FF),'-hide_banner','-loglevel','error','-i',str(out),'-f','rawvideo','-pix_fmt','rgb24','-'])
        stride=W*H*3;assert len(decoded)==288*stride
        for row,n in enumerate((48,144,240)):
            board.paste(Image.frombytes('RGB',(W,H),decoded[n*stride:(n+1)*stride]),(col*W,row*(H+24)))
            d.text((col*W+8,row*(H+24)+H+4),f'{v} {order[row]} t={n/24:.1f}s',fill='white')
        meta[v]={'frames':288,'fps':24,'seconds':12,'order':order,'audio':False,'sha256':hashlib.sha256(out.read_bytes()).hexdigest()}
    board.save(HERE/'decoded-comparison.png');(HERE/'verification.json').write_text(json.dumps(meta,indent=2),encoding='utf-8')
    Image.frombytes('RGB',(W,H),decoded[48*stride:49*stride]).save(HERE/'E-close-decoded.png')
if __name__=='__main__':main()
