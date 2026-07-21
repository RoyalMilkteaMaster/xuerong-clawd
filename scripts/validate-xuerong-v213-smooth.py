#!/usr/bin/env python3
"""Validate a smoothed Xuerong theme without changing any theme assets."""

from __future__ import annotations

import argparse
import bisect
import hashlib
import json
import math
import tempfile
from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont


CANVAS = (512, 512)
MAX_GEOMETRY_DRIFT = 0.05
CONTACT_SAMPLES = 8
WAVING_DURATION_MS = 1600
LOOP_ASSETS = {
    "failed.webp", "grabbed.webp", "idle.webp", "jumping.webp",
    "mini-alert.webp", "mini-crabwalk.webp", "mini-happy.webp",
    "mini-idle.webp", "mini-peek.webp", "mini-sleep.webp",
    "mini-working-v213.webp", "mini-working.webp", "review.webp",
    "running-left.webp", "running-right.webp", "running.webp",
    "sleeping.webp", "typing.webp", "waiting.webp", "waving.webp",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--reference-theme", type=Path)
    parser.add_argument("--candidate-theme", type=Path)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--self-check", action="store_true")
    args = parser.parse_args()
    if not args.self_check and not all((args.reference_theme, args.candidate_theme, args.output_dir)):
        parser.error("--reference-theme, --candidate-theme and --output-dir are required")
    return args


def asset_dir(theme: Path) -> Path:
    assets = theme / "assets"
    return assets if assets.is_dir() else theme


def decode(path: Path) -> tuple[list[Image.Image], list[int]]:
    image = Image.open(path)
    frames: list[Image.Image] = []
    durations = read_webp_frame_durations(path)
    for index in range(image.n_frames):
        image.seek(index)
        frames.append(image.convert("RGBA").copy())
    if len(frames) != len(durations):
        raise ValueError(
            f"decoded frame/timing mismatch: {len(frames)} frames, {len(durations)} durations"
        )
    return frames, durations


def read_webp_frame_durations(path: Path) -> list[int]:
    """Read ANMF durations directly for WebPs whose decoder omits image.info duration."""
    data = path.read_bytes()
    if len(data) < 12 or data[:4] != b"RIFF" or data[8:12] != b"WEBP":
        raise ValueError(f"not a WebP RIFF file: {path}")
    durations: list[int] = []
    position = 12
    while position + 8 <= len(data):
        tag = data[position:position + 4]
        size = int.from_bytes(data[position + 4:position + 8], "little")
        payload_start = position + 8
        payload_end = payload_start + size
        if payload_end > len(data):
            raise ValueError(f"truncated WebP chunk in {path}")
        if tag == b"ANMF":
            if size < 16:
                raise ValueError(f"invalid ANMF chunk in {path}")
            duration = int.from_bytes(data[payload_start + 12:payload_start + 15], "little")
            if duration <= 0:
                raise ValueError(f"animated WebP contains a non-positive frame duration: {path}")
            durations.append(duration)
        position = payload_end + (size & 1)
    if not durations:
        raise ValueError(f"animated WebP has no ANMF timing records: {path}")
    return durations


def timestamps(durations: list[int]) -> list[int]:
    result = []
    elapsed = 0
    for duration in durations:
        result.append(elapsed)
        elapsed += duration
    return result


def canonical_visible(frame: Image.Image) -> Image.Image:
    result = frame.copy()
    transparent = result.getchannel("A").point(lambda alpha: 255 if alpha == 0 else 0)
    result.paste((0, 0, 0, 0), mask=transparent)
    return result


def exact_visible(left: Image.Image, right: Image.Image) -> bool:
    return ImageChops.difference(canonical_visible(left), canonical_visible(right)).getbbox() is None


def exact_alpha(left: Image.Image, right: Image.Image) -> bool:
    return ImageChops.difference(left.getchannel("A"), right.getchannel("A")).getbbox() is None


def remove_detached_components(frame: Image.Image, proximity_px: int = 6) -> Image.Image:
    """Remove alpha islands not connected or visually adjacent to the main character."""
    rgba = np.asarray(frame.convert("RGBA"), dtype=np.uint8).copy()
    mask = rgba[:, :, 3] > 0
    seen = np.zeros(mask.shape, dtype=bool)
    components: list[list[tuple[int, int]]] = []
    for y, x in np.argwhere(mask):
        if seen[y, x]:
            continue
        queue = deque([(int(y), int(x))])
        seen[y, x] = True
        points: list[tuple[int, int]] = []
        while queue:
            cy, cx = queue.popleft()
            points.append((cy, cx))
            for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)):
                ny, nx = cy + dy, cx + dx
                if 0 <= ny < mask.shape[0] and 0 <= nx < mask.shape[1] and mask[ny, nx] and not seen[ny, nx]:
                    seen[ny, nx] = True
                    queue.append((ny, nx))
        components.append(points)
    if not components:
        return frame.copy()
    main = max(components, key=len)
    main_mask = Image.new("L", frame.size, 0)
    main_pixels = np.zeros(mask.shape, dtype=np.uint8)
    main_y, main_x = zip(*main)
    main_pixels[np.asarray(main_y), np.asarray(main_x)] = 255
    main_mask = Image.fromarray(main_pixels, "L").filter(ImageFilter.MaxFilter(proximity_px * 2 + 1))
    near_main = np.asarray(main_mask, dtype=np.uint8) > 0
    keep = np.zeros(mask.shape, dtype=bool)
    for component in components:
        ys, xs = zip(*component)
        y_values = np.asarray(ys)
        x_values = np.asarray(xs)
        if np.any(near_main[y_values, x_values]):
            keep[y_values, x_values] = True
    rgba[~keep] = 0
    return Image.fromarray(rgba, "RGBA")


