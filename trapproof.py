import cairosvg
from parts import BK, WH, txt, DEFS

def pair(h, sw, x=9, gap=15, tilt=-9):
    """h = outer half-height, inner half-height is 0.7h. Taper axis (x) unchanged."""
    tp = (f'<path d="M {-x} {-h} L {x} {-h*0.7:.1f} L {x} {h*0.7:.1f} L {-x} {h} Z" '
          f'fill="{BK}" stroke="{BK}" stroke-width="{sw}" stroke-linejoin="round"/>')
    return (f'<g transform="translate({-gap},0) rotate({tilt})">{tp}</g>'
            f'<g transform="rotate(180) translate({-gap},0) rotate({tilt})">{tp}</g>')

def disc(cx, cy, r, inner, dashed=True):
    d = ' stroke-dasharray="8 6"' if dashed else ''
    s = r / 34.0
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{WH}"/>'
            f'<g transform="translate({cx},{cy}) scale({s})">{inner}</g>'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{BK}" stroke-width="4"{d}/>')

OPTS = [("A  (current)", 10, 6.0),
        ("B", 8.0, 5.5),
        ("C", 6.5, 5.0),
        ("D", 5.0, 4.5),
        ("E", 3.8, 4.0)]

c = f'<rect width="1240" height="560" fill="{WH}"/>' + DEFS
c += txt(40, 48, "EZ-K / VM END VIEW  thinning options", 26, "bold")
c += txt(40, 76, "taper axis and prong spacing unchanged; only the two congruent legs move closer together", 16)

for i, (lab, h, sw) in enumerate(OPTS):
    cx = 140 + i * 230
    c += disc(cx, 210, 100, pair(h, sw))
    c += txt(cx, 348, lab, 22, "bold", BK, "middle")
    c += txt(cx, 372, f"h={h}  stroke={sw}", 15, "normal", BK, "middle")
    # actual size as printed on the cover (r=40) and in the key band (r=30)
    c += disc(cx - 34, 452, 40, pair(h, sw))
    c += disc(cx + 42, 452, 30, pair(h, sw))
    c += txt(cx, 520, "actual print size", 14, "normal", BK, "middle")

svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1240 560">{c}</svg>'
cairosvg.svg2png(bytestring=svg.encode(), write_to="out/trapproof.png", output_width=1550)
print("ok")
