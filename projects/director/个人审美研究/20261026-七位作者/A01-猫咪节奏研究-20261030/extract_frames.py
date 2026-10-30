from pathlib import Path
from PIL import Image,ImageDraw
import subprocess,json,hashlib,sys
ROOT=Path(__file__).resolve().parent
ffmpeg=ROOT.parents[1]/'研究媒体工具/imageio-ffmpeg/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
vid=sys.argv[1] if len(sys.argv)>1 else '7682994627658468841'
fps=int(sys.argv[2]) if len(sys.argv)>2 else 2
video=ROOT/f'reference-{vid}.mp4'
output=ROOT if vid=='7682994627658468841' else ROOT/vid
output.mkdir(exist_ok=True)
frames=output/'frames';frames.mkdir(exist_ok=True)
r=subprocess.run([str(ffmpeg),'-y','-hide_banner','-i',str(video),'-vf',f'fps={fps},scale=480:-1','-fps_mode','passthrough',str(frames/'frame-%03d.jpg')],capture_output=True,text=True,encoding='utf-8',errors='replace')
(output/'decode-log.txt').write_text(r.stderr,encoding='utf-8')
assert r.returncode==0
items=sorted(frames.glob('frame-*.jpg'))
for batch in range((len(items)+14)//15):
    sheet=Image.new('RGB',(1440,1450),'#eeeae2');d=ImageDraw.Draw(sheet)
    for k,p in enumerate(items[batch*15:(batch+1)*15]):
        img=Image.open(p).convert('RGB');img.thumbnail((480,264))
        x=(k%3)*480;y=(k//3)*290
        sheet.paste(img,(x,y+24));d.text((x+12,y+5),f'{(batch*15+k)/fps:05.1f}s nominal / fps{fps} diagnostic',fill='#152f3a')
    sheet.save(output/f'sheet-{batch+1}.png')
result={'source':f'https://www.douyin.com/video/{vid}','acquisition':'documented CUA video.downloadMedia on visible original page; no replay of private API','bytes':video.stat().st_size,'sha256':hashlib.sha256(video.read_bytes()).hexdigest(),'fps_sampling':fps,'frames':len(items),'boundary':'Decoded nominal time samples, exact selected input frame may vary by filter rounding; not full audiovisual viewing or listening; private third-party reference, do not include in original public/release artifacts'}
(output/'source-media.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False))
