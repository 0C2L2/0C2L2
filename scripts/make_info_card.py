"""Render a neofetch-style info card as an animated SVG.

Each line fades and slides in with staggered timing.

Output: info-card.svg
"""
from __future__ import annotations

from html import escape

from config import INFO_CARD, INFO_CARD_SVG

BG = "#0d1117"
KEY_FILL = "#58a6ff"
VAL_FILL = "#c9d1d9"
HOST_FILL = "#3fb950"
RULE_FILL = "#30363d"
FONT_SIZE = 13
LINE_H = 20
PAD = 16
STAGGER = 0.09
SLIDE_DUR = 0.4


def build_svg() -> str:
    host = INFO_CARD["user_host"]
    fields = INFO_CARD["fields"]
    key_w = max(len(k) for k, _ in fields)

    rows: list[tuple[str, str, str]] = [("host", host, "")]
    rows.append(("rule", "-" * (key_w + 2 + max(len(v) for _, v in fields)), ""))
    for k, v in fields:
        rows.append(("kv", k, v))

    width = PAD * 2 + int(
        max(len(host), key_w + 2 + max(len(v) for _, v in fields)) * 7.7
    )
    height = PAD * 2 + LINE_H * len(rows)

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" '
        f'height="{height}" viewBox="0 0 {width} {height}" role="img" '
        f'aria-label="Profile info card">',
        f'<rect width="100%" height="100%" rx="8" fill="{BG}"/>',
        '<style>'
        'text{font-family:"SFMono-Regular",Consolas,"Liberation Mono",'
        f'monospace;font-size:{FONT_SIZE}px;white-space:pre;'
        'dominant-baseline:hanging}'
        '</style>',
    ]

    for i, (kind, a, b) in enumerate(rows):
        y = PAD + i * LINE_H
        begin = round(i * STAGGER, 3)
        anim = (
            f'<animate attributeName="opacity" from="0" to="1" '
            f'begin="{begin}s" dur="{SLIDE_DUR}s" fill="freeze"/>'
            f'<animateTransform attributeName="transform" type="translate" '
            f'from="-8 0" to="0 0" begin="{begin}s" dur="{SLIDE_DUR}s" '
            f'fill="freeze" calcMode="spline" '
            f'keySplines="0.2 0.8 0.2 1" keyTimes="0;1"/>'
        )
        if kind == "host":
            body = f'<tspan fill="{HOST_FILL}">{escape(a)}</tspan>'
        elif kind == "rule":
            body = f'<tspan fill="{RULE_FILL}">{escape(a)}</tspan>'
        else:
            pad = " " * (max(len(k) for k, _ in fields) - len(a) + 2)
            body = (f'<tspan fill="{KEY_FILL}">{escape(a)}</tspan>'
                    f'<tspan fill="{VAL_FILL}">{escape(pad + b)}</tspan>')
        parts.append(
            f'<g opacity="0"><text x="{PAD}" y="{y}">{body}</text>{anim}</g>'
        )

    parts.append('</svg>')
    return "\n".join(parts)


def main() -> None:
    INFO_CARD_SVG.write_text(build_svg(), encoding="utf-8")
    print(f"wrote {INFO_CARD_SVG}")


if __name__ == "__main__":
    main()
