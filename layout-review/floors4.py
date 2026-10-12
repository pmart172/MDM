"""T4: the plot's two-storey maximum for Altkönigstraße 122 (Oberursel): GRZ 0.25 on 966.6 m² = 241.65 m² for the pair,
120.8 m² per house; boundary garages fix the width at 8.29 m, so the house grows in depth; the 3 m Abstandsfläche at the east rear corner
caps the depth at 14.07 m (t = 5.00 to 19.07), 116.6 m² per house.
East half drawn (party wall west, garage on the east side for y 0 to 7.42); the west half is its mirror.
Second iteration after the independent review: rooms reach the inner face of the south wall (y 13.71), the cellar flight is reached
from the hall through its own corridor, the ground-floor bedroom is entered through a wardrobe bay off the dining zone."""
from engine import Plan
W, H = 8.29, 14.07
YS = H - 0.36                                            # inner face of the south wall, 13.71
GARAGE = dict(x0=8.29, y0=0.0, x1=8.29+4.81, y1=7.42)   # on the boundary beside the front part of the house

def area(rect, *holes):
    """Rectangle area minus the given hole rectangles (used for L-shaped rooms and rooms with a stair in them)."""
    a = (rect[2]-rect[0])*(rect[3]-rect[1])
    for h in holes: a -= (h[2]-h[0])*(h[3]-h[1])
    return round(a, 1)

def base(title, garage=True):
    p = Plan(W, H, title, outside=dict(x0=0.0, y0=-0.3, x1=W+5.2, y1=H+0.3) if garage else None)
    p.north(W+0.45, -0.35); p.scalebar(0.0, y=H+0.90)
    p.dimstring("h", [0, W], -0.85, [f"{W:.2f} outside"])
    if garage:
        g = GARAGE
        p.L["outside"].append(f'<rect x="{g["x0"]*64:.1f}" y="{g["y0"]*64:.1f}" width="{(g["x1"]-g["x0"])*64:.1f}" height="{(g["y1"]-g["y0"])*64:.1f}" class="void"/>')
        p._t("outside", (g["x0"]+g["x1"])/2, 3.4, "double garage on the boundary", "tiny"); p._t("outside", (g["x0"]+g["x1"])/2, 3.75, "4.8–6.9 × 7.42, roof at EG + 2.57", "tiny")
        p._t("outside", (g["x0"]+g["x1"])/2, 4.1, "(east half: follows the boundary jog)", "tiny")
    return p

STAIR = (0.22, 1.36, 1.22, 5.41)   # main flight up to the south; the cellar flight runs underneath it, down to the north

def entrance_strip(p):
    """The strip on the party wall: hall with the main stair, a 0.95 m corridor beside the stair to the cellar-stair lobby,
    guest WC on the corridor (door on its long side), lobby with the head of the cellar flight."""
    p.door(1.40, 0.0, 2.34, 0.36, "E", "S"); p._t("dim", 1.87, -0.14, "entrance", "note")
    p.stairs(*STAIR, n=15, up="S", label="main stair · cellar flight below")
    p.room("Entrance hall", 0.22, 0.36, 3.42, 2.90, lx=2.2, ly=1.75, area=area((0.22,0.36,3.42,2.90), (0.22,1.36,1.22,2.90)), sub="open to the kitchen")
    p.room("Corridor", 1.34, 2.90, 2.29, 5.53, lx=1.815, ly=5.0, sub="")
    p.room("Guest WC", 2.41, 3.02, 3.30, 5.41, lx=2.855, ly=4.0, sub="")
    p.room("Cellar stair lobby", 0.22, 5.53, 3.30, 6.70, lx=1.95, ly=6.1, sub="")
    p.wall(1.22, 2.90, 1.34, 5.41)                       # stair wall: main flight above, cellar flight below
    p.wall(2.29, 2.90, 3.30, 3.02); p.wall(2.29, 3.02, 2.41, 5.41); p.wall(2.29, 5.41, 3.30, 5.53)
    p.wall(0.22, 6.70, 3.30, 6.82); p.wall(3.30, 2.90, 3.42, 6.82)
    p.door(2.29, 3.60, 2.41, 4.50, "N", "W")              # guest WC, opens out into the corridor (barrier-free rule); the leaf shields the WC from the hall
    p.door(3.30, 5.70, 3.42, 6.60, "S", "E")              # lobby door, opens to the dining side
    p._t("lab", 0.72, 5.25, "down", "tiny"); p.L["fix"].append(f'<line x1="{0.72*64:.1f}" y1="{4.70*64:.1f}" x2="{0.72*64:.1f}" y2="{5.45*64:.1f}" class="arrow"/>')
    p.wardrobe("Entrance hall", 2.82, 0.36, 3.42, 1.86, label="Wardrobe 1.5")
    p.wc("Guest WC", 2.855, 5.41, "N"); p.vanity("Guest WC", 2.55, 3.02, 3.15, 3.47, basins=1, wall="N", label="")

