from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,math,hashlib,numpy as np
R=Path(__file__).resolve().parent;V=R/'verification';A=R/'artwork'
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',20)
def board(rows,out,w=384,h=288):
 im=Image.new('RGB',(len(rows[0])*(w+12)+12,len(rows)*(h+40)+12),'#17202a');d=ImageDraw.Draw(im)
 for ri,row in enumerate(rows):
  for ci,(path,label) in enumerate(row):
   x=12+ci*(w+12);y=12+ri*(h+40)
   with Image.open(path) as src:im.paste(src.convert('RGB').resize((w,h)),(x,y))
   d.text((x,y+h+5),label,fill='white',font=font)
 im.save(V/out)
board([[(A/v/f'base-{f:04d}.png',f'{v} / frame {f}') for f in [1,192,384]] for v in ['v1','v2','v3']],'versions-contact.png')
frames=[1,72,96,144,192,216,240,250,288,336,384]
board([[(V/f'mp4-frame-{f:04d}.png',f'MP4 {f:03d} / {(f-1)/24:.2f}s') for f in frames[i:i+3]] for i in range(0,9,3)]+[[(V/f'mp4-frame-{f:04d}.png',f'MP4 {f:03d} / {(f-1)/24:.2f}s') for f in frames[9:]]],'motion-contact.png')
board([[(A/'v2'/f,'V2 '+label) for f,label in [('base-0192.png','base'),('control-white-0192.png','white'),('control-flood-0192.png','flood')]],[(A/'v2'/f,'V2 '+label) for f,label in [('control-no-rim-0192.png','no rim'),('control-all-saturated-0192.png','palette swap'),('control-no-fringe-0192.png','no fringe')]]],'controls-contact.png')
# Same saved frame at phone thumbnail size: a resampling diagnostic, not measured phone perception.
im=Image.open(A/'v3'/'base-0192.png').convert('RGB');small=im.resize((160,120));small.save(V/'phone-size-160x120.png')
dec=sorted((V/'decoded-small').glob('*.png'));assert len(dec)==384
hashes=[];means=[];previous=None;deltas=[]
for p in dec:
 with Image.open(p) as image:
  image.load();assert image.size==(192,144);arr=np.array(image.convert('RGB'),dtype=np.float32)
 assert arr.mean()>2,'possible all-black output: '+p.name
 hashes.append({'frame':int(p.stem),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
 means.append(float(arr.mean()))
 if previous is not None:deltas.append({'frame':int(p.stem),'mean_absolute_pixel_delta':float(np.abs(arr-previous).mean())})
 previous=arr
geo=[{'display_width_m':1.8,'display_height_m':1.35,'eye_distance_m':d,'horizontal_angle_deg':math.degrees(2*math.atan(1.8/(2*d)))} for d in [.9,1.8,3.6]]
result={'decode':'384 frames loaded; all 192x144, no all-black frames by declared diagnostic','mean_pixel_range':[min(means),max(means)],'encoded_file':'v3/folds-of-air.mp4','temporal_delta_scope':'numerical change diagnostic, not perceptual rhythm or continuity assessment','frame_checksums':hashes,'pixel_deltas':deltas,'gallery_geometry_assumptions':geo,'phone_thumbnail':'160x120 pixels; no actual phone display width, luminance or viewing distance measured'}
(V/'pixel-and-display-checks.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
# Mark only the three successfully viewed root references; failed downloads stay failed.
p=R/'reference_images'/'motion'/'manifest.json';rows=json.loads(p.read_text(encoding='utf-8'))
for row in rows:
 if row['status']=='downloaded':row['viewed']=True;row['view_method']='tools.view_image, original local download, 2026-10-24'
p.write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'decoded_images':len(dec),'boards_created':4,'geometry':geo},ensure_ascii=False))
