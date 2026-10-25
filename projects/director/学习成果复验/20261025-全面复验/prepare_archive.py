"""Archive original work only; third-party reference media remains local."""
from pathlib import Path
from PIL import Image, ImageDraw
import csv, hashlib, json, os, re, shutil, zipfile

TASK=Path(__file__).resolve().parent
REPO=TASK.parent/'影视资料库建库-20261020/repo'
DEST=REPO/'projects/director/学习成果复验/20261025-全面复验'
TAG='research-2026-10-25-learning-revalidation'
RELEASE='https://github.com/8j-design/film-director-library/releases/tag/'+TAG

def digest(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
    return h.hexdigest()

def write(p,t):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(t,encoding='utf-8')

def append_once(p,marker,text):
    s=p.read_text(encoding='utf-8')
    if marker not in s:write(p,s+'\n'+text)

append_once(TASK/'结尾机位实测与V7修改依据.md','## V7实际结果', '''## V7实际结果（2026-10-25）

两段共485帧完成实际重渲，按来源表与V6未改段合成60秒V7。原生210对象/139网格可重开，无外部图像依赖；视频实际技术解码1440帧。主控核看变化窗口及相邻6表48幅；知情独立复审同样看48幅并放大7原图，详见agents/sequence_read_v7.md。

纸包底边、与私箱分离、末场完整包及两把钥匙确实更可见；也发现外侧肘臂部分出画、人物变小和首尾机位不再完全匹配。没有把这些代价藏进“优化”二字。原624帧双臂归属、抓握、承重、人物发展、正常速度声画及人类观众仍未通过或未验证。当前交付是未完成预演，不是艺术定稿。
''')

write(TASK/'审查意见处理与保存范围.md', '''# 归档前审查意见的实际处理

2026-10-25。独立报告agents/final_batch_review.md保留，不删除其发现。

- B19已接续官方源取得及103幅全段静帧范围，仍写未正常速度视听/未实听；原CSV保留在audit-start-snapshots，奖项身份不改成动画获奖。
- 全44组CSV原空白列改为初核范围与后续增量的明确指向；R21等初核旧状态由入口说明接续，完整Style Guide未取得的缺口保留。
- Sprite共132图像文件、去重125个源帧位置；不是132个作品或完整视听。19矩阵与8华语项目存在交叉，不相加作29部深研。
- E稿原重复移袋已在实际正文及生成脚本修正；V7实际机位变化与仍失败手部都有报告，没有以新相机冒称接触已完成。
- 本批只保存自写正文、脚本、原创工程/输出/抽样和技术记录。整个reference_media目录、第三方原片/抽帧/网页/PDF/临时播放列表和下载描述不进入Git或媒体ZIP。稳定出处链接与准确阅读范围保留。

ZIP是打包时的原创工作快照，发布回执在包外另存；最终保存结果以媒体发布回执、文本远端核验及《保存与验证结果.md》为准。打包本身不等于已上传。
''')

write(TASK/'README.md', '''# 全面复验：原44题、完整改稿与数字预演

2026-10-24开始，2026-10-25接续。先读[研究与复验总结](复验结果与研究总结.md)。本批完成范围是44题旧证据审计、有层级的经典/制作过程扩展、A—E完整改稿和同一故事V1—V7原生试作及阶段复验；整套导演/美术学习继续进行。

- 最新剧本：[《借桌》E](writing/13-借桌-完整修订E.md)，[修后复核](writing/14-E稿复核结果.md)。事件结构有纸面进展，空间粗排、生活实证和声画尚缺。
- 影像：[V7实际机位结果](结尾机位实测与V7修改依据.md)，[独立复审](agents/sequence_read_v7.md)。60秒静音、24fps，是未完成预演；抓握/承重/中央双臂/人物表达仍不足。
- 全范围：[44组基线审计](agents/art44_audit.md)、[本轮增量CSV](44组本轮复验增量.csv)。保留原题名顺序，不把一个故事的七版当七个独立能力样本。
- 专业对照：[19项目矩阵](agents/award_benchmarks.md)、[华语八项目过程](agents/chinese_process_followup.md)、[Pas图像互证](agents/pas_visual_analysis.md)、[Sprite图像与制作正文](Sprite实看与制作正文互证.md)。深度逐项记录，没有声称完整看片或全部著作通读。
- [独立归档前审查](agents/final_batch_review.md)及[意见处理](审查意见处理与保存范围.md)。第三方媒体与抽帧仅本地，不随原创包上传。

私有媒体发布目标：RELEASE_URL。应以真实回执确认发布状态。ZIP保留film/v6与v7相对目录；V7/edit.blend引用V6未改段及V7/carry.mp4、ending.mp4，解压整个包再打开。单独V7/studio.blend无外部图像依赖，可重开全1—1440帧场景。

接续优先：回到全段修持纸/打带时的动作归属与接触；同时将《借桌》E连续粗排，验证门外箱、门内凳、退桌、离场与交袋。每项修补仍与整体表达联系，研究与制作交错。
'''.replace('RELEASE_URL',RELEASE))

# A preview derived exclusively from our own decoded frames.
selected=TASK/'film/v7/verification/selected'
frames=[1,241,505,697,1014,1440]
available={int(p.stem):p for p in selected.glob('*.png')}
chosen=[min(available,key=lambda n:abs(n-x)) for x in frames]
preview=Image.new('RGB',(1536,3*462),(24,24,24));draw=ImageDraw.Draw(preview)
for i,n in enumerate(chosen):
    im=Image.open(available[n]).convert('RGB');im.thumbnail((768,432))
    x=(i%2)*768;y=(i//2)*462
    preview.paste(im,(x,y));draw.text((x+10,y+437),f'V7 PREVIS / NOT FINAL   frame {n}   {(n-1)/24:.2f}s',fill='white')
archive=TASK/'archive';archive.mkdir(exist_ok=True)
preview.save(archive/'last-print-v7-contact.png')
shutil.copy2(TASK/'film/v6/studio.mp4',archive/'last-print-v6.mp4')
shutil.copy2(TASK/'film/v7/studio.mp4',archive/'last-print-v7.mp4')
shutil.copy2(TASK/'film/v7/studio.blend',archive/'last-print-v7.blend')

# Only explicit original-work roots, never traverse reference_media.
roots=[p for p in TASK.iterdir() if p.is_file() and p.suffix in {'.md','.csv','.py'}]
for folder in ['agents','writing','film']:
    roots.extend(p for p in (TASK/folder).rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.blend1')
roots=sorted(roots,key=lambda p:p.relative_to(TASK).as_posix())
assert all('reference_media' not in p.relative_to(TASK).parts for p in roots)
items=[{'path':p.relative_to(TASK).as_posix(),'bytes':p.stat().st_size,'sha256':digest(p)} for p in roots]
inventory={'snapshot_date':'2026-10-25','scope':'Original work only; reference_media entirely excluded','files':items,'count':len(items)}
write(TASK/'原创包文件清单.json',json.dumps(inventory,ensure_ascii=False,indent=2)+'\n')
zip_path=archive/'learning-revalidation-20261025-originals.zip'
with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for p in roots:z.write(p,p.relative_to(TASK).as_posix())
    z.write(TASK/'原创包文件清单.json','原创包文件清单.json')
with zipfile.ZipFile(zip_path) as z:
    if z.testzip() is not None:raise RuntimeError('ZIP CRC verification failed')
    for row in items:
        if hashlib.sha256(z.read(row['path'])).hexdigest()!=row['sha256']:raise RuntimeError('ZIP member mismatch')
    if any('reference_media/' in n or n.startswith('/') or '..' in Path(n).parts for n in z.namelist()):raise RuntimeError('Unexpected archive path')
manifest={'release_url':RELEASE,'tag':TAG,'archive_snapshot':'2026-10-25; final server receipts stored outside ZIP','zip_members_verified':True,'excluded':['reference_media/**','*.blend1','__pycache__/**'],'original_files':len(items),'release_assets':[]}
for p in sorted(archive.iterdir()):
    if p.is_file():manifest['release_assets'].append({'local_path':p.relative_to(TASK).as_posix(),'bytes':p.stat().st_size,'sha256':digest(p)})
write(TASK/'媒体清单.json',json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')

# Readable repository export: original text remains unchanged inside ZIP.
text_files=[p for p in roots if p.suffix in {'.md','.csv','.py'} and 'film' not in p.relative_to(TASK).parts]
text_set={p.resolve() for p in text_files}
link_pattern=re.compile(r'\[([^\]\n]+)\]\((<?(?:C:|c:)[^)]+)\)')
def export_text(p):
    s=p.read_text(encoding='utf-8-sig')
    if p.suffix=='.md':
        def fix(m):
            label=m.group(1);target=m.group(2).strip('<>')
            path=Path(target)
            if path.resolve() in text_set:
                rel=os.path.relpath(DEST/path.relative_to(TASK),DEST/p.relative_to(TASK).parent).replace('\\','/')
                return f'[{label}](<{rel}>)'
            try:
                relative=path.relative_to(TASK).as_posix()
                if relative.startswith('film/'):return f'{label}（原创ZIP内`{relative}`，见[媒体包]({RELEASE})）'
                return f'{label}（本地参考记录`{relative}`；未随库复制）'
            except ValueError:
                try:
                    relative=path.relative_to(REPO)
                    rel=os.path.relpath(REPO/relative,DEST/p.relative_to(TASK).parent).replace('\\','/')
                    return f'[{label}](<{rel}>)'
                except ValueError:return label+'（原工作区只读档案路径见本地原稿）'
        s=link_pattern.sub(fix,s)
    return s
DEST.mkdir(parents=True,exist_ok=True)
for p in text_files:write(DEST/p.relative_to(TASK),export_text(p))
for name in ['媒体清单.json','原创包文件清单.json']:shutil.copy2(TASK/name,DEST/name)
for v in ['v6','v7']:
    p=TASK/f'film/{v}/verification/native-video-receipt.json'
    if p.exists():shutil.copy2(p,DEST/f'{v}-native-video-receipt.json')
shutil.copy2(TASK/'film/v7/edit-source-map.json',DEST/'v7-edit-source-map.json')
print(json.dumps({'original_files':len(items),'text_exports':len(text_files),'zip_bytes':zip_path.stat().st_size,'assets':len(manifest['release_assets']),'zip_all_members_sha256_match':True,'third_party_directory_excluded':True},ensure_ascii=False))
