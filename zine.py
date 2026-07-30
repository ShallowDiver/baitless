"""NYC rat bait station zine, black and white. Panel = 600 x 928 (2.75 x 4.25 in)."""
import math, os
from parts import *

SAFE = 0.94   # shrink panel content about its center so nothing lands in the
              # printer's unprintable margin or gets lost in a slightly off fold

def wrap(c, bg=WH):
    """Panel content in panel units, with the SAFE shrink applied about the
       center. Deliberately NOT an <svg> element: makepdf.py nests eight of these
       in one sheet SVG to impose the print sheet as vector, and a bare group is
       what can carry the needed translate/scale/rotate. Use document() for a
       standalone file. DEFS is emitted by the container, not per panel, so eight
       nested copies cannot collide on pattern ids."""
    return (f'<rect width="{W}" height="{H}" fill="{bg}"/>'
            f'<g transform="translate({W/2},{H/2}) scale({SAFE}) '
            f'translate({-W/2},{-H/2})">{c}</g>')

def document(inner, size=None):
    """One panel as a standalone SVG file."""
    dim = f' width="{size[0]}" height="{size[1]}"' if size else ''
    return (f'<svg xmlns="http://www.w3.org/2000/svg"{dim} '
            f'viewBox="0 0 {W} {H}">{DEFS}{inner}</svg>')

def rpoly(pts, r=16):
    n = len(pts); d = ""
    for i in range(n):
        p0, p1, p2 = pts[(i - 1) % n], pts[i], pts[(i + 1) % n]
        v1 = (p0[0] - p1[0], p0[1] - p1[1]); v2 = (p2[0] - p1[0], p2[1] - p1[1])
        l1 = math.hypot(*v1) or 1; l2 = math.hypot(*v2) or 1
        u1 = (v1[0] / l1, v1[1] / l1); u2 = (v2[0] / l2, v2[1] / l2)
        rr = min(r, l1 / 2.2, l2 / 2.2)
        a = (p1[0] + u1[0] * rr, p1[1] + u1[1] * rr)
        b = (p1[0] + u2[0] * rr, p1[1] + u2[1] * rr)
        d += ("M " if i == 0 else "L ") + f"{a[0]:.1f} {a[1]:.1f} "
        d += f"Q {p1[0]:.1f} {p1[1]:.1f} {b[0]:.1f} {b[1]:.1f} "
    return d + "Z"

def prism(pathd, off, n=22, face=WH, band=GY1, sw=4):
    """Swept solid: hatched side band, white near face, heavy outline."""
    cid = uid()
    clip = f'<clipPath id="{cid}">'
    for i in range(n, 0, -1):
        t = i / n
        clip += f'<path d="{pathd}" transform="translate({off[0]*t:.2f},{off[1]*t:.2f})"/>'
    clip += f'<path d="{pathd}"/></clipPath>'
    g = clip + f'<g clip-path="url(#{cid})"><rect x="-600" y="-600" width="2400" height="2400" fill="{band}"/></g>'
    g += f'<path d="{pathd}" transform="translate({off[0]},{off[1]})" fill="none" stroke="{BK}" stroke-width="{sw}"/>'
    g += f'<path d="{pathd}" fill="{face}" stroke="{BK}" stroke-width="{sw}"/>'
    return g

def archp(w, h):
    r = w / 2
    return f'M {-r} {h} L {-r} {r} Q {-r} 0 0 0 Q {r} 0 {r} {r} L {r} {h} Z'

def entry(cx, cy, w, h, skew=0):
    sk = f' skewY({skew})' if skew else ''
    return f'<g transform="translate({cx},{cy}){sk}"><path d="{archp(w,h)}" fill="{BK}"/></g>'

def ring(x, y, rx, ry=None, dash=True):
    ry = ry or rx
    d = ' stroke-dasharray="9 7"' if dash else ''
    return (f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="none" stroke="{BK}" '
            f'stroke-width="3.5"{d}/>')

def fit(bb, ah, zone_x=48, zone_w=288, art_y=124, pad=26):
    bw = bb[2] - bb[0]; bh = bb[3] - bb[1]
    sc = min(zone_w / bw, (ah - pad) / bh)
    return (zone_x + (zone_w - bw * sc) / 2 - bb[0] * sc,
            art_y + (ah - bh * sc) / 2 - bb[1] * sc, sc)

