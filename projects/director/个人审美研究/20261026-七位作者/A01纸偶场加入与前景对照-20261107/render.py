from pathlib import Path
import argparse
import json
import subprocess

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent
WORKSPACE = ROOT.parent.parent
FFMPEG = WORKSPACE / '研究媒体工具/imageio-ffmpeg/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
WIDTH, HEIGHT, FPS, FRAMES = 768, 432, 24, 60
VARIANTS = {
    'A': (18, False),
    'B': (26, False),
    'C': (18, True),
    'D': (26, True),
}


def ramp(frame, start, duration):
    p = min(1, max(0, (frame - start) / duration))
    return p * p * (3 - 2 * p)


def link(draw, points, color, width):
    draw.line(points, fill=color, width=width, joint='curve')
    x, y = points[-1]
    draw.ellipse((x-8, y-8, x+8, y+8), fill='#f3bf91')


def technician(draw, x, outfit, cap, face, lift):
    draw.rounded_rectangle((x-46, 218, x+46, 367), radius=23, fill=outfit)
    draw.rectangle((x-27, 337, x+27, 367), fill='#344755')
    draw.ellipse((x-26, 173, x+26, 229), fill=face)
    draw.rounded_rectangle((x-30, 164, x+27, 188), radius=10, fill=cap)
    draw.line((x-26, 184, x+35, 184), fill=cap, width=8)
    for direction in (-1, 1):
        eye = x + direction * 9
        draw.ellipse((eye-2, 194, eye+2, 198), fill='#29333b')
        shoulder = (x + direction * 33, 238)
        elbow = (x + direction * (61 + 9 * lift), 280 - 61 * lift)
        hand = (x + direction * (48 + 28 * lift), 324 - 155 * lift)
        link(draw, (shoulder, elbow, hand), outfit, 20)


def signal(draw, angle, scale, shade):
    x, y = 384, 289
    def pt(dx, dy):
        return round(x + scale * dx), round(y + scale * dy)

    draw.polygon([pt(-30, 0), pt(-28, -29), pt(-13, -44), pt(20, -44), pt(32, -23), pt(28, 0)], fill='#ef7c4a')
    draw.polygon([pt(-16, -30), pt(-11, -46), pt(10, -55), pt(23, -41), pt(13, -25)], fill='#ffb45e')
    draw.polygon([pt(21, -36), pt(39, -31), pt(22, -24)], fill='#ffdc91')
    draw.ellipse((*pt(11, -43), *pt(16, -38)), fill='#233143')
    for sign in (-1, 1):
        draw.line(
            [pt(sign * 15, -16), pt(sign * (40 + 5 * angle), -7 - 50 * angle),
             pt(sign * (53 + 4 * angle), 1 - 57 * angle)],
            fill=shade, width=max(1, round(7 * scale)),
        )
    draw.line([pt(-16, 0), pt(20, 0)], fill='#57352e', width=3)


def frame_image(frame, onset, enlarge, revision):
    img = Image.new('RGB', (WIDTH, HEIGHT), '#22384a')
    draw = ImageDraw.Draw(img)
    draw.rectangle((0, 62, WIDTH, 359), fill='#334f60')
    draw.rounded_rectangle((304, 62, 464, 197), radius=11, fill='#283e51', outline='#76959a', width=3)
    for x in (330, 366, 402, 438):
        draw.line((x, 73, x, 184), fill='#466474', width=2)
    draw.rectangle((0, 359, WIDTH, HEIGHT), fill='#283542')
    draw.line((0, 358, WIDTH, 358), fill='#729296', width=2)
    draw.ellipse((134, 341, 634, 388), fill='#253642')
    lift = ramp(frame, 18, 5) * (1 - ramp(frame, 50, 8))
    technician(draw, 185, '#92b6bc', '#527d83', '#f0c5a0', lift)
    technician(draw, 583, '#b2a1ce', '#6f6591', '#dba281', lift)
    draw.rounded_rectangle((301, 287, 467, 363), radius=9, fill='#9b755c')
    draw.rectangle((313, 300, 455, 352), outline='#be9676', width=2)
    draw.line((318, 349, 450, 303), fill='#7a5c51', width=4)
    flap = ramp(frame, onset, 5) * (1 - ramp(frame, 48, 8))
    if enlarge:
        extra = 1.30 if revision == 1 else 0.72
        scale = 1 + extra * ramp(frame, 33, 5) * (1 - ramp(frame, 45, 7))
    else:
        scale = 1.0
    signal(draw, flap, scale, '#ffc377')
    return img


def render_video(path, onset, enlarge, revision):
    args = [str(FFMPEG), '-y', '-v', 'error', '-f', 'rawvideo', '-pixel_format', 'rgb24',
            '-video_size', f'{WIDTH}x{HEIGHT}', '-framerate', str(FPS), '-i', 'pipe:0',
            '-an', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', str(path)]
    with subprocess.Popen(args, stdin=subprocess.PIPE) as process:
        for i in range(FRAMES):
            process.stdin.write(frame_image(i, onset, enlarge, revision).tobytes())
        process.stdin.close()
        if process.wait():
            raise RuntimeError(f'Encoding failed: {path.name}')


def contact_sheet(output, revision):
    times = (16, 23, 32, 40)
    page = Image.new('RGB', (1536, 928), '#15212b')
    draw = ImageDraw.Draw(page)
    for row, (label, (onset, enlarge)) in enumerate(VARIANTS.items()):
        for col, frame in enumerate(times):
            x, y = col * 384, row * 232
            page.paste(frame_image(frame, onset, enlarge, revision).resize((384, 216), Image.Resampling.LANCZOS), (x, y+16))
            draw.text((x+8, y+2), f'V{revision} {label}  frame {frame:02}', fill='white')
    page.save(output)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('revision', type=int, choices=(1, 2))
    args = parser.parse_args()
    revision = args.revision
    output = ROOT / f'V{revision}'
    output.mkdir(exist_ok=True)
    contact_sheet(output / 'contact.png', revision)
    for label, (onset, enlarge) in VARIANTS.items():
        render_video(output / f'{label}.mp4', onset, enlarge, revision)
    metadata = {
        'fps': FPS, 'frames_per_variant': FRAMES, 'human_lift_starts_at_frame': 18,
        'scale_starts_at_frame': 33, 'scale_returns_from_frame': 45,
        'enlargement_peak': 2.30 if revision == 1 else 1.72,
        'variants': {key: {'signal_lift_starts_at_frame': onset, 'signal_enlarges': scale}
                     for key, (onset, scale) in VARIANTS.items()},
        'audio': None, 'audience_test': None,
    }
    (output / 'metadata.json').write_text(json.dumps(metadata, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
