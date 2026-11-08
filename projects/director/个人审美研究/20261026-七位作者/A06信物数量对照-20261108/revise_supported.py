import render as r
from PIL import Image,ImageDraw,ImageChops
import subprocess,json

def revised(n):
    im=r.frame(n,'A')
    if n>=r.CUT:
        d=ImageDraw.Draw(im)
        for group in range(4):
            for i in range(10):
                r.letter(d,252+200*(group%2)+(i%3)*3,70+96*(group//2)-i*3,.85)
    return im

out=r.HERE/'D.mp4'
subprocess.run([str(r.FF),'-hide_banner','-loglevel','error','-n','-f','rawvideo','-pix_fmt','rgb24','-s',f'{r.W}x{r.H}','-r',str(r.FPS),'-i','-','-an','-c:v','libx264','-crf','17','-pix_fmt','yuv420p','-movflags','+faststart',str(out)],input=b''.join(revised(n).tobytes() for n in range(r.N)),check=True)
raw=subprocess.check_output([str(r.FF),'-hide_banner','-loglevel','error','-i',str(out),'-f','rawvideo','-pix_fmt','rgb24','-'])
stride=r.W*r.H*3
assert len(raw)==r.N*stride
assert all(revised(n).tobytes()==r.frame(n,'B').tobytes() for n in range(r.CUT))
board=Image.new('RGB',(1280,764),'#19242c');d=ImageDraw.Draw(board)
for col,v in enumerate(('C','D')):
    data=raw if v=='D' else subprocess.check_output([str(r.FF),'-hide_banner','-loglevel','error','-i',str(r.HERE/'C.mp4'),'-f','rawvideo','-pix_fmt','rgb24','-'])
    for row,n in enumerate((84,180)):
        board.paste(Image.frombytes('RGB',(r.W,r.H),data[n*stride:(n+1)*stride]),(col*640,row*382))
        d.text((col*640+8,row*382+363),f'{v}: frame {n}',fill='white')
board.save(r.HERE/'decoded-supported-revision.png')
(r.HERE/'supported-revision-verification.json').write_text(json.dumps({'frames':r.N,'fps':r.FPS,'added_letter_count':40,'precut_exact_match':True,'change':'positions and overlap only; count and source envelope dimensions unchanged','audio':False,'viewer_feedback':False,'visibility_limitation':'overlap means drawn count is not perceived count'},indent=2),encoding='utf-8')
