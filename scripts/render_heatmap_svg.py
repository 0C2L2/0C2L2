"""Render data/contributions.json as an animated contribution heatmap SVG.

Classic 53-week x 7-day grid with GitHub's green palette and a diagonal
reveal: cells appear in waves along the anti-diagonal (week + day).

Output: contrib-heatmap.svg
"""
from __future__ import annotations

import json
import sys
from datetime import date

from config import CONTRIB_JSON, HEATMAP_SVG

CELL = 11
GAP = 3
PAD = 16
BG = "#0d1117"
EMPTY = "#161b22"
PALETTE = ["#0e4429", "#006d32", "#26a641", "#39d353"]  # levels 1..4
DIAG_STEP = 0.03   # seconds per anti-diagonal
FADE_DUR = 0.35


def load_days() -> list[dict]:
    if not CONTRIB_JSON.exists():
        sys.exit(f"{CONTRIB_JSON} missing — run fetch_contributions.py.")
    return json.loads(CONTRIB_JSON.read_text())["days"]


def build_svg(days: list[dict]) -> str:
    if not days:
        sys.exit("no days to render")

    first = date.fromisoformat(days[0]["date"])
    # column 0 starts on the Sunday on/just before the first day
    start_col_offset = (first.weekday() + 1) % 7  # Mon=0 -> Sun index

    cols: dict[int, int] = {}
    placed: list[tuple[int, int, int]] = []  # week, weekday, level
    for i, d in enumerate(days):
        slot = i + start_col_offset
        week, weekday = divmod(slot, 7)
        placed.append((week, weekday, d.get("level", 0)))
        cols[week] = 1

    weeks = max(cols) + 1
    width = PAD * 2 + weeks * (CELL + GAP) - GAP
    height = PAD * 2 + 7 * (CELL + GAP) - GAP

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" '
        f'height="{height}" viewBox="0 0 {width} {height}" role="img" '
        f'aria-label="GitHub contribution heatmap">',
        f'<rect width="100%" height="100%" fill="{BG}"/>',
    ]

    for week, weekday, level in placed:
        x = PAD + week * (CELL + GAP)
        y = PAD + weekday * (CELL + GAP)
        fill = EMPTY if level <= 0 else PALETTE[min(level, 4) - 1]
        begin = round((week + weekday) * DIAG_STEP, 3)
        parts.append(
            f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="2" '
            f'fill="{fill}" opacity="0">'
            f'<animate attributeName="opacity" from="0" to="1" '
            f'begin="{begin}s" dur="{FADE_DUR}s" fill="freeze"/>'
            f'<animateTransform attributeName="transform" type="scale" '
            f'additive="sum" from="0.4" to="1" begin="{begin}s" '
            f'dur="{FADE_DUR}s" fill="freeze" calcMode="spline" '
            f'keySplines="0.2 0.8 0.2 1" keyTimes="0;1"/>'
            f'</rect>'
        )

    parts.append('</svg>')
    return "\n".join(parts)


def main() -> None:
    HEATMAP_SVG.write_text(build_svg(load_days()), encoding="utf-8")
    print(f"wrote {HEATMAP_SVG}")


if __name__ == "__main__":
    main()
