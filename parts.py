"""B&W zine primitives. Key geometry is patent-sourced:
   Protecta 2-prong  US5448852A  (two flat tabs at 90 deg to each other)
   Protecta EVO      US8793929B1 (two prongs of DIFFERING cross section)
   Aegis             US6082042A  (oval cam, twisted)
   VM / EZ-Klean     US9637950B2 (hollow socket + 2 notched ears, drops over a post)
"""
import math

W, H = 600, 928
BK, WH = "#000000", "#ffffff"
GY1, GY2, GY3 = "#d6d6d6", "#a8a8a8", "#6b6b6b"   # light / mid / dark gray
F = "DejaVu Sans"

DEFS = ('<defs>'
        '<pattern id="hatch" width="9" height="9" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
        f'<rect width="9" height="9" fill="{WH}"/><rect width="3.3" height="9" fill="{BK}"/></pattern>'
        '<pattern id="hatchL" width="13" height="13" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
        f'<rect width="13" height="13" fill="{WH}"/><rect width="2.4" height="13" fill="{BK}"/></pattern>'
        '<pattern id="dots" width="9" height="9" patternUnits="userSpaceOnUse">'
        f'<rect width="9" height="9" fill="{WH}"/><circle cx="4.5" cy="4.5" r="1.6" fill="{BK}"/></pattern>'
        '</defs>')
HATCH, HATCHL, DOTS = "url(#hatch)", "url(#hatchL)", "url(#dots)"

_uid = [0]
def uid():
    _uid[0] += 1
    return f"c{_uid[0]}"

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def txt(x, y, s, size=22, w="normal", fill=BK, anchor="start", spacing=None):
    sp = f' letter-spacing="{spacing}"' if spacing else ""
    return (f'<text x="{x}" y="{y}" font-family="{F}" font-size="{size}" font-weight="{w}" '
            f'fill="{fill}" text-anchor="{anchor}"{sp}>{esc(s)}</text>')

def lines(x, y, rows, size=22, lh=None, w="normal", fill=BK, anchor="start"):
    lh = lh or int(size * 1.32)
    return "".join(txt(x, y + i * lh, r, size, w, fill, anchor) for i, r in enumerate(rows))

def rule(x1, y, x2, sw=3, color=BK):
    return f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{color}" stroke-width="{sw}"/>'

# ------------------------------------------------------------------- arrows
def arrow(x1, y1, x2, y2, color=BK, w=6, head=13):
    a = math.atan2(y2 - y1, x2 - x1)
    bx, by = x2 - head * 0.85 * math.cos(a), y2 - head * 0.85 * math.sin(a)
    hx, hy = x2 - head * math.cos(a), y2 - head * math.sin(a)
    ox, oy = head * 0.60 * math.sin(a), head * 0.60 * math.cos(a)
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{bx:.1f}" y2="{by:.1f}" stroke="{color}" '
            f'stroke-width="{w}" stroke-linecap="round"/>'
            f'<path d="M {x2:.1f} {y2:.1f} L {hx+ox:.1f} {hy-oy:.1f} L {hx-ox:.1f} {hy+oy:.1f} Z" fill="{color}"/>')

def arc_arrow(cx, cy, r, a0, a1, color=BK, w=6, head=13):
    r0, r1 = math.radians(a0), math.radians(a1)
    x0, y0 = cx + r * math.cos(r0), cy + r * math.sin(r0)
    x1, y1 = cx + r * math.cos(r1), cy + r * math.sin(r1)
    sweep = 1 if a1 > a0 else 0
    large = 1 if abs(a1 - a0) > 180 else 0
    tan = r1 + (math.pi / 2 if a1 > a0 else -math.pi / 2)
    return (f'<path d="M {x0:.1f} {y0:.1f} A {r} {r} 0 {large} {sweep} {x1:.1f} {y1:.1f}" '
            f'stroke="{color}" stroke-width="{w}" fill="none" stroke-linecap="round"/>'
            + arrow(x1, y1, x1 + head * math.cos(tan), y1 + head * math.sin(tan), color, w, head))

# --------------------------------------------------------- motion icons r=24
def _disc():
    return f'<circle cx="0" cy="0" r="23" fill="{WH}" stroke="{BK}" stroke-width="3"/>'

