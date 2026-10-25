"""Original, editable six-shot puppet previs of the existing Last Print exercise.
No imported character/image/music assets. Blender 5.2.3. Not a finished film.
"""
import bpy, math, argparse,sys,json
from pathlib import Path
from mathutils import Vector,Matrix,Quaternion
P=argparse.ArgumentParser();P.add_argument('--version',default='v1');P.add_argument('--mode',default='samples',choices=['samples','movie','single']);P.add_argument('--frames',default='')
a=P.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []);R=Path(__file__).resolve().parent;O=R/'film'/a.version;O.mkdir(parents=True,exist_ok=True);REV=a.version!='v1'
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
s=bpy.context.scene;s.render.engine='BLENDER_EEVEE';s.render.resolution_x=960;s.render.resolution_y=540;s.render.resolution_percentage=100;s.render.fps=24;s.frame_start=1;s.frame_end=1440
s.render.image_settings.media_type='IMAGE';s.render.image_settings.file_format='PNG';s.view_settings.view_transform='AgX';s.view_settings.look='AgX - Medium High Contrast';s.view_settings.exposure=0
s.world.color=(.18,.18,.18);s.unit_settings.system='METRIC';s.unit_settings.scale_length=1
def col(h):
 v=[int(h[i:i+2],16)/255 for i in [0,2,4]];return tuple(x/12.92 if x<.04045 else ((x+.055)/1.055)**2.4 for x in v)+(1,)
def mat(name,h,rough=.8,metal=0,noise=False):
 m=bpy.data.materials.new(name);m.diffuse_color=col(h);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=m.diffuse_color;p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal
 if noise:
  n=m.node_tree.nodes.new('ShaderNodeTexNoise');n.inputs['Scale'].default_value=95;n.inputs['Detail'].default_value=2;b=m.node_tree.nodes.new('ShaderNodeBump');b.inputs['Strength'].default_value=.18;b.inputs['Distance'].default_value=.002;m.node_tree.links.new(n.outputs['Fac'],b.inputs['Height']);m.node_tree.links.new(b.outputs['Normal'],p.inputs['Normal'])
 return m
M={n:mat(n,h,r,me,tex) for n,h,r,me,tex in [('wall','C9C2AA',.95,0,True),('wood','91734C',.84,0,True),('darkwood','403A30',.8,0,True),('paper','E6D9B9',.95,0,True),('card','A08053',.96,0,True),('blue','284E6B',.85,0,True),('rust','974D36',.94,0,True),('teal','406D6A',.95,0,True),('skinA','BC9274',.95,0,True),('skinB','CBA586',.95,0,True),('hair','2E2924',.9,0,True),('pants','353E46',.92,0,True),('metal','525958',.48,.6,False),('black','151D21',.8,0,False),('leaf','596848',.9,0,True),('mark','DBD6C2',.97,0,False)]}
def empty(name,parent=None):
 ob=bpy.data.objects.new(name,None);s.collection.objects.link(ob);ob.parent=parent;return ob
def cube(name,loc,dim,material,parent=None,bevel=.008):
 bpy.ops.mesh.primitive_cube_add(size=1);ob=bpy.context.object;ob.name=name;ob.parent=parent;ob.location=loc;ob.dimensions=dim;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);ob.data.materials.append(material)
 if bevel:md=ob.modifiers.new('Soft handmade edges','BEVEL');md.width=bevel;md.segments=2
 return ob
def ball(name,loc,scale,material,parent=None):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=20,ring_count=12,radius=1);o=bpy.context.object;o.name=name;o.parent=parent;o.location=loc;o.scale=scale;o.data.materials.append(material)
 for p in o.data.polygons:p.use_smooth=True
 return o
def line(name,points,r,material,parent=None):
 cu=bpy.data.curves.new(name,'CURVE');cu.dimensions='3D';cu.bevel_depth=r;cu.bevel_resolution=2;sp=cu.splines.new('POLY');sp.points.add(len(points)-1)
 for p,v in zip(sp.points,points):p.co=(*v,1)
 ob=bpy.data.objects.new(name,cu);s.collection.objects.link(ob);ob.parent=parent;ob.data.materials.append(material);return ob
