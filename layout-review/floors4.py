"""T4: the plot's two-storey maximum for Altkönigstraße 122 (Oberursel): GRZ 0.25 on 966.6 m² = 241.65 m² for the pair,
120.8 m² per house; boundary garages fix the width at 8.29 m, so the house grows in depth; the 3 m Abstandsfläche at the east rear corner
caps the depth at 14.07 m (t = 5.00 to 19.07), 116.6 m² per house.
East half drawn (party wall west, garage on the east side for y 0 to 7.42); the west half is its mirror."""
from engine import Plan
W, H = 8.29, 14.07
GARAGE = dict(x0=8.29, y0=0.0, x1=8.29+4.81, y1=7.42)   # on the boundary beside the front part of the house

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

def entrance_strip(p):
    """Hall with the main stair, guest WC, cupboard, cellar-stair lobby: the strip on the party wall."""
    p.door(1.40, 0.0, 2.34, 0.36, "W", "S"); p._t("dim", 1.87, -0.14, "entrance", "note")
    p.stairs(0.22, 1.36, 1.22, 5.41, n=15, up="S", label="main stair · cellar flight below")
    p.room("Entrance hall", 0.22, 0.36, 3.12, 2.90, lx=2.05, ly=1.55, area=7.4, sub="")
    p.room("Guest WC", 1.34, 3.02, 3.00, 4.40, lx=1.9, ly=3.35, sub="")
    p.room("Cupboard", 1.34, 4.52, 3.00, 5.41, lx=2.17, ly=5.0, sub="")
    p.room("Cellar stair lobby", 0.22, 5.53, 3.00, 6.70, lx=1.75, ly=6.15, sub="")
    p.wall(1.22, 2.90, 3.12, 3.02); p.wall(1.22, 3.02, 1.34, 5.41); p.wall(1.34, 4.40, 3.00, 4.52); p.wall(1.22, 5.41, 3.00, 5.53)
    p.wall(0.22, 6.70, 3.12, 6.82)
    p.door(1.45, 2.90, 2.35, 3.02, "E", "N")              # guest WC, opens out; the open leaf screens the WC
    p.door(3.00, 4.60, 3.12, 5.35, "N", "E", kind="open")  # cupboard, folding doors from the living side
    p.door(3.00, 5.70, 3.12, 6.60, "S", "E")              # lobby door, opens to the kitchen side
    p._t("lab", 0.72, 5.25, "down", "tiny"); p.L["fix"].append(f'<line x1="{0.72*64:.1f}" y1="{4.70*64:.1f}" x2="{0.72*64:.1f}" y2="{5.45*64:.1f}" class="arrow"/>')
    p.wardrobe("Entrance hall", 2.52, 0.36, 3.12, 1.86, label="Wardrobe 1.5")
    p.wc("Guest WC", 1.80, 4.40, "N"); p.vanity("Guest WC", 2.50, 3.10, 3.00, 3.60, basins=1, wall="E", label="")
    p.furn("Cupboard", 1.34, 4.52, 3.00, 5.41, "", tall=True)
    p.furn("Cellar stair lobby", 1.40, 5.60, 2.90, 5.95, "Coats · boots")