def ic_press():
    return _disc() + f'<rect x="-15" y="11" width="30" height="5" fill="{BK}"/>' + arrow(0, -16, 0, 6, BK, 5.5, 12)

def ic_push_in():
    return _disc() + f'<rect x="11" y="-15" width="5" height="30" fill="{BK}"/>' + arrow(-16, 0, 6, 0, BK, 5.5, 12)

def ic_drop_over():                 # the ring drops down over the post
    return (_disc() + f'<rect x="-2.5" y="-2" width="5" height="17" fill="{BK}"/>'
            + f'<rect x="-15" y="14" width="30" height="4" fill="{BK}"/>'
            + f'<ellipse cx="0" cy="-6" rx="14" ry="5" fill="none" stroke="{BK}" stroke-width="3.5"/>'
            + arrow(-17, -18, -17, 2, BK, 4, 9))

def ic_lever():
    return (_disc() + f'<rect x="-16" y="9" width="32" height="5" fill="{BK}"/>'
            + f'<circle cx="-6" cy="9" r="3.5" fill="{BK}"/>'
            + f'<line x1="-6" y1="9" x2="-6" y2="-13" stroke="{BK}" stroke-width="4.5" stroke-linecap="round"/>'
            + arrow(-1, -13, 14, -6, BK, 5, 11))

def ic_turn():
    return _disc() + arc_arrow(0, 0, 12.5, 200, 20, BK, 5, 12) + f'<circle cx="0" cy="0" r="3" fill="{BK}"/>'

def ic_turn_arrow():
    return _disc() + arc_arrow(0, 1, 11.5, 195, 15, BK, 5, 11) + arrow(-15, 16, 4, 16, BK, 3.5, 8)

def ic_pull_back():
    return _disc() + f'<rect x="-16" y="-15" width="5" height="30" fill="{BK}"/>' + arrow(15, 0, -5, 0, BK, 5.5, 12)

def ic_lift():
    return _disc() + f'<rect x="-15" y="-15" width="30" height="5" fill="{BK}"/>' + arrow(0, 16, -0, -5, BK, 5.5, 12)

def ic_repeat():
    return _disc() + arc_arrow(0, 0, 13, 120, 400, BK, 4.5, 10) + txt(0, 6, "2", 17, "bold", BK, "middle")

def ic_snap():
    return (_disc() + f'<rect x="-15" y="9" width="30" height="5" fill="{BK}"/>'
            + arrow(-8, -15, -8, 3, BK, 5, 11) + arrow(8, -15, 8, 3, BK, 5, 11))

def ic_hex():
    pts = [(11 * math.cos(math.radians(a)), 11 * math.sin(math.radians(a))) for a in range(0, 360, 60)]
    return (_disc() + '<path d="M ' + ' L '.join(f'{p[0]:.1f} {p[1]:.1f}' for p in pts)
            + f' Z" fill="none" stroke="{BK}" stroke-width="3.5"/>'
            + arc_arrow(0, 0, 18, 30, -150, BK, 4, 10))

def ic_hand():
    return (_disc() + f'<rect x="-13" y="-2" width="26" height="16" rx="6" fill="none" stroke="{BK}" stroke-width="3"/>'
            + f'<rect x="-9" y="-14" width="5" height="14" rx="2.5" fill="{BK}"/>'
            + f'<rect x="-1" y="-17" width="5" height="17" rx="2.5" fill="{BK}"/>'
            + f'<rect x="7" y="-13" width="5" height="13" rx="2.5" fill="{BK}"/>')

def icon(fn, x, y, s=1.0):
    return f'<g transform="translate({x},{y}) scale({s})">{fn()}</g>'

# =============================================== KEY END VIEWS  (the cross-section)
def end_lp():
    """Two flat tabs at 90 DEGREES to each other, set well apart , not stacked."""
    return (f'<rect x="-24" y="-19" width="17" height="7" rx="2" fill="{BK}"/>'
            f'<rect x="12" y="7" width="7" height="17" rx="2" fill="{BK}"/>')