def cylinder(name,r,material):
 bpy.ops.mesh.primitive_cylinder_add(vertices=16,radius=r,depth=1);o=bpy.context.object;o.name=name;o.data.materials.append(material)
 for p in o.data.polygons:p.use_smooth=True
 return o
def segment(ob,start,end):
 start,end=Vector(start),Vector(end);ob.location=(start+end)/2;ob.rotation_euler=(end-start).to_track_quat('Z','Y').to_euler();ob.scale.z=(end-start).length;ob.keyframe_insert('location');ob.keyframe_insert('rotation_euler');ob.keyframe_insert('scale')
def key(ob,loc=None,rot=None,scale=None):
 if loc is not None:ob.location=loc;ob.keyframe_insert('location')
 if rot is not None:ob.rotation_euler=rot;ob.keyframe_insert('rotation_euler')
 if scale is not None:ob.scale=scale;ob.keyframe_insert('scale')
def smooth(t):return max(0,min(1,t))**2*(3-2*max(0,min(1,t)))
def blend(x,y,t):return Vector(x).lerp(Vector(y),max(0,min(1,t)))
def path(f,keys):
 if f<=keys[0][0]:return Vector(keys[0][1])
 for (f0,p0),(f1,p1) in zip(keys,keys[1:]):
  if f<=f1:return blend(p0,p1,smooth((f-f0)/(f1-f0)))
 return Vector(keys[-1][1])
# A coherent room, with a real gap for the doorway and a right-hand window opening.
cube('Floor',(0,0,-.06),(5.2,4.3,.12),M['wood'])
for i in range(15):line('Floor seam %02d'%i,[(-2.6,-2+i*.29,.002),(2.6,-2+i*.29,.002)],.003,M['darkwood'])
cube('Back wall main',(.65,2.02,1.35),(3.9,.12,2.7),M['wall']);cube('Back left wall',(-2.4,2.02,1.35),(.4,.12,2.7),M['wall']);cube('Above door',(-1.75,2.02,2.43),(1,.12,.54),M['wall'])
for x in [-2.25,-1.25]:cube('Door jamb',(x,1.95,1.05),(.055,.12,2.1),M['darkwood'])
cube('Door lintel',(-1.75,1.95,2.1),(1.06,.12,.07),M['darkwood'])
cube('Right wall lower',(2.53,0,.5),(.12,4,1),M['wall']);cube('Right wall upper',(2.53,0,2.6),(.12,4,.2),M['wall'])
for y in [-1.95,.4,1.95]:cube('Right wall pier',(2.53,y,1.8),(.12,.14,1.6),M['wall'])
for z in [1.05,2.4]:cube('Window frame',(2.45,-.7,z),(.08,2.3,.06),M['paper'])
for y in [-1.8,-.7,.4]:cube('Window mullion',(2.45,y,1.74),(.08,.04,1.35),M['paper'])
cube('Worktable top',(0,0,.88),(2.25,1.12,.09),M['wood'])
for x in [-.93,.93]:
 for y in [-.43,.43]:cube('Table leg',(x,y,.43),(.085,.085,.86),M['darkwood'])
cube('Table stretcher',(0,.35,.19),(1.9,.055,.08),M['darkwood'])
cube('Back bench',(.4,1.68,.72),(2.7,.44,.08),M['darkwood'])
# Permanent print rack/press are deliberately retained; personal belongings move separately.
for z in [.25,.45,.65,.85,1.05,1.25]:cube('Drying rack tray',(1.73,1.58,z),(.7,.55,.022),M['metal'])
for x in [1.38,2.08]:cube('Rack upright',(x,1.58,.72),(.035,.55,1.45),M['metal'])
cube('Printing press base',(1.2,-.65,.66),(.75,.6,.13),M['metal']);cube('Press feet',(1.2,-.65,.29),(.6,.46,.58),M['darkwood'])
for x in [.9,1.5]:cube('Press support',(x,-.65,.94),(.08,.11,.6),M['black'])
roller=cylinder('Press roller',.08,M['metal']);roller.location=(1.2,-.65,1.13);roller.rotation_euler.y=math.pi/2;roller.scale.z=.7
line('Press handle',[(1.59,-.65,1.13),(1.75,-.65,1.13),(1.75,-.65,1.32)],.018,M['metal'])
# Two wall marks and hooks, revealed by actually removing the personal pictures.
wallart=[]
for idx,x in enumerate([-.9,.6]):
 cube('Wall trace '+str(idx),(x,1.945,1.55),(.42,.006,.34),M['mark'],bevel=0)
 ball('Wall hook '+str(idx),(x,1.92,1.76),(.015,.015,.015),M['metal'])
 root=empty('Personal picture '+str(idx));root.location=(x,1.90,1.55)
 cube('Picture paper '+str(idx),(0,0,0),(.36,.014,.28),M['paper'],root)
 for j in range(4):line('Private picture mark',[(v, -.011,.055*math.sin(v*25+j)) for v in [-.14,-.07,0,.07,.14]],.007,M['rust' if idx==0 else 'teal'],root)
 wallart.append(root)
