from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,sys
version=sys.argv[1] if len(sys.argv)>1 else 'v6'
R=Path(__file__).resolve().parent/'film'/version/'verification/selected';out=R/'contacts';out.mkdir(exist_ok=True);files=sorted(R.glob('*.png'));font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',17);manifest=[]
for st in range(0,len(files),8):
 im=Image.new('RGB',(984,4*302+12),'#26313b');d=ImageDraw.Draw(im);subset=files[st:st+8]
 for i,p in enumerate(subset):
  x=8+i%2*488;y=8+i//2*302
  with Image.open(p) as f:im.paste(f.convert('RGB').resize((480,270)),(x,y))
  d.text((x,y+274),f'Actual MP4 {int(p.stem)} / {(int(p.stem)-1)/24:.2f}s',font=font,fill='white')
 name=f'contact-{st//8+1:02d}.png';im.save(out/name);manifest.append({'file':name,'frames':[int(p.stem) for p in subset]})
(out/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8');print(len(files),'frames',len(manifest),'sheets')
