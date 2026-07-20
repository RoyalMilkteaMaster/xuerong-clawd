#!/usr/bin/env python3
"""Build one smooth Xuerong WebP without interpolating RGB and alpha separately."""

from __future__ import annotations

import argparse
import math
import shutil
import subprocess
from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--strip", type=Path)
    source.add_argument("--source-webp", type=Path)
    parser.add_argument("--first-frame-webp", type=Path)
    parser.add_argument("--last-frame-webp", type=Path)
    parser.add_argument("--fit-between-endpoints", action="store_true")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--work-dir", type=Path, required=True)
    parser.add_argument("--rife", type=Path, required=True)
    parser.add_argument("--model", type=Path, required=True)
    parser.add_argument("--python", type=Path, required=True)
    parser.add_argument("--chroma-helper", type=Path, required=True)
    parser.add_argument("--duration-ms", type=int, required=True)
    parser.add_argument("--fps", type=int, choices=(24, 30), default=30)
    parser.add_argument("--target-height", type=int, required=True)
    parser.add_argument("--baseline", type=int, required=True)
    parser.add_argument("--align", choices=("left", "center", "right"), default="center")
    parser.add_argument("--offset-x", type=int, default=0)
    parser.add_argument("--offset-y", type=int, default=0)
    parser.add_argument("--registration", choices=("shared", "preserve"), default="shared")
    parser.add_argument("--loop", type=int, default=0)
    parser.add_argument("--close-loop", type=int, choices=(0, 1), default=1)
    parser.add_argument("--keep-terminal-duplicate", action="store_true")
    parser.add_argument("--segment-weights", default="")
    parser.add_argument("--hold-fractions", default="")
    parser.add_argument("--cut-segments", default="")
    parser.add_argument("--edge-contract", type=int, choices=(0, 1, 2), default=1)
    parser.add_argument("--motion-equalized", action="store_true")
    parser.add_argument("--reuse-work-dir", action="store_true")
    parser.add_argument("--hard-chroma-threshold", type=int, default=0)
    parser.add_argument("--normalize-each-output", action="store_true")
    parser.add_argument("--binary-output-alpha", action="store_true")
    return parser.parse_args()


def parse_float_list(value: str, count: int, default: float) -> list[float]:
    if not value:
        return [default] * count
    result = [float(item) for item in value.split(",")]
    if len(result) != count:
        raise ValueError(f"expected {count} comma-separated values, got {len(result)}")
    return result


def safe_reset_dir(path: Path) -> None:
    resolved = path.resolve()
    build_root = (Path.cwd() / "build").resolve()
    if build_root not in resolved.parents:
        raise RuntimeError(f"refusing to reset work dir outside build: {resolved}")
    if resolved.exists():
        shutil.rmtree(resolved)
    resolved.mkdir(parents=True)


def remove_chroma(args: argparse.Namespace, source: Path, output: Path) -> None:
    command = [
        str(args.python), str(args.chroma_helper),
        "--input", str(source), "--out", str(output),
        "--auto-key", "border", "--soft-matte",
        "--transparent-threshold", "12", "--opaque-threshold", "220",
        "--despill", "--edge-contract", str(args.edge_contract), "--force",
    ]
    subprocess.run(command, check=True, stdout=subprocess.DEVNULL)


def component_boxes(image: Image.Image) -> list[tuple[int, int, int, int]]:
    alpha = np.asarray(image.getchannel("A"), dtype=np.uint8)
    mask = alpha > 16
    height, width = mask.shape
    seen = np.zeros_like(mask, dtype=bool)
    components: list[tuple[int, tuple[int, int, int, int]]] = []
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
        if len(points) < 24:
            continue
        ys, xs = zip(*points)
        components.append((len(points), (min(xs), min(ys), max(xs) + 1, max(ys) + 1)))
    if len(components) < 8:
        raise RuntimeError(f"expected 8 pose components, found {len(components)}")
    components.sort(reverse=True)
    poses = [box for _, box in components[:8]]
    for _, effect in components[8:]:
        effect_x = (effect[0] + effect[2]) / 2
        index = min(range(8), key=lambda item: abs((poses[item][0] + poses[item][2]) / 2 - effect_x))
        left, top, right, bottom = poses[index]
        poses[index] = (
            min(left, effect[0]), min(top, effect[1]),
            max(right, effect[2]), max(bottom, effect[3]),
        )
    return sorted(poses, key=lambda box: box[0])