def callout(px, py, lx, ly, text, size=18, bold=False):
    return (f'<path d="M {px} {py} L {lx} {ly}" stroke="{BK}" stroke-width="2.5" fill="none"/>'
            + txt(lx + 10, ly + 6, text, size, "bold" if bold else "normal"))

def ring_pt(cx, cy, rx, ry, tx, ty, pad=4):
    """The point on a dashed ring (plus a little air) toward a label, so callout
       lines stop AT the ring instead of stabbing through to the keyhole."""
    dx, dy = tx - cx, ty - cy
    t = 1 / math.hypot(dx / (rx + pad), dy / (ry + pad))
    return cx + dx * t, cy + dy * t

def box(x, y, w, h, fill=WH, sw=3):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" '
            f'stroke="{BK}" stroke-width="{sw}"/>')

def header(no, title, sub, tsize=38):
    return (box(36, 32, 54, 54, WH, 4)
            + txt(63, 72, no, 32, "bold", BK, "middle")
            + txt(106, 60, title, tsize, "bold", BK, "start", "0.5")
            + txt(106, 92, sub, 20, "normal")
            + rule(36, 110, W - 36, 5))

def chip(x, y, s):
    w = int(11.8 * len(s)) + 28
    return box(x, y, w, 34, WH, 3) + txt(x + w / 2, y + 23, s, 18, "bold", BK, "middle"), w

ROW1, ROW2 = 50, 74
def rows_h(steps):
    return sum(ROW1 if len(b) == 1 else ROW2 for _, b in steps)

def icon_steps(x, y, steps, size=21):
    out = ""; cy = y
    for i, (fn, body) in enumerate(steps):
        rh = ROW1 if len(body) == 1 else ROW2
        mid = cy + rh / 2 - 3
        out += f'<circle cx="{x+4}" cy="{mid}" r="12" fill="{WH}" stroke="{BK}" stroke-width="3"/>'
        out += txt(x + 4, mid + 6, str(i + 1), 16, "bold", BK, "middle")
        out += icon(fn, x + 46, mid, 0.90)
        out += lines(x + 80, mid - 13 * (len(body) - 1) + 7, body, size, 26)
        cy += rh
    return out

# ================================================================== STATIONS
def face(pts, fill, sw=4):
    d = "M " + " L ".join(f"{p[0]:.1f} {p[1]:.1f}" for p in pts) + " Z"
    return (f'<path d="{d}" fill="{fill}" stroke="{BK}" stroke-width="{sw}" '
            f'stroke-linejoin="round"/>')

def band(chain, off, fill, sw=4):
    """A face swept off one edge-chain of the front polygon."""
    return face(list(chain) + [(p[0] + off[0], p[1] + off[1]) for p in reversed(chain)], fill, sw)

# PROTECTA LP , 13" back edge x 9" deep x 3-3/8" tall. Lid LIFTS OFF.
LP = [(20, 40), (410, 40), (215, 176)]
LP_DZ = 56
LP_A = math.degrees(math.atan2(136, 195))

def _lpy(x, left=True):
    return 40 + (x - 20) / 195 * 136 if left else 176 - (x - 215) / 195 * 136

def lp_entry(x, left=True):
    """Arched mouse-hole entry: semicircle top, sides extending straight down to
       the wall's bottom edge. Sheared so the base rides the sloped end wall."""
    a = math.radians(LP_A if left else -LP_A)
    ca, sa = math.cos(a), math.sin(a)
    yb = _lpy(x, left) + LP_DZ
    return (f'<g transform="translate({x},{yb:.1f}) matrix({ca:.3f},{sa:.3f},0,1,0,0)">'
            f'<path d="{archp(40, 42)}" transform="translate(0,-42)" fill="{BK}"/></g>')

def lp_lock(x, y, rot=0):
    """One lock = two slots set at 90 degrees to one another. Wider sides face
       OUTWARD: the implied vertex of the two slots points INTO the station."""
    g = (f'<rect x="-40" y="-26" width="28" height="10" rx="3" fill="{BK}"/>'
         f'<rect x="14" y="4" width="10" height="28" rx="3" fill="{BK}"/>')
    return f'<g transform="translate({x},{y}) rotate({rot})">{g}</g>'