def kids_rooms(p, x_mid, x_e):
    p.room("Closet", 0.22, 0.36, 1.22, 1.36, sub="")
    p.room("Bedroom NW", 1.34, 0.36, x_mid, 4.90, lx=(1.34+x_mid)/2, ly=3.9)
    p.room("Bedroom NE", x_mid+0.12, 0.36, x_e, 4.90, lx=(x_mid+0.12+x_e)/2, ly=3.9)

def t4_eg():
    p = base("Two storeys T4 · ground floor · 8.29 × 14.07")
    p.window("N", 4.60, 7.00, note="kitchen window, sill 1.20"); p.window("E", 8.10, 8.90, note="en suite, obscured glass")
    p.window("S", 0.80, 4.40, note="glass front 3.6 m: lift-slide 3.0 + fixed pane"); p.window("S", 5.50, 7.40, note="bedroom window 1.9 m")
    entrance_strip(p)
    LDK, LNG, BED, ENS = "Living · dining · kitchen", "Living · lounge", "Bedroom EG", "En suite"
    a_ldk = area((3.42,0.36,7.93,YS), (4.61,7.83,7.93,YS)); a_lng = area((0.22,6.82,3.30,YS))
    p.room(LDK, 3.42, 0.36, 7.93, YS, lx=4.9, ly=7.0, area=a_ldk, sub=f"{a_ldk+a_lng:.0f} m² with the lounge")
    p.room(LNG, 0.22, 6.82, 3.30, YS, lx=1.76, ly=12.4, sub="")
    p.room(BED, 4.73, 7.95, 7.93, YS, lx=6.3, ly=10.2, area=area((4.73,9.95,7.93,YS)) + area((4.73,7.95,5.81,9.95)), sub="incl. the entry bay")
    p.room(ENS, 5.93, 7.95, 7.93, 9.83, lx=6.45, ly=9.2, sub="")
    p.wall(4.61, 7.95, 4.73, YS); p.wall(4.61, 7.83, 7.93, 7.95); p.wall(5.81, 7.95, 5.93, 9.95); p.wall(5.93, 9.83, 7.93, 9.95)
    p.door(7.93, 1.60, 8.29, 2.50, "N", "W"); p._t("dim", W+0.22, 2.05, "door from the garage", "note", rot=-90)
    p.door(4.61, 8.75, 4.73, 9.65, "S", "E")              # dining zone -> bedroom bay, opens into the bay against its west wall
    p.door(5.81, 8.93, 5.93, 9.83, "S", "E")              # bay -> en suite, opens flat against the en suite's south wall
    # kitchen along the whole north wall: tall column (fridge, oven) at the hall end, 3.91 m worktop under the window, island
    p.furn(LDK, 3.42, 0.36, 4.02, 0.96, "Fridge · oven", tall=True)
    p.kitchen(LDK, 4.02, 0.36, 7.93, 0.96, sink=5.20, hob=6.80)
    p.furn(LDK, 4.50, 2.10, 6.90, 3.30, "Island 2.4 × 1.2")
    p.table(LDK, 4.90, 5.10, 6.90, 6.10, chairs=(3,3,0,0), label="Table")
    # living: two sofas and the coffee table in the lounge, TV on the bedroom wall, glass front free
    p.sofa(LNG, 0.22, 9.30, 1.22, 11.30, back="W")
    p.sofa(LNG, 1.30, 7.90, 3.30, 8.90, back="N")
    p.furn(LNG, 1.60, 9.90, 2.60, 10.70, "Coffee table")
    p.furn(LDK, 4.21, 10.40, 4.61, 12.00, "TV")
    p.furn(LNG, 0.22, 6.90, 0.62, 8.40, "Shelves", tall=True)
    # bedroom EG 3.20 x 3.76 behind a 1.08 x 2.00 bay with a wardrobe; bed on the east wall, no window behind the head
    p.wardrobe(BED, 4.73, 7.95, 5.81, 8.55, label="Wardrobe 1.1")
    p.bed(BED, 5.93, 10.60, 7.93, 12.20, head="E", label="Bed 1.6 × 2.0")
    p.nightstand(BED, 7.51, 10.10, 7.93, 10.52); p.nightstand(BED, 7.51, 12.28, 7.93, 12.70)
    p.wardrobe(BED, 4.73, 12.30, 5.33, YS, label="Wardrobe 1.4")
    p.chair(BED, 6.55, 13.15, r=0.30); p._t("lab", 6.55, 13.6, "armchair", "tiny")
    # en suite 2.00 x 1.88 off the bay: walk-in shower 1.00 x 0.90 in the north-west corner, WC on the north wall, basin on the south wall
    p.shower(ENS, 5.93, 7.95, 6.93, 8.85, glass=("S","E"), entry="S")
    p.wc(ENS, 7.40, 7.95, "S"); p.vanity(ENS, 7.13, 9.33, 7.93, 9.83, basins=1, wall="S", label="")
    p.dimstring("v", [0.36, 2.90, 3.02, 5.41, 5.53, 6.70, 6.82, YS], -0.40, ["2.54", "", "2.39", "", "1.17", "", "6.89"])
    p.dimstring("h", [0.22, 4.61, 4.73, 7.93], H+0.55, ["4.39", "", "3.20"])
    p.dimstring("h", [0.22, 1.22, 1.34, 2.29, 2.41, 3.30, 3.42, 7.93], -0.40, ["1.00", "", "0.95", "", "0.89", "", "4.51 kitchen wall"])
    return p

