from pathlib import Path
root=Path(__file__).resolve().parent
ns={'__file__':str(root/'修订V4.py')}
src=(root/'修订V4.py').read_text(encoding='utf-8');exec(src[:src.index('exec(compile')],ns)
s=ns['s'].replace('[(4,4)]','[(5,4),(6,0)]').replace('V4实际输出元信息.json','V5V6实际输出元信息.json')
s=s.replace('150*math.cos(a)','100*math.cos(a)').replace('150*math.sin(a)','100*math.sin(a)')
start=s.index('def params(t):');end=s.index('def draw_person',start)
s=s[:start]+'''def params(t):
 if t<1.5:p=ease(t/1.5);return mix(300,340,p),mix(600,560,p),-85,-95,0
 if t<2.083333:q=ease((t-1.5)/.583333);return 340,560,mix(-85,-105,q),mix(-95,-75,q),mix(0,6,q)
 if t<2.5:q=ease((t-2.083333)/.416667);return 340,560,mix(-105,-60,q),mix(-75,-120,q),mix(6,12,q)
 if t<3.25:q=ease((t-2.5)/.75);return mix(340,330,q),mix(560,570,q),mix(-60,-85,q),mix(-120,-95,q),mix(12,0,q)
 if t<4.5:return 330,570,-85,-95,0
 if t<6:q=ease((t-4.5)/1.5);return mix(330,270,q),mix(570,630,q),-85,-95,0
 q=ease((t-6)/1);return 270,630,mix(-85,80,q),mix(-95,-260,q),0
''' +s[end:]
s=s.replace("'versions':1", "'versions':2")
exec(compile(s,str(root/'制作粗版.py'),'exec'))