def box(name,color):
 e=empty(name);cube(name+' base',(0,0,0),(.38,.29,.025),M['card'],e)
 for x in [-.18,.18]:cube(name+' side',(x,0,.12),(.018,.29,.25),M['card'],e)
 for y in [-.14,.14]:cube(name+' face',(0,y,.12),(.38,.018,.25),M['card'],e)
 cube(name+' identification strip',(0,-.152,.12),(.2,.005,.045),M[color],e,0)
 return e
boxes=[box('Private box A','rust'),box('Private box B','teal')]
boxstart=[Vector((-.87,-.02,.94)),Vector((.87,-.02,.94))]
# The single persistent print, boards, lid and band share a stable asset root.
pack=empty('Shared object PRINT_01');pack['paper_dimensions_m']=[1.1,.4];pack['board_dimensions_m']=[1.14,.44]
cube('Bottom board',(0,0,0),(1.14,.44,.018),M['card'],pack)
cube('Single sheet PRINT_01',(0,0,.013),(1.1,.4,.002),M['paper'],pack,0)
for j in range(6):line('Original print blue wave '+str(j),[(x,-.16+j*.058+.013*math.sin(x*15+j*.7),.015) for x in [i*.022-.52 for i in range(48)]],.0065,M['blue'],pack)
lidhinge=empty('Board cover hinge',pack);lidhinge.location=(0,.22,.026)
cube('Top cover',(0,-.22,0),(1.14,.44,.015),M['card'],lidhinge)
band=cube('Blue cotton band',(0,0,.043),(.037,.45,.007),M['blue'],pack,.002)
bow=empty('Cotton knot',pack);bow.location=(0,0,.056)
for side in [-1,1]:line('Bow loop',[(0,0,0),(side*.065,.035,.016),(side*.06,-.025,.012),(0,0,0)],.007,M['blue'],bow)
line('Bow tail',[(-.01,0,0),(-.07,-.09,.006)],.006,M['blue'],bow)
# Independent private tools and keys, never duplicate the long shared package.
tools=[]
for idx,loc in enumerate([(-.7,-.28,.95),(.7,-.28,.95)]):
 e=empty('Private tool '+str(idx));ball('Ink bottle',(.0,0,.06),(.035,.035,.065),M['blue'],e);cube('Bottle cap',(0,0,.125),(.045,.045,.02),M['metal'],e);tools.append(e)
keys=[]
for idx in range(2):
 e=empty('Room key '+str(idx));line('Key stem',[(0,0,0),(.07,0,0),(.07,.025,0),(.06,.025,0)],.006,M['metal'],e);line('Key ring',[(.017*math.cos(i*math.pi/8),.017*math.sin(i*math.pi/8),0) for i in range(17)],.004,M['metal'],e);keys.append(e)