def t4_og():
    p = base("Two storeys T4 · upper floor", garage=False)
    p.window("N", 1.60, 3.00); p.window("N", 4.80, 6.60); p.window("E", 7.30, 8.70); p.window("E", 10.80, 12.60); p.window("S", 1.00, 2.90); p.window("S", 5.20, 7.40)
    p.stairs(*STAIR, n=15, up="S", label="main stair")
    kids_rooms(p, 4.30, 7.93)
    p.room("Landing", 0.22, 5.02, 5.88, 6.82, lx=3.0, ly=5.75, area=area((0.22,5.02,5.88,6.82), (0.22,5.02,1.34,5.41)), sub="")
    p.room("Laundry", 6.00, 5.02, 7.93, 6.82, lx=6.6, ly=5.5, sub="")
    p.room("Dressing", 0.22, 6.94, 3.72, 9.33, lx=1.97, ly=8.15, sub="")
    p.room("Master bedroom", 0.22, 9.45, 3.72, YS, lx=1.97, ly=9.95, sub="")
    p.room("Family bath", 3.84, 6.94, 7.93, 9.30, lx=5.9, ly=8.1, sub="")
    p.room("Master bath", 3.84, 9.42, 7.93, YS, lx=5.6, ly=11.6, sub="incl. WC room")
    p.wall(1.22, 0.36, 1.34, 5.41); p.wall(1.22, 4.90, 7.93, 5.02); p.wall(4.30, 0.36, 4.42, 4.90)
    p.wall(5.88, 5.02, 6.00, 6.82); p.wall(0.22, 6.82, 7.93, 6.94); p.wall(3.72, 6.94, 3.84, YS); p.wall(0.22, 9.33, 3.72, 9.45); p.wall(3.84, 9.30, 7.93, 9.42)
    p.wall(4.94, 9.42, 5.06, 10.90); p.wall(3.84, 10.90, 5.06, 11.02)
    p.door(1.22, 0.46, 1.34, 1.26, "N", "E", kind="open"); p._t("lab", 0.72, 1.27, "for NW", "tiny")
    p.door(1.60, 4.90, 2.50, 5.02, "W", "N"); p.door(4.50, 4.90, 5.40, 5.02, "E", "N")
    p.door(5.88, 5.20, 6.00, 6.10, "N", "E")            # laundry, opens into the laundry (the landing stays free)
    p.door(2.60, 6.82, 3.50, 6.94, "E", "S")            # landing -> dressing
    p.door(4.50, 6.82, 5.40, 6.94, "W", "S")            # landing -> family bath
    p.door(2.60, 9.33, 3.50, 9.45, "E", "S")            # dressing -> master bedroom, in line with the landing door
    p.door(3.72, 12.50, 3.84, 13.40, "S", "E")          # bedroom -> master bath
    p.door(4.00, 10.90, 4.80, 11.02, "W", "S")          # WC room, opens out into the bath
    # children's rooms: beds on the partitions, desks under the north windows
    p.bed("Bedroom NW", 2.30, 1.70, 4.30, 3.10, head="E", label="Bed 1.4 × 2.0"); p.nightstand("Bedroom NW", 3.88, 1.20, 4.30, 1.62)
    p.furn("Bedroom NW", 1.60, 0.36, 3.00, 0.96, "Desk"); p.chair("Bedroom NW", 2.0, 1.2, r=0.2)
    p.wardrobe("Bedroom NW", 2.70, 4.30, 4.30, 4.90, label="Wardrobe 1.6")
    p.bed("Bedroom NE", 5.93, 1.70, 7.93, 3.10, head="E", label="Bed 1.4 × 2.0"); p.nightstand("Bedroom NE", 7.51, 1.20, 7.93, 1.62)
    p.furn("Bedroom NE", 4.90, 0.36, 6.50, 0.96, "Desk"); p.chair("Bedroom NE", 5.3, 1.2, r=0.2)
    p.wardrobe("Bedroom NE", 5.62, 4.30, 7.93, 4.90, label="Wardrobe 2.3")
    p.appliance("Laundry", 6.10, 6.15, 6.75, 6.80, "W+D"); p.furn("Laundry", 7.00, 5.10, 7.85, 6.70, "Shelves", tall=True)
    # dressing 3.50 x 2.39: 2.18 m rails on both long walls, 1.19 m aisle, doors in line at the east end
    p.wardrobe("Dressing", 0.22, 8.73, 2.40, 9.33, label="Wardrobe 2.2"); p.wardrobe("Dressing", 0.22, 6.94, 2.40, 7.54, label="Wardrobe 2.2")
    # master bedroom 3.50 x 4.26: head on the party wall (double-leaf wall, see the text), door at the foot end
    p.bed("Master bedroom", 0.22, 10.70, 2.22, 12.50, head="W", label="Bed 1.8 × 2.0")
    p.nightstand("Master bedroom", 0.22, 10.15, 0.72, 10.65); p.nightstand("Master bedroom", 0.22, 12.55, 0.72, 13.05)
    p.furn("Master bedroom", 3.32, 10.60, 3.72, 12.30, "Dresser / TV")
    # family bath 4.09 x 2.36: tub under the east window, shower south-west, double vanity south, WC north
    p.tub("Family bath", 7.13, 7.10, 7.93, 8.90)
    p.shower("Family bath", 3.84, 8.30, 4.84, 9.30, glass=("N","E"), entry="N")
    p.vanity("Family bath", 5.00, 8.75, 6.60, 9.30, basins=2, wall="S", label="")
    p.wc("Family bath", 6.40, 6.94, "S"); p.radiator("Family bath", 3.84, 7.2, 3.92, 7.8)
    # master bath 4.09 x 4.29: WC room, tub under the south window, 1.2 x 1.2 shower clear of the east window, 1.6 m double vanity
    p.wc("Master bath", 4.39, 9.42, "S"); p._t("lab", 4.45, 10.6, "WC room", "tiny")
    p.tub("Master bath", 6.13, 12.91, 7.93, YS)
    p.shower("Master bath", 6.73, 9.42, 7.93, 10.62, glass=("S","W"), entry="S")
    p.vanity("Master bath", 5.10, 9.42, 6.70, 9.97, basins=2, wall="N", label="")
    p.furn("Master bath", 3.84, 11.90, 4.24, 12.25, "Bench"); p.radiator("Master bath", 3.84, 11.10, 3.92, 11.80)
    p.dimstring("v", [0.36, 4.90, 5.02, 6.82, 6.94, 9.33, 9.45, YS], -0.40, ["4.54", "", "1.80", "", "2.39", "", "4.26"])
    p.dimstring("h", [0.22, 3.72, 3.84, 7.93], H+0.55, ["3.50", "", "4.09"])
    p.dimstring("h", [0.22, 1.22, 1.34, 4.30, 4.42, 7.93], -0.40, ["1.00", "", "2.96", "", "3.51"])
    return p

