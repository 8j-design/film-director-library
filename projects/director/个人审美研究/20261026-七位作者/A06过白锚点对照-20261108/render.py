from pathlib import Path
import json
import os
import shutil
import subprocess
from PIL import Image, ImageChops, ImageDraw

HERE = Path(__file__).resolve().parent
LOCAL_FFMPEG = HERE.parent.parent / '研究媒体工具/imageio-ffmpeg/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
FFMPEG = os.environ.get('FFMPEG') or (str(LOCAL_FFMPEG) if LOCAL_FFMPEG.is_file() else shutil.which('ffmpeg'))
SIZE = (480, 270)
FPS = 24
FRAME_COUNT = 72
WHITE_START = 29
WHITE_END = 32
FRAMES_ON_BOARD = (25, 30, 38, 56)

def draw_token(draw, x, y, opposite):
    draw.ellipse((x-19, y-19, x+19, y+19), fill='#26687c', outline='#bde7ed', width=3)
    draw.ellipse((x-13, y-13, x+13, y+13), outline='#60a3a9', width=2)
    delta = -1 if opposite else 1
    draw.line((x-10, y+delta*6, x+10, y-delta*6), fill='#e1faf5', width=3)

def frame(index, changed, revision):
    if WHITE_START <= index <= WHITE_END:
        return Image.new('RGB', SIZE, '#fff8ed')
    after = index > WHITE_END
    image = Image.new('RGB', SIZE, '#705157' if not after else '#233a59')
    draw = ImageDraw.Draw(image)
    if after:
        draw.polygon([(0,0),(479,0),(369,126),(132,126)], fill='#b4bbbc')
        draw.polygon([(132,126),(369,126),(479,269),(0,269)], fill='#78a9b9')
        draw.rectangle((132,85,369,126), fill='#596b83')
        for x, y in [(72,45),(151,65),(305,36),(395,107),(92,202),(403,213)]:
            draw.ellipse((x-9,y-9,x+9,y+9), fill='#477c97', outline='#a0d3db', width=2)
        person_x, person_y = (264+(index-33)//4, 171-(index-33)//8)
    else:
        draw.polygon([(0,0),(479,0),(479,147),(0,133)], fill='#bd8d77')
        draw.polygon([(0,133),(479,147),(479,269),(0,269)], fill='#754e4e')
        for x in (52,121,365,434):
            draw.rectangle((x,72,x+23,184), fill='#563d4c')
        person_x, person_y = (184+index//4, 180-index//8)
    draw.ellipse((person_x-8,person_y-27,person_x+8,person_y-11), fill='#303341')
    draw.line((person_x,person_y-10,person_x,person_y+15), fill='#303341', width=10)
    draw.line((person_x-1,person_y+12,person_x-9,person_y+26), fill='#303341', width=4)
    draw.line((person_x+1,person_y+12,person_x+11,person_y+23), fill='#303341', width=4)
    if revision == 1:
        token_x, token_y = (240, 131)
    elif after:
        token_x, token_y = (239+(index-33)//6, 132-(index-33)//9)
    else:
        token_x, token_y = (225+index//2, 143-index//3)
    draw_token(draw, token_x, token_y, changed and after)
    return image

def render():
    if not FFMPEG:
        raise SystemExit("Set FFMPEG or put ffmpeg on PATH.")
    statistics = {}
    stride = SIZE[0]*SIZE[1]*3
    for revision in (1, 2):
        pair = [[frame(i, changed, revision) for i in range(FRAME_COUNT)] for changed in (False, True)]
        assert all(ImageChops.difference(pair[0][i],pair[1][i]).getbbox() is None for i in range(WHITE_END+1))
        differences = [ImageChops.difference(pair[0][i],pair[1][i]).getbbox() for i in range(WHITE_END+1,FRAME_COUNT)]
        assert all(box and box[2]-box[0] <= 24 and box[3]-box[1] <= 18 for box in differences)
        board = Image.new('RGB',(960,4*294),'#161d27')
        labels = ImageDraw.Draw(board)
        for col, frames in enumerate(pair):
            name = f'v{revision}-'+('changed' if col else 'retained')
            movie = HERE/(name+'.mp4')
            subprocess.run([str(FFMPEG),'-hide_banner','-loglevel','error','-y','-f','rawvideo','-pixel_format','rgb24','-video_size','480x270','-framerate',str(FPS),'-i','-','-c:v','libx264','-pix_fmt','yuv420p','-movflags','+faststart',str(movie)], input=b''.join(im.tobytes() for im in frames),check=True)
            decoded = subprocess.check_output([str(FFMPEG),'-hide_banner','-loglevel','error','-i',str(movie),'-f','rawvideo','-pix_fmt','rgb24','-'])
            assert len(decoded)==stride*FRAME_COUNT
            for row,i in enumerate(FRAMES_ON_BOARD):
                board.paste(Image.frombytes('RGB',SIZE,decoded[i*stride:(i+1)*stride]),(480*col,294*row))
                labels.text((480*col+12,294*row+275),f'{name} | frame {i}',fill='white')
        board.save(HERE/f'v{revision}-decoded.png')
        statistics[f'v{revision}'] = {'identical_frames_through_white':WHITE_END+1,'different_frames_after_white':len(differences),'first_difference_bounds':list(differences[0])}
    (HERE/'metadata.json').write_text(json.dumps({'fps':FPS,'frames_each':FRAME_COUNT,'white_frame_range_inclusive':[WHITE_START,WHITE_END],'board_frames':list(FRAMES_ON_BOARD),'statistics':statistics,'audio':False,'observer_test':False},indent=2)+'\n',encoding='utf-8')

if __name__=='__main__':
    render()