def normalized_reference_frames(asset_name: str, frames: list[Image.Image]) -> list[Image.Image]:
    if asset_name != "running-left.webp":
        return frames
    return [remove_detached_components(frame) for frame in frames]


def checker(size: int, tile: int = 16) -> Image.Image:
    image = Image.new("RGBA", (size, size), "white")
    draw = ImageDraw.Draw(image)
    colors = ((199, 220, 234, 255), (245, 249, 252, 255))
    for y in range(0, size, tile):
        for x in range(0, size, tile):
            draw.rectangle((x, y, x + tile - 1, y + tile - 1), fill=colors[(x // tile + y // tile) % 2])
    return image


def visible_difference(left: Image.Image, right: Image.Image) -> float:
    background = checker(left.width)
    left_visible = background.copy()
    right_visible = background.copy()
    left_visible.alpha_composite(left)
    right_visible.alpha_composite(right)
    difference = ImageChops.difference(left_visible.convert("RGB"), right_visible.convert("RGB"))
    total = sum(value * (index % 256) for index, value in enumerate(difference.histogram()))
    return total / (left.width * left.height * 3 * 255)


def bbox_geometry(frame: Image.Image) -> tuple[float, float, float, float] | None:
    bbox = frame.getchannel("A").getbbox()
    if not bbox:
        return None
    left, top, right, bottom = bbox
    return (right - left, bottom - top, (left + right) / 2, bottom)


def interpolate_geometry(
    time_ms: int,
    reference_times: list[int],
    reference_geometry: list[tuple[float, float, float, float] | None],
) -> tuple[float, float, float, float] | None:
    right_index = bisect.bisect_right(reference_times, time_ms)
    if right_index == 0:
        return reference_geometry[0]
    if right_index >= len(reference_times):
        return reference_geometry[-1]
    left_index = right_index - 1
    left_geometry = reference_geometry[left_index]
    right_geometry = reference_geometry[right_index]
    if left_geometry is None or right_geometry is None:
        return left_geometry or right_geometry
    span = reference_times[right_index] - reference_times[left_index]
    ratio = (time_ms - reference_times[left_index]) / span if span else 0
    return tuple(left + (right - left) * ratio for left, right in zip(left_geometry, right_geometry))


def geometry_drift(
    actual: tuple[float, float, float, float] | None,
    expected: tuple[float, float, float, float] | None,
) -> dict:
    if actual is None or expected is None:
        return {"ok": actual == expected, "reason": "empty silhouette mismatch"}
    width, height, center_x, baseline = actual
    expected_width, expected_height, expected_center_x, expected_baseline = expected
    values = {
        "width": abs(width - expected_width) / max(expected_width, 1),
        "height": abs(height - expected_height) / max(expected_height, 1),
        "center_x": abs(center_x - expected_center_x) / max(expected_width, 1),
        "baseline": abs(baseline - expected_baseline) / max(expected_height, 1),
    }
    return {"ok": max(values.values()) <= MAX_GEOMETRY_DRIFT, **values}


def count_mask(mask: Image.Image) -> int:
    return mask.histogram()[255]


def transparency_metrics(frame: Image.Image) -> dict:
    red, green, blue, alpha = frame.split()
    semi = alpha.point(lambda value: 255 if 0 < value < 255 else 0)
    low = alpha.point(lambda value: 255 if 0 < value <= 127 else 0)
    strong_low = alpha.point(lambda value: 255 if 16 <= value <= 127 else 0)
    core = alpha.point(lambda value: 255 if value >= 192 else 0)
    supported = core.filter(ImageFilter.MaxFilter(7))
    unsupported = ImageChops.multiply(semi, ImageChops.invert(supported))

    maximum = ImageChops.lighter(ImageChops.lighter(red, green), blue)
    minimum = ImageChops.darker(ImageChops.darker(red, green), blue)
    chroma = ImageChops.subtract(maximum, minimum)
    white = ImageChops.multiply(
        ImageChops.multiply(red.point(lambda value: 255 if value >= 210 else 0), green.point(lambda value: 255 if value >= 210 else 0)),
        ImageChops.multiply(blue.point(lambda value: 255 if value >= 210 else 0), chroma.point(lambda value: 255 if value <= 28 else 0)),
    )
    colored = chroma.point(lambda value: 255 if value >= 32 else 0)
    unsupported_low = ImageChops.multiply(unsupported, low)
    visible_white = ImageChops.multiply(ImageChops.multiply(unsupported_low, strong_low), white)
    visible_colored = ImageChops.multiply(ImageChops.multiply(unsupported_low, strong_low), colored)

    opaque_count = sum(alpha.histogram()[192:])
    visible_limit = max(8, math.ceil(opaque_count * 0.0005))
    visible_white_count = count_mask(visible_white)
    visible_colored_count = count_mask(visible_colored)
    coverage = sum(alpha.histogram()[1:]) / (frame.width * frame.height)
    background_fail = coverage > 0.85
    return {
        "semi_alpha_count": count_mask(semi),
        "unsupported_semi_alpha_count": count_mask(unsupported),
        "white_low_alpha_count": count_mask(ImageChops.multiply(low, white)),
        "colored_low_alpha_count": count_mask(ImageChops.multiply(low, colored)),
        "visible_unsupported_white_count": visible_white_count,
        "visible_unsupported_colored_count": visible_colored_count,
        "visible_limit": visible_limit,
        "visible_white_membrane_fail": visible_white_count > visible_limit,
        "visible_colored_background_fail": visible_colored_count > visible_limit,
        "opaque_background_fail": background_fail,
    }


def mode_baseline(frames: list[Image.Image]) -> dict:
    geometry = [bbox_geometry(frame) for frame in frames]
    present = [value for value in geometry if value]
    return {
        "source": "same-mode informational baseline only",
        "median_width": sorted(value[0] for value in present)[len(present) // 2],
        "median_height": sorted(value[1] for value in present)[len(present) // 2],
        "median_center_x": sorted(value[2] for value in present)[len(present) // 2],
        "median_baseline": sorted(value[3] for value in present)[len(present) // 2],
    }


def waving_idle_drift(actual: tuple[float, float, float, float] | None, idle: dict) -> dict:
    if actual is None:
        return {"ok": False, "reason": "empty waving silhouette"}
    _, height, center_x, baseline = actual
    values = {
        "height": abs(height - idle["median_height"]) / max(idle["median_height"], 1),
        "center_x": abs(center_x - idle["median_center_x"]) / max(idle["median_width"], 1),
        "baseline": abs(baseline - idle["median_baseline"]) / max(idle["median_height"], 1),
    }
    return {"ok": max(values.values()) <= MAX_GEOMETRY_DRIFT, **values}


def validate_asset(reference_path: Path, candidate_path: Path, idle_baseline: dict | None = None) -> tuple[dict, list[Image.Image]]:
    errors: list[str] = []
    warnings: list[str] = []
    try:
        reference_frames, reference_durations = decode(reference_path)
        candidate_frames, candidate_durations = decode(candidate_path)
        reference_frames = normalized_reference_frames(reference_path.name, reference_frames)
    except Exception as error:
        return {"asset": reference_path.name, "status": "FAIL", "errors": [f"decode failed: {error}"], "warnings": []}, []

    if any(frame.size != CANVAS for frame in reference_frames + candidate_frames):
        errors.append("every frame must be 512x512")
    if any(duration <= 0 for duration in reference_durations + candidate_durations):
        errors.append("every frame duration must be positive")
    reference_total = sum(reference_durations)
    candidate_total = sum(candidate_durations)
    action_reset_exception = reference_path.name == "waving.webp"
    expected_total = WAVING_DURATION_MS if action_reset_exception else reference_total
    if candidate_total != expected_total:
        errors.append(f"duration mismatch: expected={expected_total}ms candidate={candidate_total}ms")

    reference_times = timestamps(reference_durations)
    candidate_times = timestamps(candidate_durations)
    keyframes = []
    used_candidate_indices = set()
    for reference_index, reference_time in enumerate(reference_times):
        candidate_index = min(range(len(candidate_times)), key=lambda index: abs(candidate_times[index] - reference_time))
        used_candidate_indices.add(candidate_index)
        visible_ok = exact_visible(reference_frames[reference_index], candidate_frames[candidate_index])
        alpha_ok = exact_alpha(reference_frames[reference_index], candidate_frames[candidate_index])
        if not action_reset_exception and (not visible_ok or not alpha_ok):
            errors.append(f"reference keyframe {reference_index} missing at nearest candidate frame {candidate_index}")
        keyframes.append({
            "reference_frame": reference_index,
            "reference_time_ms": reference_time,
            "candidate_frame": candidate_index,
            "candidate_time_ms": candidate_times[candidate_index],
            "time_offset_ms": candidate_times[candidate_index] - reference_time,
            "visible_rgba_exact": visible_ok,
            "alpha_exact": alpha_ok,
            "required": not action_reset_exception,
        })
    if not action_reset_exception and len(used_candidate_indices) != len(reference_frames):
        errors.append("multiple reference keyframes collapse onto the same candidate frame")

    reference_geometry = [bbox_geometry(frame) for frame in reference_frames]
    geometry_checks = []
    for index, (time_ms, frame) in enumerate(zip(candidate_times, candidate_frames)):
        if action_reset_exception and idle_baseline:
            drift = waving_idle_drift(bbox_geometry(frame), idle_baseline)
        else:
            drift = geometry_drift(bbox_geometry(frame), interpolate_geometry(time_ms, reference_times, reference_geometry))
        geometry_checks.append({"candidate_frame": index, "time_ms": time_ms, **drift})
    failed_geometry = [item for item in geometry_checks if not item["ok"]]
    if failed_geometry:
        policy = "2.1.3 idle height/center/baseline" if action_reset_exception else "same-asset 2.1.3 envelope"
        errors.append(f"{policy} drift exceeds 5% in {len(failed_geometry)} candidate frames")

    canonical_hashes = [hashlib.sha256(canonical_visible(frame).tobytes()).hexdigest() for frame in candidate_frames]
    duplicate_pairs = []
    unexpected_duplicates = []
    for index in range(1, len(candidate_frames)):
        if canonical_hashes[index] != canonical_hashes[index - 1]:
            continue
        reference_index_a = max(0, bisect.bisect_right(reference_times, candidate_times[index - 1]) - 1)
        reference_index_b = max(0, bisect.bisect_right(reference_times, candidate_times[index]) - 1)
        intentional = reference_index_a == reference_index_b and exact_visible(candidate_frames[index], reference_frames[reference_index_a])
        item = {"frames": [index - 1, index], "intentional_hold": intentional}
        duplicate_pairs.append(item)
        if not intentional:
            unexpected_duplicates.append(item)
    if unexpected_duplicates:
        errors.append(f"unexpected consecutive duplicate frames: {len(unexpected_duplicates)}")

    reference_adjacent = [visible_difference(reference_frames[index - 1], reference_frames[index]) for index in range(1, len(reference_frames))]
    candidate_adjacent = [visible_difference(candidate_frames[index - 1], candidate_frames[index]) for index in range(1, len(candidate_frames))]
    reference_jump = max(reference_adjacent, default=0)
    candidate_jump = max(candidate_adjacent, default=0)
    jump_limit = max(0.003, reference_jump * 1.10)
    if candidate_jump > jump_limit:
        errors.append(f"adjacent visible jump {candidate_jump:.6f} exceeds reference-derived limit {jump_limit:.6f}")

    reference_loop = reference_path.name in LOOP_ASSETS
    if action_reset_exception:
        endpoint_ok = exact_visible(candidate_frames[0], candidate_frames[-1]) and exact_alpha(candidate_frames[0], candidate_frames[-1])
        endpoint_contract = "waving reset loop seam exact"
    elif reference_loop:
        endpoint_ok = exact_visible(candidate_frames[0], candidate_frames[-1]) and exact_alpha(candidate_frames[0], candidate_frames[-1])
        endpoint_contract = "loop seam exact"
    else:
        endpoint_ok = (
            exact_visible(candidate_frames[0], reference_frames[0])
            and exact_alpha(candidate_frames[0], reference_frames[0])
            and exact_visible(candidate_frames[-1], reference_frames[-1])
            and exact_alpha(candidate_frames[-1], reference_frames[-1])
        )
        endpoint_contract = "one-shot endpoints match reference"
    if not endpoint_ok:
        errors.append(endpoint_contract + " failed")

    transparency = [transparency_metrics(frame) for frame in candidate_frames]
    white_fail_frames = [index for index, item in enumerate(transparency) if item["visible_white_membrane_fail"]]
    colored_fail_frames = [index for index, item in enumerate(transparency) if item["visible_colored_background_fail"]]
    background_fail_frames = [index for index, item in enumerate(transparency) if item["opaque_background_fail"]]
    if white_fail_frames:
        errors.append(f"visible white membrane detected in frames {white_fail_frames}")
    if colored_fail_frames:
        errors.append(f"visible colored low-alpha background detected in frames {colored_fail_frames}")
    if background_fail_frames:
        errors.append(f"opaque background detected in frames {background_fail_frames}")
    warnings.append("checker/dark/magenta contact sheets remain the required human visual confirmation")

    return {
        "asset": reference_path.name,
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "warnings": warnings,
        "reference_frame_count": len(reference_frames),
        "candidate_frame_count": len(candidate_frames),
        "reference_duration_ms": reference_total,
        "candidate_duration_ms": candidate_total,
        "action_reset_exception": action_reset_exception,
        "keyframes": keyframes,
        "geometry_5_percent": {
            "status": "PASS" if not failed_geometry else "FAIL",
            "policy": "2.1.3 idle height/center/baseline" if action_reset_exception else "same-asset 2.1.3 envelope",
            "failed_frames": failed_geometry,
        },
        "duplicates": duplicate_pairs,
        "unexpected_duplicate_count": len(unexpected_duplicates),
        "adjacent_jump": {"reference_max": reference_jump, "candidate_max": candidate_jump, "limit": jump_limit},
        "endpoint": {"contract": endpoint_contract, "status": "PASS" if endpoint_ok else "FAIL"},
        "transparency": {
            "unsupported_semi_alpha_max": max((item["unsupported_semi_alpha_count"] for item in transparency), default=0),
            "white_low_alpha_max": max((item["white_low_alpha_count"] for item in transparency), default=0),
            "colored_low_alpha_max": max((item["colored_low_alpha_count"] for item in transparency), default=0),
            "visible_white_membrane_fail_frames": white_fail_frames,
            "visible_colored_background_fail_frames": colored_fail_frames,
            "opaque_background_fail_frames": background_fail_frames,
        },
    }, candidate_frames


def sample_indices(frame_count: int) -> list[int]:
    if frame_count <= CONTACT_SAMPLES:
        return list(range(frame_count))
    return sorted({round(index * (frame_count - 1) / (CONTACT_SAMPLES - 1)) for index in range(CONTACT_SAMPLES)})


def contact_background(mode: str, size: int) -> Image.Image:
    if mode == "dark":
        return Image.new("RGBA", (size, size), (8, 11, 18, 255))
    if mode == "magenta":
        return Image.new("RGBA", (size, size), (205, 0, 120, 255))
    return checker(size, 10)


def write_contact_sheet(output: Path, mode: str, decoded_assets: dict[str, list[Image.Image]]) -> None:
    cell = 128
    label_width = 190
    row_height = cell + 22
    width = label_width + CONTACT_SAMPLES * cell
    height = max(1, len(decoded_assets)) * row_height
    sheet = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()
    for row, (asset, frames) in enumerate(sorted(decoded_assets.items())):
        y = row * row_height
        indices = sample_indices(len(frames))
        draw.text((6, y + 8), f"{asset}\n{len(frames)} frames", fill="black", font=font)
        for column, index in enumerate(indices):
            background = contact_background(mode, cell)
            background.alpha_composite(frames[index].resize((cell, cell), Image.Resampling.LANCZOS))
            x = label_width + column * cell
            sheet.paste(background.convert("RGB"), (x, y))
            draw.text((x + 3, y + cell + 2), f"f{index:02d}", fill="black", font=font)
    sheet.save(output)


def write_markdown(report: dict, path: Path) -> None:
    lines = [
        "# Xuerong 2.1.3 smooth validation",
        "",
        f"**Overall: {report['overall']}**",
        "",
        "| Asset | Result | Ref/Candidate frames | Duration | Keyframes | Geometry | Transparency |",
        "|---|---|---:|---:|---|---|---|",
    ]
    for asset in report["assets"]:
        if asset.get("action_reset_exception"):
            keyframes_result = "EXEMPT"
        else:
            keyframes_result = "PASS" if all(item["visible_rgba_exact"] and item["alpha_exact"] for item in asset.get("keyframes", [])) else "FAIL"
        transparency_ok = not any(asset.get("transparency", {}).get(key, []) for key in (
            "visible_white_membrane_fail_frames", "visible_colored_background_fail_frames", "opaque_background_fail_frames"
        ))
        lines.append(
            f"| `{asset['asset']}` | **{asset['status']}** | "
            f"{asset.get('reference_frame_count', 0)}/{asset.get('candidate_frame_count', 0)} | "
            f"{asset.get('reference_duration_ms', 0)}/{asset.get('candidate_duration_ms', 0)} ms | "
            f"{keyframes_result} | {asset.get('geometry_5_percent', {}).get('status', 'FAIL')} | "
            f"{'PASS' if transparency_ok else 'FAIL'} |"
        )
    lines += [
        "",
        "## Contract",
        "",
        "- Every 2.1.3 keyframe must occur unchanged at the nearest candidate timeline frame.",
        "- The 5% scale/position gate follows each asset's own 2.1.3 trajectory. Idle and mini-idle are group baselines; special poses are never normalized to idle.",
        "- `waving.webp` is the only action-reset exception: its keyframe identity is exempt, but every frame must remain within 5% of 2.1.3 idle height, center and baseline.",
        "- Checker, dark and magenta contact sheets are required for final human confirmation of white membrane, afterimage and background-color spill.",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def validate(reference_theme: Path, candidate_theme: Path, output_dir: Path) -> dict:
    reference_assets = asset_dir(reference_theme)
    candidate_assets = asset_dir(candidate_theme)
    output_dir.mkdir(parents=True, exist_ok=True)
    reference_files = sorted(reference_assets.glob("*.webp"))
    candidate_names = {path.name for path in candidate_assets.glob("*.webp")}
    idle_path = reference_assets / "idle.webp"
    mini_idle_path = reference_assets / "mini-idle.webp"
    idle_baseline = mode_baseline(decode(idle_path)[0]) if idle_path.is_file() else None
    mini_idle_baseline = mode_baseline(decode(mini_idle_path)[0]) if mini_idle_path.is_file() else None
    assets = []
    decoded_assets: dict[str, list[Image.Image]] = {}
    for reference_path in reference_files:
        candidate_path = candidate_assets / reference_path.name
        if not candidate_path.is_file():
            assets.append({"asset": reference_path.name, "status": "FAIL", "errors": ["candidate asset missing"], "warnings": []})
            continue
        result, frames = validate_asset(reference_path, candidate_path, idle_baseline)
        assets.append(result)
        decoded_assets[reference_path.name] = frames

    extra_assets = sorted(candidate_names - {path.name for path in reference_files})
    baseline = {}
    if idle_baseline:
        baseline["general_idle_2_1_3"] = idle_baseline
    if mini_idle_baseline:
        baseline["mini_idle_2_1_3"] = mini_idle_baseline
    group_report = []
    for asset in assets:
        name = asset["asset"]
        frames = decoded_assets.get(name, [])
        group = "mini" if name.startswith("mini-") else "normal"
        group_baseline = mini_idle_baseline if group == "mini" else idle_baseline
        if not frames or not group_baseline:
            continue
        candidate_geometry = mode_baseline(frames)
        group_report.append({
            "asset": name,
            "group": group,
            "baseline_asset": "mini-idle.webp" if group == "mini" else "idle.webp",
            "candidate_height_ratio": candidate_geometry["median_height"] / group_baseline["median_height"],
            "candidate_width_ratio": candidate_geometry["median_width"] / group_baseline["median_width"],
            "candidate_center_x_delta_px": candidate_geometry["median_center_x"] - group_baseline["median_center_x"],
            "candidate_baseline_delta_px": candidate_geometry["median_baseline"] - group_baseline["median_baseline"],
            "gate": "hard 5% for waving only; informational for special poses",
        })
    overall = "PASS" if reference_files and all(asset["status"] == "PASS" for asset in assets) else "FAIL"
    report = {
        "overall": overall,
        "reference_theme": str(reference_theme.resolve()),
        "candidate_theme": str(candidate_theme.resolve()),
        "asset_count": len(reference_files),
        "extra_candidate_assets": extra_assets,
        "geometry_policy": "5% hard gate against the same asset's interpolated 2.1.3 geometry; waving alone uses 2.1.3 idle height/center/baseline",
        "mode_baselines": baseline,
        "group_report": group_report,
        "assets": assets,
        "contact_sheets": {},
    }
    for mode in ("checker", "dark", "magenta"):
        path = output_dir / f"{mode}-contact-sheet.png"
        write_contact_sheet(path, mode, decoded_assets)
        report["contact_sheets"][mode] = str(path.resolve())
    (output_dir / "validation.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    write_markdown(report, output_dir / "validation.md")
    return report


def save_animation(path: Path, frames: list[Image.Image], durations: list[int]) -> None:
    frames[0].save(
        path,
        save_all=True,
        append_images=frames[1:],
        duration=durations,
        loop=0,
        lossless=True,
        method=6,
        exact=True,
        background=(0, 0, 0, 0),
        minimize_size=False,
        kmin=1,
        kmax=1,
    )


def self_check() -> None:
    with tempfile.TemporaryDirectory(prefix="xuerong-v213-validator-") as temporary:
        root = Path(temporary)
        reference = root / "reference/assets"
        good = root / "good/assets"
        bad = root / "bad/assets"
        reference.mkdir(parents=True)
        good.mkdir(parents=True)
        bad.mkdir(parents=True)

        first = Image.new("RGBA", CANVAS, (0, 0, 0, 0))
        second = Image.new("RGBA", CANVAS, (0, 0, 0, 0))
        ImageDraw.Draw(first).rectangle((200, 300, 299, 449), fill=(230, 240, 255, 255))
        ImageDraw.Draw(second).rectangle((220, 300, 319, 449), fill=(230, 240, 255, 255))
        save_animation(reference / "collapsing.webp", [first, second], [500, 500])
        save_animation(good / "collapsing.webp", [first, second], [500, 500])

        broken = Image.new("RGBA", CANVAS, (0, 0, 0, 0))
        ImageDraw.Draw(broken).rectangle((250, 300, 349, 449), fill=(230, 240, 255, 255))
        save_animation(bad / "collapsing.webp", [first, broken], [500, 500])

        good_report = validate(root / "reference", root / "good", root / "good-output")
        bad_report = validate(root / "reference", root / "bad", root / "bad-output")
        assert good_report["overall"] == "PASS", good_report
        assert bad_report["overall"] == "FAIL", bad_report
    print("self-check=PASS")


def main() -> int:
    args = parse_args()
    if args.self_check:
        self_check()
        return 0
    report = validate(args.reference_theme, args.candidate_theme, args.output_dir)
    print(json.dumps({"overall": report["overall"], "assets": report["asset_count"], "output": str(args.output_dir)}, ensure_ascii=False))
    return 0 if report["overall"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
