#!/usr/bin/env python3
"""Scale Xuerong's curled sleep pose while preserving its baseline and timing."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image


SLEEP_ASSETS = ("sleeping.webp", "collapsing.webp", "waking.webp")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--asset-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--sleep-scale", type=float, default=1.08)
    parser.add_argument("--standing-height", type=float, default=350.0)
    parser.add_argument("--sleep-height", type=float, default=175.0)
    return parser.parse_args()


def decode(path: Path) -> tuple[list[Image.Image], list[int], int]:
    image = Image.open(path)
    frames: list[Image.Image] = []
    durations: list[int] = []
    loop = int(image.info.get("loop", 0))
    for index in range(image.n_frames):
        image.seek(index)
        frames.append(image.convert("RGBA").copy())
        durations.append(int(image.info.get("duration", 0)))
    if not frames or any(duration <= 0 for duration in durations):
        raise ValueError(f"Missing frames or durations: {path}")
    return frames, durations, loop


def pose_scale(name: str, height: int, args: argparse.Namespace) -> float:
    if name == "sleeping.webp":
        return args.sleep_scale
    denominator = args.standing_height - args.sleep_height
    progress = (args.standing_height - height) / denominator
    progress = max(0.0, min(1.0, progress))
    return 1.0 + (args.sleep_scale - 1.0) * progress


def scale_about_baseline(frame: Image.Image, scale: float) -> Image.Image:
    box = frame.getchannel("A").getbbox()
    if not box or abs(scale - 1.0) < 0.0001:
        return frame.copy()
    crop = frame.crop(box).convert("RGBa")
    width = max(1, round(crop.width * scale))
    height = max(1, round(crop.height * scale))
    resized = crop.resize((width, height), Image.Resampling.LANCZOS).convert("RGBA")
    center_x = (box[0] + box[2]) / 2
    x = round(center_x - width / 2)
    y = box[3] - height
    output = Image.new("RGBA", frame.size, (0, 0, 0, 0))
    output.alpha_composite(resized, (x, y))
    return output


def encode(path: Path, frames: list[Image.Image], durations: list[int], loop: int) -> None:
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


def read_webp_timing(path: Path) -> tuple[int, int, int]:
    data = path.read_bytes()
    position = 12
    frame_count = 0
    total_duration = 0
    loop = 0
    while position + 8 <= len(data):
        tag = data[position:position + 4]
        size = int.from_bytes(data[position + 4:position + 8], "little")
        payload = data[position + 8:position + 8 + size]
        if tag == b"ANIM" and len(payload) >= 6:
            loop = int.from_bytes(payload[4:6], "little")
        elif tag == b"ANMF" and len(payload) >= 15:
            frame_count += 1
            total_duration += int.from_bytes(payload[12:15], "little")
        position += 8 + size + (size & 1)
    return frame_count, total_duration, loop


def main() -> int:
    args = parse_args()
    reports = []
    for name in SLEEP_ASSETS:
        frames, durations, loop = decode(args.asset_dir / name)
        output_frames = []
        scales = []
        for frame in frames:
            box = frame.getchannel("A").getbbox()
            height = 0 if not box else box[3] - box[1]
            scale = pose_scale(name, height, args)
            output_frames.append(scale_about_baseline(frame, scale))
            scales.append(scale)
        output = args.output_dir / name
        encode(output, output_frames, durations, loop)
        output_count, output_duration, output_loop = read_webp_timing(output)
        if (output_count, output_duration, output_loop) != (len(frames), sum(durations), loop):
            raise ValueError(f"Timing changed while scaling {name}")
        boxes = [frame.getchannel("A").getbbox() for frame in output_frames]
        visible_boxes = [box for box in boxes if box]
        reports.append(
            {
                "asset": name,
                "frames": len(frames),
                "duration_ms": sum(durations),
                "scale_range": [round(min(scales), 4), round(max(scales), 4)],
                "height_range": [
                    min(box[3] - box[1] for box in visible_boxes),
                    max(box[3] - box[1] for box in visible_boxes),
                ],
                "bottom_range": [
                    min(box[3] - 1 for box in visible_boxes),
                    max(box[3] - 1 for box in visible_boxes),
                ],
            }
        )
    report_path = args.output_dir.parent / "sleep-scale-report.json"
    report_path.write_text(
        json.dumps({"ok": True, "sleep_scale": args.sleep_scale, "assets": reports}, indent=2),
        encoding="utf-8",
    )
    print(report_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
