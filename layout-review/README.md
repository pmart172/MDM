# Floor plan review (EG / OG / DG) and a two-storey version, sixth edition

`index.html` opens on an Index of all versions with their key figures; Compare shows two or three versions side by side
(plans level by level plus a facts table); Full review is the complete text. T5 adds the Rötha-inspired version with a straight stair parallel to the street.
In the full review, section 0 is the two-storey version of the house on the real envelope of
Altkönigstraße 122 (Oberursel): plot 966.6 m² for the mirrored pair, GRZ 0.25, GFZ 0.50, Baufenster
5–20 m behind the street, boundary garages. Option T1 keeps today's 8.29 × 11.04 m plate; option T4 is
the maximum, 8.29 × 14.07 m per house (97 % of GRZ and GFZ, the depth capped by the 3 m Abstandsfläche
at the east rear corner) with a WU basement, drawn as ground floor, upper floor, basement and a site
plan, with the brief checked item by item. Two earlier studies (T2, T3) drawn before the plot data
arrived are kept in a collapsed block. Sections 1–7 are the review of the three-storey plans.

Generator: `engine.py` (drawing engine with geometry checks: walls meeting windows, rooms without
doors, door swings, fixture overlaps, pocket-door cavities, VDI 6000 clearances by ray-casting),
`floors.py` (the nine three-storey plans), `floors2.py` (T1/T2), `floors3.py` (T3), `floors4.py` (T4), `floors5.py` (T5, the Rötha stair), `siteplan.py` (site plan), `plancss.py`
(tokens), `build3.py` (three-storey sections), `build4.py` / `build5.py` (section 0), `build6.py` (Index, Compare and Full review views; writes `index.html`), `dump_plan.py` (compact geometry dump of one plan),
`render.py` / `render2.py` (PNG renders with headless Chromium), `export4.py` (this export).
`python3 floors.py` … `python3 floors4.py` list the check results; `python3 build6.py` rebuilds `index.html`.
`svg/` holds the twenty-three drawings and the site plan as standalone files.
