from pathlib import Path
import subprocess,json,hashlib
from PIL import Image,ImageDraw
task=Path(__file__).resolve().parent;root=task/'本地参考/Mei再次拥抱-20261105';out=root/'逐秒';out.mkdir(exist_ok=True)
ff=task.parent/'研究媒体工具/imageio-ffmpeg/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe';source=root/'原发布7697316429544066344.mp4'
times=list(range(31))
for start in range(0,len(times),6):
    batch=times[start:start+6];board=Image.new('RGB',(1280,((len(batch)+1)//2)*504),'#202020');d=ImageDraw.Draw(board)
    for j,t in enumerate(batch):
        dest=out/f'{t:02}.png';assert not dest.exists()
        subprocess.run([str(ff),'-hide_banner','-loglevel','error','-ss',str(t),'-i',str(source),'-frames:v','1','-vf','scale=640:480',str(dest)],check=True)
        x=(j%2)*640;y=(j//2)*504;board.paste(Image.open(dest),(x,y+24));d.text((x+8,y+4),f'{t:02}s nominal seek / source original',fill='white')
    board.save(out/f'board{start//6+1}.png')
meta={'source_url':'https://www.douyin.com/video/7697316429544066344','publisher':'MeiGc（梅干菜）','page_title':'当你终于有机会，再次拥抱最爱的人','publication_time_on_page':'2026-10-17 08:00','page_declaration':'内容由AI生成','author_credit':'灵感参考@ty7h嘉，小小改编','series':'练习第5集，页面同目录可见2—7集，非全作者覆盖','DOM_duration_seconds':30.046009,'bytes':source.stat().st_size,'sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'visual_nominal_seconds':times,'boards_generated':6,'read_status':'generated, actual viewing logged separately','limits':'1s grid, no continuous audiovisual claim; 0.046009s tail and motion between samples unresolved; original project/model/prompt unverified'}
(root/'metadata.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf-8')
print({'samples':31,'boards':6})