def end_evo():
    """Not separate fins, one continuous ribbon folded into a rounded square wave."""
    a, verts = 13, (-24, -12, 0, 12, 24)
    y = a                                   # start at the BOTTOM
    d = f"M {verts[0]} {y}"
    for i, x in enumerate(verts):
        if i:
            d += f" L {x} {y}"              # across
        y = -y
        d += f" L {x} {y}"                  # up or down
    return (f'<path d="{d}" stroke="{BK}" stroke-width="5" fill="none" '
            f'stroke-linecap="round" stroke-linejoin="round"/>')

def end_aegis():
    """A plain flattened oval. No slot."""
    return f'<ellipse cx="0" cy="0" rx="26" ry="14" fill="{BK}"/>'

VM_X, VM_H, VM_SW, VM_GAP, VM_TILT = 9.0, 4.4, 4.25, 15.0, -9
# VM_H is the outer half-height. Thinning it brings the two congruent legs closer
# together. Do NOT thin VM_X, that is the taper axis. VM_GAP is the prong spacing
# and is correct as it stands.

def _vm_prong(k=1.0):
    """Soft trapezoid, nearly a rectangle. Wide end outward, pointier end inward."""
    x, h, hi, sw = VM_X * k, VM_H * k, VM_H * 0.7 * k, VM_SW * k
    return (f'<path d="M {-x:.2f} {-h:.2f} L {x:.2f} {-hi:.2f} L {x:.2f} {hi:.2f} '
            f'L {-x:.2f} {h:.2f} Z" fill="{BK}" stroke="{BK}" '
            f'stroke-width="{sw:.2f}" stroke-linejoin="round"/>')

def vm_pair(k=1.0):
    """The SAME prong twice, turned 180 deg about the axis. Rotational, not mirror.
       Both pointier ends aim nearly (not exactly) inward, which is the giveaway."""
    tp = _vm_prong(k); g = VM_GAP * k
    return (f'<g transform="translate({-g:.2f},0) rotate({VM_TILT})">{tp}</g>'
            f'<g transform="rotate(180) translate({-g:.2f},0) rotate({VM_TILT})">{tp}</g>')

def end_vm():
    return vm_pair()

def end_hex():
    pts = [(20 * math.cos(math.radians(a)), 20 * math.sin(math.radians(a))) for a in range(0, 360, 60)]
    return '<path d="M ' + ' L '.join(f'{p[0]:.1f} {p[1]:.1f}' for p in pts) + f' Z" fill="{BK}"/>'

# ================================================ HOLE DETAILS (seen on the box)
def hole_lp():
    return end_lp()

def hole_evo():
    """The wiggly opening, with the U-shaped locating ledge molded beneath it."""
    return (end_evo()
            + f'<path d="M -22 24 Q 0 35 22 24" fill="none" stroke="{BK}" stroke-width="4"/>')

def hole_aegis():
    """A lozenge with a central circle that bulges just past it, their union."""
    return (f'<rect x="-26" y="-9" width="52" height="18" rx="9" fill="{BK}"/>'
            f'<circle cx="0" cy="0" r="14" fill="{BK}"/>')

def hole_vm():
    return end_vm()

def hole_none():
    return (f'<rect x="-13" y="-14" width="26" height="28" rx="5" fill="none" stroke="{BK}" stroke-width="3"/>'
            + arrow(-30, 0, -17, 0, BK, 4.5, 10) + arrow(30, 0, 17, 0, BK, 4.5, 10))

def detail(cx, cy, r, fn, dashed=False):
    dash = ' stroke-dasharray="8 6"' if dashed else ''
    s = r / 34.0
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{WH}"/>'
            f'<g transform="translate({cx},{cy}) scale({s})">{fn()}</g>'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{BK}" stroke-width="4"{dash}/>')

# ==================== KEY SIDE VIEWS , traced from photographs of the real keys
def side_lp():
    """BRASS flat metal. Rounded head + ring hole, flared foot, forked legs
       whose tips are formed at 90 degrees to one another."""
    g = (f'<path d="M -34 34 A 34 34 0 0 1 34 34 L 34 148 L 66 180 L 66 250 '
         f'L 30 250 L 30 234 L 19 234 L 19 208 A 19 19 0 0 0 -19 208 L -19 234 '
         f'L -30 234 L -30 250 L -66 250 L -66 180 L -34 148 Z" '
         f'fill="{GY1}" stroke="{BK}" stroke-width="4" stroke-linejoin="round"/>')
    g += f'<circle cx="0" cy="36" r="15" fill="{WH}" stroke="{BK}" stroke-width="4"/>'
    return g

