from engine import Plan

# ======================================================================= DG
DG_OUT = dict(x0=0.0, y0=-1.23, x1=8.29, y1=9.73)   # lower-floor outline in DG coords

def dg_base(title, outside=True):
    p = Plan(7.13, 8.20, title, outside=DG_OUT if outside else None)
    p.shell()
    if outside: p.set_back("dashed: floor below · hatched: set-back strips 1.2–1.5 m (roof terrace if the slab is walkable)")
    p.window("N", 0.66, 2.50); p.window("E", 1.04, 3.05); p.window("E", 4.96, 6.90); p.window("S", 0.80, 2.83)
    p.stairs(0.22, 0.35, 1.25, 2.60, n=13, up="S")
    p.void(1.25, 0.50, 2.10, 2.50)
    p.chimney(2.82, 0.35, 3.06, 1.95)
    p.wall(2.82, 1.95, 3.06, 3.64)
    p.north(7.13+0.9, -0.5); p.scalebar(0.0)
    return p

def dg_current():
    p = dg_base("Top floor, as drawn today")
    p.window("S", 4.10, 6.14)
    p.room("Hall / stairs", 0.22, 0.35, 2.82, 3.64, lx=1.65, ly=3.15)
    p.room("Closet room", 3.06, 0.35, 6.75, 3.64, lx=4.9, ly=2.75)
    p.room("Bath", 0.22, 3.74, 3.35, 7.84, lx=2.0, ly=6.3)
    p.room("Bedroom", 3.45, 3.74, 6.75, 7.84, lx=5.9, ly=4.55)
    p.wall(0.22, 3.64, 6.75, 3.74); p.wall(3.35, 3.74, 3.45, 7.84)
    p.door(2.82, 2.03, 3.06, 2.93, "N", "E")
    p.door(1.84, 3.64, 2.74, 3.74, "E", "S")
    p.door(5.71, 3.64, 6.60, 3.74, "E", "S")
    p.wardrobe("closet", 3.06, 6.75 and 3.06+0.0, 6.75, 0.94) if False else None
    p.wardrobe("Closet", 3.06, 0.35, 6.75, 0.94)
    p.furn("Closet", 3.97, 1.62, 5.43, 2.29, "Table")
    p.wardrobe("Closet", 3.06, 3.05, 5.62, 3.64)
    p.shower("Bath", 0.38, 3.74, 1.42, 5.53, glass=("E","S"))
    p.wc("Bath", 0.50, 5.80, 1.00, 6.23, facing="E")
    p.vanity("Bath", 2.88, 3.78, 3.35, 5.76, basins=2, wall="E")
    p.tub("Bath", 0.90, 6.85, 2.69, 7.65)
    p.bed("Bedroom", 3.45, 4.77, 5.43, 6.75, head="W", label="Bed 2.0 × 2.0")
    p.dim("h", 0.22, 3.35, 8.20+0.4, "3.13"); p.dim("h", 3.45, 6.75, 8.20+0.4, "3.30")
    p.dim("v", 3.74, 7.84, -0.35, "4.10"); p.dim("v", 0.35, 3.64, 7.13+0.35, "3.29")
    p.dim("h", 0, 7.13, -0.3, "7.13 (floor below 8.29)")
    return p