def t4_kg():
    p = base("Two storeys T4 · basement (WU)", garage=False)
    p.stairs(*STAIR, n=15, up="S", label="cellar flight, under the main stair")
    p.room("Cellar hall", 0.22, 0.36, 3.00, 6.82, lx=2.17, ly=5.9, area=area((0.22,0.36,3.00,6.82), (0.22,1.36,1.34,5.41)), sub="")
    p.room("Plant room", 3.12, 0.36, 5.52, 3.60, lx=4.3, ly=2.4, sub="heat pump · tank · Hebeanlage")
    p.room("Store", 5.64, 0.36, 7.93, 3.60, lx=6.8, ly=2.4, sub="food · bikes")
    p.room("Laundry", 3.12, 3.72, 7.93, 6.82, lx=5.5, ly=5.9, sub="washer · dryer · drying")
    p.room("Hobby / fitness", 0.22, 6.94, 3.72, YS, lx=1.97, ly=9.5, sub="light well south")
    p.room("Store 2", 3.84, 6.94, 7.93, YS, lx=5.9, ly=9.5, sub="light well east · seasonal · garden")
    p.wall(1.22, 1.36, 1.34, 5.41)                       # stairwell wall beside the flight, continuous with the ground floor
    p.wall(3.00, 0.36, 3.12, 6.82); p.wall(3.12, 3.60, 7.93, 3.72); p.wall(5.52, 0.36, 5.64, 3.60)
    p.wall(0.22, 6.82, 7.93, 6.94); p.wall(3.72, 6.94, 3.84, YS)
    p.door(3.00, 1.60, 3.12, 2.50, "N", "E"); p.door(3.00, 4.80, 3.12, 5.70, "N", "E")
    p.door(6.30, 3.60, 7.20, 3.72, "W", "N")             # store from the laundry, not through the plant room
    p.door(1.50, 6.82, 2.40, 6.94, "W", "S"); p.door(5.00, 6.82, 5.90, 6.94, "E", "S")
    p._t("dim", 2.0, H+0.24, "light well", "note"); p._t("dim", W+0.22, 10.2, "light well", "note", rot=-90)
    p._r("win", 1.0, H-0.36, 3.0, H, "win-new"); p._r("win", W-0.36, 9.0, W, 11.4, "win-new")
    p.appliance("Plant room", 3.25, 0.45, 3.95, 1.15, "Heat pump"); p.appliance("Plant room", 4.15, 0.45, 4.95, 1.25, "Tank")
    p.furn("Plant room", 3.25, 3.20, 4.45, 3.60, "Electrics"); p.furn("Plant room", 4.70, 2.80, 5.45, 3.55, "Hebeanlage")
    p.appliance("Laundry", 3.25, 3.80, 3.90, 4.45, "Washer"); p.appliance("Laundry", 4.00, 3.80, 4.65, 4.45, "Dryer"); p.furn("Laundry", 5.00, 3.80, 6.20, 4.30, "Sink / folding")
    p.furn("Hobby / fitness", 0.40, 8.30, 1.80, 9.10, "Treadmill"); p.furn("Hobby / fitness", 2.30, 11.80, 3.60, 12.60, "Weights")
    p.dimstring("v", [0.36, 3.60, 3.72, 6.82, 6.94, YS], -0.40, ["3.24", "", "3.10", "", "6.77"])
    return p

ALL = dict(t4_eg=t4_eg, t4_og=t4_og, t4_kg=t4_kg)
if __name__ == "__main__":
    for k, f in ALL.items():
        p = f(); issues = p.check()
        print(f"== {k}: {len(issues)} issues; rooms {[(n, round(v[4],1)) for n, v in p.rooms.items()]}")
        for i in issues: print("   -", i)
        for c in p.clearances:
            room, label, facing, dep, mn, cf = c
            flag = "✗" if dep + 0.005 < mn else ("(min ok)" if dep + 0.005 < cf else "")
            print(f"     · {room:22s} {label:28s} {facing:6s} {dep:5.2f} m  [min {mn:.2f} / comfort {cf:.2f}]  {flag}")
