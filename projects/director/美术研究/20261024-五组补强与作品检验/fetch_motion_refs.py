from pathlib import Path
import urllib.request, hashlib, json, concurrent.futures
from PIL import Image
ROOT=Path(__file__).resolve().parent/'reference_images'/'motion'
ROOT.mkdir(parents=True,exist_ok=True)
ITEMS=[
('ue-transfiguration.jpg','https://static.universaleverything.com/wp-content/uploads/2022/11/11104412/Lifeforms-by-Universal-Everything-Transfiguration-3-scaled.jpg','https://www.universaleverything.com/art/transfiguration-2020'),
('rainbow-dance.jpg','https://www.lenlyefoundation.com/uploads/images/Rainbow%20Dance%2C%201936.jpg','https://www.lenlyefoundation.com/films/rainbow-dance/24/'),
('weave-costume.jpg','https://directorsnotes.com/wp-content/uploads/2017/04/weave_01.jpg','https://directorsnotes.com/2017/04/04/iqbal-ahmed-weave/'),
('collapse-01.webp','https://cdn.prod.website-files.com/63ecbcbcf16f0d4c676b0ede/6a1decc1d7fc366a391fc02e_Screenshot%202026-04-27%20at%204.41.34%E2%80%AFPM.webp','https://www.hellohornet.com/projects/nowness---collapse-body-form'),
('collapse-02.webp','https://cdn.prod.website-files.com/63ecbcbcf16f0d4c676b0ede/6a1ded94463804fd5d5d7d25_Screenshot%202026-04-27%20at%204.43.28%E2%80%AFPM.webp','https://www.hellohornet.com/projects/nowness---collapse-body-form')]
def fetch(item):
 name,url,page=item
 row={'file':name,'url':url,'page':page,'rights':'第三方原图；仅本地私人研究，不随原创作品归库或发布','viewed':False}
 try:
  data=urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=35).read()
  path=ROOT/name;path.write_bytes(data)
  with Image.open(path) as im: row['dimensions']=list(im.size)
  row.update(status='downloaded',sha256=hashlib.sha256(data).hexdigest(),bytes=len(data))
 except Exception as e: row.update(status='failed',error=str(e))
 return row
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex: rows=list(ex.map(fetch,ITEMS))
(ROOT/'manifest.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(rows,ensure_ascii=False))