def dg_A():
    p = dg_base("Top floor, option A")
    p.window("S", 4.10, 6.14)
    p.room("Suite foyer / stairs", 0.22, 0.35, 2.82, 3.64, lx=1.65, ly=3.15)
    p.room("Dressing", 3.06, 0.35, 6.75, 3.05, lx=4.9, ly=1.75)
    p.room("Bedroom", 2.94, 3.17, 6.75, 7.84, lx=5.95, ly=4.1)
    p.room("Bath", 0.22, 3.76, 2.82, 7.84, lx=1.75, ly=4.35)
    # walls: hall|bath (existing line), bath|bedroom (moved west), dressing|bedroom (moved north)
    p.wall(0.22, 3.64, 2.82, 3.76)
    p.wall(2.82, 3.17, 2.94, 7.84, new=True)
    p.wall(2.94, 3.05, 6.75, 3.17, new=True)
    p.removed_wall(3.35, 3.76, 3.45, 7.84); p.removed_wall(2.94, 3.64, 6.75, 3.74)
    # doors
    p.door(2.82, 2.03, 3.06, 2.93, "N", "E")                 # foyer -> dressing (existing opening)
    p.door(1.84, 3.64, 2.74, 3.76, "W", "S", kind="pocket", new=True)   # foyer -> bath (existing opening, now a pocket door)
    p.door(5.70, 3.05, 6.60, 3.17, "W", "S", kind="pocket", new=True)   # dressing -> bedroom (pocket)
    # dressing
    p.wardrobe("Dressing", 3.06, 0.35, 6.75, 0.95)
    p.wardrobe("Dressing", 3.06, 0.95, 3.66, 1.95)
    p.wardrobe("Dressing", 4.00, 2.45, 5.60, 3.05)
    p.furn("Dressing", 6.25, 1.30, 6.75, 2.60, "Dressing table")
    p.zone("dressing aisle 1.5 m", 3.66, 0.95, 6.25, 2.45, "aisle 1.5 m")
    # bedroom
    p.bed("Bedroom", 2.94, 4.90, 4.94, 6.90, head="W", label="Bed 2.0 × 2.0")
    p.nightstand("Bedroom", 2.94, 4.30, 3.44, 4.80); p.nightstand("Bedroom", 2.94, 7.00, 3.44, 7.50)
    p.furn("Bedroom", 5.05, 5.10, 5.50, 6.70, "Bench")
    p.furn("Bedroom", 5.10, 7.24, 6.30, 7.84, "Desk")
    p.furn("Bedroom", 5.45, 6.75, 5.90, 7.18, "")
    p.zone("bed side N 0.75", 3.44, 4.15, 4.94, 4.90, "0.75")
    p.zone("bed side S 0.75", 3.44, 6.90, 4.94, 7.65, "0.75")
    p.zone("foot aisle", 5.50, 5.10, 6.70, 6.70, "1.2 m")
    # bath
    p.wc("Bath", 0.42, 3.76, 0.82, 4.44, facing="S")
    p.wall(1.02, 3.76, 1.14, 4.80, new=True)   # 1.2 m high screen between door and WC
    p.label(1.22, 4.25, "screen h 1.2", "tiny", rot=-90)
    p.shower("Bath", 0.22, 5.10, 1.22, 6.50, glass=("E",))
    p.vanity("Bath", 2.27, 5.20, 2.82, 7.00, basins=2, wall="E")
    p.tub("Bath", 0.90, 7.04, 2.70, 7.84)
    p.wardrobe("Bath", 0.22, 6.60, 0.82, 7.84, label="Linen")
    p.radiator("Bath", 2.74, 3.90, 2.82, 5.00)
    p.zone("vanity standing 0.9", 1.37, 5.20, 2.27, 7.00, "0.9")
    p.zone("WC front 0.6", 0.22, 4.44, 1.02, 5.04, "0.6", kind="path")
    p.zone("entry landing", 1.84, 3.76, 2.74, 4.66, "")
    L = p.path([(3.6, 4.1), (3.6, 3.5), (6.15, 3.5), (6.15, 2.6), (3.3, 2.6), (2.5, 2.6), (2.5, 3.3), (2.3, 3.3), (2.3, 4.75), (1.4, 4.75), (0.62, 4.75)], "bed→WC")
    p.callout(1, 2.88, 6.0); p.callout(2, 4.3, 3.11); p.callout(3, 2.29, 3.70); p.callout(4, 1.45, 4.15)
    p.dim("h", 0.22, 2.82, 8.20+0.4, "2.60"); p.dim("h", 2.94, 6.75, 8.20+0.4, "3.81")
    p.dim("v", 3.17, 7.84, -0.35, "4.67"); p.dim("v", 0.35, 3.05, 7.13+0.35, "2.70")
    p.dim("h", 0, 7.13, -0.3, "7.13")
    p.pathlen = L
    return p

