# The Bait Station Liberation Guide

An 8-panel black-and-white fold-and-cut mini-zine (one landscape US Letter
sheet) for identifying rat bait stations, matching the right key, and opening
each one. Current version 0.4.3, printed on the cover.

**Download and fold instructions: https://shallowdiver.github.io/baitless**

- `Bait_Station_Field_Guide_PRINT.pdf` — the fold-and-cut sheet.
- `Bait_Station_Field_Guide_READ.pdf` — 8 sequential pages for screen.
- `Bait_Station_Field_Guide_NIGHT.pdf` — the same 8 pages in dark mode, gray on
  true black, for reading at night.

In all three PDFs the SCAN THESE rows on the back panel are tappable links,
code and text alike, so a reader on a screen does not have to scan a code off
their own display.

The PDFs are committed to this repo because the site serves them directly.

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
safe-zone and copy checks, writes the PDFs, and decode-tests all three QR
codes off 300 dpi renders of both the print sheet and the night PDF's QR page.
It then cuts every link annotation's own rectangle out of a 300 dpi render of
each PDF and decodes the code inside it, so a link that lands on the wrong row,
or in the wrong cell of the imposed sheet, fails the build. A build that fails
any step is not done.

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

Also covered, on the THREE ODD ONES panel: the B&G Rodent Cafe (a flat
two-prong fork; prongs in, push down hard, push the key toward the back), the
JT Eaton 902 (one hex screw, counterclockwise, part XHEXKEY-G), and the Tomcat,
which has no keyhole at all.

The B&G key is not in the pack, so `BandG_Rodent_Bait_Station_Cafe_Key.stl` is
served alongside the PDFs for anyone with a 3D printer. The key drawings in the
zine are traced off that solid, not drawn by eye.

## License

Do what you like with it. Print it, copy it, hand it out.

### Third-Party Notices

B&G Rodent Bait Station Cafe Key STL courtesy of Thingiverse user [fiveseven808](https://www.thingiverse.com/fiveseven808), who has [it](https://www.thingiverse.com/thing:2980948) licensed under the Creative Commons - Attribution - Non-Commercial license.