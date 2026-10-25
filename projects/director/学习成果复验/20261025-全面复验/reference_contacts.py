from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json
R=Path(__file__).resolve().parent/'reference_media/pas_frames';out=R/'contacts';out.mkdir(exist_ok=True);files=sorted(R.glob('*.png'));font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',17)
for st in range(0,len(files),8):
 im=Image.new('RGB',(984,4*390+12),'#222222');d=ImageDraw.Draw(im)
 for i,p in enumerate(files[st:st+8]):
  x=8+i%2*488;y=8+i//2*390
  with Image.open(p) as f:im.paste(f.convert('RGB'),(x,y))
  d.text((x,y+364),f'Source frame {int(p.stem)} / {(int(p.stem)-1)/23.9760246:.2f}s',font=font,fill='white')
 im.save(out/f'contact-{st//8+1:02d}.png')
print(len(files),'stills',len(list(out.glob('*.png'))),'sheets')
