import bpy,json
from mathutils import Vector
from pathlib import Path
R=Path(__file__).resolve().parent;O=R/'film/ending-view-tests';O.mkdir(exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(R/'film/v6/studio-animation.blend'));s=bpy.context.scene
for marker in list(s.timeline_markers):s.timeline_markers.remove(marker)
s.render.image_settings.media_type='IMAGE';s.render.image_settings.file_format='PNG';s.render.resolution_x=960;s.render.resolution_y=540;s.render.resolution_percentage=100
tests=[('A-wide',None,None,47),('B-left-corner',(-3.6,-1.4,2.6),(-.8,1,.8),46),('C-high-left',(-3.6,-3.8,3.5),(-.1,.6,.85),46),('D-package-insert',(-2.8,.45,1.45),(-1.03,1.895,.60),50)]
receipt=[]
for name,pos,target,lens in tests:
 if pos:
  data=bpy.data.cameras.new(name);cam=bpy.data.objects.new(name,data);s.collection.objects.link(cam);cam.location=pos;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.lens=lens;cam.data.sensor_width=36
 else:cam=bpy.data.objects['06 After']
 for f in [850,1440]:
  s.frame_set(f);s.camera=cam;s.render.filepath=str(O/f'{name}-{f}.png');bpy.ops.render.render(write_still=True)
 receipt.append({'view':name,'position':list(cam.location),'target':target,'lens_mm':cam.data.lens,'frames':[850,1440]})
(O/'tested-views.json').write_text(json.dumps(receipt,indent=2),encoding='utf-8')
print('ENDING_VIEWS_COMPLETE',flush=True)
