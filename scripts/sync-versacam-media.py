#!/usr/bin/env python3
"""Import verified demonstrations; compose cropped RoboTwin multiview videos at 4x.

python3 scripts/sync-versacam-media.py --real-dir PATH --simulation-dir PATH
Only completed successful simulations are published; rerun as more finish.
Run --self-check for a small check of path, status, and hash validation.
"""

import argparse
import hashlib
import json
import math
from pathlib import Path
import re
import shutil
import subprocess
import tempfile


MEDIA = "VersaCamVLA.github.io/media"
EXCLUDED_SIM_TASKS = {"place_a2b_right", "place_dual_shoes"}
OUTPUT_SIZE = (1920, 1488)
VIDEO_FILTER = (
    "[0:v]setpts=(PTS-STARTPTS)/4,fps=30,split=5[h][l][r][a][o];"
    "[h]crop=320:268:302:12,scale=480:402:flags=lanczos[head];"
    "[l]crop=320:268:634:12,scale=480:402:flags=lanczos[left];"
    "[r]crop=320:268:966:12,scale=480:402:flags=lanczos[right];"
    "[a]crop=320:268:1298:12,scale=480:402:flags=lanczos[agent];"
    "[head][left][right][agent]hstack=inputs=4,pad=1920:408:0:0:color=white[top];"
    "[o]crop=1024:576:448:384,scale=1920:1080:flags=lanczos[observer];"
    "[top][observer]vstack=inputs=2,setsar=1[out]"
)
RECIPE = f"{VIDEO_FILTER};libx264;crf24;fast;yuv420p;silent;faststart;poster-midpoint-q2;decoded-frame-count;v4"
REAL_TASKS = (
    ("pickcube", "Pick Cube", "Move a cube to the center, then place it in the bowl."),
    ("stackcube", "Stack Cubes", "Build a three-cube tower through coordinated bimanual actions."),
    ("inserttube", "Insert Tube", "Hand over a test tube, then align it with the rack."),
)


def inside(root, relative):
    if not isinstance(relative, str) or Path(relative).is_absolute():
        raise ValueError(f"Expected a relative path: {relative!r}")
    path = (root / relative).resolve()
    if not path.is_relative_to(root):
        raise ValueError(f"Path leaves its source or destination directory: {relative}")
    return path


def read_json(root, relative):
    return json.loads(inside(root, relative).read_text(encoding="utf-8"))


def fingerprint(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    size = path.stat().st_size
    if not size:
        raise ValueError(f"Empty media file: {path.name}")
    return {"bytes": size, "sha256": digest.hexdigest()}


def collect_real(root):
    report = read_json(root, "verification/report.json")
    if (report.get("full_decode_check") != "passed_for_all_six_files"
            or report.get("resolution") != "1920x1080"
            or report.get("speed") != 4 or report.get("fps") != 30):
        raise ValueError("Real videos need the verified 1080p, 30 fps, 4x report")
    verified = {entry["name"]: entry for entry in report["files"]}
    tasks, copies = [], []
    for task, title, description in REAL_TASKS:
        item = {"id": task, "title": title, "description": description}
        for view in ("front", "back"):
            name = f"{task}_{view}"
            clip = verified[name]
            video = f"{name}_4x_1080p.mp4"
            if (clip["output"] != video or clip["output_resolution"] != [1920, 1080]
                    or clip["fps"] != "30/1" or clip["codec"] != "h264"):
                raise ValueError(f"Unexpected real-video verification: {name}")
            item[view] = {}
            for field, source in (("video", video), ("poster", f"verification/{name}.jpg")):
                path = inside(root, source)
                check = fingerprint(path)
                if field == "video" and check["bytes"] != clip["bytes"]:
                    raise ValueError(f"Real video differs from its verification: {name}")
                target = f"{MEDIA}/real/{path.name}"
                copies.append((path, target, check))
                item[view][field] = "/" + target
        tasks.append(item)
    return tasks, copies


def collect_simulation(root):
    entries = read_json(root, "metadata.json")["videos"]
    if not isinstance(entries, list):
        raise ValueError("Simulation metadata must contain a videos list")
    tasks, copies, seen = [], [], set()
    for entry in entries:
        task = entry["task"]
        if not isinstance(task, str) or not re.fullmatch(r"[a-z0-9_]+", task) or task in seen:
            raise ValueError(f"Invalid or duplicate simulation task: {task!r}")
        seen.add(task)
        if task in EXCLUDED_SIM_TASKS or entry.get("status") != "ready" or entry.get("success") is not True:
            continue
        marker = f"records/{task}/ready.json"
        if not inside(root, marker).is_file():
            continue
        ready = read_json(root, marker)
        if ready.get("task") != task or ready.get("seed") != entry.get("seed"):
            raise ValueError(f"Simulation verification does not match metadata: {task}")
        composite = ready["verified_media"]["composite.mp4"]
        duration = entry["duration"]
        if (isinstance(duration, bool) or not isinstance(duration, (int, float))
                or not math.isfinite(duration) or duration <= 0
                or not math.isclose(duration, composite["duration"], abs_tol=0.01)
                or (composite["width"], composite["height"], composite["fps"]) != (1920, 1080, 30)
                or composite["frames"] != entry["frames"] or entry["fps"] != 30):
            raise ValueError(f"Inconsistent simulation media verification: {task}")
        title = entry["title"]
        if not isinstance(title, str) or not title.strip():
            raise ValueError(f"Missing simulation title: {task}")
        expected = f"masters/{task}.mp4"
        if entry["master"] != expected:
            raise ValueError(f"Unexpected simulation master path: {task}")
        source = inside(root, expected)
        check = fingerprint(source)
        if check != ready["files"][expected]:
            raise ValueError(f"Simulation master fails its size/hash check: {task}")
        target = f"{MEDIA}/simulation/{task}_multiview_crop_4x.mp4"
        item = {"id": task, "title": title, "duration": duration, "playback_speed": 4,
                "view": "multiview", "width": OUTPUT_SIZE[0], "height": OUTPUT_SIZE[1],
                "video": "/" + target, "poster": f"/{MEDIA}/simulation/{task}_multiview_crop.jpg"}
        copies.append((source, target, check))
        tasks.append(item)
    return tasks, copies


def copy_changed(source, target, expected):
    if target.is_file() and target.stat().st_size and fingerprint(target) == expected:
        return 0
    target.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=target.parent, delete=False) as stream:
        temporary = Path(stream.name)
    try:
        shutil.copyfile(source, temporary)
        if fingerprint(temporary) != expected:
            raise ValueError(f"Source changed during import: {source.name}; rerun the importer")
        temporary.replace(target)
    finally:
        temporary.unlink(missing_ok=True)
    return 1