def dg_B():
    p = dg_base("Top floor, option B")
    p.room("Suite foyer / stairs", 0.22, 0.35, 2.82, 3.64, lx=1.65, ly=3.15)
    p.room("Bath", 3.06, 0.35, 6.75, 3.64, lx=4.75, ly=2.45)
    p.room("Bedroom", 0.22, 3.76, 4.40, 7.84, lx=3.2, ly=5.1)
    p.room("Dressing", 4.52, 3.76, 6.75, 7.84, lx=5.68, ly=5.95)
    p.wall(0.22, 3.64, 6.75, 3.76)
    p.wall(4.40, 3.76, 4.52, 7.84, new=True)
    p.removed_wall(3.35, 3.76, 3.45, 7.84)
    p.window("S", 4.10, 6.14, note="south window: drop or re-size (dressing)", new=True)
    p.door(2.82, 2.03, 3.06, 2.93, "N", "E")                 # foyer -> bath (existing)
    p.door(1.84, 3.64, 2.74, 3.76, "E", "S")                 # foyer -> bedroom (existing opening)
    p.door(3.30, 3.64, 4.20, 3.76, "W", "S", kind="pocket", new=True)  # bedroom -> bath
    p.door(4.40, 3.90, 4.52, 4.80, "N", "E", kind="pocket", new=True)  # bedroom -> dressing
    p.door(4.60, 3.64, 5.50, 3.76, "W", "N", kind="pocket", new=True)  # dressing -> bath
    # bath
    p.wc("Bath", 3.26, 0.35, 3.66, 1.03, facing="S")
    p.shower("Bath", 4.00, 0.35, 5.20, 1.55, glass=("S","W"))
    p.vanity("Bath", 5.25, 0.35, 6.75, 0.90, basins=2, wall="N")
    p.tub("Bath", 5.95, 1.85, 6.75, 3.64)
    p.radiator("Bath", 3.06, 1.30, 3.16, 1.90)
    p.zone("vanity standing 0.9", 5.25, 0.90, 6.75, 1.80, "0.9")
    p.zone("WC front 0.8", 3.06, 1.03, 3.86, 1.83, "0.8", kind="path")
    p.zone("bedroom door landing", 3.30, 2.74, 4.20, 3.64, "")
    p.zone("dressing door landing", 4.60, 2.74, 5.50, 3.64, "")
    # bedroom
    p.bed("Bedroom", 0.22, 4.90, 2.22, 6.90, head="W", label="Bed 2.0 × 2.0")
    p.nightstand("Bedroom", 0.22, 4.30, 0.72, 4.80); p.nightstand("Bedroom", 0.22, 7.00, 0.72, 7.50)
    p.furn("Bedroom", 2.33, 5.10, 2.78, 6.70, "Bench")
    p.furn("Bedroom", 3.90, 5.00, 4.40, 6.80, "Dresser / TV")
    p.furn("Bedroom", 3.00, 6.95, 3.80, 7.75, "Chair")
    p.zone("bed side N 0.75", 0.72, 4.15, 2.22, 4.90, "0.75")
    p.zone("bed side S 0.75", 0.72, 6.90, 2.22, 7.65, "0.75")
    p.zone("foot aisle", 2.78, 5.10, 3.90, 6.70, "1.1 m")
    # dressing
    p.wardrobe("Dressing", 4.52, 4.90, 5.12, 7.24)
    p.wardrobe("Dressing", 5.60, 3.76, 6.75, 4.36)
    p.wardrobe("Dressing", 4.52, 7.24, 6.75, 7.84)
    p.furn("Dressing", 6.25, 5.20, 6.75, 6.60, "Dressing table")
    p.zone("dressing aisle", 5.12, 4.90, 6.25, 7.24, "1.1 m")
    L = p.path([(0.9, 4.1), (3.75, 4.1), (3.75, 3.2), (3.45, 3.2), (3.45, 1.4)], "bed→WC")
    p.callout(1, 1.3, 3.70); p.callout(2, 4.46, 5.4); p.callout(3, 3.75, 3.70)
    p.dim("h", 0.22, 4.40, 8.20+0.4, "4.18"); p.dim("h", 4.52, 6.75, 8.20+0.4, "2.23")
    p.dim("v", 3.76, 7.84, -0.35, "4.08"); p.dim("v", 0.35, 3.64, 7.13+0.35, "3.29")
    p.dim("h", 0, 7.13, -0.3, "7.13")
    p.pathlen = L
    return p

def dg_C():
    p = dg_base("Top floor, option C")
    p.window("S", 4.10, 6.14)
    p.room("Suite foyer / stairs", 0.22, 0.35, 2.82, 3.64, lx=1.65, ly=3.15)
    p.room("Dressing", 3.06, 0.35, 6.75, 3.64, lx=4.9, ly=2.2)
    p.room("Bedroom", 0.22, 3.76, 3.90, 7.84, lx=1.3, ly=4.05)
    p.room("Bath", 4.02, 3.76, 6.75, 7.84, lx=4.85, ly=4.25)
    p.wall(0.22, 3.64, 6.75, 3.76)
    p.wall(3.90, 3.76, 4.02, 7.84, new=True)
    p.removed_wall(3.35, 3.76, 3.45, 7.84)
    p.door(2.82, 2.03, 3.06, 2.93, "N", "E")                 # foyer -> dressing (existing)
    p.door(1.84, 3.64, 2.74, 3.76, "E", "S")                 # foyer -> bedroom (existing opening)
    p.door(3.90, 6.84, 4.02, 7.74, "N", "E", kind="pocket", new=True)  # bedroom -> bath
    p.door(4.40, 3.64, 5.30, 3.76, "W", "S", kind="pocket", new=True)  # dressing -> bath
    # dressing
    p.wardrobe("Dressing", 3.06, 0.35, 6.75, 0.95)
    p.wardrobe("Dressing", 3.06, 0.95, 3.66, 1.95)
    p.wardrobe("Dressing", 3.06, 3.04, 4.30, 3.64)
    p.wardrobe("Dressing", 5.40, 3.04, 6.75, 3.64)
    p.furn("Dressing", 6.25, 1.30, 6.75, 2.60, "Dressing table")
    p.zone("dressing aisle", 3.66, 0.95, 6.25, 3.04, "aisle 2.1 m")
    # bedroom
    p.bed("Bedroom", 0.22, 4.90, 2.22, 6.90, head="W", label="Bed 2.0 × 2.0")
    p.nightstand("Bedroom", 0.22, 4.30, 0.72, 4.80); p.nightstand("Bedroom", 0.22, 7.00, 0.72, 7.50)
    p.furn("Bedroom", 2.33, 5.10, 2.78, 6.70, "Bench")
    p.furn("Bedroom", 3.40, 3.86, 3.90, 4.96, "Dresser")
    p.zone("bed side N 0.75", 0.72, 4.15, 2.22, 4.90, "0.75")
    p.zone("bed side S 0.75", 0.72, 6.90, 2.22, 7.65, "0.75")
    p.zone("foot aisle", 2.78, 5.10, 3.90, 6.70, "1.1 m")
    # bath
    p.shower("Bath", 5.40, 3.76, 6.75, 4.96, glass=("S","W"))
    p.tub("Bath", 5.95, 5.00, 6.75, 6.80)
    p.vanity("Bath", 4.02, 4.80, 4.57, 6.60, basins=2, wall="W")
    p.wc("Bath", 5.20, 7.16, 5.60, 7.84, facing="N")
    p.radiator("Bath", 4.02, 4.00, 4.12, 4.70)
    p.zone("vanity standing 0.8", 4.57, 4.80, 5.37, 6.60, "0.8")
    p.zone("WC front 0.8", 5.00, 6.36, 5.80, 7.16, "0.8", kind="path")
    p.zone("bedroom door landing", 4.02, 6.84, 4.92, 7.74, "")
    p.zone("dressing door landing", 4.40, 3.76, 5.30, 4.66, "")
    L = p.path([(0.9, 7.25), (3.3, 7.25), (4.4, 7.25), (4.4, 6.7), (5.4, 6.7)], "bed→WC")
    p.callout(1, 1.3, 3.70); p.callout(2, 3.96, 6.35); p.callout(3, 4.85, 3.70)
    p.dim("h", 0.22, 3.90, 8.20+0.4, "3.68"); p.dim("h", 4.02, 6.75, 8.20+0.4, "2.73")
    p.dim("v", 3.76, 7.84, -0.35, "4.08"); p.dim("v", 0.35, 3.64, 7.13+0.35, "3.29")
    p.dim("h", 0, 7.13, -0.3, "7.13")
    p.pathlen = L
    return p

