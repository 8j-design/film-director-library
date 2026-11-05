from pathlib import Path
import subprocess,json,argparse
from PIL import Image,ImageDraw
p=argparse.ArgumentParser();p.add_argument('--label',required=True);p.add_argument('--times',required=True);p.add_argument('--contexts',required=True);a=p.parse_args()
task=Path(__file__).resolve().parent;root=task/'本地参考/M飞屋完结-20261105';out=root/a.label;out.mkdir(exist_ok=True)
ff=task.parents[0]/'研究媒体工具/imageio-ffmpeg/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
source=root/'M飞屋完结-7644503190498528554.mp4';times=[float(x) for x in a.times.split(',')];contexts=[float(x) for x in a.contexts.split(',')]
assert times==sorted(set(times)) and contexts==sorted(set(contexts))
for start in range(0,len(times),8):
    batch=times[start:start+8];board=Image.new('RGB',(1280,len(batch)*144),'#202020');d=ImageDraw.Draw(board)
    for j,t in enumerate(batch):
        dest=out/f'sub{t:g}.png';assert not dest.exists()
        subprocess.run([str(ff),'-hide_banner','-loglevel','error','-ss',str(t),'-i',str(source),'-frames:v','1','-vf','crop=1920:180:0:900,scale=1280:120',str(dest)],check=True)
        board.paste(Image.open(dest),(0,j*144+24));d.text((8,j*144+4),f'nominal {int(t)//60}:{t%60:04.1f} / seek not exact PTS',fill='white')
    board.save(out/f'board{start//8+1}.png')
for t in contexts:
    dest=out/f'context{t:g}.png';assert not dest.exists()
    subprocess.run([str(ff),'-hide_banner','-loglevel','error','-ss',str(t),'-i',str(source),'-frames:v','1','-vf','scale=960:540',str(dest)],check=True)
(out/'metadata.json').write_text(json.dumps({'source':'https://www.douyin.com/video/7644503190498528554','subtitle_positions':times,'context_positions':contexts,'generated_only_not_read_claim':True,'boundary':'local original selected subtitle crops and full frames, not continuous viewing/listening'},ensure_ascii=False,indent=2),encoding='utf-8')
print({'subtitle_positions':len(times),'boards':(len(times)+7)//8,'contexts':len(contexts)})