def st_lp():
    g  = band([(20, 40), (215, 176)], (0, LP_DZ), GY2)        # left end wall
    g += band([(215, 176), (410, 40)], (0, LP_DZ), GY1)       # right end wall
    g += face(LP, WH)                                          # lid, on top
    g += lp_entry(104) + lp_entry(326, False)
    g += lp_lock(126, 88) + lp_lock(284, 88, -90)
    g += ring(118, 92, 48, 42) + ring(276, 92, 48, 42)
    return g

# PROTECTA EVO EXPRESS , hinged cover, floor-level entries front and back,
# two prong-holes in the SIDE of the cover.
EVO_FRONT = [(0, 186), (0, 72), (26, 30), (84, 10), (306, 10), (364, 30), (390, 72), (390, 186)]
EVO_OFF = (100, -112)
def st_evo():
    g  = band(EVO_FRONT[1:7], EVO_OFF, GY1)                             # cover top
    g += band([(390, 72), (390, 186)], EVO_OFF, GY2)                    # right end
    g += face(EVO_FRONT, WH)
    g += (f'<path d="M 4 68 L 30 34 L 86 15 L 304 15 L 360 34 L 386 68" '
          f'stroke="{BK}" stroke-width="3.5" fill="none"/>')             # cover seam
    # entries sit in the END walls: one below the keyhole on this end, its twin
    # in the hidden opposite end. The keyhole end is opposite the hinge end.
    g += (f'<g transform="translate(420,152.4) matrix(0.666,-0.746,0,1,0,0)">'
          f'<path d="{archp(36, 40)}" transform="translate(0,-40)" fill="{BK}"/></g>')
    ang = math.degrees(math.atan2(EVO_OFF[1], EVO_OFF[0]))
    g += (f'<g transform="translate(438,60) rotate({ang:.1f}) scale(0.85)">'
          f'{end_evo()}</g>')                                   # wiggly keyhole slot
    g += ring(438, 60, 36, 42)
    return g

# AEGIS RP , 12-7/8 x 7-7/8 x 4 in CLOSED. Trapezoidal seen from the top, wider
# at the back. Hinge at the rear. TWO lock slots on TOP, one left, one right.
# Each slot is a lozenge with a central circle bulging just past it (their union).
# Parallel side walls at the back (the tunnel entries sit in these, opposite each
# other, near the rear), then long front chamfers give the trapezoid read.
AEG_TOP = [(30, 56), (56, 30), (364, 30), (390, 56),
           (390, 170), (300, 262), (120, 262), (30, 170)]
AEG_OFF = (66, 36)   # oblique sweep so the right side wall is wide enough for its entry

def aeg_slot(x, y):
    return (f'<g transform="translate({x},{y})">'
            f'<rect x="-26" y="-8" width="52" height="16" rx="8" fill="{BK}"/>'
            f'<circle cx="0" cy="0" r="13" fill="{BK}"/></g>')

def st_aegis():
    g  = band([AEG_TOP[3], AEG_TOP[4]], AEG_OFF, GY2)                   # right side wall
    g += band(AEG_TOP[4:7], AEG_OFF, GY1)   # front wall; left chamfer faces away
    g += face(AEG_TOP, WH)                                              # the lid
    g += (f'<path d="M 60 46 L 360 46" stroke="{BK}" stroke-width="3.5" '
          'fill="none"/>')                                              # rear hinge line
    # arched entry in the right side wall near the BACK; its twin sits in the
    # hidden left wall, directly opposite. Base on the floor edge.
    g += (f'<g transform="translate(456,126) matrix(0,1,0.878,0.479,0,0)">'
          f'<path d="{archp(38, 44)}" transform="translate(0,-44)" fill="{BK}"/></g>')
    g += aeg_slot(135, 170) + aeg_slot(275, 170)
    g += ring(135, 170, 42, 26) + ring(275, 170, 42, 26)
    return g

# EZ-KLEAN , 12.5 x 8.75 x 3.25 in. D-SHAPED from the top: a straight front
# edge, one big rounded arc around the back. Two lid slots + a molded arrow.
EZK_OFF = (66, 38)   # oblique sweep so the right SIDE wall is wide enough for its entry
# The back of the D is slightly FLATTENED at the crown, not a pure arc.
EZD_FACE = ('M 34 292 L 34 228 C 34 130 90 66 150 64 L 268 64 '
            'C 328 66 384 130 384 228 L 384 292 Z')
EZK_SHOULDER = [(311.5, 76.7), (348.5, 110.0), (374.3, 161.3),
                (384, 228), (384, 292)]   # curve points down the right shoulder + side
