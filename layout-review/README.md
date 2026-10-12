# Floor plan review (EG / OG / DG) and a two-storey version, fourth edition

`index.html` is the review. Section 0 is the two-storey version of the house requested on 12 October:
option T1 on the existing 8.29 × 11.04 m plate (one stair, nine windows, master suite upstairs) and
option T2 on a 9.79 × 12.04 m plate (master suite on the ground floor with a 10.2 m² bath and an
8.0 m² dressing; needs a Baufenster / GRZ / Abstandsfläche check). Sections 1–7 are the review of
the three-storey plans: how the building reads, a benchmark against 5-star hotel planning standards
and luxury-residential / German norms (VDI 6000, DIN 18040-2, DIN 18101), an audit of the current
plans, three options for the top floor, two for the upper floor and one for the ground floor, each
drawn to scale with standard architectural symbols, decision matrices, fixture and door schedules,
the free-depth check in front of every fixture, and a build list with wall coordinates.

Generator: `engine.py` (drawing engine with geometry checks: walls meeting windows, rooms without
doors, door swings, fixture overlaps, pocket-door cavities, VDI 6000 clearances by ray-casting),
`floors.py` (the nine three-storey plans), `floors2.py` (the four two-storey plans), `plancss.py`
(tokens), `build3.py` (three-storey sections), `build4.py` (adds section 0 and writes `index.html`),
`render.py` / `render2.py` (PNG renders with headless Chromium), `export4.py` (this export).
`python3 floors.py` and `python3 floors2.py` list the check results; `python3 build4.py` rebuilds
`index.html`. `svg/` holds the thirteen drawings as standalone files.
