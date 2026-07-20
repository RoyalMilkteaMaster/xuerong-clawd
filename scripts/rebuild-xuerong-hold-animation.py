#!/usr/bin/env python3
"""Rebuild mostly-still WebP loops with explicit holds and no optical flow."""

from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-webp", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--work-dir", type=Path, required=True)
    parser.add_argument("--python", type=Path, required=True)
    parser.add_argument("--chroma-helper", type=Path, required=True)
    parser.add_argument("--durations", required=True)
    parser.add_argument("--frame-map", default="")
    parser.add_argument("--scale", type=float, default=1.0)
    parser.add_argument("--offset-x", type=int, default=0)
    parser.add_argument("--offset-y", type=int, default=0)
    parser.add_argument("--fit-to-first", action="store_true")
    parser.add_argument("--binary-alpha", action="store_true")
    parser.add_argument("--loop", type=int, default=0)
    parser.add_argument("--close-loop", type=int, choices=(0, 1), default=1)
    return parser.parse_args()


def safe_reset_dir(path: Path) -> None:
    resolved = path.resolve()
    build_root = (Path.cwd() / "build").resolve()
    if build_root not in resolved.parents:
        raise RuntimeError(f"refusing to reset work dir outside build: {resolved}")
    if resolved.exists():
        shutil.rmtree(resolved)
    resolved.mkdir(parents=True)


def decode(path: Path) -> list[Image.Image]:
    frames = []
    with Image.open(path) as image:
        for index in range(getattr(image, "n_frames", 1)):
            image.seek(index)
            frames.append(image.convert("RGBA").copy())
    return frames


def clean_alpha(args: argparse.Namespace, frame: Image.Image, index: int) -> Image.Image:
    green = Image.new("RGBA", frame.size, (0, 255, 0, 255))
    green.alpha_composite(frame)
    source = args.work_dir / f"{index:02d}-green.png"
    output = args.work_dir / f"{index:02d}-alpha.png"
    green.convert("RGB").save(source)
    subprocess.run([
        str(args.python), str(args.chroma_helper),
        "--input", str(source), "--out", str(output),
        "--auto-key", "border", "--soft-matte",
        "--transparent-threshold", "12", "--opaque-threshold", "220",
        "--despill", "--edge-contract", "1",
    ], check=True, stdout=subprocess.DEVNULL)
    return Image.open(output).convert("RGBA").copy()


def scale_about_baseline(frame: Image.Image, scale: float) -> Image.Image:
    box = frame.getchannel("A").getbbox()
    if box is None or abs(scale - 1.0) < 0.0001:
        return frame.copy()
    crop = frame.crop(box).convert("RGBa")
    size = (max(1, round(crop.width * scale)), max(1, round(crop.height * scale)))
    crop = crop.resize(size, Image.Resampling.LANCZOS).convert("RGBA")
    x = round((box[0] + box[2] - crop.width) / 2)
    y = box[3] - crop.height
    output = Image.new("RGBA", frame.size, (0, 0, 0, 0))
    output.alpha_composite(crop, (x, y))
    return output


def clear_transparent_rgb(frame: Image.Image) -> Image.Image:
    pixels = np.array(frame, dtype=np.uint8, copy=True)
    pixels[pixels[:, :, 3] == 0, :3] = 0
    return Image.fromarray(pixels, "RGBA")


def translate_frame(frame: Image.Image, offset_x: int, offset_y: int) -> Image.Image:
    if offset_x == 0 and offset_y == 0:
        return frame.copy()
    output = Image.new("RGBA", frame.size, (0, 0, 0, 0))
    output.alpha_composite(frame, (offset_x, offset_y))
    return output


def fit_to_box(frame: Image.Image, box: tuple[int, int, int, int]) -> Image.Image:
    source_box = frame.getchannel("A").getbbox()
    if source_box is None:
        return frame.copy()
    crop = frame.crop(source_box).convert("RGBa")
    crop = crop.resize((box[2] - box[0], box[3] - box[1]), Image.Resampling.LANCZOS)
    output = Image.new("RGBA", frame.size, (0, 0, 0, 0))
    output.alpha_composite(crop.convert("RGBA"), (box[0], box[1]))
    return output


def make_binary_alpha(frame: Image.Image) -> Image.Image:
    pixels = np.array(frame, dtype=np.uint8, copy=True)
    pixels[:, :, 3] = np.where(pixels[:, :, 3] >= 128, 255, 0).astype(np.uint8)
    pixels[pixels[:, :, 3] == 0, :3] = 0
    return Image.fromarray(pixels, "RGBA")


def main() -> int:
    args = parse_args()
    safe_reset_dir(args.work_dir)
    durations = [int(value) for value in args.durations.split(",")]
    source_frames = decode(args.source_webp)
    frame_map = (
        [int(value) for value in args.frame_map.split(",")]
        if args.frame_map else list(range(len(source_frames)))
    )
    frames = [source_frames[index] for index in frame_map]
    if len(frames) != len(durations):
        raise ValueError(f"{len(frames)} selected frames but {len(durations)} durations")
    frames = [
        clear_transparent_rgb(scale_about_baseline(clean_alpha(args, frame, index), args.scale))
        for index, frame in enumerate(frames)
    ]
    if args.fit_to_first:
        target_box = frames[0].getchannel("A").getbbox()
        if target_box is None:
            raise ValueError("first selected frame is empty")
        frames = [fit_to_box(frame, target_box) for frame in frames]
    frames = [translate_frame(frame, args.offset_x, args.offset_y) for frame in frames]
    if args.binary_alpha:
        frames = [make_binary_alpha(frame) for frame in frames]
    if args.close_loop:
        frames[-1] = frames[0].copy()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    frames[0].save(
        args.output, format="WEBP", save_all=True, append_images=frames[1:],
        duration=durations, loop=args.loop, lossless=True, quality=100, method=4,
        exact=True, background=(0, 0, 0, 0), minimize_size=False,
        kmin=1, kmax=1, allow_mixed=False,
    )
    print(f"frames={len(frames)} duration_ms={sum(durations)} output={args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
