from pathlib import Path
import subprocess,json
from PIL import Image,ImageDraw
root=Path(__file__).resolve().parent/'本地参考/M-P3-20261102'
out=root/'机器语音1980-2256-20261104/回字幕';out.mkdir(exist_ok=True)
ff=Path(__file__).resolve().parents[1]/'研究媒体工具/imageio-ffmpeg/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
times=[1981,1985,1990,1996,2001,2006,2011,2016,2020,2024,2030,2035,2040,2046,2052,2058,2063,2068,2073,2078,2083,2088,2093,2098,2103,2108,2113,2118,2123,2128,2134,2138,2143,2148,2153,2157,2163,2168,2173,2178,2183,2188,2193,2198,2203,2208,2213,2218,2223,2228,2233,2238,2243,2248,2253,2255]
contexts=[1985,2040,2088,2128,2157,2178,2208,2218,2248,2255]
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
(out/'metadata.json').write_text(json.dumps({'source':'https://www.douyin.com/video/7672707839571283242','subtitle_nominal_seconds':times,'full_context_seconds':contexts,'boundary':'56 subtitle samples and 10 context frames; not continuous viewing or listening'},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print({'subtitle_positions':len(times),'full_contexts':len(contexts)})
