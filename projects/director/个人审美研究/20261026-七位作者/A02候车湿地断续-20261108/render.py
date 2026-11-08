from pathlib import Path
from hashlib import sha256
import json

import numpy as np
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / 'tests/A02-雨后候车-20261027/F.png'
W, H = 640, 420
X, Y = np.meshgrid(np.arange(W), np.arange(H))

def mask_from_polygon(points):
    mask = Image.new('L',(W,H),0)
    ImageDraw.Draw(mask).polygon(points,fill=255)
    return np.asarray(mask)>0

def f_perimeter():
    layer=Image.new('L',(W,H),0)
    draw=ImageDraw.Draw(layer)
    draw.polygon([(40,307),(280,271),(595,293),(559,386),(193,407),(42,369)],fill=255)
    for j in range(45):
        x=55+j*11
        y=306-(x-40)*.16 if x<280 else 271+(x-280)*.07
        draw.line((x,y,x+7,y-1),fill=255,width=2)
    draw.line((42,369,193,407,559,386),fill=255,width=2)
    return np.asarray(layer)>0

def wet_mask():
    left=[(274,273),(326,277),(316,286),(341,290),(332,296),(287,294),(262,303),(276,315),
          (239,325),(255,332),(228,342),(232,352),(203,364),(239,365),(267,373),(253,380),
          (289,391),(282,399),(188,403),(142,388),(90,381),(70,369),(95,365),(75,355),
          (102,345),(151,336),(142,325),(182,314),(160,308),(192,297),(230,289),(217,282)]
    right=[(359,287),(385,285),(419,289),(414,301),(460,304),(499,294),(552,296),(562,306),
           (540,315),(569,327),(528,340),(548,348),(521,359),(533,370),(503,379),(466,377),
           (435,389),(387,391),(414,375),(377,369),(381,360),(407,350),(386,343),(397,334),
           (369,325),(398,319),(382,308),(342,303)]
    islands=[[(80,316),(110,310),(137,310),(123,318),(100,322)],
             [(282,338),(305,330),(335,333),(315,344),(291,345)],
             [(310,371),(331,365),(353,368),(341,376),(320,377)],
             [(482,390),(512,384),(537,386),(505,393)]]
    wet=mask_from_polygon(left)|mask_from_polygon(right)
    for island in islands:
        wet|=mask_from_polygon(island)
    return wet

base=np.asarray(Image.open(SOURCE).convert('RGB')).copy()
old=f_perimeter()
wet=wet_mask()&old
body_shadow=(X>=295)&(X<=313)&(Y>=285)&(Y<=350)&np.all(base==[37,37,55],axis=2)
removed=old&~wet&~body_shadow
g=base.copy()
g[removed]=[43,41,59]
assert np.any(g!=base) and np.array_equal(g[~removed],base[~removed])

warm=np.all(g==[247,201,121],axis=2)|np.all(g==[230,170,192],axis=2)
subject=warm&wet&(abs(X-192)<48)&(Y>=292)
# Keep the candidate strokes in place. Break up the strength of one reflection
# by moving between the local dark paint and its existing bright stroke color.
dy=(Y-292)
pulse=.23+.77*np.cos((dy+.11*(X-192))*.135)**4
falloff=np.clip(1-abs(X-(191+6*np.sin(dy*.061)))/47,.18,1)
gain=pulse*falloff
h=g.copy()
h[subject]=np.rint(np.array([87,64,88])+(g[subject]-np.array([87,64,88]))*gain[subject,None]).astype('uint8')
diff=np.any(h!=g,axis=2)
assert diff.any() and not (diff&~subject).any()
assert np.array_equal(base[:267],h[:267])

for name,im in [('G-shape.png',g),('H-reflection.png',h)]:
    Image.fromarray(im).save(HERE/name)
board=Image.new('RGB',(1500,368),'#292b40')
d=ImageDraw.Draw(board)
for col,(data,label) in enumerate([(base,'F | saved baseline'),(g,'G | separated wet areas'),(h,'H | reduced reflection in short sections')]):
    board.paste(Image.fromarray(data).resize((500,329),Image.Resampling.LANCZOS),(col*500,0))
    d.text((col*500+13,342),label,fill='#eedee4')
board.save(HERE/'comparison.png')
(HERE/'verification.json').write_text(json.dumps({
    'baseline_sha256':sha256(SOURCE.read_bytes()).hexdigest(),'dimensions':[W,H],
    'f_to_g_changed_pixels':int(np.count_nonzero(np.any(g!=base,axis=2))),
    'g_to_h_changed_pixels':int(diff.sum()),'upper_267_rows_identical':True,
    'g_to_h_limited_to_existing_warm_marks':True,'audience_test':False},indent=2)+'\n',encoding='utf-8')
