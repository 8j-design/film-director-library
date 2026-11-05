"""Local ASR only; never treats machine transcription as complete audiovisual viewing."""
from pathlib import Path
import sys,subprocess,json,time,importlib.metadata,wave,argparse
parser=argparse.ArgumentParser();parser.add_argument("--start",type=int,required=True);parser.add_argument("--end",type=int,required=True);args=parser.parse_args();assert 0<=args.start<args.end<=1856
workspace=Path(__file__).resolve().parents[1];deps=workspace/'研究媒体工具'/'faster-whisper';sys.path.insert(0,str(deps))
from faster_whisper import WhisperModel
import numpy as np
root=Path(__file__).resolve().parent/'本地参考'/'M老树新芽-20261105';out=root/f'机器语音{args.start}-{args.end}-20261105';out.mkdir(exist_ok=True)
ff=workspace/'研究媒体工具/imageio-ffmpeg/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
audio=out/'mono16k.wav'
assert not (out/'machine-asr.json').exists(),'Preserve existing transcription'
if not audio.exists():subprocess.run([str(ff),'-hide_banner','-loglevel','error','-ss',str(args.start),'-i',str(root/'M老树新芽-7641169894272175360.mp4'),'-t',str(args.end-args.start),'-vn','-ac','1','-ar','16000',str(audio)],check=True)
started=time.monotonic()
model=WhisperModel('small',device='cpu',compute_type='int8',cpu_threads=4,download_root=str(workspace/'研究媒体工具'/'whisper-models'))
with wave.open(str(audio),'rb') as w:
    assert w.getnchannels()==1 and w.getframerate()==16000 and w.getsampwidth()==2
    samples=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(np.float32)/32768.0
segments,info=model.transcribe(samples,language='zh',beam_size=5,condition_on_previous_text=False,vad_filter=True)
rows=[{'start_seconds':args.start+s.start,'end_seconds':args.start+s.end,'text_machine_unverified':s.text,'avg_logprob':s.avg_logprob,'no_speech_prob':s.no_speech_prob} for s in segments]
result={'source_url':'https://www.douyin.com/video/7641169894272175360','audio_start':args.start,'audio_end':args.end,'engine':'SYSTRAN/faster-whisper','version':importlib.metadata.version('faster-whisper'),'model':'small','device':'cpu/int8/4 threads','language_forced':'zh','elapsed_seconds':round(time.monotonic()-started,2),'segments':rows,'boundary':'machine ASR only; proper names and music/film dialogue may be wrong; no claim of listening or full AV; source remains local'}
(out/'machine-asr.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k!='segments'},ensure_ascii=False));print({'segments_written':len(rows)})
