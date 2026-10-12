from engine import Plan

# ======================================================================= DG
DG_OUT = dict(x0=0.0, y0=-1.23, x1=8.29, y1=9.73)

def dg_base(title, s_window2=True):
    p = Plan(7.13, 8.20, title, outside=DG_OUT)
    p.set_back("dashed: floor below · tinted: set-back strips N 1.23 · E 1.16 · S 1.53 m")
    p.window("N", 0.66, 2.50); p.window("E", 1.04, 3.05); p.window("E", 4.96, 6.90); p.window("S", 0.80, 2.83)
    if s_window2: p.window("S", 4.10, 6.14)
    p.stairs(0.22, 0.35, 1.25, 2.60, n=13, up="S")
    p.void(1.25, 0.50, 2.10, 2.50, "landing / void")
    p.chimney(2.82, 0.35, 3.06, 1.95)
    p.wall(2.82, 1.95, 3.06, 3.64)
    p.north(7.13+0.45, -0.35); p.scalebar(0.0)
    p.dimstring("h", [0, 7.13], -0.85, ["7.13 outside"])
    p.dimstring("h", [0.22, 2.82, 3.06, 6.75], -0.40, ["2.60", "", "3.69"])
    return p

def dg_current():
    p = dg_base("Top floor as drawn today")
    p.room("Hall / stairs", 0.22, 0.35, 2.82, 3.64, lx=1.6, ly=3.1)
    p.room("Closet room", 3.06, 0.35, 6.75, 3.64, lx=4.9, ly=2.6)
    p.room("Bath", 0.22, 3.74, 3.35, 7.84, lx=2.1, ly=6.2)
    p.room("Bedroom", 3.45, 3.74, 6.75, 7.84, lx=5.9, ly=4.45)
    p.wall(0.22, 3.64, 6.75, 3.74); p.wall(3.35, 3.74, 3.45, 7.84)
    p.door(2.82, 2.03, 3.06, 2.93, "N", "E"); p.door(1.84, 3.64, 2.74, 3.74, "E", "S"); p.door(5.71, 3.64, 6.60, 3.74, "E", "S")
    p.wardrobe("Closet room", 3.06, 0.35, 6.75, 0.94); p.furn("Closet room", 3.97, 1.62, 5.43, 2.29, "Table"); p.wardrobe("Closet room", 3.06, 3.05, 5.62, 3.64)
    p.shower("Bath", 0.38, 3.74, 1.42, 5.53, glass=("E","S"), entry="E")
    p.wc("Bath", 6.0, 0.22, "E")
    p.vanity("Bath", 2.88, 3.78, 3.35, 5.76, basins=2, wall="E", label="")
    p.tub("Bath", 0.90, 6.85, 2.69, 7.65)
    p.bed("Bedroom", 3.45, 4.77, 5.43, 6.75, head="W", label="Bed 2.0 × 2.0")
    p.dimstring("h", [0.22, 3.35, 3.45, 6.75], 8.20+0.40, ["3.13", "", "3.30"])
    p.dimstring("v", [0.35, 3.64, 3.74, 7.84], -0.40, ["3.29", "", "4.10"])
    return p

