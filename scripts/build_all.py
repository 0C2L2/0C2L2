"""Run the whole pipeline locally.

  python scripts/build_all.py            # everything
  python scripts/build_all.py --no-photo # skip the portrait (no rembg needed)
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def run(name: str) -> None:
    print(f"\n=== {name} ===")
    subprocess.run([sys.executable, str(HERE / name)], check=True, cwd=HERE)


def main() -> None:
    skip_photo = "--no-photo" in sys.argv
    if not skip_photo:
        run("prep_photo.py")
        run("make_ascii_svg.py")
    run("make_info_card.py")
    run("fetch_contributions.py")
    run("render_heatmap_svg.py")
    print("\nAll SVGs written to the repo root.")


if __name__ == "__main__":
    main()
