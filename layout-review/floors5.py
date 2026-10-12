"""T5: the Rötha-inspired half on the T4 plate (8.29 x 14.07): a straight stair across the house, parallel to the street,
between the entrance band and the living room; a daylit gallery upstairs; mudroom with the garage door; kitchen east,
ground-floor bedroom south-west, master suite with a sitting area across the garden front.
Second iteration: rooms reach the inner face of the south wall (y 13.71), balustrade on the open side of the flight, no desk in front of the bedroom door."""
from engine import Plan
W, H = 8.29, 14.07
YS = H - 0.36

def area(rect, *holes):
    a = (rect[2]-rect[0])*(rect[3]-rect[1])
    for h in holes: a -= (h[2]-h[0])*(h[3]-h[1])
    return round(a, 1)
GARAGE = dict(x0=8.29, y0=0.0, x1=8.29+4.81, y1=7.42)

def base(title, garage=True):
    p = Plan(W, H, title, outside=dict(x0=0.0, y0=-0.3, x1=W+5.2, y1=H+0.3) if garage else None)
    p.north(W+0.45, -0.35); p.scalebar(0.0, y=H+0.90)
    p.dimstring("h", [0, W], -0.85, [f"{W:.2f} outside"])
    if garage:
        g = GARAGE
        p.L["outside"].append(f'<rect x="{g["x0"]*64:.1f}" y="{g["y0"]*64:.1f}" width="{(g["x1"]-g["x0"])*64:.1f}" height="{(g["y1"]-g["y0"])*64:.1f}" class="void"/>')
        p._t("outside", (g["x0"]+g["x1"])/2, 3.4, "double garage on the boundary", "tiny"); p._t("outside", (g["x0"]+g["x1"])/2, 3.75, "4.8–6.9 × 7.42, roof at EG + 2.57", "tiny")
    return p

STAIR = (1.42, 4.18, 5.72, 5.18)   # straight flight across the house, foot west, head east

