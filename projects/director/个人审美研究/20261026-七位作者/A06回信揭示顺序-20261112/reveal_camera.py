from pathlib import Path
import importlib.util,subprocess,json,hashlib
from PIL import Image,ImageDraw
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('original',HERE/'render.py');r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)
N,W,H=288,640,360
def box(n,v):
    if n<96:return r.BOXES['close']
    if n>=192:return r.BOXES['mid']
    t=(n-96)/(60 if v=='F' else 95);t=max(0,min(1,t));u=t*t*(3-2*t)
    a=r.BOXES['close'];b=r.BOXES['wide'];return tuple(round(x+(y-x)*u) for x,y in zip(a,b))
def main():
    result={};board=Image.new('RGB',(W*3,5*(H+22)),'#18272f');draw=ImageDraw.Draw(board)
    for col,v in enumerate(('E','F','G')):
        out=HERE/f'{v}.mp4'
        if v!='E':
            p=subprocess.Popen([str(r.FF),'-hide_banner','-loglevel','error','-n','-f','rawvideo','-pix_fmt','rgb24','-s','640x360','-r','24','-i','-','-an','-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(out)],stdin=subprocess.PIPE)
            for n in range(N):
                im=r.scene(n%96,2).crop(box(n,v)).resize((W,H),Image.Resampling.LANCZOS);p.stdin.write(im.tobytes())
            p.stdin.close();assert p.wait()==0
        raw=subprocess.check_output([str(r.FF),'-hide_banner','-loglevel','error','-i',str(out),'-f','rawvideo','-pix_fmt','rgb24','-']);stride=W*H*3;assert len(raw)==N*stride
        for row,n in enumerate((95,108,132,180,240)):
            board.paste(Image.frombytes('RGB',(W,H),raw[n*stride:(n+1)*stride]),(col*W,row*(H+22)))
            draw.text((col*W+8,row*(H+22)+H+4),f'{v} {n/24:.2f}s',fill='white')
        result[v]={'frames':288,'seconds':12,'audio':False,'middle':'hard cut' if v=='E' else ('2.5s zoom + 1.5s wide hold' if v=='F' else '4s zoom, no wide hold'),'sha256':hashlib.sha256(out.read_bytes()).hexdigest()}
    # The same scene and source-frame timing are used; only middle framing changes.
    assert all(box(n,'F')==box(n,'G') for n in list(range(96))+list(range(192,288)))
    board.save(HERE/'camera-decoded-comparison.png');(HERE/'camera-verification.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
if __name__=='__main__':main()
