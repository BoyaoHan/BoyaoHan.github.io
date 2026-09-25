#!/usr/bin/env python3
"""Prepare verified camera-count clips from the supplied ZIP and its local masters."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
import zipfile


def sha(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def layout(count):
    if count not in (3, 4, 5, 6):
        raise ValueError('Expected 3, 4, 5, or 6 cameras')
    width = min(320, (1920 - (count + 1) * 12) // count)
    return (1920 - (count * width + (count - 1) * 12)) // 2, width, width * 3 // 4 + 28


def graph(count):
    left, width, height = layout(count)
    pane_width = min(480, 1920 // count)
    parts = [f'[0:v]setpts=(PTS-STARTPTS)/4,fps=30,split={count+1}' + ''.join(f'[s{i}]' for i in range(count)) + '[base]']
    for i in range(count):
        parts.append(f'[s{i}]crop={width}:{height}:{left+i*(width+12)}:12:exact=1,scale={pane_width}:-2:flags=lanczos[p{i}]')
    parts.append(''.join(f'[p{i}]' for i in range(count)) + f'hstack=inputs={count},pad=1920:408:(ow-iw)/2:(oh-ih)/2:white[top]')
    parts.append('[base]crop=1024:576:448:384,scale=1920:1080:flags=lanczos[bottom]')
    parts.append('[top][bottom]vstack=inputs=2,setsar=1[out]')
    return ';'.join(parts)


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n')


def prepare(zip_path, destination, report_path):
    source = zip_path.parent
    output = destination / 'VersaCamVLA.github.io/media/camera-counts'
    output.mkdir(parents=True, exist_ok=True)
    cache_path = destination / 'scripts/.versacam-counts-cache.json'
    cache = json.loads(cache_path.read_text()) if cache_path.exists() else {}
    records = []
    with zipfile.ZipFile(zip_path) as archive:
        items = json.loads(archive.read('metadata.json'))['videos']
        seen = set()
        for item in items:
            case, count = item['case'], item['camera_count']
            if (not re.fullmatch(r'[a-z0-9_]+--cameras-[3-6]', case)
                    or case in seen or not case.endswith(f'--cameras-{count}')
                    or item['status'] != 'ready' or item['success'] is not True):
                raise ValueError(f'Invalid or incomplete case: {case}')
            seen.add(case)
            ready = json.loads((source / f'records/{case}/ready.json').read_text())
            master_name = f'masters/{case}.mp4'
            web_name = f'videos/{case}.mp4'
            master = source / master_name
            proof = ready['verified_media']['composite.mp4']
            if (ready['case'] != case or ready['camera_count'] != count
                    or item['master'] != master_name or item['video'] != web_name
                    or len(item['input_camera_names']) != count
                    or proof['frames'] != item['frames']
                    or (proof['width'], proof['height'], proof['fps']) != (1920, 1080, 30)):
                raise ValueError(f'Inconsistent camera-count proof: {case}')
            master_hash = sha(master)
            if (master_hash != ready['files'][master_name]['sha256']
                    or hashlib.sha256(archive.read(web_name)).hexdigest() != ready['files'][web_name]['sha256']):
                raise ValueError(f'Source integrity check failed: {case}')
            recipe = graph(count) + ';crf24;fast;poster-midpoint;v1'
            video = output / f'{case}_multiview_4x.mp4'
            poster = output / f'{case}_multiview.jpg'
            saved = cache.get(case, {})
            if not (saved.get('source_sha256') == master_hash and saved.get('recipe') == recipe
                    and video.exists() and poster.exists() and sha(video) == saved.get('video_sha256')
                    and sha(poster) == saved.get('poster_sha256')):
                print(f'Encoding {case}', flush=True)
                with tempfile.TemporaryDirectory(dir=output) as temporary:
                    temp_video = Path(temporary) / 'video.mp4'
                    temp_poster = Path(temporary) / 'poster.jpg'
                    subprocess.run(['ffmpeg', '-v', 'error', '-nostdin', '-y', '-threads', '2', '-i', str(master),
                                    '-filter_complex_threads', '1', '-filter_complex', graph(count), '-map', '[out]', '-an',
                                    '-c:v', 'libx264', '-preset', 'fast', '-crf', '24', '-threads', '2', '-pix_fmt', 'yuv420p',
                                    '-movflags', '+faststart', str(temp_video)], check=True)
                    result = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-select_streams', 'v:0',
                        '-show_entries', 'stream=width,height,avg_frame_rate,nb_frames,sample_aspect_ratio:format=duration', '-of', 'json', str(temp_video)]))
                    stream, duration = result['streams'][0], float(result['format']['duration'])
                    if ((stream['width'], stream['height'], stream['avg_frame_rate'], stream['sample_aspect_ratio']) != (1920, 1488, '30/1', '1:1')
                            or abs(duration - item['duration'] / 4) > 1/30 + .00001):
                        raise ValueError(f'Output shape/timing mismatch: {case}')
                    decoded = subprocess.check_output(['ffmpeg', '-v', 'error', '-xerror', '-threads', '2', '-i', str(temp_video),
                        '-map', '0:v:0', '-progress', 'pipe:1', '-f', 'null', '-'], text=True)
                    frames = int([line.split('=')[1] for line in decoded.splitlines() if line.startswith('frame=')][-1])
                    if frames != int(stream['nb_frames']):
                        raise ValueError(f'Decode frame mismatch: {case}')
                    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(duration/2), '-i', str(temp_video),
                        '-frames:v', '1', '-q:v', '2', '-update', '1', str(temp_poster)], check=True)
                    if sha(master) != master_hash:
                        raise ValueError(f'Source changed during encode: {case}')
                    temp_video.replace(video)
                    temp_poster.replace(poster)
                saved = {'source_sha256': master_hash, 'recipe': recipe, 'video_sha256': sha(video), 'poster_sha256': sha(poster),
                         'duration': duration, 'frames': frames, 'full_decode': 'passed'}
                cache[case] = saved
                write_json(cache_path, cache)
            records.append({'id': case, 'task': item['task'], 'task_title': item['title'], 'camera_count': count,
                            'title': f"{item['title']} · {count} cameras", 'width': 1920, 'height': 1488,
                            'duration': saved['duration'], 'playback_speed': 4,
                            'video': '/' + str(video.relative_to(destination)), 'poster': '/' + str(poster.relative_to(destination))})
    write_json(destination / '_data/versacam_counts.json', records)
    write_json(report_path, {'archive': str(zip_path), 'crop': [1024, 576, 448, 384], 'output': [1920, 1488],
                            'playback_speed': 4, 'cases': cache, 'included_count': len(records),
                            'available_tasks': sorted({x['task'] for x in records}),
                            'stackcube_available': any('stack' in x['task'] for x in records)})
    print(f'Prepared {len(records)} verified clips; tasks: {sorted({x["task"] for x in records})}')


def self_check():
    assert [layout(n) for n in (3,4,5,6)] == [(468,320,268),(302,320,268),(136,320,268),(12,306,257)]
    for n in (3,4,5,6):
        left,width,height=layout(n)
        assert left >= 0 and left+(n-1)*(width+12)+width <= 1920
        assert graph(n).count('exact=1') == n and f'split={n+1}' in graph(n)
    try: layout(7)
    except ValueError: pass
    else: raise AssertionError('Invalid camera count accepted')
    print('Camera-pane geometry checks passed for 3/4/5/6 inputs.')


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('zip', type=Path, nargs='?')
    parser.add_argument('--destination', type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument('--report', type=Path)
    parser.add_argument('--self-check', action='store_true')
    args=parser.parse_args()
    if args.self_check: self_check()
    else:
        if not args.zip or not args.report: parser.error('ZIP and --report are required')
        prepare(args.zip.resolve(), args.destination.resolve(), args.report.resolve())
