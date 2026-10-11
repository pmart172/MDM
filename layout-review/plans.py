"""Draws the proposed floor plans as SVG (metres -> px)."""
S = 62  # px per metre
PAD_L, PAD_T, PAD_R, PAD_B = 46, 30, 42, 46

def px(v): return round(v * S, 1)

class Plan:
    def __init__(self, W, H, left=0.22, other=0.36):
        self.W, self.H = W, H
        self.left, self.other = left, other
        self.parts = []
        self.dims = []
    def rect(self, x0, y0, x1, y1, cls, rx=0):
        self.parts.append(f'<rect x="{px(x0)}" y="{px(y0)}" width="{px(x1-x0)}" height="{px(y1-y0)}" class="{cls}"{f' rx="{rx}"' if rx else ""} shape-rendering="crispEdges"/>')
    def room(self, name, x0, y0, x1, y1, area=None, cls="room", lx=None, ly=None):
        self.rect(x0, y0, x1, y1, cls)
        a = area if area is not None else (x1-x0)*(y1-y0)
        cx = (x0+x1)/2 if lx is None else lx
        cy = (y0+y1)/2 if ly is None else ly
        self.parts.append(
            f'<text x="{px(cx)}" y="{px(cy)-4}" class="rname">{name}</text>'
            f'<text x="{px(cx)}" y="{px(cy)+12}" class="rarea">{a:.1f} m²</text>')
    def wall(self, x0, y0, x1, y1):
        self.rect(x0, y0, x1, y1, "wall")
    def window(self, side, a, b, note=None):
        t = self.other
        if side == "N": r = (a, 0, b, t)
        elif side == "S": r = (a, self.H - t, b, self.H)
        elif side == "E": r = (self.W - t, a, self.W, b)
        else: r = (0, a, self.left, b)
        x0, y0, x1, y1 = r
        self.rect(x0, y0, x1, y1, "win")
        if side in "NS":
            ym = (y0+y1)/2
            self.parts.append(f'<line x1="{px(x0)}" y1="{px(ym)}" x2="{px(x1)}" y2="{px(ym)}" class="winl"/>')
        else:
            xm = (x0+x1)/2
            self.parts.append(f'<line x1="{px(xm)}" y1="{px(y0)}" x2="{px(xm)}" y2="{px(y1)}" class="winl"/>')
        if note:
            cx, cy = (x0+x1)/2, (y0+y1)/2
            dy = -14 if side == "N" else (16 if side == "S" else 0)
            anchor = "middle" if side in "NS" else ("start" if side == "E" else "end")
            dx = 8 if side == "E" else (-8 if side == "W" else 0)
            self.parts.append(f'<text x="{px(cx)+dx}" y="{px(cy)+dy+4}" class="note" text-anchor="{anchor}">{note}</text>')
    def door(self, x0, y0, x1, y1, hinge, swing, sliding=False):
        # opening rect, hinge end (N/S/E/W), swing direction (N/S/E/W)
        self.rect(x0, y0, x1, y1, "open")
        horiz = (x1-x0) > (y1-y0)
        L = (x1-x0) if horiz else (y1-y0)
        if horiz:
            hy = (y0+y1)/2
            hx = x0 if hinge == "W" else x1
            ex = x1 if hinge == "W" else x0
            ty = hy + (L if swing == "S" else -L)
            tip = (hx, ty)
        else:
            hx = (x0+x1)/2
            hy = y0 if hinge == "N" else y1
            ey = y1 if hinge == "N" else y0
            tx = hx + (L if swing == "E" else -L)
            tip = (tx, hy)
        if sliding:
            if horiz:
                self.parts.append(f'<line x1="{px(x0)}" y1="{px(hy)}" x2="{px(x1)}" y2="{px(hy)}" class="slide"/>')
            else:
                self.parts.append(f'<line x1="{px(hx)}" y1="{px(y0)}" x2="{px(hx)}" y2="{px(y1)}" class="slide"/>')
            return
        # leaf
        self.parts.append(f'<line x1="{px(hx)}" y1="{px(hy)}" x2="{px(tip[0])}" y2="{px(tip[1])}" class="leaf"/>')
        # arc from the far end of the opening to the leaf tip
        if horiz:
            start = (ex, hy)
        else:
            start = (hx, ey)
        r = px(L)
        # choose sweep so the arc is the quarter circle on the swing side
        import math
        a0 = math.atan2(start[1]-hy, start[0]-hx)
        a1 = math.atan2(tip[1]-hy, tip[0]-hx)
        d = (a1 - a0) % (2*math.pi)
        sweep = 1 if d < math.pi else 0
        self.parts.append(f'<path d="M {px(start[0])} {px(start[1])} A {r} {r} 0 0 {sweep} {px(tip[0])} {px(tip[1])}" class="arc"/>')
    def fix(self, kind, x0, y0, x1, y1, label=None):
        cls = {"bed":"f-bed","bath":"f-wet","wc":"f-wet","shower":"f-wet","basin":"f-wet",
               "ward":"f-ward","furn":"f-furn","appl":"f-furn","rad":"f-rad"}[kind]
        rx = 4 if kind in ("bath","wc") else 0
        self.rect(x0, y0, x1, y1, cls, rx)
        if kind == "bed":
            # pillows
            w, h = x1-x0, y1-y0
            if w >= h:  # head on W or E? assume head at the narrower side -> pillows along one short side; caller passes label 'W'/'E'/'N'/'S'
                pass
        if kind == "shower":
            self.parts.append(f'<line x1="{px(x0)}" y1="{px(y0)}" x2="{px(x1)}" y2="{px(y1)}" class="thin"/><line x1="{px(x1)}" y1="{px(y0)}" x2="{px(x0)}" y2="{px(y1)}" class="thin"/>')
        if kind == "ward":
            # hanging rail line
            if (x1-x0) > (y1-y0):
                ym=(y0+y1)/2; self.parts.append(f'<line x1="{px(x0)}" y1="{px(ym)}" x2="{px(x1)}" y2="{px(ym)}" class="thin"/>')
            else:
                xm=(x0+x1)/2; self.parts.append(f'<line x1="{px(xm)}" y1="{px(y0)}" x2="{px(xm)}" y2="{px(y1)}" class="thin"/>')
        if label:
            cx, cy = (x0+x1)/2, (y0+y1)/2
            if (y1-y0) > (x1-x0) and (x1-x0) < 1.0:
                self.parts.append(f'<text transform="translate({px(cx)+3} {px(cy)}) rotate(-90)" class="flabel">{label}</text>')
            else:
                self.parts.append(f'<text x="{px(cx)}" y="{px(cy)+3}" class="flabel">{label}</text>')
    def pillows(self, head, x0, y0, x1, y1):
        # draw two pillows at the head side of the bed rectangle
        if head == "W":
            for i,(a,b) in enumerate([(y0+0.1, (y0+y1)/2-0.05), ((y0+y1)/2+0.05, y1-0.1)]):
                self.rect(x0+0.1, a, x0+0.5, b, "pillow", 2)
        elif head == "E":
            for a,b in [(y0+0.1, (y0+y1)/2-0.05), ((y0+y1)/2+0.05, y1-0.1)]:
                self.rect(x1-0.5, a, x1-0.1, b, "pillow", 2)
        elif head == "N":
            for a,b in [(x0+0.1, (x0+x1)/2-0.05), ((x0+x1)/2+0.05, x1-0.1)]:
                self.rect(a, y0+0.1, b, y0+0.5, "pillow", 2)
        else:
            for a,b in [(x0+0.1, (x0+x1)/2-0.05), ((x0+x1)/2+0.05, x1-0.1)]:
                self.rect(a, y1-0.5, b, y1-0.1, "pillow", 2)
    def stair(self, x0, y0, x1, y1, n=12):
        self.rect(x0, y0, x1, y1, "stairs")
        for i in range(1, n):
            y = y0 + (y1-y0)*i/n
            self.parts.append(f'<line x1="{px(x0)}" y1="{px(y)}" x2="{px(x1)}" y2="{px(y)}" class="thin"/>')
        xm=(x0+x1)/2
        self.parts.append(f'<line x1="{px(xm)}" y1="{px(y1)-6}" x2="{px(xm)}" y2="{px(y0)+6}" class="arrow"/>')
    def chimney(self, x0, y0, x1, y1):
        self.rect(x0, y0, x1, y1, "chim")
    def text(self, x, y, s, cls="note", anchor="middle"):
        self.parts.append(f'<text x="{px(x)}" y="{px(y)}" class="{cls}" text-anchor="{anchor}">{s}</text>')
    def dim(self, kind, a, b, pos, label):
        # kind 'h': horizontal from a to b at y=pos ; 'v': vertical from a to b at x=pos
        if kind == "h":
            self.parts.append(f'<line x1="{px(a)}" y1="{px(pos)}" x2="{px(b)}" y2="{px(pos)}" class="dim"/>'
                              f'<line x1="{px(a)}" y1="{px(pos)-5}" x2="{px(a)}" y2="{px(pos)+5}" class="dim"/>'
                              f'<line x1="{px(b)}" y1="{px(pos)-5}" x2="{px(b)}" y2="{px(pos)+5}" class="dim"/>'
                              f'<text x="{px((a+b)/2)}" y="{px(pos)-5}" class="dimt" text-anchor="middle">{label}</text>')
        else:
            self.parts.append(f'<line x1="{px(pos)}" y1="{px(a)}" x2="{px(pos)}" y2="{px(b)}" class="dim"/>'
                              f'<line x1="{px(pos)-5}" y1="{px(a)}" x2="{px(pos)+5}" y2="{px(a)}" class="dim"/>'
                              f'<line x1="{px(pos)-5}" y1="{px(b)}" x2="{px(pos)+5}" y2="{px(b)}" class="dim"/>'
                              f'<text transform="translate({px(pos)-6} {px((a+b)/2)}) rotate(-90)" class="dimt" text-anchor="middle">{label}</text>')
    def svg(self, title):
        w = px(self.W) + PAD_L + PAD_R
        h = px(self.H) + PAD_T + PAD_B
        body = "\n".join(self.parts)
        return (f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="{title}" class="plan">'
                f'<g transform="translate({PAD_L} {PAD_T})">'
                f'<rect x="0" y="0" width="{px(self.W)}" height="{px(self.H)}" class="wall"/>'
                f'{body}</g></svg>')

