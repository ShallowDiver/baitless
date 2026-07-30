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
$PY - <<'EOF'
import cv2, sys
WANT = {"https://shallowdiver.github.io/cityrats/",
        "https://www.nyc.gov/site/dsny/what-we-do/programs/safe-disposal-events.page",
        "https://shallowdiver.github.io/baitless"}
ok, decoded, pts, _ = cv2.QRCodeDetector().detectAndDecodeMulti(cv2.imread('sheet-1.png'))
got = {d for d in (decoded if ok else []) if d}
for u in sorted(WANT):
    print(("  ok   " if u in got else "  MISS ") + u)
extra = got - WANT
if extra:
    print("  UNEXPECTED:", extra)
sys.exit(0 if got == WANT else 1)
EOF
echo "BUILD OK"
