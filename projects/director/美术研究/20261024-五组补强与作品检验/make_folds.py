"""Original editable garment sculpture; Blender 5.2.3. No external assets.
Run blender --background --factory-startup --python make_folds.py -- --version v1 --mode stills
"""
import bpy, math, sys, argparse, json
from pathlib import Path
from mathutils import Vector
P=argparse.ArgumentParser();P.add_argument('--version',default='v1');P.add_argument('--mode',default='stills',choices=['stills','movie','controls','gallery']);P.add_argument('--variant',default='base')
args=P.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
ROOT=Path(__file__).resolve().parent; OUT=ROOT/'artwork'/args.version;OUT.mkdir(parents=True,exist_ok=True)
V3=args.version=='v3';V2=args.version in ['v2','v3']
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
s=bpy.context.scene;s.render.engine='BLENDER_EEVEE';s.render.resolution_x=960;s.render.resolution_y=720;s.render.resolution_percentage=100
s.render.fps=24;s.frame_start=1;s.frame_end=384;s.render.image_settings.file_format='PNG'
s.view_settings.view_transform='AgX';s.view_settings.look='AgX - Medium High Contrast';s.view_settings.exposure=0;s.view_settings.gamma=1
s.world.color=(0.035,0.035,0.035);s.unit_settings.system='METRIC';s.unit_settings.scale_length=1
s.render.film_transparent=False
def rgba(hex):
 vals=[int(hex[i:i+2],16)/255 for i in (0,2,4)]
 return tuple(c/12.92 if c<.04045 else ((c+.055)/1.055)**2.4 for c in vals)+(1,)
def mat(name,hex,rough=.6,metal=0,weave=False):
 m=bpy.data.materials.new(name);m.diffuse_color=rgba(hex);m.use_nodes=True
 n=m.node_tree.nodes;p=n.get('Principled BSDF');p.inputs['Base Color'].default_value=m.diffuse_color;p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal
 if weave:
  tex=n.new('ShaderNodeTexNoise');tex.inputs['Scale'].default_value=240;tex.inputs['Detail'].default_value=2
  bump=n.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.22;bump.inputs['Distance'].default_value=.003
  m.node_tree.links.new(tex.outputs['Fac'],bump.inputs['Height']);m.node_tree.links.new(bump.outputs['Normal'],p.inputs['Normal'])
 return m
indigo=mat('01 Deep indigo woven shell','183C4A',.68,0,True)
linen=mat('02 Linen fold faces','A99A7D' if V2 else 'CDC0A1',.88 if V2 else .78,0,True)
red=mat('03 Vermilion inner seam','B2442B',.7,0,True)
gold=mat('04 Oxidised brass clasp','A68855',.38,.65)
floor=mat('Stage charcoal','151D24',.86)
def objmesh(name,verts,faces,materials):
 me=bpy.data.meshes.new(name+' mesh');me.from_pydata(verts,[],faces);me.update();ob=bpy.data.objects.new(name,me);s.collection.objects.link(ob)
 for m in materials:me.materials.append(m)
 for p in me.polygons:p.use_smooth=True
 return ob
def animate_shapes(ob,opened,settled):
 ob.shape_key_add(name='Basis');op=ob.shape_key_add(name='Open');tail=ob.shape_key_add(name='Afterimage')
 for v,co in zip(op.data,opened):v.co=co
 for v,co in zip(tail.data,settled):v.co=co
 keys=[(1,0),(72,.03),(96,.14),(192,1),(240,1),(336,.08),(384,0)]
 # V2 asymmetry shifts the sleeve's onset and return without changing garment identity.
 lag=10 if V2 and ob.name.startswith('Sleeve right') else 0
 for f,v in keys:op.value=v;op.keyframe_insert('value',frame=min(384,f+lag))
 for f,v in [(1,0),(240,0),(336,1),(384,1)]:tail.value=v;tail.keyframe_insert('value',frame=f)
 ob['deformation']='Authored shape interpolation; not cloth simulation, not motion capture'
