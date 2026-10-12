"""Two-storey version: one stair, no set-back storey.
T1 = same plate 8.29 x 11.04 (master suite upstairs); T2 = 10.29 x 12.04 plate, master suite on the ground floor."""
from engine import Plan

def base(W, H, title):
    p = Plan(W, H, title)
    p.north(W+0.45, -0.35); p.scalebar(0.0, y=H+0.90)
    p.dimstring("h", [0, W], -0.85, [f"{W:.2f} outside"])
    return p

def entrance_strip(p, utility_s):
    """Hall, guest shower bath and utility beside the stair: identical in T1 and T2."""
    p.door(1.30, 0.0, 2.24, 0.36, "W", "S"); p._t("dim", 1.77, -0.14, "entrance", "note")
    p.stairs(0.22, 1.36, 1.22, 5.41, n=15, up="S", label="new stair 15 × 27 cm")
    p.room("Entrance hall", 0.22, 0.36, 3.12, 2.90, lx=1.9, ly=1.55, area=7.4, sub="")
    p.room("Guest bath", 1.34, 3.02, 3.00, 5.41, lx=2.0, ly=3.95, sub="")
    p.room("Utility", 0.22, 5.53, 3.00, utility_s, lx=1.6, ly=6.75, sub="")
    p.wall(1.22, 2.90, 3.12, 3.02); p.wall(1.22, 3.02, 1.34, 5.41); p.wall(0.22, 5.41, 3.00, 5.53)
    p.door(1.45, 2.90, 2.35, 3.02, "E", "N")              # guest bath, opens out; open leaf screens the WC from the hall
    p.door(3.00, 6.10, 3.12, 7.00, "S", "W")              # utility, opens in
    p.wardrobe("Entrance hall", 2.52, 0.36, 3.12, 1.86, label="Wardrobe 1.5")
    p.wc("Guest bath", 3.30, 1.34, "E")
    p.vanity("Guest bath", 2.50, 3.72, 3.00, 4.40, basins=1, wall="E", label="")
    p.shower("Guest bath", 1.34, 4.41, 2.34, 5.41, glass=("N","E"), entry="N")
    p.radiator("Guest bath", 2.92, 4.55, 3.00, 5.15)
    p.appliance("Utility", 0.30, 5.60, 0.95, 6.25, "W+D"); p.appliance("Utility", 0.30, 6.55, 0.95, 7.20, "Heat pump"); p.appliance("Utility", 1.15, 5.60, 1.85, 6.30, "Tank")
    p.furn("Utility", 2.05, 5.60, 2.95, 6.00, "Sink")

def kids_rooms(p, x_mid, x_e):
    """Two children's rooms north of the landing wall. Beds on the partition / east wall, desks centred under the windows."""
    p.room("Bedroom NW", 1.34, 0.36, x_mid, 4.49, lx=(1.34+x_mid)/2, ly=3.55)
    p.room("Bedroom NE", x_mid+0.12, 0.36, x_e, 4.49, lx=(x_mid+0.12+x_e)/2, ly=3.55)
    p.room("Linen", 0.22, 0.36, 1.22, 1.36, sub="")
    p.wall(1.22, 0.36, 1.34, 4.49); p.wall(x_mid, 0.36, x_mid+0.12, 4.49)
    p.door(1.22, 0.46, 1.34, 1.26, "N", "E", kind="open")
    p.door(1.60, 4.49, 2.50, 4.61, "W", "N")
    # NW: bed head on the partition (away from the stair), window and desk on the west part of the north wall
    p.window("N", 1.50, 2.90)
    p.bed("Bedroom NW", x_mid-2.0, 1.70, x_mid, 3.10, head="E", label="Bed 1.4 × 2.0"); p.nightstand("Bedroom NW", x_mid-0.42, 1.20, x_mid, 1.62)
    p.furn("Bedroom NW", 1.50, 0.36, 2.90, 0.96, "Desk"); p.chair("Bedroom NW", 2.0, 1.2, r=0.2)
    p.wardrobe("Bedroom NW", 2.70, 3.89, x_mid, 4.49, label=f"Wardrobe {x_mid-2.70:.1f}")
    # NE: bed head on the east wall, window and desk centred on the room's west part
    wn0 = x_mid + 0.12 + 0.40; p.window("N", wn0, wn0+1.40)
    p.bed("Bedroom NE", x_e-2.0, 1.70, x_e, 3.10, head="E", label="Bed 1.4 × 2.0"); p.nightstand("Bedroom NE", x_e-0.42, 1.20, x_e, 1.62)
    p.furn("Bedroom NE", wn0, 0.36, wn0+1.40, 0.96, "Desk"); p.chair("Bedroom NE", wn0+0.30, 1.2, r=0.2)
    p.wardrobe("Bedroom NE", x_mid+0.12+1.20, 3.89, x_e, 4.49, label=f"Wardrobe {x_e-(x_mid+0.12+1.20):.1f}")
    p.door(x_mid+0.20, 4.49, x_mid+1.10, 4.61, "E", "N")

