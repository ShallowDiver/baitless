"""Option sheet for the cover's broken chain. Each row is shown at the size it
will actually print on the cover as well as blown up, because a chain is exactly
the kind of drawing that reads fine at 3x and turns to mud at 1x."""
import cairosvg, os
from parts import *

OPTS = [
    ("A  baseline: 3 a side, burst",        dict()),
    ("B  no burst",                         dict(burst=False)),
    ("C  narrower turned links (rn 5)",     dict(rn=5.0)),
    ("D  4 a side, slightly smaller",       dict(n=4, rx=15, ry=10, rn=6)),
    ("E  wider break, more splay",          dict(gap=40, splay=24, dx=10)),
    ("F  heavier metal (t 5.0)",            dict(t=5.0)),
]

c = f'<rect width="1180" height="{150*len(OPTS)+60}" fill="{WH}"/>' + DEFS
for i, (lab, kw) in enumerate(OPTS):
    y = 92 + i * 150
    c += txt(30, y - 40, lab, 20, "bold")
    c += rule(30, y - 28, 1150, 2)
    # left: 2.6x, to judge the drawing. right: on-cover size, to judge legibility
    c += f'<g transform="translate(340,{y+16}) scale(2.6)">{chain_break(**kw)}</g>'
    c += txt(340, y + 74, "2.6x", 13, "normal", BK, "middle")
    c += f'<g transform="translate(880,{y+16}) scale(1.15)">{chain_break(**kw)}</g>'
    c += txt(880, y + 74, "1.15x, actual cover size", 13, "normal", BK, "middle")

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" '
       f'viewBox="0 0 1180 {150*len(OPTS)+60}">{c}</svg>')
os.makedirs("out", exist_ok=True)
cairosvg.svg2png(bytestring=svg.encode(), write_to="out/chainproof.png",
                 output_width=1400)
print("ok")
