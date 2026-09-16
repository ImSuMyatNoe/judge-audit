"""Assemble the deck: template plus the photo and the two QR codes.

    python talk/build.py

Writes two identical files:

  talk/btv-slides.html   the deck you present from
  docs/index.html        the same file, where GitHub Pages serves it

Everything is inlined, so either file works from a USB stick on a laptop that
has never seen this repository. The only thing it fetches is the Google Fonts
stylesheet, and it degrades to Georgia and Helvetica without it.
"""

from __future__ import annotations

import json
import pathlib

HERE = pathlib.Path(__file__).parent
ROOT = HERE.parent


def main() -> int:
    template = (HERE / "_btv_template.html").read_text()
    photo = (HERE / "assets" / "photo.txt").read_text().strip()
    qr = json.loads((HERE / "assets" / "qr.json").read_text())

    marker = '<section class="slide">'
    page = (template
            .replace("{{PHOTO}}", photo)
            .replace("{{QR1}}", qr["portfolio"])
            .replace("{{QR2}}", qr["repo"]))
    if "{{" in page:
        raise SystemExit("a placeholder was left unfilled")

    for out in (HERE / "btv-slides.html", ROOT / "docs" / "index.html"):
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(page)
        print(f"wrote {out.relative_to(ROOT)}  {len(page):,} bytes  "
              f"{page.count(marker)} slides")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
