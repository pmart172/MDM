"""T3: two storeys plus basement at the GRZ/GFZ limit. Drawn for a 370 m² half-plot at GRZ 0.4 / GFZ 0.8:
plate 12.29 x 12.04 m (148 m² gross per storey). Living room across the garden front, master suite north-east,
entrance hall and stair north-west on the party wall, cellar flight under the main flight."""
from engine import Plan
W, H = 12.29, 12.04

def base(title):
    p = Plan(W, H, title)
    p.north(W+0.45, -0.35); p.scalebar(0.0, y=H+0.90)
    p.dimstring("h", [0, W], -0.85, [f"{W:.2f} outside"])
    return p

def t3_eg():
    p = base("Two storeys + basement T3 · ground floor")
    p.window("N", 4.00, 5.60, note="bath window, obscured"); p.window("E", 1.00, 3.00); p.window("E", 5.50, 7.50)
    p.window("S", 1.00, 2.80, note="kitchen window"); p.window("S", 4.00, 7.00, note="terrace door 3.0 m, lift-slide"); p.window("S", 9.00, 11.50)
    p.door(1.40, 0.0, 2.34, 0.36, "W", "S"); p._t("dim", 1.87, -0.14, "entrance", "note")
    p.stairs(0.22, 1.36, 1.22, 5.41, n=15, up="S", label="main stair · cellar flight below")
    p.room("Entrance hall", 1.22, 0.36, 3.60, 4.44, lx=1.9, ly=3.3, area=8.1, sub="")
    p.room("Guest WC", 2.50, 0.36, 3.60, 2.40, lx=3.05, ly=1.55, sub="")
    p.room("Master bath", 3.72, 0.36, 6.12, 4.44, lx=4.92, ly=2.3, sub="")
    p.room("Dressing", 6.24, 0.36, 8.04, 4.44, lx=7.04, ly=2.3, sub="")
    p.room("Master bedroom", 8.16, 0.36, 11.93, 4.44, lx=10.0, ly=3.45)
    p.room("Cellar stair", 0.22, 5.53, 1.34, 6.70, lx=0.78, ly=6.3, sub="")
    p.room("Living · dining · kitchen", 0.22, 4.56, 11.93, 11.68, lx=6.3, ly=9.3, area=81.0, sub="open plan, full garden front")
    p.wall(3.60, 0.36, 3.72, 4.44); p.wall(6.12, 0.36, 6.24, 4.44); p.wall(8.04, 0.36, 8.16, 4.44)
    p.wall(3.72, 4.44, 11.93, 4.56); p.wall(2.38, 0.36, 2.50, 2.40); p.wall(2.38, 2.40, 3.60, 2.52)
    p.wall(1.22, 4.44, 1.34, 5.53); p.wall(1.34, 5.53, 1.46, 6.70); p.wall(0.22, 6.70, 1.46, 6.82)
    p.door(2.38, 1.45, 2.50, 2.35, "S", "W")              # guest WC, opens out into the hall
    p.door(6.40, 4.44, 7.30, 4.56, "W", "N")              # living -> dressing, opens into the dressing
    p.door(6.12, 1.90, 6.24, 2.80, "N", "W")              # dressing -> bath, opens into the bath
    p.door(8.04, 3.30, 8.16, 4.20, "N", "E")              # dressing -> bedroom, foot end
    p.door(1.34, 5.75, 1.46, 6.65, "N", "E")              # cellar stair lobby, opens to the kitchen
    p._t("lab", 0.72, 5.25, "down", "tiny"); p.L["fix"].append(f'<line x1="{0.72*64:.1f}" y1="{4.70*64:.1f}" x2="{0.72*64:.1f}" y2="{5.45*64:.1f}" class="arrow"/>')
    # hall
    p.wardrobe("Entrance hall", 3.00, 2.80, 3.60, 4.30, label="Wardrobe 1.5")
    p.wc("Guest WC", 3.05, 0.36, "S"); p.vanity("Guest WC", 2.95, 1.98, 3.45, 2.40, basins=1, wall="S", label="")
    # master bath 2.40 x 4.08: tub under the north window, double vanity on the hall wall, shower south-east, WC south
    p.tub("Master bath", 3.90, 0.36, 5.70, 1.16)
    p.vanity("Master bath", 3.72, 1.40, 4.27, 3.00, basins=2, wall="W", label="")
    p.shower("Master bath", 4.92, 3.24, 6.12, 4.44, glass=("N","W"), entry="N")
    p.wc("Master bath", 4.20, 4.44, "N")
    p.radiator("Master bath", 6.04, 0.50, 6.12, 1.10)
    # dressing 1.80 x 4.08: rail on the bedroom wall, end wardrobe north
    p.wardrobe("Dressing", 7.44, 0.36, 8.04, 3.20, label="Wardrobe 2.8 m")
    p.wardrobe("Dressing", 6.24, 0.36, 7.44, 0.96, label="Wardrobe 1.2")
    p.furn("Dressing", 6.24, 1.10, 6.64, 2.90, "Shelves")
    # master bedroom 3.77 x 4.08: bed on the north wall (no street window), east window, door at the foot end
    p.bed("Master bedroom", 9.10, 0.36, 10.90, 2.36, head="N", label="Bed 1.8 × 2.0")
    p.nightstand("Master bedroom", 8.55, 0.36, 9.05, 0.86); p.nightstand("Master bedroom", 10.95, 0.36, 11.45, 0.86)
    p.furn("Master bedroom", 9.20, 2.47, 10.80, 2.92, "Bench", kind="bench")
    p.furn("Master bedroom", 9.20, 4.04, 10.80, 4.44, "Dresser / TV")
    p.chair("Master bedroom", 11.5, 3.6, r=0.32); p._t("lab", 11.5, 4.15, "armchair", "tiny")
    # kitchen on the party wall, island, dining under the suite wall, lounge south-east
    p.kitchen("Living · dining · kitchen", 0.22, 6.86, 0.82, 11.06, sink=None, hob=None, label="Kitchen run")
    p._r("fix", 0.32, 8.70, 0.72, 9.50, "basin", rx=3); p._c("fix", 0.52, 9.10, 0.03, "drain")
    for dx,dy in ((-0.13,-0.15),(0.13,-0.15),(-0.13,0.15),(0.13,0.15)): p._c("fix", 0.52+dx, 10.30+dy, 0.08, "hob")
    p.furn("Living · dining · kitchen", 0.22, 11.08, 0.82, 11.68, "", tall=True); p._t("lab", 0.52, 11.0, "fridge", "tiny")
    p.furn("Living · dining · kitchen", 1.92, 7.40, 3.12, 9.80, "Island 2.4 × 1.2")
    p.table("Living · dining · kitchen", 4.60, 6.20, 6.60, 7.20, chairs=(3,3,0,0), label="Table")
    p.sofa("Living · dining · kitchen", 8.60, 8.40, 9.60, 10.40, back="W")
    p.sofa("Living · dining · kitchen", 9.80, 10.60, 11.80, 11.60, back="S")
    p.furn("Living · dining · kitchen", 10.00, 8.80, 10.80, 9.60, "Coffee table")
    p.furn("Living · dining · kitchen", 11.53, 8.50, 11.93, 9.90, "TV")
    p.furn("Living · dining · kitchen", 3.90, 4.56, 5.90, 4.96, "Sideboard")
    p.dimstring("v", [0.36, 4.44, 4.56, 11.68], -0.40, ["4.08", "", "7.12"])
    p.dimstring("h", [0.22, 1.22, 1.34, 3.60, 3.72, 6.12, 6.24, 8.04, 8.16, 11.93], -0.40, ["1.00", "", "2.26", "", "2.40", "", "1.80", "", "3.77"])
    p.dimstring("h", [0.22, 11.93], H+0.55, ["11.71 clear"])
    return p

