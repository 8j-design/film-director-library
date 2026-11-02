from pathlib import Path
import subprocess
from PIL import Image,ImageDraw
root=Path(__file__).resolve().parent/'本地参考/M-P3-20261102';out=root/'机器语音0-180-20261102/回字幕';out.mkdir(exist_ok=True)
ff='C:/Users/scvfv/Documents/ChatGPT/导演/新工作/研究媒体工具/imageio-ffmpeg/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
times=[6,12,14,26,29,43,66,73,78,94,102,107,112,151,167,175,179]
for start in range(0,len(times),9):
 batch=times[start:start+9];board=Image.new('RGB',(1280,len(batch)*125),'#202020');d=ImageDraw.Draw(board)
 for j,t in enumerate(batch):
  p=out/f'字幕{t}.png';assert not p.exists()
  subprocess.run([ff,'-hide_banner','-loglevel','error','-ss',str(t),'-i',str(root/'原发布7672707839571283242.mp4'),'-frames:v','1','-vf','crop=1920:150:0:930,scale=1280:100',str(p)],check=True)
  board.paste(Image.open(p),(0,j*125+24));d.text((8,j*125+4),f'nominal {t//60}:{t%60:02} / seek not exact PTS',fill='white')
 board.save(out/f'board{start//9+1}.png')
for t in [94,102,107]:
 p=out/f'全图{t}.png';assert not p.exists()
 subprocess.run([ff,'-hide_banner','-loglevel','error','-ss',str(t),'-i',str(root/'原发布7672707839571283242.mp4'),'-frames:v','1','-vf','scale=960:540',str(p)],check=True)
print({'subtitle_positions':len(times),'full_frame_contexts':3,'not_complete_audiovisual':True})