def make_person(name,shirt,skin,bun=False):
 root=empty(name)
 ball(name+' pelvis',(0,0,.88),(.16,.105,.16),M['pants'],root)
 ball(name+' shirt torso',(0,0,1.18),(.22,.125,.31),M[shirt],root)
 cube(name+' shirt opening',(0,-.126,1.21),(.018,.012,.35),M['darkwood'],root,.002)
 for z in [1.06,1.17,1.28]:ball(name+' button',(0,-.14,z),(.009,.009,.009),M['paper'],root)
 ball(name+' neck',(0,0,1.45),(.058,.058,.09),M[skin],root)
 head=empty(name+' head',root);head.location=(0,0,1.60)
 ball(name+' face',(0,-.015,0),(.108,.095,.14),M[skin],head)
 ball(name+' nose',(0,-.105,-.018),(.025,.031,.028),M[skin],head)
 for x in [-.108,.108]:ball(name+' ear',(x,0,-.005),(.02,.017,.035),M[skin],head)
 for x in [-.045,.045]:
  ball(name+' eye white',(x,-.101,.026),(.021,.009,.013),M['paper'],head);ball(name+' pupil',(x,-.109,.026),(.009,.006,.01),M['black'],head)
  line(name+' eyebrow',[(x-.022,-.099,.057),(x,-.105,.061),(x+.02,-.099,.053)],.006,M['hair'],head)
 line(name+' mouth',[(-.027,-.102,-.057),(0,-.109,-.061),(.026,-.102,-.056)],.003,M['darkwood'],head)
 ball(name+' hair cap',(0,.016,.085),(.116,.097,.075),M['hair'],head)
 for x,z in [(-.065,.085),(.01,.115),(.07,.08)]:ball(name+' hair lock',(x,-.073,z),(.052,.035,.034),M['hair'],head)
 if bun:ball(name+' bun',(0,.12,.07),(.077,.07,.073),M['hair'],head)
 limbs={}
 for side in [-1,1]:
  limbs[side]={'upper':cylinder(name+' upper arm',.065,M[shirt]),'lower':cylinder(name+' sleeve',.052,M[shirt]),'hand':ball(name+' mitten',(0,0,0),(.043,.028,.066),M[skin]),'thigh':cylinder(name+' trouser thigh',.075,M['pants']),'calf':cylinder(name+' trouser calf',.06,M['pants']),'shoe':ball(name+' shoe',(0,0,0),(.07,.13,.048),M['darkwood'])}
 return root,head,limbs
people=[make_person('Person A','rust','skinA'),make_person('Person B','teal','skinB',True)]
def aim(ob,pt):ob.rotation_euler=(Vector(pt)-ob.location).to_track_quat('-Z','Y').to_euler()
def camera(name,pos,pt,lens):
 bpy.ops.object.camera_add(location=pos);c=bpy.context.object;c.name=name;c.data.lens=lens;c.data.sensor_width=36;aim(c,pt);return c
cams=[camera('01 Shared studio',(4.2,-6.7,3.4),(0,.3,1),43),camera('02 Personal traces',(3.1,-4.8,2.6),(-.1,1,1.4),48),camera('03 Shared print',(2.7,-4.4,2.35),(0,.2,1.17),59),camera('04 Wrapping',(1.6,-2.6,2.7),(0,.1,1.0),53),camera('05 Carry and depart',(3.4,-5.8,3.2),(-.3,.6,1),43),camera('06 After',(4.2,-6.7,3.4),(0,.3,1),43)]
starts=[1,145,289,433,625,1249]
for i,(c,f) in enumerate(zip(cams,starts)):m=s.timeline_markers.new('Shot '+str(i+1),frame=f);m.camera=c
s.camera=cams[0]
for name,pos,power,color,size in [('Window light',(3,-.5,4),1100,(1,.94,.82),4),('Soft front',(-2,-4,3),650,(.83,.91,1),5),('Back bounce',(0,1,3.8),300,(1,.88,.72),3)]:
 d=bpy.data.lights.new(name,'AREA');d.energy=power;d.color=color;d.shape='DISK';d.size=size;o=bpy.data.objects.new(name,d);s.collection.objects.link(o);o.location=pos;aim(o,(0,.4,1))
def shotidx(f):return sum(f>=x for x in starts)-1
finalrot=Matrix(((0,1,0),(0,0,1),(1,0,0))).to_quaternion()
roots0=[Vector((-.72,.66,0)),Vector((.72,.66,0))]
contacts=[]
def state(f,idx):
 side=-1 if idx==0 else 1;origin=roots0[idx]
 return path(f,[(1,origin),(145,origin),(176,(side*.75,1.46,0)),(208,(side*.75,1.46,0)),(264,origin),(624,origin),(696,(side*.60,.65,0)),(792,(-1.03+side*.58,1.35,0)),(850,(-1.03+side*.58,1.35,0)),(942,origin),(1080+idx*48,origin),(1176+idx*24,(-1.75,2.15,0)),(1248,(-4.5,3,0)),(1440,(-4.5,3,0))])
