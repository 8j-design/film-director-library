"""Native reopen, explicit scale/state receipt, actual movie decode. Not artistic acceptance."""
import bpy,json,hashlib,math,sys
from pathlib import Path
R=Path(__file__).resolve().parent;version=sys.argv[sys.argv.index('--')+1] if '--' in sys.argv else 'v6';O=R/'film'/version;V=O/'verification';V.mkdir(exist_ok=True)
native_path=O/'studio-animation.blend' if (O/'studio-animation.blend').exists() else O/'studio.blend'
bpy.ops.wm.open_mainfile(filepath=str(native_path));s=bpy.context.scene
native={'blender':bpy.app.version_string,'objects':len(s.objects),'meshes':sum(x.type=='MESH' for x in s.objects),'external_images':[x.filepath for x in bpy.data.images if x.source=='FILE' and not x.packed_file],'states':[]}
for f in [1,188,252,333,400,480,558,624,660,792,850,1014,1050,1176,1240,1440]:
 s.frame_set(f)
 row={'frame':f,'camera':s.camera.name,'print_position':list(bpy.data.objects['Shared object PRINT_01'].matrix_world.translation),'paper_local_dimensions':list(bpy.data.objects['Single sheet PRINT_01'].dimensions),'bottom_board_local_dimensions':list(bpy.data.objects['Bottom board'].dimensions),'person_positions':[list(bpy.data.objects[x].location) for x in ['Person A','Person B']]}
 assert all(math.isfinite(v) for v in row['print_position']);native['states'].append(row)
assert not native['external_images']
# A distinct editable variant, keeping the original source and movie intact.
band=bpy.data.objects['Blue cotton band'];copy=band.data.materials[0].copy();copy.name='Local edit band teal';copy.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.05,.25,.23,1);band.data.materials[0]=copy
bpy.ops.wm.save_as_mainfile(filepath=str(V/'reopened-band-color-edit.blend'))
bpy.ops.wm.read_factory_settings(use_empty=True);s=bpy.context.scene;s.render.engine='BLENDER_EEVEE';s.render.use_sequencer=True;s.render.use_compositing=False;s.render.fps=24
s.render.resolution_x=192;s.render.resolution_y=108;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.view_settings.view_transform='Standard';s.view_settings.look='None'
seq=s.sequence_editor_create();movie=seq.strips.new_movie('Actual original preview',str(O/'studio.mp4'),channel=1,frame_start=1)
assert movie.frame_duration==1440,movie.frame_duration
tiny=V/'decoded-all';tiny.mkdir(exist_ok=True)
for f in range(1,1441):
 s.frame_set(f);s.render.filepath=str(tiny/f'{f:04d}.png');bpy.ops.render.render(write_still=True)
selected=sorted(set([1,1440]+list(range(1,1441,24))+list(range(180,265,12))+list(range(324,403,6))+list(range(396,559,12))+list(range(552,661,6))+list(range(792,851,6))+list(range(960,1057,6))+list(range(1080,1297,12))))
large=V/'selected';large.mkdir(exist_ok=True);s.render.resolution_x=768;s.render.resolution_y=432
for f in selected:
 s.frame_set(f);s.render.filepath=str(large/f'{f:04d}.png');bpy.ops.render.render(write_still=True)
receipt={'native_reopen':native,'movie':{'file':'studio.mp4','bytes':(O/'studio.mp4').stat().st_size,'sha256':hashlib.sha256((O/'studio.mp4').read_bytes()).hexdigest(),'fps':movie.fps,'frames':movie.frame_duration,'seconds':movie.frame_duration/movie.fps,'technical_decode_frames':1440,'technical_decode_size':[192,108],'selected_actual_frames':selected,'selected_size':[768,432],'audio':'No audio track authored. This is an unfinished silent motion/layout preview, not final sound design.'},'limits':'Technical decode and systematic visual still review remain separate from real-time viewing, hearing, human feedback, weight, finger or cloth physics, full artistic pass.'}
(V/'native-video-receipt.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2),encoding='utf-8')
print('VERIFY_COMPLETE',len(selected),'systematic and dense samples',flush=True)