# ======================================================================= OG
def og_base(title):
    p = Plan(8.29, 11.04, title)
    p.shell()
    p.window("N", 1.08, 3.02); p.window("N", 5.15, 7.13)
    p.window("S", 1.08, 3.02); p.window("S", 5.15, 7.13)
    p.stairs(0.22, 1.37, 1.25, 3.92, n=14, up="S")
    p.void(1.25, 0.80, 1.70, 1.37, ""); p.void(1.25, 3.92, 1.70, 4.85, "")
    p.chimney(2.82, 1.37, 3.05, 3.92)
    p.north(8.29+0.9, -0.5); p.scalebar(0.0, 11.04+0.75)
    return p

def og_current():
    p = og_base("Upper floor, as drawn today")
    p.window("E", 1.70, 3.63); p.window("E", 7.13, 9.11)
    p.room("Hall + living", 0.22, 0.38, 4.18, 10.68, lx=2.5, ly=8.9, area=34.3)
    p.room("Bath", 0.22, 5.13, 2.81, 6.94, lx=1.6, ly=6.2)
    p.room("Bedroom N", 4.30, 0.38, 7.93, 5.29, lx=6.1, ly=3.4)
    p.room("Bedroom S", 4.30, 5.43, 7.93, 10.68, lx=6.1, ly=9.9)
    p.wall(4.18, 0.38, 4.30, 10.68); p.wall(4.30, 5.29, 7.93, 5.43)
    p.wall(0.22, 5.01, 2.93, 5.13); p.wall(0.22, 6.94, 2.93, 7.06); p.wall(2.81, 5.01, 2.93, 7.06)
    p.door(1.27, 5.01, 2.12, 5.13, "E", "S")
    p.door(4.18, 3.90, 4.30, 4.77, "N", "E"); p.door(4.18, 6.09, 4.30, 6.94, "N", "E")
    p.vanity("Bath", 0.41, 5.38, 0.90, 5.81, basins=1, wall="W", label="Basin")
    p.shower("Bath", 0.41, 6.09, 1.50, 6.94, glass=("N","E"))
    p.wc("Bath", 2.13, 5.38, 2.81, 5.78, facing="W"); p.wc("Bath", 2.13, 6.28, 2.81, 6.68, facing="W")
    p.radiator("Bath", 0.22, 5.2, 0.32, 5.9)
    p.bed("Bedroom N", 4.30, 1.84, 6.19, 2.88, head="W", label="Bed 1.0 × 1.9"); p.nightstand("Bedroom N", 4.30, 1.37, 4.72, 1.84)
    p.wardrobe("Bedroom N", 4.30, 4.72, 7.93, 5.29)
    p.bed("Bedroom S", 4.30, 7.70, 6.19, 8.74, head="W", label="Bed 1.0 × 1.9"); p.nightstand("Bedroom S", 4.30, 8.74, 4.72, 9.16)
    p.wardrobe("Bedroom S", 4.30, 5.43, 7.93, 6.00)
    p.sofa("Living", 0.22, 7.84, 1.23, 9.82, back="W"); p.furn("Living", 3.83, 7.84, 4.18, 9.82, "TV")
    p.dim("h", 0.22, 4.18, 11.04+0.4, "3.96"); p.dim("h", 4.30, 7.93, 11.04+0.4, "3.63")
    p.dim("v", 0.38, 5.29, 8.29+0.35, "4.91"); p.dim("v", 5.43, 10.68, 8.29+0.35, "5.25")
    return p