def register_crops(
    crops: list[Image.Image],
    target_height: int,
    baseline: int,
    align: str,
) -> list[Image.Image]:
    heights = [crop.height for crop in crops]
    shared_scale = target_height / np.median(heights)
    frames = []
    for crop in crops:
        size = (max(1, round(crop.width * shared_scale)), max(1, round(crop.height * shared_scale)))
        crop = crop.resize(size, Image.Resampling.LANCZOS)
        frame = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
        if align == "left":
            x = 0
        elif align == "right":
            x = 512 - crop.width
        else:
            x = round((512 - crop.width) / 2)
        frame.alpha_composite(crop, (x, baseline - crop.height))
        frames.append(frame)
    return frames


def register_each_frame(
    frames: list[Image.Image],
    target_height: int,
    baseline: int,
    align: str,
) -> list[Image.Image]:
    registered = []
    for frame in frames:
        box = frame.getchannel("A").getbbox()
        if box is None:
            raise ValueError("cannot register an empty output frame")
        crop = frame.crop(box).convert("RGBa")
        scale = target_height / crop.height
        width = max(1, round(crop.width * scale))
        crop = crop.resize((width, target_height), Image.Resampling.LANCZOS).convert("RGBA")
        if align == "left":
            x = 0
        elif align == "right":
            x = 512 - width
        else:
            x = round((512 - width) / 2)
        output = Image.new("RGBA", frame.size, (0, 0, 0, 0))
        output.alpha_composite(crop, (x, baseline - target_height))
        registered.append(clear_transparent_rgb(output))
    return registered


def strip_crops(strip: Image.Image) -> list[Image.Image]:
    return [strip.crop(box) for box in component_boxes(strip)]


def webp_frames(path: Path) -> list[Image.Image]:
    frames = []
    with Image.open(path) as image:
        for index in range(getattr(image, "n_frames", 1)):
            image.seek(index)
            frame = image.convert("RGBA")
            if frame.getchannel("A").getbbox() is not None:
                frames.append(frame.copy())
    if len(frames) < 2:
        raise RuntimeError(f"expected at least 2 visible WebP frames, found {len(frames)}")
    return frames


def first_webp_frame(path: Path) -> Image.Image:
    with Image.open(path) as image:
        image.seek(0)
        return clear_transparent_rgb(image.convert("RGBA").copy())


def crop_visible_frames(frames: list[Image.Image]) -> list[Image.Image]:
    return [frame.crop(frame.getchannel("A").getbbox()) for frame in frames]


def distribute_counts(total: int, weights: list[float]) -> list[int]:
    raw = [total * weight / sum(weights) for weight in weights]
    counts = [max(1, math.floor(value)) for value in raw]
    while sum(counts) < total:
        index = max(range(len(raw)), key=lambda item: raw[item] - counts[item])
        counts[index] += 1
    while sum(counts) > total:
        choices = [item for item, count in enumerate(counts) if count > 1]
        index = min(choices, key=lambda item: raw[item] - counts[item])
        counts[index] -= 1
    return counts


def composite_green(frame: Image.Image) -> Image.Image:
    canvas = Image.new("RGBA", frame.size, (0, 255, 0, 255))
    canvas.alpha_composite(frame)
    return canvas.convert("RGB")


def interpolate_pair(
    args: argparse.Namespace,
    first: Image.Image,
    second: Image.Image,
    segment_dir: Path,
    count: int,
    hold_fraction: float,
    cut: bool,
    include_start: bool,
) -> list[Image.Image]:
    if cut:
        if count <= 1:
            return [second.copy()]
        return [first.copy() for _ in range(count - 1)] + [second.copy()]
    if count <= 1:
        return [second.copy()]
    input_dir = segment_dir / "input"
    output_dir = segment_dir / "output"
    alpha_dir = segment_dir / "alpha"
    dense_count = max(17, count * 6 + 1)
    dense_paths = sorted(output_dir.glob("*.png")) if output_dir.exists() else []
    if not args.reuse_work_dir or len(dense_paths) < dense_count:
        if output_dir.exists():
            shutil.rmtree(output_dir)
        input_dir.mkdir(parents=True, exist_ok=True)
        output_dir.mkdir(parents=True)
        composite_green(first).save(input_dir / "00000000.png")
        composite_green(second).save(input_dir / "00000001.png")
        subprocess.run([
            str(args.rife), "-i", str(input_dir), "-o", str(output_dir),
            "-n", str(dense_count), "-m", str(args.model), "-g", "0", "-j", "2:2:2",
        ], check=True, stdout=subprocess.DEVNULL)
    alpha_dir.mkdir(parents=True, exist_ok=True)
    dense_paths = sorted(output_dir.glob("*.png"))
    if len(dense_paths) < 2:
        raise RuntimeError(f"RIFE produced too few frames for {segment_dir}")
    motion_positions = None
    if args.motion_equalized:
        cumulative = [0.0]
        previous = np.asarray(Image.open(dense_paths[0]).convert("RGB"), dtype=np.int16)
        for dense_path in dense_paths[1:]:
            current = np.asarray(Image.open(dense_path).convert("RGB"), dtype=np.int16)
            cumulative.append(cumulative[-1] + float(np.abs(current - previous).mean()))
            previous = current
        total_motion = cumulative[-1]
        motion_positions = (
            [value / total_motion for value in cumulative]
            if total_motion > 1e-9 else [index / (len(cumulative) - 1) for index in range(len(cumulative))]
        )
    result = []
    for index in range(count):
        phase = index / (count - 1) if include_start else (index + 1) / count
        if phase <= hold_fraction:
            eased = 0.0
        else:
            phase = (phase - hold_fraction) / max(1e-6, 1.0 - hold_fraction)
            eased = phase * phase * (3.0 - 2.0 * phase)
        if motion_positions is None:
            dense_index = round(eased * (len(dense_paths) - 1))
        else:
            dense_index = min(
                range(len(motion_positions)),
                key=lambda item: abs(motion_positions[item] - eased),
            )
        keyed = output_dir / dense_paths[dense_index].name
        if args.hard_chroma_threshold:
            result.append(remove_chroma_hard(Image.open(keyed), args.hard_chroma_threshold))
        else:
            alpha_path = alpha_dir / f"{index:03d}.png"
            remove_chroma(args, keyed, alpha_path)
            result.append(Image.open(alpha_path).convert("RGBA").copy())
    return result