def start(W, H):
    p = Plan(W, H)
    return p

# ---------------------------------------------------------------- DG loop 1
def dg_l1():
    p = start(7.13, 8.20)
    # rooms
    p.room("Hall / stairs", 0.22, 0.35, 2.82, 3.64, lx=1.6, ly=3.1)
    p.room("Walk-in closet", 3.06, 0.35, 6.75, 3.05, ly=1.75)
    p.room("Bedroom", 2.94, 3.17, 6.75, 7.84, lx=5.5, ly=4.3)
    p.room("Bath", 0.22, 3.76, 2.82, 7.84, lx=1.1, ly=6.5)
    # walls
    p.wall(2.82, 0.35, 3.06, 3.17)       # hall | closet (with chimney)
    p.wall(2.82, 3.17, 2.94, 7.84)       # hall+bath | bedroom (moved 0.5 m west)
    p.wall(2.94, 3.05, 6.75, 3.17)       # closet | bedroom (moved 0.6 m north)
    p.wall(0.22, 3.64, 2.82, 3.76)       # hall | bath
    p.chimney(2.82, 0.35, 3.06, 1.95)
    # windows (unchanged)
    p.window("N", 0.66, 2.50); p.window("E", 1.04, 3.05); p.window("E", 4.96, 6.90)
    p.window("S", 0.80, 2.83); p.window("S", 4.10, 6.14)
    # stair
    p.stair(0.22, 0.35, 1.25, 2.60)
    p.rect(1.25, 0.5, 2.1, 2.5, "void")
    # doors
    p.door(2.82, 2.03, 3.06, 2.93, "N", "E")        # hall -> closet (existing)
    p.door(1.84, 3.64, 2.74, 3.76, "E", "S")        # hall -> bath (existing)
    p.door(5.70, 3.05, 6.60, 3.17, "E", "S")        # closet -> bedroom
    # closet fixtures
    p.fix("ward", 3.06, 0.35, 6.75, 0.95, "Wardrobe 3.7 m")
    p.fix("ward", 3.06, 0.95, 3.66, 1.95)
    p.fix("ward", 4.00, 2.45, 5.60, 3.05, "Wardrobe 1.6 m")
    p.fix("furn", 6.25, 1.30, 6.75, 2.60, "Table")
    # bedroom
    p.fix("bed", 2.94, 4.90, 4.94, 6.90, "Bed 2.0 × 2.0"); p.pillows("W", 2.94, 4.90, 4.94, 6.90)
    p.fix("furn", 2.94, 4.30, 3.44, 4.80); p.fix("furn", 2.94, 7.00, 3.44, 7.50)
    p.fix("furn", 4.60, 7.24, 5.80, 7.84, "Desk")
    p.fix("furn", 6.25, 5.00, 6.75, 6.80, "Dresser")
    # bath
    p.fix("shower", 0.22, 3.76, 1.62, 4.96, "Walk-in shower 1.4×1.2")
    p.fix("basin", 2.27, 5.10, 2.82, 6.60, "2 basins")
    p.fix("wc", 0.22, 5.25, 0.90, 5.65, "WC")
    p.fix("bath", 1.00, 7.04, 2.80, 7.84, "Tub 1.8×0.8")
    p.fix("rad", 0.22, 6.0, 0.32, 6.9)
    # dims
    p.dim("h", 2.94, 6.75, 8.20+0.35, "3.81")
    p.dim("h", 0.22, 2.82, 8.20+0.35, "2.60")
    p.dim("v", 3.17, 7.84, -0.35, "4.67")
    p.dim("v", 0.35, 3.05, 7.13+0.30, "2.70")
    p.dim("h", 0, 7.13, -0.25, "7.13")
    return p.svg("Top floor (DG), loop 1")