def encode_simulation(source, target, poster, expected, original_duration, cached):
    if (cached.get("source") == expected and cached.get("recipe") == RECIPE
            and target.is_file() and target.stat().st_size
            and fingerprint(target) == cached.get("output")
            and poster.is_file() and poster.stat().st_size
            and fingerprint(poster) == cached.get("poster")):
        return cached, 0
    target.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(suffix=".mp4", dir=target.parent, delete=False) as stream:
        temporary = Path(stream.name)
    with tempfile.NamedTemporaryFile(suffix=".jpg", dir=poster.parent, delete=False) as stream:
        poster_temporary = Path(stream.name)
    print(f"Composing and checking {source.stem} multiview at 4x...", flush=True)
    try:
        subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(source),
                        "-filter_complex", VIDEO_FILTER, "-map", "[out]", "-an",
                        "-c:v", "libx264", "-preset", "fast", "-crf", "24", "-threads", "2",
                        "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(temporary)], check=True)
        result = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0",
                                 "-show_entries", "stream=codec_name,width,height,avg_frame_rate,pix_fmt,nb_frames:format=duration",
                                 "-of", "json", str(temporary)], check=True, capture_output=True, text=True)
        probe = json.loads(result.stdout)
        video, duration = probe["streams"][0], float(probe["format"]["duration"])
        if ((video["width"], video["height"], video["avg_frame_rate"], video["codec_name"], video["pix_fmt"])
                != (*OUTPUT_SIZE, "30/1", "h264", "yuv420p")
                or abs(duration - original_duration / 4) > 1 / 30 + 0.00001):
            raise ValueError(f"4x encode failed resolution/frame-rate/duration checks: {source.name}")
        decoded = subprocess.run(["ffmpeg", "-v", "error", "-xerror", "-threads", "2", "-i", str(temporary),
                                  "-map", "0:v:0", "-progress", "pipe:1", "-f", "null", "-"],
                                 check=True, capture_output=True, text=True)
        frames = int([line.split("=", 1)[1] for line in decoded.stdout.splitlines() if line.startswith("frame=")][-1])
        if frames != int(video["nb_frames"]):
            raise ValueError(f"Decoded frame count differs from encoded frame count: {source.name}")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(duration / 2), "-i", str(temporary),
                        "-frames:v", "1", "-q:v", "2", "-update", "1", str(poster_temporary)], check=True)
        if fingerprint(source) != expected:
            raise ValueError(f"Source changed during encoding: {source.name}; rerun the importer")
        result = {"source": expected, "output": fingerprint(temporary), "poster": fingerprint(poster_temporary),
                  "recipe": RECIPE, "duration": duration, "decoded_frames": frames}
        temporary.replace(target)
        poster_temporary.replace(poster)
        return result, 2
    finally:
        temporary.unlink(missing_ok=True)
        poster_temporary.unlink(missing_ok=True)


def write_changed(path, data):
    content = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
    if path.is_file() and path.read_text(encoding="utf-8") == content:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent, delete=False) as stream:
        temporary = Path(stream.name)
        stream.write(content)
    temporary.replace(path)