# ---------------------------------------------------------------- T1: same plate, master upstairs
def t1_eg():
    p = base(8.29, 11.04, "Two storeys T1 · ground floor")
    p.window("N", 4.60, 6.40, note="kitchen window, sill 1.20"); p.window("E", 4.40, 6.40); p.window("S", 0.80, 2.80); p.window("S", 3.60, 6.60, note="terrace door 3.0 m, lift-slide")
    entrance_strip(p, 7.24)
    p.room("Living · reading nook", 0.22, 7.36, 3.12, 10.68, lx=1.85, ly=7.9, sub="")
    p.room("Living · dining · kitchen", 3.12, 0.36, 7.93, 10.68, lx=5.55, ly=6.6, area=49.6, sub="open plan, 59 m² with the nook")
    p.wall(3.00, 3.02, 3.12, 7.36); p.wall(0.22, 7.24, 3.12, 7.36)
    p.furn("Living · dining · kitchen", 3.12, 0.36, 3.72, 1.86, "Pantry", tall=True)
    p.kitchen("Living · dining · kitchen", 3.73, 0.36, 7.93, 0.96, sink=5.20, hob=7.00)
    p.furn("Living · dining · kitchen", 4.55, 2.10, 6.95, 3.30, "Island 2.4 × 1.2")
    p.table("Living · dining · kitchen", 4.90, 4.80, 6.90, 5.80, chairs=(3,3,0,0), label="Table")
    # seating in the south end, facing the garden door; TV on a low divider at the nook edge
    p.sofa("Living · dining · kitchen", 6.83, 8.00, 7.83, 10.00, back="E")
    p.sofa("Living · dining · kitchen", 4.00, 7.60, 6.00, 8.60, back="N")
    p.furn("Living · dining · kitchen", 5.00, 9.00, 6.00, 9.80, "Coffee table")
    p.furn("Living · dining · kitchen", 3.12, 8.40, 3.52, 10.00, "TV unit")
    p.furn("Living · reading nook", 0.80, 10.08, 2.30, 10.68, "Desk"); p.chair("Living · reading nook", 1.55, 9.78)
    p.furn("Living · reading nook", 0.22, 7.50, 0.62, 9.50, "Shelves", tall=True)
    p.furn("Living · reading nook", 1.30, 8.20, 2.10, 9.00, "Armchair")
    p.dimstring("v", [0.36, 2.90, 3.02, 5.41, 5.53, 7.24, 7.36, 10.68], -0.40, ["2.54", "", "2.39", "", "1.71", "", "3.32"])
    p.dimstring("h", [0.22, 3.00, 3.12, 7.93], 11.04+0.55, ["2.78", "", "4.81"])
    p.dimstring("h", [3.73, 7.93], -0.40, ["4.20 kitchen run"])
    return p

