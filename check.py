from PIL import Image
import numpy as np, re, sys

bad = 0
for i in range(8):
    a = np.array(Image.open(f"out/panel_{i}.png").convert("L"))
    h, w = a.shape
    mx, my = int(0.20/2.75*w), int(0.20/4.25*h)
    hits = (int((a[:, :mx] < 200).sum()), int((a[:, w-mx:] < 200).sum()),
            int((a[:my, :] < 200).sum()), int((a[h-my:, :] < 200).sum()))
    if any(hits):
        bad += 1; print(f"  panel {i} ink in 0.20in safe zone L/R/T/B: {hits}")
print("SAFE ZONE: clear" if not bad else f"SAFE ZONE: {bad} panel(s) with ink too near the edge")

txtbad = []
for f in ("zine.py", "parts.py"):
    for n, l in enumerate(open(f).read().split("\n"), 1):
        if "—" in l or "·" in l or re.search(r"colour|moulded|armoured|grey|Grey|GREY|centre|anti-clock", l):
            txtbad.append(f"  {f}:{n}")
print("COPY: clean" if not txtbad else "COPY:\n" + "\n".join(txtbad))