def side_evo():
    """BLACK plastic. Arched head + oval hole. The business end is ONE corrugated
       piece with a wavy edge , it only reads as separate fins."""
    g = (f'<path d="M -74 76 A 74 76 0 0 1 74 76 L 74 166 L -74 166 Z" '
         f'fill="{GY3}" stroke="{BK}" stroke-width="4" stroke-linejoin="round"/>')
    g += (f'<rect x="-30" y="26" width="60" height="34" rx="17" '
          f'fill="{WH}" stroke="{BK}" stroke-width="4"/>')
    wav = "M -90 232 Q -78 250 -66 232 Q -54 214 -42 232 Q -30 250 -18 232 " \
          "Q -6 214 6 232 Q 18 250 30 232 Q 42 214 54 232 Q 66 250 78 232 Q 84 224 90 230"
    g += (f'<path d="M -90 166 L 90 166 L 90 230 {wav[1:].replace("M ", "L ", 1)} L -90 232 Z" '
          f'fill="{GY3}" stroke="{BK}" stroke-width="4" stroke-linejoin="round"/>')
    for x in (-45, 0, 45):
        g += f'<path d="M {x} 172 L {x} 226" stroke="{BK}" stroke-width="3.5" fill="none"/>'
    return g

def side_aegis():
    """BLACK plastic. Nub on top, ribbed shield with a big oval grip hole,
       then a round collar and a plain oval working tip."""
    g = (f'<path d="M -12 -28 L 12 -28 L 16 6 L -16 6 Z" '
         f'fill="{GY3}" stroke="{BK}" stroke-width="4" stroke-linejoin="round"/>')
    g += (f'<path d="M 0 4 L 78 44 L 86 150 L 40 206 L -40 206 L -86 150 L -78 44 Z" '
          f'fill="{GY3}" stroke="{BK}" stroke-width="4" stroke-linejoin="round"/>')
    for i in range(5):
        g += (f'<rect x="-62" y="{62 + i*22}" width="58" height="11" rx="5" '
              f'fill="{GY1}" stroke="{BK}" stroke-width="3"/>')
    g += (f'<ellipse cx="42" cy="118" rx="27" ry="54" fill="{WH}" '
          f'stroke="{BK}" stroke-width="4"/>')
    g += (f'<rect x="-27" y="202" width="54" height="44" rx="16" '
          f'fill="{GY3}" stroke="{BK}" stroke-width="4"/>')
    g += (f'<ellipse cx="0" cy="268" rx="20" ry="26" '
          f'fill="{GY3}" stroke="{BK}" stroke-width="4"/>')
    return g

def side_vm():
    """GRAY plastic. Oval fob with a grip slot and a side boss, then two prongs.
       They are the SAME prong twice, turned 180 degrees about the axis."""
    g = (f'<ellipse cx="0" cy="76" rx="98" ry="76" fill="{GY2}" '
         f'stroke="{BK}" stroke-width="4"/>')
    g += (f'<rect x="-38" y="16" width="76" height="40" rx="18" '
          f'fill="{WH}" stroke="{BK}" stroke-width="4"/>')
    g += f'<circle cx="-62" cy="92" r="17" fill="{GY1}" stroke="{BK}" stroke-width="4"/>'
    g += (f'<rect x="-84" y="146" width="168" height="24" rx="6" '
          f'fill="{GY2}" stroke="{BK}" stroke-width="4"/>')
    g += (f'<rect x="-74" y="166" width="54" height="112" rx="6" '
          f'fill="{GY2}" stroke="{BK}" stroke-width="4"/>')
    g += (f'<rect x="-60" y="188" width="22" height="56" rx="10" '
          f'fill="{WH}" stroke="{BK}" stroke-width="4"/>')
    g += (f'<rect x="20" y="166" width="54" height="112" rx="6" '
          f'fill="{GY2}" stroke="{BK}" stroke-width="4"/>')
    g += (f'<rect x="38" y="200" width="22" height="56" rx="10" '
          f'fill="{WH}" stroke="{BK}" stroke-width="4"/>')
    return g