def t1_og():
    p = base(8.29, 11.04, "Two storeys T1 · upper floor")
    p.window("E", 5.30, 6.10); p.window("S", 1.00, 2.90); p.window("S", 5.90, 7.30)
    p.stairs(0.22, 1.36, 1.22, 5.41, n=15, up="S", label="new stair 15 × 27 cm")
    p.room("Landing", 0.22, 4.61, 5.44, 6.41, lx=3.0, ly=5.3, area=9.4, sub="incl. stair head")
    kids_rooms(p, 4.30, 7.93)
    p.room("Family bath", 5.56, 4.61, 7.93, 7.21, lx=6.65, ly=5.95, sub="")
    p.room("Master bedroom", 0.22, 6.53, 3.72, 10.68, lx=2.0, ly=7.1)
    p.room("Dressing", 3.84, 6.53, 5.44, 10.68, lx=4.94, ly=8.3, sub="")
    p.room("Master bath", 5.56, 7.33, 7.93, 10.68, lx=6.62, ly=8.85, sub="")
    p.wall(1.22, 4.49, 7.93, 4.61)
    p.wall(0.22, 6.41, 5.44, 6.53); p.wall(5.44, 4.61, 5.56, 10.68); p.wall(5.56, 7.21, 7.93, 7.33); p.wall(3.72, 6.53, 3.84, 10.68)
    p.door(5.44, 4.80, 5.56, 5.70, "N", "E")            # family bath, opens in
    p.door(4.50, 6.41, 5.40, 6.53, "E", "S")            # landing -> dressing, opens into the dressing
    p.door(3.72, 9.50, 3.84, 10.40, "S", "W")           # dressing -> master bedroom, at the foot end
    p.door(5.44, 7.60, 5.56, 8.50, "N", "E")            # dressing -> master bath, swing door into the bath
    # family bath 2.37 x 2.60
    p.vanity("Family bath", 5.56, 6.66, 7.03, 7.21, basins=2, wall="S", label="Double vanity 1.47")
    p.shower("Family bath", 7.03, 6.21, 7.93, 7.21, glass=("N","W"), entry="N")
    p.wc("Family bath", 7.50, 4.61, "S")
    p.radiator("Family bath", 5.56, 5.9, 5.64, 6.5)
    # master bedroom 3.50 x 4.15: head on the party wall, door at the foot end
    p.bed("Master bedroom", 0.22, 7.65, 2.22, 9.45, head="W", label="Bed 1.8 × 2.0")
    p.nightstand("Master bedroom", 0.22, 7.10, 0.72, 7.60); p.nightstand("Master bedroom", 0.22, 9.50, 0.72, 10.00)
    p.furn("Master bedroom", 3.32, 7.10, 3.72, 9.10, "Dresser / TV")
    # dressing 1.60 x 4.15: one-sided rail + end wardrobe
    p.wardrobe("Dressing", 3.84, 6.53, 4.44, 9.40, label="Wardrobe 2.9 m")
    p.wardrobe("Dressing", 4.44, 10.08, 5.44, 10.68, label="Wardrobe 1.0")
    # master bath 2.37 x 3.35
    p.tub("Master bath", 5.56, 9.93, 7.26, 10.68)
    p.shower("Master bath", 6.73, 7.33, 7.93, 8.33, glass=("S","W"), entry="W")
    p.vanity("Master bath", 7.38, 8.40, 7.93, 9.85, basins=2, wall="E", label="")
    p.wc("Master bath", 9.20, 5.56, "E")
    p.dimstring("v", [0.36, 4.49, 4.61, 6.41, 6.53, 10.68], -0.40, ["4.13", "", "1.80", "", "4.15"])
    p.dimstring("h", [0.22, 3.72, 3.84, 5.44, 5.56, 7.93], 11.04+0.55, ["3.50", "", "1.60", "", "2.37"])
    p.dimstring("h", [0.22, 1.22, 1.34, 4.30, 4.42, 7.93], -0.40, ["1.00", "", "2.96", "", "3.51"])
    return p