def dg_A():
    p = dg_base("Top floor, option A")
    p.room("Suite foyer / stairs", 0.22, 0.35, 2.82, 3.64, lx=1.6, ly=3.1)
    p.room("Dressing", 3.06, 0.35, 6.75, 3.20, lx=4.95, ly=1.75)
    p.room("Bedroom", 3.10, 3.32, 6.75, 7.84, lx=5.95, ly=4.1)
    p.room("Bath", 0.22, 3.76, 2.98, 7.84, lx=1.9, ly=4.75)
    p.wall(0.22, 3.64, 3.10, 3.76)
    p.wall(2.98, 3.76, 3.10, 7.84, new=True)
    p.wall(3.06, 3.20, 6.75, 3.32, new=True)
    p.removed(3.35, 3.76, 3.45, 7.84); p.removed(3.10, 3.64, 6.75, 3.74)
    p.door(2.82, 2.03, 3.06, 2.93, "N", "E")
    p.door(1.84, 3.64, 2.74, 3.76, "W", "S", kind="pocket", new=True)
    p.door(5.70, 3.20, 6.60, 3.32, "W", "S", kind="pocket", new=True)
    # dressing
    p.wardrobe("Dressing", 3.06, 0.35, 6.75, 0.95); p.wardrobe("Dressing", 3.06, 0.95, 3.66, 1.95); p.wardrobe("Dressing", 4.00, 2.60, 5.60, 3.20)
    p.furn("Dressing", 6.25, 1.30, 6.75, 2.60, "Dressing table"); p.chair("Dressing", 5.95, 1.95)
    # bedroom
    p.bed("Bedroom", 3.10, 4.80, 5.10, 6.80, head="W", label="Bed 2.0 × 2.0")
    p.nightstand("Bedroom", 3.10, 4.20, 3.60, 4.70); p.nightstand("Bedroom", 3.10, 6.90, 3.60, 7.40)
    p.furn("Bedroom", 5.21, 5.00, 5.66, 6.60, "Bench", kind="bench")
    p.furn("Bedroom", 5.30, 7.24, 6.50, 7.84, "Desk"); p.chair("Bedroom", 5.95, 7.0, r=0.2)
    # bath
    p.wc("Bath", 0.61, 3.76, "S")
    p.screen(1.02, 3.76, 1.14, 4.76)
    p.shower("Bath", 0.22, 5.36, 1.22, 6.76, glass=(("E", 5.36, 6.16),), entry="E")
    p.vanity("Bath", 2.43, 4.90, 2.98, 6.70, basins=2, wall="E")
    p.tub("Bath", 0.90, 7.04, 2.70, 7.84)
    p.furn("Bath", 0.22, 6.84, 0.52, 7.84, "Shelves")
    p.radiator("Bath", 2.90, 3.90, 2.98, 4.80)
    p.callout(1, 3.04, 6.0); p.callout(2, 3.5, 3.26); p.callout(3, 2.29, 4.2); p.callout(4, 1.5, 4.5)
    p.dimstring("h", [0.22, 2.98, 3.10, 6.75], 8.20+0.40, ["2.76", "", "3.65"])
    p.dimstring("v", [0.35, 3.64, 3.76, 7.84], -0.40, ["3.29", "", "4.08"])
    p.dimstring("v", [0.35, 3.20, 3.32, 7.84], 7.13+0.40, ["2.85", "", "4.52"])
    return p

def dg_B():
    p = dg_base("Top floor, option B", s_window2=False)
    p.infill("S", 4.10, 6.14, note="south window infilled: facade change, needs a permit")
    p.room("Suite foyer / stairs", 0.22, 0.35, 2.82, 3.64, lx=1.6, ly=3.1)
    p.room("Bath", 3.06, 0.35, 6.75, 3.64, lx=5.0, ly=2.55)
    p.room("Bedroom", 0.22, 3.76, 4.40, 7.84, lx=1.3, ly=4.0)
    p.room("Dressing", 4.52, 3.76, 6.75, 7.84, lx=5.68, ly=5.0)
    p.wall(0.22, 3.64, 6.75, 3.76)
    p.wall(4.40, 3.76, 4.52, 7.84, new=True)
    p.removed(3.35, 3.76, 3.45, 7.84)
    p.door(2.82, 2.03, 3.06, 2.93, "N", "E")                       # foyer -> bath (existing)
    p.door(1.84, 3.64, 2.74, 3.76, "E", "S")                       # foyer -> bedroom (existing opening)
    p.door(3.45, 3.64, 4.35, 3.76, "E", "N", new=True)             # bedroom -> bath, swing into the bath
    p.door(4.40, 3.90, 4.52, 4.80, "S", "E", kind="pocket", new=True)  # bedroom -> dressing, slides south
    # bath 3.69 x 3.29
    p.wc("Bath", 3.46, 0.35, "S"); p.screen(3.06, 1.75, 3.70, 1.87)
    p.vanity("Bath", 4.35, 0.35, 5.75, 0.90, basins=2, wall="N")
    p.tub("Bath", 5.95, 0.60, 6.75, 2.40)
    p.shower("Bath", 5.55, 2.44, 6.75, 3.64, glass=("N","W"), entry="W")
    p.radiator("Bath", 3.06, 2.98, 3.14, 3.58)
    # bedroom
    p.bed("Bedroom", 0.22, 4.90, 2.22, 6.90, head="W", label="Bed 2.0 × 2.0")
    p.nightstand("Bedroom", 0.22, 4.30, 0.72, 4.80); p.nightstand("Bedroom", 0.22, 7.00, 0.72, 7.50)
    p.furn("Bedroom", 2.33, 5.10, 2.78, 6.70, "Bench", kind="bench")
    p.furn("Bedroom", 3.90, 5.00, 4.40, 6.80, "Dresser / TV")
    p.chair("Bedroom", 3.40, 7.35, r=0.32)
    # dressing
    p.wardrobe("Dressing", 4.52, 4.90, 5.12, 7.24); p.wardrobe("Dressing", 4.52, 7.24, 6.75, 7.84); p.wardrobe("Dressing", 5.50, 3.76, 6.75, 4.36)
    p.furn("Dressing", 6.25, 5.20, 6.75, 6.60, "Dressing table"); p.chair("Dressing", 5.95, 5.90)
    p.callout(1, 1.3, 3.45); p.callout(2, 4.46, 6.0); p.callout(3, 3.9, 4.15); p.callout(4, 4.0, 2.2)
    p.dimstring("h", [0.22, 4.40, 4.52, 6.75], 8.20+0.40, ["4.18", "", "2.23"])
    p.dimstring("v", [0.35, 3.64, 3.76, 7.84], -0.40, ["3.29", "", "4.08"])
    return p

