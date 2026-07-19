#!/usr/bin/env python3
"""Extract, register, interpolate, and encode Xuerong's upright menu twirl."""

from __future__ import annotations

import argparse
import shutil
import subprocess
from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--strip", type=Path, required=True)
    parser.add_argument("--ffmpeg", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--work-dir", type=Path, default=Path("build/xuerong-twirl/work"))
    parser.add_argument("--duration-ms", type=int, default=1100)
    parser.add_argument("--target-height", type=int, default=349)
    parser.add_argument("--baseline", type=int, default=487)
    parser.add_argument("--loop", type=int, default=0)
    parser.add_argument("--clean-keyframes", action="store_true")
    return parser.parse_args()


def component_boxes(image: Image.Image) -> list[tuple[int, int, int, int]]:
    alpha = np.asarray(image.getchannel("A"), dtype=np.uint8)
    mask = alpha > 16
    height, width = mask.shape
    seen = np.zeros_like(mask, dtype=bool)
    boxes = []
    for y, x in np.argwhere(mask):
        if seen[y, x]:
            continue
        queue = deque([(int(y), int(x))])
        seen[y, x] = True
        points = []
        while queue:
            cy, cx = queue.popleft()
            points.append((cy, cx))
            for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                ny, nx = cy + dy, cx + dx
                if 0 <= ny < height and 0 <= nx < width and mask[ny, nx] and not seen[ny, nx]:
                    seen[ny, nx] = True
                    queue.append((ny, nx))
        if len(points) < 20:
            continue
        ys, xs = zip(*points)
        boxes.append((len(points), (min(xs), min(ys), max(xs) + 1, max(ys) + 1)))
    if len(boxes) < 8:
        raise RuntimeError(f"Expected at least 8 separated pose components, found {len(boxes)}")
    boxes.sort(reverse=True)
    poses = [box for _, box in boxes[:8]]
    for _, effect in boxes[8:]:
        effect_center = (effect[0] + effect[2]) / 2
        pose_index = min(
            range(8),
            key=lambda index: abs((poses[index][0] + poses[index][2]) / 2 - effect_center),
        )
        left, top, right, bottom = poses[pose_index]
        poses[pose_index] = (
            min(left, effect[0]), min(top, effect[1]),
            max(right, effect[2]), max(bottom, effect[3]),
        )
    poses.sort(key=lambda box: box[0])
    return poses


def register_frames(strip: Image.Image, boxes: list[tuple[int, int, int, int]], target_height: int, baseline: int) -> list[Image.Image]:
    heights = [bottom - top for _, top, _, bottom in boxes]
    scale = target_height / sorted(heights)[len(heights) // 2]
    frames = []
    for box in boxes:
        crop = strip.crop(box)
        size = (max(1, round(crop.width * scale)), max(1, round(crop.height * scale)))
        crop = crop.resize(size, Image.Resampling.LANCZOS)
        frame = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
        x = round((512 - crop.width) / 2)
        y = baseline - crop.height
        frame.alpha_composite(crop, (x, y))
        frames.append(frame)
    return frames


def save_channels(frames: list[Image.Image], rgb_dir: Path, alpha_dir: Path, loop: int) -> None:
    rgb_dir.mkdir(parents=True, exist_ok=True)
    alpha_dir.mkdir(parents=True, exist_ok=True)
    closing_frame = frames[0] if loop == 0 else frames[-1]
    for index, frame in enumerate([*frames, closing_frame]):
        alpha = frame.getchannel("A")
        premultiplied = Image.composite(frame.convert("RGB"), Image.new("RGB", frame.size, "black"), alpha)
        name = f"{index:02d}.png"
        premultiplied.save(rgb_dir / name)
        Image.merge("RGB", (alpha, alpha, alpha)).save(alpha_dir / name)


def interpolate(ffmpeg: Path, input_dir: Path, output_dir: Path, source_fps: float, frame_count: int) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    command = [
        str(ffmpeg), "-hide_banner", "-loglevel", "error", "-y",
        "-framerate", f"{source_fps:.9f}", "-i", str(input_dir / "%02d.png"),
        "-vf", "minterpolate=fps=30:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1",
        "-frames:v", str(frame_count), str(output_dir / "%03d.png"),
    ]
    subprocess.run(command, check=True)


def unpremultiply(rgb: Image.Image, alpha_image: Image.Image) -> Image.Image:
    premultiplied = np.asarray(rgb.convert("RGB"), dtype=np.float32)
    alpha = np.asarray(alpha_image.convert("L"), dtype=np.uint8).copy()
    alpha[alpha <= 3] = 0
    alpha[alpha >= 252] = 255
    safe = np.maximum(alpha, 1).astype(np.float32)[..., None]
    colors = np.clip(np.rint(premultiplied * 255.0 / safe), 0, 255).astype(np.uint8)
    colors[alpha == 0] = 0
    return Image.fromarray(np.dstack((colors, alpha)), "RGBA")


def distribute_durations(total_ms: int, count: int) -> list[int]:
    base, remainder = divmod(total_ms, count)
    return [base + (1 if index < remainder else 0) for index in range(count)]


def make_contact_sheet(frames: list[Image.Image], path: Path) -> None:
    chosen = [frames[round(index * (len(frames) - 1) / 7)] for index in range(8)]
    sheet = Image.new("RGB", (8 * 180, 210), (8, 12, 20))
    draw = ImageDraw.Draw(sheet)
    for index, frame in enumerate(chosen):
        preview = frame.copy()
        preview.thumbnail((170, 180), Image.Resampling.LANCZOS)
        tile = Image.new("RGBA", (180, 180), (210, 0, 120, 255))
        tile.alpha_composite(preview, ((180 - preview.width) // 2, (180 - preview.height) // 2))
        sheet.paste(tile.convert("RGB"), (index * 180, 24))
        draw.text((index * 180 + 6, 5), str(index + 1), fill=(255, 255, 255))
    path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(path)


def main() -> int:
    args = parse_args()
    if args.work_dir.exists():
        shutil.rmtree(args.work_dir)
    strip = Image.open(args.strip).convert("RGBA")
    keyframes = register_frames(strip, component_boxes(strip), args.target_height, args.baseline)
    frame_count = round(args.duration_ms * 30 / 1000)
    if args.clean_keyframes:
        frames = []
        for index in range(frame_count):
            phase = index * 8 / frame_count
            keyframe_index = min(7, int(phase))
            frames.append(keyframes[keyframe_index].copy())
    else:
        save_channels(keyframes, args.work_dir / "rgb-in", args.work_dir / "alpha-in", args.loop)
        source_fps = 8 * 1000 / args.duration_ms
        interpolate(args.ffmpeg, args.work_dir / "rgb-in", args.work_dir / "rgb-out", source_fps, frame_count)
        interpolate(args.ffmpeg, args.work_dir / "alpha-in", args.work_dir / "alpha-out", source_fps, frame_count)
        rgb_paths = sorted((args.work_dir / "rgb-out").glob("*.png"))
        alpha_paths = sorted((args.work_dir / "alpha-out").glob("*.png"))
        frames = [unpremultiply(Image.open(rgb), Image.open(alpha)) for rgb, alpha in zip(rgb_paths, alpha_paths)]
        if len(frames) != frame_count:
            frames = [
                frames[round(index * (len(frames) - 1) / (frame_count - 1))].copy()
                for index in range(frame_count)
            ]
    frames[0] = keyframes[0]
    frames[-1] = keyframes[0] if args.loop == 0 else keyframes[-1]
    durations = distribute_durations(args.duration_ms, len(frames))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    frames[0].save(
        args.output,
        format="WEBP",
        save_all=True,
        append_images=frames[1:],
        duration=durations,
        loop=args.loop,
        lossless=True,
        quality=100,
        method=4,
    )
    make_contact_sheet(frames, args.output.parent.parent / "qa" / f"{args.output.stem}-contact-sheet.png")
    print(f"frames={len(frames)} duration_ms={sum(durations)} output={args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
