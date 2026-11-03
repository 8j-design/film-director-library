from pathlib import Path
root=Path(__file__).resolve().parent
s=(root/'制作粗版.py').read_text(encoding='utf-8')
s=s.replace('[(1,0),(2,4)]','[(4,4)]').replace('实际输出元信息.json','V4实际输出元信息.json').replace("'versions':2", "'versions':1")
start=s.index('def params(t):');end=s.index('def draw_person',start)
s=s[:start]+'''def params(t):
 if t<1.5:p=ease(t/1.5);return mix(300,340,p),mix(600,560,p),-70,-110,0
 if t<2.083333:q=ease((t-1.5)/.583333);return 340,560,mix(-70,-95,q),mix(-110,-80,q),mix(0,6,q)
 if t<2.5:q=ease((t-2.083333)/.416667);return 340,560,mix(-95,-30,q),mix(-80,-150,q),mix(6,12,q)
 if t<3.25:q=ease((t-2.5)/.75);return mix(340,330,q),mix(560,570,q),mix(-30,-85,q),mix(-150,-95,q),mix(12,0,q)
 if t<4.5:return 330,570,-85,-95,0
 if t<6:q=ease((t-4.5)/1.5);return mix(330,270,q),mix(570,630,q),-85,-95,0
 q=ease((t-6)/1);return 270,630,mix(-85,80,q),mix(-95,-260,q),0
''' +s[end:]
exec(compile(s,str(root/'制作粗版.py'),'exec'))