def t4_eg():
    p = base("Two storeys T4 · ground floor · 8.29 × 14.07")
    p.window("N", 4.60, 7.00, note="kitchen window, sill 1.20"); p.window("E", 12.30, 13.30); p.window("S", 0.80, 4.40, note="glass front 3.6 m: lift-slide 3.0 + fixed pane"); p.window("S", 5.20, 7.40)
    entrance_strip(p)
    p.room("Living · dining · kitchen", 3.12, 0.36, 7.93, 13.35, lx=4.5, ly=7.2, area=48.7, sub="67 m² with the lounge")
    p.room("Living · lounge", 0.22, 6.82, 3.12, 13.35, lx=1.7, ly=11.9, sub="")
    p.room("Bedroom EG", 4.73, 9.95, 7.93, 13.35, lx=6.45, ly=10.28, sub="")
    p.room("En suite", 5.93, 7.95, 7.93, 9.83, lx=6.95, ly=9.25, sub="")
    p.wall(3.00, 3.02, 3.12, 6.82)
    p.wall(4.61, 9.95, 4.73, 13.35); p.wall(4.73, 9.83, 7.93, 9.95); p.wall(5.81, 7.95, 5.93, 9.83); p.wall(5.93, 7.83, 7.93, 7.95)
    p.door(7.93, 1.60, 8.29, 2.50, "N", "W"); p._t("dim", W+0.22, 2.05, "door from the garage", "note", rot=-90)
    p.door(4.61, 12.30, 4.73, 13.20, "S", "W")            # living -> bedroom EG, at the foot end, opens to the living
    p.door(6.80, 9.83, 7.70, 9.95, "E", "N")              # bedroom -> en suite, opens into the en suite
    # kitchen 4.2 m on the north wall, pantry column, island
    p.furn("Living · dining · kitchen", 3.12, 0.36, 3.72, 1.86, "Pantry", tall=True)
    p.kitchen("Living · dining · kitchen", 3.73, 0.36, 7.93, 0.96, sink=5.80, hob=4.30)
    p.furn("Living · dining · kitchen", 7.33, 1.00, 7.93, 1.50, "Boots", tall=False)
    p.furn("Living · dining · kitchen", 4.30, 2.10, 6.70, 3.30, "Island 2.4 × 1.2")
    p.table("Living · dining · kitchen", 4.60, 4.80, 6.60, 5.80, chairs=(3,3,0,0), label="Table")
    # lounge: sofas in the south-west, TV on the bedroom wall, terrace door free
    p.sofa("Living · lounge", 0.22, 8.90, 1.22, 10.90, back="W")
    p.sofa("Living · dining · kitchen", 3.30, 8.20, 5.30, 9.20, back="N")
    p.furn("Living · lounge", 1.60, 9.70, 2.60, 10.50, "Coffee table")
    p.furn("Living · dining · kitchen", 4.21, 10.10, 4.61, 11.70, "TV")
    p.furn("Living · lounge", 0.22, 6.90, 0.62, 8.40, "Shelves", tall=True)
    # bedroom EG 3.20 x 3.40 with en suite 2.00 x 1.48: bed on the east wall under no window, south window
    p.bed("Bedroom EG", 5.93, 10.55, 7.93, 12.15, head="E", label="Bed 1.6 × 2.0")
    p.nightstand("Bedroom EG", 7.51, 10.05, 7.93, 10.47)
    p.wardrobe("Bedroom EG", 4.73, 9.95, 5.33, 11.95, label="Wardrobe 2.0")
    p.furn("Bedroom EG", 4.80, 12.75, 6.00, 13.35, "Desk"); p.chair("Bedroom EG", 5.4, 12.48, r=0.2)
    p.shower("En suite", 7.03, 7.95, 7.93, 8.85, glass=("S","W"), entry="S")
    p.wc("En suite", 6.65, 7.95, "S"); p.vanity("En suite", 5.93, 9.00, 6.43, 9.60, basins=1, wall="W", label="")
    p.dimstring("v", [0.36, 2.90, 3.02, 4.40, 4.52, 5.41, 5.53, 6.70, 6.82, 13.35], -0.40, ["2.54", "", "1.38", "", "0.89", "", "1.17", "", "6.53"])
    p.dimstring("h", [0.22, 4.61, 4.73, 7.93], H+0.55, ["4.39", "", "3.20"])
    p.dimstring("h", [3.73, 7.93], -0.40, ["4.20 kitchen run"])
    return p