def og_O1():
    p = og_base("Upper floor, option O1")
    p.window("E", 1.70, 3.63); p.window("E", 7.13, 9.11)
    p.room("Landing + living", 0.22, 0.38, 4.18, 7.50, lx=2.2, ly=4.45, area=28.2)
    p.room("Family bath", 0.22, 7.62, 4.18, 10.68, lx=2.2, ly=8.95)
    p.room("Bedroom N", 4.30, 0.38, 7.93, 5.29, lx=6.9, ly=1.85, sub="net 14.5 + closet 3.3")
    p.room("Bedroom S", 4.30, 5.43, 7.93, 10.68, lx=6.9, ly=8.95, sub="net 15.8 + closet 3.3")
    p.wall(4.18, 0.38, 4.30, 10.68); p.wall(4.30, 5.29, 7.93, 5.43)
    p.wall(0.22, 7.50, 4.18, 7.62, new=True)
    p.removed_wall(0.22, 5.01, 2.93, 5.13); p.removed_wall(0.22, 6.94, 2.93, 7.06); p.removed_wall(2.81, 5.13, 2.93, 6.94)
    p.door(4.18, 3.90, 4.30, 4.77, "N", "E"); p.door(4.18, 6.09, 4.30, 6.94, "N", "E")   # existing bedroom doors
    p.door(1.20, 7.50, 2.10, 7.62, "E", "S", new=True)                                   # landing -> bath
    # landing / living nook
    p.furn("Landing", 1.75, 0.42, 2.95, 1.02, "Desk nook")
    p.sofa("Landing", 0.22, 5.00, 1.22, 7.00, back="W")
    p.furn("Landing", 3.78, 5.10, 4.18, 6.00, "TV")
    p.zone("tv distance", 1.22, 5.3, 3.78, 6.7, "2.6 m to screen", kind="path")
    # family bath 3.96 x 3.06
    p.wall(2.96, 7.62, 3.08, 9.12, new=True); p.wall(3.08, 9.00, 4.18, 9.12, new=True)
    p.door(2.96, 7.95, 3.08, 8.75, "S", "W", new=True)
    p.wc("Bath", 3.50, 7.62, 3.90, 8.30, facing="S"); p.label(3.63, 8.7, "WC room 1.1×1.5", "tiny")
    p.shower("Bath", 2.98, 9.48, 4.18, 10.68, glass=("N","W"))
    p.tub("Bath", 1.10, 9.88, 2.90, 10.68)
    p.vanity("Bath", 0.22, 7.80, 0.77, 9.60, basins=2, wall="W")
    p.appliance("Bath", 0.22, 9.98, 0.92, 10.68, "W+D")
    p.radiator("Bath", 1.6, 9.30, 2.6, 9.40)
    p.zone("vanity standing 0.9", 0.77, 7.80, 1.67, 9.60, "0.9")
    p.zone("WC-room door landing", 2.06, 7.95, 2.96, 8.75, "")
    p.zone("WC front", 3.18, 8.30, 4.18, 9.00, "", kind="path")
    # bedroom N: walk-in NW, bed head on S partition
    p.wall(5.80, 0.38, 5.92, 2.70, new=True); p.wall(4.30, 2.58, 5.92, 2.70, new=True)
    p.door(4.60, 2.58, 5.40, 2.70, "W", "S", kind="pocket", new=True)
    p.wardrobe("Bedroom N", 4.30, 0.38, 4.90, 2.58); p.wardrobe("Bedroom N", 4.90, 0.38, 5.80, 0.98)
    p.label(5.35, 1.9, "walk-in 1.5×2.2", "tiny", rot=-90)
    p.bed("Bedroom N", 5.70, 3.29, 7.30, 5.29, head="S", label="Bed 1.6 × 2.0")
    p.nightstand("Bedroom N", 5.20, 4.84, 5.65, 5.29); p.nightstand("Bedroom N", 7.35, 4.84, 7.80, 5.29)
    p.furn("Bedroom N", 5.95, 0.38, 7.35, 0.98, "Desk"); p.furn("Bedroom N", 6.45, 1.05, 6.90, 1.50, "")
    p.zone("bed side W", 5.00, 3.29, 5.70, 4.84, "0.7"); p.zone("bed side E", 7.30, 3.29, 7.93, 4.84, "0.63"); p.zone("foot", 5.70, 2.70, 7.30, 3.29, "0.6", kind="path")
    # bedroom S: walk-in SW, bed head on N partition
    p.wall(5.80, 8.36, 5.92, 10.68, new=True); p.wall(4.30, 8.36, 5.92, 8.48, new=True)
    p.door(4.60, 8.36, 5.40, 8.48, "W", "N", kind="pocket", new=True)
    p.wardrobe("Bedroom S", 4.30, 8.48, 4.90, 10.68); p.wardrobe("Bedroom S", 4.90, 10.08, 5.80, 10.68)
    p.label(5.35, 9.3, "walk-in 1.5×2.2", "tiny", rot=-90)
    p.bed("Bedroom S", 5.70, 5.43, 7.30, 7.43, head="N", label="Bed 1.6 × 2.0")
    p.nightstand("Bedroom S", 5.20, 5.43, 5.65, 5.88); p.nightstand("Bedroom S", 7.35, 5.43, 7.80, 5.88)
    p.furn("Bedroom S", 5.95, 10.08, 7.35, 10.68, "Desk"); p.furn("Bedroom S", 6.45, 9.55, 6.90, 10.00, "")
    p.zone("bed side W", 5.00, 5.88, 5.70, 7.43, "0.7"); p.zone("bed side E", 7.30, 5.88, 7.93, 7.43, "0.63"); p.zone("foot", 5.70, 7.43, 7.30, 8.36, "0.9", kind="path")
    p.callout(1, 1.1, 7.56); p.callout(2, 3.6, 9.3); p.callout(3, 0.57, 9.8); p.callout(4, 5.86, 1.5); p.callout(5, 3.98, 5.55)
    p.dim("h", 0.22, 4.18, 11.04+0.4, "3.96"); p.dim("h", 4.30, 7.93, 11.04+0.4, "3.63")
    p.dim("v", 7.62, 10.68, -0.35, "3.06"); p.dim("v", 0.38, 7.50, -0.35, "7.12")
    return p