# ---------------------------------------------------------------- DG loop 2
def dg_l2():
    p = start(7.13, 8.20)
    p.room("Hall / stairs", 0.22, 0.35, 2.82, 3.64, lx=1.6, ly=3.1)
    p.room("Bath", 3.06, 0.35, 6.75, 3.64, lx=5.2, ly=2.4)
    p.room("Bedroom", 0.22, 3.76, 4.40, 7.84, lx=3.3, ly=5.3)
    p.room("Closet", 4.52, 3.76, 6.75, 7.84, lx=5.68, ly=5.9)
    p.wall(2.82, 0.35, 3.06, 3.64)
    p.wall(0.22, 3.64, 6.75, 3.76)
    p.wall(4.40, 3.76, 4.52, 7.84)
    p.chimney(2.82, 0.35, 3.06, 1.95)
    p.window("N", 0.66, 2.50); p.window("E", 1.04, 3.05); p.window("E", 4.96, 6.90)
    p.window("S", 0.80, 2.83)
    p.text(5.6, 8.20+0.62, "south window dropped (closet)", "note")
    p.stair(0.22, 0.35, 1.25, 2.60)
    p.rect(1.25, 0.5, 2.1, 2.5, "void")
    p.door(2.82, 2.03, 3.06, 2.93, "S", "E")        # hall -> bath (existing opening)
    p.door(1.84, 3.64, 2.74, 3.76, "E", "S")        # hall -> bedroom (existing opening)
    p.door(3.30, 3.64, 4.20, 3.76, "W", "S", sliding=True)  # bedroom -> bath, sliding
    p.door(4.40, 3.90, 4.52, 4.80, "N", "E")        # bedroom -> closet
    # bath
    p.fix("shower", 3.06, 0.35, 4.46, 1.55, "Walk-in shower 1.4×1.2")
    p.fix("basin", 4.60, 0.35, 6.20, 0.90, "2 basins")
    p.fix("bath", 5.95, 1.20, 6.75, 3.00, "Tub")
    p.fix("wc", 4.50, 2.96, 4.90, 3.64, "WC")
    p.fix("rad", 3.06, 1.70, 3.16, 2.0)
    # bedroom
    p.fix("bed", 0.22, 4.90, 2.22, 6.90, "Bed 2.0 × 2.0"); p.pillows("W", 0.22, 4.90, 2.22, 6.90)
    p.fix("furn", 0.22, 4.30, 0.72, 4.80); p.fix("furn", 0.22, 7.00, 0.72, 7.50)
    p.fix("furn", 3.90, 5.00, 4.40, 6.80, "Dresser")
    p.fix("furn", 2.80, 6.90, 3.60, 7.70, "Chair")
    # closet
    p.fix("ward", 4.52, 4.90, 5.12, 7.84, "Wardrobe 2.9 m")
    p.fix("ward", 5.45, 3.76, 6.75, 4.36, "Wardrobe 1.3 m")
    p.fix("ward", 5.12, 7.24, 6.75, 7.84, "Wardrobe 1.6 m")
    p.fix("furn", 6.25, 5.10, 6.75, 6.80, "Table")
    p.dim("h", 0.22, 4.40, 8.20+0.35, "4.18")
    p.dim("h", 4.52, 6.75, 8.20+0.35, "2.23")
    p.dim("v", 3.76, 7.84, -0.35, "4.08")
    p.dim("v", 0.35, 3.64, 7.13+0.30, "3.29")
    p.dim("h", 0, 7.13, -0.25, "7.13")
    return p.svg("Top floor (DG), loop 2")