def t5_eg():
    p = base("Two storeys T5 · ground floor · Rötha stair")
    p.window("N", 1.90, 2.90, note="hall window"); p.window("N", 5.20, 7.20, note="mudroom window, sill 1.20")
    p.window("E", 8.00, 9.40); p.window("S", 0.80, 3.20); p.window("S", 3.80, 7.40, note="glass wall 3.6 m: lift-slide 3.0 + fixed pane")
    p.door(0.80, 0.0, 1.74, 0.36, "W", "S"); p._t("dim", 1.27, -0.14, "entrance", "note")
    p.stairs(*STAIR, n=15, up="E", label="straight flight parallel to the street · cellar flight below")
    p.screen(1.42, 5.18, 5.72, 5.30, h=1.0); p.floor(0.22, 4.06, 1.42, 5.30); p.floor(7.04, 4.18, 7.93, 5.30)
    p.room("Entrance hall", 0.22, 0.36, 2.98, 4.06, lx=1.6, ly=2.3, area=10.2, sub="")
    p.room("Guest WC", 3.10, 0.36, 4.30, 2.40, lx=3.7, ly=1.5, sub="")
    p.room("Cloaks", 3.10, 2.52, 4.30, 4.06, lx=3.7, ly=3.3, sub="")
    p.room("Mudroom · pantry (HWR)", 4.42, 0.36, 7.93, 4.06, lx=6.2, ly=2.1, area=13.0, sub="door from the garage")
    p.room("Cellar stair", 5.72, 4.18, 6.92, 5.18, lx=6.32, ly=4.75, sub="")
    p.room("Living · dining · kitchen", 0.22, 5.30, 7.93, YS, lx=3.6, ly=8.7, area=area((0.22,5.30,7.93,YS), (0.22,7.83,3.54,YS)), sub="open plan behind the stair")
    p.room("Bedroom EG", 0.22, 9.95, 3.42, YS, lx=1.8, ly=10.3, sub="")
    p.room("En suite", 0.22, 7.95, 2.22, 9.83, lx=1.2, ly=9.3, sub="")
    p.wall(2.98, 0.36, 3.10, 4.06); p.wall(3.10, 2.40, 4.30, 2.52); p.wall(4.30, 0.36, 4.42, 4.06); p.wall(1.42, 4.06, 7.93, 4.18)
    p.wall(5.60, 4.18, 5.72, 5.18); p.wall(6.92, 4.18, 7.04, 5.18); p.wall(5.72, 5.18, 6.92, 5.30)
    p.wall(3.42, 9.95, 3.54, YS); p.wall(0.22, 9.83, 3.54, 9.95); p.wall(2.22, 7.95, 2.34, 9.83); p.wall(0.22, 7.83, 2.34, 7.95)
    p.door(2.98, 0.90, 3.10, 1.80, "N", "W")              # guest WC from the hall, opens out
    p.door(2.98, 2.90, 3.10, 3.80, "N", "E", kind="open")  # cloaks cupboard, folding doors
    p.door(7.93, 1.20, 8.29, 2.10, "N", "W"); p._t("dim", W+0.22, 1.65, "door from the garage", "note", rot=-90)
    p.door(6.95, 4.06, 7.85, 4.18, "W", "N")              # mudroom -> kitchen passage, opens into the mudroom
    p.door(5.60, 4.30, 5.72, 5.10, "N", "W", kind="open")  # cellar flight entry at the head of the main flight
    p.door(6.92, 4.30, 7.04, 5.10, "N", "E")              # cellar lobby from the kitchen passage
    p.door(3.42, 12.30, 3.54, 13.20, "S", "W")            # living -> bedroom, foot end, opens into the bedroom
    p.door(0.35, 9.83, 1.25, 9.95, "W", "N")              # bedroom -> en suite
    # hall and service rooms
    p.wardrobe("Entrance hall", 0.22, 1.60, 0.82, 3.10, label="Wardrobe 1.5")
    p.furn("Entrance hall", 1.40, 3.40, 2.60, 3.80, "Bench")
    p.wc("Guest WC", 3.70, 0.36, "S"); p.vanity("Guest WC", 3.10, 1.75, 3.55, 2.25, basins=1, wall="W", label="")
    p.wardrobe("Cloaks", 3.70, 2.52, 4.30, 4.06, label="Coats")
    p.furn("Mudroom · pantry (HWR)", 4.42, 0.36, 5.02, 3.00, "Shelves", tall=True); p.appliance("Mudroom · pantry (HWR)", 5.20, 0.45, 5.85, 1.10, "Freezer")
    p.furn("Mudroom · pantry (HWR)", 6.90, 0.36, 7.93, 0.86, "Bench · boots"); p.furn("Mudroom · pantry (HWR)", 4.42, 3.30, 5.60, 3.90, "Worktop")
    # kitchen east: L-run on the north and east walls, island
    p.furn("Living · dining · kitchen", 4.42, 5.30, 5.02, 5.90, "", tall=True); p._t("lab", 4.72, 6.1, "fridge / oven", "tiny")
    p.kitchen("Living · dining · kitchen", 5.02, 5.30, 6.80, 5.90, sink=None, hob=6.10, label="Run 1.8")
    p.kitchen("Living · dining · kitchen", 7.33, 6.30, 7.93, 10.50, sink=None, hob=None, label="Run 4.2 m")
    p._r("fix", 7.43, 7.60, 7.83, 8.40, "basin", rx=3); p._c("fix", 7.63, 8.00, 0.03, "drain")
    p.furn("Living · dining · kitchen", 4.90, 7.00, 6.10, 9.40, "Island 1.2 × 2.4")
    p.table("Living · dining · kitchen", 2.60, 5.50, 3.60, 7.50, chairs=(0,0,3,3), label="Table")
    p.sofa("Living · dining · kitchen", 6.93, 10.60, 7.93, 12.60, back="E")
    p.sofa("Living · dining · kitchen", 4.10, 10.20, 6.10, 11.20, back="N")
    p.furn("Living · dining · kitchen", 5.20, 11.60, 6.20, 12.40, "Coffee table")
    p.furn("Living · dining · kitchen", 3.54, 10.50, 3.94, 12.10, "TV")
    # ground-floor bedroom south-west with en suite on the party wall
    p.bed("Bedroom EG", 0.22, 10.55, 2.22, 12.15, head="W", label="Bed 1.6 × 2.0")
    p.nightstand("Bedroom EG", 0.22, 10.05, 0.64, 10.47)
    p.wardrobe("Bedroom EG", 2.82, 9.95, 3.42, 11.95, label="Wardrobe 2.0")
    p.chair("Bedroom EG", 1.30, 13.25, r=0.28); p._t("lab", 1.30, 13.62, "armchair", "tiny")
    p.shower("En suite", 0.22, 7.95, 1.12, 8.85, glass=("S","E"), entry="S")
    p.wc("En suite", 1.50, 7.95, "S"); p.vanity("En suite", 1.72, 9.00, 2.22, 9.60, basins=1, wall="E", label="")
    p.dimstring("v", [0.36, 4.06, 4.18, 5.18, 5.30, 7.83, 7.95, 9.83, 9.95, YS], -0.40, ["3.70", "", "1.00", "", "2.53", "", "1.88", "", "3.76"])
    p.dimstring("h", [0.22, 2.98, 3.10, 4.30, 4.42, 7.93], -0.40, ["2.76", "", "1.20", "", "3.51"])
    p.dimstring("h", [0.22, 3.42, 3.54, 7.93], H+0.55, ["3.20", "", "4.39"])
    return p

