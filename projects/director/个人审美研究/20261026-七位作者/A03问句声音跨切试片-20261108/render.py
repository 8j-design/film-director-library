from array import array
from hashlib import sha256
from pathlib import Path
import json
import os
import shutil
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
REFERENCE = HERE.parent / 'A03问句跨切试片-20261108' / 'carry-02.mp4'
LOCAL_FFMPEG = HERE.parent.parent / '研究媒体工具/imageio-ffmpeg/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
FFMPEG = os.environ.get('FFMPEG') or (str(LOCAL_FFMPEG) if LOCAL_FFMPEG.is_file() else shutil.which('ffmpeg'))
RATE = 48000
CUT = 43 * RATE // 30
LENGTH = 3 * RATE
SPEECH_THRESHOLD = 96

def ffmpeg(*args, data=None):
    return subprocess.check_output([FFMPEG, '-v', 'error', *map(str, args)], input=data)

def decode(source, codec):
    if codec == 'video':
        return ffmpeg('-i', source, '-map', '0:v:0', '-pix_fmt', 'yuv420p', '-f', 'rawvideo', '-')
    return array('h', ffmpeg('-i', source, '-map', '0:a:0', '-ac', '1', '-ar', RATE, '-f', 's16le', '-'))

def active_range(samples):
    active = [i for i, value in enumerate(samples) if abs(value) >= SPEECH_THRESHOLD]
    return active[0], active[-1] + 1

def synthesize():
    with tempfile.TemporaryDirectory(prefix='a03-voice-', dir=HERE) as tmp:
        out = Path(tmp) / 'voice.wav'
        env = dict(os.environ, A03_TEST_WAV=str(out))
        script = (
            'Add-Type -AssemblyName System.Speech; '
            '$speaker=[System.Speech.Synthesis.SpeechSynthesizer]::new(); '
            'try { $speaker.SelectVoice("Microsoft Zira Desktop"); $speaker.Rate=3; '
            '$speaker.SetOutputToWaveFile($env:A03_TEST_WAV); '
            '$speaker.Speak("Where are you taking her?"); } finally { $speaker.Dispose() }'
        )
        subprocess.run(['powershell', '-NoProfile', '-NonInteractive', '-Command', script], env=env, check=True)
        samples = decode(out, 'audio')
    first, last = active_range(samples)
    utterance = samples[max(first - 144, 0):last + 144]
    return utterance, active_range(utterance)

def main():
    assert FFMPEG and REFERENCE.is_file()
    utterance, (first, last) = synthesize()
    picture = decode(REFERENCE, 'video')
    assert len(picture) == 480 * 270 * 3 // 2 * 90
    summary = {'fixed_picture_sha256': sha256(picture).hexdigest(), 'frames': 90, 'fps': 30,
               'sample_rate': RATE, 'video_cut_sample': CUT, 'activity_threshold_pcm16': SPEECH_THRESHOLD,
               'voice': 'Windows Microsoft Zira Desktop, rate 3', 'human_listener_test': False, 'versions': {}}
    for name, offset in [('early', -12000), ('flush', 0), ('carry', 9600)]:
        insert = CUT + offset - last
        assert 0 <= insert and insert + len(utterance) <= LENGTH
        samples = array('h', [0]) * LENGTH
        samples[insert:insert + len(utterance)] = utterance
        output = HERE / f'voice-{name}.mp4'
        ffmpeg('-y', '-i', REFERENCE, '-f', 's16le', '-ac', '1', '-ar', RATE, '-i', '-',
               '-map', '0:v:0', '-map', '1:a:0', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '96k',
               '-t', '3', '-movflags', '+faststart', output, data=samples.tobytes())
        assert decode(output, 'video') == picture
        pcm = decode(output, 'audio')
        actual_first, actual_last = active_range(pcm)
        assert abs(actual_last - (CUT + offset)) < RATE * 0.035
        postcut = max(abs(s) for s in pcm[CUT:CUT + 9600])
        assert (postcut >= 320) == (name == 'carry')
        summary['versions'][name] = {'source_onset_sample': insert + first,
            'target_end_sample': CUT + offset, 'decoded_onset_sample': actual_first,
            'decoded_end_sample': actual_last, 'decoded_end_offset_ms': round((actual_last-CUT)*1000/RATE,2),
            'decoded_post_cut_peak_pcm16': postcut, 'file_sha256': sha256(output.read_bytes()).hexdigest()}
    (HERE / 'metadata.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(summary, ensure_ascii=False))

if __name__ == '__main__':
    main()
