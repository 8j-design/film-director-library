import bpy,math,json
from pathlib import Path
R=Path(__file__).resolve().parent;O=R/'artwork/v3'
bpy.ops.wm.open_mainfile(filepath=str(O/'gallery.blend'));s=bpy.context.scene;c=s.camera;screen=bpy.data.objects['Display 1.8m x 1.35m']
assert any(i.packed_file for i in bpy.data.images if i.source=='FILE')
rows=[]
for d,lens in [(.9,28),(1.8,28),(3.6,28),(.9,16.5)]:
 c.location.y=screen.location.y-d;c.data.lens=lens;bpy.context.view_layer.update()
 matrix=c.calc_matrix_camera(bpy.context.evaluated_depsgraph_get(),x=s.render.resolution_x,y=s.render.resolution_y,scale_x=s.render.pixel_aspect_x,scale_y=s.render.pixel_aspect_y)
 hfov=math.degrees(2*math.atan(1/matrix[0][0]));vfov=math.degrees(2*math.atan(1/matrix[1][1]))
 actual=abs(c.location.y-screen.location.y);assert abs(actual-d)<1e-6
 neededh=math.degrees(2*math.atan(1.8/(2*actual)));neededv=math.degrees(2*math.atan(1.35/(2*actual)))
 rows.append({'distance_m':actual,'lens_mm':lens,'render_horizontal_fov_deg':hfov,'render_vertical_fov_deg':vfov,'needed_horizontal_deg':neededh,'needed_vertical_deg':neededv,'whole_display_in_fixed_field':hfov>=neededh and vfov>=neededv,'rna_angle_y_deg':math.degrees(c.data.angle_y),'note':'Rendered field computed from projection matrix; RNA sensor angle_y alone omits output aspect/fit'})
assert rows[0]['whole_display_in_fixed_field']==False
assert all(rows[i]['whole_display_in_fixed_field'] for i in [1,2,3])
(R/'verification/gallery-projection-check.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
old=json.loads((O/'gallery-corrected-geometry.json').read_text(encoding='utf-8'))
for a,b in zip(old,rows):
 if 'vertical_fov_deg' in a:a['rna_angle_y_deg']=a.pop('vertical_fov_deg')
 a['render_horizontal_fov_deg']=b['render_horizontal_fov_deg'];a['render_vertical_fov_deg']=b['render_vertical_fov_deg'];a['whole_display_in_fixed_field']=b['whole_display_in_fixed_field']
(O/'gallery-corrected-geometry.json').write_text(json.dumps(old,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(rows,ensure_ascii=False))