def og_O2():
    p = og_base("Upper floor, option O2")
    p.window("E", 0.90, 2.80, note="moved 0.8 N", new=True); p.window("E", 7.90, 9.90, note="moved 0.8 S", new=True)
    p.room("Landing + living", 0.22, 0.38, 4.18, 7.50, lx=2.2, ly=4.45, area=28.2)
    p.room("Study / guest", 0.22, 7.62, 4.18, 10.68, lx=2.2, ly=9.0)
    p.room("Bedroom N", 4.30, 0.38, 7.93, 5.29, lx=5.0, ly=1.8, sub="en suite 4.3")
    p.room("Bedroom S", 4.30, 5.43, 7.93, 10.68, lx=6.4, ly=9.95, sub="en suite 4.3")
    p.wall(4.18, 0.38, 4.30, 10.68); p.wall(4.30, 5.29, 7.93, 5.43)
    p.wall(0.22, 7.50, 4.18, 7.62, new=True)
    p.removed_wall(0.22, 5.01, 2.93, 5.13); p.removed_wall(0.22, 6.94, 2.93, 7.06); p.removed_wall(2.81, 5.13, 2.93, 6.94)
    p.door(4.18, 3.90, 4.30, 4.77, "N", "E"); p.door(4.18, 6.09, 4.30, 6.94, "N", "E")
    p.door(1.20, 7.50, 2.10, 7.62, "E", "S", new=True)
    p.furn("Landing", 1.75, 0.42, 2.95, 1.02, "Desk nook")
    p.sofa("Landing", 0.22, 5.00, 1.22, 7.00, back="W"); p.furn("Landing", 3.78, 5.10, 4.18, 6.00, "TV")
    p.wall(3.10, 1.37, 3.22, 2.57, new=True); p.wall(3.22, 2.45, 4.18, 2.57, new=True)
    p.appliance("Landing", 3.25, 1.40, 3.85, 2.00, "W+D"); p.label(3.7, 2.3, "laundry closet", "tiny")
    p.furn("Study", 1.10, 10.08, 2.50, 10.68, "Desk"); p.sofa("Study", 0.22, 7.90, 1.22, 9.90, back="W", label="Day bed")
    # bedroom N: hotel bay — vestibule, reach-in closet, en suite along the south edge
    p.wall(5.95, 3.00, 6.07, 5.29, new=True); p.wall(5.30, 3.00, 7.93, 3.12, new=True)
    p.door(6.20, 3.00, 7.00, 3.12, "W", "S", kind="pocket", new=True)
    p.wardrobe("Bedroom N", 5.30, 3.12, 5.95, 5.29, label="Closet 2.2 m")
    p.shower("Bedroom N", 6.07, 4.09, 7.00, 5.29, glass=("N","E"))
    p.wc("Bedroom N", 7.20, 4.61, 7.60, 5.29, facing="N")
    p.vanity("Bedroom N", 7.33, 3.12, 7.93, 3.82, basins=1, wall="E", label="Basin")
    p.bed("Bedroom N", 5.80, 1.00, 7.40, 3.00, head="S", label="Bed 1.6 × 2.0")
    p.nightstand("Bedroom N", 5.33, 2.55, 5.78, 3.00); p.nightstand("Bedroom N", 7.45, 2.55, 7.90, 3.00)
    p.furn("Bedroom N", 4.30, 0.38, 5.50, 0.98, "Desk")
    p.zone("vestibule", 4.30, 3.12, 5.30, 5.29, "vestibule 1.0", kind="path")
    # bedroom S mirrored
    p.wall(5.95, 5.43, 6.07, 7.72, new=True); p.wall(5.30, 7.60, 7.93, 7.72, new=True)
    p.door(6.20, 7.60, 7.00, 7.72, "W", "N", kind="pocket", new=True)
    p.wardrobe("Bedroom S", 5.30, 5.43, 5.95, 7.60, label="Closet 2.2 m")
    p.shower("Bedroom S", 6.07, 5.43, 7.00, 6.63, glass=("S","E"))
    p.wc("Bedroom S", 7.20, 5.43, 7.60, 6.11, facing="S")
    p.vanity("Bedroom S", 7.33, 6.90, 7.93, 7.60, basins=1, wall="E", label="Basin")
    p.bed("Bedroom S", 5.80, 7.72, 7.40, 9.72, head="N", label="Bed 1.6 × 2.0")
    p.nightstand("Bedroom S", 5.33, 7.72, 5.78, 8.17); p.nightstand("Bedroom S", 7.45, 7.72, 7.90, 8.17)
    p.furn("Bedroom S", 4.30, 10.08, 5.50, 10.68, "Desk")
    p.zone("vestibule", 4.30, 5.43, 5.30, 7.60, "vestibule 1.0", kind="path")
    p.callout(1, 4.75, 4.2); p.callout(2, 6.5, 3.5); p.callout(3, 3.0, 9.0); p.callout(4, 3.55, 1.0)
    p.dim("h", 4.30, 5.30, 11.04+0.4, "1.0"); p.dim("h", 5.30, 5.95, 11.04+0.4, "0.65"); p.dim("h", 6.07, 7.93, 11.04+0.4, "1.86")
    p.dim("v", 7.72, 10.68, -0.35, "2.96"); p.dim("v", 5.43, 7.72, -0.35, "2.29")
    return p

