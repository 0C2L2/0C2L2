"""Preprocess a portrait photo for ASCII conversion.

Pipeline:
  1. Remove the background with rembg.
  2. Boost local contrast with OpenCV CLAHE.
  3. Composite onto a pure white background.

Output: assets/source-prepped.png
"""
from __future__ import annotations

import sys

import numpy as np
from PIL import Image, ImageOps

from config import PREPPED_PHOTO, SOURCE_PHOTO

try:
    import cv2
except ImportError:
    cv2 = None


def remove_background(img: Image.Image) -> Image.Image:
    try:
        from rembg import remove
    except ImportError:
        print("rembg not installed; skipping background removal "
              "(pip install rembg)", file=sys.stderr)
        return img.convert("RGBA")
    return remove(img.convert("RGBA"))


def clahe_contrast(rgba: Image.Image) -> Image.Image:
    if cv2 is None:
        print("opencv not installed; using PIL autocontrast instead",
              file=sys.stderr)
        r, g, b, a = rgba.split()
        rgb = ImageOps.autocontrast(Image.merge("RGB", (r, g, b)), cutoff=1)
        return Image.merge("RGBA", (*rgb.split(), a))
    arr = np.array(rgba)
    rgb, alpha = arr[:, :, :3], arr[:, :, 3]
    lab = cv2.cvtColor(rgb, cv2.COLOR_RGB2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
    l = clahe.apply(l)
    rgb = cv2.cvtColor(cv2.merge((l, a, b)), cv2.COLOR_LAB2RGB)
    return Image.fromarray(np.dstack((rgb, alpha)), mode="RGBA")


def composite_white(rgba: Image.Image) -> Image.Image:
    bg = Image.new("RGBA", rgba.size, (255, 255, 255, 255))
    return Image.alpha_composite(bg, rgba).convert("RGB")


def main() -> None:
    if not SOURCE_PHOTO.exists():
        sys.exit(f"Put your photo at {SOURCE_PHOTO} first.")
    img = Image.open(SOURCE_PHOTO)
    img = remove_background(img)
    img = clahe_contrast(img)
    img = composite_white(img)
    PREPPED_PHOTO.parent.mkdir(parents=True, exist_ok=True)
    img.save(PREPPED_PHOTO)
    print(f"wrote {PREPPED_PHOTO}")


if __name__ == "__main__":
    main()