def normalize_endpoint(
    args: argparse.Namespace,
    frame: Image.Image,
    work_dir: Path,
    name: str,
) -> Image.Image:
    source = work_dir / f"{name}-green.png"
    output = work_dir / f"{name}-alpha.png"
    composite_green(frame).save(source)
    remove_chroma(args, source, output)
    return Image.open(output).convert("RGBA").copy()


def clear_transparent_rgb(frame: Image.Image) -> Image.Image:
    pixels = np.array(frame, dtype=np.uint8, copy=True)
    pixels[pixels[:, :, 3] == 0, :3] = 0
    return Image.fromarray(pixels, "RGBA")


def remove_chroma_hard(frame: Image.Image, threshold: int) -> Image.Image:
    rgb = np.asarray(frame.convert("RGB"), dtype=np.int32)
    distance_squared = (
        rgb[:, :, 0] ** 2
        + (255 - rgb[:, :, 1]) ** 2
        + rgb[:, :, 2] ** 2
    )
    mask = distance_squared >= threshold * threshold
    output = rgb.copy()
    red_blue_max = np.maximum(output[:, :, 0], output[:, :, 2])
    output[:, :, 1] = np.minimum(output[:, :, 1], red_blue_max + 20)
    rgba = np.zeros((frame.height, frame.width, 4), dtype=np.uint8)
    rgba[:, :, :3] = np.clip(output, 0, 255).astype(np.uint8)
    rgba[:, :, 3] = np.where(mask, 255, 0).astype(np.uint8)
    rgba[~mask, :3] = 0
    return Image.fromarray(rgba, "RGBA")


def make_binary_alpha(frame: Image.Image) -> Image.Image:
    pixels = np.array(frame, dtype=np.uint8, copy=True)
    pixels[:, :, 3] = np.where(pixels[:, :, 3] >= 128, 255, 0).astype(np.uint8)
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
        raise ValueError("cannot fit an empty keyframe")
    crop = frame.crop(source_box).convert("RGBa")
    crop = crop.resize((box[2] - box[0], box[3] - box[1]), Image.Resampling.LANCZOS)
    output = Image.new("RGBA", frame.size, (0, 0, 0, 0))
    output.alpha_composite(crop.convert("RGBA"), (box[0], box[1]))
    return clear_transparent_rgb(output)


def distribute_durations(total_ms: int, count: int) -> list[int]:
    base, remainder = divmod(total_ms, count)
    return [base + (1 if index < remainder else 0) for index in range(count)]


