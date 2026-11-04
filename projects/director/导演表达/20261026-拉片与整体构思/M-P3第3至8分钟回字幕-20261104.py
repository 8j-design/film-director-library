from pathlib import Path
import subprocess,json
from PIL import Image,ImageDraw
root=Path(__file__).resolve().parent/'本地参考/M-P3-20261102'
out=root/'机器语音180-480-20261104/回字幕';out.mkdir(exist_ok=True)
ff='C:/Users/scvfv/Documents/ChatGPT/导演/新工作/研究媒体工具/imageio-ffmpeg/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
times=[183,190,196,201,204,210,213,216,218,225,239,244,249,253,256,259,263,271,274,283,288,296,301,312,314,333,345,349,353,355,359,367,370,375,384,392,399,405,418,423,429,437,440,449,451,462,465,470,474,479]
for start in range(0,len(times),9):
    batch=times[start:start+9];board=Image.new('RGB',(1280,len(batch)*125),'#202020');d=ImageDraw.Draw(board)
    for j,t in enumerate(batch):
        p=out/f'字幕{t}.png';assert not p.exists()
        subprocess.run([ff,'-hide_banner','-loglevel','error','-ss',str(t),'-i',str(root/'原发布7672707839571283242.mp4'),'-frames:v','1','-vf','crop=1920:150:0:930,scale=1280:100',str(p)],check=True)
        board.paste(Image.open(p),(0,j*125+24));d.text((8,j*125+4),f'nominal {t//60}:{t%60:02} / seek not exact PTS',fill='white')
    board.save(out/f'board{start//9+1}.png')
for t in [312,367,429]:
    p=out/f'全图{t}.png';assert not p.exists()
    subprocess.run([ff,'-hide_banner','-loglevel','error','-ss',str(t),'-i',str(root/'原发布7672707839571283242.mp4'),'-frames:v','1','-vf','scale=960:540',str(p)],check=True)
(out/'metadata.json').write_text(json.dumps({'source':'https://www.douyin.com/video/7672707839571283242','subtitle_nominal_seconds':times,'full_context_seconds':[312,367,429],'boundary':'50 subtitle samples plus 3 context frames; not continuous viewing or listening'},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print({'subtitle_positions':len(times),'full_contexts':3})