def packstate(f):
 p=path(f,[(1,(0,0,.946)),(624,(0,0,.946)),(684,(0,0,1.15)),(792,(-1.03,1.40,1.15)),(850,(-1.03,1.66,.59)),(1440,(-1.03,1.66,.59))])
 q=Quaternion((1,0,0,0)).slerp(finalrot,smooth((f-792)/58))
 return p,q
def transform(p,yaw,v):return Vector(p)+Matrix.Rotation(yaw,3,'Z')@Vector(v)
for f in range(1,1441,3):
 s.frame_set(f);pp,pq=packstate(f);key(pack,pp,pq.to_euler())
 lidangle=-math.radians(105)*(1-smooth((f-450)/108));key(lidhinge,rot=(lidangle,0,0))
 bandt=smooth((f-558)/45);key(band,scale=(1,max(.001,bandt),1));key(bow,scale=(max(.001,smooth((f-603)/21)),)*3)
 for idx,(root,head,limbs) in enumerate(people):
  side=-1 if idx==0 else 1;rp=state(f,idx);future=state(f+3,idx);vel=future-rp
  yaw=0
  if 150<f<236:yaw=math.pi
  if 650<f<850:yaw=0
  if 1080+idx*48<f<1248:yaw=math.pi
  key(root,rp,rot=(0,0,yaw))
  key(head,rot=(.20 if f<624 else .08,0,side*.22 if 320<f<400 else 0))
  # Pictures are removed through visible movement, not an unexplained cut.
  wp=Vector(([-.9,.6][idx],1.9,1.55));bp=boxstart[idx]
  picpos=path(f,[(1,wp),(188+idx*12,wp),(210+idx*12,wp+Vector((0,-.13,0))),(252+idx*12,bp+Vector((0,0,.06))),(1440,bp+Vector((0,0,.06)))])
  key(wallart[idx],picpos,rot=(math.radians(90)*smooth((f-214-idx*12)/40),0,0))
  bpos=bp
  if f>1044+idx*48:
   carry=transform(rp,yaw,(0,-.29,1.04));bpos=blend(bp,carry,smooth((f-1044-idx*48)/36))
  key(boxes[idx],bpos,rot=(0,0,yaw if f>1080+idx*48 else 0))
  tstart=Vector((side*.7,-.28,.95));tend=bp+Vector((0,0,.06));toolp=path(f,[(1,tstart),(42,tstart+Vector((0,0,.16))),(84,tend+Vector((0,0,.15))),(120,tend),(1440,tend)])
  if f>1044+idx*48:toolp=bpos+Vector((0,0,.06))
  key(tools[idx],toolp)
  if f>1044+idx*48:key(wallart[idx],bpos+Vector((0,0,.08)))
  keyp=path(f,[(1,transform(rp,yaw,(side*.1,-.09,1.0))),(966+idx*36,transform(rp,yaw,(side*.1,-.09,1.0))),(1014+idx*36,(side*.16,-.18,.937)),(1440,(side*.16,-.18,.937))])
  key(keys[idx],keyp)
  for arm_side,bones in limbs.items():
   shoulder=transform(rp,yaw,(arm_side*.20,0,1.39));hand=transform(rp,yaw,(arm_side*.22,-.28,.99))
   if f<144 and arm_side==side:hand=toolp+Vector((0,0,.04))
   elif 176+idx*12<f<270+idx*12 and arm_side==side:hand=picpos+Vector((side*.10,-.01,.01))
   elif 289<f<433:hand=Vector((arm_side*.43,.12,.97))
   elif 433<=f<624:
    if idx==0:hand=Vector((arm_side*.45,-.12,.98))
    else:
     local=Vector((arm_side*.40,-.21,0));hand=pp+Vector((0,.22,.026))+Matrix.Rotation(lidangle,3,'X')@local
     if f>558:hand=Vector((arm_side*.11,(1-bandt)*.22-.02,1.03))
   elif 624<=f<792:hand=pp+pq@Vector((side*.49,arm_side*.09,.05))
   elif 792<=f<850:
    if idx==0:hand=blend(pp+pq@Vector((-.49,arm_side*.09,.05)),transform(rp,yaw,(arm_side*.22,-.24,1.0)),smooth((f-792)/24))
    else:hand=pp+pq@Vector((.43,arm_side*.16,.05))
   elif 966+idx*36<=f<=1014+idx*36 and arm_side==side:hand=keyp+Vector((0,0,.025))
   elif f>=1044+idx*48:hand=bpos+Matrix.Rotation(yaw,3,'Z')@Vector((arm_side*.17,-.05,.09))
   diff=hand-shoulder;length=diff.length
   # Both arm segments together measure 60cm. Record out-of-reach instead of hiding it.
   if length>.60 and f%24==1:contacts.append({'frame':f,'person':idx,'arm':arm_side,'reach_m':length,'target':list(hand)})
   direction=diff.normalized();out=Vector((arm_side*.85,-.12,-.7));out=(out-direction*out.dot(direction)).normalized();distance=min(length,.598);mid=shoulder+direction*(distance/2)+out*math.sqrt(max(0,.30**2-(distance/2)**2))
   actualhand=shoulder+direction*distance
   segment(bones['upper'],shoulder,mid);segment(bones['lower'],mid,actualhand);key(bones['hand'],actualhand,rot=(0,0,yaw))
   walk=vel.length>.004;stride=.08*math.sin(f*.14+arm_side*math.pi/2) if walk else 0;lift=max(0,.05*math.sin(f*.14+arm_side*math.pi/2)) if walk else 0
   hip=transform(rp,yaw,(arm_side*.09,0,.87));foot=transform(rp,yaw,(arm_side*.095,stride,.05+lift));knee=blend(hip,foot,.53)+Matrix.Rotation(yaw,3,'Z')@Vector((0,-.055,0));segment(bones['thigh'],hip,knee);segment(bones['calf'],knee,foot);key(bones['shoe'],foot+Matrix.Rotation(yaw,3,'Z')@Vector((0,-.045,0)),rot=(0,0,yaw))