def bodypos(u,t,opened=False,settled=False):
 a=.32+(2*math.pi-.64)*t
 pleat=(.027*math.cos(a*24+.45*math.sin(u*7+a*3))*(.8+.2*math.cos(a*5))+.006*math.cos(a*48+u*3)) if V2 else (.038*math.cos(a*28)+.009*math.cos(a*56))
 r=.285+.32*(1-u)**1.5+pleat*(.45+.55*(1-u))
 z=.45+1.68*u+.035*math.sin(a*3)*(1-u)
 if V3 and u>.82:
  q=(u-.82)/.18;r=(r-pleat*(.45+.55*(1-u)))*(1-.16*q)+pleat*(1-q)*(.45+.55*(1-u));z+=.13*q
 x=r*math.sin(a);y=-r*math.cos(a)
 if opened:
  x*=1+.45*(1-u);y+=.13*math.sin(a*2+.5)*(1-u);z+=.22*(math.sin(a*2)**2)*(1-u)
 if settled:
  x+=(.19 if V2 else .10)*(1-u)**1.4;y+=.04*math.sin(a*3)*(1-u);z+=(.075 if V2 else .035)*math.sin(a*2)*(1-u)
 return (x,y,z)
NU=36;NT=168
verts=[bodypos(i/NU,j/NT) for i in range(NU+1) for j in range(NT+1)]
faces=[(i*(NT+1)+j,i*(NT+1)+j+1,(i+1)*(NT+1)+j+1,(i+1)*(NT+1)+j) for i in range(NU) for j in range(NT)]
body=objmesh('Coat shell - open front',verts,faces,[indigo,linen,red])
for p in body.data.polygons:
 t=(p.index%NT+.5)/NT
 p.material_index=1 if t<.15 or t>.82 or (V3 and p.index//NT>NU*.91) else 0
 if .15<t<.17:p.material_index=2
sol=body.modifiers.new('Fabric thickness','SOLIDIFY');sol.thickness=.012
animate_shapes(body,[bodypos(i/NU,j/NT,True) for i in range(NU+1) for j in range(NT+1)],[bodypos(i/NU,j/NT,False,True) for i in range(NU+1) for j in range(NT+1)])
def sleevepos(u,t,side,opened=False,settled=False):
 ang=t*2*math.pi;rad=(.17-.06*u)*(1+.10*math.cos(ang*12))
 dx=.82 if opened else .45;drop=.25 if opened else .83
 cx=side*(.28+dx*u-(.10*(1-u) if V3 else 0));cy=-.005-.04*u;cz=(2.01 if V2 else 2.06)-drop*u+.05*math.sin(u*math.pi)
 if settled:cx+=side*.03*u;cz-=.045*u if side==1 else 0
 return (cx+side*.64*rad*math.sin(ang),cy+rad*math.cos(ang),cz+.76*rad*math.sin(ang))
for side,label in [(-1,'left'),(1,'right')]:
 nu=22;nt=48
 ob=objmesh('Sleeve '+label,[sleevepos(i/nu,j/nt,side) for i in range(nu+1) for j in range(nt)],[(i*nt+j,i*nt+(j+1)%nt,(i+1)*nt+(j+1)%nt,(i+1)*nt+j) for i in range(nu) for j in range(nt)],[indigo,linen])
 for p in ob.data.polygons:p.material_index=1 if (p.index%nt)<14 else 0
 md=ob.modifiers.new('Cuff fabric thickness','SOLIDIFY');md.thickness=.012
 animate_shapes(ob,[sleevepos(i/nu,j/nt,side,True) for i in range(nu+1) for j in range(nt)],[sleevepos(i/nu,j/nt,side,False,True) for i in range(nu+1) for j in range(nt)])
# Collar is a separate open band, preserving a hollow aperture at all times.
def collarpos(u,t):
 a=.15+(2*math.pi-.3)*t;r=.235+.04*u
 return (r*math.sin(a),-.83*r*math.cos(a),2.08+.21*u+.035*math.cos(a))
nu=6;nt=100
collar=objmesh('Standing hollow collar',[collarpos(i/nu,j/nt) for i in range(nu+1) for j in range(nt+1)],[(i*(nt+1)+j,i*(nt+1)+j+1,(i+1)*(nt+1)+j+1,(i+1)*(nt+1)+j) for i in range(nu) for j in range(nt)],[linen])
md=collar.modifiers.new('Collar thickness','SOLIDIFY');md.thickness=.018
if V3:collar.hide_render=True
if V2 and not V3:
 nu=5;nt=100
 def yokepos(u,t):
  a=.25+(2*math.pi-.5)*t;r=.23+.09*u
  return (r*math.sin(a),-.93*r*math.cos(a),2.105+.014*math.sin(a)**2)
 yoke=objmesh('Shoulder connecting yoke',[yokepos(i/nu,j/nt) for i in range(nu+1) for j in range(nt+1)],[(i*(nt+1)+j,i*(nt+1)+j+1,(i+1)*(nt+1)+j+1,(i+1)*(nt+1)+j) for i in range(nu) for j in range(nt)],[indigo])
 md=yoke.modifiers.new('Yoke fabric thickness','SOLIDIFY');md.thickness=.012
# Narrow authored fabric strips at the hem; these are fringe geometry, not hair/groom.
for k in range(36):
 t=.06+.88*k/35;start=bodypos(0,t);vo=[];op=[];ta=[]
 for j in range(8):
  q=j/7
  for sign in [-1,1]:
   def strip(p,openstate=False,after=False):
    return (p[0]+sign*(.0014 if V2 else .003)+(.04 if openstate else .012)*math.sin(q*3+k),p[1]-.015+(.06 if openstate else .01)*q*math.sin(k),p[2]-.12*q)
   vo.append(strip(bodypos(0,t)));op.append(strip(bodypos(0,t,True),True));ta.append(strip(bodypos(0,t,False,True),False,True))
 ob=objmesh('Hem fibre strip %02d'%k,vo,[(j*2,j*2+1,j*2+3,j*2+2) for j in range(7)],[linen if k%7 else red]);animate_shapes(ob,op,ta)
 if args.variant=='no-fringe':ob.hide_render=True
def cube(name,loc,scale,material):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=name;o.scale=scale;o.data.materials.append(material)
 bevel=o.modifiers.new('Soft edges','BEVEL');bevel.width=.025;bevel.segments=3;return o
cube('Low stage plinth',(0,.1,.045),(2.9,2.0,.09),floor)
cube('Ground',(0,0,-.05),(200,200,.05),floor)
# Small clasp is an authored identity anchor; no mythological symbol copied.
bpy.ops.mesh.primitive_uv_sphere_add(segments=24,ring_count=12,radius=.034,location=(.085,-.30,1.92));bpy.context.object.name='Brass clasp';bpy.context.object.data.materials.append(gold)
def aim(ob,point):ob.rotation_euler=(Vector(point)-ob.location).to_track_quat('-Z','Y').to_euler()
def area(name,pos,power,color,size,target=(0,0,1.3)):
 d=bpy.data.lights.new(name,'AREA');d.energy=power;d.color=color;d.shape='DISK';d.size=size;o=bpy.data.objects.new(name,d);s.collection.objects.link(o);o.location=pos;aim(o,target);return o
key=area('Key neutral',(-3,-4,4.6),800 if V2 else 1050,(1,.89,.74),3)
rim=area('Rim cool',(2.6,1.0,3.5),480 if V2 else 850,(.35,.68,1),2.3)
fill=area('Front quiet fill',(2,-3,2),100 if not V2 else 210,(.72,.85,1),2)
if args.variant=='white':
 for l in [key,rim,fill]:l.data.color=(1,1,1)
elif args.variant=='flood':
 key.data.color=(1,.08,.15);rim.data.color=(.08,.15,1);fill.data.color=(1,.08,.15)
elif args.variant=='no-rim':rim.data.energy=0
if args.variant=='all-saturated':
 for m,h in [(indigo,'005AAB'),(linen,'E3B52E'),(red,'FA260B')]:
  m.diffuse_color=rgba(h);m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=m.diffuse_color
bpy.ops.object.camera_add(location=(3.25,-6.9,3.0));camera=bpy.context.object;camera.name='Locked master camera';aim(camera,(0,0,1.25));camera.data.type='ORTHO';camera.data.ortho_scale=3.65;s.camera=camera
if V2:
 camera.location=(1.5,-7.4,2.75);aim(camera,(0,0,1.27))
# All geometry and authored keys are persistent in the .blend. No handlers or add-ons required.
s['title']='Folds of Air / 风的褶皱';s['scope']='Original garment sculpture; no body-contact, physics, skin or groom validation'
s['version']=args.version;s['variant']=args.variant;s['color_contract']='sRGB swatches linearised in shader; AgX Medium High Contrast; exposure 0'
s.frame_set(192)
blend=OUT/('folds-'+args.variant+'.blend')
if args.mode in ['stills','controls']:
 bpy.ops.wm.save_as_mainfile(filepath=str(blend))
 for frame in ([192] if args.mode=='controls' else [1,192,384]):
  s.frame_set(frame);s.render.filepath=str(OUT/f'{args.variant}-{frame:04d}.png');bpy.ops.render.render(write_still=True)
elif args.mode=='movie':
 s.render.resolution_x=768;s.render.resolution_y=576
 s.render.image_settings.media_type='VIDEO';s.render.image_settings.file_format='FFMPEG';s.render.ffmpeg.format='MPEG4';s.render.ffmpeg.codec='H264';s.render.ffmpeg.constant_rate_factor='MEDIUM';s.render.ffmpeg.ffmpeg_preset='GOOD'
 s.render.filepath=str(OUT/'folds-of-air.mp4');s.render.use_file_extension=True
 bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'folds-animation.blend'));bpy.ops.render.render(animation=True)