def t5_og():
    p = base("Two storeys T5 · upper floor · daylit gallery", garage=False)
    p.window("N", 1.30, 2.70); p.window("N", 5.20, 6.60); p.window("E", 4.30, 6.20, note="gallery window"); p.window("E", 7.60, 9.00)
    p.window("S", 0.80, 2.80); p.window("S", 4.60, 7.40)
    p.stairs(*STAIR, n=15, up="E", label="stair opening")
    p.room("Bedroom NW", 0.22, 0.36, 3.80, 4.06, lx=2.2, ly=3.5, sub="")
    p.room("Bedroom NE", 3.92, 0.36, 7.93, 4.06, lx=5.6, ly=3.25, sub="")
    p.room("Gallery", 0.22, 4.18, 7.93, 6.40, lx=3.6, ly=5.75, area=12.8, sub="daylit hall around the stair")
    p.room("Family bath", 0.22, 6.52, 3.00, 9.70, lx=1.6, ly=8.0, sub="")
    p.room("Dressing", 3.12, 6.52, 5.02, 9.70, lx=4.25, ly=7.6, sub="")
    p.room("Master bath", 5.14, 6.52, 7.93, 9.70, lx=6.4, ly=8.1, sub="")
    p.room("Master bedroom", 0.22, 9.82, 7.93, YS, lx=3.3, ly=10.35, sub="with sitting area")
    p.wall(3.80, 0.36, 3.92, 4.06); p.wall(0.22, 4.06, 7.93, 4.18); p.wall(0.22, 6.40, 7.93, 6.52)
    p.wall(3.00, 6.52, 3.12, 9.70); p.wall(5.02, 6.52, 5.14, 9.70); p.wall(0.22, 9.70, 7.93, 9.82)
    p.door(0.35, 4.06, 1.25, 4.18, "W", "N"); p.door(6.00, 4.06, 6.90, 4.18, "E", "N")
    p.door(1.10, 6.40, 2.00, 6.52, "W", "S")              # family bath from the gallery, between tub and shower
    p.door(3.60, 6.40, 4.50, 6.52, "E", "S")              # dressing from the gallery
    p.door(5.02, 7.50, 5.14, 8.40, "N", "E")              # dressing -> master bath
    p.door(3.60, 9.70, 4.50, 9.82, "E", "S")              # dressing -> bedroom, foot end
    # children: beds on the partition, desks under the windows
    p.bed("Bedroom NW", 1.80, 1.60, 3.80, 3.00, head="E", label="Bed 1.4 × 2.0"); p.nightstand("Bedroom NW", 3.38, 1.10, 3.80, 1.52)
    p.furn("Bedroom NW", 1.30, 0.36, 2.70, 0.96, "Desk"); p.chair("Bedroom NW", 1.55, 1.2, r=0.2)
    p.wardrobe("Bedroom NW", 0.22, 1.10, 0.82, 3.00, label="Wardrobe 1.9")
    p.bed("Bedroom NE", 5.93, 1.60, 7.93, 3.00, head="E", label="Bed 1.4 × 2.0"); p.nightstand("Bedroom NE", 7.51, 1.10, 7.93, 1.52)
    p.furn("Bedroom NE", 5.20, 0.36, 6.60, 0.96, "Desk"); p.chair("Bedroom NE", 5.45, 1.2, r=0.2)
    p.wardrobe("Bedroom NE", 3.92, 3.46, 5.80, 4.06, label="Wardrobe 1.9")
    p.furn("Gallery", 0.22, 4.30, 0.62, 5.10, "Books", tall=True); p.chair("Gallery", 6.9, 5.3, r=0.32); p._t("lab", 6.9, 5.85, "armchair", "tiny")
    # family bath 2.78 x 3.18 with laundry column
    p.tub("Family bath", 0.22, 6.52, 1.02, 8.32)
    p.shower("Family bath", 2.00, 6.52, 3.00, 7.52, glass=("S","W"), entry="S")
    p.vanity("Family bath", 1.50, 9.15, 3.00, 9.70, basins=2, wall="S", label="")
    p.wc("Family bath", 1.10, 9.70, "N"); p.appliance("Family bath", 0.22, 8.45, 0.87, 9.10, "W+D")
    # dressing 1.90 x 3.18
    p.wardrobe("Dressing", 3.12, 7.50, 3.72, 9.70, label="Wardrobe 2.2 m"); p.furn("Dressing", 4.62, 8.50, 5.02, 9.70, "Drawers")
    # master bath 2.79 x 3.18, east window
    p.tub("Master bath", 7.13, 6.60, 7.93, 8.40)
    p.shower("Master bath", 5.14, 8.50, 6.34, 9.70, glass=("N","E"), entry="N")
    p.vanity("Master bath", 5.14, 6.52, 6.74, 7.07, basins=2, wall="N", label="")
    p.wc("Master bath", 7.60, 9.70, "N"); p.radiator("Master bath", 6.50, 9.62, 7.10, 9.70)
    # master bedroom 7.71 x 3.53 across the garden front, bed on the party wall, sitting area east
    p.bed("Master bedroom", 0.22, 10.60, 2.22, 12.40, head="W", label="Bed 1.8 × 2.0")
    p.nightstand("Master bedroom", 0.22, 10.05, 0.72, 10.55); p.nightstand("Master bedroom", 0.22, 12.45, 0.72, 12.95)
    p.furn("Master bedroom", 2.33, 10.80, 2.78, 12.20, "Bench", kind="bench")
    p.furn("Master bedroom", 4.70, 9.82, 6.30, 10.22, "Dresser / TV")
    p.sofa("Master bedroom", 5.93, 11.00, 7.93, 12.00, back="E", label="Sofa"); p.furn("Master bedroom", 6.60, 12.30, 7.40, 13.00, "Side table")
    p.furn("Master bedroom", 4.10, 13.11, 5.50, YS, "Desk"); p.chair("Master bedroom", 4.8, 12.84, r=0.2)
    p.dimstring("v", [0.36, 4.06, 4.18, 6.40, 6.52, 9.70, 9.82, YS], -0.40, ["3.70", "", "2.22", "", "3.18", "", "3.89"])
    p.dimstring("h", [0.22, 3.00, 3.12, 5.02, 5.14, 7.93], H+0.55, ["2.78", "", "1.90", "", "2.79"])
    p.dimstring("h", [0.22, 3.80, 3.92, 7.93], -0.40, ["3.58", "", "4.01"])
    return p