def dg_C():
    p = dg_base("Top floor, option C")
    p.room("Suite foyer / stairs", 0.22, 0.35, 2.82, 3.64, lx=1.6, ly=3.1)
    p.room("Dressing", 3.06, 0.35, 6.75, 3.64, lx=4.95, ly=1.9)
    p.room("Bedroom", 0.22, 3.76, 3.80, 7.84, lx=1.3, ly=4.0)
    p.room("Bath", 3.92, 3.76, 6.75, 7.84, lx=5.1, ly=5.3)
    p.wall(0.22, 3.64, 6.75, 3.76)
    p.wall(3.80, 3.76, 3.92, 7.84, new=True)
    p.removed(3.35, 3.76, 3.45, 7.84)
    p.door(2.82, 2.03, 3.06, 2.93, "N", "E")
    p.door(1.84, 3.64, 2.74, 3.76, "E", "S")
    p.door(3.80, 4.00, 3.92, 4.90, "N", "E", new=True)            # bedroom -> bath, swing into the bath
    p.door(4.40, 3.64, 5.30, 3.76, "E", "N", new=True)            # dressing -> bath, swing into the dressing
    # dressing
    p.wardrobe("Dressing", 3.06, 0.35, 6.75, 0.95); p.wardrobe("Dressing", 3.06, 0.95, 3.66, 1.95)
    p.wardrobe("Dressing", 3.06, 3.04, 4.30, 3.64); p.wardrobe("Dressing", 5.40, 3.10, 6.75, 3.64)
    p.furn("Dressing", 6.25, 1.30, 6.75, 2.60, "Dressing table"); p.chair("Dressing", 5.95, 1.95)
    # bedroom
    p.bed("Bedroom", 0.22, 4.90, 2.22, 6.90, head="W", label="Bed 2.0 × 2.0")
    p.nightstand("Bedroom", 0.22, 4.30, 0.72, 4.80); p.nightstand("Bedroom", 0.22, 7.00, 0.72, 7.50)
    p.furn("Bedroom", 2.33, 5.10, 2.78, 6.70, "Bench", kind="bench")
    p.furn("Bedroom", 3.30, 6.70, 3.80, 7.80, "Dresser")
    # bath 2.83 x 4.08
    p.shower("Bath", 5.40, 3.76, 6.75, 4.86, glass=("S", ("W", 3.76, 4.26)), entry="W")
    p.tub("Bath", 5.95, 5.00, 6.75, 6.80)
    p.vanity("Bath", 3.92, 4.95, 4.47, 6.75, basins=2, wall="W")
    p.wc("Bath", 7.14, 3.92, "E")
    p.radiator("Bath", 6.67, 7.0, 6.75, 7.7)
    p.callout(1, 1.3, 3.45); p.callout(2, 3.5, 5.4); p.callout(3, 5.0, 2.35)
    p.dimstring("h", [0.22, 3.80, 3.92, 6.75], 8.20+0.40, ["3.58", "", "2.83"])
    p.dimstring("v", [0.35, 3.64, 3.76, 7.84], -0.40, ["3.29", "", "4.08"])
    return p