def t4_og():
    p = base("Two storeys T4 · upper floor", garage=False)
    p.window("N", 1.50, 2.90); p.window("N", 4.82, 6.22); p.window("E", 7.30, 8.70); p.window("E", 10.60, 12.60); p.window("S", 1.00, 2.90); p.window("S", 5.20, 7.40)
    p.stairs(0.22, 1.36, 1.22, 5.41, n=15, up="S", label="main stair")
    p.room("Linen", 0.22, 0.36, 1.22, 1.36, sub="")
    p.room("Bedroom NW", 1.34, 0.36, 4.30, 4.90, lx=2.82, ly=3.9)
    p.room("Bedroom NE", 4.42, 0.36, 7.93, 4.90, lx=6.17, ly=3.9)
    p.room("Landing", 0.22, 5.02, 5.88, 6.82, lx=3.0, ly=5.75, area=10.2, sub="incl. stair head")
    p.room("Laundry", 6.00, 5.02, 7.93, 6.82, lx=6.6, ly=5.5, sub="")
    p.room("Dressing", 0.22, 6.94, 3.72, 9.33, lx=1.97, ly=8.15, sub="")
    p.room("Master bedroom", 0.22, 9.45, 3.72, 13.35, lx=1.65, ly=9.85, sub="")
    p.room("Family bath", 3.84, 6.94, 7.93, 9.30, lx=5.9, ly=8.1, sub="")
    p.room("Master bath", 3.84, 9.42, 7.93, 13.35, lx=5.6, ly=11.6, sub="incl. WC room")
    p.wall(1.22, 0.36, 1.34, 4.90); p.wall(1.22, 4.90, 7.93, 5.02); p.wall(4.30, 0.36, 4.42, 4.90)
    p.wall(5.88, 5.02, 6.00, 6.82); p.wall(0.22, 6.82, 7.93, 6.94); p.wall(3.72, 6.94, 3.84, 13.35); p.wall(0.22, 9.33, 3.72, 9.45); p.wall(3.84, 9.30, 7.93, 9.42)
    p.wall(4.94, 9.42, 5.06, 10.90); p.wall(3.84, 10.90, 5.06, 11.02)
    p.door(1.22, 0.46, 1.34, 1.26, "N", "E", kind="open")
    p.door(1.60, 4.90, 2.50, 5.02, "W", "N"); p.door(4.50, 4.90, 5.40, 5.02, "E", "N")
    p.door(5.88, 5.30, 6.00, 6.20, "N", "W")            # laundry, opens to the landing
    p.door(1.50, 6.82, 2.40, 6.94, "W", "S")            # landing -> dressing
    p.door(4.50, 6.82, 5.40, 6.94, "W", "S")            # landing -> family bath
    p.door(2.60, 9.33, 3.50, 9.45, "E", "S")            # dressing -> master bedroom, foot end
    p.door(3.72, 12.35, 3.84, 13.25, "S", "E")          # bedroom -> master bath
    p.door(4.00, 10.90, 4.80, 11.02, "W", "S")          # WC room, opens out into the bath
    # children's rooms: beds on the partitions, desks under the north windows
    p.bed("Bedroom NW", 2.30, 1.70, 4.30, 3.10, head="E", label="Bed 1.4 × 2.0"); p.nightstand("Bedroom NW", 3.88, 1.20, 4.30, 1.62)
    p.furn("Bedroom NW", 1.50, 0.36, 2.90, 0.96, "Desk"); p.chair("Bedroom NW", 2.0, 1.2, r=0.2)
    p.wardrobe("Bedroom NW", 2.70, 4.30, 4.30, 4.90, label="Wardrobe 1.6")
    p.bed("Bedroom NE", 5.93, 1.70, 7.93, 3.10, head="E", label="Bed 1.4 × 2.0"); p.nightstand("Bedroom NE", 7.51, 1.20, 7.93, 1.62)
    p.furn("Bedroom NE", 4.82, 0.36, 6.22, 0.96, "Desk"); p.chair("Bedroom NE", 5.12, 1.2, r=0.2)
    p.wardrobe("Bedroom NE", 5.62, 4.30, 7.93, 4.90, label="Wardrobe 2.3")
    p.appliance("Laundry", 6.10, 6.10, 6.75, 6.75, "W+D"); p.furn("Laundry", 7.00, 5.10, 7.85, 6.70, "Shelves", tall=True)
    # dressing 3.50 x 2.39: rails on the south and north walls, 1.19 m aisle
    p.wardrobe("Dressing", 0.22, 8.73, 2.40, 9.33, label="Wardrobe 2.2"); p.wardrobe("Dressing", 2.70, 6.94, 3.72, 7.54, label="Wardrobe 1.0"); p.wardrobe("Dressing", 0.22, 6.94, 1.30, 7.54, label="Wardrobe 1.1")
    # master bedroom 3.50 x 3.90: head on the party wall, door at the foot end
    p.bed("Master bedroom", 0.22, 10.50, 2.22, 12.30, head="W", label="Bed 1.8 × 2.0")
    p.nightstand("Master bedroom", 0.22, 9.95, 0.72, 10.45); p.nightstand("Master bedroom", 0.22, 12.35, 0.72, 12.85)
    p.furn("Master bedroom", 3.32, 10.50, 3.72, 12.20, "Dresser / TV")
    # family bath 4.09 x 2.36: tub under the east window, shower south-west, double vanity south, WC north
    p.tub("Family bath", 7.13, 7.10, 7.93, 8.90)
    p.shower("Family bath", 3.84, 8.30, 4.84, 9.30, glass=("N","E"), entry="N")
    p.vanity("Family bath", 5.00, 8.75, 6.60, 9.30, basins=2, wall="S", label="")
    p.wc("Family bath", 6.40, 6.94, "S"); p.radiator("Family bath", 3.84, 7.2, 3.92, 7.8)
    # master bath 4.09 x 3.93: WC room, tub under the south window, 1.2 x 1.2 shower, double vanity on the north wall
    p.wc("Master bath", 4.39, 9.42, "S"); p._t("lab", 4.45, 10.6, "WC room", "tiny")
    p.tub("Master bath", 6.13, 12.55, 7.93, 13.35)
    p.shower("Master bath", 6.73, 9.42, 7.93, 10.62, glass=("S","W"), entry="S")
    p.vanity("Master bath", 5.26, 9.42, 6.61, 9.97, basins=2, wall="N", label="")
    p.furn("Master bath", 3.84, 11.90, 4.24, 12.25, "Bench"); p.radiator("Master bath", 7.85, 10.8, 7.93, 11.4)
    p.dimstring("v", [0.36, 4.90, 5.02, 6.82, 6.94, 9.33, 9.45, 13.35], -0.40, ["4.54", "", "1.80", "", "2.39", "", "3.90"])
    p.dimstring("h", [0.22, 3.72, 3.84, 7.93], H+0.55, ["3.50", "", "4.09"])
    p.dimstring("h", [0.22, 1.22, 1.34, 4.30, 4.42, 7.93], -0.40, ["1.00", "", "2.96", "", "3.51"])
    return p

