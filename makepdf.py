"""Imposition, VECTOR. The panels are SVG all the way down, so they are nested
into one sheet SVG and handed to cairosvg once, instead of being rasterized to
PNG and re-embedded as bitmaps.

Why it matters on paper: as bitmaps the QR modules and the 15-unit type were
resampled twice, once by us at 2x and again by the printer driver. As vector,
module edges and glyph outlines land on the printer's own device grid. DejaVu
Sans embeds and subsets, so the PDF carries real selectable text. It is also
about 18x smaller, which keeps the committed PDFs from bloating git history.

Everything geometric below is unchanged from the raster version: same grid, same
demarcations, same cut, same calibration hooks."""
import cairosvg, pypdf, io
from zine import PAGES, document
from parts import W, H

PT = 72.0
PGW, PGH = 2.75 * PT, 4.25 * PT          # one panel, 198 x 306 pt
SW, SH = 11 * PT, 8.5 * PT               # the sheet, 792 x 612 pt (letter, landscape)
cw, ch = SW / 4, SH / 2                  # a grid cell, same 198 x 306 pt

# Panel units are not perfectly square: 600u/2.75in = 218.18 but 928u/4.25in =
# 218.35. The raster path hid this because drawImage stretched each PNG to the
# cell. Keep that behavior by scaling x and y independently.
SX, SY = cw / W, ch / H

# ---------------------------------------------------------------- READ, screen
# One page per panel, in reading order. cairosvg emits a single page per call,
# so render eight and merge.
merged = pypdf.PdfWriter()
for inner in PAGES:
    buf = io.BytesIO()
    cairosvg.svg2pdf(bytestring=document(inner, size=(f"{PGW}pt", f"{PGH}pt")).encode(),
                     write_to=buf)
    merged.append(pypdf.PdfReader(io.BytesIO(buf.getvalue())))
with open("Bait_Station_Field_Guide_READ.pdf", "wb") as f:
    merged.write(f)

# --------------------------------------------------------------- PRINT, imposed
# Sized for NATURAL folding: hot dog, then hamburger twice. That only registers
# if the panel boundaries sit exactly at the paper's halves and quarters, so the
# grid spans the full sheet and each panel is exactly 2.75 x 4.25 in.
#
# MUST BE PRINTED AT 100% / ACTUAL SIZE. The print dialog's "fit to page" default
# shrinks the sheet about 5% and shifts it toward the printable-area center, which
# pulls every boundary off its crease (up to ~4 mm at the outer quarter folds).
# At 100% the only residual is the printer's mechanical feed bias, a millimeter
# or so, which the panels' internal margins absorb. The creases are the truth:
# where a printed line and a crease disagree, follow the crease.
top, bot = [5, 4, 3, 2], [6, 7, 8, 1]

# Per-printer registration compensation, measured with calibrate.py's sheet.
# The readings transfer directly: CAL_DX_MM = the A/B value, CAL_DY_MM = the
# C/D value. Positive DX moves the printed image right, positive DY moves it up.
CAL_DX_MM, CAL_DY_MM = 0.0, 0.0
MM = PT / 25.4

def cell(pg, col, row, flip):
    """One panel placed in the grid. Rightmost transform applies first, so the
       panel is scaled into cell size, moved to its cell, then (top row only)
       turned 180 degrees about that cell's own center."""
    x, y = col * cw, row * ch
    t = f"translate({x},{y}) scale({SX:.6f},{SY:.6f})"
    if flip:
        t = f"rotate(180,{x + cw / 2},{y + ch / 2}) " + t
    return f'<g transform="{t}">{PAGES[pg - 1]}</g>'

g = f'<rect width="{SW}" height="{SH}" fill="#ffffff"/>'
g += "".join(cell(pg, col, 0, True) for col, pg in enumerate(top))
g += "".join(cell(pg, col, 1, False) for col, pg in enumerate(bot))

# Page demarcations, thin, at the true boundaries (= the intended creases). Their
# ends stop 0.25 in short of the sheet edge so the unprintable band cannot chew
# them into ragged stubs. No outer border: the sheet edge demarcates itself.
E = 0.25 * PT          # hold line ends 0.25 in off the sheet edge
L = 'stroke="#000000" fill="none" stroke-width="{}"'
for i in (1, 2, 3):
    g += f'<line x1="{i*cw}" y1="{E}" x2="{i*cw}" y2="{SH-E}" {L.format(0.6)}/>'
g += f'<line x1="{E}" y1="{ch}" x2="{cw}" y2="{ch}" {L.format(0.6)}/>'
g += f'<line x1="{3*cw}" y1="{ch}" x2="{SW-E}" y2="{ch}" {L.format(0.6)}/>'
# the cut, heavy, across the middle two columns only
g += f'<line x1="{cw}" y1="{ch}" x2="{3*cw}" y2="{ch}" {L.format(2.0)}/>'

# Positive CAL_DY_MM moves the image UP, so it is negative in SVG's y-down space.
sheet = (f'<svg xmlns="http://www.w3.org/2000/svg" width="11in" height="8.5in" '
         f'viewBox="0 0 {SW} {SH}">'
         f'<g transform="translate({CAL_DX_MM*MM},{-CAL_DY_MM*MM})">{g}</g></svg>')
cairosvg.svg2pdf(bytestring=sheet.encode(),
                 write_to="Bait_Station_Field_Guide_PRINT.pdf")
print("PDFs written")
