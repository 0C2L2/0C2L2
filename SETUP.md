# Setup

Animated GitHub profile README built from three self-contained animated SVGs:

| SVG | Source | Animation |
|-----|--------|-----------|
| `avi-ascii.svg` | your photo → monochrome ASCII | row-by-row typing wipe |
| `info-card.svg` | `scripts/config.py` fields | staggered fade + slide-in |
| `contrib-heatmap.svg` | scraped public contribution calendar | diagonal reveal |

## 1. Configure

Edit `scripts/config.py`:

- `GITHUB_USERNAME` — your handle (used for scraping + README).
- `INFO_CARD` — the neofetch-style fields.
- `ASCII_COLS`, `ASCII_GAMMA`, `ASCII_RAMP` — portrait tuning.

Then replace `YOUR_USERNAME` in `README.md` with your handle.

## 2. Add your photo

Drop a portrait at `assets/source.png`. Front-lit, plain-ish background works best.

## 3. Local environment

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r scripts/requirements.txt
pip install rembg          # portrait background removal (heavy, optional)
```

## 4. Build

```bash
python scripts/build_all.py            # full pipeline
python scripts/build_all.py --no-photo # skip the ASCII portrait
```

Individual steps:

```bash
python scripts/prep_photo.py           # assets/source-prepped.png
python scripts/make_ascii_svg.py       # avi-ascii.svg
python scripts/make_info_card.py       # info-card.svg
python scripts/fetch_contributions.py  # data/contributions.json  (no token)
python scripts/render_heatmap_svg.py   # contrib-heatmap.svg
```

Preview the SVGs in a browser to check the animations.

## 5. Publish

```bash
git add -A
git commit -m "feat: animated profile README"
git remote add origin git@github.com:YOUR_USERNAME/YOUR_USERNAME.git
git push -u origin main
```

Create the repo as `YOUR_USERNAME/YOUR_USERNAME` (public) and GitHub renders
`README.md` on your profile page.

## 6. Daily refresh

`.github/workflows/update-profile-art.yml` runs daily (~06:17 UTC), re-scrapes
your contributions, re-renders `contrib-heatmap.svg`, and commits with
`[skip ci]` so it doesn't retrigger itself. Needs no secrets — the calendar is
public HTML. Trigger it manually once from the Actions tab to verify.

CI installs only `scripts/requirements-ci.txt` (`requests` + `beautifulsoup4`) —
the heatmap steps need nothing else. `requirements.txt` is for local work.

## Notes / constraints

- GitHub READMEs strip `<script>`, `style=` attributes, and external CSS.
  All motion must be SMIL (`<animate>`) or a `<style>` block *inside* the SVG.
- If the heatmap ever renders empty, GitHub changed the calendar markup —
  update the selectors in `fetch_contributions.py`.
- The scraper is best-effort and unauthenticated; don't hammer it.
