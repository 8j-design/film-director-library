from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import sys
R=Path(__file__).resolve().parent/'reference_media'/(sys.argv[1] if len(sys.argv)>1 else 'sprite_frames');out=R/'contacts';out.mkdir(exist_ok=True);files=sorted(R.glob('*.png'));font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',17)
for st in range(0,len(files),8):
 im=Image.new('RGB',(984,4*234+12),'#222222');d=ImageDraw.Draw(im)
 for i,p in enumerate(files[st:st+8]):
  x=8+i%2*488;y=8+i//2*234
  with Image.open(p) as f:im.paste(f.convert('RGB').resize((480,201)),(x,y))
  d.text((x,y+204),f'Source frame {int(p.stem)} / {(int(p.stem)-1)/24:.2f}s',font=font,fill='white')
 im.save(out/f'contact-{st//8+1:02d}.png')
print(len(files),'stills',len(list(out.glob('*.png'))),'sheets')
