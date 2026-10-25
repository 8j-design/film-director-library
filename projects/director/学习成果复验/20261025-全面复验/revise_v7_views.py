"""Revise viewing position after actual A/B/C/D comparison; preserve all story/assets/actions."""
import bpy,json
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent;O=R/'film/v7';O.mkdir(exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(R/'film/v6/studio-animation.blend'));s=bpy.context.scene
for name in ['05 Carry','06 After']:
 cam=bpy.data.objects[name];cam.location=(-3.6,-3.8,3.5);cam.rotation_euler=(Vector((-.1,.6,.85))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.lens=46
s['version']='v7';s['changes']='Carry and after cameras use tested C high-left view; all actions/assets/story retained. Recut with V6 unaffected intervals.'
s.frame_start=1;s.frame_end=1440;bpy.ops.wm.save_as_mainfile(filepath=str(O/'studio.blend'))
s.render.image_settings.media_type='VIDEO';s.render.image_settings.file_format='FFMPEG';s.render.ffmpeg.format='MPEG4';s.render.ffmpeg.codec='H264';s.render.ffmpeg.constant_rate_factor='MEDIUM';s.render.ffmpeg.ffmpeg_preset='GOOD'
for name,start,end in [('carry',625,965),('ending',1297,1440)]:
 s.frame_start=start;s.frame_end=end;s.render.filepath=str(O/f'{name}.mp4');bpy.ops.wm.save_as_mainfile(filepath=str(O/f'{name}-render-range.blend'));bpy.ops.render.render(animation=True)
# Actual edited movie: preserve unaffected V6 source intervals, rather than rerendering unchanged shots.
bpy.ops.wm.read_factory_settings(use_empty=True);s=bpy.context.scene;s.render.engine='BLENDER_EEVEE';s.render.use_sequencer=True;s.render.fps=24;s.frame_start=1;s.frame_end=1440
s.render.resolution_x=768;s.render.resolution_y=432;s.render.resolution_percentage=100;s.view_settings.view_transform='Standard';s.view_settings.look='None';seq=s.sequence_editor_create()
first=seq.strips.new_movie('V6 source frames 1-624',str(R/'film/v6/studio.mp4'),channel=1,frame_start=1);first.frame_offset_end=816
carry=seq.strips.new_movie('V7 new carry frames 625-965',str(O/'carry.mp4'),channel=2,frame_start=625)
middle=seq.strips.new_movie('V6 source frames 966-1296',str(R/'film/v6/studio.mp4'),channel=3,frame_start=1);middle.frame_offset_start=965;middle.frame_offset_end=144
ending=seq.strips.new_movie('V7 new ending frames 1297-1440',str(O/'ending.mp4'),channel=4,frame_start=1297)
expected=[(first,1,625),(carry,625,966),(middle,966,1297),(ending,1297,1441)]
for strip,st,en in expected:assert (strip.frame_final_start,strip.frame_final_end)==(st,en),(strip.name,strip.frame_final_start,strip.frame_final_end)
s.render.image_settings.media_type='VIDEO';s.render.image_settings.file_format='FFMPEG';s.render.ffmpeg.format='MPEG4';s.render.ffmpeg.codec='H264';s.render.ffmpeg.constant_rate_factor='MEDIUM';s.render.ffmpeg.ffmpeg_preset='GOOD';s.render.filepath=str(O/'studio.mp4');bpy.ops.wm.save_as_mainfile(filepath=str(O/'edit.blend'));bpy.ops.render.render(animation=True)
(O/'edit-source-map.json').write_text(json.dumps([{'strip':x.name,'timeline_inclusive':[st,en-1],'file':x.filepath,'offset_start':x.frame_offset_start,'offset_end':x.frame_offset_end} for x,st,en in expected],ensure_ascii=False,indent=2),encoding='utf-8')
print('V7_COMPLETE',flush=True)
