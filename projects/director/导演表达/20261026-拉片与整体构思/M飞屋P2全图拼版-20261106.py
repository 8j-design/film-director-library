from pathlib import Path
import json,sys
from PIL import Image,ImageDraw
root=Path(__file__).resolve().parent/'本地参考/M飞屋P2-20261106'/sys.argv[1]
j=json.loads((root/'metadata.json').read_text(encoding='utf-8'));times=j['context_positions']
for start in range(0,len(times),6):
    batch=times[start:start+6];b=Image.new('RGB',(1920,564*((len(batch)+1)//2)),'#202020');d=ImageDraw.Draw(b)
    for k,t in enumerate(batch):
        b.paste(Image.open(root/f'context{t:g}.png'),(k%2*960,k//2*564+24));d.text((k%2*960+12,k//2*564+5),f'nominal {t:g}s, seek not exact PTS',fill='white')
    dest=root/f'context-board{start//6+1}.png';assert not dest.exists();b.save(dest)
print({'full_context_positions':len(times),'boards_generated_not_yet_viewed':(len(times)+5)//6})
