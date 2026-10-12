"""Writes standalone SVGs (with embedded style) and copies the review into the repo."""
import floors, plancss, os, shutil
REPO = "/home/user/MDM/layout-review"
style = "<style>" + plancss.TOKENS.replace("\n", " ") + plancss.PLAN_CSS.replace("\n", " ") + " svg{background:var(--paper2)}</style>"
defs = '<defs><marker id="ah" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="context-stroke"/></marker></defs>'
os.makedirs(f"{REPO}/svg", exist_ok=True)
for old in os.listdir(f"{REPO}/svg"): os.remove(f"{REPO}/svg/{old}")
for k, fn in floors.ALL.items():
    s = fn().svg().replace('<svg ', '<svg xmlns="http://www.w3.org/2000/svg" ', 1).replace('class="plan">', 'class="plan">' + style + defs, 1)
    open(f"{REPO}/svg/{k}.svg", "w").write(s)
for f in ("engine.py", "floors.py", "plancss.py", "build3.py", "render.py", "export.py"):
    shutil.copy(f, f"{REPO}/{f}")
for old in ("build2.py", "plans.py"):
    p = f"{REPO}/{old}"
    if os.path.exists(p): os.remove(p)
shutil.copy("index.html", f"{REPO}/index.html")
open(f"{REPO}/README.md", "w").write("""# Floor plan review (EG / OG / DG), third edition

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
""")
print("exported to", REPO)
