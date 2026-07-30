import cairosvg
from parts import *

c = f'<rect width="1220" height="900" fill="{WH}"/>' + DEFS
c += txt(30, 44, "MOTION ICONS", 22, "bold")
ics=[(ic_press,"press"),(ic_push_in,"push in"),(ic_drop_over,"drop over post"),(ic_lever,"lever away"),
     (ic_turn,"turn"),(ic_turn_arrow,"turn w/arrow"),(ic_pull_back,"pull back"),(ic_lift,"lift"),
     (ic_repeat,"2nd lock"),(ic_snap,"snap shut"),(ic_hex,"hex ccw"),(ic_hand,"gloves")]
for i,(fn,lab) in enumerate(ics):
    x=68+i*98
    c += icon(fn,x,104,1.35); c += txt(x,168,lab,13,"normal",BK,"middle")

c += txt(30, 232, "KEY SIDE VIEW  →  END VIEW  →  THE HOLE ON THE BOX", 22, "bold")
rows=[(side_lp,end_lp,hole_lp,"Protecta 2-prong"),(side_evo,end_evo,hole_evo,"Protecta EVO"),
      (side_aegis,end_aegis,hole_aegis,"Aegis"),(side_vm,end_vm,hole_vm,"VM / EZ-Klean")]
for i,(sf,ef,hf,lab) in enumerate(rows):
    x=130+i*290
    c += place(sf,x,270,0.46)
    c += detail(x, 452, 40, ef)
    c += arrow(x+62, 452, x+112, 452, BK, 5, 12)
    c += detail(x+174, 452, 40, hf, dashed=True)
    c += txt(x,530,lab,17,"bold",BK,"middle")
    c += txt(x,552,"side",13,"normal",BK,"middle")
    c += txt(x,382,"END VIEW        THE HOLE",12,"normal",WH,"middle")

c += txt(30, 620, "TONE TEST (photocopy safe)", 22, "bold")
for i,(f_,lab) in enumerate([(HATCH,"hatch"),(HATCHL,"hatch light"),(DOTS,"dots"),(BK,"solid"),(WH,"white")]):
    x=40+i*150
    c += f'<rect x="{x}" y="640" width="120" height="80" fill="{f_}" stroke="{BK}" stroke-width="3"/>'
    c += txt(x+60,740,lab,14,"normal",BK,"middle")

svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1220 900">{c}</svg>'
cairosvg.svg2png(bytestring=svg.encode(), write_to="out/proof.png", output_width=1500)
print("ok")