# ======================================================================= OG
def og_base(title):
    p = Plan(8.29, 11.04, title)
    p.window("N", 1.08, 3.02); p.window("N", 5.15, 7.13); p.window("S", 1.08, 3.02); p.window("S", 5.15, 7.13)
    p.stairs(0.22, 1.37, 1.25, 3.92, n=14, up="S")
    p.void(1.25, 0.80, 1.70, 1.37, "landing"); p.void(1.25, 3.92, 1.70, 4.85, "landing")
    p.chimney(2.82, 1.37, 3.05, 3.92)
    p.north(8.29+0.45, -0.35); p.scalebar(0.0)
    p.dimstring("h", [0, 8.29], -0.85, ["8.29 outside"])
    p.dimstring("h", [0.22, 4.18, 4.30, 7.93], -0.40, ["3.96", "", "3.63"])
    return p

def og_current():
    p = og_base("Upper floor as drawn today")
    p.window("E", 1.70, 3.63); p.window("E", 7.13, 9.11)
    p.room("Hall + living", 0.22, 0.38, 4.18, 10.68, lx=2.5, ly=8.9, area=34.3, sub="open landing")
    p.room("Bath", 0.22, 5.13, 2.81, 6.94, lx=1.8, ly=6.5, sub="")
    p.room("Bedroom N", 4.30, 0.38, 7.93, 5.29, lx=6.1, ly=3.4)
    p.room("Bedroom S", 4.30, 5.43, 7.93, 10.68, lx=6.1, ly=9.9)
    p.wall(4.18, 0.38, 4.30, 10.68); p.wall(4.30, 5.29, 7.93, 5.43)
    p.wall(0.22, 5.01, 2.93, 5.13); p.wall(0.22, 6.94, 2.93, 7.06); p.wall(2.81, 5.01, 2.93, 7.06)
    p.door(1.27, 5.01, 2.12, 5.13, "E", "S"); p.door(4.18, 3.90, 4.30, 4.77, "N", "E"); p.door(4.18, 6.09, 4.30, 6.94, "N", "E")
    p.vanity("Bath", 0.41, 5.38, 0.90, 5.81, basins=1, wall="W", label="Basin")
    p.shower("Bath", 0.41, 6.09, 1.50, 6.94, glass=("N","E"), entry="E")
    p.wc("Bath", 5.58, 2.81, "W"); p.wc("Bath", 6.47, 2.81, "W"); p._t("lab", 2.3, 6.9, "2nd fixture as drawn (bidet?)", "tiny")
    p.radiator("Bath", 0.22, 5.2, 0.32, 5.9)
    p.bed("Bedroom N", 4.30, 1.84, 6.19, 2.88, head="W", label="Bed 1.0 × 1.9"); p.nightstand("Bedroom N", 4.30, 1.37, 4.72, 1.84)
    p.wardrobe("Bedroom N", 4.30, 4.72, 7.93, 5.29)
    p.bed("Bedroom S", 4.30, 7.70, 6.19, 8.74, head="W", label="Bed 1.0 × 1.9"); p.nightstand("Bedroom S", 4.30, 8.74, 4.72, 9.16)
    p.wardrobe("Bedroom S", 4.30, 5.43, 7.93, 6.00)
    p.sofa("Hall + living", 0.22, 7.84, 1.23, 9.82, back="W"); p.furn("Hall + living", 3.83, 7.84, 4.18, 9.82, "TV")
    p.dimstring("v", [0.38, 5.29, 5.43, 10.68], 8.29+0.40, ["4.91", "", "5.25"])
    p.dimstring("v", [0.38, 5.01, 5.13, 6.94, 7.06, 10.68], -0.40, ["4.63", "", "1.81", "", "3.62"])
    return p

