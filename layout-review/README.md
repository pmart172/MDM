# Floor plan review (EG / OG / DG), third edition

`index.html` is the review: how the building reads (set-back storey, stair, flue, window piers,
stacks), a benchmark against 5-star hotel planning standards and luxury-residential / German norms
(VDI 6000, DIN 18040-2, DIN 18101, hausbaujournal modules), an audit of the current plans, three
options for the top floor, two for the upper floor and one for the ground floor, each drawn to scale
with standard architectural symbols, a decision matrix, fixture and door schedules, the free-depth
check in front of every fixture, and a build list with wall coordinates.

Generator: `engine.py` (drawing engine with geometry checks: walls meeting windows, rooms without
doors, door swings, fixture overlaps, pocket-door cavities, VDI 6000 clearances by ray-casting),
`floors.py` (the nine plans), `plancss.py` (tokens), `build3.py` (page), `render.py` (PNG renders
with headless Chromium), `export.py` (this export). `python3 floors.py` lists the check results;
`python3 build3.py` rebuilds `index.html`. `svg/` holds the nine drawings as standalone files.
