#!/usr/bin/env bash
# Full build + verification. A build that fails any step is not done.
set -euo pipefail
cd "$(dirname "$0")"

PY=python3
[ -x .venv/bin/python ] && PY=.venv/bin/python

$PY zine.py
$PY check.py
$PY makepdf.py

pdftoppm -r 300 -png -f 1 -l 1 Bait_Station_Field_Guide_PRINT.pdf sheet
pdftoppm -r 300 -png -f 8 -l 8 Bait_Station_Field_Guide_READ.pdf read
pdftoppm -r 300 -png -f 8 -l 8 Bait_Station_Field_Guide_NIGHT.pdf night
$PY - <<'EOF'
import cv2, sys
WANT = {"https://shallowdiver.github.io/cityrats/",
        "https://www.nyc.gov/site/dsny/what-we-do/programs/safe-disposal-events.page",
        "https://shallowdiver.github.io/baitless"}
fail = False
# The night page's codes are light-on-dark, which cv2 cannot read directly, so
# invert that image first. Phone scanners handle inverted codes on their own.
for img, invert in (("sheet-1.png", False), ("night-8.png", True)):
    im = cv2.imread(img)
    if invert:
        im = cv2.bitwise_not(im)
    ok, decoded, pts, _ = cv2.QRCodeDetector().detectAndDecodeMulti(im)
    got = {d for d in (decoded if ok else []) if d}
    print(img)
    for u in sorted(WANT):
        print(("  ok   " if u in got else "  MISS ") + u)
    extra = got - WANT
    if extra:
        print("  UNEXPECTED:", extra)
    fail = fail or got != WANT

# Every SCAN THESE row in all THREE pdfs carries an invisible link annotation, so
# a reader on a screen can tap instead of scanning a code off their own display.
# Checking that the annotations merely EXIST would not catch one landing on the
# wrong row or in the wrong cell of the imposed sheet, so each annotation's own
# rectangle is cut out of a 300 dpi render and the code inside it is decoded: the
# link and the code under it have to agree, or the build fails.
import pypdf
DPI = 300
for pdf, page, img, invert in (
        ("Bait_Station_Field_Guide_PRINT.pdf", 0, "sheet-1.png", False),
        ("Bait_Station_Field_Guide_READ.pdf",  7, "read-8.png",  False),
        ("Bait_Station_Field_Guide_NIGHT.pdf", 7, "night-8.png", True)):
    p = pypdf.PdfReader(pdf).pages[page]
    ph = float(p.mediabox.height)
    im = cv2.imread(img)
    if invert:
        im = cv2.bitwise_not(im)
    annots = p.get("/Annots") or []
    print(f"{pdf} page {page+1}: {len(annots)} link(s)")
    if len(annots) != len(WANT):
        fail = True
    for a in annots:
        o = a.get_object()
        url = o["/A"]["/URI"]
        x0, y0, x1, y1 = (float(v) for v in o["/Rect"])
        # The row's link stops at the panel's 36-unit margin, but the code's
        # quiet zone runs 2 modules further left, so the crop is opened by a
        # hair on every side. 14 px at 300 dpi is 0.05 in, far too little to
        # let a link that sat on the wrong row still find its code.
        P = 14
        px = lambda v: max(0, int(v / 72 * DPI))
        c = im[px(ph - y1) - P:px(ph - y0) + P, px(x0) - P:px(x1) + P]
        got_url, _, _ = cv2.QRCodeDetector().detectAndDecode(c)
        ok = got_url == url
        print(("  ok   " if ok else "  BAD  ") + url
              + ("" if ok else f"  -> code under it decoded as {got_url!r}"))
        fail = fail or not ok
sys.exit(1 if fail else 0)
EOF
echo "BUILD OK"
