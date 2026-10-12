# Floor plan review (EG / OG / DG) and a two-storey version, fifth edition

`index.html` is the review. Section 0 is the two-storey version of the house on the real envelope of
Altkönigstraße 122 (Oberursel): plot 966.6 m² for the mirrored pair, GRZ 0.25, GFZ 0.50, Baufenster
5–20 m behind the street, boundary garages. Option T1 keeps today's 8.29 × 11.04 m plate; option T4 is
the maximum, 8.29 × 14.07 m per house (97 % of GRZ and GFZ, the depth capped by the 3 m Abstandsfläche
at the east rear corner) with a WU basement, drawn as ground floor, upper floor, basement and a site
plan, with the brief checked item by item. Two earlier studies (T2, T3) drawn before the plot data
arrived are kept in a collapsed block. Sections 1–7 are the review of the three-storey plans.

Generator: `engine.py` (drawing engine with geometry checks: walls meeting windows, rooms without
doors, door swings, fixture overlaps, pocket-door cavities, VDI 6000 clearances by ray-casting),
`floors.py` (the nine three-storey plans), `floors2.py` (T1/T2), `floors3.py` (T3), `floors4.py` (T4), `siteplan.py` (site plan), `plancss.py`
(tokens), `build3.py` (three-storey sections), `build4.py` / `build5.py` (section 0; build5 writes `index.html`),
`render.py` / `render2.py` (PNG renders with headless Chromium), `export4.py` (this export).
`python3 floors.py` … `python3 floors4.py` list the check results; `python3 build5.py` rebuilds `index.html`.
`svg/` holds the twenty drawings as standalone files.
