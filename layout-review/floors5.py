"""T5, second iteration: the Rötha pattern on the Altkönigstraße plate. Bauwerk's upper floor is 12.50 m deep over an 11.00 m
ground floor, so the bedroom storey cantilevers 1.50 m over the garden glazing; the entrance sits beside the garage under the
upper floor; the straight stair runs across the house parallel to the street. Here: upper floor 8.29 × 14.07 (the plate T4 uses),
ground floor 8.29 × 12.57 with a 1.50 m overhang over the glass wall and a 1.39 × 2.32 m covered porch beside the garage;
no utility room on the ground floor; children's rooms of 16.8 and 18.8 m² over a 4.70 m entrance band; living room 45.6 m²."""
from engine import Plan
W, H_OG, H_EG = 8.29, 14.07, 12.57
OVER = H_OG - H_EG                                      # 1.50 m overhang of the upper floor
GARAGE = dict(x0=8.29, y0=0.0, x1=8.29+4.81, y1=7.42)
STAIR = (2.21, 5.18, 6.51, 6.18)                        # straight flight across the house: foot east by the entrance, head west
BAND = 5.06                                             # inner face of the wall behind the entrance band / children's rooms

def area(rect, *holes):
    a = (rect[2]-rect[0])*(rect[3]-rect[1])
    for h in holes: a -= (h[2]-h[0])*(h[3]-h[1])
    return round(a, 1)

def base(title, H, garage=True, overhang=False):
    p = Plan(W, H, title, outside=dict(x0=0.0, y0=-0.3, x1=W+5.2, y1=H_OG+0.3) if garage else None)
    p.north(W+0.45, -0.35); p.scalebar(0.0, y=H+0.90 + (OVER if overhang else 0))
    p.dimstring("h", [0, W], -0.85, [f"{W:.2f} outside"])
    if garage:
        g = GARAGE
        p.L["outside"].append(f'<rect x="{g["x0"]*64:.1f}" y="{g["y0"]*64:.1f}" width="{(g["x1"]-g["x0"])*64:.1f}" height="{(g["y1"]-g["y0"])*64:.1f}" class="void"/>')
        p._t("outside", (g["x0"]+g["x1"])/2, 3.4, "double garage on the boundary", "tiny"); p._t("outside", (g["x0"]+g["x1"])/2, 3.75, "4.8–6.9 × 7.42, roof at EG + 2.57", "tiny")
    if overhang:
        p.L["outside"].append(f'<rect x="0" y="{H*64:.1f}" width="{W*64:.1f}" height="{OVER*64:.1f}" class="void"/>')
        p._t("outside", W/2, H + 0.62, "upper floor above: 1.50 m overhang, covered terrace strip", "tiny")
        p._t("outside", W/2, H + 0.95, "glass wall in its shade, as at Rötha", "tiny")
    return p

