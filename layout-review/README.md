# Floor plan review (EG / OG / DG), second edition

`index.html` is the review: how the building reads (set-back storey, stair, flue, stacks),
a benchmark against 5-star hotel planning standards and luxury-residential / German norms
(VDI 6000, DIN 18040-2, DIN 18101, hausbaujournal modules), an audit of the current plans,
three options for the top floor, two for the upper floor and one for the ground floor, each
drawn to scale with clearance zones, a decision matrix, fixture and door schedules and a
build list with wall coordinates.

Generator: `engine.py` (drawing engine with a clearance checker), `floors.py` (the nine
plans), `plancss.py` (tokens), `build2.py` (page). Run `python3 floors.py` to list clearance
conflicts and `python3 build2.py` to rebuild `index.html`. `svg/` holds the nine drawings as
standalone files.