def og_O1():
    p = og_base("Upper floor, option O1")
    p.window("E", 1.70, 3.63); p.window("E", 7.13, 9.11)
    p.room("Landing + living", 0.22, 0.38, 4.18, 7.50, lx=2.6, ly=4.45, area=28.2, sub="incl. stair")
    p.room("Family bath", 0.22, 7.62, 4.18, 10.68, lx=2.75, ly=8.95)
    p.room("Bedroom N", 4.30, 0.38, 7.93, 5.29, lx=6.1, ly=3.45)
    p.room("Bedroom S", 4.30, 5.43, 7.93, 10.68, lx=6.1, ly=7.0)
    p.wall(4.18, 0.38, 4.30, 10.68); p.wall(4.30, 5.29, 7.93, 5.43)
    p.wall(0.22, 7.50, 4.18, 7.62, new=True)
    p.wall(1.12, 7.62, 1.24, 9.34, new=True); p.wall(0.22, 9.22, 1.24, 9.34, new=True)
    p.removed(0.22, 5.01, 2.93, 5.13); p.removed(0.22, 6.94, 2.93, 7.06); p.removed(2.81, 5.13, 2.93, 6.94)
    p.door(4.18, 3.90, 4.30, 4.77, "N", "E"); p.door(4.18, 6.09, 4.30, 6.94, "N", "E")
    p.door(2.30, 7.50, 3.20, 7.62, "E", "S", new=True)              # landing -> bath
    p.door(1.12, 7.95, 1.24, 8.75, "S", "E", new=True)              # WC room door, opens out into the bath
    # landing
    p.furn("Landing + living", 1.75, 0.42, 2.95, 1.02, "Desk nook"); p.chair("Landing + living", 2.35, 1.3)
    p.sofa("Landing + living", 0.22, 5.00, 1.22, 7.00, back="W"); p.furn("Landing + living", 3.78, 5.10, 4.18, 6.00, "TV")
    # family bath 3.96 x 3.06
    p.wc("Family bath", 0.67, 7.62, "S"); p._t("lab", 0.67, 8.75, "WC room", "tiny"); p._t("lab", 0.67, 8.9, "0.9 × 1.6", "tiny")
    p.appliance("Family bath", 3.30, 7.62, 4.00, 8.32, "W+D")
    p.vanity("Family bath", 3.63, 8.45, 4.18, 9.85, basins=2, wall="E")
    p.shower("Family bath", 0.22, 9.34, 1.42, 10.68, glass=(("E", 9.34, 9.94),), entry="E")
    p.tub("Family bath", 2.38, 9.88, 4.18, 10.68)
    p.radiator("Family bath", 1.24, 8.80, 1.32, 9.20)
    # bedroom N: wardrobe wall on the partition, bed on the west wall, desk at the north window
    p.wardrobe("Bedroom N", 5.25, 4.64, 7.93, 5.29)
    p.bed("Bedroom N", 4.30, 1.10, 6.30, 2.70, head="W", label="Bed 1.6 × 2.0")
    p.nightstand("Bedroom N", 4.30, 0.62, 4.72, 1.04); p.nightstand("Bedroom N", 4.30, 2.76, 4.72, 3.18)
    p.furn("Bedroom N", 6.45, 0.38, 7.85, 0.98, "Desk"); p.chair("Bedroom N", 7.55, 1.22, r=0.2)
    # bedroom S mirrored
    p.wardrobe("Bedroom S", 5.25, 5.43, 7.93, 6.08)
    p.bed("Bedroom S", 4.30, 8.35, 6.30, 9.95, head="W", label="Bed 1.6 × 2.0")
    p.nightstand("Bedroom S", 4.30, 7.87, 4.72, 8.29); p.nightstand("Bedroom S", 4.30, 10.01, 4.72, 10.43)
    p.furn("Bedroom S", 6.45, 10.08, 7.85, 10.68, "Desk"); p.chair("Bedroom S", 7.55, 9.84, r=0.2)
    p.callout(1, 2.75, 7.25); p.callout(2, 0.45, 9.08); p.callout(3, 1.85, 9.6); p.callout(4, 6.6, 4.4); p.callout(5, 3.98, 5.55)
    p.dimstring("v", [0.38, 7.50, 7.62, 10.68], -0.40, ["7.12", "", "3.06"])
    p.dimstring("v", [0.38, 5.29, 5.43, 10.68], 8.29+0.40, ["4.91", "", "5.25"])
    p.dimstring("h", [0.22, 1.12, 1.24, 4.18], 11.04+0.40, ["0.90", "", "2.94"])
    return p

