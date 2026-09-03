"""Convert the prepped photo into an animated ASCII-art SVG.

The portrait is drawn one row of monospace text per <text> element. A
horizontal clip wipe reveals each row in sequence, giving a row-by-row
"typing" effect. A single light-gray fill keeps the result clean.

Output: avi-ascii.svg
"""
from __future__ import annotations

import sys
from html import escape

import numpy as np
from PIL import Image

from config import (
    ASCII_COLS,
    ASCII_GAMMA,
    ASCII_RAMP,
    ASCII_SVG,
    PREPPED_PHOTO,
)

# Monospace cell metrics (px). Typical char aspect ~0.5.
CELL_W = 7.2
CELL_H = 12.0
FONT_SIZE = 12
FILL = "#d0d0d0"
BG = "#0d1117"
ROW_REVEAL = 0.05   # seconds between rows
WIPE_DUR = 0.35     # seconds for a single row wipe


def load_luma(path: Image.Image) -> np.ndarray:
    img = Image.open(path).convert("L")
    w, h = img.size
    rows = max(1, int(ASCII_COLS * (h / w) * (CELL_W / CELL_H)))
    img = img.resize((ASCII_COLS, rows), Image.LANCZOS)
    arr = np.asarray(img, dtype=np.float32) / 255.0
    if ASCII_GAMMA != 1.0:
        arr = np.power(arr, ASCII_GAMMA)
    return arr


def to_ascii(luma: np.ndarray) -> list[str]:
    ramp = ASCII_RAMP
    # dark pixel -> dense glyph (end of ramp)
    idx = np.clip(((1.0 - luma) * (len(ramp) - 1)).round().astype(int),
                  0, len(ramp) - 1)
    return ["".join(ramp[i] for i in row) for row in idx]


def build_svg(lines: list[str]) -> str:
    cols = max((len(l) for l in lines), default=ASCII_COLS)
    width = int(cols * CELL_W) + 16
    height = int(len(lines) * CELL_H) + 16
    parts: list[str] = [
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" '
        f'aria-label="ASCII self-portrait">',
        f'<rect width="100%" height="100%" fill="{BG}"/>',
        f'<style>text{{font-family:"SFMono-Regular",Consolas,'
        f'"Liberation Mono",monospace;font-size:{FONT_SIZE}px;'
        f'fill:{FILL};white-space:pre;dominant-baseline:hanging}}</style>',
        '<defs>',
    ]
    # per-row clip wipes
    for i in range(len(lines)):
        begin = round(i * ROW_REVEAL, 3)
        parts.append(
            f'<clipPath id="w{i}"><rect x="8" y="{8 + i * CELL_H:.1f}" '
            f'height="{CELL_H:.1f}" width="0">'
            f'<animate attributeName="width" from="0" to="{cols * CELL_W:.1f}" '
            f'begin="{begin}s" dur="{WIPE_DUR}s" fill="freeze" '
            f'calcMode="spline" keySplines="0.2 0.8 0.2 1" keyTimes="0;1"/>'
            f'</rect></clipPath>'
        )
    parts.append('</defs>')
    for i, line in enumerate(lines):
        y = 8 + i * CELL_H
        parts.append(
            f'<text x="8" y="{y:.1f}" clip-path="url(#w{i})">'
            f'{escape(line)}</text>'
        )
    parts.append('</svg>')
    return "\n".join(parts)


def main() -> None:
    if not PREPPED_PHOTO.exists():
        sys.exit(f"Run prep_photo.py first ({PREPPED_PHOTO} missing).")
    luma = load_luma(PREPPED_PHOTO)
    lines = to_ascii(luma)
    ASCII_SVG.write_text(build_svg(lines), encoding="utf-8")
    print(f"wrote {ASCII_SVG} ({len(lines)} rows)")


if __name__ == "__main__":
    main()
