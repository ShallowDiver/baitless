"""One-print printer calibration sheet.

Print at 100%, fold in half both ways, and each crease crosses printed mm
scales. The reading at the crease IS the compensation value: report A/B (from
the vertical crease) and C/D (from the horizontal crease). A pure feed offset
gives A = B and C = D; a mismatch means the printer also rotates the page.
"""
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

MM = 72 / 25.4
SW, SH = 11 * inch, 8.5 * inch
CX, CY = SW / 2, SH / 2

c = canvas.Canvas("Print_Calibration.pdf", pagesize=(SW, SH))

def hruler(cx, cy, label):
    """Horizontal mm scale; a VERTICAL crease crosses it. + is right."""
    c.setLineWidth(0.5)
    for mm in range(-12, 13):
        x = cx + mm * MM
        t = 26 if mm == 0 else (14 if mm % 5 == 0 else 8)
        c.setLineWidth(1.4 if mm == 0 else 0.5)
        c.line(x, cy - t, x, cy + t)
        if mm % 5 == 0:
            c.setFont("Helvetica", 7)
            c.drawCentredString(x, cy + t + 3, f"{mm:+d}" if mm else "0")
    c.setFont("Helvetica-Bold", 9)
    c.drawCentredString(cx, cy - 40, label)

def vruler(cx, cy, label):
    """Vertical mm scale; a HORIZONTAL crease crosses it. + is up."""
    for mm in range(-12, 13):
        y = cy + mm * MM
        t = 26 if mm == 0 else (14 if mm % 5 == 0 else 8)
        c.setLineWidth(1.4 if mm == 0 else 0.5)
        c.line(cx - t, y, cx + t, y)
        if mm % 5 == 0:
            c.setFont("Helvetica", 7)
            c.drawString(cx + t + 3, y - 2.5, f"{mm:+d}" if mm else "0")
    c.setFont("Helvetica-Bold", 9)
    c.drawCentredString(cx, cy - 12 * MM - 16, label)

# vertical crease (hamburger fold) reads on these two:
hruler(CX, SH - 1.5 * inch, "A")
hruler(CX, 1.5 * inch, "B")
# horizontal crease (hot dog fold) reads on these two:
vruler(2.2 * inch, CY, "C")
vruler(SW - 2.2 * inch, CY, "D")

c.setFont("Helvetica-Bold", 13)
c.drawCentredString(CX, SH - 0.6 * inch, "PRINT AT 100% / ACTUAL SIZE")
c.setFont("Helvetica", 10)
for i, s in enumerate([
        "1. Fold in half left-to-right (hamburger), crease hard, unfold.",
        "   The crease crosses scales A and B. Note where it sits on each, in mm.",
        "2. Fold in half top-to-bottom (hot dog), crease hard, unfold.",
        "   The crease crosses scales C and D. Note both readings.",
        "3. Report the four numbers. Crease left of 0 is negative on A/B;",
        "   crease below 0 is negative on C/D. Half-millimeters are fine."]):
    c.drawString(3.4 * inch, CY + 0.9 * inch - i * 14, s)

c.showPage(); c.save()
print("Print_Calibration.pdf written")