elif args.mode=='gallery':
 # Geometric display mockup, not a light-calibrated projector simulation.
 for ob in list(s.objects):ob.hide_render=True
 wallmat=mat('Gallery wall','8F8B83',.9);groundmat=mat('Gallery floor','464846',.95)
 wall=cube('Display wall',(0,.05,1.5),(5,.1,3),wallmat);wall.hide_render=False
 ground=cube('Gallery floor',(0,-2,-.03),(6,6,.06),groundmat);ground.hide_render=False
 screenmat=bpy.data.materials.new('Screen self luminous, uncalibrated');screenmat.use_nodes=True;n=screenmat.node_tree.nodes;n.clear();out=n.new('ShaderNodeOutputMaterial');em=n.new('ShaderNodeEmission');tx=n.new('ShaderNodeTexImage');tx.image=bpy.data.images.load(str(OUT/'base-0192.png'));screenmat.node_tree.links.new(tx.outputs['Color'],em.inputs['Color']);screenmat.node_tree.links.new(em.outputs[0],out.inputs[0]);em.inputs['Strength'].default_value=1
 bpy.ops.mesh.primitive_plane_add(size=2,location=(0,-.015,1.55),rotation=(math.pi/2,0,0));screen=bpy.context.object;screen.name='Display 1.8m x 1.35m';screen.scale=(.9,.675,1);screen.data.materials.append(screenmat)
 for l in [key,rim,fill]:l.hide_render=False;l.data.color=(1,1,1);l.data.energy=350
 camera.hide_render=False;camera.data.type='PERSP';camera.data.lens=28;camera.data.sensor_width=36;camera.data.sensor_fit='HORIZONTAL';s.camera=camera
 gallery_records=[]
 for distance in [.9,1.8,3.6]:
  camera.location=(0,-distance-.015,1.55);aim(camera,(0,-.015,1.55));s.render.filepath=str(OUT/f'gallery-{distance:.1f}m.png');bpy.ops.render.render(write_still=True)
  gallery_records.append({'requested_eye_to_screen_m':distance,'actual_eye_to_screen_m':abs(camera.location.y-screen.location.y),'screen_center':list(screen.location),'camera_center':list(camera.location),'sensor_width_mm':camera.data.sensor_width,'sensor_fit':camera.data.sensor_fit,'lens_mm':camera.data.lens,'horizontal_fov_deg':math.degrees(camera.data.angle_x),'vertical_fov_deg':math.degrees(camera.data.angle_y),'note':'Fixed camera field; not simulation of human head/eye movement'})
 camera.location=(0,-.915,1.55);aim(camera,(0,-.015,1.55));camera.data.lens=16.5;s.render.filepath=str(OUT/'gallery-0.9m-wide-explanation.png');bpy.ops.render.render(write_still=True)
 gallery_records.append({'requested_eye_to_screen_m':.9,'actual_eye_to_screen_m':abs(camera.location.y-screen.location.y),'lens_mm':16.5,'horizontal_fov_deg':math.degrees(camera.data.angle_x),'note':'Different lens, full-screen explanatory view; NOT same-field distance comparison or human perception claim'})
 (OUT/'gallery-corrected-geometry.json').write_text(json.dumps(gallery_records,ensure_ascii=False,indent=2),encoding='utf-8')
 bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'gallery.blend'))
(OUT/(args.mode+'-'+args.variant+'-receipt.json')).write_text(json.dumps({'blender':bpy.app.version_string,'version':args.version,'mode':args.mode,'variant':args.variant,'frames':[1,192,384] if args.mode=='stills' else None,'fps':s.render.fps,'frame_range':[s.frame_start,s.frame_end],'resolution':[s.render.resolution_x,s.render.resolution_y],'view_transform':s.view_settings.view_transform,'look':s.view_settings.look,'exposure':s.view_settings.exposure,'objects':len(s.objects)},ensure_ascii=False,indent=2),encoding='utf-8')
print('FOLDS_COMPLETE',args.version,args.mode,args.variant,flush=True)
