#!/usr/bin/env bash
# Full build + verification. A build that fails any step is not done.
set -euo pipefail
cd "$(dirname "$0")"

python3 zine.py
python3 check.py
python3 makepdf.py

pdftoppm -r 300 -png -f 1 -l 1 Bait_Station_Field_Guide_PRINT.pdf sheet
python3 - <<'EOF'
import cv2, sys
ok, decoded, pts, _ = cv2.QRCodeDetector().detectAndDecodeMulti(cv2.imread('sheet-1.png'))
decoded = [d for d in (decoded if ok else []) if d]
print("QR:", decoded)
sys.exit(0 if len(decoded) == 2 else 1)
EOF
echo "BUILD OK"
