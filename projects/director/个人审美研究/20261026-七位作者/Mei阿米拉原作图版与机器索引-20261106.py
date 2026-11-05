from pathlib import Path
import subprocess,json,time,sys
from PIL import Image,ImageDraw
task=Path(__file__).resolve().parent;root=task/'本地参考/Mei阿米拉-20261106';src=root/'Mei阿米拉-7672920482366180642.mp4';ff=task.parent/'研究媒体工具/imageio-ffmpeg/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
mode=sys.argv[1]
if mode=='grid':
    out=root/'一秒全构图首轮';out.mkdir(exist_ok=True);times=list(range(88))+[87.9];times=sorted(times)
    for start in range(0,len(times),8):
        batch=times[start:start+8];board=Image.new('RGB',(1280,384*((len(batch)+1)//2)),'#202020');d=ImageDraw.Draw(board)
        for k,t in enumerate(batch):
            p=out/f'frame{t:g}.png';assert not p.exists()
            subprocess.run([str(ff),'-hide_banner','-loglevel','error','-ss',str(t),'-i',str(src),'-frames:v','1','-vf','scale=640:360',str(p)],check=True)
            assert p.exists();board.paste(Image.open(p),(k%2*640,k//2*384+24));d.text((k%2*640+10,k//2*384+5),f'nominal {t:g}s, seek not exact PTS',fill='white')
        board.save(out/f'board{start//8+1}.png')
    (out/'metadata.json').write_text(json.dumps({'nominal_positions':times,'boards_generated':(len(times)+7)//8,'boundary':'generated only, not read until actually viewed; includes blanks and transitions'},ensure_ascii=False,indent=2),encoding='utf-8');print({'images':len(times),'boards':(len(times)+7)//8})
elif mode=='asr':
    sys.path.insert(0,str(task.parent/'研究媒体工具/faster-whisper'))
    from faster_whisper import WhisperModel
    import wave,numpy as np
    wav=root/'mono16k.wav';dest=root/'machine-asr.json';assert not dest.exists()
    subprocess.run([str(ff),'-hide_banner','-loglevel','error','-i',str(src),'-vn','-ac','1','-ar','16000',str(wav)],check=True)
    with wave.open(str(wav),'rb') as w:samples=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(np.float32)/32768.0
    s=time.time();model=WhisperModel('small',device='cpu',compute_type='int8',cpu_threads=4,download_root=str(task.parent/'研究媒体工具/whisper-models'));segments,info=model.transcribe(samples,language='zh',vad_filter=True,condition_on_previous_text=False)
    rows=[{'start_seconds':v.start,'end_seconds':v.end,'text_machine_unverified':v.text,'avg_logprob':v.avg_logprob,'no_speech_prob':v.no_speech_prob} for v in segments]
    j={'source':'https://www.douyin.com/video/7672920482366180642','engine':'faster-whisper small cpu/int8 zh forced VAD','segments':rows,'elapsed_seconds':round(time.time()-s,2),'boundary':'machine index, not listening; names and dialogue remain unverified'}
    dest.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print({'segments':len(rows),'elapsed':j['elapsed_seconds']})
else:raise ValueError(mode)
