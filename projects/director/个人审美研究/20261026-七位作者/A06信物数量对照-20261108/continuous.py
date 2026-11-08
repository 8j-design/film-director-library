"""Original continuous blocking revision, with synthetic cue audio, not natural foley."""
import render as r
from PIL import Image,ImageDraw,ImageChops
import math,struct,wave,subprocess,json,hashlib

N=240; SR=22050
def frame(n,many):
    t=n/24;im=Image.new('RGB',(640,360),'#283e4c');d=ImageDraw.Draw(im)
    d.rectangle((0,260,640,360),fill='#53636a')
    d.rectangle((45,40,176,257),fill='#172a39',outline='#789397',width=3)
    d.rectangle((210,42,602,233),fill='#334c58',outline='#182e3c',width=4)
    for y in (90,138,186,234):d.line((210,y,602,y),fill='#a47e58',width=5)
    if many:
        for group in range(4):
            for i in range(10):r.letter(d,252+200*(group%2)+(i%3)*3,70+96*(group//2)-i*3,.85)
    d.rectangle((324,260,592,276),fill='#a47e58')
    for q in (340,575):d.line((q,277,q,344),fill='#80634c',width=8)
    r.letter(d,430,240,1)
    x=105+55*min(t/1.5,1)+140*max(0,min((t-2.5)/4,1))
    walking=t<1.5 or 2.5<=t<6.5
    sway=math.sin(t*7)*7 if walking else 0
    d.ellipse((x-11,199,x+11,222),fill='#c0ac91')
    d.ellipse((x+4,205,x+7,208),fill='#172a39')
    d.polygon([(x-13,222),(x+14,222),(x+20,279),(x-18,279)],fill='#d19557')
    d.line((x-7,278,x-10+sway,325),fill='#172a39',width=8)
    d.line((x+8,278,x+13-sway,325),fill='#172a39',width=8)
    reach=max(0,min((t-6.5)/.7,1))
    lx=x+22+23*reach;ly=244
    if t>=7.2:lx=345
    retract=max(0,min((t-7.3)/.7,1))
    handx=(lx+5)*(1-retract)+(x+15)*retract
    handy=250*(1-retract)+270*retract
    d.line((x+10,234,handx,handy),fill='#c0ac91',width=7)
    r.letter(d,lx,ly,.7)
    return im

def run():
    events=[.22,.67,1.12,2.72,3.17,3.62,4.07,4.52,4.97,5.42,5.87,6.32]
    samples=[]
    for i in range(SR*10):
        t=i/SR;v=0
        for e in events:
            q=t-e
            if 0<=q<.12:v+=.18*math.sin(2*math.pi*110*q)*math.exp(-q*42)
        q=t-7.2
        if 0<=q<.08:v+=.12*math.sin(2*math.pi*1300*q)*math.exp(-q*70)
        samples.append(round(v*32767))
    wav=r.HERE/'continuous-cues.wav'
    with wave.open(str(wav),'wb') as w:w.setparams((1,2,SR,0,'NONE','not compressed'));w.writeframes(struct.pack('<'+'h'*len(samples),*samples))
    raws={};audios={}
    for label,many in [('E',False),('F',True)]:
        out=r.HERE/f'{label}.mp4'
        subprocess.run([str(r.FF),'-hide_banner','-loglevel','error','-n','-f','rawvideo','-pix_fmt','rgb24','-s','640x360','-r','24','-i','-','-i',str(wav),'-c:v','libx264','-crf','17','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-t','10','-movflags','+faststart',str(out)],input=b''.join(frame(n,many).tobytes() for n in range(N)),check=True)
        raws[label]=subprocess.check_output([str(r.FF),'-hide_banner','-loglevel','error','-i',str(out),'-map','0:v:0','-f','rawvideo','-pix_fmt','rgb24','-'])
        audios[label]=subprocess.check_output([str(r.FF),'-hide_banner','-loglevel','error','-i',str(out),'-map','0:a:0','-f','s16le','-ac','1','-ar',str(SR),'-'])
        assert len(raws[label])==N*640*360*3
    assert audios['E']==audios['F']
    boxes={ImageChops.difference(frame(n,False),frame(n,True)).getbbox() for n in range(N)}
    board=Image.new('RGB',(1280,4*382),'#19242c');d=ImageDraw.Draw(board);stride=640*360*3
    for col,v in enumerate(('E','F')):
        for row,n in enumerate((48,156,173,216)):
            board.paste(Image.frombytes('RGB',(640,360),raws[v][n*stride:(n+1)*stride]),(col*640,row*382))
            d.text((col*640+8,row*382+363),f'{v} {n/24:.2f}s / frame {n}',fill='white')
    board.save(r.HERE/'continuous-decoded.png')
    (r.HERE/'continuous-verification.json').write_text(json.dumps({'frames_each':N,'duration':10,'fps':24,'audio':'synthetic timing cues, not natural footsteps; not listened to','decoded_audio_identical':True,'audio_sha256':hashlib.sha256(audios['E']).hexdigest(),'difference_bounds':sorted(boxes),'physical_letter_continuity':'hand-carried letter ends at x345,y244; no cut','observer_feedback':False},indent=2),encoding='utf-8')

if __name__=='__main__':run()