def t4_kg():
    p = base("Two storeys T4 · basement (WU)", garage=False)
    p.stairs(0.22, 1.36, 1.22, 5.41, n=15, up="S", label="cellar flight, under the main stair")
    p.room("Cellar hall", 1.22, 0.36, 3.00, 6.82, lx=2.1, ly=3.2, area=12.3, sub="")
    p.room("Plant room", 3.12, 0.36, 5.52, 3.60, lx=4.3, ly=2.4, sub="heat pump · tank")
    p.room("Store", 5.64, 0.36, 7.93, 3.60, lx=6.8, ly=2.4, sub="food · bikes")
    p.room("Laundry", 3.12, 3.72, 7.93, 6.82, lx=5.5, ly=5.9, sub="washer · dryer · drying · Hebeanlage")
    p.room("Hobby / fitness", 0.22, 6.94, 3.72, 13.35, lx=1.97, ly=9.5, sub="light well south")
    p.room("Store 2", 3.84, 6.94, 7.93, 13.35, lx=5.9, ly=9.5, sub="light well east · seasonal · garden")
    p.wall(3.00, 0.36, 3.12, 6.82); p.wall(3.12, 3.60, 7.93, 3.72); p.wall(5.52, 0.36, 5.64, 3.60)
    p.wall(0.22, 6.82, 7.93, 6.94); p.wall(3.72, 6.94, 3.84, 13.35)
    p.door(3.00, 1.60, 3.12, 2.50, "N", "E"); p.door(3.00, 4.80, 3.12, 5.70, "N", "E")
    p.door(5.52, 1.60, 5.64, 2.50, "N", "E"); p.door(1.50, 6.82, 2.40, 6.94, "W", "S"); p.door(5.00, 6.82, 5.90, 6.94, "E", "S")
    p._t("dim", 2.0, H+0.24, "light well", "note"); p._t("dim", W+0.22, 10.2, "light well", "note", rot=-90)
    p._r("win", 1.0, H-0.36, 3.0, H, "win-new"); p._r("win", W-0.36, 9.0, W, 11.4, "win-new")
    p.appliance("Plant room", 3.25, 0.45, 3.95, 1.15, "Heat pump"); p.appliance("Plant room", 4.15, 0.45, 4.95, 1.25, "Tank"); p.furn("Plant room", 3.25, 2.80, 4.45, 3.20, "Electrics")
    p.appliance("Laundry", 3.25, 3.80, 3.90, 4.45, "Washer"); p.appliance("Laundry", 4.00, 3.80, 4.65, 4.45, "Dryer"); p.furn("Laundry", 5.00, 3.80, 6.20, 4.30, "Sink / folding"); p.furn("Laundry", 7.00, 5.90, 7.80, 6.70, "Hebeanlage")
    p.furn("Hobby / fitness", 0.40, 8.30, 1.80, 9.10, "Treadmill"); p.furn("Hobby / fitness", 2.30, 11.80, 3.60, 12.60, "Weights")
    p.dimstring("v", [0.36, 3.60, 3.72, 6.82, 6.94, 13.35], -0.40, ["3.24", "", "3.10", "", "6.41"])
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
