from pathlib import Path
import re,json,urllib.parse
R=Path(__file__).resolve().parent;REPO=R.parent/'影视资料库建库-20261020/repo';REL='projects/director/美术研究/20261024-五组补强与作品检验';D=REPO/REL
def prepend_after_heading(path,paragraph,marker):
 t=path.read_text(encoding='utf-8')
 if marker in t:return
 a,sep,b=t.partition('\n');path.write_text(a+'\n\n'+paragraph+'\n'+b.lstrip('\n'),encoding='utf-8')
entry='2026-10-24五组补强已进入实作：[资料大纲与检验]('+REL+'/README.md)。保留原44组，补R09/R10/R12/R17/R36，实际做原创空衣三版、16秒静音输出、固定帧控制、单项灯尺寸/本色测试、展示距离修正和原生/视频读回；袖根、完整视听、人体接触、groom/妆造、真实展场和观众仍有缺口。旧盘点为当时快照，不把本次有限试作记为五组掌握。'
prepend_after_heading(REPO/'START_HERE.md',entry,'2026-10-24五组补强已进入实作')
prepend_after_heading(REPO/'projects/director/STATUS.md',entry.replace(REL+'/', '美术研究/20261024-五组补强与作品检验/'),'2026-10-24五组补强已进入实作')
snapshot='**盘点后更新：**用户指出的五组已继续补资料并完成有限三维试作/修补/对照，见[五组补强大纲与实际结果](../20261024-五组补强与作品检验/README.md)。下面数字和分类保留为补强前的盘点快照；原44题不变，不能据此忽略最新证据，也不把有限实作当掌握。'
for name in ['README.md','44组速览.md','44组美术研究总纲.md']:
 prepend_after_heading(REPO/'projects/director/美术研究/20261024-44组资料与能力总览'/name,snapshot,'**盘点后更新：**')
localentry='2026-10-24五组补强：[五组资料大纲](新工作/美术五组补强与作品检验-20261024/五组资料大纲.md)、[研究与实际检验](新工作/美术五组补强与作品检验-20261024/研究总结与作品检验.md)、[16秒试作](新工作/美术五组补强与作品检验-20261024/artwork/v3/folds-of-air.mp4)。原44题保留，实际三版Blender/色光对照/单项测试/展示距离修正/原生和384帧技术读回；完整观看、人体承重、妆发及现场/观众仍未验证。归库结果以本批回执为准。'
prepend_after_heading(R.parent.parent/'开始.md',localentry,'2026-10-24五组补强：')
for name in ['README.md','44组速览.md','44组美术研究总纲.md']:
 p=R.parent/'美术44组资料能力总览-20261024'/name
 if p.exists():prepend_after_heading(p,snapshot.replace('../20261024-五组补强与作品检验/README.md','../美术五组补强与作品检验-20261024/README.md'),'**盘点后更新：**')
note=REPO/'notes/美术五组补强归库-20261024.md'
note.write_text('# 五组美术补强归库\n\n常规私有归库，沿用已有影视库，不新建库/公开或扩大权限。\n\n[本批研究及检验](../'+REL+'/README.md)：自写报告、来源元数据与脚本进入正文，原创工程/输出/核验另存私有Release；第三方参考原图/网页不入包。colour-science/colour与3b1b/manim各按现有协议登记为仅参考，未安装。\n\n原44组题名/次序不改，旧统计留快照并接最新结果。全片视听、观众/现场、真实妆发/人体接触未通过；一个最终审查agent达到用量上限，未伪称完成终审，主控据已收意见核源/修补。\n\n媒体清单见本批目录，具体服务器SHA/长度与文本树结果以后续回执为准。\n',encoding='utf-8')
# Local link paths only: semantic anchors and external links not asserted by this check.
broken=[]
for p in D.rglob('*.md'):
 for dest in re.findall(r'\]\(([^)]+)\)',p.read_text(encoding='utf-8')):
  if dest.startswith(('http:','https:','#','C:')):continue
  raw=urllib.parse.unquote(dest.split('#',1)[0])
  if raw and not (p.parent/raw).exists():broken.append({'file':str(p.relative_to(REPO)),'target':dest})
result={'new_batch_markdown_local_path_links_checked':True,'broken':broken,'source_pages_in_navigation':62,'source_pages_not_read_count':True,'third_party_raw_media_in_repo':False,'old_44_titles_preserved':'Only update paragraphs added; title/body navigation left in place'}
(R/'归库前核对.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False))
assert not broken
