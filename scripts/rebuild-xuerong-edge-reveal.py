#!/usr/bin/env python3
"""Build a fixed-anchor edge entrance by revealing one exact source pose."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-webp", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--duration-ms", type=int, required=True)
    parser.add_argument("--fps", type=int, choices=(24, 30), default=30)
    parser.add_argument("--loop", type=int, default=1)
    parser.add_argument("--start-hold", type=float, default=0.04)
    parser.add_argument("--end-hold", type=float, default=0.14)
    parser.add_argument("--vertical-bias", type=float, default=0.22)
    return parser.parse_args()


def first_frame(path: Path) -> Image.Image:
    with Image.open(path) as image:
        image.seek(0)
        return image.convert("RGBA").copy()


def clear_transparent_rgb(frame: Image.Image) -> Image.Image:
    pixels = np.array(frame, dtype=np.uint8, copy=True)
    pixels[pixels[:, :, 3] == 0, :3] = 0
    return Image.fromarray(pixels, "RGBA")


def eased_progress(index: int, count: int, start_hold: float, end_hold: float) -> float:
    initial_progress = 0.012
    phase = index / max(1, count - 1)
    if phase <= start_hold:
        return initial_progress
    if phase >= 1.0 - end_hold:
        return 1.0
    phase = (phase - start_hold) / (1.0 - start_hold - end_hold)
    eased = phase * phase * (3.0 - 2.0 * phase)
    return initial_progress + (1.0 - initial_progress) * eased


def reveal(frame: Image.Image, progress: float, vertical_bias: float) -> Image.Image:
    pixels = np.array(frame, dtype=np.uint8, copy=True)
    alpha = pixels[:, :, 3]
    ys, xs = np.nonzero(alpha > 0)
    if len(xs) == 0:
        raise ValueError("source frame is empty")
    left, top, right, bottom = xs.min(), ys.min(), xs.max() + 1, ys.max() + 1
    x_distance = (right - 1 - np.arange(frame.width)) / max(1, right - left - 1)
    y_distance = (np.arange(frame.height) - top) / max(1, bottom - top - 1)
    score = (
        x_distance[np.newaxis, :] + vertical_bias * y_distance[:, np.newaxis]
    ) / (1.0 + vertical_bias)
    visible_scores = score[alpha > 0]
    threshold = float(np.quantile(visible_scores, progress))
    keep = score <= threshold
    pixels[~keep, 3] = 0
    pixels[pixels[:, :, 3] == 0, :3] = 0
    return Image.fromarray(pixels, "RGBA")


def distribute_durations(total_ms: int, count: int) -> list[int]:
    base, remainder = divmod(total_ms, count)
    return [base + (1 if index < remainder else 0) for index in range(count)]


def make_contact_sheet(frames: list[Image.Image], path: Path) -> None:
    selected = [frames[round(index * (len(frames) - 1) / 7)] for index in range(8)]
    sheet = Image.new("RGB", (8 * 180, 210), (10, 14, 22))
    draw = ImageDraw.Draw(sheet)
    for index, frame in enumerate(selected):
        tile = Image.new("RGBA", (180, 180), (214, 0, 120, 255))
        preview = frame.copy()
        preview.thumbnail((172, 176), Image.Resampling.LANCZOS)
        tile.alpha_composite(preview, ((180 - preview.width) // 2, 180 - preview.height))
        sheet.paste(tile.convert("RGB"), (index * 180, 24))
        draw.text((index * 180 + 6, 5), str(index + 1), fill=(255, 255, 255))
    path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(path)


def main() -> int:
    args = parse_args()
    source = clear_transparent_rgb(first_frame(args.source_webp))
    count = round(args.duration_ms * args.fps / 1000)
    frames = [
        reveal(
            source,
            eased_progress(index, count, args.start_hold, args.end_hold),
            args.vertical_bias,
        )
        for index in range(count)
    ]
    frames[-1] = source.copy()
    durations = distribute_durations(args.duration_ms, count)
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
        exact=True,
        background=(0, 0, 0, 0),
        minimize_size=False,
        kmin=1,
        kmax=1,
        allow_mixed=False,
    )
    make_contact_sheet(
        frames,
        args.output.parent.parent / "qa" / f"{args.output.stem}.png",
    )
    print(f"frames={count} duration_ms={sum(durations)} output={args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