def t5_eg():
    p = base("Two storeys T5 · ground floor · 8.29 × 12.57 under the 14.07 m upper floor", H_EG, overhang=True)
    YS = H_EG - 0.36                                   # 12.21
    p.window("N", 0.80, 2.80, note="bedroom window 2.0 m"); p.window("E", 8.20, 10.20, note="kitchen window, sill 1.20")
    p.window("S", 0.80, 4.40, note="glass wall 3.6 m: lift-slide 3.0 + fixed pane"); p.window("S", 5.40, 7.40, note="fixed glazing 2.0 m")
    # covered porch beside the garage: a 1.39 x 2.32 m notch in the north-east corner, the front door in its south wall
    p._r("floor", 6.90, 0.0, W, 2.32, "terrace", crisp=True); p.wall(6.54, 0.0, 6.90, 2.32); p.wall(6.54, 2.32, W, 2.68)
    p._t("lab", 7.6, 1.05, "covered", "tiny"); p._t("lab", 7.6, 1.35, "porch", "tiny"); p._t("dim", 7.6, -0.14, "entrance", "note")
    p.door(6.90, 2.32, 7.84, 2.68, "E", "S")              # front door, opens into the hall against the east wall
    p.door(7.93, 3.90, 8.29, 4.80, "S", "W"); p._t("dim", W+0.22, 4.35, "door from the garage", "note", rot=-90)
    p.stairs(*STAIR, n=15, up="W", label="straight flight parallel to the street · cellar flight below")
    p.screen(2.21, 6.18, 6.51, 6.30, h=1.0); p.floor(6.51, 5.18, 7.93, 6.30)
    # entrance band 4.70 m deep: ground-floor bedroom with en suite, guest WC, hall
    p.room("Bedroom EG", 0.22, 0.36, 3.30, BAND, lx=1.76, ly=3.7, sub="")
    p.room("En suite", 3.42, 0.36, 5.42, 2.56, lx=4.42, ly=1.55, sub="")
    p.room("Guest WC", 5.54, 0.36, 6.54, 2.56, lx=6.04, ly=1.3, sub="")
    p.room("Entrance hall", 3.42, 2.68, 7.93, BAND, lx=5.9, ly=3.9, area=area((3.42,2.68,7.93,BAND)) + area((6.51,5.18,7.93,6.30)), sub="incl. the stair foot")
    p.room("Cellar stair", 0.22, 5.18, 2.21, 6.18, lx=1.2, ly=5.55, sub="")
    LDK = "Living · dining · kitchen"
    p.room(LDK, 0.22, 6.30, 7.93, YS, lx=2.45, ly=11.55, sub="")
    p.wall(3.30, 0.36, 3.42, BAND); p.wall(3.42, 2.56, 6.54, 2.68); p.wall(5.42, 0.36, 5.54, 2.56)
    p.wall(0.22, BAND, 6.51, 5.18); p.wall(0.22, 6.18, 2.21, 6.30)
    p.door(3.30, 3.90, 3.42, 4.80, "S", "W")              # hall -> bedroom, opens into the bedroom against its south wall
    p.door(3.30, 1.50, 3.42, 2.40, "S", "E")              # bedroom -> en suite
    p.door(5.64, 2.56, 6.44, 2.68, "W", "S")              # guest WC, opens out into the hall
    p.door(0.90, 6.18, 1.80, 6.30, "W", "S")              # cellar-stair lobby, opens into the living room
    p._t("lab", 1.2, 5.95, "down", "tiny"); p.L["fix"].append(f'<line x1="{1.40*64:.1f}" y1="{5.80*64:.1f}" x2="{2.10*64:.1f}" y2="{5.80*64:.1f}" class="arrow"/>')
    # bedroom EG 3.08 x 4.70: bed on the party wall, wardrobe on the south wall, armchair at the window
    p.bed("Bedroom EG", 0.22, 1.30, 2.22, 2.90, head="W", label="Bed 1.6 × 2.0")
    p.nightstand("Bedroom EG", 0.22, 0.80, 0.64, 1.22); p.nightstand("Bedroom EG", 0.22, 2.98, 0.64, 3.40)
    p.wardrobe("Bedroom EG", 0.22, 4.46, 2.22, BAND, label="Wardrobe 2.0")
    p.chair("Bedroom EG", 2.80, 3.40, r=0.30); p._t("lab", 2.80, 3.85, "armchair", "tiny")
    p.shower("En suite", 3.42, 0.36, 4.42, 1.26, glass=("S","E"), entry="S")
    p.wc("En suite", 4.90, 0.36, "S"); p.vanity("En suite", 4.62, 2.06, 5.42, 2.56, basins=1, wall="S", label="")
    p.wc("Guest WC", 5.93, 0.36, "S"); p.vanity("Guest WC", 6.14, 1.40, 6.54, 2.00, basins=1, wall="E", label="")
    p.wardrobe("Entrance hall", 3.60, 2.68, 5.10, 3.28, label="Wardrobe 1.5"); p.furn("Entrance hall", 4.80, 4.56, 5.80, 4.96, "Bench")
    # living 7.71 x 5.91: kitchen on the east wall with the island, table beside the open flight, lounge at the glass wall
    p.kitchen(LDK, 7.33, 7.00, 7.93, 11.20, sink=9.20, hob=10.60, label="Run 4.2 m")
    p.furn(LDK, 7.33, 11.20, 7.93, 11.80, "", tall=True); p._t("lab", 7.0, 11.5, "fridge · oven", "tiny")
    p.furn(LDK, 5.13, 7.60, 6.33, 10.00, "Island 1.2 × 2.4")
    p.table(LDK, 2.30, 6.95, 4.30, 7.95, chairs=(3,3,0,0), label="Table")
    p.sofa(LDK, 0.22, 9.20, 1.22, 11.20, back="W")
    p.sofa(LDK, 1.60, 8.70, 3.60, 9.70, back="N")
    p.furn(LDK, 1.70, 10.20, 2.70, 11.00, "Coffee table")
    p.furn(LDK, 3.70, 9.90, 4.10, 11.50, "TV")
    p.dimstring("v", [0.36, BAND, 5.18, 6.18, 6.30, YS], -0.40, ["4.70", "", "1.00", "", "5.91"])
    p.dimstring("v", [H_EG, H_OG], -0.40, ["1.50"])
    p.dimstring("h", [0.22, 3.30, 3.42, 5.42, 5.54, 6.54, 6.90, W], -0.40, ["3.08", "", "2.00", "", "1.00", "", "porch"])
    p.dimstring("h", [0.22, 7.93], H_OG+0.55, ["7.71 living room, 5.91 deep"])
    return p