# ---------------------------------------------------------------- T2: 10.29 x 12.04 plate, master suite on the ground floor
def t2_eg():
    p = base(10.29, 12.04, "Two storeys T2 · ground floor")
    p.window("N", 5.20, 7.60, note="kitchen window, sill 1.20"); p.window("E", 3.40, 5.00); p.window("E", 5.40, 7.10, note="terrace door 1.7 m")
    p.window("S", 6.00, 9.00); p.window("S", 0.80, 2.20)
    entrance_strip(p, 7.48)
    p.room("Living · dining · kitchen", 3.12, 0.36, 9.93, 7.48, lx=8.2, ly=3.75, sub="")
    p.room("Master bath", 0.22, 7.60, 2.72, 11.68, lx=1.75, ly=9.35, sub="")
    p.room("Dressing", 2.84, 7.60, 5.14, 11.68, lx=3.99, ly=9.9, sub="")
    p.room("Master bedroom", 5.26, 7.60, 9.93, 11.68, lx=7.0, ly=8.15)
    p.wall(3.00, 3.02, 3.12, 7.48); p.wall(0.22, 7.48, 9.93, 7.60)
    p.wall(2.72, 7.60, 2.84, 11.68); p.wall(5.14, 7.60, 5.26, 11.68)
    p.door(3.30, 7.48, 4.20, 7.60, "E", "S")              # living -> dressing, opens into the dressing
    p.door(5.14, 7.80, 5.26, 8.70, "N", "E")              # dressing -> bedroom, foot end
    p.door(2.72, 7.80, 2.84, 8.70, "S", "W", kind="pocket")  # dressing -> bath, slides south
    p.furn("Living · dining · kitchen", 3.12, 0.36, 3.72, 1.86, "Pantry", tall=True)
    p.kitchen("Living · dining · kitchen", 3.73, 0.36, 9.33, 0.96, sink=6.40, hob=8.60, label="Kitchen run")
    p.furn("Living · dining · kitchen", 9.33, 0.36, 9.93, 0.96, "", tall=True); p._t("lab", 9.63, 1.15, "fridge / oven", "tiny")
    p.furn("Living · dining · kitchen", 4.20, 2.00, 6.60, 3.20, "Island 2.4 × 1.2")
    p.table("Living · dining · kitchen", 6.90, 4.60, 8.90, 5.60, chairs=(3,3,0,0), label="Table")
    p.sofa("Living · dining · kitchen", 4.30, 4.30, 6.30, 5.30, back="N")
    p.sofa("Living · dining · kitchen", 4.40, 5.40, 5.40, 7.40, back="W")
    p.furn("Living · dining · kitchen", 5.60, 5.60, 6.40, 6.40, "Coffee table")
    p.furn("Living · dining · kitchen", 5.60, 7.08, 7.00, 7.48, "TV")
    # master bath 2.50 x 4.08: shower NW, double vanity on the party wall, WC on the dressing wall, tub under the south window
    p.shower("Master bath", 0.22, 7.60, 1.42, 8.80, glass=("S","E"), entry="E")
    p.vanity("Master bath", 0.22, 9.00, 0.77, 10.50, basins=2, wall="W", label="Double vanity 1.5")
    p.wc("Master bath", 9.90, 2.72, "W")
    p.tub("Master bath", 0.40, 10.88, 2.20, 11.68)
    p.radiator("Master bath", 2.64, 10.2, 2.72, 10.8)
    # dressing 2.30 x 4.08: rails on both long walls beyond the doors, end wardrobe, 1.10 m aisle
    p.wardrobe("Dressing", 2.84, 8.80, 3.44, 11.08, label="Wardrobe 2.3 m")
    p.wardrobe("Dressing", 4.54, 8.80, 5.14, 11.08, label="Wardrobe 2.3 m")
    p.wardrobe("Dressing", 3.44, 11.08, 4.54, 11.68, label="Wardrobe 1.1")
    # master bedroom 4.67 x 4.08: bed on the solid east wall, door at the foot end, garden window south
    p.bed("Master bedroom", 7.93, 8.60, 9.93, 10.40, head="E", label="Bed 1.8 × 2.0")
    p.nightstand("Master bedroom", 9.43, 8.05, 9.93, 8.55); p.nightstand("Master bedroom", 9.43, 10.45, 9.93, 10.95)
    p.furn("Master bedroom", 7.37, 8.80, 7.82, 10.20, "Bench", kind="bench")
    p.furn("Master bedroom", 5.26, 9.00, 5.66, 10.60, "Dresser / TV")
    p.furn("Master bedroom", 5.60, 11.08, 6.80, 11.68, "Desk"); p.chair("Master bedroom", 6.2, 10.8, r=0.2)
    p.dimstring("v", [0.36, 2.90, 3.02, 5.41, 5.53, 7.48, 7.60, 11.68], -0.40, ["2.54", "", "2.39", "", "1.95", "", "4.08"])
    p.dimstring("h", [0.22, 2.72, 2.84, 5.14, 5.26, 9.93], 12.04+0.55, ["2.50", "", "2.30", "", "4.67"])
    p.dimstring("h", [3.73, 9.33], -0.40, ["5.60 kitchen run"])
    return p

