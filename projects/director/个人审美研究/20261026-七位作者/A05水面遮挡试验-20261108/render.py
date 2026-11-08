from pathlib import Path
import json
import math
import random

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
WIDTH, HEIGHT = 840, 480
SIZE = (WIDTH, HEIGHT)
SOURCE_PNGS = ('01-unmasked.png', '02-occluded.png', '03-warm-reflection.png', '04-falloff.png')
Y, X = np.mgrid[:HEIGHT, :WIDTH]
WATER_EDGE = 309 + .075 * (X - 510)
rng = random.Random(842)

def solid(color):
    return Image.new('RGB', SIZE, color)

def background():
    high = np.array([16, 56, 73], dtype=float)
    low = np.array([10, 125, 119], dtype=float)
    a = (Y / HEIGHT)[..., None]
    field = high * (1 - a) + low * a
    reflected_glow = np.exp(-((X - 515) / 285)**2 - ((Y - 365) / 177)**2)
    field += reflected_glow[..., None] * [17, 25, 20]
    image = Image.fromarray(np.uint8(np.clip(field, 0, 255)))
    draw = ImageDraw.Draw(image)
    draw.polygon([(0, 0), (162, 0), (266, 77), (218, 117), (0, 111)], fill='#273e4b')
    draw.polygon([(0, 111), (218, 117), (266, 77), (261, 102), (224, 142), (0, 136)], fill='#112c37')
    draw.line([(24, 37), (179, 44), (215, 72)], fill='#52616b', width=3)
    draw.line([(0, 79), (181, 86), (221, 77)], fill='#40505c', width=4)
    draw.line([(246, 106), (299, 103), (345, 116), (391, 131), (472, 125)], fill='#92ae9f', width=3)
    draw.line([(246, 108), (299, 105), (345, 118), (391, 133), (472, 127)], fill='#243d3e', width=2)
    for _ in range(54):
        x = rng.randrange(-80, WIDTH)
        y = rng.randrange(83, HEIGHT)
        length = rng.randrange(9, 115)
        c = rng.choice(('#1a5e65', '#236c72', '#1d7278', '#287e7f', '#277477'))
        draw.line([(x,y),(x+length//2,y-3),(x+length,y+1)], fill=c, width=1)
    return image

def lantern():
    layer = Image.new('RGBA', SIZE)
    draw = ImageDraw.Draw(layer)
    draw.ellipse((457, 84, 566, 179), outline='#362d35', width=10)
    draw.arc((459, 84, 564, 172), 174, 355, fill='#ed9662', width=4)
    draw.polygon([(456, 137), (560, 132), (590, 177), (436, 187)], fill='#cb654c')
    draw.polygon([(436, 187), (590, 177), (582, 200), (449, 208)], fill='#7c3937')
    draw.line([(463, 140), (555, 135), (576, 166)], fill='#f5ae74', width=4)
    draw.polygon([(456, 207), (574, 200), (567, 347), (461, 363)], fill='#693e3d')
    draw.polygon([(472, 220), (558, 213), (550, 338), (480, 349)], fill='#e68c4f')
    draw.polygon([(479, 226), (544, 220), (540, 338), (489, 344)], fill='#f9b665')
    draw.polygon([(498, 303), (519, 238), (530, 277), (527, 315), (507, 332)], fill='#ffe7a5')
    draw.line([(462, 208), (471, 349)], fill='#412e34', width=11)
    draw.line([(567, 198), (556, 343)], fill='#4c3437', width=10)
    draw.line([(467, 250), (560, 240)], fill='#8d4c43', width=4)
    draw.polygon([(458, 345), (568, 333), (590, 360), (576, 382), (459, 395), (443, 376)], fill='#9f493e')
    draw.polygon([(443, 376), (590, 360), (576, 382), (459, 395)], fill='#60363b')
    draw.line([(450, 374), (578, 359)], fill='#e69865', width=4)
    draw.ellipse((468, 125, 483, 140), fill='#342d34', outline='#e29864', width=2)
    return layer

def ripple_mask():
    layer = Image.new('L', SIZE)
    d = ImageDraw.Draw(layer)
    for row in range(16):
        cy = 92 + row * 24
        for i in range(7):
            cx = -55 + i * 150 + rng.randrange(-50, 52)
            rx = rng.randrange(33, 110)
            amp = rng.randrange(3, 11)
            theta = rng.uniform(0, 6.28)
            n = rng.randrange(8, 17)
            coords = [(round(cx-rx+2*rx*j/n),
                       round(cy+amp*math.sin(j/n*6.28+theta)+2*math.sin(j/n*16+theta)))
                      for j in range(n+1)]
            bright = int(np.clip(74 + row * 5 + rng.randint(-28, 41), 42, 198))
            d.line(coords, fill=bright, width=2 if row < 9 else rng.choice((2, 3, 4)))
    for j in range(10):
        top = 321 + j * 8
        shift = (-1)**j * (4 + j)
        d.line([(461+shift,top+6), (502+shift,top), (540+shift,top+1),
                (572+shift,top-2), (601+shift,top+1)], fill=132+j*5, width=3 if j < 5 else 4)
    return np.asarray(layer).copy()

scene = background().convert('RGBA')
source = lantern()
scene.alpha_composite(source)
base = np.asarray(scene.convert('RGB')).copy()
object_mask = np.asarray(source)[:,:,3] > 0
above = object_mask & (Y < WATER_EDGE)
base[object_mask & ~above] = np.uint8(.49 * base[object_mask & ~above] + .51 * np.array([26, 106, 103]))
alpha = ripple_mask()
alpha_masked = alpha.copy()
alpha_masked[above] = 0
cool = np.broadcast_to(np.array([185, 238, 229]), base.shape)
warm = cool.copy()
reflection = (Y > WATER_EDGE) & (Y < 422) & (abs(X-518) < (57 + (Y-302)*.56))
warm[reflection] = [250, 204, 128]
# The constant band looked like parallel gold bars. Keep the strokes fixed and
# vary their reflection color along a wavering center and depth.
center = 516 + 13*np.sin((Y-313)*.105) + 6*np.sin((Y-313)*.31)
color_weight = reflection * np.exp(-((X-center)/(43 + (Y-309)*.18))**2)
color_weight *= np.clip(1-(Y-314)/112, .24, 1) * (.70 + .30*np.cos((Y-311)*.16)**2)
soft = np.rint(cool + (warm-cool)*color_weight[...,None]).astype(np.int32)

def composite(color, a):
    k = a[..., None]/255
    return np.uint8(np.rint(base*(1-k)+color*k))

frames = [composite(cool,alpha),composite(cool,alpha_masked),composite(warm,alpha_masked),composite(soft,alpha_masked)]
diff12 = np.any(frames[0]!=frames[1],axis=2)
diff23 = np.any(frames[1]!=frames[2],axis=2)
assert diff12.any() and not (diff12 & ~above).any()
assert diff23.any() and not (diff23 & ~reflection).any()
assert not (diff23 & above).any()
diff34 = np.any(frames[2]!=frames[3],axis=2)
assert diff34.any() and not (diff34 & ~reflection).any()
assert np.array_equal(frames[1][~reflection], frames[3][~reflection])
for name, frame in zip(SOURCE_PNGS, frames):
    Image.fromarray(frame).save(HERE/name)
contact = Image.new('RGB',(1200,748),'#192d3a')
draw = ImageDraw.Draw(contact)
labels = ['01 / water texture over everything','02 / dry lantern blocks ripples','03 / solid band of warm reflections','04 / broken, tapered reflection color']
for i, (frame,label) in enumerate(zip(frames,labels)):
    x0,y0=(i%2)*600,(i//2)*374
    contact.paste(Image.fromarray(frame).resize((600,343),Image.Resampling.LANCZOS),(x0,y0))
    draw.text((x0+15,y0+350),label,fill='#eef9f6')
contact.save(HERE/'comparison.png')
(HERE/'verification.json').write_text(json.dumps({'width':WIDTH,'height':HEIGHT,
    'v1_v2_changed_pixels':int(diff12.sum()),'v1_v2_all_changes_inside_dry_object':True,
    'v2_v3_changed_pixels':int(diff23.sum()),'v2_v3_all_changes_inside_reflection_band':True,
    'v2_v3_unchanged_ripple_alpha':True,'v3_v4_changed_pixels':int(diff34.sum()),
    'v3_v4_only_color_changes_inside_same_reflection_band':True,'audience_test':False},indent=2)+'\n',encoding='utf-8')
