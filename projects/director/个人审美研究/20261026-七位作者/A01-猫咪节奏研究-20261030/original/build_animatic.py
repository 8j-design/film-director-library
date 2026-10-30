"""把原创静帧排成可播放镜头草稿；不生成帧间角色运动或声音。"""
from pathlib import Path
import subprocess,json,hashlib
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parent
ffmpeg=ROOT.parents[2]/'研究媒体工具/imageio-ffmpeg/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
timings=[2.5,2,2,3,2.5]
reports=[]
for version in [1,2]:
    names=['establish.png','left-near.png','right-near.png' if version==1 else 'right-near-v2.png','bird-near.png' if version==1 else 'bird-near-v2.png','establish.png']
    cmd=[str(ffmpeg),'-y','-hide_banner','-loglevel','error']
    for name,duration in zip(names,timings):cmd+=['-loop','1','-framerate','24','-t',str(duration),'-i',str(ROOT/name)]
    parts=[]
    for i in range(5):parts.append(f'[{i}:v]trim=end_frame={int(timings[i]*24)},setpts=N/(24*TB),scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,setsar=1,format=yuv420p[v{i}]')
    parts.append(''.join(f'[v{i}]' for i in range(5))+'concat=n=5:v=1:a=0[out]')
    dest=ROOT/f'animatic-v{version}.mp4'
    cmd+=['-filter_complex',';'.join(parts),'-map','[out]','-an','-c:v','libx264','-crf','18','-preset','fast','-movflags','+faststart',str(dest)]
    subprocess.run(cmd,check=True,capture_output=True)
    checksum=ROOT/f'animatic-v{version}-frames.md5'
    subprocess.run([str(ffmpeg),'-y','-hide_banner','-loglevel','error','-i',str(dest),'-f','framemd5',str(checksum)],check=True,capture_output=True)
    count=len([s for s in checksum.read_text().splitlines() if s and not s.startswith('#')])
    assert count==288
    reports.append({'version':version,'shots':names,'durations':timings,'frames':count,'fps':24,'seconds':12,'size':[1280,720],'audio':False,'bytes':dest.stat().st_size,'sha256':hashlib.sha256(dest.read_bytes()).hexdigest()})
    # 这张仅是镜头时序查看表，不替代连续观看。
    sheet=Image.new('RGB',(1280,756),'#e9e5dc');d=ImageDraw.Draw(sheet)
    for k,name in enumerate(names):
        im=Image.open(ROOT/name).convert('RGB');im.thumbnail((640,360))
        x=(k%2)*640;y=(k//2)*252
        im.thumbnail((440,244));sheet.paste(im,(x,y+12));d.text((x+446,y+30),f'Shot {k+1}\n{timings[k]} sec',fill='#1c3136')
    sheet.save(ROOT/f'animatic-v{version}-shots.png')
(ROOT/'animatic-metadata.json').write_text(json.dumps({'scope':'Original still-shot animatic, no interpolated motion, no sound, no audience validation','versions':reports},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(reports,ensure_ascii=False))