def qr(x, y, size, data, border=2):
    """QR drawn as SVG rects. Keep `size` generous: modules want ~0.5mm on paper."""
    import qrcode
    q = qrcode.QRCode(border=border, box_size=1,
                      error_correction=qrcode.constants.ERROR_CORRECT_L)
    q.add_data(data); q.make(fit=True)
    m = q.get_matrix(); n = len(m); cell = size / n
    out = f'<rect x="{x}" y="{y}" width="{size}" height="{size}" fill="{WH}"/>'
    for r in range(n):
        c = 0
        while c < n:
            if m[r][c]:
                c0 = c
                while c < n and m[r][c]:
                    c += 1
                out += (f'<rect x="{x + c0*cell:.2f}" y="{y + r*cell:.2f}" '
                        f'width="{(c-c0)*cell:.2f}" height="{cell:.2f}" fill="{BK}"/>')
            else:
                c += 1
    return out

def poison():
    """Skull and crossbones, drawn about 76 units wide, centered on the origin."""
    g = '<g transform="translate(0,14)">'
    for ang in (38, -38):
        g += (f'<g transform="rotate({ang})">'
              f'<rect x="-28" y="-4.5" width="56" height="9" rx="4.5" fill="{BK}"/>'
              f'<circle cx="-28" cy="-6" r="6.5" fill="{BK}"/>'
              f'<circle cx="-28" cy="6" r="6.5" fill="{BK}"/>'
              f'<circle cx="28" cy="-6" r="6.5" fill="{BK}"/>'
              f'<circle cx="28" cy="6" r="6.5" fill="{BK}"/></g>')
    g += "</g>"
    g += f'<path d="M -12 4 L 12 4 L 10 20 L -10 20 Z" fill="{BK}"/>'
    g += f'<ellipse cx="0" cy="-8" rx="20" ry="21" fill="{BK}"/>'
    g += f'<ellipse cx="-7.5" cy="-10" rx="6" ry="7.5" fill="{WH}"/>'
    g += f'<ellipse cx="7.5" cy="-10" rx="6" ry="7.5" fill="{WH}"/>'
    g += f'<path d="M 0 0 L 4.5 9 L -4.5 9 Z" fill="{WH}"/>'
    g += (f'<path d="M -5.5 12 L -5.5 20 M 0 12 L 0 20 M 5.5 12 L 5.5 20" '
          f'stroke="{WH}" stroke-width="2.4"/>')
    return g

# ==================================================== BROKEN CHAIN (cover art)
def _link(cx, cy, rx, ry, t, hw=2.6):
    """One chain link, as a STROKED ellipse rather than a filled ring. That is the
       whole trick: the white underlay is the same ellipse stroked wider, so it
       follows the ring's contour and notches a neighbor only where this link's
       metal actually crosses it. A solid white ellipse underlay instead eats the
       previous link's far side and the row reads as a line of C shapes.
       hw is how far the notch extends past the metal on each side; keep it small,
       around 2 to 3 units, or the notch swallows the whole end of the link."""
    e = f'<ellipse cx="{cx:.2f}" cy="{cy:.2f}" rx="{rx:.2f}" ry="{ry:.2f}" fill="none"'
    g = f'{e} stroke="{WH}" stroke-width="{t+2*hw:.2f}"/>' if hw else ""
    return g + f'{e} stroke="{BK}" stroke-width="{t:.2f}"/>'

def _arc(cx, cy, rx, ry, a0, a1, t, hw=0):
    """A thick elliptical arc, sampled as a polyline so there is no large/sweep
       flag arithmetic to get wrong."""
    n = max(10, int(abs(a1 - a0) / 5))
    pts = [(cx + rx * math.cos(math.radians(a0 + (a1-a0)*i/n)),
            cy + ry * math.sin(math.radians(a0 + (a1-a0)*i/n))) for i in range(n+1)]
    d = "M " + " L ".join(f"{x:.2f} {y:.2f}" for x, y in pts)
    g = (f'<path d="{d}" fill="none" stroke="{WH}" stroke-width="{t+2*hw}" '
         f'stroke-linecap="round"/>') if hw else ""
    return g + (f'<path d="{d}" fill="none" stroke="{BK}" stroke-width="{t}" '
                f'stroke-linecap="round" stroke-linejoin="round"/>')

