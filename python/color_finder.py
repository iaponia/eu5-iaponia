#!/usr/bin/env python3
"""Find pixels for a specific RGB color in an image file."""

from __future__ import annotations

import argparse
from pathlib import Path


def parse_rgb_hex(value: str) -> tuple[int, int, int]:
    hex_value = value.strip().lstrip("#")
    if len(hex_value) != 6:
        raise argparse.ArgumentTypeError(
            "Color must be a 6-digit hex RGB value like 1E0F0D"
        )
    try:
        r = int(hex_value[0:2], 16)
        g = int(hex_value[2:4], 16)
        b = int(hex_value[4:6], 16)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            "Color must be a valid hex RGB value like 1E0F0D"
        ) from exc
    return r, g, b


def find_color(image_path: Path, rgb: tuple[int, int, int]) -> None:
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

        rgb_image = image.convert("RGB")
        width, height = rgb_image.size
        pixels = rgb_image.load()
        if pixels is None:
            raise SystemExit("Unable to access pixel data for this image.")

        count = 0
        first_pos: tuple[int, int] | None = None
        sum_x = 0
        sum_y = 0

        for y in range(height):
            for x in range(width):
                if pixels[x, y] == rgb:
                    if first_pos is None:
                        first_pos = (x, y)
                    count += 1
                    sum_x += x
                    sum_y += y

    if count == 0:
        print("0")
        print("first: none")
        print("center: none")
        return

    center_x = sum_x / count
    center_y = sum_y / count

    print(count)
    assert first_pos is not None
    print(f"first: {first_pos[0]} {first_pos[1]}")
    print(f"center: {center_x:.2f} {center_y:.2f}")


def parse_color_args(values: list[str]) -> tuple[int, int, int]:
    if len(values) == 1:
        return parse_rgb_hex(values[0])
    if len(values) == 3:
        try:
            rgb = tuple(int(value) for value in values)
        except ValueError as exc:
            raise argparse.ArgumentTypeError(
                "RGB values must be integers like 255 255 255"
            ) from exc
        if any(channel < 0 or channel > 255 for channel in rgb):
            raise argparse.ArgumentTypeError(
                "RGB values must be between 0 and 255"
            )
        return rgb  # type: ignore[return-value]
    raise argparse.ArgumentTypeError(
        "Provide either one hex RGB value or three integers (R G B)"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Find a specific RGB color in an image."
    )
    parser.add_argument(
        "image",
        type=Path,
        help="Path to the image file (e.g., in_game/map_data/locations.png)",
    )
    parser.add_argument(
        "color",
        nargs="+",
        help="RGB hex like 1E0F0D or #1E0F0D, or three integers like 255 255 255",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    image_path = args.image
    if not image_path.exists():
        raise SystemExit(f"File not found: {image_path}")

    color = parse_color_args(args.color)
    find_color(image_path, color)


if __name__ == "__main__":
    main()