def og_O2():
    p = og_base("Upper floor, option O2")
    p.window("E", 1.20, 3.10, note="moved 0.5 N", new=True); p.window("E", 7.60, 9.50, note="moved 0.5 S", new=True)
    p.room("Landing + living", 0.22, 0.38, 4.18, 7.50, lx=2.6, ly=4.45, area=28.2, sub="incl. stair")
    p.room("Study / guest", 0.22, 7.62, 4.18, 10.68, lx=2.4, ly=9.0)
    p.room("Bedroom N", 4.30, 0.38, 7.93, 5.29, lx=7.1, ly=2.3, sub="en suite 3.4 · closet 1.2")
    p.room("Bedroom S", 4.30, 5.43, 7.93, 10.68, lx=7.1, ly=8.6, sub="en suite 3.4 · closet 1.2")
    p.wall(4.18, 0.38, 4.30, 10.68); p.wall(4.30, 5.29, 7.93, 5.43)
    p.wall(0.22, 7.50, 4.18, 7.62, new=True)
    p.removed(0.22, 5.01, 2.93, 5.13); p.removed(0.22, 6.94, 2.93, 7.06); p.removed(2.81, 5.13, 2.93, 6.94)
    p.door(4.18, 3.90, 4.30, 4.77, "S", "E"); p.door(4.18, 6.09, 4.30, 6.94, "N", "E")
    p.door(1.20, 7.50, 2.10, 7.62, "E", "S", new=True)
    p.furn("Landing + living", 1.75, 0.42, 2.95, 1.02, "Desk nook"); p.chair("Landing + living", 2.35, 1.3)
    p.sofa("Landing + living", 0.22, 5.00, 1.22, 7.00, back="W"); p.furn("Landing + living", 3.78, 5.10, 4.18, 6.00, "TV")
    p.wall(3.05, 1.37, 3.17, 2.57, new=True); p.wall(3.17, 2.45, 4.18, 2.57, new=True)
    p.door(3.25, 2.45, 4.10, 2.57, "W", "S", kind="open", new=True); p._t("lab", 3.68, 2.85, "bifold doors", "tiny")
    p.appliance("Landing + living", 3.22, 1.40, 3.82, 2.00, "W+D"); p._t("lab", 3.72, 2.25, "laundry closet", "tiny")
    p.furn("Study / guest", 1.10, 10.08, 2.50, 10.68, "Desk"); p.chair("Study / guest", 1.8, 9.78)
    p.sofa("Study / guest", 0.22, 7.90, 1.18, 9.90, back="W", label="Day bed")
    # bedroom N: hotel bay — vestibule, reach-in closet, en suite in a 1.95 m strip; bed on the west wall
    p.wall(5.95, 3.34, 6.07, 5.29, new=True); p.wall(5.30, 3.34, 7.93, 3.46, new=True)
    p.door(6.20, 3.34, 7.00, 3.46, "E", "S", kind="pocket", new=True)
    p.wardrobe("Bedroom N", 5.30, 3.46, 5.95, 5.29, label="Closet 1.8 m, sliding")
    p.vanity("Bedroom N", 7.10, 3.46, 7.90, 3.96, basins=1, wall="N", label="Basin 0.8")
    p.wc("Bedroom N", 7.50, 5.29, "N")
    p.shower("Bedroom N", 6.07, 4.29, 7.07, 5.29, glass=("N","E"), entry="N")
    p.bed("Bedroom N", 4.30, 1.00, 6.30, 2.60, head="W", label="Bed 1.6 × 2.0")
    p.nightstand("Bedroom N", 4.30, 0.52, 4.72, 0.94); p.nightstand("Bedroom N", 4.30, 2.66, 4.72, 3.08)
    p.furn("Bedroom N", 6.45, 0.38, 7.85, 0.98, "Desk"); p.chair("Bedroom N", 7.55, 1.22, r=0.2)
    # bedroom S mirrored
    p.wall(5.95, 5.43, 6.07, 7.38, new=True); p.wall(5.30, 7.26, 7.93, 7.38, new=True)
    p.door(6.20, 7.26, 7.00, 7.38, "E", "N", kind="pocket", new=True)
    p.wardrobe("Bedroom S", 5.30, 5.43, 5.95, 7.26, label="Closet 1.8 m, sliding")
    p.vanity("Bedroom S", 7.10, 6.76, 7.90, 7.26, basins=1, wall="S", label="Basin 0.8")
    p.wc("Bedroom S", 7.50, 5.43, "S")
    p.shower("Bedroom S", 6.07, 5.43, 7.07, 6.43, glass=("S","E"), entry="S")
    p.bed("Bedroom S", 4.30, 8.40, 6.30, 10.00, head="W", label="Bed 1.6 × 2.0")
    p.nightstand("Bedroom S", 4.30, 7.93, 4.72, 8.35); p.nightstand("Bedroom S", 4.30, 10.05, 4.72, 10.47)
    p.furn("Bedroom S", 6.45, 10.08, 7.85, 10.68, "Desk"); p.chair("Bedroom S", 7.55, 9.84, r=0.2)
    p.callout(1, 4.8, 4.35); p.callout(2, 7.4, 3.0); p.callout(3, 3.6, 8.4); p.callout(4, 3.55, 1.0)
    p.dimstring("h", [4.30, 5.30, 5.95, 6.07, 7.93], 11.04+0.40, ["1.00", "0.65", "", "1.86"])
    p.dimstring("v", [0.38, 3.34, 3.46, 5.29, 5.43, 7.26, 7.38, 10.68], -0.40, ["2.96", "", "1.83", "", "1.83", "", "3.30"])
    return p

