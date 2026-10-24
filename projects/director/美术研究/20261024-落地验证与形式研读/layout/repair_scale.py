"""Repair a proposed scale contract; this does not repair the raster storyboard."""
from pathlib import Path
import json,xml.etree.ElementTree as ET,hashlib
P=Path(__file__).resolve().parent
src=P/'space_plan.svg';dst=P/'space_plan_scale_revision.svg'
old=src.read_bytes();root=ET.fromstring(old)
def at(i):
    n=root.find(f".//*[@id='{i}']");assert n is not None,i;return n
S=100/170
pw,ph=110*S,40*S
ww,wh=pw+4,ph+4
md=at('layout_metadata');m=json.loads(md.text)
m.update(print_face=[pw,ph],package_face=[ww,wh],package_state_note='Proposed prompt-relative scale only; package upright footprint width x thickness, height=long edge; NOT measured from board',revision_basis='V2 prompt: print110x40cm; proposed adult170cm=100u; not original frozen story measurements')
md.text=json.dumps(m,ensure_ascii=False)
for ident,w,h in [('PRINT_FACE',pw,ph),('PRINT_SIZE',pw,ph),('PACKAGE_FACE',ww,wh),('PACKAGE_FACE_SIZE',ww,wh)]:
    n=at(ident)
    if n.tag.endswith('g'):n.set('data-width',str(w));n.set('data-height',str(h))
    else:n.set('width',str(w));n.set('height',str(h))
for ident in ['PACKAGE_UPRIGHT_FOOTPRINT','PACKAGE_FOOTPRINT_SIZE']:
    n=at(ident)
    if n.tag.endswith('g'):n.set('data-width',str(wh));n.set('data-height',str(ww))
    else:n.set('width',str(wh))
at('PACKAGE_FACE_BAND').set('x',str(ww*.62));at('PACKAGE_FACE_BAND').set('height',str(wh))
at('PACKAGE_FOOTPRINT_BAND').set('x',str(wh*.62));at('PACKAGE_FOOTPRINT_BAND').set('width','3')
paper=at('PRINT_FACE')
for n in paper:
    if n.tag.endswith('path'):n.set('d',f'M5 7 H{pw-5} M5 13 H{pw-9} M8 19 H{pw-4}')
replacements={
'最后一张：三状态平面布局与同尺对象索引 v1':'最后一张：尺度契约修订；尚未配准图板',
'占地52×8u；高164u':f'占地{wh:.2f}×8u；高{ww:.2f}u',
'对象尺寸索引（同一单位，不是实测）：原纸160×48u；包装面164×52u；私人箱占地32×24u。':f'尺度修订（假设成人170cm=100u）：原纸{pw:.2f}×{ph:.2f}u；包装面{ww:.2f}×{wh:.2f}u。',
'C是立靠状态，俯视只见52×8u占地；包装本体尺寸未变。':'C为立靠俯视；高为包件长边，宽为短边。需另核倾角/支撑。',
'修改演示v2仅改变最终PACK_01的深蓝带颜色；不是新增剧情或已完成视觉验收。':'本版只统一提示词与布局的尺度提案；没有修复生成图中的比例，也未作视觉验收。',
}
for n in root.iter():
    if n.text in replacements:n.text=replacements[n.text]
ET.indent(root,space='  ');ET.ElementTree(root).write(dst,encoding='utf-8',xml_declaration=True)
# Reread the result and verify a meaningful cross-asset constraint, not rendering.
r=ET.parse(dst).getroot();meta=json.loads(r.find(".//*[@id='layout_metadata']").text)
assert abs(meta['print_face'][0]/meta['person_relative_height_reference']['C_A']-110/170)<1e-9
assert meta['package_face'][0]>meta['print_face'][0] and meta['package_face'][1]>meta['print_face'][1]
for ident in ['ROOM_FIXED','C_A_0','C_B_0','C_A_1','C_B_1']:
    a=ET.fromstring(old).find(f".//*[@id='{ident}']");b=r.find(f".//*[@id='{ident}']")
    assert ET.tostring(a)==ET.tostring(b),ident
assert src.read_bytes()==old
out={'source':src.name,'revision':dst.name,'basis':'proposed human170cm=100u; print110x40cm from V2 prompt','original_unchanged':True,'print_face':meta['print_face'],'package_face':meta['package_face'],'paper_to_person_long_ratio':110/170,'package_can_contain_paper_in_defined_2D_dimensions':True,'not_verified':['board proportions','material thickness/folds','handling/contact','visual rendering','animation','DCC import'],'sha256':hashlib.sha256(dst.read_bytes()).hexdigest()}
(P/'scale_repair_verification.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(out,ensure_ascii=False))