def t5_og():
    p = base("Two storeys T5 · upper floor · 8.29 × 14.07, children's rooms 16.8 and 18.8 m²", H_OG, garage=False)
    YS = H_OG - 0.36                                   # 13.71
    p.window("N", 1.20, 3.00); p.window("N", 5.00, 6.80); p.window("E", 5.40, 7.20, note="gallery window"); p.window("E", 7.70, 9.00, note="bath, obscured")
    p.window("S", 0.80, 3.80, note="bedroom window 3.0 m"); p.window("S", 6.20, 7.40, note="bath window over the tub")
    p.stairs(*STAIR, n=15, up="W", label="stair opening · arrival at the west end")
    p.room("Bedroom NW", 0.22, 0.36, 3.80, BAND, lx=2.0, ly=4.0, sub="")
    p.room("Bedroom NE", 3.92, 0.36, 7.93, BAND, lx=5.5, ly=4.0, sub="")
    p.room("Gallery", 0.22, 5.18, 7.93, 7.40, lx=4.36, ly=6.95, area=area((0.22,5.18,7.93,7.40), STAIR), sub="")
    p.room("Dressing", 0.22, 7.52, 4.32, 9.62, lx=1.6, ly=8.6, sub="")
    p.room("Master bedroom", 0.22, 9.74, 4.32, YS, lx=2.5, ly=10.2, sub="")
    p.room("Family bath", 4.44, 7.52, 7.93, 10.47, lx=6.3, ly=9.0, sub="")
    p.room("Master bath", 4.44, 10.59, 7.93, YS, lx=5.5, ly=12.0, sub="")
    p.wall(3.80, 0.36, 3.92, BAND); p.wall(0.22, BAND, 7.93, 5.18); p.wall(0.22, 7.40, 7.93, 7.52)
    p.wall(4.32, 7.52, 4.44, YS); p.wall(0.22, 9.62, 4.32, 9.74); p.wall(4.44, 10.47, 7.93, 10.59)
    p.door(0.60, BAND, 1.50, 5.18, "W", "N"); p.door(6.60, BAND, 7.50, 5.18, "E", "N")   # children's rooms from the ends of the gallery
    p.door(3.20, 7.40, 4.10, 7.52, "E", "S")              # gallery -> dressing
    p.door(3.20, 9.62, 4.10, 9.74, "E", "S")              # dressing -> master bedroom, in line
    p.door(4.32, 12.60, 4.44, 13.50, "S", "E")            # master bedroom -> master bath
    p.door(4.70, 7.40, 5.60, 7.52, "W", "S")              # gallery -> family bath
    # children's rooms 3.58 x 4.70 and 4.01 x 4.70: desks under the windows, beds on the outer walls, 2.2 and 2.4 m wardrobes
    p.bed("Bedroom NW", 0.22, 2.00, 2.22, 3.40, head="W", label="Bed 1.4 × 2.0"); p.nightstand("Bedroom NW", 0.22, 1.50, 0.64, 1.92)
    p.furn("Bedroom NW", 1.20, 0.36, 2.80, 0.96, "Desk"); p.chair("Bedroom NW", 2.0, 1.2, r=0.2)
    p.wardrobe("Bedroom NW", 1.60, 4.46, 3.80, BAND, label="Wardrobe 2.2")
    p.bed("Bedroom NE", 5.93, 2.00, 7.93, 3.40, head="E", label="Bed 1.4 × 2.0"); p.nightstand("Bedroom NE", 7.51, 1.50, 7.93, 1.92)
    p.furn("Bedroom NE", 5.00, 0.36, 6.60, 0.96, "Desk"); p.chair("Bedroom NE", 5.4, 1.2, r=0.2)
    p.wardrobe("Bedroom NE", 3.92, 4.46, 6.32, BAND, label="Wardrobe 2.4")
    p.chair("Gallery", 7.40, 6.90, r=0.30); p._t("lab", 7.40, 7.33, "reading chair", "tiny")
    # dressing 4.10 x 2.10: 2.8 m rails on both long walls, 0.90 aisle, both doors in line at the east end
    p.wardrobe("Dressing", 0.22, 7.52, 3.00, 8.12, label="Wardrobe 2.8"); p.wardrobe("Dressing", 0.22, 9.02, 3.00, 9.62, label="Wardrobe 2.8")
    # master bedroom 4.10 x 3.97: head on the party wall, south window, dresser and TV opposite, bath through the east wall
    p.bed("Master bedroom", 0.22, 10.95, 2.22, 12.75, head="W", label="Bed 1.8 × 2.0")
    p.nightstand("Master bedroom", 0.22, 10.40, 0.72, 10.90); p.nightstand("Master bedroom", 0.22, 12.80, 0.72, 13.30)
    p.furn("Master bedroom", 3.92, 10.70, 4.32, 12.30, "Dresser / TV")
    # master bath 3.49 x 3.12: tub under the south window, 1.2 x 1.2 shower, double vanity, WC
    p.tub("Master bath", 6.13, 12.91, 7.93, YS)
    p.shower("Master bath", 6.73, 10.59, 7.93, 11.79, glass=("S","W"), entry="S")
    p.vanity("Master bath", 4.44, 10.90, 4.99, 12.50, basins=2, wall="W", label="")
    p.wc("Master bath", 6.20, 10.59, "S")
    # family bath 3.49 x 2.95: tub under the east window, shower, double vanity, WC, stacked washer-dryer
    p.tub("Family bath", 7.13, 7.62, 7.93, 9.42)
    p.shower("Family bath", 4.44, 9.47, 5.44, 10.47, glass=("N","E"), entry="N")
    p.vanity("Family bath", 5.50, 9.92, 7.10, 10.47, basins=2, wall="S", label="")
    p.wc("Family bath", 6.00, 7.52, "S"); p.appliance("Family bath", 6.40, 7.52, 7.05, 8.17, "W+D")
    p.dimstring("v", [0.36, BAND, 5.18, 7.40, 7.52, 9.62, 9.74, YS], -0.40, ["4.70", "", "2.22", "", "2.10", "", "3.97"])
    p.dimstring("h", [0.22, 3.80, 3.92, 7.93], -0.40, ["3.58", "", "4.01"])
    p.dimstring("h", [0.22, 4.32, 4.44, 7.93], H_OG+0.55, ["4.10", "", "3.49"])
    return p

