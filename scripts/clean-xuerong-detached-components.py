#!/usr/bin/env python3
"""Remove detached alpha fragments while preserving timing and nearby details."""

from __future__ import annotations

import argparse
import runpy
from pathlib import Path

from PIL import ImageChops


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--validator-script", type=Path, required=True)
    parser.add_argument("--rebuild-script", type=Path, required=True)
    parser.add_argument("--proximity-px", type=int, default=6)
    parser.add_argument("--mode", choices=("loop", "one-shot"), default="loop")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    validator = runpy.run_path(str(args.validator_script))
    rebuild = runpy.run_path(str(args.rebuild_script))
    frames, durations = rebuild["decode_webp"](args.input)
    cleaned = [validator["remove_detached_components"](frame, args.proximity_px) for frame in frames]
    removed = [
        sum(ImageChops.difference(before.getchannel("A"), after.getchannel("A")).histogram()[1:])
        for before, after in zip(frames, cleaned)
    ]
    rebuild["save_webp"](args.output, cleaned, durations, args.mode)
    print(f"frames={len(cleaned)} duration_ms={sum(durations)} changed_alpha_weight={sum(removed)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
