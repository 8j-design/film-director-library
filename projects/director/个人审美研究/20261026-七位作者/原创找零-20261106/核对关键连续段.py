from pathlib import Path
from PIL import Image,ImageDraw
import json
t=Path(__file__).resolve().parent;d=t/'v3/decoded';files=sorted(d.glob('*.png'))
indices=list(range(47,67))+list(range(75,112));assert len(indices)==57
for s in range(0,len(indices),16):
    batch=indices[s:s+16];b=Image.new('RGB',(1200,224*((len(batch)+3)//4)),'#202020');draw=ImageDraw.Draw(b)
    for k,n in enumerate(batch):
        im=Image.open(files[n]).crop((400,260,700,460));x=k%4*300;y=k//4*224;b.paste(im,(x,y+24));draw.text((x+4,y+4),f'encoded #{n} {n/24:.3f}s',fill='white')
    b.save(t/f'v3/连续补核{s//16+1}.png')
(t/'连续补核元信息.json').write_text(json.dumps({'decoded_frame_indices':indices,'crop':[400,260,700,460],'generated_only_until_viewed':True,'not_complete_playback':True},indent=2),encoding='utf-8');print(len(indices))
