from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader

PW, PH = 2.75*inch, 4.25*inch
pngs = [f"out/panel_{i}.png" for i in range(8)]

c = canvas.Canvas("Bait_Station_Field_Guide_READ.pdf", pagesize=(PW, PH))
for p in pngs:
    c.drawImage(ImageReader(p), 0, 0, PW, PH); c.showPage()
c.save()

# Imposition, sized for NATURAL folding: hot dog, then hamburger twice. That only
# registers if the panel boundaries sit exactly at the paper's halves and quarters,
# so the grid spans the full sheet and each panel is exactly 2.75 x 4.25 in.
#
# MUST BE PRINTED AT 100% / ACTUAL SIZE. The print dialog's "fit to page" default
# shrinks the sheet about 5% and shifts it toward the printable-area center, which
# pulls every boundary off its crease (up to ~4 mm at the outer quarter folds).
# At 100% the only residual is the printer's mechanical feed bias, a millimeter
# or so, which the panels' internal margins absorb. The creases are the truth:
# where a printed line and a crease disagree, follow the crease.
SW, SH = 11*inch, 8.5*inch
cw, ch = SW/4, SH/2
top, bot = [5, 4, 3, 2], [6, 7, 8, 1]

# Per-printer registration compensation, measured with calibrate.py's sheet.
# The readings transfer directly: CAL_DX_MM = the A/B value, CAL_DY_MM = the
# C/D value. Positive DX moves the printed image right, positive DY moves it up.
CAL_DX_MM, CAL_DY_MM = 0.0, 0.0
MM = 72 / 25.4

c = canvas.Canvas("Bait_Station_Field_Guide_PRINT.pdf", pagesize=(SW, SH))
c.translate(CAL_DX_MM * MM, CAL_DY_MM * MM)
for col, pg in enumerate(bot):
    c.drawImage(ImageReader(pngs[pg-1]), col*cw, 0, cw, ch)
for col, pg in enumerate(top):
    c.saveState(); c.translate(col*cw + cw, 2*ch); c.rotate(180)
    c.drawImage(ImageReader(pngs[pg-1]), 0, 0, cw, ch); c.restoreState()

# Page demarcations, thin, at the true boundaries (= the intended creases). Their
# ends stop 0.25 in short of the sheet edge so the unprintable band cannot chew
# them into ragged stubs. No outer border: the sheet edge demarcates itself.
E = 0.25*inch
c.setStrokeColorRGB(0, 0, 0); c.setLineWidth(0.6)
for i in (1, 2, 3):
    c.line(i*cw, E, i*cw, SH - E)
c.line(E, ch, cw, ch)
c.line(3*cw, ch, SW - E, ch)
# the cut, heavy, across the middle two columns only
c.setLineWidth(2.0)
c.line(cw, ch, 3*cw, ch)
c.showPage(); c.save()
print("PDFs written")