def t3_og():
    p = base("Two storeys + basement T3 · upper floor")
    p.window("N", 1.60, 3.00); p.window("N", 5.90, 7.30); p.window("N", 9.80, 11.20); p.window("E", 1.00, 3.00); p.window("E", 8.00, 10.00)
    p.window("S", 1.00, 2.90); p.window("S", 6.00, 8.00); p.window("S", 9.50, 11.50)
    p.stairs(0.22, 1.36, 1.22, 5.41, n=15, up="S", label="main stair")
    p.room("Landing", 0.22, 4.61, 11.93, 6.41, lx=6.0, ly=5.5, area=21.1, sub="incl. stair head")
    p.room("Linen", 0.22, 0.36, 1.22, 1.36, sub="")
    p.room("Bedroom NW", 1.34, 0.36, 5.20, 4.49, lx=3.27, ly=3.55)
    p.room("Bedroom N", 5.32, 0.36, 9.10, 4.49, lx=7.21, ly=3.55)
    p.room("Family bath", 9.22, 0.36, 11.93, 4.49, lx=10.57, ly=2.5, sub="")
    p.room("Bedroom 3 / guest", 0.22, 6.53, 3.72, 11.68, lx=2.2, ly=7.7)
    p.room("Shower room", 3.84, 6.53, 5.30, 9.20, lx=4.8, ly=7.75, sub="")
    p.room("Family room / TV", 5.42, 6.53, 8.52, 11.68, lx=6.97, ly=8.0)
    p.room("Study", 8.64, 6.53, 11.93, 11.68, lx=10.3, ly=8.0)
    p.wall(1.22, 0.36, 1.34, 4.49); p.wall(1.22, 4.49, 11.93, 4.61); p.wall(5.20, 0.36, 5.32, 4.49); p.wall(9.10, 0.36, 9.22, 4.49)
    p.wall(0.22, 6.41, 11.93, 6.53); p.wall(3.72, 6.53, 3.84, 11.68); p.wall(5.30, 6.53, 5.42, 11.68); p.wall(8.52, 6.53, 8.64, 11.68); p.wall(3.84, 9.20, 5.30, 9.32)
    p.door(1.22, 0.46, 1.34, 1.26, "N", "E", kind="open")
    p.door(1.60, 4.49, 2.50, 4.61, "W", "N"); p.door(5.50, 4.49, 6.40, 4.61, "E", "N"); p.door(9.40, 4.49, 10.30, 4.61, "W", "N")
    p.door(1.50, 6.41, 2.40, 6.53, "W", "S"); p.door(4.20, 6.41, 5.10, 6.53, "E", "N"); p.door(6.80, 6.41, 7.70, 6.53, "E", "S"); p.door(9.00, 6.41, 9.90, 6.53, "W", "S")
    # bedrooms NW and N: beds on the partitions, desks centred under the windows
    p.bed("Bedroom NW", 3.20, 1.70, 5.20, 3.10, head="E", label="Bed 1.4 × 2.0"); p.nightstand("Bedroom NW", 4.78, 1.20, 5.20, 1.62)
    p.furn("Bedroom NW", 1.60, 0.36, 3.00, 0.96, "Desk"); p.chair("Bedroom NW", 2.3, 1.2, r=0.2)
    p.wardrobe("Bedroom NW", 2.70, 3.89, 5.20, 4.49, label="Wardrobe 2.5")
    p.bed("Bedroom N", 7.10, 1.70, 9.10, 3.10, head="E", label="Bed 1.4 × 2.0"); p.nightstand("Bedroom N", 8.68, 1.20, 9.10, 1.62)
    p.furn("Bedroom N", 5.90, 0.36, 7.30, 0.96, "Desk"); p.chair("Bedroom N", 6.2, 1.2, r=0.2)
    p.wardrobe("Bedroom N", 6.60, 3.89, 9.10, 4.49, label="Wardrobe 2.5")
    # family bath 2.71 x 4.13: tub under the north window, double vanity on the partition, shower south-east, WC
    p.tub("Family bath", 9.40, 0.36, 11.20, 1.16)
    p.vanity("Family bath", 9.22, 1.40, 9.77, 3.00, basins=2, wall="W", label="")
    p.shower("Family bath", 10.73, 3.29, 11.93, 4.49, glass=("N","W"), entry="N")
    p.wc("Family bath", 11.60, 1.40, "S"); p.radiator("Family bath", 11.85, 2.30, 11.93, 2.90)
    # bedroom 3 / guest
    p.bed("Bedroom 3 / guest", 0.22, 8.40, 2.22, 10.20, head="W", label="Bed 1.8 × 2.0")
    p.nightstand("Bedroom 3 / guest", 0.22, 7.85, 0.72, 8.35); p.nightstand("Bedroom 3 / guest", 0.22, 10.25, 0.72, 10.75)
    p.wardrobe("Bedroom 3 / guest", 3.12, 6.53, 3.72, 9.00, label="Wardrobe 2.5")
    p.furn("Bedroom 3 / guest", 2.30, 11.08, 3.70, 11.68, "Desk"); p.chair("Bedroom 3 / guest", 3.0, 10.8, r=0.2)
    # shower room 1.46 x 2.27 for the guest room and the family room
    p.shower("Shower room", 4.40, 8.30, 5.30, 9.20, glass=("N","W"), entry="N")
    p.wc("Shower room", 4.90, 6.53, "S"); p.vanity("Shower room", 3.84, 7.40, 4.24, 8.00, basins=1, wall="W", label="")
    # family room / TV: sofa under the south window, TV on the shower-room wall
    p.sofa("Family room / TV", 6.00, 10.60, 8.00, 11.60, back="S")
    p.furn("Family room / TV", 5.42, 8.60, 5.82, 10.00, "TV")
    p.furn("Family room / TV", 7.90, 6.70, 8.50, 9.70, "Shelves", tall=True)
    p.furn("Family room / TV", 6.40, 8.80, 7.20, 9.60, "Table")
    # study
    p.furn("Study", 10.33, 8.20, 11.93, 8.80, "Desk 1.6"); p.chair("Study", 11.1, 9.1, r=0.2)
    p.wardrobe("Study", 8.64, 7.50, 9.24, 10.10, label="Shelves 2.6"); p.sofa("Study", 8.90, 10.60, 10.90, 11.60, back="S", label="Day bed")
    p.dimstring("v", [0.36, 4.49, 4.61, 6.41, 6.53, 11.68], -0.40, ["4.13", "", "1.80", "", "5.15"])
    p.dimstring("h", [0.22, 1.22, 1.34, 5.20, 5.32, 9.10, 9.22, 11.93], -0.40, ["1.00", "", "3.86", "", "3.78", "", "2.71"])
    p.dimstring("h", [0.22, 3.72, 3.84, 5.30, 5.42, 8.52, 8.64, 11.93], H+0.55, ["3.50", "", "1.46", "", "3.10", "", "3.29"])
    return p

