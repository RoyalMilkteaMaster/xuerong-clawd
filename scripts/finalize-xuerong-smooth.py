#!/usr/bin/env python3
"""Restore Xuerong's original pose rhythm and clean translucent edge colors."""

from __future__ import annotations

import argparse
import json
from bisect import bisect_right
from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--theme-dir", type=Path, default=Path("themes/xuerong-hd"))
    parser.add_argument("--source-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, default=Path("build/xuerong-final/assets"))
    parser.add_argument("--transition-ms", type=int, default=67)
    parser.add_argument("--transparent-threshold", type=int, default=3)
    parser.add_argument("--only", nargs="*", default=[])
    return parser.parse_args()


def decode_frames(path: Path) -> list[Image.Image]:
    image = Image.open(path)
    frames = []
    for index in range(getattr(image, "n_frames", 1)):
        image.seek(index)
        frames.append(image.convert("RGBA").copy())
    return frames


def distribute_durations(total_ms: int, count: int) -> list[int]:
    base, remainder = divmod(total_ms, count)
    return [base + (1 if index < remainder else 0) for index in range(count)]


def rhythm_time(
    time_ms: float,
    starts: list[int],
    durations: list[int],
    loop: int,
    transition_ms: int,
) -> tuple[float, int, bool]:
    index = max(0, min(len(starts) - 1, bisect_right(starts, time_ms) - 1))
    duration = durations[index]
    local = time_ms - starts[index]
    if loop != 0 and index == len(starts) - 1:
        return float(starts[index]), index, True
    transition = min(transition_ms, max(1, duration))
    hold = duration - transition
    if local <= hold:
        return float(starts[index]), index, True
    progress = min(1.0, max(0.0, (local - hold) / transition))
    return starts[index] + progress * duration, index, False


def sample_frame(frames: list[Image.Image], total_ms: int, time_ms: float) -> Image.Image:
    if len(frames) == 1 or total_ms <= 0:
        return frames[0].copy()
    position = min(1.0, max(0.0, time_ms / total_ms))
    index = min(len(frames) - 1, round(position * (len(frames) - 1)))
    return frames[index].copy()


def clean_edge_colors(frame: Image.Image, transparent_threshold: int) -> tuple[Image.Image, dict]:
    rgba = np.asarray(frame.convert("RGBA"), dtype=np.uint8).copy()
    alpha = rgba[:, :, 3]
    cleared = (alpha > 0) & (alpha <= transparent_threshold)
    alpha[cleared] = 0
    rgba[alpha == 0, :3] = 0

    edge = (alpha > 0) & (alpha < 250)
    interior = alpha >= 250
    height, width = alpha.shape
    assigned = np.zeros_like(edge, dtype=bool)
    queue: deque[tuple[int, int, int, int, int]] = deque()

    for y, x in np.argwhere(edge):
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                if not (dx or dy):
                    continue
                ny, nx = y + dy, x + dx
                if 0 <= ny < height and 0 <= nx < width and interior[ny, nx]:
                    red, green, blue = (int(value) for value in rgba[ny, nx, :3])
                    queue.append((int(y), int(x), red, green, blue))
                    assigned[y, x] = True
                    break
            if assigned[y, x]:
                break

    recolored = 0
    while queue:
        y, x, red, green, blue = queue.popleft()
        rgba[y, x, :3] = (red, green, blue)
        recolored += 1
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                if not (dx or dy):
                    continue
                ny, nx = y + dy, x + dx
                if 0 <= ny < height and 0 <= nx < width and edge[ny, nx] and not assigned[ny, nx]:
                    assigned[ny, nx] = True
                    queue.append((ny, nx, red, green, blue))

    return Image.fromarray(rgba, "RGBA"), {
        "edge_pixels": int(edge.sum()),
        "edge_pixels_recolored": recolored,
        "low_alpha_pixels_cleared": int(cleared.sum()),
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


def process_asset(args: argparse.Namespace, entry: dict) -> dict:
    name = entry["asset"]
    smooth_frames = decode_frames(args.theme_dir / "assets" / name)
    source_frames = decode_frames(args.source_dir / name)
    durations = [int(value) for value in entry["durations_ms"]]
    total_ms = sum(durations)
    starts = []
    elapsed = 0
    for duration in durations:
        starts.append(elapsed)
        elapsed += duration

    output_durations = distribute_durations(total_ms, len(smooth_frames))
    output_frames = []
    held_frames = 0
    edge_pixels = 0
    recolored = 0
    cleared = 0
    time_ms = 0.0
    for duration in output_durations:
        mapped_time, source_index, held = rhythm_time(
            time_ms, starts, durations, int(entry["loop"]), args.transition_ms
        )
        frame = source_frames[min(source_index, len(source_frames) - 1)].copy() if held else sample_frame(smooth_frames, total_ms, mapped_time)
        frame, cleanup = clean_edge_colors(frame, args.transparent_threshold)
        output_frames.append(frame)
        held_frames += int(held)
        edge_pixels += cleanup["edge_pixels"]
        recolored += cleanup["edge_pixels_recolored"]
        cleared += cleanup["low_alpha_pixels_cleared"]
        time_ms += duration

    output_path = args.output_dir / name
    encode_webp(output_path, output_frames, output_durations, int(entry["loop"]))
    return {
        "asset": name,
        "frames": len(output_frames),
        "total_duration_ms": total_ms,
        "held_frames": held_frames,
        "transition_frames": len(output_frames) - held_frames,
        "edge_pixels": edge_pixels,
        "edge_pixels_recolored": recolored,
        "low_alpha_pixels_cleared": cleared,
        "output_bytes": output_path.stat().st_size,
    }


def main() -> int:
    args = parse_args()
    manifest = json.loads((args.theme_dir / "qa" / "asset-build-v21.json").read_text(encoding="utf-8"))
    entries = manifest["assets"]
    if args.only:
        requested = {name if name.endswith(".webp") else f"{name}.webp" for name in args.only}
        entries = [entry for entry in entries if entry["asset"] in requested]
    args.output_dir.mkdir(parents=True, exist_ok=True)
    reports = []
    for index, entry in enumerate(entries, start=1):
        print(f"[{index}/{len(entries)}] {entry['asset']}", flush=True)
        reports.append(process_asset(args, entry))
    report = {
        "ok": True,
        "transition_ms": args.transition_ms,
        "transparent_threshold": args.transparent_threshold,
        "assets": reports,
    }
    report_path = args.output_dir.parent / "finalize-report.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(report_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
