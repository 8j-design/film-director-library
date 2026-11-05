from pathlib import Path
import json,shutil,hashlib
from PIL import Image,ImageDraw
src=Path('C:/Users/scvfv/AppData/Local/Temp/browser-use/assets/70d90236-bd32-4b11-8d9c-c005c794683f')
out=Path(__file__).resolve().parent/'本地参考/MeiGc天蓬24图-20261105';out.mkdir(parents=True,exist_ok=True)
order='e9a192b2ae9f11e7 a4668cde8e49c24f 52035a390c99ca64 03097192ffb7f97f f52d993173e72f47 bac7d2fa2dcc6b21 e74a301672401412 f8b0747919b01c57 a98a57cf19185b03 24c532604d130193 af4dcade74a1eeb3 c84a4fc6c2461358 85c15028ccd58e0f 60f2524fc8231af3 f363ee6b0f222de8 20d12902269819ee 066d4685de2b293a 81ce82f00b9f6315 939e741642bf772c 4ec8d8b8e4e79a2b 67acffb8cb887ad0 5781446142df9411 ca7428bf13587fad 4b214bdee669e316'.split()
assets={a['id']:a for a in json.loads((src/'manifest.json').read_text(encoding='utf-8'))['assets']};assert len(order)==len(set(order))==24
rows=[]
for i,aid in enumerate(order,1):
 p=out/f'{i:02d}.webp';assert not p.exists();shutil.copyfile(assets[aid]['path'],p)
 im=Image.open(p);assert im.size==(1920,1080)
 rows.append({'page':i,'asset_id':aid,'size':[1920,1080],'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
for start in range(0,24,4):
 b=Image.new('RGB',(1920,1128),'#171717');d=ImageDraw.Draw(b)
 for j in range(4):
  i=start+j+1;x=j%2*960;y=j//2*564
  b.paste(Image.open(out/f'{i:02d}.webp').resize((960,540)),(x,y+24));d.text((x+8,y+5),f'page {i}/24 / source still, not animation',fill='white')
 b.save(out/f'board{start//4+1}.png')
(out/'metadata.json').write_text(json.dumps({'source_url':'https://www.douyin.com/note/7405938094026853641','source_publisher':'MeiGc（梅干菜）','publication_time_on_page':'2024-08-22 20:22:19','order_basis':'unique 1920px image elements in DOM order; gallery24 confirmed; not inventory sorting','images':rows,'boundary':'page publication is not proof of original visual authorship; source media local only; no AV claim'},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print({'images':24,'boards':6,'all_1920x1080':True})