def ezk_slots(x, y, s=2.1):
    """Same prong pair as the key end view, so the hole and the key always agree."""
    return f'<g transform="translate({x},{y}) scale({s})">{vm_pair()}</g>'

def st_ezk():
    g  = band(EZK_SHOULDER, EZK_OFF, GY2)                   # right shoulder + side wall
    g += band([(384, 292), (34, 292)], EZK_OFF, GY1)        # front wall
    g += (f'<path d="{EZD_FACE}" fill="{WH}" stroke="{BK}" stroke-width="4" '
          f'stroke-linejoin="round"/>')                      # the D-shaped lid
    # arched entry in the right SIDE wall; its twin sits in the hidden left wall,
    # directly opposite. Base on the floor edge, sides riding the sweep.
    g += (f'<g transform="translate(450,296) matrix(0,1,0.866,0.499,0,0)">'
          f'<path d="{archp(40, 46)}" transform="translate(0,-46)" fill="{BK}"/></g>')
    g += (f'<path d="M 66 280 L 352 280" stroke="{BK}" stroke-width="3" '
          'stroke-dasharray="6 5" fill="none"/>')            # raised lip
    g += ezk_slots(209, 126)                    # up near the flattened crown
    g += ring(209, 126, 92, 50)
    g += arc_arrow(209, 224, 46, 205, 25, BK, 6, 15)
    return g

# JT EATON 902 , a TALL VERTICAL station. Twist-off cap, one hex screw.
JTE_BODY = [(0, 330), (0, 78), (168, 78), (168, 330)]
JTE_CAP  = [(30, 78), (30, 0), (138, 0), (138, 78)]
JTE_OFF = (52, -42)
def st_jte():
    g  = band([(0, 78), (168, 78)], JTE_OFF, GY1)                       # body top surface
    g += band([(168, 78), (168, 330)], JTE_OFF, GY2)                    # body right wall
    g += face(JTE_BODY, WH)
    g += band([(30, 0), (138, 0)], JTE_OFF, GY1)                        # cap top
    g += band([(138, 0), (138, 78)], JTE_OFF, GY2)                      # cap right wall
    g += face(JTE_CAP, WH)
    g += f'<circle cx="84" cy="38" r="14" fill="{BK}"/>'
    g += f'<circle cx="84" cy="38" r="5.5" fill="{WH}"/>'
    g += entry(40, 254, 44, 52)
    g += ring(84, 38, 30)
    return g

# TOMCAT , roughly square, living hinge, window, NO KEYHOLE.
TOM_FRONT = [(0, 160), (0, 66), (40, 22), (250, 22), (290, 66), (290, 160)]
TOM_OFF = (108, -114)
def st_tomcat():
    g  = band(TOM_FRONT[1:5], TOM_OFF, GY1)
    g += band([(290, 66), (290, 160)], TOM_OFF, GY2)
    g += face(TOM_FRONT, WH)
    g += f'<path d="M 5 69 L 42 27 L 248 27 L 285 69" stroke="{BK}" stroke-width="3.5" fill="none"/>'
    g += (f'<rect x="112" y="84" width="80" height="36" rx="6" fill="{GY1}" '
          f'stroke="{BK}" stroke-width="3.5"/>')
    g += entry(42, 106, 40, 54)
    return g

# ====================================================================== RAT
def rat(x, y, s=1.0, flip=False):
    sx = -s if flip else s
    body = ("M 10 46 C 6 6 62 -16 120 -14 C 174 -12 208 12 228 36 "
            "C 233 43 229 50 220 51 C 202 53 182 56 162 62 "
            "C 122 76 60 78 32 69 C 14 63 10 55 10 46 Z")
    g = (f'<path d="M 12 52 C -34 68 -78 52 -96 22 C -104 8 -100 -8 -86 -12" '
         f'stroke="{BK}" stroke-width="9" fill="none" stroke-linecap="round"/>')
    g += f'<circle cx="128" cy="-6" r="24" fill="{BK}"/>'
    g += f'<path d="{body}" fill="{BK}"/>'
    g += f'<rect x="62" y="64" width="17" height="22" rx="8" fill="{BK}"/>'
    g += f'<rect x="116" y="60" width="17" height="22" rx="8" fill="{BK}"/>'
    g += f'<circle cx="192" cy="30" r="6" fill="{WH}"/>'
    g += f'<circle cx="128" cy="-6" r="11" fill="{WH}"/>'
    g += (f'<path d="M 219 45 L 252 35 M 219 49 L 252 54" stroke="{BK}" '
          'stroke-width="2.6" stroke-linecap="round"/>')
    return f'<g transform="translate({x},{y}) scale({sx},{s})">{g}</g>'

