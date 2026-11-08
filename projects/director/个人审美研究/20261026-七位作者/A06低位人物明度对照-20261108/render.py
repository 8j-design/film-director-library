from pathlib import Path
from PIL import Image, ImageChops, ImageDraw

here = Path(__file__).resolve().parent


def shot(band):
    frame = Image.new('RGB', (480, 270), '#667477')
    draw = ImageDraw.Draw(frame)
    draw.ellipse((-85, -176, 489, 205), fill='#39474a')
    draw.ellipse((-110, -155, 289, 177), fill='#b2aca0')
    draw.polygon([(0, 202), (80, 185), (164, 211), (304, 198), (480, 178), (480, 269), (0, 269)], fill='#343939')
    draw.polygon([(136, 216), (310, 205), (390, 209), (480, 207), (480, 224), (320, 226), (130, 229)], fill=band)
    draw.polygon([(0, 222), (120, 230), (270, 230), (480, 241), (480, 269), (0, 269)], fill='#292e30')
    draw.ellipse((245, 207, 256, 218), fill='#26292a')
    draw.polygon([(244, 213), (256, 216), (260, 231), (243, 231)], fill='#26292a')
    draw.line((251, 227, 247, 238), fill='#26292a', width=4)
    draw.line((253, 227, 258, 238), fill='#26292a', width=4)
    draw.polygon([(250, 212), (226, 213), (241, 208)], fill='#26292a')
    return frame


dim, lit = shot((61, 65, 64)), shot((145, 149, 148))
assert ImageChops.difference(dim, lit).getbbox() == (130, 205, 480, 230)
assert dim.getpixel((252, 221)) == lit.getpixel((252, 221)) == (38, 41, 42)
assert dim.getpixel((266, 221)) == (61, 65, 64)
assert lit.getpixel((266, 221)) == (145, 149, 148)
board = Image.new('RGB', (960, 291), '#202329')
board.paste(dim, (0, 0))
board.paste(lit, (480, 0))
labels = ImageDraw.Draw(board)
labels.text((8, 273), 'DIM GROUND BAND', fill='white')
labels.text((488, 273), 'LIT GROUND BAND', fill='white')
board.save(here / 'contact.png')