def chain_break(n=3, rx=16, ry=10.5, rn=6.5, t=4.2, pitch=26, gap=32,
                alt=True, burst=True, splay=16, dx=6, hw=0):
    """A chain snapped in the middle, running horizontally, origin AT the break.
       Alternating wide and narrow ellipses is how a chain reads flat: a link
       turned 90 degrees about the chain axis keeps its length but loses almost
       all its height.

       hw defaults to 0, meaning NO white notch where links cross, and that is
       deliberate. Notching was tried at 2.2, 2.6 and 3.0 and every value cuts the
       links open into a row of C shapes, because near its end an ellipse runs
       nearly vertical, so even a narrow notch sweeps a wide bite out of the
       neighbor. Letting the strokes simply cross reads as interlocked, and the
       wide/narrow alternation carries the depth on its own."""
    g = ""
    for side in (-1, 1):
        for i in range(n - 1, -1, -1):     # far link first, so nearer ones sit over it
            cx = side * (gap / 2 + rx + i * pitch)
            g += _link(cx, 0, rx, (ry if i % 2 == 0 else rn) if alt else ry, t, hw)
    for side in (-1, 1):                   # the snapped link, two halves bent apart
        a0, a1 = (90, 270) if side < 0 else (-90, 90)
        g += (f'<g transform="translate({side*dx},0) rotate({side*splay})">'
              f'{_arc(0, 0, rx, ry, a0, a1, t, hw)}</g>')
    if burst:
        for a in (-52, 52, 128, -128):
            ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
            g += (f'<line x1="{7*ca:.1f}" y1="{7*sa:.1f}" x2="{15*ca:.1f}" '
                  f'y2="{15*sa:.1f}" stroke="{BK}" stroke-width="2.8" '
                  f'stroke-linecap="round"/>')
    return g

def _stadium(cx, cy, a, b, t):
    """A chain link as a stadium ring: a rounded-rect outline whose end radius is
       its own half-height, stroked. Reads as a loop with a visible hole, which a
       thin ellipse does not once the hole closes up at print size."""
    f = max(a - b, 0.1)
    d = (f"M {cx-f:.2f} {cy-b:.2f} L {cx+f:.2f} {cy-b:.2f} "
         f"A {b:.2f} {b:.2f} 0 0 1 {cx+f:.2f} {cy+b:.2f} "
         f"L {cx-f:.2f} {cy+b:.2f} "
         f"A {b:.2f} {b:.2f} 0 0 1 {cx-f:.2f} {cy-b:.2f} Z")
    return (f'<path d="{d}" fill="none" stroke="{BK}" stroke-width="{t:.2f}" '
            f'stroke-linejoin="round"/>')

def _torn(cx, cy, a, b, t, opens=1, gapdeg=34, splay=2.4):
    """The one link that failed. A stadium that keeps MOST of its loop and gaps only
       at the tip on the break side, the two cut ends splayed apart.

       Removing a whole end cap, which is what the first versions did, leaves 60
       percent of a loop and reads as a bracket or a horseshoe, not as a broken
       link. Here the gap spans only +/-gapdeg about the outer tip, so the eye still
       completes the loop and sees it as torn open.

       Drawn canonically with the gap facing RIGHT, then mirrored by transform for
       opens=-1, which avoids the arc-sweep and cap-direction sign errors that made
       every earlier attempt fold back on itself. `opens` must point AT the break:
       a half sitting right of the break opens LEFT, so opens = -side."""
    f = max(a - b, 0.1)
    n = 13
    P = []
    for i in range(n + 1):                       # upper cut tip, up over the near cap
        ang = math.radians(-gapdeg - (90 - gapdeg) * i / n)
        P.append((f + b * math.cos(ang), b * math.sin(ang)))
    P.append((-f, -b))                           # straight run along the top
    for i in range(2 * n + 1):                   # far cap, bulging away from the break
        ang = math.radians(-90 - 180 * i / (2 * n))
        P.append((-f + b * math.cos(ang), b * math.sin(ang)))
    P.append((f, b))                             # straight run back along the bottom
    for i in range(n + 1):                       # down the near cap to the lower tip
        ang = math.radians(90 - (90 - gapdeg) * i / n)
        P.append((f + b * math.cos(ang), b * math.sin(ang)))
    # splay the two cut ends apart, and tear them to unequal lengths
    P[0] = (P[0][0] + splay * 0.7, P[0][1] - splay)
    P[-1] = (P[-1][0] + splay * 0.4, P[-1][1] + splay * 0.65)
    d = "M " + " L ".join(f"{x:.2f} {y:.2f}" for x, y in P)
    g = (f'<path d="{d}" fill="none" stroke="{BK}" stroke-width="{t:.2f}" '
         f'stroke-linecap="round" stroke-linejoin="round"/>')
    mir = "" if opens > 0 else " scale(-1,1)"
    return f'<g transform="translate({cx},{cy}){mir}">{g}</g>'

