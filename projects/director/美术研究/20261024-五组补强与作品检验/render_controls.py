"""Open V2 native scene; change one declared factor group at a time."""
import bpy,json
from pathlib import Path
R=Path(__file__).resolve().parent;O=R/'artwork'/'v2';B=O/'folds-base.blend'; rows=[]
variants=['white','flood','no-rim','all-saturated','no-fringe']
def color(h):
 vals=[int(h[i:i+2],16)/255 for i in (0,2,4)]
 return tuple(v/12.92 if v<.04045 else ((v+.055)/1.055)**2.4 for v in vals)+(1,)
for variant in variants:
 bpy.ops.wm.open_mainfile(filepath=str(B));s=bpy.context.scene;s.frame_set(192)
 # Every variant starts from the same saved file; geometry, pose, camera and display transform preserved.
 if variant=='white':
  for n in ['Key neutral','Rim cool','Front quiet fill']:bpy.data.objects[n].data.color=(1,1,1)
 elif variant=='flood':
  for n,c in [('Key neutral',(1,.08,.15)),('Rim cool',(.08,.15,1)),('Front quiet fill',(1,.08,.15))]:bpy.data.objects[n].data.color=c
 elif variant=='no-rim':bpy.data.objects['Rim cool'].data.energy=0
 elif variant=='all-saturated':
  for n,h in [('01 Deep indigo woven shell','005AAB'),('02 Linen fold faces','E3B52E'),('03 Vermilion inner seam','FA260B')]:
   m=bpy.data.materials[n];m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=color(h)
 elif variant=='no-fringe':
  for ob in s.objects:
   if ob.name.startswith('Hem fibre strip'):ob.hide_render=True
 s.render.filepath=str(O/f'control-{variant}-0192.png');bpy.ops.render.render(write_still=True)
 rows.append({'variant':variant,'frame':192,'base':'folds-base.blend','geometry_camera_frame_locked':True,'changed_factor':{'white':'All three light chromaticities, powers unchanged','flood':'All three light chromaticities, powers unchanged','no-rim':'Only rim power 480 to 0W','all-saturated':'Three surface base colours together; not individual hue causation','no-fringe':'Only visibility of authored hem strips'}[variant],'view_transform':s.view_settings.view_transform,'look':s.view_settings.look,'exposure':s.view_settings.exposure,'resolution':[s.render.resolution_x,s.render.resolution_y]})
(O/'control-receipts.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
print('CONTROLS_COMPLETE',len(rows),flush=True)