# ======================================================================= EG
def eg_base(title):
    p = Plan(8.29, 11.04, title)
    p.shell()
    p.window("N", 4.78, 6.75); p.window("E", 7.08, 9.06); p.window("S", 1.08, 3.02); p.window("S", 4.98, 6.98)
    p.door(1.84, 0.0, 2.78, 0.36, "W", "S"); p._text("dims", 2.31, -0.12, "entrance", "note")
    p.stairs(0.22, 1.55, 1.25, 3.82, n=13, up="S")
    p.chimney(2.78, 1.98, 3.63, 3.63)
    p.north(8.29+0.9, -0.5); p.scalebar(0.0, 11.04+0.75)
    return p

def eg_current():
    p = eg_base("Ground floor, as drawn today")
    p.room("Hall + living + kitchen", 0.22, 0.38, 7.93, 10.68, lx=5.8, ly=6.2, area=60.0)
    p.room("Guest WC", 0.22, 5.11, 1.58, 7.36, lx=0.9, ly=6.9)
    p.room("Bedroom", 0.22, 7.55, 3.02, 10.68, lx=1.6, ly=7.9, area=13.0, sub="incl. corridor")
    p.wall(0.22, 4.98, 3.12, 5.11); p.wall(1.58, 5.11, 1.70, 7.36); p.wall(0.22, 7.36, 1.70, 7.55); p.wall(3.02, 5.11, 3.12, 10.68); p.wall(1.70, 7.36, 3.02, 7.55)
    p.door(1.84, 4.98, 2.74, 5.11, "E", "S"); p.door(1.58, 5.71, 1.70, 6.56, "N", "E"); p.door(1.84, 7.36, 2.74, 7.55, "E", "S")
    p.vanity("WC", 0.28, 5.76, 0.52, 6.13, basins=1, wall="W", label="Basin"); p.wc("WC", 0.90, 5.43, 1.27, 5.80, facing="S")
    p.radiator("WC", 0.22, 5.11, 1.58, 5.21)
    p.bed("Bedroom", 0.22, 8.20, 2.22, 10.10, head="W", label="Bed 1.9 × 2.0")
    p.nightstand("Bedroom", 0.22, 7.70, 0.64, 8.17); p.nightstand("Bedroom", 0.22, 10.13, 0.64, 10.52)
    p.kitchen("Kitchen", 3.63, 0.42, 7.93, 1.00); p.furn("Kitchen", 4.58, 2.17, 6.98, 3.40, "Island 2.4 × 1.2")
    p.furn("Dining", 4.67, 4.48, 6.75, 5.61, "Table 2.1 × 1.1")
    p.sofa("Living", 4.62, 6.56, 6.65, 7.60, back="N"); p.sofa("Living", 6.75, 8.26, 7.79, 10.24, back="E")
    p.dim("h", 3.63, 7.93, -0.3, "4.30 kitchen wall"); p.dim("v", 7.55, 10.68, -0.35, "3.13"); p.dim("h", 0.22, 3.02, 11.04+0.4, "2.80")
    return p