def import_media(real_root, simulation_root, destination):
    real, real_copies = collect_real(real_root.resolve())
    simulation, sim_copies = collect_simulation(simulation_root.resolve())
    destination = destination.resolve()
    copies = real_copies + sim_copies
    targets = [(source, inside(destination, relative), check) for source, relative, check in copies]
    manifests = [(inside(destination, "_data/versacam_real.json"), real),
                 (inside(destination, "_data/versacam_sim.json"), simulation)]
    cache_path = inside(destination, "scripts/.versacam-media-cache.json")
    cache = json.loads(cache_path.read_text()) if cache_path.is_file() else {}
    sim_tasks = {item["id"]: item for item in simulation}
    changed = 0
    for source, target, check in targets:
        if target.parent.name == "simulation" and source.suffix == ".mp4":
            task = sim_tasks[source.stem]
            key = target.name
            poster = inside(destination, task["poster"].lstrip("/"))
            cache[key], count = encode_simulation(source, target, poster, check, task["duration"], cache.get(key, {}))
            task["duration"] = cache[key]["duration"]
            write_changed(cache_path, cache)
            changed += count
        else:
            changed += copy_changed(source, target, check)
    for path, data in manifests:
        write_changed(path, data)
    sizes = [(target.stat().st_size, target.name) for _, target, _ in targets]
    sizes.extend((inside(destination, item["poster"].lstrip("/")).stat().st_size,
                  Path(item["poster"]).name) for item in simulation)
    largest, name = max(sizes)
    total = sum(size for size, _ in sizes)
    print(f"Imported 6 real videos and {len(simulation)} verified 4x simulations; {changed} media files changed.")
    print(f"Referenced media: {total / 1_000_000:.2f} MB; largest: {name} ({largest / 1_000_000:.2f} MB).")


def self_check():
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory).resolve()
        (root / "masters").mkdir()
        (root / "records/demo").mkdir(parents=True)
        (root / "masters/demo.mp4").write_bytes(b"sample composite master")
        entry = {"task": "demo", "title": "Demo", "status": "ready", "success": True,
                 "seed": 1, "duration": 2, "frames": 60, "fps": 30,
                 "master": "masters/demo.mp4"}
        excluded = [dict(entry, task=task, master=f"masters/{task}.mp4") for task in EXCLUDED_SIM_TASKS]
        write_changed(root / "metadata.json", {"videos": [entry, {"task": "pending", "status": "running"}] + excluded})
        ready = {"task": "demo", "seed": 1, "verified_media": {"composite.mp4": {
            "duration": 2, "frames": 60, "fps": 30, "width": 1920, "height": 1080}},
            "files": {entry["master"]: fingerprint(root / entry["master"])}}
        write_changed(root / "records/demo/ready.json", ready)
        for item in excluded:
            (root / item["master"]).write_bytes(b"sample composite master")
            excluded_ready = dict(ready, task=item["task"], files={item["master"]: fingerprint(root / item["master"])})
            write_changed(root / f"records/{item['task']}/ready.json", excluded_ready)
        tasks, copies = collect_simulation(root)
        assert len(tasks) == 1 and tasks[0]["id"] == "demo" and len(copies) == 1
        assert tasks[0]["view"] == "multiview" and tasks[0]["playback_speed"] == 4
        assert (tasks[0]["width"], tasks[0]["height"]) == (1920, 1488)
        assert tasks[0]["video"].endswith("demo_multiview_crop_4x.mp4")
        assert tasks[0]["poster"].endswith("demo_multiview_crop.jpg")
        source, _, check = copies[0]
        target = root / "copy.mp4"
        assert copy_changed(source, target, check) == 1
        assert copy_changed(source, target, check) == 0
        poster = root / "poster.jpg"
        poster.write_bytes(b"cropped multiview poster")
        cached = {"source": check, "output": check, "poster": fingerprint(poster), "recipe": RECIPE, "duration": 0.5}
        assert encode_simulation(source, target, poster, check, 2, cached) == (cached, 0)
        (root / "escape").symlink_to(root.parent, target_is_directory=True)
        for relative in ("../outside", "/absolute", "escape/outside"):
            try:
                inside(root, relative)
            except ValueError:
                pass
            else:
                raise AssertionError(f"Unsafe path accepted: {relative}")
        source.write_bytes(b"modified video")
        try:
            collect_simulation(root)
        except ValueError:
            pass
        else:
            raise AssertionError("Changed video accepted")
        entry["success"] = False
        write_changed(root / "metadata.json", {"videos": [entry]})
        assert collect_simulation(root) == ([], [])
    print("Self-check passed: incomplete/failed jobs skipped; paths, hashes, and unchanged copies checked.")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--real-dir", type=Path)
    parser.add_argument("--simulation-dir", type=Path)
    parser.add_argument("--destination", type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument("--self-check", action="store_true")
    args = parser.parse_args()
    if args.self_check:
        self_check()
        return
    if not args.real_dir or not args.simulation_dir:
        parser.error("--real-dir and --simulation-dir are required")
    try:
        import_media(args.real_dir, args.simulation_dir, args.destination)
    except (OSError, ValueError, KeyError, TypeError, subprocess.CalledProcessError) as error:
        parser.exit(1, f"Media import stopped: {error}\n")


if __name__ == "__main__":
    main()
