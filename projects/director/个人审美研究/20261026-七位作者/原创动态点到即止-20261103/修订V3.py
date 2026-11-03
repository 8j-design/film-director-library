from pathlib import Path
root=Path(__file__).resolve().parent
s=(root/'制作粗版.py').read_text(encoding='utf-8')
s=s.replace('[(1,0),(2,4)]','[(3,4)]').replace('实际输出元信息.json','V3实际输出元信息.json')
s=s.replace('mix(-70,-125,q)','mix(-70,-95,q)').replace('mix(-125,-30,q)','mix(-95,-30,q)')
s=s.replace('mix(-30,-65,q)','mix(-30,-85,q)').replace('mix(-150,-115,q)','mix(-150,-95,q)')
s=s.replace('mix(-65,40,q)','mix(-85,80,q)').replace('mix(-115,140,q)','mix(-95,100,q)')
s=s.replace('),40,140,0', '),80,100,0')
s=s.replace("'versions':2", "'versions':1")
exec(compile(s,str(root/'制作粗版.py'),'exec'))
