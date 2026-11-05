from pathlib import Path
import subprocess,json,hashlib
from PIL import Image,ImageDraw
root=Path(__file__).resolve().parent
ff=root.parents[1]/'研究媒体工具/imageio-ffmpeg/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
times=[0,.8,1.6,2.4,3.2,4,4.6,5.2,5.4,5.8,6.2,6.5,6.7,7.2,7.95]
results=[]
for version in range(1,5):
    path=root/f'v{version}/assembly.mp4';out=root/f'v{version}/decoded';out.mkdir(exist_ok=True)
    raw=subprocess.check_output([str(ff),'-v','error','-i',str(path),'-f','rawvideo','-pix_fmt','rgb24','-an','-'])
    size=960*540*3;assert len(raw)%size==0
    count=len(raw)//size;assert count==192
    selected=times if version==4 else [6.2,6.5,6.7]
    for t in selected:
        n=round(t*24);im=Image.frombytes('RGB',(960,540),raw[n*size:(n+1)*size]);im.save(out/f'frame{n}.png')
    for start in range(0,len(selected),6):
        batch=selected[start:start+6];board=Image.new('RGB',(1440,426*((len(batch)+1)//2)),'#292e2b')
        for k,t in enumerate(batch):
            n=round(t*24);im=Image.open(out/f'frame{n}.png');board.paste(im.resize((720,405)),(k%2*720,k//2*426+21));ImageDraw.Draw(board).text((k%2*720+8,k//2*426+2),f'V{version} frame {n}, actual {n/24:.4f}s',fill='white')
        board.save(out/f'board{start//6+1}.png')
    results.append({'version':version,'decoded_frames':count,'decoded_frame_bytes':len(raw),'nominal_selected_seconds':selected,'actual_frame_indices':[round(t*24) for t in selected],'actual_selected_seconds':[round(t*24)/24 for t in selected],'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'human_continuous_viewing':False,'selected_images_review':'pending visual inspection'})
(root/'encoded-verification.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(results,ensure_ascii=False))
