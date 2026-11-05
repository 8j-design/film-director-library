from pathlib import Path
import subprocess,json
from PIL import Image,ImageDraw
root=Path(__file__).resolve().parent/'本地参考/M-P3-20261102'
out=root/'机器语音1380-1680-20261104/回字幕';out.mkdir(exist_ok=True)
ff=Path(__file__).resolve().parents[1]/'研究媒体工具/imageio-ffmpeg/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
times=[1381,1387,1393,1400,1406,1411,1415,1420,1424,1428,1433,1438,1443,1448,1454,1460,1465,1470,1477,1483,1488,1493,1498,1503,1507,1512,1516,1520,1525,1530,1536,1544,1550,1558,1565,1573,1579,1584,1589,1594,1598,1604,1608,1612,1616,1620,1625,1629,1635,1643,1648,1653,1658,1663,1668,1673,1678]
for start in range(0,len(times),9):
    batch=times[start:start+9];board=Image.new('RGB',(1280,len(batch)*125),'#202020');d=ImageDraw.Draw(board)
    for j,t in enumerate(batch):
        p=out/f'字幕{t}.png';assert not p.exists()
        subprocess.run([str(ff),'-hide_banner','-loglevel','error','-ss',str(t),'-i',str(root/'原发布7672707839571283242.mp4'),'-frames:v','1','-vf','crop=1920:150:0:930,scale=1280:100',str(p)],check=True)
        board.paste(Image.open(p),(0,j*125+24));d.text((8,j*125+4),f'nominal {t//60}:{t%60:02} / seek not exact PTS',fill='white')
    board.save(out/f'board{start//9+1}.png')
for t in [1415,1465,1507,1579,1604,1658,1668]:
    p=out/f'全图{t}.png';assert not p.exists()
    subprocess.run([str(ff),'-hide_banner','-loglevel','error','-ss',str(t),'-i',str(root/'原发布7672707839571283242.mp4'),'-frames:v','1','-vf','scale=960:540',str(p)],check=True)
(out/'metadata.json').write_text(json.dumps({'source':'https://www.douyin.com/video/7672707839571283242','subtitle_nominal_seconds':times,'full_context_seconds':[1415,1465,1507,1579,1604,1658,1668],'boundary':'57 subtitle samples and 7 context frames; not continuous viewing or listening'},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print({'subtitle_positions':len(times),'full_contexts':7})
