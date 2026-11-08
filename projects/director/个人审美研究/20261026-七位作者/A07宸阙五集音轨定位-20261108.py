from pathlib import Path
from hashlib import sha256
import json
import subprocess
import re
import numpy as np

here=Path('新工作/个人审美与风格研究-20261026')
root=here/'本地参考/A07-宸阙观古-20261104'
ff=next(Path('新工作/研究媒体工具').rglob('ffmpeg-win-x86_64-v7.1.exe'))
rate=16000
hop=160
width=640
anchors={1:[1.533333,4,7.066667,9.666667,10.866667,13.366667,16.6,18.566667,20.933333],2:[14.066667,14.4,27.5,29.433333,33.5],3:[3.466667,6.066667,8.133333,9.6,13.033333,14.133333,15.633333,17.133333,19.4,22.066667,22.433333,23.333333,23.666667,25.766667,28.033333],4:[10.033333,18.8,21.7,26.6,29.733333],5:[6.5,12.2,15.9,24.933333,28.933333]}
report={'sample_rate':rate,'hop_s':hop/rate,'spectral_window_s':width/rate,'anchors_s':anchors,'episodes':{}}
def measure(source,n):
    info=subprocess.run([str(ff),'-hide_banner','-i',str(source)],capture_output=True,text=True,encoding='utf-8',errors='replace').stderr
    raw=subprocess.check_output([str(ff),'-v','error','-i',str(source),'-map','0:a:0','-af','aresample=16000:first_pts=0','-ac','1','-c:a','pcm_f32le','-f','f32le','-'])
    x=np.frombuffer(raw,dtype='<f4')
    rows=np.lib.stride_tricks.sliding_window_view(x,width)[::hop]
    r=20*np.log10(np.maximum(np.sqrt(np.mean(rows**2,axis=1)),1e-8))
    spec=np.log1p(np.abs(np.fft.rfft(rows*np.hanning(width),axis=1))*20)
    flux=np.maximum(np.diff(spec,axis=0),0).mean(axis=1)
    ts=(np.arange(len(flux))*hop+width/2+hop/2)/rate
    pct=float(np.percentile(flux,95))
    local=(flux[1:-1]>flux[:-2]) & (flux[1:-1]>=flux[2:]) & (flux[1:-1]>=pct)
    peak_idx=np.flatnonzero(local)+1
    tests=[]
    for s in anchors[n]:
        around=np.flatnonzero(abs(ts-s)<=.15)
        nearest=int(peak_idx[np.argmin(abs(ts[peak_idx]-s))])
        tests.append({'visual_s':s,'nearest_top_5pct_local_rise_s':round(float(ts[nearest]),4),
           'delta_s':round(float(ts[nearest]-s),4),'within_150ms':bool(abs(ts[nearest]-s)<=.15),
           'window_flux_percentile':round(float(100*np.mean(flux<=flux[around].max())),1)})
    def db(v):return round(float(20*np.log10(max(np.sqrt(np.mean(v**2)),1e-8))),2)
    def interval(s,e):return db(x[round(s*rate):round(e*rate)])
    return {'source':source.name,'source_sha256':sha256(source.read_bytes()).hexdigest(),'duration_audio_s':len(x)/rate,
       'container_header':next((line.strip() for line in info.splitlines() if 'Duration:' in line),None),
       'stream_headers':[line.strip() for line in info.splitlines() if re.search(r'Stream #0:\d.*(Video:|Audio:)',line)],
       'start_250ms_dbfs':interval(0,.25),'e3_black_tail_dbfs':interval(28.033333,len(x)/rate) if n==3 else None,'end_250ms_dbfs':interval(len(x)/rate-.25,len(x)/rate),
       'final_seconds_quarter_dbfs':[interval(len(x)/rate-j*.25,len(x)/rate-(j-1)*.25) for j in range(8,0,-1)],
       'flux_p95':pct,'top_local_rises_count':len(peak_idx),
       'flux_peaks_s':[round(float(ts[j]),4) for j in peak_idx],
       'fraction_track_within_150ms_of_peak':round(float(np.mean(np.any(abs(ts[:,None]-ts[peak_idx])<=.15,axis=1))),3),
       'visual_anchor_tests':tests}
for n in anchors:
    report['episodes'][n]=measure(next(root.glob(f'E{n}-*.mp4')),n)
f=here/'A07宸阙五集音轨定位元信息-20261108.json'
f.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for n,e in report['episodes'].items():
    print(n,e['duration_audio_s'],e['e3_black_tail_dbfs'],e['final_seconds_quarter_dbfs'],e['fraction_track_within_150ms_of_peak'],sum(t['within_150ms'] for t in e['visual_anchor_tests']),len(e['visual_anchor_tests']))
    print([(a['visual_s'],a['delta_s'],a['window_flux_percentile']) for a in e['visual_anchor_tests']])