# Shrapnel around the break, mostly thrown upward as in a real snap. Hardcoded
# rather than random so every build draws it identically.
# (dx, dy, size, rotation) relative to the break.
_SHARDS = [(-5, -19, 2.4, 18), (4, -24, 1.9, -32), (12, -16, 2.2, 44),
           (-13, -13, 1.8, -12), (18, -8, 1.7, 25), (-19, -5, 1.5, 60),
           (7, -10, 1.4, -50), (22, -19, 1.6, 10), (-2, 11, 1.9, 30),
           (11, 15, 1.5, -20), (-11, 13, 1.4, 55)]

def _shard(x, y, s, rot):
    p = [(-s, -s*0.78), (s*0.9, -s), (s, s*0.85), (-s*0.85, s)]
    d = "M " + " L ".join(f"{u:.2f} {v:.2f}" for u, v in p) + " Z"
    return f'<g transform="translate({x},{y}) rotate({rot})"><path d="{d}" fill="{BK}"/></g>'

def chain_snap(n=3, a=17, b=12, bt=8.5, t=4.2, pitch=24, gap=26, tilt=10,
               alt=True, debris=True, motion=True, broke=-1,
               gapdeg=24, splay=2.0):
    """A chain snapped in the middle. The two halves TILT APART about the break,
       which is what makes it read as broken under tension rather than as a chain
       with a gap in it. tilt>0 puts the break at the PEAK, halves falling away to
       either side; tilt<0 sags into a V, which reads as slack, not snapped.

       Links are stadium rings, and the narrower ones (bt) stay tall enough to keep
       an open hole. A link squashed to a slit reads as a bead, which is what
       killed the first attempt. Links simply CROSS with no white notch at the
       crossing, see drawing rule 7.

       ONLY ONE link breaks, on the side given by `broke`. A real chain fails at a
       single link in a single place; tearing open the end link of BOTH halves reads
       as two unrelated broken chains laid end to end. The other half simply ends in
       an intact link, the one the failed link used to pass through."""
    g = ""
    for side in (-1, 1):
        seg = ""
        for i in range(n - 1, 0, -1):               # full links, far to near
            cx = side * (gap / 2 + a + i * pitch)
            seg += _stadium(cx, 0, a, (b if i % 2 == 0 else bt) if alt else b, t)
        cx = side * (gap / 2 + a)                   # the innermost link
        seg += (_torn(cx, 0, a, b, t, -side, gapdeg, splay) if side == broke
                else _stadium(cx, 0, a, b, t))
        g += f'<g transform="rotate({side * tilt})">{seg}</g>'
    if motion:                                       # short speed ticks off the break
        for dx, dy in ((-14, -24), (1, -28), (15, -23)):
            g += (f'<line x1="{dx*0.66:.1f}" y1="{dy*0.66:.1f}" x2="{dx:.1f}" '
                  f'y2="{dy:.1f}" stroke="{BK}" stroke-width="2.0" '
                  f'stroke-linecap="round"/>')
    if debris:
        g += "".join(_shard(*s) for s in _SHARDS)
    return g

def place(fn, x, y, s=1.0, rot=0):
    r = f' rotate({rot})' if rot else ''
    return f'<g transform="translate({x},{y}) scale({s}){r}">{fn()}</g>'
