#!/usr/bin/env python3
"""Create visual QA contact sheets for Xuerong animated WebP assets."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--theme-dir", type=Path, default=Path("themes/xuerong-hd"))
    parser.add_argument("--asset-dir", type=Path, default=Path("build/xuerong-smooth/assets"))
    parser.add_argument("--output-dir", type=Path, default=Path("build/xuerong-smooth/qa"))
    parser.add_argument("--samples", type=int, default=6)
    parser.add_argument("--rows-per-page", type=int, default=6)
    return parser.parse_args()


def decode_frames(path: Path) -> list[Image.Image]:
    image = Image.open(path)
    frames = []
    for index in range(image.n_frames):
        image.seek(index)
        frames.append(image.convert("RGBA").copy())
    return frames


def checkerboard(size: int, tile: int = 16) -> Image.Image:
    image = Image.new("RGBA", (size, size), "white")
    draw = ImageDraw.Draw(image)
    colors = ((224, 239, 248, 255), (244, 249, 252, 255))
    for y in range(0, size, tile):
        for x in range(0, size, tile):
            draw.rectangle((x, y, x + tile - 1, y + tile - 1), fill=colors[(x // tile + y // tile) % 2])
    return image


def sample_indices(frame_count: int, sample_count: int) -> list[int]:
    if sample_count <= 1 or frame_count <= 1:
        return [0]
    return [round(index * (frame_count - 1) / (sample_count - 1)) for index in range(sample_count)]


def main() -> int:
    args = parse_args()
    manifest_path = args.theme_dir / "qa" / "asset-build-v21.json"
    assets = [entry["asset"] for entry in json.loads(manifest_path.read_text(encoding="utf-8"))["assets"]]
    args.output_dir.mkdir(parents=True, exist_ok=True)

    cell_size = 256
    label_height = 30
    row_height = cell_size + label_height
    page_count = math.ceil(len(assets) / args.rows_per_page)
    font = ImageFont.load_default()
    outputs = []

    for page_index in range(page_count):
        page_assets = assets[
            page_index * args.rows_per_page:(page_index + 1) * args.rows_per_page
        ]
        page = Image.new(
            "RGB",
            (cell_size * args.samples, row_height * len(page_assets)),
            "white",
        )
        draw = ImageDraw.Draw(page)
        for row_index, asset in enumerate(page_assets):
            frames = decode_frames(args.asset_dir / asset)
            indices = sample_indices(len(frames), args.samples)
            y = row_index * row_height
            draw.text((8, y + 9), f"{asset} | {len(frames)} frames", fill="black", font=font)
            for column, frame_index in enumerate(indices):
                background = checkerboard(cell_size)
                frame = frames[frame_index]
                background.alpha_composite(frame.resize((cell_size, cell_size), Image.Resampling.LANCZOS))
                page.paste(background.convert("RGB"), (column * cell_size, y + label_height))
        output = args.output_dir / f"contact-sheet-{page_index + 1:02d}.png"
        page.save(output)
        outputs.append(output.name)

    (args.output_dir / "contact-sheets.json").write_text(
        json.dumps({"ok": True, "assets": len(assets), "pages": outputs}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print("\n".join(outputs))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
