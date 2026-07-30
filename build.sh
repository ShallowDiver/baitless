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
sys.exit(1 if fail else 0)
EOF
echo "BUILD OK"