# ==================================================================== PANELS
# The cover's snapped chain: settings and placement. It lives in the clear band
# below the station and left of the rat, at the rat's own height so the two read
# as a pair. Kept as constants so chainproof.py can sweep them without editing
# p_cover(). See drawing rule 7 before changing how links are drawn.
CHAIN = dict(tilt=12, gapdeg=30, splay=2.4, t=4.6, bt=9.0)
CHAIN_AT = (182, 385, 1.15)
# Hard-wrapped against real DejaVu Sans metrics at size 17: widest line 521 of
# the 528 units between the 36-unit margins. Rewrap, never shrink.
WHY = ["NYC and most cities use an excruciating class of poisons",
       "called anticoagulants to kill rats and mice slowly, over days",
       "or weeks of internal bleeding. The poison is deadly to the",
       "rats and mice themselves, and often to the animals who eat",
       "them. For all that suffering, it lowers the number of rodents",
       "only a little, because the population is capped mainly by",
       "territory and food, not by poison. Killing the adults only gives",
       "the survivors room to breed, so it may even mean more very",
       "young rats, fighting and starving over the same scraps.",
       "These stations are a blight on any city that uses them.",
       "If you can legally remove one, do."]

def p_cover():
    c = box(34, 34, W - 68, 172, BK, 0)
    c += txt(W / 2, 108, "THE BAIT STATION", 42, "bold", WH, "middle", "1")
    c += txt(W / 2, 160, "LIBERATION GUIDE", 38, "bold", WH, "middle", "1")
    c += f'<g transform="translate(86,216) scale(0.52)">{st_lp()}</g>'
    c += f'<g transform="translate(424,296) scale(0.85)">{poison()}</g>'
    c += rat(380, 372, 0.52)
    # Snapped chain in the clear band under the station and left of the rat.
    c += (f'<g transform="translate({CHAIN_AT[0]},{CHAIN_AT[1]}) '
          f'scale({CHAIN_AT[2]})">{chain_snap(**CHAIN)}</g>')
    c += rule(56, 434, W - 56, 4)
    c += txt(W / 2, 462, "ONE, TWO, THREE, FOUR...", 22, "bold", BK, "middle", "2")
    for i, ef in enumerate([end_lp, end_evo, end_aegis, end_vm]):
        cx = 108 + i * 128
        c += detail(cx, 520, 36, ef)
    c += rule(56, 572, W - 56, 4)
    c += lines(36, 618, WHY, 17, 22)   # no header, the paragraph stands alone
    c += txt(W / 2, 892, "guide version 0.3.3", 14, "normal", BK, "middle")
    return wrap(c)

MATCH = [(side_lp, end_lp, "PROTECTA LP",
          ["the 2-prong key: flat BRASS",
           "fork, tips at 90 degrees",
           "to each other"]),
         (side_evo, end_evo, "PROTECTA EVO",
          ["the EVO key: BLACK arched tab.",
           "The end is one WIGGLY ribbon,",
           "not separate fins"]),
         (side_aegis, end_aegis, "AEGIS RP",
          ["the Aegis key: BLACK, ribbed.",
           "The big oval is a GRIP hole.",
           "The tip is a plain oval."]),
         (side_vm, end_vm, "EZ-KLEAN",
          ["the VM key: GRAY fob. The same",
           "prong twice, turned 180 deg.",
           "Not a mirror image"])]

def p_keys():
    c = header("1", "LOOK DOWN THE KEY", "side and end view of each", 35)
    c += txt(86, 156, "SIDE", 17, "bold", BK, "middle", "1")
    c += txt(208, 156, "END VIEW", 17, "bold", BK, "middle", "1")
    c += rule(36, 170, W - 36, 3)
    for i, (sf, ef, name, note) in enumerate(MATCH):
        cy = 248 + i * 156
        if i:
            c += rule(36, cy - 78, W - 36, 1.5)
        c += place(sf, 86, cy - 56, 0.44)
        c += detail(208, cy, 44, ef)
        c += txt(272, cy - 12, name, 20, "bold")
        c += lines(272, cy + 16, note, 17, 22)
    c += rule(36, 796, W - 36, 4)
    c += txt(W / 2, 842, "All four keys sell as one cheap pack online.", 18, "normal", BK, "middle")
    c += txt(W / 2, 872, 'Search "bait station keys".', 18, "bold", BK, "middle")
    return wrap(c)

