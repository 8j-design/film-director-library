from pathlib import Path
import json,math,subprocess,hashlib
r=Path(__file__).resolve().parent;ff=r.parents[1]/'研究媒体工具/imageio-ffmpeg/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
rows=json.loads((r/'V5V6实际输出元信息.json').read_text(encoding='utf-8'));checks=[]
for row in rows:
 v=row['version'];p=r/f'点到即止-V{v}.mp4'
 decoded=subprocess.run([str(ff),'-v','error','-i',str(p),'-f','null','-'],capture_output=True,text=True)
 assert decoded.returncode==0 and not decoded.stderr,decoded.stderr
 distances=[]
 for contact in row['contact_geometry']:
  _,a,_,b=contact['swords'];distances.append(math.dist(a,b))
 assert max(distances)<1e-6
 checks.append({'version':v,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'video_and_audio_decode':True,'tip_distance_at_planned_contact_pixels':max(distances),'contact_pose_frames':len(distances),'limitations':'geometry/decode/keypose review only; no full playback quality or audio listening pass'})
(r/'核验输出.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(checks,ensure_ascii=False))