def t5_kg():
    p = base("Two storeys T5 · basement (WU) under the ground-floor footprint", H_EG, garage=False)
    YS = H_EG - 0.36
    p.stairs(*STAIR, n=15, up="W", label="cellar flight under the main flight · arrival at the east end")
    p.room("Plant room", 0.22, 0.36, 2.92, BAND, lx=1.57, ly=3.45, sub="heat pump · tank · electrics · Hebeanlage")
    p.room("Store", 3.04, 0.36, 5.42, BAND, lx=4.23, ly=2.6, sub="food · bikes")
    p.room("Laundry", 5.54, 0.36, 7.93, BAND, lx=6.73, ly=2.6, sub="washer · dryer · drying")
    p.room("Cellar hall", 0.22, 5.18, 7.93, 7.40, lx=4.36, ly=6.95, area=area((0.22,5.18,7.93,7.40), STAIR), sub="")
    p.room("Hobby / fitness", 0.22, 7.52, 3.80, YS, lx=2.0, ly=10.0, sub="light well south, under the overhang")
    p.room("Store 2", 3.92, 7.52, 7.93, YS, lx=5.9, ly=10.0, sub="light well east · seasonal · garden")
    p.wall(2.92, 0.36, 3.04, BAND); p.wall(5.42, 0.36, 5.54, BAND); p.wall(0.22, BAND, 7.93, 5.18); p.wall(0.22, 7.40, 7.93, 7.52); p.wall(3.80, 7.52, 3.92, YS)
    p.door(0.60, BAND, 1.50, 5.18, "W", "N"); p.door(6.60, BAND, 7.50, 5.18, "E", "N"); p.door(5.42, 1.20, 5.54, 2.10, "N", "W")
    p.door(1.00, 7.40, 1.90, 7.52, "W", "S"); p.door(6.00, 7.40, 6.90, 7.52, "E", "S")
    p._t("dim", 2.0, H_EG+0.24, "light well", "note"); p._t("dim", W+0.22, 10.2, "light well", "note", rot=-90)
    p._r("win", 1.0, H_EG-0.36, 3.0, H_EG, "win-new"); p._r("win", W-0.36, 9.0, W, 11.4, "win-new")
    p.appliance("Plant room", 0.35, 0.45, 1.05, 1.15, "Heat pump"); p.appliance("Plant room", 1.25, 0.45, 2.05, 1.25, "Tank")
    p.furn("Plant room", 0.35, 2.00, 0.75, 3.20, "Electrics"); p.furn("Plant room", 2.00, 4.20, 2.75, 4.95, "Hebeanlage")
    p.appliance("Laundry", 5.65, 0.45, 6.30, 1.10, "Washer"); p.appliance("Laundry", 6.40, 0.45, 7.05, 1.10, "Dryer"); p.furn("Laundry", 5.65, 4.40, 6.45, 4.90, "Sink / folding")
    p.furn("Hobby / fitness", 0.40, 8.60, 1.80, 9.40, "Treadmill"); p.furn("Hobby / fitness", 2.30, 11.00, 3.60, 11.80, "Weights")
    p.dimstring("v", [0.36, BAND, 5.18, 7.40, 7.52, YS], -0.40, ["4.70", "", "2.22", "", "4.69"])
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
