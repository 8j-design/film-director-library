import bpy,json
from pathlib import Path
R=Path(__file__).resolve().parent;O=R/'reference_media/sprite_detail';O.mkdir(exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True);s=bpy.context.scene;s.render.engine='BLENDER_EEVEE';s.render.use_sequencer=True;s.render.fps=24;s.render.resolution_x=768;s.render.resolution_y=322;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.view_settings.view_transform='Standard';s.view_settings.look='None'
strip=s.sequence_editor_create().strips.new_movie('Official film detail research',str(R/'reference_media/sprite_fright_official_720p.mp4'),channel=1,frame_start=1)
frames=list(range(10489,10718,12))+[1249,4465,5041,5905,7489,14833]
for f in frames:
 s.frame_set(f);s.render.filepath=str(O/f'{f:05d}.png');bpy.ops.render.render(write_still=True)
(O/'detail-sample-map.json').write_text(json.dumps({'frames':frames,'basis':'Chosen after actual whole-span interval review: object use window near438-446s plus prop/pose and final license credits','fps':24,'limits':'stills, not real-time or audio perception'},indent=2),encoding='utf-8')
print('DETAIL_COMPLETE',len(frames),flush=True)
