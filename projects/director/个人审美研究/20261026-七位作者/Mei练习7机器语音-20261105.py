from pathlib import Path
import subprocess,sys,json,wave,time
import numpy as np
task=Path(__file__).resolve().parent;workspace=task.parent
sys.path.insert(0,str(workspace/'研究媒体工具/faster-whisper'))
from faster_whisper import WhisperModel
root=task/'本地参考/Mei练习67-20261105';out=root/'练习7机器音轨';out.mkdir(exist_ok=True)
assert not (out/'machine-asr.json').exists()
ff=workspace/'研究媒体工具/imageio-ffmpeg/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
subprocess.run([str(ff),'-hide_banner','-loglevel','error','-i',str(root/'练习7-7702285485346934079.mp4'),'-vn','-ac','1','-ar','16000',str(out/'mono16k.wav')],check=True)
model=WhisperModel('small',device='cpu',compute_type='int8',cpu_threads=4,download_root=str(workspace/'研究媒体工具/whisper-models'))
with wave.open(str(out/'mono16k.wav'),'rb') as w:samples=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(np.float32)/32768.0
start=time.monotonic();seg,info=model.transcribe(samples,language=None,beam_size=5,condition_on_previous_text=False,vad_filter=True)
rows=[{'start':s.start,'end':s.end,'machine_unverified':s.text,'avg_logprob':s.avg_logprob,'no_speech_prob':s.no_speech_prob} for s in seg]
r={'source_url':'https://www.douyin.com/video/7702285485346934079','model':'faster-whisper small CPU int8','audio_frames':len(samples),'sample_rate':16000,'automatic_language':info.language,'language_probability':info.language_probability,'elapsed':round(time.monotonic()-start,2),'segments':rows,'boundary':'machine only; music/effects/crying can cause hallucination; not human listening or verified dialogue'}
(out/'machine-asr.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(r,ensure_ascii=False))