# ---------------------------------------------------------------- OG loop 2
def og_l2():
    p = start(8.29, 11.04)
    p.room("Landing / living", 0.22, 0.38, 3.51, 7.50, lx=2.2, ly=4.4)
    p.room("Bath", 0.22, 7.62, 3.51, 10.68, lx=1.5, ly=8.9)
    p.room("Bedroom N", 3.63, 0.38, 7.93, 5.30, lx=6.3, ly=1.5)
    p.room("Bedroom S", 3.63, 5.42, 7.93, 10.68, lx=6.3, ly=9.2)
    p.wall(3.51, 0.38, 3.63, 10.68)
    p.wall(3.63, 5.30, 7.93, 5.42)
    p.wall(0.22, 7.50, 3.51, 7.62)
    p.chimney(2.82, 1.37, 3.05, 3.92)
    p.window("N", 1.08, 3.02); p.window("N", 5.15, 7.13)
    p.window("E", 1.70, 3.63); p.window("E", 7.13, 9.11)
    p.window("S", 1.08, 3.02); p.window("S", 5.15, 7.13)
    p.stair(0.22, 1.37, 1.25, 3.92)
    p.door(3.51, 3.60, 3.63, 4.50, "N", "E")   # -> Zimmer Nord
    p.door(3.51, 6.50, 3.63, 7.40, "S", "E")   # -> Zimmer Süd
    p.door(1.00, 7.50, 1.90, 7.62, "E", "S")   # -> Bad
    # living nook
    p.fix("furn", 0.22, 5.00, 1.22, 7.00, "Sofa 2×1")
    p.fix("furn", 3.10, 5.00, 3.51, 6.40, "TV")
    p.fix("furn", 1.50, 0.40, 3.00, 1.00, "Desk nook")
    # bath
    p.fix("basin", 0.22, 7.90, 0.77, 9.40, "2 basins")
    p.wall(2.28, 7.62, 2.40, 9.12); p.wall(2.40, 9.00, 3.51, 9.12)
    p.door(2.28, 8.15, 2.40, 8.95, "S", "W", sliding=True)
    p.fix("wc", 2.83, 7.70, 3.51, 8.10, "WC")
    p.text(2.95, 8.65, "WC room", "note")
    p.fix("shower", 2.31, 9.48, 3.51, 10.68, "Shower 1.2×1.2")
    p.fix("bath", 0.22, 9.88, 2.02, 10.68, "Tub 1.8×0.8")
    p.fix("rad", 1.0, 9.30, 2.0, 9.40)
    # bedroom N
    p.fix("ward", 3.63, 0.38, 5.13, 3.20, "Closet 1.5×2.8")
    p.wall(5.13, 0.38, 5.25, 3.20); p.wall(3.63, 3.20, 5.25, 3.32)
    p.door(4.00, 3.20, 4.80, 3.32, "W", "S", sliding=True)
    p.fix("bed", 4.80, 3.30, 6.40, 5.30, "Bed 1.6×2.0"); p.pillows("S", 4.80, 3.30, 6.40, 5.30)
    p.fix("furn", 4.30, 4.80, 4.80, 5.30); p.fix("furn", 6.40, 4.80, 6.90, 5.30)
    p.fix("furn", 7.33, 1.90, 7.93, 3.30, "Table")
    # bedroom S
    p.fix("ward", 3.63, 7.86, 5.13, 10.68, "Closet 1.5×2.8")
    p.wall(5.13, 7.86, 5.25, 10.68); p.wall(3.63, 7.74, 5.25, 7.86)
    p.door(4.00, 7.74, 4.80, 7.86, "W", "N", sliding=True)
    p.fix("bed", 5.30, 5.42, 6.90, 7.42, "Bed 1.6×2.0"); p.pillows("N", 5.30, 5.42, 6.90, 7.42)
    p.fix("furn", 4.80, 5.42, 5.30, 5.92); p.fix("furn", 6.90, 5.42, 7.40, 5.92)
    p.fix("furn", 7.33, 7.50, 7.93, 8.90, "Table")
    p.dim("h", 0.22, 3.51, 11.04+0.35, "3.29")
    p.dim("h", 3.63, 7.93, 11.04+0.35, "4.30")
    p.dim("v", 0.38, 5.30, 8.29+0.30, "4.92")
    p.dim("v", 5.42, 10.68, 8.29+0.30, "5.26")
    p.dim("v", 7.62, 10.68, -0.35, "3.06")
    return p.svg("Upper floor (OG), loop 2")

