"""Writes standalone SVGs (with embedded style) for all thirteen plans and copies the fourth edition into the repo."""
import floors, floors2, floors3, floors4, floors5, siteplan, plancss, os, shutil
REPO = "/home/user/MDM/layout-review"
style = "<style>" + plancss.TOKENS.replace("\n", " ") + plancss.PLAN_CSS.replace("\n", " ") + " svg{background:var(--paper2)}</style>"
defs = '<defs><marker id="ah" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="context-stroke"/></marker></defs>'
os.makedirs(f"{REPO}/svg", exist_ok=True)
for old in os.listdir(f"{REPO}/svg"): os.remove(f"{REPO}/svg/{old}")
for k, fn in list(floors.ALL.items()) + list(floors2.ALL.items()) + list(floors3.ALL.items()) + list(floors4.ALL.items()) + list(floors5.ALL.items()):
    s = fn().svg().replace('<svg ', '<svg xmlns="http://www.w3.org/2000/svg" ', 1).replace('class="plan">', 'class="plan">' + style + defs, 1)
    open(f"{REPO}/svg/{k}.svg", "w").write(s)
for f in ("engine.py", "floors.py", "floors2.py", "floors3.py", "floors4.py", "floors5.py", "siteplan.py", "plancss.py", "build3.py", "build4.py", "build5.py", "build6.py", "dump_plan.py", "render.py", "render2.py", "export6.py"):
    shutil.copy(f, f"{REPO}/{f}")
for old in ("export.py", "export4.py", "export5.py"):
    p = f"{REPO}/{old}"
    if os.path.exists(p): os.remove(p)
shutil.copy("index.html", f"{REPO}/index.html")
site = siteplan.svg()[0].replace('<svg ', '<svg xmlns="http://www.w3.org/2000/svg" ', 1).replace('class="plan"', 'class="plan"' + '', 1)
site = site.replace('style="max-width:520px">', 'style="max-width:520px">' + style + defs, 1)
open(f"{REPO}/svg/site_plan.svg", "w").write(site)
open(f"{REPO}/README.md", "w").write("""# Floor plan review (EG / OG / DG) and a two-storey version, sixth edition

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
""")
print("exported to", REPO)