# ======================================================================= EG
def eg_base(title):
    p = Plan(8.29, 11.04, title)
    p.window("N", 4.78, 6.75); p.window("E", 7.08, 9.06); p.window("S", 1.08, 3.02); p.window("S", 4.98, 6.98)
    p.door(1.84, 0.0, 2.78, 0.36, "W", "S"); p._t("dim", 2.31, -0.14, "entrance", "note")
    p.stairs(0.22, 1.55, 1.25, 3.82, n=13, up="S")
    p.chimney(2.78, 1.98, 3.63, 3.63)
    p.north(8.29+0.45, -0.35); p.scalebar(0.0)
    p.dimstring("h", [0, 8.29], -0.85, ["8.29 outside"])
    p.dimstring("h", [3.63, 7.93], -0.40, ["4.30 kitchen wall"])
    return p

def eg_current():
    p = eg_base("Ground floor as drawn today")
    p.room("Hall + living + kitchen", 0.22, 0.38, 7.93, 10.68, lx=5.8, ly=6.2, area=60.0, sub="open plan")
    p.room("Guest WC", 0.22, 5.11, 1.58, 7.36, lx=0.9, ly=6.75)
    p.room("Bedroom", 0.22, 7.55, 3.02, 10.68, lx=1.6, ly=7.95, area=13.0, sub="incl. corridor")
    p.wall(0.22, 4.98, 3.12, 5.11); p.wall(1.58, 5.11, 1.70, 7.36); p.wall(0.22, 7.36, 1.70, 7.55); p.wall(3.02, 5.11, 3.12, 10.68); p.wall(1.70, 7.36, 3.02, 7.55)
    p.door(1.84, 4.98, 2.74, 5.11, "E", "S"); p.door(1.58, 5.71, 1.70, 6.56, "N", "E"); p.door(1.84, 7.36, 2.74, 7.55, "E", "S")
    p.vanity("Guest WC", 0.22, 5.70, 0.52, 6.20, basins=1, wall="W", label="Basin"); p.wc("Guest WC", 1.08, 5.11, "S")
    p.radiator("Guest WC", 0.22, 5.11, 1.58, 5.21)
    p.bed("Bedroom", 0.22, 8.20, 2.22, 10.10, head="W", label="Bed 1.9 × 2.0")
    p.nightstand("Bedroom", 0.22, 7.70, 0.64, 8.17); p.nightstand("Bedroom", 0.22, 10.13, 0.64, 10.52)
    p.kitchen("Hall + living + kitchen", 3.63, 0.42, 7.93, 1.00); p.furn("Hall + living + kitchen", 4.58, 2.17, 6.98, 3.40, "Island 2.4 × 1.2")
    p.furn("Hall + living + kitchen", 4.67, 4.48, 6.75, 5.61, "Table 2.1 × 1.1")
    p.sofa("Hall + living + kitchen", 4.62, 6.56, 6.65, 7.60, back="N"); p.sofa("Hall + living + kitchen", 6.75, 8.26, 7.79, 10.24, back="E")
    p.dimstring("v", [0.38, 4.98, 5.11, 7.36, 7.55, 10.68], -0.40, ["4.60", "", "2.25", "", "3.13"])
    p.dimstring("h", [0.22, 1.58, 1.70, 3.02, 3.12, 7.93], 11.04+0.40, ["1.36", "", "1.32", "", "4.81"])
    return p

