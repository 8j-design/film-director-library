"""Official public full-film research copy: interval still coverage, not real-time playback."""
import bpy,json,hashlib
from pathlib import Path
R=Path(__file__).resolve().parent;src=R/'reference_media/sprite_fright_official_720p.mp4';out=R/'reference_media/sprite_frames';out.mkdir(exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True);s=bpy.context.scene;s.render.engine='BLENDER_EEVEE';s.render.use_sequencer=True;s.render.fps=24
s.render.resolution_x=768;s.render.resolution_y=322;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.view_settings.view_transform='Standard';s.view_settings.look='None'
strip=s.sequence_editor_create().strips.new_movie('Official public Sprite Fright',str(src),channel=1,frame_start=1)
frames=sorted(set([1,strip.frame_duration]+list(range(1,strip.frame_duration+1,144))))
receipt={'source':src.name,'sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'blender_fps':strip.fps,'blender_duration_frames':strip.frame_duration,'duration_seconds':strip.frame_duration/strip.fps,'extract_size':[768,322],'source_server_probe_dimensions':[1718,720],'every_source_frames':144,'samples':frames,'limits':'Interval still coverage; not whole-film real-time viewing, no hearing or audience acceptance.'}
(out/'decode-receipt.json').write_text(json.dumps(receipt,indent=2),encoding='utf-8')
for f in frames:
 s.frame_set(f);s.render.filepath=str(out/f'{f:05d}.png');bpy.ops.render.render(write_still=True)
print('SPRITE_DECODE',json.dumps(receipt),flush=True)
