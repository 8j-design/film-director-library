from pathlib import Path
import subprocess,json
from PIL import Image,ImageDraw
task=Path(__file__).resolve().parent;root=task/'本地参考/Mei再次拥抱-20261105';out=root/'关键转接';out.mkdir(exist_ok=True)
ff=task.parent/'研究媒体工具/imageio-ffmpeg/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe';source=root/'原发布7697316429544066344.mp4'
times=[13.5,14,14.5,15,15.5,20.25,20.5,20.75,21,21.25,21.5,27,27.25,27.5,27.75,28,28.25,28.5]
for start in range(0,len(times),6):
    batch=times[start:start+6];board=Image.new('RGB',(1280,((len(batch)+1)//2)*504),'#202020');d=ImageDraw.Draw(board)
    for j,t in enumerate(batch):
        dest=out/f'{t:g}.png';assert not dest.exists()
        subprocess.run([str(ff),'-hide_banner','-loglevel','error','-ss',str(t),'-i',str(source),'-frames:v','1','-vf','scale=640:480',str(dest)],check=True)
        x=(j%2)*640;y=(j//2)*504;board.paste(Image.open(dest),(x,y+24));d.text((x+8,y+4),f'{t:.2f}s nominal / source original',fill='white')
    board.save(out/f'board{start//6+1}.png')
(out/'metadata.json').write_text(json.dumps({'times':times,'source_url':'https://www.douyin.com/video/7697316429544066344','generated_only_not_viewing_claim':True,'unique_total_with_1s_grid':len(set(times)|set(range(31))),'boundary':'selected bottle and transition stills; not exact cuts or whole motion/audio'},ensure_ascii=False,indent=2),encoding='utf-8');print({'samples':18,'boards':3,'unique_with_previous31':44})
