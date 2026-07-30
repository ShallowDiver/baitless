"""Option sheet for the cover's snapped chain.

Each row shows the break cropped and large, which is where every failed attempt
failed, then the whole chain at its real on-cover size. Crops are rendered as
separate images with a ROOT-level viewBox and composited: cairosvg does not clip
nested <svg> viewports, so an inline crop overflows and covers the sheet."""
import cairosvg, io, os
from PIL import Image, ImageDraw, ImageFont
from parts import *

OPTS = [
    ("A  gap 34, splay 2.4", dict(gapdeg=34, splay=2.4)),
    ("B  gap 24, splay 2.0", dict(gapdeg=24, splay=2.0)),
    ("C  gap 18, splay 1.6  barely parted", dict(gapdeg=18, splay=1.6)),
    ("D  gap 24, splay 3.4  sprung open", dict(gapdeg=24, splay=3.4)),
    ("E  gap 24, splay 2.0, heavier metal", dict(gapdeg=24, splay=2.0, t=5.0)),
    ("F  gap 24, splay 2.0, tilt 13", dict(gapdeg=24, splay=2.0, tilt=13)),
]

def render(inner, vb, out_w):
    x, y, w, h = vb
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x} {y} {w} {h}">'
           f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{WH}"/>'
           f'{inner}</svg>')
    buf = io.BytesIO()
    cairosvg.svg2png(bytestring=svg.encode(), write_to=buf,
                     output_width=out_w, output_height=int(out_w * h / w))
    return Image.open(io.BytesIO(buf.getvalue())).convert("RGB")

os.makedirs("out", exist_ok=True)
rows = []
for lab, kw in OPTS:
    bare = dict(kw); bare.update(debris=False, motion=False)
    crop = render(chain_snap(**bare), (-58, -30, 116, 58), 520)   # the break, big
    full = render(chain_snap(**kw), (-115, -46, 230, 92), 300)     # cover size-ish
    big = render(chain_snap(**kw), (-115, -46, 230, 92), 640)
    rows.append((lab, crop, big, full))

PAD, LH = 22, 34
W = PAD * 4 + max(c.width + b.width + f.width for _, c, b, f in rows)
RH = max(max(c.height, b.height, f.height) for _, c, b, f in rows) + LH + PAD
sheet = Image.new("RGB", (W, RH * len(rows)), "white")
d = ImageDraw.Draw(sheet)
fb = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 21)
fs = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 15)
for i, (lab, crop, big, full) in enumerate(rows):
    top = i * RH
    d.line((0, top, W, top), fill="black", width=2)
    d.text((PAD, top + 7), lab, fill="black", font=fb)
    x = PAD
    for im, cap in ((crop, "the break, cropped"), (big, "whole chain"),
                    (full, "actual cover size")):
        sheet.paste(im, (x, top + LH))
        d.text((x, top + LH + im.height + 4), cap, fill="#555", font=fs)
        x += im.width + PAD
sheet.save("out/chainproof.png")
print("ok")
