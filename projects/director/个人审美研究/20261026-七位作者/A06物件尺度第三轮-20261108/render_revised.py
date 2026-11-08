from pathlib import Path
import json
import subprocess

from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
FFMPEG = HERE.parent.parent / '研究媒体工具/imageio-ffmpeg/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
SIZE = (480, 270)
FPS = 24
CUT_FRAME = 30
FRAME_COUNT = 72
SCALES = {'small': 0.65, 'large': 1.72}


def draw_marker(draw, x, y, scale):
    def polygon(points):
        return [(round(x + a * scale), round(y + b * scale)) for a, b in points]
    draw.polygon(polygon([(-30, -34), (20, -34), (32, -22), (32, 0), (-30, 0)]), fill='#e59755', outline='#422e38', width=2)
    draw.ellipse((round(x - 7 * scale), round(y - 26 * scale), round(x + 8 * scale), round(y - 12 * scale)), fill='#3d4453')
    draw.line(polygon([(-20, -7), (-9, -7), (3, -7)]), fill='#fff1cb', width=max(1, round(2 * scale)))


def frame(number, variant):
    img = Image.new('RGB', SIZE, '#242c46')
    draw = ImageDraw.Draw(img)
    if number < CUT_FRAME:
        draw.rectangle((29, 37, 402, 153), fill='#506781', outline='#809bab', width=3)
        draw.rectangle((54, 154, 452, 269), fill='#4f4655')
        draw.rectangle((78, 170, 380, 187), fill='#ad815e')
        draw.line((93, 185, 93, 265), fill='#ad815e', width=10)
        draw.line((361, 185, 361, 265), fill='#ad815e', width=10)
        draw_marker(draw, 230, 171, 0.9)
    else:
        draw.rectangle((0, 0, 479, 163), fill='#8dacba')
        draw.polygon([(0, 154), (116, 111), (225, 157), (355, 117), (479, 151), (479, 269), (0, 269)], fill='#819075')
        draw.polygon([(0, 202), (226, 179), (326, 187), (479, 171), (479, 269), (0, 269)], fill='#aaa17b')
        draw.line((295, 212, 295, 131), fill='#534858', width=3)
        draw.polygon([(297, 131), (326, 140), (297, 151)], fill='#cdb574')
        x = 329 + (number - CUT_FRAME) // 8
        draw.ellipse((x-5, 170, x+5, 180), fill='#282d42')
        draw.line((x, 180, x, 196), fill='#282d42', width=6)
        draw.line((x-1, 195, x-5, 208), fill='#282d42', width=3)
        draw.line((x+1, 195, x+6, 208), fill='#282d42', width=3)
        draw_marker(draw, 230, 209, SCALES[variant])
    return img


def run():
    raw = {}
    for variant in SCALES:
        frames = [frame(number, variant) for number in range(FRAME_COUNT)]
        encoded = HERE / f'{variant}-revised.mp4'
        subprocess.run([str(FFMPEG),'-hide_banner','-loglevel','error','-n','-f','rawvideo','-pixel_format','rgb24','-video_size','480x270','-framerate',str(FPS),'-i','-','-c:v','libx264','-pix_fmt','yuv420p','-crf','17','-movflags','+faststart',str(encoded)],
                       input=b''.join(item.tobytes() for item in frames),check=True)
        raw[variant] = subprocess.check_output([str(FFMPEG),'-hide_banner','-loglevel','error','-i',str(encoded),'-f','rawvideo','-pix_fmt','rgb24','-'])
    stride = SIZE[0]*SIZE[1]*3
    assert all(len(pixels)==FRAME_COUNT*stride for pixels in raw.values())
    from PIL import ImageChops
    assert all(frame(number,'small').tobytes()==frame(number,'large').tobytes() for number in range(CUT_FRAME))
    boxes = [ImageChops.difference(frame(number,'small'),frame(number,'large')).getbbox() for number in range(CUT_FRAME,FRAME_COUNT)]
    assert set(boxes)=={(178,151,286,210)}, set(boxes)
    board = Image.new('RGB',(960,564),'#181d25')
    labels = ImageDraw.Draw(board)
    for col,variant in enumerate(SCALES):
        for row,number in enumerate((23,48)):
            decoded = Image.frombytes('RGB',SIZE,raw[variant][number*stride:(number+1)*stride])
            board.paste(decoded,(480*col,282*row))
            labels.text((480*col+12,282*row+270),f'{variant} - frame {number}',fill='white')
    board.save(HERE/'decoded-contact-revised.png')
    metadata = {'size':list(SIZE),'fps':FPS,'frame_count_each':FRAME_COUNT,'cut_frame_zero_based':CUT_FRAME,'board_frames_zero_based':[23,48],
                'outdoor_scales':SCALES,'pre_cut_pixel_match_before_encoding':True,'outdoor_difference_bounds_xyxy_exclusive':list(boxes[0]),
                'audio':False,'observer_test':False}
    (HERE/'metadata-revised.json').write_text(json.dumps(metadata,indent=2)+'\n',encoding='utf-8')


if __name__=='__main__':
    run()
