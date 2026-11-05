from pathlib import Path
import subprocess,json
from PIL import Image,ImageDraw
root=Path(__file__).resolve().parent/'本地参考/M-P3-20261102'
out=root/'机器语音1080-1380-20261104/回字幕';out.mkdir(exist_ok=True)
ff='C:/Users/scvfv/Documents/ChatGPT/导演/新工作/研究媒体工具/imageio-ffmpeg/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
times=[1080,1088,1093,1099,1103,1108,1112,1116,1126,1132,1136,1159,1164,1168,1175,1181,1195,1200,1204,1209,1225,1230,1251,1256,1260,1266,1271,1275,1280,1287,1291,1294,1304,1308,1310,1319,1323,1327,1337,1342,1349,1353,1357,1362,1366,1369,1372,1375,1378,1379]
for start in range(0,len(times),9):
    batch=times[start:start+9];board=Image.new('RGB',(1280,len(batch)*125),'#202020');d=ImageDraw.Draw(board)
    for j,t in enumerate(batch):
        p=out/f'字幕{t}.png';assert not p.exists()
        subprocess.run([ff,'-hide_banner','-loglevel','error','-ss',str(t),'-i',str(root/'原发布7672707839571283242.mp4'),'-frames:v','1','-vf','crop=1920:150:0:930,scale=1280:100',str(p)],check=True)
        board.paste(Image.open(p),(0,j*125+24));d.text((8,j*125+4),f'nominal {t//60}:{t%60:02} / seek not exact PTS',fill='white')
    board.save(out/f'board{start//9+1}.png')
for t in [1108,1271,1357,1369]:
    p=out/f'全图{t}.png';assert not p.exists()
    subprocess.run([ff,'-hide_banner','-loglevel','error','-ss',str(t),'-i',str(root/'原发布7672707839571283242.mp4'),'-frames:v','1','-vf','scale=960:540',str(p)],check=True)
(out/'metadata.json').write_text(json.dumps({'source':'https://www.douyin.com/video/7672707839571283242','subtitle_nominal_seconds':times,'full_context_seconds':[1108,1271,1357,1369],'boundary':'50 subtitle samples plus 4 context frames; not continuous viewing or listening'},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print({'subtitle_positions':len(times),'full_contexts':4})
