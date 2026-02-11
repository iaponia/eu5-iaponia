#!/usr/bin/env python3
"""Count unique colors in an image file."""

from __future__ import annotations

import argparse
from pathlib import Path


def count_unique_colors(image_path: Path) -> int:
	try:
		from PIL import Image
	except ImportError as exc:
		raise SystemExit(
			"Pillow is required. Install with: pip install Pillow"
		) from exc

	with Image.open(image_path) as image:
		if "A" in image.getbands() or "transparency" in image.info:
			raise SystemExit(
				"Alpha channel detected. EU5 map PNGs must not have alpha."
			)
		rgb = image.convert("RGB")
		return len(set(rgb.getdata()))


def parse_args() -> argparse.Namespace:
	parser = argparse.ArgumentParser(
		description="Count the number of unique colors in an image."
	)
	parser.add_argument(
		"image",
		type=Path,
		help="Path to the image file (e.g., in_game/map_data/locations.png)",
	)
	return parser.parse_args()


def main() -> None:
	args = parse_args()
	image_path = args.image
	if not image_path.exists():
		raise SystemExit(f"File not found: {image_path}")

	unique_colors = count_unique_colors(image_path)
	print(unique_colors)


if __name__ == "__main__":
	main()
