"""Decode locally obtained official public movie for visual research; no redistribution."""
import bpy,json,sys,hashlib
from pathlib import Path
R=Path(__file__).resolve().parent;src=R/'reference_media/pas_de_deux_360p_hls_concat.ts';out=R/'reference_media/pas_frames';out.mkdir(exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True);s=bpy.context.scene
s.render.engine='BLENDER_EEVEE';s.render.use_sequencer=True;s.render.fps=24
s.render.resolution_x=480;s.render.resolution_y=360;s.render.resolution_percentage=100
s.render.image_settings.file_format='PNG';s.view_settings.view_transform='Standard';s.view_settings.look='None'
seq=s.sequence_editor_create();strip=seq.strips.new_movie('Official NFB research copy',str(src),channel=1,frame_start=1)
frames=sorted(set([1,strip.frame_duration]+list(range(1,strip.frame_duration+1,192))))
receipt={'source_local':src.name,'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'strip_duration_frames':strip.frame_duration,'scene_fps':24,'scene_duration_seconds':strip.frame_duration/24,'source_fps':getattr(strip,'fps',None),'samples':frames,'limits':'Full-file movie-strip load and systematic stills, not real-time viewing or hearing. Local only.'}
(out/'decode-receipt.json').write_text(json.dumps(receipt,indent=2),encoding='utf-8')
for f in frames:
 s.frame_set(f);s.render.filepath=str(out/f'{f:05d}.png');bpy.ops.render.render(write_still=True)
print(json.dumps(receipt),flush=True)
