# The Bait Station Liberation Guide

An 8-panel black-and-white fold-and-cut mini-zine for identifying NYC rat bait
stations, matching the right key, and opening each one. Built around the Amazon
4-key pack (ASIN B0GJ63VV35).

**Current printed version: 0.2.8.** The version prints on the cover
("guide version X.Y.Z" in `p_cover()` in `zine.py`). Bump it on EVERY change to
the zine, even if the user does not say so.

## Build and verify

```
python3 zine.py       # renders out/panel_0..7.png from SVG
python3 check.py      # safe-zone ink scan + copy lint. Must print clear/clean.
python3 makepdf.py    # writes Bait_Station_Field_Guide_PRINT.pdf and _READ.pdf
```

Then decode-test both QR codes off a 300 dpi render of the print sheet:

```
pdftoppm -r 300 -png -f 1 -l 1 Bait_Station_Field_Guide_PRINT.pdf sheet
python3 -c "import cv2; ok,d,_,_ = cv2.QRCodeDetector().detectAndDecodeMulti(cv2.imread('sheet-1.png')); print(d if ok else 'FAIL')"
```

Python deps in requirements.txt; `pdftoppm` needs poppler-utils.

**Always render a proof image of any changed panel and SHOW IT to the user
before declaring done.** Never claim a drawing is fixed without looking at it.

## Files

- `parts.py` — palette, type helpers, arrows, motion icons, key END views
  (cross-sections), hole details, key SIDE views, `poison()`, `qr()`, VM and
  EVO constants.
- `zine.py` — `SAFE`, station geometry, `ring_pt()`, the 8 panel builders,
  render loop.
- `makepdf.py` — imposition, demarcation lines, cut line, printer-calibration
  hooks (`CAL_DX_MM` / `CAL_DY_MM`).
- `check.py` — safe-zone scan of the rendered panels + copy lint (em dashes,
  middle dots, British spellings).
- `calibrate.py` — fold-and-read mm-ruler sheet for measuring a printer's feed
  offset (shelved, kept for later).
- `proof.py`, `stproof.py`, `trapproof.py` — small labeled proof sheets. For a
  shape judgement, render an option sheet like these instead of rebuilding the
  whole zine.

## Printing and folding (why the imposition is the way it is)

- Panel space is 600 x 928 units = 2.75 x 4.25 in (1 unit ≈ 0.116 mm,
  ≈ 0.31 pt of type).
- The user folds NATURALLY: hot dog, then hamburger twice. Panel boundaries
  must sit exactly at the paper's halves and quarters, so the grid spans the
  full sheet. **Do not inset or scale the grid** (tried once, rejected).
- **Print at 100% / Actual Size, never fit-to-page.** Fit-to-page is what made
  earlier prints land off their creases.
- Thin (0.6 pt) demarcation lines print on the true panel boundaries with ends
  held 0.25 in off the sheet edge; one heavy (2 pt) cut line spans the middle
  two columns. Creases beat printed lines when they disagree.
- No full-panel border boxes: a printed rectangle near a page edge cannot
  register to a physical crease and reads as a defect.
- `wrap()` shrinks panel content by `SAFE = 0.94` about the panel center.
  `check.py` enforces a 0.20 in clear band on every panel edge. Anything sized
  absolutely (QR codes especially) must be enlarged to compensate.

## Toner and readability

- Only ONE filled black box in the zine: the cover title block. Everything
  else that was once a black box is an outlined white box with black text.
- Minimum text ~15 units, body 17. Never shrink text to fix an overflow;
  rewrap the line instead.

## Callout style

- No dots on leader-line ends.
- A leader aimed at a ringed keyhole stops AT the dashed ring via `ring_pt()`,
  never stabbing through to the keyhole.

## House style (hard rules)

- Title: **The Bait Station Liberation Guide**.
- No em dashes, no middle dots in printed copy. American spelling only
  (color, molded, armored, gray, center, counterclockwise).
- When asked to remove filler, REMOVE it. Do not write replacement filler.
- Do not claim the hole matches the key's end view; it often does not.
- Do not tell people to log anything.
- Page 1 entries are titled by STATION, matching station page headers exactly.
  Cover end views carry no names and no captions.
- The zine ends on exactly these three lines, in caps, centered:

      FOR THE BETTERMENT OF ALL BEINGS THROUGHOUT THE LIGHT CONE
      UNTIL THE LAST PANG OF SUFFERING HAS FOREVER FADED
      AND DEATH IS NO MORE

## QR codes

Cover: https://shallowdiver.github.io/cityrats/ (NYC rat density map).
Back: https://www.nyc.gov/site/dsny/what-we-do/programs/safe-disposal-events.page
(captioned SAFE DISPOSAL EVENTS). A printed module wants ~0.5 mm: after the
0.94 shrink that is ~4.6 drawn units per module, so size at modules x 4.6 or
larger, and always decode-test the finished sheet.

## The four keys (user-verified, do not regress)