# ---------------------------------------------------------------- EG loop 2
def eg_l2():
    p = start(8.29, 11.04)
    p.room("Entrance hall", 0.22, 0.38, 2.78, 4.90, lx=1.9, ly=4.3, area=11.6)
    p.room("Living / dining / kitchen", 2.78, 0.38, 7.93, 10.68, lx=5.7, ly=6.5, area=46.5)
    p.chimney(2.78, 1.98, 3.63, 3.63)
    p.room("Bath", 0.22, 5.02, 2.00, 7.30, lx=1.55, ly=6.1)
    p.room("Utility", 2.12, 5.02, 3.63, 7.30, lx=3.1, ly=5.9)
    p.room("Bedroom", 0.22, 7.42, 3.63, 10.68, lx=1.6, ly=7.75)
    p.wall(0.22, 4.90, 3.75, 5.02)
    p.wall(2.00, 5.02, 2.12, 7.30)
    p.wall(3.63, 5.02, 3.75, 10.68)
    p.wall(0.22, 7.30, 3.63, 7.42)
    p.window("N", 4.78, 6.75); p.window("E", 7.08, 9.06)
    p.window("S", 1.08, 3.02); p.window("S", 4.98, 6.98)
    p.stair(0.22, 1.55, 1.25, 3.82)
    p.door(1.84, 0.0, 2.78, 0.36, "W", "S")       # entrance
    p.text(2.3, -0.12, "Entrance", "note")
    p.door(0.90, 4.90, 1.80, 5.02, "E", "S")       # hall -> bath
    p.door(3.63, 5.30, 3.75, 6.20, "N", "E")       # living -> HWR
    p.door(3.63, 7.60, 3.75, 8.50, "N", "W")       # living -> bedroom
    # hall
    p.fix("ward", 2.18, 1.40, 2.78, 3.50, "Wardrobe 2.1 m")
    # bath
    p.fix("basin", 0.22, 5.10, 0.72, 5.80, "Basin")
    p.fix("shower", 0.22, 6.10, 1.22, 7.30, "Shower")
    p.fix("wc", 1.50, 6.62, 1.90, 7.30, "WC")
    # utility
    p.fix("appl", 2.12, 6.70, 2.72, 7.30, "Washer"); p.fix("appl", 2.72, 6.70, 3.32, 7.30, "Dryer")
    p.fix("ward", 2.12, 5.10, 2.52, 6.40, "Shelves")
    # bedroom
    p.fix("bed", 0.22, 8.20, 2.22, 10.10, "Bed 1.9 × 2.0"); p.pillows("W", 0.22, 8.20, 2.22, 10.10)
    p.fix("furn", 0.22, 7.60, 0.72, 8.10); p.fix("furn", 0.22, 10.18, 0.72, 10.68)
    p.fix("ward", 3.03, 8.70, 3.63, 10.68, "Wardrobe")
    # kitchen / living
    p.fix("furn", 3.63, 0.38, 7.93, 0.98, "Kitchen run 4.3 m")
    p.fix("furn", 4.70, 2.10, 7.10, 3.30, "Island 2.4 × 1.2")
    p.fix("furn", 4.90, 4.60, 6.90, 5.60, "Table 2 × 1")
    p.fix("furn", 4.40, 7.30, 6.40, 8.30, "Sofa 2 × 1")
    p.fix("furn", 6.93, 8.60, 7.93, 10.60, "Sofa 2 × 1")
    p.fix("furn", 5.20, 8.70, 6.30, 9.50, "Table")
    p.fix("furn", 3.75, 8.80, 4.15, 10.50, "TV")
    p.dim("h", 3.63, 7.93, -0.25+0.0, "4.30")
    p.dim("v", 7.42, 10.68, -0.35, "3.26")
    p.dim("v", 5.02, 7.30, -0.35, "2.28")
    p.dim("h", 0.22, 3.63, 11.04+0.35, "3.41")
    return p.svg("Ground floor (EG), loop 2")

if __name__ == "__main__":
    import sys
    for f in (dg_l1, dg_l2, og_l2, eg_l2):
        open(f"{f.__name__}.svg","w").write(f())
        print(f.__name__, "ok")
