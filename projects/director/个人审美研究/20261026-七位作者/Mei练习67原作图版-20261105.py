from pathlib import Path
import subprocess,json,hashlib
from PIL import Image,ImageDraw
a=Path(__file__).resolve().parent;root=a/'本地参考/Mei练习67-20261105';ff=a.parent/'研究媒体工具/imageio-ffmpeg/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
six=root/'练习6逐帧';six.mkdir(exist_ok=True);assert not list(six.glob('f*.png'))
source6=root/'练习6-7701738751680122139.mp4'
subprocess.run([str(ff),'-hide_banner','-loglevel','error','-i',str(source6),'-vsync','0','-vf','scale=480:270','-start_number','0',str(six/'f%04d.png')],check=True)
frames=sorted(six.glob('f*.png'))
for start in range(0,len(frames),12):
    batch=frames[start:start+12];board=Image.new('RGB',(1440,((len(batch)+2)//3)*294),'#202020');d=ImageDraw.Draw(board)
    for j,p in enumerate(batch):
        x=j%3*480;y=j//3*294;board.paste(Image.open(p),(x,y+24));d.text((x+6,y+4),f'decoded {start+j:03} / index30fps {((start+j)/30):.3f}s not PTS',fill='white')
    board.save(six/f'board{start//12+1}.png')
for t in [0,2.5,5.05]:
    subprocess.run([str(ff),'-hide_banner','-loglevel','error','-ss',str(t),'-i',str(source6),'-frames:v','1',str(six/f'full{t:g}.png')],check=True)
seven=root/'练习7半秒';seven.mkdir(exist_ok=True);times=[i/2 for i in range(60)]+[29.95];source7=root/'练习7-7702285485346934079.mp4'
for start in range(0,len(times),6):
    batch=times[start:start+6];board=Image.new('RGB',(1280,((len(batch)+1)//2)*384),'#202020');d=ImageDraw.Draw(board)
    for j,t in enumerate(batch):
        p=seven/f'{t:g}.png';assert not p.exists()
        subprocess.run([str(ff),'-hide_banner','-loglevel','error','-ss',str(t),'-i',str(source7),'-frames:v','1','-vf','scale=640:360',str(p)],check=True)
        x=j%2*640;y=j//2*384;board.paste(Image.open(p),(x,y+24));d.text((x+6,y+4),f'{t:g}s nominal / source original',fill='white')
    board.save(seven/f'board{start//6+1}.png')
sources=[]
for p,vid,title,date,duration in [(source6,'7701738751680122139','仿33号远征队','2026-10-28 23:20',5.085011),(source7,'7702285485346934079','LibTV广告尝试','2026-10-30 10:41',30)]:
    sources.append({'url':'https://www.douyin.com/video/'+vid,'title':title,'publisher':'MeiGc（梅干菜）','publication_time_on_page':date,'DOM_duration_seconds':duration,'dimensions':[1024,576],'fps':30,'page_declaration':'内容由AI生成','bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
meta={'sources':sources,'six_decoded_frames':len(frames),'six_boards':(len(frames)+11)//12,'six_full_context_nominal_seconds':[0,2.5,5.05],'seven_halfsecond_positions':times,'seven_boards':11,'generated_only_not_viewing_claim':True,'limits':'decoded-frame contact sheets do not prove sound, detailed motion physics or game source match; half-second episode7 gaps remain; no source media upload'}
(root/'metadata.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf-8');print({k:v for k,v in meta.items() if k not in ['sources','seven_halfsecond_positions']})
