import cairosvg, zine as Z
from parts import *
c = f'<rect width="1500" height="820" fill="{WH}"/>' + DEFS
items=[(Z.st_lp,0.62,"LP"),(Z.st_evo,0.50,"EVO"),(Z.st_aegis,0.50,"AEGIS"),
       (Z.st_ezk,0.52,"EZ-KLEAN"),(Z.st_jte,0.60,"JT EATON"),(Z.st_tomcat,0.62,"TOMCAT")]
for i,(fn,s,lab) in enumerate(items):
    col=i%3; row=i//3
    x=60+col*470; y=60+row*380
    c += f'<g transform="translate({x},{y}) scale({s})">{fn()}</g>'
    c += txt(x+120, y+330, lab, 24, "bold")
svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1500 820">{c}</svg>'
cairosvg.svg2png(bytestring=svg.encode(), write_to="out/stproof.png", output_width=1500)
print("ok")
