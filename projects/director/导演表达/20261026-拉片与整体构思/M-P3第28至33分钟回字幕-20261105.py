from pathlib import Path
import subprocess,json
from PIL import Image,ImageDraw
root=Path(__file__).resolve().parent/'本地参考/M-P3-20261102'
out=root/'机器语音1680-1980-20261104/回字幕';out.mkdir(exist_ok=True)
ff=Path(__file__).resolve().parents[1]/'研究媒体工具/imageio-ffmpeg/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
times=[1682,1687,1694,1698,1704,1709,1713,1720,1726,1732,1738,1743,1749,1753,1757,1766,1771,1775,1779,1783,1791,1797,1803,1808,1813,1817,1821,1825,1832,1837,1847,1852,1857,1862,1867,1872,1877,1882,1888,1895,1901,1905,1910,1915,1920,1925,1930,1936,1941,1946,1951,1955,1960,1967,1973,1978]
contexts=[1682,1743,1753,1821,1837,1862,1901,1936,1978]
for start in range(0,len(times),9):
    batch=times[start:start+9];board=Image.new('RGB',(1280,len(batch)*125),'#202020');d=ImageDraw.Draw(board)
    for j,t in enumerate(batch):
        p=out/f'字幕{t}.png';assert not p.exists()
        subprocess.run([str(ff),'-hide_banner','-loglevel','error','-ss',str(t),'-i',str(root/'原发布7672707839571283242.mp4'),'-frames:v','1','-vf','crop=1920:150:0:930,scale=1280:100',str(p)],check=True)
        board.paste(Image.open(p),(0,j*125+24));d.text((8,j*125+4),f'nominal {t//60}:{t%60:02} / seek not exact PTS',fill='white')
    board.save(out/f'board{start//9+1}.png')
for t in contexts:
    p=out/f'全图{t}.png';assert not p.exists()
    subprocess.run([str(ff),'-hide_banner','-loglevel','error','-ss',str(t),'-i',str(root/'原发布7672707839571283242.mp4'),'-frames:v','1','-vf','scale=960:540',str(p)],check=True)
(out/'metadata.json').write_text(json.dumps({'source':'https://www.douyin.com/video/7672707839571283242','subtitle_nominal_seconds':times,'full_context_seconds':contexts,'boundary':'56 subtitle samples and 9 context frames; not continuous viewing or listening'},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print({'subtitle_positions':len(times),'full_contexts':len(contexts)})
