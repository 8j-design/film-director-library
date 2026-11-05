from pathlib import Path
import subprocess,json,hashlib
from PIL import Image,ImageDraw
a=Path(__file__).resolve().parent;root=a/'本地参考/ty7h告别-20261105';out=root/'逐秒';out.mkdir(exist_ok=True)
ff=a.parent/'研究媒体工具/imageio-ffmpeg/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe';source=root/'原发布7681397912714202410.mp4'
times=list(range(30))+[29.9]
for start in range(0,len(times),6):
    batch=times[start:start+6];board=Image.new('RGB',(1280,((len(batch)+1)//2)*504),'#202020');d=ImageDraw.Draw(board)
    for j,t in enumerate(batch):
        dest=out/f'{t:g}.png';assert not dest.exists()
        subprocess.run([str(ff),'-hide_banner','-loglevel','error','-ss',str(t),'-i',str(source),'-frames:v','1','-vf','scale=640:480',str(dest)],check=True)
        x=j%2*640;y=j//2*504;board.paste(Image.open(dest),(x,y+24));d.text((x+8,y+4),f'{t:g}s nominal / credited creator original',fill='white')
    board.save(out/f'board{start//6+1}.png')
meta={'source_url':'https://www.douyin.com/video/7681397912714202410','publisher':'ty7h嘉','title':'当你要经历一次最难的告别','publication_time_on_page':'2026-09-04 10:26','page_declaration':'内容由AI生成','source_duration':29.958333,'dimensions':[1440,1080],'fps':24,'bytes':source.stat().st_size,'sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'positions':times,'boards':6,'relation':'candidate original on creator explicitly credited by MeiGc; formal comparison separately determines confidence','limits':'selected visual positions, no full audio or continuous motion; last0.058333s unresolved; no engineering/prompt ownership verified'}
(root/'metadata.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf-8');print({'positions':31,'boards':6})
