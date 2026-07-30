# The Bait Station Liberation Guide

An 8-panel black-and-white fold-and-cut mini-zine (one landscape US Letter
sheet) for identifying rat bait stations, matching the right key, and opening
each one. Current version 0.3.1, printed on the cover.

**Download and fold instructions: https://shallowdiver.github.io/baitless**

- `Bait_Station_Field_Guide_PRINT.pdf` — the fold-and-cut sheet.
- `Bait_Station_Field_Guide_READ.pdf` — 8 sequential pages for screen.

Both PDFs are committed to this repo because the site serves them directly.

## Print

Print at **100% / Actual Size** (never "fit to page"), single-sided,
landscape. Fold hot dog, then hamburger twice, unfold, cut the heavy center
line, refold into a booklet. Where a printed line and a crease disagree,
follow the crease.

## Build

```
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
./build.sh
```

`pdftoppm` comes from poppler-utils. `build.sh` renders the panels, runs the
safe-zone and copy checks, writes both PDFs, and decode-tests all three QR
codes off a 300 dpi render of the print sheet. A build that fails any step is
not done.

## Layout

All content is generated Python-to-SVG. Panel builders live in `zine.py`,
shared drawing primitives in `parts.py`, imposition in `makepdf.py`, checks in
`check.py`. A panel is 600 x 928 units = 2.75 x 4.25 in.

The PDFs are vector end to end: the eight panels are nested into one sheet SVG
and rendered once, so type is embedded and searchable and the QR modules land on
the printer's device grid rather than being resampled from a bitmap. The print
sheet is about 56 KB.

## The four keys it covers

| Key | Color | Motion |
|---|---|---|
| Protecta 2-prong | brass | push down, lever the key away from the box |
| Protecta EVO | black | push straight in, no turn |
| Aegis | black | in narrow-way, then twist |
| VM / EZ-Klean | gray | press down hard, turn 90 deg toward the arrow, pull back |

They sell as one cheap pack online. Search "bait station keys."

Also covered: JT Eaton 902 (one hex screw, counterclockwise, part XHEXKEY-G)
and the Tomcat, which has no keyhole at all.

## License

Do what you like with it. Print it, copy it, hand it out.