def station_panel(no, title, sub, art_fn, chips, spot, hole_fn, key_fn, key_name, key_sub,
                  steps, shut, banner=None):
    bh = 60 if banner else 0
    AH = min(250, 436 - rows_h(steps) - bh)
    ab = 124 + AH
    band = ab + 56
    after = band + 92 + bh
    spot_lbl = after + 34
    spot0 = spot_lbl + 30
    r1 = spot0 + 26 + 16
    open_lbl = r1 + 32
    st0 = open_lbl + 16
    c = header(no, title, sub)
    c += box(36, 124, W - 72, AH)
    c += art_fn(AH)
    tx = 36
    for t in chips:
        sv, tw = chip(tx, ab + 12, t); c += sv; tx += tw + 10
    if banner:
        c += box(36, band + 100, W - 72, 52, WH, 3)
        c += txt(W / 2, band + 122, banner[0], 19, "bold", BK, "middle")
        c += txt(W / 2, band + 143, banner[1], 16, "normal", BK, "middle")
    c += box(36, band, W - 72, 92)
    c += detail(92, band + 38, 30, hole_fn, dashed=True)
    c += txt(92, band + 84, "the hole", 15, "normal", BK, "middle")
    c += arrow(134, band + 40, 172, band + 40, BK, 5, 12)
    c += place(key_fn, 214, band + 6, 0.28)
    c += txt(270, band + 40, key_name, 20, "bold")
    c += txt(270, band + 64, key_sub, 17, "normal")
    c += txt(36, spot_lbl, "SPOT IT", 22, "bold", BK, "start", "1")
    c += lines(36, spot0, spot, 20, 26)
    c += rule(36, r1, W - 36, 3)
    c += txt(36, open_lbl, "OPEN IT", 22, "bold", BK, "start", "1")
    c += icon_steps(38, st0, steps)
    c += icon(ic_snap, 52, 890, 0.58)
    c += txt(78, 897, shut, 18, "bold")
    return wrap(c)

LP_BB  = (20, 40, 410, 232)
EVO_BB = (0, -62, 502, 186)
AEG_BB = (30, 30, 456, 300)
EZK_BB = (30, 60, 452, 332)

def p_lp():
    def art(ah):
        ox, oy, s = fit(LP_BB, ah)
        y1, y2 = 124 + ah * 0.26, 124 + ah * 0.74
        g = f'<g transform="translate({ox},{oy}) scale({s})">{st_lp()}</g>'
        px, py = ring_pt(ox + 276 * s, oy + 92 * s, 48 * s, 42 * s, 348, y1)
        g += callout(px, py, 348, y1, "TWO locks", 19, True)
        g += lines(358, y1 + 24, ["each a PAIR of slots,", "so four holes in all"], 17, 22)
        g += callout(ox + 326 * s, oy + (_lpy(326, False) + 30) * s, 348, y2, "2-in entries", 18)
        g += txt(358, y2 + 24, "one at each end", 16, "normal")
        return g
    return station_panel(
        "2", "PROTECTA LP", "Bell Labs, 13 x 9 x 3⅜ in", art,
        ["flat triangle", "lid LIFTS OFF"],
        ["The flat triangle that tucks along a wall. Two locks on",
         "the top face, four slots in all. The lid lifts clean off."],
        hole_lp, side_lp, "The 2-prong key", "BRASS, tips at 90 deg",
        [(ic_press, ["Tabs face the INSIDE edge.", "Push straight down, firm."]),
         (ic_lever, ["Tip the key top AWAY from the", "box. That lock lets go."]),
         (ic_repeat, ["Now the second lock."]),
         (ic_lift, ["Lift the lid straight off."])],
        "Shut: press both sides till they CLICK.")

