from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import argparse,json
P=argparse.ArgumentParser();P.add_argument('version');a=P.parse_args();R=Path(__file__).resolve().parent;D=R/'film'/a.version;files=sorted(p for p in D.glob('*.png') if p.stem.isdigit());out=D/'contacts';out.mkdir(exist_ok=True)
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',17);manifest=[]
for start in range(0,len(files),8):
 chunk=files[start:start+8];im=Image.new('RGB',(984,4*302+12),'#26313b');draw=ImageDraw.Draw(im)
 for i,p in enumerate(chunk):
  x=8+(i%2)*488;y=8+(i//2)*302
  with Image.open(p) as src:im.paste(src.convert('RGB').resize((480,270)),(x,y))
  draw.text((x,y+274),f'Frame {int(p.stem)} / {(int(p.stem)-1)/24:.2f}s',font=font,fill='white')
 target=out/f'contact-{start//8+1:02d}.png';im.save(target);manifest.append({'file':target.name,'frames':[int(p.stem) for p in chunk]})
(out/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print(json.dumps({'version':a.version,'actual_frame_images':len(files),'contact_sheets':len(manifest)},ensure_ascii=False))