def t5_kg():
    p = base("Two storeys T5 · basement (WU)", garage=False)
    p.stairs(*STAIR, n=15, up="E", label="cellar flight under the main flight")
    p.room("Cellar hall", 0.22, 4.18, 7.93, 6.40, lx=3.0, ly=5.9, area=12.8, sub="")
    p.room("Plant room", 0.22, 0.36, 3.80, 4.06, lx=2.0, ly=2.2, sub="heat pump · tank · electrics · Hebeanlage")
    p.room("Laundry", 3.92, 0.36, 7.93, 4.06, lx=5.9, ly=2.2, sub="washer · dryer · drying")
    p.room("Hobby / fitness", 0.22, 6.52, 3.80, YS, lx=2.0, ly=9.5, sub="light well south")
    p.room("Store", 3.92, 6.52, 7.93, YS, lx=5.9, ly=9.5, sub="light well east · food · bikes · garden")
    p.wall(3.80, 0.36, 3.92, 4.06); p.wall(0.22, 4.06, 7.93, 4.18); p.wall(0.22, 6.40, 7.93, 6.52); p.wall(3.80, 6.52, 3.92, YS)
    p.door(1.00, 4.06, 1.90, 4.18, "W", "N"); p.door(6.00, 4.06, 6.90, 4.18, "E", "N"); p.door(1.00, 6.40, 1.90, 6.52, "W", "S"); p.door(6.00, 6.40, 6.90, 6.52, "E", "S")
    p._t("dim", 2.0, H+0.24, "light well", "note"); p._t("dim", W+0.22, 10.2, "light well", "note", rot=-90)
    p._r("win", 1.0, H-0.36, 3.0, H, "win-new"); p._r("win", W-0.36, 9.0, W, 11.4, "win-new")
    p.appliance("Plant room", 0.35, 0.45, 1.05, 1.15, "Heat pump"); p.appliance("Plant room", 1.25, 0.45, 2.05, 1.25, "Tank"); p.furn("Plant room", 2.40, 0.45, 3.60, 0.85, "Electrics")
    p.appliance("Laundry", 4.05, 0.45, 4.70, 1.10, "Washer"); p.appliance("Laundry", 4.80, 0.45, 5.45, 1.10, "Dryer"); p.furn("Laundry", 5.80, 0.45, 7.00, 0.95, "Sink / folding"); p.furn("Plant room", 2.40, 3.20, 3.15, 3.95, "Hebeanlage")
    p.furn("Hobby / fitness", 0.40, 8.30, 1.80, 9.10, "Treadmill"); p.furn("Hobby / fitness", 2.30, 11.80, 3.60, 12.60, "Weights")
    p.dimstring("v", [0.36, 4.06, 4.18, 6.40, 6.52, YS], -0.40, ["3.70", "", "2.22", "", "7.19"])
    return p

ALL = dict(t5_eg=t5_eg, t5_og=t5_og, t5_kg=t5_kg)
if __name__ == "__main__":
    for k, f in ALL.items():
        p = f(); issues = p.check()
        print(f"== {k}: {len(issues)} issues; rooms {[(n, round(v[4],1)) for n, v in p.rooms.items()]}")
        for i in issues: print("   -", i)
        for c in p.clearances:
            room, label, facing, dep, mn, cf = c
            flag = "✗" if dep + 0.005 < mn else ("(min ok)" if dep + 0.005 < cf else "")
            print(f"     · {room:22s} {label:28s} {facing:6s} {dep:5.2f} m  [min {mn:.2f} / comfort {cf:.2f}]  {flag}")