def p_evo():
    def art(ah):
        ox, oy, s = fit(EVO_BB, ah)
        y1, y2 = 124 + ah * 0.26, 124 + ah * 0.76
        g = f'<g transform="translate({ox},{oy}) scale({s})">{st_evo()}</g>'
        kx, ky = ring_pt(ox + 438 * s, oy + 60 * s, 36 * s, 42 * s, 344, y1)
        g += callout(kx, ky, 344, y1, "wiggly keyhole", 19, True)
        g += lines(354, y1 + 24, ["in the SIDE of the lid,", "with a little U-shaped",
                                  "ledge molded below."], 17, 22)
        g += callout(ox + 424 * s, oy + 145 * s, 344, y2, "floor-level entry", 18)
        g += txt(354, y2 + 24, "one at each end", 16, "normal")
        return g
    return station_panel(
        "3", "PROTECTA EVO", "Express, the heavy armored one", art,
        ["hinged cover", "very heavy"],
        ["Chunky rounded shell with a hinged cover. It hides a",
         "concrete block, so it is heavy for its size."],
        hole_evo, side_evo, "The EVO key", "BLACK tab, wiggly end",
        [(ic_push_in, ["Match the pattern and push it", "straight IN. No turning at all."]),
         (ic_lift, ["The cover usually pops itself. If", "not, lever it with the key."])],
        "Shut: press both sides till it SNAPS.")

def p_aegis():
    def art(ah):
        ox, oy, s = fit(AEG_BB, ah)
        y1, y2 = 124 + ah * 0.30, 124 + ah * 0.76
        g = f'<g transform="translate({ox},{oy}) scale({s})">{st_aegis()}</g>'
        g += callout(ox + 443 * s, oy + 118 * s, 344, y1, "tunnel entries", 18)
        g += txt(354, y1 + 24, "one at each end", 16, "normal")
        px, py = ring_pt(ox + 275 * s, oy + 170 * s, 42 * s, 26 * s, 344, y2)
        g += callout(px, py, 344, y2, "TWO slots, on TOP", 19, True)
        g += lines(354, y2 + 24, ["the oval goes in", "narrow-way, then twists"], 17, 22)
        return g
    return station_panel(
        "4", "AEGIS RP", "Liphatech, 12⅞ x 7⅞ x 4 in", art,
        ["low box", "hinge at back"],
        ["A low box, wider at the back and only 4 inches tall.",
         "The lid is hinged and opens away from the wall."],
        hole_aegis, side_aegis, "The Aegis key", "BLACK, plain oval tip",
        [(ic_push_in, ["Slide the oval in narrow-way."]),
         (ic_turn, ["TWIST it. The oval spreads four", "spring flanges and frees the lid."]),
         (ic_repeat, ["Now the second lock."]),
         (ic_lift, ["Swing the lid up and back."])],
        "Shut: drop the lid, press till it clicks.")

def p_ezk():
    def art(ah):
        ox, oy, s = fit(EZK_BB, ah)
        y1, y2 = 124 + ah * 0.24, 124 + ah * 0.72
        g = f'<g transform="translate({ox},{oy}) scale({s})">{st_ezk()}</g>'
        px, py = ring_pt(ox + 209 * s, oy + 126 * s, 92 * s, 50 * s, 344, y1)
        g += callout(px, py, 344, y1, "TWO slots, on TOP", 18, True)
        g += lines(354, y1 + 24, ["the SAME slot twice,", "turned round 180 deg"], 17, 22)
        g += callout(ox + 246 * s, oy + 228 * s, 344, y2, "molded arrow", 18)
        g += txt(354, y2 + 24, "turn the way it points", 16, "normal")
        return g
    return station_panel(
        "5", "EZ-KLEAN", "VM Products, 12½ x 8¾ x 3¼ in", art,
        ["flattest one", "raised front lip"],
        ["The flattest box out here. One arched entry on",
         "each side, set opposite each other."],
        hole_vm, side_vm, "The VM key", "gray fob, twin prongs",
        [(ic_press, ["Both prongs into the two slots.", "Press down HARD and hold."]),
         (ic_turn_arrow, ["Turn it 90 degrees, the way the", "molded arrow beside it points."]),
         (ic_pull_back, ["Tug it toward the BACK, then lift."])],
        "Shut: press both sides till it clicks.",
        banner=("ROTATIONAL, NOT MIRROR.",
                "Turn the key 180 degrees and it still drops in."))

