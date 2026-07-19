#!/usr/bin/env python3
"""Build 30 FPS Xuerong animated WebP assets with RIFE interpolation."""

from __future__ import annotations

import argparse
import json
import math
import shutil
import subprocess
import sys
from bisect import bisect_right
from pathlib import Path

import numpy as np
from PIL import Image


UPRIGHT_ASSETS = {
    "dozing.webp",
    "idle.webp",
    "review.webp",
    "typing.webp",
    "waiting.webp",
    "waving.webp",
    "yawning.webp",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--theme-dir", type=Path, default=Path("themes/xuerong-hd"))
    parser.add_argument("--rife", type=Path, required=True)
    parser.add_argument("--model", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, default=Path("build/xuerong-smooth/assets"))
    parser.add_argument("--work-dir", type=Path, default=Path("build/xuerong-smooth/work"))
    parser.add_argument("--fps", type=int, default=30)
    parser.add_argument("--base-fps", type=int, default=15)
    parser.add_argument("--gpu", type=int, default=0)
    parser.add_argument("--only", nargs="*", default=[])
    parser.add_argument("--keep-work", action="store_true")
    return parser.parse_args()


def load_build_manifest(theme_dir: Path) -> list[dict]:
    path = theme_dir / "qa" / "asset-build-v21.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    return data["assets"]


def decode_rgba_frames(path: Path) -> list[Image.Image]:
    image = Image.open(path)
    frames = []
    for index in range(getattr(image, "n_frames", 1)):
        image.seek(index)
        frames.append(image.convert("RGBA").copy())
    return frames


def frame_at_time(frames: list[Image.Image], durations: list[int], time_ms: float) -> Image.Image:
    starts = []
    elapsed = 0
    for duration in durations:
        starts.append(elapsed)
        elapsed += duration
    if time_ms >= elapsed:
        return frames[-1]
    index = max(0, min(len(frames) - 1, bisect_right(starts, time_ms) - 1))
    return frames[index]


def sample_base_frames(
    frames: list[Image.Image], durations: list[int], loop: int, base_fps: int
) -> list[Image.Image]:
    total_ms = sum(durations)
    if loop == 0:
        unique_count = max(len(frames), math.ceil(total_ms * base_fps / 1000))
        sampled = [
            frame_at_time(frames, durations, index * total_ms / unique_count).copy()
            for index in range(unique_count)
        ]
        sampled.append(frames[0].copy())
        return sampled

    count = max(len(frames), math.ceil(total_ms * base_fps / 1000) + 1)
    return [
        frame_at_time(frames, durations, index * total_ms / (count - 1)).copy()
        for index in range(count)
    ]


def save_rife_channels(frames: list[Image.Image], rgb_dir: Path, alpha_dir: Path) -> None:
    rgb_dir.mkdir(parents=True, exist_ok=True)
    alpha_dir.mkdir(parents=True, exist_ok=True)
    for index, frame in enumerate(frames):
        alpha = frame.getchannel("A")
        rgb = frame.convert("RGB")
        black = Image.new("RGB", frame.size, "black")
        premultiplied = Image.composite(rgb, black, alpha)
        name = f"{index:08d}.png"
        premultiplied.save(rgb_dir / name)
        Image.merge("RGB", (alpha, alpha, alpha)).save(alpha_dir / name)


def run_rife(
    executable: Path,
    model: Path,
    input_dir: Path,
    output_dir: Path,
    frame_count: int,
    gpu: int,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    command = [
        str(executable),
        "-i", str(input_dir),
        "-o", str(output_dir),
        "-n", str(frame_count),
        "-m", str(model),
        "-g", str(gpu),
        "-j", "2:2:2",
    ]
    subprocess.run(command, check=True)


def unpremultiply(premultiplied: Image.Image, alpha_image: Image.Image) -> Image.Image:
    premultiplied_array = np.asarray(premultiplied.convert("RGB"), dtype=np.float32)
    alpha_array = np.asarray(alpha_image.convert("L"), dtype=np.uint8).copy()
    alpha_array[alpha_array <= 2] = 0
    alpha_array[alpha_array >= 253] = 255

    safe_alpha = np.maximum(alpha_array, 1).astype(np.float32)[..., None]
    rgb_array = np.clip(
        np.rint(premultiplied_array * 255.0 / safe_alpha), 0, 255
    ).astype(np.uint8)
    rgb_array[alpha_array == 0] = 0
    rgba_array = np.dstack((rgb_array, alpha_array))
    return Image.fromarray(rgba_array, "RGBA")


def load_rife_frames(rgb_dir: Path, alpha_dir: Path) -> list[Image.Image]:
    rgb_paths = sorted(rgb_dir.glob("*.png"))
    alpha_paths = sorted(alpha_dir.glob("*.png"))
    if not rgb_paths or len(rgb_paths) != len(alpha_paths):
        raise RuntimeError("RIFE RGB and alpha output counts do not match")
    return [
        unpremultiply(Image.open(rgb_path), Image.open(alpha_path))
        for rgb_path, alpha_path in zip(rgb_paths, alpha_paths)
    ]


def distribute_durations(total_ms: int, count: int) -> list[int]:
    base, remainder = divmod(total_ms, count)
    return [base + (1 if index < remainder else 0) for index in range(count)]


def alpha_bbox(frame: Image.Image, threshold: int = 16) -> tuple[int, int, int, int] | None:
    alpha = frame.getchannel("A").point(lambda value: 255 if value >= threshold else 0)
    return alpha.getbbox()


def frame_metrics(frame: Image.Image) -> dict:
    bbox = alpha_bbox(frame)
    if not bbox:
        return {"bbox": None, "width": 0, "height": 0, "center_x": None, "bottom": None}
    left, top, right, bottom = bbox
    return {
        "bbox": list(bbox),
        "width": right - left,
        "height": bottom - top,
        "center_x": (left + right) / 2,
        "bottom": bottom,
    }


def validate_asset(
    name: str,
    source_frames: list[Image.Image],
    output_frames: list[Image.Image],
    idle_height: float,
) -> dict:
    source_metrics = [frame_metrics(frame) for frame in source_frames]
    output_metrics = [frame_metrics(frame) for frame in output_frames]
    source_heights = [metric["height"] for metric in source_metrics if metric["height"]]
    output_heights = [metric["height"] for metric in output_metrics if metric["height"]]
    source_bottoms = [metric["bottom"] for metric in source_metrics if metric["bottom"] is not None]
    output_bottoms = [metric["bottom"] for metric in output_metrics if metric["bottom"] is not None]
    warnings = []

    tolerance = max(5, round(idle_height * 0.04))
    if output_heights and (
        min(output_heights) < min(source_heights) - tolerance
        or max(output_heights) > max(source_heights) + tolerance
    ):
        warnings.append("interpolated height exceeds the source motion envelope")
    if output_bottoms and (
        min(output_bottoms) < min(source_bottoms) - tolerance
        or max(output_bottoms) > max(source_bottoms) + tolerance
    ):
        warnings.append("interpolated baseline exceeds the source motion envelope")

    upright_ratio = None
    if name in UPRIGHT_ASSETS and output_heights:
        upright_ratio = sorted(output_heights)[len(output_heights) // 2] / idle_height
        if not 0.92 <= upright_ratio <= 1.08:
            warnings.append("upright character scale differs from idle by more than 8%")

    return {
        "warnings": warnings,
        "source_height_range": [min(source_heights), max(source_heights)],
        "output_height_range": [min(output_heights), max(output_heights)],
        "source_bottom_range": [min(source_bottoms), max(source_bottoms)],
        "output_bottom_range": [min(output_bottoms), max(output_bottoms)],
        "upright_idle_height_ratio": upright_ratio,
    }


def encode_webp(path: Path, frames: list[Image.Image], durations: list[int], loop: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    frames[0].save(
        path,
        format="WEBP",
        save_all=True,
        append_images=frames[1:],
        duration=durations,
        loop=loop,
        lossless=True,
        quality=100,
        method=4,
    )


def build_asset(args: argparse.Namespace, entry: dict, idle_height: float) -> dict:
    name = entry["asset"]
    source_path = args.theme_dir / "assets" / name
    source_frames = decode_rgba_frames(source_path)
    durations = [int(value) for value in entry["durations_ms"]]
    total_ms = sum(durations)
    target_count = max(len(source_frames), round(total_ms * args.fps / 1000))
    work = args.work_dir / source_path.stem
    if work.exists():
        shutil.rmtree(work)
    rgb_input = work / "rgb-input"
    alpha_input = work / "alpha-input"
    rgb_output = work / "rgb-output"
    alpha_output = work / "alpha-output"

    base_frames = sample_base_frames(source_frames, durations, int(entry["loop"]), args.base_fps)
    save_rife_channels(base_frames, rgb_input, alpha_input)
    run_rife(args.rife, args.model, rgb_input, rgb_output, target_count, args.gpu)
    run_rife(args.rife, args.model, alpha_input, alpha_output, target_count, args.gpu)
    output_frames = load_rife_frames(rgb_output, alpha_output)

    output_frames[0] = source_frames[0].copy()
    output_frames[-1] = (source_frames[0] if int(entry["loop"]) == 0 else source_frames[-1]).copy()
    output_durations = distribute_durations(total_ms, len(output_frames))
    output_path = args.output_dir / name
    encode_webp(output_path, output_frames, output_durations, int(entry["loop"]))

    validation = validate_asset(name, source_frames, output_frames, idle_height)
    if not args.keep_work:
        shutil.rmtree(work)
    return {
        "asset": name,
        "source_frames": len(source_frames),
        "output_frames": len(output_frames),
        "total_duration_ms": total_ms,
        "effective_fps": round(len(output_frames) * 1000 / total_ms, 3),
        "durations_ms": output_durations,
        "source_bytes": source_path.stat().st_size,
        "output_bytes": output_path.stat().st_size,
        **validation,
    }


def main() -> int:
    args = parse_args()
    args.theme_dir = args.theme_dir.resolve()
    args.rife = args.rife.resolve()
    args.model = args.model.resolve()
    args.output_dir = args.output_dir.resolve()
    args.work_dir = args.work_dir.resolve()
    if not args.rife.is_file() or not args.model.is_dir():
        raise SystemExit("RIFE executable or model directory does not exist")

    entries = load_build_manifest(args.theme_dir)
    if args.only:
        requested = {name if name.endswith(".webp") else f"{name}.webp" for name in args.only}
        entries = [entry for entry in entries if entry["asset"] in requested]
        missing = requested - {entry["asset"] for entry in entries}
        if missing:
            raise SystemExit(f"Unknown assets: {sorted(missing)}")

    idle_frames = decode_rgba_frames(args.theme_dir / "assets" / "idle.webp")
    idle_heights = [frame_metrics(frame)["height"] for frame in idle_frames]
    idle_height = sorted(idle_heights)[len(idle_heights) // 2]
    args.output_dir.mkdir(parents=True, exist_ok=True)
    reports = []
    for index, entry in enumerate(entries, start=1):
        print(f"[{index}/{len(entries)}] {entry['asset']}", flush=True)
        reports.append(build_asset(args, entry, idle_height))

    report = {
        "ok": not any(item["warnings"] for item in reports),
        "fps": args.fps,
        "base_fps": args.base_fps,
        "idle_reference_height": idle_height,
        "model": args.model.name,
        "assets": reports,
    }
    report_path = args.output_dir.parent / "smooth-build-report.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(report_path)
    return 0 if report["ok"] else 2


if __name__ == "__main__":
    sys.exit(main())