def make_contact_sheet(frames: list[Image.Image], path: Path) -> None:
    chosen = [frames[round(index * (len(frames) - 1) / 7)] for index in range(8)]
    sheet = Image.new("RGB", (8 * 180, 210), (10, 14, 22))
    draw = ImageDraw.Draw(sheet)
    for index, frame in enumerate(chosen):
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
    if args.reuse_work_dir:
        args.work_dir.resolve().mkdir(parents=True, exist_ok=True)
    else:
        safe_reset_dir(args.work_dir)
    transparent_strip_source = False
    if args.strip is not None:
        transparent_strip = args.work_dir / "strip-alpha.png"
        with Image.open(args.strip.resolve()) as source_strip:
            source_rgba = source_strip.convert("RGBA")
            transparent_strip_source = source_rgba.getchannel("A").getextrema()[0] < 255
            if transparent_strip_source:
                source_rgba.save(transparent_strip)
            else:
                remove_chroma(args, args.strip.resolve(), transparent_strip)
        strip = Image.open(transparent_strip).convert("RGBA")
        if args.registration == "preserve":
            if strip.height != 512 or strip.width % 512:
                raise ValueError("preserved strips must contain 512x512 cells")
            keyframes = [
                strip.crop((x, 0, x + 512, 512))
                for x in range(0, strip.width, 512)
            ]
        else:
            crops = strip_crops(strip)
            keyframes = register_crops(crops, args.target_height, args.baseline, args.align)
    else:
        source_frames = webp_frames(args.source_webp.resolve())
        keyframes = source_frames if args.registration == "preserve" else register_crops(
            crop_visible_frames(source_frames), args.target_height, args.baseline, args.align
        )
    keyframes = [translate_frame(frame, args.offset_x, args.offset_y) for frame in keyframes]
    first_override = (
        first_webp_frame(args.first_frame_webp.resolve())
        if args.first_frame_webp is not None else None
    )
    last_override = (
        first_webp_frame(args.last_frame_webp.resolve())
        if args.last_frame_webp is not None else None
    )
    if first_override is not None:
        keyframes[0] = first_override
    if last_override is not None:
        keyframes[-1] = last_override
    if args.fit_between_endpoints:
        if first_override is None or last_override is None:
            raise ValueError("--fit-between-endpoints requires both endpoint WebPs")
        first_box = first_override.getchannel("A").getbbox()
        last_box = last_override.getchannel("A").getbbox()
        if first_box is None or last_box is None:
            raise ValueError("endpoint frame is empty")
        for index in range(1, len(keyframes) - 1):
            phase = index / (len(keyframes) - 1)
            target_box = tuple(
                round(start + (end - start) * phase)
                for start, end in zip(first_box, last_box)
            )
            keyframes[index] = fit_to_box(keyframes[index], target_box)
    if (
        args.close_loop
        and not args.keep_terminal_duplicate
        and len(keyframes) > 2
        and np.array_equal(np.asarray(keyframes[0]), np.asarray(keyframes[-1]))
    ):
        keyframes.pop()
    segment_count = len(keyframes) if args.close_loop else len(keyframes) - 1
    weights = parse_float_list(args.segment_weights, segment_count, 1.0)
    holds = parse_float_list(args.hold_fractions, segment_count, 0.0)
    if any(not 0.0 <= value < 1.0 for value in holds):
        raise ValueError("hold fractions must be in [0, 1)")
    cuts = {int(item) for item in args.cut_segments.split(",") if item.strip()}
    total_frames = round(args.duration_ms * args.fps / 1000)
    counts = distribute_counts(total_frames, weights)
    frames = []
    for index, count in enumerate(counts):
        frames.extend(interpolate_pair(
            args,
            keyframes[index], keyframes[(index + 1) % len(keyframes)],
            args.work_dir / f"segment-{index:02d}", count, holds[index], index in cuts,
            index == 0,
        ))
    if len(frames) != total_frames:
        raise AssertionError((len(frames), total_frames))
    if args.normalize_each_output:
        frames = register_each_frame(
            frames, args.target_height, args.baseline, args.align
        )
    if args.binary_output_alpha:
        frames = [make_binary_alpha(frame) for frame in frames]
    if first_override is not None:
        first = first_override
    elif transparent_strip_source:
        first = clear_transparent_rgb(keyframes[0])
    else:
        first = normalize_endpoint(args, keyframes[0], args.work_dir, "endpoint-first")
    if args.close_loop:
        last = first.copy()
    else:
        if last_override is not None:
            last = last_override
        elif transparent_strip_source:
            last = clear_transparent_rgb(keyframes[-1])
        else:
            last = normalize_endpoint(args, keyframes[-1], args.work_dir, "endpoint-last")
    frames[0] = first
    frames[-1] = last
    frames = [clear_transparent_rgb(frame) for frame in frames]
    durations = distribute_durations(args.duration_ms, len(frames))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    frames[0].save(
        args.output, format="WEBP", save_all=True, append_images=frames[1:],
        duration=durations, loop=args.loop, lossless=True, quality=100, method=4,
        exact=True, background=(0, 0, 0, 0), minimize_size=False,
        kmin=1, kmax=1, allow_mixed=False,
    )
    make_contact_sheet(frames, args.output.parent.parent / "qa" / f"{args.output.stem}.png")
    print(f"frames={len(frames)} duration_ms={sum(durations)} output={args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