def eg_E1():
    p = eg_base("Ground floor, option E1")
    p.room("Entrance hall", 0.22, 0.38, 2.78, 4.98, lx=1.75, ly=4.35, area=11.6)
    p.room("Living · dining · kitchen", 2.78, 0.38, 7.93, 10.68, lx=5.9, ly=6.85, area=46.7, sub="open plan")
    p.room("Guest bath", 0.22, 5.10, 2.22, 7.36, lx=0.75, ly=6.1)
    p.room("Corridor", 2.34, 5.10, 3.51, 7.36, lx=2.93, ly=6.9)
    p.room("Bedroom", 0.22, 7.55, 3.51, 10.68, lx=1.6, ly=7.78)
    p.wall(0.22, 4.98, 3.63, 5.10); p.wall(0.22, 7.36, 3.51, 7.55)
    p.wall(2.22, 5.10, 2.34, 7.36, new=True); p.wall(3.51, 5.10, 3.63, 10.68, new=True)
    p.removed(1.58, 5.11, 1.70, 7.36); p.removed(3.02, 5.11, 3.12, 10.68)
    p.door(2.46, 4.98, 3.39, 5.10, "W", "S", kind="open")
    p.door(2.22, 5.30, 2.34, 6.20, "N", "E", new=True)               # bath door opens out into the corridor
    p.door(2.46, 7.36, 3.36, 7.55, "E", "S", new=True)               # corridor -> bedroom
    # hall
    p.wardrobe("Entrance hall", 2.23, 2.00, 2.78, 3.50); p.furn("Entrance hall", 0.22, 0.45, 0.62, 1.45, "Bench")
    # guest bath 2.00 x 2.26
    p.vanity("Guest bath", 0.30, 5.10, 1.20, 5.60, basins=1, wall="N", label="Basin 0.9")
    p.wc("Guest bath", 0.60, 7.36, "N")
    p.shower("Guest bath", 1.22, 6.36, 2.22, 7.36, glass=("W", ("N", 1.22, 1.62)), entry="N")
    p.radiator("Guest bath", 0.22, 5.80, 0.30, 6.30)
    # bedroom
    p.bed("Bedroom", 0.22, 8.16, 2.22, 10.06, head="W", label="Bed 1.9 × 2.0")
    p.nightstand("Bedroom", 0.22, 7.65, 0.64, 8.10); p.nightstand("Bedroom", 0.22, 10.12, 0.64, 10.57)
    p.wardrobe("Bedroom", 3.03, 8.50, 3.51, 10.50, label="Slim wardrobe 0.48")
    # kitchen / dining / living
    p.kitchen("Living · dining · kitchen", 3.63, 0.38, 7.93, 0.98, sink=4.95, hob=7.25); p._t("lab", 4.2, 1.2, "tall units", "tiny")
    p.furn("Living · dining · kitchen", 4.60, 2.18, 7.00, 3.38, "Island 2.4 × 1.2")
    p.table("Living · dining · kitchen", 4.90, 4.90, 6.90, 5.90, chairs=(3,3,0,0), label="Table")
    p.sofa("Living · dining · kitchen", 4.30, 7.20, 6.30, 8.20, back="N")
    p.sofa("Living · dining · kitchen", 6.93, 8.50, 7.93, 10.50, back="E")
    p.furn("Living · dining · kitchen", 5.20, 8.60, 6.20, 9.40, "Coffee table")
    p.furn("Living · dining · kitchen", 3.63, 8.60, 4.03, 10.40, "TV")
    p.callout(1, 2.5, 1.75); p.callout(2, 1.0, 7.1); p.callout(3, 2.93, 6.45); p.callout(4, 2.6, 10.5); p.callout(5, 4.75, 2.3)
    p.dimstring("h", [0.22, 2.22, 2.34, 3.51, 3.63, 7.93], 11.04+0.40, ["2.00", "", "1.17", "", "4.30"])
    p.dimstring("v", [0.38, 4.98, 5.10, 7.36, 7.55, 10.68], -0.40, ["4.60", "", "2.26", "", "3.13"])
    return p

ALL = dict(dg_current=dg_current, dg_A=dg_A, dg_B=dg_B, dg_C=dg_C, og_current=og_current, og_O1=og_O1, og_O2=og_O2, eg_current=eg_current, eg_E1=eg_E1)

if __name__ == "__main__":
    for k, f in ALL.items():
        p = f(); issues = p.check()
        print(f"== {k}: {len(issues)} issues; rooms {[(n, round(v[4],1)) for n,v in p.rooms.items()]}")
        for i in issues: print("   -", i)
        for c in p.clearances:
            flag = "" if c[3] >= c[5]-0.005 else ("  (min ok)" if c[3] >= c[4]-0.005 else "  ✗")
            print(f"     · {c[0]:<22} {c[1]:<28} {c[2]:<8} {c[3]:.2f} m  [min {c[4]:.2f} / comfort {c[5]:.2f}]{flag}")