# Preserve a deterministic baked action without runtime handlers.
for action in bpy.data.actions:
 try:
  for layer in action.layers:
   for strip in layer.strips:
    for bag in strip.channelbags:
     for fc in bag.fcurves:
      for kp in fc.keyframe_points:kp.interpolation='LINEAR'
 except Exception:pass
s['exercise']='Existing Last Print, six-shot native puppet previs, no dialogue/captions';s['version']=a.version;s['limits']='No live cloth/finger physics, realistic face acting, actual audience or full audiovisual acceptance'
s.frame_set(1);bpy.ops.wm.save_as_mainfile(filepath=str(O/'studio.blend'))
(O/'reach-diagnostics.json').write_text(json.dumps({'scope':'Targets over 0.60m sampled each second, not a collision/art pass','out_of_reach':contacts},ensure_ascii=False,indent=2),encoding='utf-8')
if a.mode=='movie':
 s.render.resolution_x=768;s.render.resolution_y=432;s.render.image_settings.media_type='VIDEO';s.render.image_settings.file_format='FFMPEG';s.render.ffmpeg.format='MPEG4';s.render.ffmpeg.codec='H264';s.render.ffmpeg.constant_rate_factor='MEDIUM';s.render.ffmpeg.ffmpeg_preset='GOOD';s.render.filepath=str(O/'studio.mp4');bpy.ops.wm.save_as_mainfile(filepath=str(O/'studio-animation.blend'));bpy.ops.render.render(animation=True)
else:
 frames=[int(x) for x in a.frames.split(',')] if a.frames else sorted(set(list(range(1,1441,24))+[144,145,188,210,252,288,289,432,433,450,504,558,603,624,625,684,792,820,850,942,966,1014,1044,1080,1128,1176,1200,1248,1249,1440]))
 for f in frames:
  s.frame_set(f);s.camera=cams[shotidx(f)];s.render.filepath=str(O/f'{f:04d}.png');bpy.ops.render.render(write_still=True)
 (O/'sample-frames.json').write_text(json.dumps(frames),encoding='utf-8')
print('STUDIO_COMPLETE',a.version,a.mode,'reach warnings',len(contacts),flush=True)
