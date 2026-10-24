"""Executed in Blender; actual reopening and full video-frame decode, not a viewing claim."""
import bpy, math,json,hashlib
from pathlib import Path
R=Path(__file__).resolve().parent;O=R/'artwork'/'v3';V=R/'verification';V.mkdir(exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(O/'folds-animation.blend'));s=bpy.context.scene
objects=[ob for ob in s.objects if ob.type=='MESH'];sample=[]
for frame in [1,72,96,144,192,216,240,250,288,336,384]:
 s.frame_set(frame);dg=bpy.context.evaluated_depsgraph_get();ob=bpy.data.objects['Coat shell - open front'];ev=ob.evaluated_get(dg);me=ev.to_mesh()
 coords=[tuple(v.co) for v in me.vertices];assert all(math.isfinite(c) for v in coords for c in v)
 sample.append({'frame':frame,'shell_x_range':[min(v[0] for v in coords),max(v[0] for v in coords)],'Open':ob.data.shape_keys.key_blocks['Open'].value,'Afterimage':ob.data.shape_keys.key_blocks['Afterimage'].value,'vertex_count':len(coords)})
 ev.to_mesh_clear()
native={'blender':bpy.app.version_string,'object_count':len(s.objects),'mesh_count':len(objects),'shape_key_objects':sum(bool(ob.data.shape_keys) for ob in objects),'external_images':[im.filepath for im in bpy.data.images if im.source=='FILE' and not im.packed_file],'samples':sample}
assert not native['external_images']
# A separate local edit and save demonstrates editability without touching the source.
clasp=bpy.data.objects['Brass clasp'];clasp.location.x+=.06
bpy.ops.wm.save_as_mainfile(filepath=str(V/'reopened-local-edit.blend'))
bpy.ops.wm.read_factory_settings(use_empty=True);s=bpy.context.scene
s.render.engine='BLENDER_EEVEE';s.render.resolution_x=192;s.render.resolution_y=144;s.render.resolution_percentage=100;s.render.fps=24
s.render.image_settings.media_type='IMAGE';s.render.image_settings.file_format='PNG';s.view_settings.view_transform='Standard';s.view_settings.look='None';s.view_settings.exposure=0
s.render.use_sequencer=True;s.render.use_compositing=False;s.world=bpy.data.worlds.new('Black')
seq=s.sequence_editor_create();movie=seq.strips.new_movie(name='Actual final MP4',filepath=str(O/'folds-of-air.mp4'),channel=1,frame_start=1)
assert movie.frame_duration==384, movie.frame_duration
s.frame_start=1;s.frame_end=384
decoded=V/'decoded-small';decoded.mkdir(exist_ok=True)
for frame in range(1,385):
 s.frame_set(frame);s.render.filepath=str(decoded/f'{frame:04d}.png');bpy.ops.render.render(write_still=True)
selected=[1,72,96,144,192,216,240,250,288,336,384]
s.render.resolution_x=768;s.render.resolution_y=576
for frame in selected:
 s.frame_set(frame);s.render.filepath=str(V/f'mp4-frame-{frame:04d}.png');bpy.ops.render.render(write_still=True)
receipt={'native_reopen':native,'video':{'path':str(O/'folds-of-air.mp4'),'bytes':(O/'folds-of-air.mp4').stat().st_size,'sha256':hashlib.sha256((O/'folds-of-air.mp4').read_bytes()).hexdigest(),'frame_duration':movie.frame_duration,'fps':s.render.fps,'duration_seconds':movie.frame_duration/s.render.fps,'full_decode_frames':384,'full_decode_size':[192,144],'selected_full_size_frames':selected,'selected_size':[768,576],'audio':'silent by design; no audio comprehension or MV completion claimed','scope':'Technical full-frame decode; selected images can be inspected, not continuous audiovisual viewing'}}
(V/'native-video-receipt.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2),encoding='utf-8')
print('NATIVE_VIDEO_VERIFY_COMPLETE',flush=True)