def eg_E1():
    p = eg_base("Ground floor, option E1")
    p.room("Entrance hall", 0.22, 0.38, 2.78, 4.90, lx=1.75, ly=4.3, area=11.6)
    p.room("Living · dining · kitchen", 2.78, 0.38, 7.93, 10.68, lx=5.9, ly=6.35, area=46.7)
    p.room("Guest bath", 0.22, 5.02, 2.22, 7.30, lx=0.78, ly=5.92)
    p.room("Corridor", 2.34, 5.02, 3.51, 7.30, lx=2.93, ly=6.95)
    p.room("Bedroom", 0.22, 7.42, 3.51, 10.68, lx=1.6, ly=7.75)
    p.wall(0.22, 4.90, 3.63, 5.02, new=True); p.wall(2.22, 5.02, 2.34, 7.30, new=True)
    p.wall(3.51, 5.02, 3.63, 10.68, new=True); p.wall(0.22, 7.30, 3.51, 7.42, new=True)
    p.removed_wall(1.58, 5.11, 1.70, 7.36); p.removed_wall(3.02, 5.11, 3.12, 10.68); p.removed_wall(0.22, 7.36, 1.70, 7.55)
    p.door(2.46, 4.90, 3.39, 5.02, "W", "S", kind="open")          # hall -> corridor, open
    p.door(2.22, 5.60, 2.34, 6.50, "N", "E", new=True)              # bath door, opens outward into corridor
    p.door(2.46, 7.30, 3.36, 7.42, "E", "S", new=True)              # corridor -> bedroom
    # hall
    p.wardrobe("Hall", 2.18, 1.40, 2.78, 3.50)
    p.furn("Hall", 0.22, 0.45, 0.62, 1.45, "Bench")
    p.zone("entrance door swing", 1.84, 0.36, 2.78, 1.30, "")
    # guest bath 2.0 x 2.28
    p.shower("Bath", 0.22, 6.30, 1.42, 7.30, glass=("N","E"))
    p.wc("Bath", 1.62, 6.62, 2.02, 7.30, facing="N")
    p.vanity("Bath", 1.10, 5.02, 2.00, 5.52, basins=1, wall="N", label="Basin 0.9 m")
    p.radiator("Bath", 0.22, 5.10, 0.32, 5.90)
    p.zone("basin standing", 1.10, 5.52, 2.00, 6.30, "0.8")
    p.zone("WC front", 1.42, 5.82, 2.22, 6.62, "0.8", kind="path")
    # bedroom
    p.bed("Bedroom", 0.22, 8.15, 2.22, 10.05, head="W", label="Bed 1.9 × 2.0")
    p.nightstand("Bedroom", 0.22, 7.60, 0.72, 8.10); p.nightstand("Bedroom", 0.22, 10.10, 0.72, 10.60)
    p.wardrobe("Bedroom", 2.96, 8.60, 3.51, 10.68)
    p.zone("foot aisle", 2.22, 8.15, 2.96, 10.05, "0.74")
    p.zone("bed side N", 0.72, 7.42, 2.22, 8.15, "0.73"); p.zone("bed side S", 0.72, 10.05, 2.22, 10.68, "0.63")
    # kitchen / dining / living
    p.kitchen("Kitchen", 3.63, 0.38, 7.93, 0.98, sink=4.95, hob=7.25)
    p.label(4.2, 1.2, "tall units", "tiny")
    p.furn("Kitchen", 4.90, 2.18, 7.30, 3.38, "Island 2.4 × 1.2")
    p.zone("island aisle 1.2", 4.90, 0.98, 7.30, 2.18, "1.2 m", kind="path")
    p.table("Dining", 4.90, 4.90, 6.90, 5.90, chairs=(3,3,0,0), label="Table")
    p.sofa("Living", 4.30, 7.20, 6.30, 8.20, back="N")
    p.sofa("Living", 6.93, 8.50, 7.93, 10.50, back="E")
    p.furn("Living", 5.20, 8.60, 6.20, 9.40, "Coffee table")
    p.furn("Living", 3.63, 8.60, 4.03, 10.40, "TV")
    p.zone("passage hall→living", 2.78, 3.63, 3.63, 4.90, "0.85", kind="path")
    p.callout(1, 2.5, 1.2); p.callout(2, 0.62, 6.12); p.callout(3, 2.93, 6.3); p.callout(4, 3.0, 9.9); p.callout(5, 4.6, 1.5)
    p.dim("h", 3.63, 7.93, -0.3, "4.30 kitchen wall"); p.dim("h", 0.22, 2.22, 11.04+0.4, "2.00"); p.dim("h", 2.34, 3.51, 11.04+0.4, "1.17")
    p.dim("v", 7.42, 10.68, -0.35, "3.26"); p.dim("v", 5.02, 7.30, -0.35, "2.28")
    return p

ALL = dict(dg_current=dg_current, dg_A=dg_A, dg_B=dg_B, dg_C=dg_C, og_current=og_current, og_O1=og_O1, og_O2=og_O2, eg_current=eg_current, eg_E1=eg_E1)

if __name__ == "__main__":
    for k, f in ALL.items():
        p = f()
        issues = p.check()
        print(f"== {k}: {len(issues)} issues; rooms {[(n, round(a,1)) for n,a in p.rooms]}")
        for i in issues: print("   -", i)