def p_others():
    c = header("6", "TWO ODD ONES", "neither takes a key off your ring")
    c += box(36, 124, W - 72, 292)
    c += f'<g transform="translate(74,148) scale(0.58)">{st_jte()}</g>'
    c += txt(232, 178, "JT EATON 902", 22, "bold")
    c += lines(232, 208, ["It STANDS UP. Everything",
                          "else here lies flat, so that",
                          "alone tells you what it is.",
                          "",
                          "Bait hangs on a rod inside",
                          "the tube. Two entries, low",
                          "down, one on each side."], 17, 23)
    c += detail(516, 172, 32, end_hex, dashed=True)
    c += txt(516, 216, "hex socket", 15, "normal", BK, "middle")
    c += box(36, 430, W - 72, 74, WH, 3)
    c += icon(ic_hex, 80, 467, 0.76)
    c += txt(118, 458, "ONE screw. Hex key COUNTERclockwise.", 18, "bold", BK)
    c += txt(118, 484, "JT Eaton replacement part XHEXKEY-G.", 17, "normal", BK)
    c += box(36, 520, W - 72, 218)
    c += f'<g transform="translate(68,556) scale(0.44)">{st_tomcat()}</g>'
    c += txt(252, 584, "TOMCAT RAT STATION", 20, "bold")
    c += lines(252, 612, ["Squarish, about 6 in tall, a",
                          "see-through window in the lid,",
                          "and a molded living hinge."], 17, 23)
    c += detail(508, 686, 30, hole_none, dashed=True)
    c += txt(68, 688, "NO KEYHOLE AT ALL.", 20, "bold")
    c += lines(68, 712, ["It just opens. Some get", "zip-tied or screwed shut."], 17, 21)
    return wrap(c)

# Every code sized 172 units: the longest URL needs 37 modules, which lands at
# 0.50 mm per printed module after the 0.94 shrink. Decode-test any change.
# Row geometry is shared with makepdf.py, which lays an invisible link
# annotation over each row in the two screen PDFs.
SCAN_Y0, SCAN_DY, SCAN_SZ = 242, 186, 172
SCANS = [("https://shallowdiver.github.io/cityrats/", "NYC RAT DENSITY MAP",
          ["Find likely poison locations."]),
         ("https://www.nyc.gov/site/dsny/what-we-do/programs/safe-disposal-events.page",
          "SAFE DISPOSAL EVENTS",
          ["Double bag anything you take out and",
           "bring it to a NYC SAFE Disposal Event.",
           "If you cannot, put the bagged bait in",
           "the trash."]),
         ("https://shallowdiver.github.io/baitless", "PRINT ANOTHER COPY",
          ["One to read on a screen, one to print",
           "and fold, plus how to fold it. Print at",
           "100 percent, never fit to page."])]

def p_back():
    c = txt(W / 2, 78, "FINAL NOTES", 32, "bold", BK, "middle", "2")
    c += rule(56, 100, W - 56, 5)
    c += txt(36, 132, "GLOVES ON BEFORE YOU START", 19, "bold")
    c += lines(36, 158, ["A new lock is stiff and loosens with use.",
                         "Wash your hands when you are done."], 17, 22)
    c += rule(56, 196, W - 56, 3)
    c += txt(36, 224, "SCAN THESE", 22, "bold", BK, "start", "1")
    y = SCAN_Y0
    for url, label, body in SCANS:
        c += qr(36, y, SCAN_SZ, url)
        c += txt(224, y + 24, label, 18, "bold")
        c += lines(224, y + 52, body, 17, 22)
        y += SCAN_DY
    c += rule(56, 796, W - 56, 3)
    c += lines(W / 2, 826,
               ["FOR THE BETTERMENT OF ALL BEINGS THROUGHOUT THE LIGHT CONE",
                "UNTIL THE LAST PANG OF SUFFERING HAS FOREVER FADED",
                "AND DEATH IS NO MORE"], 14, 22, "normal", BK, "middle")
    return wrap(c)

PAGES = [p_cover(), p_keys(), p_lp(), p_evo(), p_aegis(), p_ezk(), p_others(), p_back()]

if __name__ == "__main__":
    import cairosvg
    os.makedirs("out", exist_ok=True)
    for i, inner in enumerate(PAGES):
        svg = document(inner)
        open(f"out/panel_{i}.svg", "w").write(svg)
        cairosvg.svg2png(bytestring=svg.encode(), write_to=f"out/panel_{i}.png",
                         output_width=W * 2, output_height=H * 2)
    print("panels rendered")
