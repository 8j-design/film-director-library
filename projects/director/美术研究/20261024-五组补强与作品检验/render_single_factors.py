"""Next limited R09/R10 step: a single lamp-size variable or one material input."""
import bpy,json
from pathlib import Path
R=Path(__file__).resolve().parent;O=R/'artwork'/'v3';rows=[]
for variant in ['key-size-0.4m','key-size-5m','red-to-linen']:
 bpy.ops.wm.open_mainfile(filepath=str(O/'folds-base.blend'));s=bpy.context.scene;s.frame_set(192)
 if variant.startswith('key-size'):
  bpy.data.objects['Key neutral'].data.size=.4 if '0.4' in variant else 5
  change={'object':'Key neutral','property':'size','base_m':3,'new_m':bpy.data.objects['Key neutral'].data.size,'energy_W':800,'caution':'Power held; local irradiance and highlights can change, not constant observed brightness'}
 else:
  m=bpy.data.materials['03 Vermilion inner seam'];inp=m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'];old=list(inp.default_value)
  inp.default_value=bpy.data.materials['02 Linen fold faces'].node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value
  change={'material':m.name,'property':'Base Color','before_linear_RGBA':old,'after_linear_RGBA':list(inp.default_value),'caution':'One input changed, multiple colour dimensions may differ; not pure saturation test'}
 s.render.filepath=str(O/f'single-{variant}-0192.png');bpy.ops.render.render(write_still=True)
 rows.append({'variant':variant,'base':'v3/folds-base.blend','frame':192,'change':change,'locked':'Geometry, pose, camera, all other shader/light settings, exposure, view transform'})
(O/'single-factor-receipts.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
print('SINGLE_FACTORS_COMPLETE',flush=True)
