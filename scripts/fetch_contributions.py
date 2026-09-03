"""Scrape the public GitHub contribution calendar (no auth / no PAT).

Reads https://github.com/users/<username>/contributions and writes a
normalized calendar to data/contributions.json.
"""
from __future__ import annotations

import json
import sys

import requests
from bs4 import BeautifulSoup

from config import CONTRIB_JSON, GITHUB_USERNAME

URL = "https://github.com/users/{user}/contributions"
HEADERS = {"User-Agent": "profile-art-bot (+https://github.com)"}


def fetch(user: str) -> list[dict]:
    resp = requests.get(URL.format(user=user), headers=HEADERS, timeout=30)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    days: list[dict] = []
    for cell in soup.select("td.ContributionCalendar-day"):
        date = cell.get("data-date")
        if not date:
            continue
        level = int(cell.get("data-level", 0))
        # Newer markup carries the count in a tool-tip element.
        count = 0
        tip = soup.select_one(f'tool-tip[for="{cell.get("id", "")}"]')
        if tip and tip.text:
            head = tip.text.strip().split()[0].replace(",", "")
            count = int(head) if head.isdigit() else 0
        days.append({"date": date, "count": count, "level": level})

    days.sort(key=lambda d: d["date"])
    return days


def main() -> None:
    if GITHUB_USERNAME == "YOUR_USERNAME":
        sys.exit("Set GITHUB_USERNAME in scripts/config.py first.")
    days = fetch(GITHUB_USERNAME)
    if not days:
        sys.exit("No contribution cells parsed — GitHub markup may have changed.")
    payload = {
        "username": GITHUB_USERNAME,
        "total": sum(d["count"] for d in days),
        "days": days,
    }
    CONTRIB_JSON.parent.mkdir(parents=True, exist_ok=True)
    CONTRIB_JSON.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"wrote {CONTRIB_JSON} ({len(days)} days, {payload['total']} total)")


if __name__ == "__main__":
    main()
