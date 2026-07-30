# The Bait Station Liberation Guide

An 8-panel black-and-white fold-and-cut mini-zine (one landscape US Letter
sheet) for identifying NYC rat bait stations, matching the right key, and
opening each one. Current version 0.2.8, printed on the cover.

## Build

```
pip install -r requirements.txt   # plus poppler-utils for pdftoppm
./build.sh
```

Outputs:

- `Bait_Station_Field_Guide_PRINT.pdf` — the fold-and-cut sheet.
- `Bait_Station_Field_Guide_READ.pdf` — 8 sequential pages for screen.

`build.sh` also runs the safe-zone/copy checks and decode-tests both QR codes
off a 300 dpi render. A build that fails any of these is not done.

## Print

Print at **100% / Actual Size** (never "fit to page"), single-sided,
landscape. Fold hot dog, then hamburger twice, unfold, cut the heavy center
line, refold into a booklet.

## Editing

All content is generated Python-to-SVG. Read `CLAUDE.md` first; it carries the
accumulated corrections and hard style rules. The panel builders live in
`zine.py`, shared drawing primitives in `parts.py`, imposition in `makepdf.py`.
