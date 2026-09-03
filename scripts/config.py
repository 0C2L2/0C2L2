"""Shared configuration for the profile-art scripts."""
from pathlib import Path

# --- Edit these ---------------------------------------------------------------
GITHUB_USERNAME = "0C2L2"

INFO_CARD = {
    "user_host": "rashid@github",
    "fields": [
        ("Name",     "Rashid Tagaev"),
        ("Role",     "Engineering student"),
        ("Tagline",  "Turning curiosity into code"),
        ("Focus",    "AI / computer vision / full-stack"),
        ("Stack",    "Python / TypeScript / Next.js / R"),
        ("Projects", "face_detect - GymEye - MagicFlow - NemoFlow"),
        ("LinkedIn", "in/rashid-tagaev"),
        ("Badges",   "YOLO - Quickdraw"),
    ],
}

# ASCII portrait
ASCII_COLS = 120            # character width of the rendered portrait
ASCII_GAMMA = 1.0           # >1 darkens, <1 brightens the mapping
# density ramp: sparse -> dense
ASCII_RAMP = " .:-=+*#%@"
# ---------------------------------------------------------------------------

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
ASSETS_DIR = ROOT / "assets"

SOURCE_PHOTO = ASSETS_DIR / "source.png"          # your input photo
PREPPED_PHOTO = ASSETS_DIR / "source-prepped.png" # output of prep_photo.py

ASCII_SVG = ROOT / "avi-ascii.svg"
INFO_CARD_SVG = ROOT / "info-card.svg"
HEATMAP_SVG = ROOT / "contrib-heatmap.svg"
CONTRIB_JSON = DATA_DIR / "contributions.json"
