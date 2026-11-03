from pathlib import Path
import math,subprocess,wave,struct,json
from PIL import Image,ImageDraw,ImageFont
root=Path(__file__).resolve().parent
ff=root.parents[1]/'研究媒体工具/imageio-ffmpeg/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
font=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',19)
small=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',14)
W,H,FPS,N=900,506,24,192
def mix(a,b,u):return a+(b-a)*max(0,min(1,u))
def ease(u):u=max(0,min(1,u));return u*u*(3-2*u)
def params(t):
 if t<1.5:p=ease(t/1.5);return mix(300,340,p),mix(600,560,p),-70,-110,0
 if t<2.083333:q=ease((t-1.5)/.583333);return 340,560,mix(-70,-125,q),mix(-110,-80,q),mix(0,6,q)
 if t<2.5:q=ease((t-2.083333)/.416667);return 340,560,mix(-125,-30,q),mix(-80,-150,q),mix(6,12,q)
 if t<3.25:q=ease((t-2.5)/.75);return mix(340,330,q),mix(560,570,q),mix(-30,-65,q),mix(-150,-115,q),mix(12,0,q)
 if t<4.5:q=ease((t-3.25)/1.25);return 330,570,mix(-65,40,q),mix(-115,140,q),0
 q=ease((t-4.5)/1.5);return mix(330,295,q),mix(570,605,q),40,140,0
def draw_person(d,x,direction,angle,col,lean,t):
 hip=(x,342);shoulder=(x+direction*lean,238);head=(shoulder[0]+direction*4,205)
 d.ellipse((x-50,408,x+54,425),fill='#1c3039')
 step=math.sin(t*math.pi*1.7)*9 if t<1.5 or 4.5<t<6 else 0
 feet=[(x-28,415+step),(x+28,415-step)]
 for foot in feet:d.line([hip,((hip[0]+foot[0])/2,379),foot],fill=col,width=15)
 d.polygon([(shoulder[0]-19,238),(shoulder[0]+19,238),(x+35,358),(x-32,358)],fill=col)
 d.line([(shoulder[0]-17,263),(x-direction*26,307),(x-direction*35,332)],fill=col,width=13)
 hand=(x+direction*60,270)
 elbow=((shoulder[0]+hand[0])/2,255+abs(lean)*.3)
 d.line([shoulder,elbow,hand],fill=col,width=15)
 d.ellipse((head[0]-15,head[1]-19,head[0]+15,head[1]+19),fill='#bcae9c')
 d.pieslice((head[0]-17,head[1]-22,head[0]+17,head[1]+15),180,360,fill='#172a35')
 d.line([(head[0],head[1]+20),(head[0]-direction*30,head[1]+27)],fill=col,width=7)
 a=math.radians(angle);tip=(hand[0]+150*math.cos(a),hand[1]+150*math.sin(a))
 base=(hand[0]-16*math.cos(a),hand[1]-16*math.sin(a))
 d.line([base,hand],fill='#514c45',width=8)
 d.line([(hand[0]-9*math.sin(a),hand[1]+9*math.cos(a)),(hand[0]+9*math.sin(a),hand[1]-9*math.cos(a))],fill='#d0ae71',width=4)
 d.line([hand,tip],fill='#ecf0e9',width=4)
 return hand,tip
manifest=[]
for version,hold in [(1,0),(2,4)]:
 out=root/f'V{version}-帧';out.mkdir(exist_ok=True)
 assert not list(out.glob('f*.png'))
 selected=[];contacts=[]
 for f in range(N):
  warped=f if f<=60 else max(60,f-hold)
  t=warped/FPS;a,b,aa,bb,lean=params(t)
  im=Image.new('RGB',(W,H),'#293f4a');d=ImageDraw.Draw(im)
  d.ellipse((245,-160,655,385),fill='#526872')
  for x in [90,150,750,810]:d.rectangle((x,70,x+22,410),fill='#263c46')
  d.rectangle((0,402,W,H),fill='#344b53');d.line((0,415,W,415),fill='#71848a',width=2)
  for y in [438,474,502]:d.line((0,y,W,y),fill='#3e565f')
  ha,ta=draw_person(d,a,1,aa,'#cdd8d5',lean,t)
  hb,tb=draw_person(d,b,-1,bb,'#7b5c5c',lean,t)
  d.text((24,20),'点到即止 · 原创二维动作粗版',font=font,fill='#edf0e8')
  d.text((24,48),f'V{version} · 接触停顿 {hold}/24 秒 · 固定全景',font=small,fill='#c5d0cf')
  d.text((24,478),f'{f/FPS:04.2f}s  |  练习：进步 / 试招 / 架开 / 收剑 / 退开',font=small,fill='#c5d0cf')
  if f in [0,24,48,55,59,60,62,64,72,96,120,168]:selected.append((f,im.copy()))
  if warped==60:contacts.append({'frame':f,'time':f/FPS,'swords':[ha,ta,hb,tb]})
  im.save(out/f'f{f:03}.png')
 board=Image.new('RGB',(1200,3*192),'#1f2b31');bd=ImageDraw.Draw(board)
 for k,(f,im) in enumerate(selected):
  im.thumbnail((298,168));x=k%4*300;y=k//4*192;board.paste(im,(x,y+22));bd.text((x+3,y+3),f'{f}/24 = {f/FPS:.3f}s',fill='white')
 board.save(root/f'V{version}-检查图版.jpg',quality=94)
 rate=24000;audio=[]
 for n in range(rate*8):
  t=n/rate;s=0.0
  for start in [.7,5.2]:
   u=t-start
   if 0<=u<.12:s+=.07*math.exp(-u*35)*math.sin(2*math.pi*130*u)
  u=t-2.5
  if 0<=u<.6:s+=.14*math.exp(-u*10)*(math.sin(2*math.pi*1500*u)+.5*math.sin(2*math.pi*2317*u))
  audio.append(max(-32767,min(32767,int(s*32767))))
 with wave.open(str(root/f'V{version}-临时声.wav'),'wb') as w:w.setparams((1,2,rate,0,'NONE','not compressed'));w.writeframes(struct.pack('<'+'h'*len(audio),*audio))
 subprocess.run([str(ff),'-hide_banner','-loglevel','error','-framerate',str(FPS),'-i',str(out/'f%03d.png'),'-i',str(root/f'V{version}-临时声.wav'),'-c:v','libx264','-crf','20','-pix_fmt','yuv420p','-c:a','aac','-movflags','+faststart',str(root/f'点到即止-V{version}.mp4')],check=True)
 manifest.append({'version':version,'frames':N,'fps':FPS,'duration':8,'hold_frames':hold,'contact_geometry':contacts,'checks':'visual board inspection required; audio generated but not yet listened'})
(root/'实际输出元信息.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'versions':2,'frames_each':N,'duration_each':8,'output':str(root)},ensure_ascii=False))
