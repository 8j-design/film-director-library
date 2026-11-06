from pathlib import Path
import sys,json,subprocess,wave,time
from PIL import Image,ImageDraw
t=Path(__file__).resolve().parent;r=t/'本地参考/Mei练习1-20261106';src=r/'Mei练习1-7669468328963919138.mp4';ff=t.parent/'研究媒体工具/imageio-ffmpeg/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
if sys.argv[1]=='asr':
    sys.path.insert(0,str(t.parent/'研究媒体工具/faster-whisper'));from faster_whisper import WhisperModel
    import numpy as np
    wav=r/'mono16k.wav';dest=r/'machine-asr.json';assert not dest.exists()
    subprocess.run([str(ff),'-hide_banner','-loglevel','error','-i',str(src),'-vn','-ac','1','-ar','16000',str(wav)],check=True)
    with wave.open(str(wav),'rb') as w:samples=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(np.float32)/32768.0
    start=time.time();model=WhisperModel('small',device='cpu',compute_type='int8',cpu_threads=4,download_root=str(t.parent/'研究媒体工具/whisper-models'))
    segs,info=model.transcribe(samples,language='zh',vad_filter=True,condition_on_previous_text=False)
    rows=[{'start_seconds':v.start,'end_seconds':v.end,'text_machine_unverified':v.text} for v in segs]
    j={'segments':rows,'elapsed_seconds':round(time.time()-start,2),'boundary':'machine index only; no original listening claim'};dest.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(j)
elif sys.argv[1]=='frames':
    out=r/'转场与结尾补核';out.mkdir(exist_ok=True);intervals=[]
    for begin,end in [(9.5,12.5),(26.5,29)]:
        d=out/f'连续{begin:g}-{end:g}';d.mkdir();filt=f'select=gte(t\\,{begin})*lt(t\\,{end}),scale=450:192'
        subprocess.run([str(ff),'-hide_banner','-loglevel','error','-i',str(src),'-vf',filt,'-vsync','0',str(d/'frame%04d.png')],check=True)
        frames=sorted(d.glob('frame*.png'));assert frames
        for s in range(0,len(frames),16):
            batch=frames[s:s+16];board=Image.new('RGB',(1800,214*((len(batch)+3)//4)),'#202020');draw=ImageDraw.Draw(board)
            for k,p in enumerate(batch):
                x=k%4*450;y=k//4*214;board.paste(Image.open(p),(x,y+22));draw.text((x+5,y+4),f'interval {begin:g}-{end:g}s decoded #{s+k}',fill='white')
            board.save(d/f'board{s//16+1}.png')
        intervals.append({'start_seconds':begin,'end_seconds_exclusive':end,'decoded_frames':len(frames),'boards_generated':(len(frames)+15)//16,'folder':d.name})
    times=[0,2,9,12.5,16,19,20,24,25,28,29,31.5,32.4]
    for s in range(0,len(times),6):
        batch=times[s:s+6];board=Image.new('RGB',(1352,312*((len(batch)+1)//2)),'#202020');draw=ImageDraw.Draw(board)
        for k,z in enumerate(batch):
            dest=out/f'context{z:g}.png';assert not dest.exists()
            subprocess.run([str(ff),'-hide_banner','-loglevel','error','-ss',str(z),'-i',str(src),'-frames:v','1','-vf','scale=676:288',str(dest)],check=True);assert dest.exists()
            x=k%2*676;y=k//2*312;board.paste(Image.open(dest),(x,y+24));draw.text((x+5,y+4),f'nominal {z:g}s; seek not exact PTS',fill='white')
        board.save(out/f'context-board{s//6+1}.png')
    j={'intervals':intervals,'context_positions':times,'context_boards_generated':3,'generated_not_yet_viewed':True,'boundary':'decoded all source frames in selected intervals, no inferred source frame rate; no audio/full AV claim'}
    (out/'metadata.json').write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(j)
else:raise ValueError(sys.argv[1])