| Key | Color | END view | Motion |
|---|---|---|---|
| Protecta 2-prong | brass | two flat slots at 90 deg to each other, well apart | push straight down, lever key AWAY from box |
| Protecta EVO | black | one ribbon folded into a rounded square wave | push straight in, no turn |
| Aegis | black | plain flattened oval, no slot | in narrow-way, then twist |
| VM / EZ-Klean | gray | two soft trapezoids, pointier ends nearly inward, 180 deg rotational symmetry | press down hard, turn 90 deg toward molded arrow, pull back |

- EVO end view: two wavelengths, starting at the BOTTOM going up. Amplitude 13,
  stroke 5, verticals at x = -24,-12,0,12,24.
- VM constants (shared by key end view and EZ-K lid slots via `vm_pair()`):
  `VM_X, VM_H, VM_SW, VM_GAP, VM_TILT = 9.0, 4.4, 4.25, 15.0, -9`.
  Thinning means lowering `VM_H`. Never thin `VM_X` (taper axis). `VM_GAP` is
  correct.
- The brass key's side view is bilaterally symmetric.

## Keyholes on the stations (user-corrected, do not regress)

- **LP**: two locks on top, each a pair of slots at 90 deg. Wider sides face
  OUTWARD, implied vertex points INTO the station. Left lock is reference;
  right lock is the same pair rotated 90 deg CCW. Both circled, both must be
  opened ("Now the second lock." step).
- **EVO**: one wiggly slot (the key's end view) running horizontally along the
  cover side. Keyhole end is opposite the hinge end.
- **Aegis**: two slots on TOP, left and right, both circled, both opened. Each
  slot = lozenge with a central circle bulging just past it (their union).
- **EZ-Klean**: the VM prong pair, up near the flattened crown of the D, arrow
  between the slots and the front lip.

## Entry placement (user-corrected, do not regress)

- LP: one arched entry in each sloped end wall.
- EVO: entries in the END walls (one under the keyhole, twin opposite). NOT
  front/back.
- Aegis: entries in the parallel side walls near the BACK, opposite each other.
- EZ-Klean: entries in the side walls, opposite each other.
- When only one side wall is visible, draw the visible entry; the callout text
  states the pair.

## Station geometry

- **LP** 13 x 9 x 3⅜ in, triangular, lid lifts off.
- **EVO Express**: hinged cover, U-shaped ledge under the keyhole slot.
- **Aegis RP** 12⅞ x 7⅞ x 4 in: trapezoidal from the top, wider at back, but
  the SIDE walls are PARALLEL (taper comes from long front chamfers).
  `AEG_TOP`, sweep `AEG_OFF = (66, 36)`, rear hinge.
- **EZ-Klean** 12½ x 8¾ x 3¼ in: D-SHAPED from the top; straight front edge,
  rounded back whose crown is slightly FLATTENED (cubic path `EZD_FACE`, bands
  from `EZK_SHOULDER`). Raised front lip (dashed). Sweep `EZK_OFF = (66, 38)`.
- **JT Eaton 902**: tall vertical, twist-off cap, ONE hex screw,
  counterclockwise, replacement part XHEXKEY-G (size in inches is genuinely
  unpublished; print the part number, never a guessed size).
- **Tomcat 33450**: squarish, living hinge, window, no keyhole.

## Drawing rules (do not regress)

Black, white, flat grays (#d6d6d6 top / #a8a8a8 side / #6b6b6b dark key
bodies). No hatch, no dot screens. Stations are explicit faces via `face()` /
`band()`; a curved silhouette (EZ-K's D) gets a smooth path face drawn OVER
polyline-approximated bands so the curve hides the facets.

1. Every station shows a top face and at least one side wall.
2. The sweep's vertical component must be comparable to the front face height
   or tops degenerate into rims. Current sweeps: EVO (100,-112),
   Tomcat (108,-114), JT Eaton (52,-42), EZ-Klean (66,38), LP (0,56),
   Aegis (66,36).
3. Draw the top band before the side band, and every band before the face
   that covers its inner edge.
4. Every entryway is an arched mouse-hole (`archp()`), base on the wall's
   floor edge, sheared to the wall plane (matrix columns = floor-edge
   direction and sweep direction). No lozenges, no rect slots.
5. Never put an arch on a near-edge-on wall (screen axes < ~60 deg apart
   smear it into a blob). Make the sweep more oblique until the wall opens.
6. With an oblique sweep, only sweep viewer-facing facets, or away-facing
   ones fold under the lid as bowtie overlaps.

## Working with this user

- They are a domain expert who has physically handled these keys and boxes.
  Their corrections override patents, product photos, and your priors.
  A photo settles a silhouette; only they settle a cross-section.
- They print and fold for real. Physical constraints (natural folding, toner,
  legibility at 2.75 in wide) are requirements.
- Show proofs. For shape questions, render a small labeled option sheet and
  let them pick before rebuilding everything.
- Direct communication, no filler, no em dashes, no AI-isms.

## History

Twenty-one correction rounds so far; the themes that keep recurring: forms
come from the user's photos and hands, not patents; text must be legible at
print size; nothing printed may pretend to be a page edge; and when the user
says remove, remove.