def t2_og():
    p = base(10.29, 12.04, "Two storeys T2 · upper floor")
    p.window("E", 5.40, 6.30); p.window("E", 8.80, 10.80); p.window("S", 1.00, 2.90); p.window("S", 6.60, 8.60)
    p.stairs(0.22, 1.36, 1.22, 5.41, n=15, up="S", label="new stair 15 × 27 cm")
    p.room("Landing", 0.22, 4.61, 6.98, 6.41, lx=3.3, ly=5.5, area=12.2, sub="incl. stair head")
    p.floor(5.92, 6.41, 6.98, 7.21)
    kids_rooms(p, 5.40, 9.93)
    p.room("Family bath", 7.10, 4.61, 9.93, 7.21, lx=8.5, ly=5.75, sub="")
    p.room("Bedroom 3 / guest", 0.22, 6.53, 3.72, 11.68, lx=2.2, ly=7.7)
    p.room("Laundry", 3.84, 6.53, 5.80, 8.20, lx=4.82, ly=7.15, sub="")
    p.room("Study / TV room", 5.92, 7.33, 9.93, 11.68, lx=7.6, ly=9.4)
    p.wall(1.22, 4.49, 9.93, 4.61)
    p.wall(0.22, 6.41, 5.92, 6.53); p.wall(6.98, 4.61, 7.10, 7.33); p.wall(5.92, 7.21, 9.93, 7.33)
    p.wall(3.72, 6.53, 3.84, 11.68); p.wall(5.80, 6.53, 5.92, 11.68); p.wall(3.84, 8.20, 5.80, 8.32)
    p.door(6.98, 5.10, 7.10, 6.00, "S", "W")            # family bath, opens out, leaf folds toward the bath wall
    p.door(1.50, 6.41, 2.40, 6.53, "W", "S")            # bedroom 3
    p.door(4.20, 6.41, 5.10, 6.53, "E", "N")            # laundry, opens to the landing
    p.door(6.05, 7.21, 6.95, 7.33, "E", "N")            # study, opens to the landing strip
    # family bath 2.83 x 2.60: double vanity and WC on the north wall, shower SW, tub under the east window
    p.vanity("Family bath", 7.40, 4.61, 8.90, 5.16, basins=2, wall="N", label="Double vanity 1.5")
    p.wc("Family bath", 9.55, 4.61, "S")
    p.shower("Family bath", 7.10, 6.21, 8.10, 7.21, glass=("N","E"), entry="N")
    p.tub("Family bath", 8.10, 6.41, 9.93, 7.21)
    p.furn("Landing", 2.70, 4.61, 4.10, 4.95, "Shelves")
    p.bed("Bedroom 3 / guest", 0.22, 8.40, 2.22, 10.20, head="W", label="Bed 1.8 × 2.0")
    p.nightstand("Bedroom 3 / guest", 0.22, 7.85, 0.72, 8.35); p.nightstand("Bedroom 3 / guest", 0.22, 10.25, 0.72, 10.75)
    p.wardrobe("Bedroom 3 / guest", 3.12, 6.53, 3.72, 9.00, label="Wardrobe 2.5")
    p.furn("Bedroom 3 / guest", 2.30, 11.08, 3.70, 11.68, "Desk"); p.chair("Bedroom 3 / guest", 3.0, 10.8, r=0.2)
    p.appliance("Laundry", 3.90, 7.50, 4.55, 8.15, "W+D"); p.furn("Laundry", 4.65, 7.50, 5.75, 8.15, "Shelves")
    p.wardrobe("Study / TV room", 7.00, 7.33, 9.00, 7.93, label="Wardrobe 2.0")
    p.furn("Study / TV room", 5.92, 8.60, 6.32, 10.00, "TV")
    p.sofa("Study / TV room", 8.93, 8.60, 9.93, 10.60, back="E", label="Day bed")
    p.furn("Study / TV room", 7.30, 11.08, 8.70, 11.68, "Desk"); p.chair("Study / TV room", 8.0, 10.8, r=0.2)
    p.dimstring("v", [0.36, 4.49, 4.61, 6.41, 6.53, 11.68], -0.40, ["4.13", "", "1.80", "", "5.15"])
    p.dimstring("h", [0.22, 3.72, 3.84, 5.80, 5.92, 9.93], 12.04+0.55, ["3.50", "", "1.96", "", "4.01"])
    p.dimstring("h", [0.22, 1.22, 1.34, 5.40, 5.52, 9.93], -0.40, ["1.00", "", "4.06", "", "4.41"])
    return p

ALL = dict(t1_eg=t1_eg, t1_og=t1_og, t2_eg=t2_eg, t2_og=t2_og)
if __name__ == "__main__":
    for k, f in ALL.items():
        p = f(); issues = p.check()
        print(f"== {k}: {len(issues)} issues; rooms {[(n, round(v[4],1)) for n, v in p.rooms.items()]}")
        for i in issues: print("   -", i)
        for c in p.clearances:
            room, label, facing, dep, mn, cf = c
            flag = "✗" if dep + 0.005 < mn else ("(min ok)" if dep + 0.005 < cf else "")
            print(f"     · {room:22s} {label:28s} {facing:6s} {dep:5.2f} m  [min {mn:.2f} / comfort {cf:.2f}]  {flag}")