def t3_kg():
    p = base("Two storeys + basement T3 · basement")
    p.stairs(0.22, 1.36, 1.22, 5.41, n=15, up="S", label="cellar flight, under the main stair")
    p.room("Cellar hall", 1.22, 0.36, 3.60, 6.80, lx=2.4, ly=3.0, area=14.3, sub="bikes · pram")
    p.room("Corridor", 3.72, 5.65, 11.93, 6.80, lx=7.8, ly=6.3, sub="")
    p.room("Plant room", 3.72, 0.36, 6.72, 2.90, lx=5.2, ly=2.1, sub="heat pump · tank · electrics")
    p.room("Laundry", 3.72, 3.02, 6.72, 5.53, lx=5.2, ly=4.9, sub="washer · dryer · drying")
    p.room("Store", 6.84, 0.36, 8.80, 5.53, lx=7.82, ly=3.0, sub="food store")
    p.room("Hobby / fitness", 8.92, 0.36, 11.93, 5.53, lx=10.4, ly=3.0, sub="light well east")
    p.room("Guest / office", 0.22, 6.92, 5.40, 11.68, lx=2.8, ly=9.0, sub="light well south")
    p.room("Store 2", 5.52, 6.92, 11.93, 11.68, lx=8.7, ly=9.3, sub="general · seasonal · garden")
    p.wall(3.60, 0.36, 3.72, 6.80); p.wall(3.72, 2.90, 6.72, 3.02); p.wall(6.72, 0.36, 6.84, 5.53); p.wall(8.80, 0.36, 8.92, 5.53)
    p.wall(3.72, 5.53, 11.93, 5.65); p.wall(0.22, 6.80, 11.93, 6.92); p.wall(5.40, 6.92, 5.52, 11.68)
    p.door(3.60, 1.60, 3.72, 2.50, "N", "E"); p.door(3.60, 3.80, 3.72, 4.70, "N", "E")
    p.door(7.30, 5.53, 8.20, 5.65, "E", "N"); p.door(10.00, 5.53, 10.90, 5.65, "E", "S")
    p.door(1.60, 6.80, 2.50, 6.92, "W", "S"); p.door(6.00, 6.80, 6.90, 6.92, "W", "S")
    p._t("dim", W+0.22, 3.0, "light well", "note", rot=-90); p._t("dim", 2.8, H+0.24, "light well", "note")
    p._r("win", W-0.36, 1.8, W, 4.2, "win-new"); p._r("win", 1.0, H-0.36, 4.6, H, "win-new")
    p.appliance("Plant room", 3.85, 0.45, 4.55, 1.15, "Heat pump"); p.appliance("Plant room", 4.75, 0.45, 5.55, 1.25, "Tank"); p.furn("Plant room", 5.80, 0.45, 6.60, 0.85, "Electrics")
    p.appliance("Laundry", 3.85, 3.10, 4.50, 3.75, "Washer"); p.appliance("Laundry", 4.60, 3.10, 5.25, 3.75, "Dryer"); p.furn("Laundry", 5.50, 3.10, 6.60, 3.60, "Sink / folding")
    p.furn("Hobby / fitness", 9.10, 0.50, 10.50, 1.30, "Treadmill"); p.furn("Hobby / fitness", 9.10, 4.60, 11.80, 5.40, "Bench / weights")
    p.sofa("Guest / office", 0.40, 10.60, 2.40, 11.60, back="S", label="Sofa bed"); p.furn("Guest / office", 3.80, 7.10, 5.30, 7.70, "Desk")
    p.dimstring("v", [0.36, 5.53, 5.65, 6.80, 6.92, 11.68], -0.40, ["5.17", "", "1.15", "", "4.76"])
    p.dimstring("h", [0.22, 1.22, 1.34, 3.60, 3.72, 6.72, 6.84, 8.80, 8.92, 11.93], -0.40, ["1.00", "", "2.26", "", "3.00", "", "1.96", "", "3.01"])
    return p

ALL = dict(t3_eg=t3_eg, t3_og=t3_og, t3_kg=t3_kg)
if __name__ == "__main__":
    for k, f in ALL.items():
        p = f(); issues = p.check()
        print(f"== {k}: {len(issues)} issues; rooms {[(n, round(v[4],1)) for n, v in p.rooms.items()]}")
        for i in issues: print("   -", i)
        for c in p.clearances:
            room, label, facing, dep, mn, cf = c
            flag = "✗" if dep + 0.005 < mn else ("(min ok)" if dep + 0.005 < cf else "")
            print(f"     · {room:22s} {label:28s} {facing:6s} {dep:5.2f} m  [min {mn:.2f} / comfort {cf:.2f}]  {flag}")
