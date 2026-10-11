"""Floor-plan drawing engine v2. Metres in, inline SVG out.

Layers (drawn in this order): floor, outside, zones, fixtures, walls, windows, openings,
leaves, diff, labels, dims. Every shape carries an explicit fill via a CSS class.
"""
import math

S = 64.0  # px per metre
PAD = dict(l=52, t=40, r=52, b=60)

def P(v): return round(v * S, 1)

class Plan:
    def __init__(self, W, H, title, ext=0.36, west=0.22, outside=None):
        self.W, self.H, self.title = W, H, title
        self.ext, self.west = ext, west
        self.layers = {k: [] for k in ("floor","outside","zones","fixtures","walls","windows","openings","leaves","diff","labels","dims")}
        self.rooms = []      # (name, area)
        self.fixtures = []   # (room, name, w, d)
        self.boxes = []      # (name, x0,y0,x1,y1, kind) for clearance checks
        self.wall_boxes = []
        self.openings = []   # (x0,y0,x1,y1)
        self.swings = []     # (name, x0,y0,x1,y1)
        self.zones = []      # (name, x0,y0,x1,y1)
        self.outside = outside  # dict(x0,y0,x1,y1) lower-floor outline in plan coords
        self.extra = dict(l=0, t=0, r=0, b=0)
        if outside:
            self.extra = dict(l=max(0, -outside["x0"]), t=max(0, -outside["y0"]),
                              r=max(0, outside["x1"]-W), b=max(0, outside["y1"]-H))
    # ---------------------------------------------------------------- primitives
    def _rect(self, layer, x0, y0, x1, y1, cls, rx=0, extra=""):
        self.layers[layer].append(
            f'<rect x="{P(x0)}" y="{P(y0)}" width="{P(x1-x0)}" height="{P(y1-y0)}" class="{cls}"'
            + (f' rx="{rx}"' if rx else "") + (f" {extra}" if extra else "") + "/>")
    def _line(self, layer, x0, y0, x1, y1, cls):
        self.layers[layer].append(f'<line x1="{P(x0)}" y1="{P(y0)}" x2="{P(x1)}" y2="{P(y1)}" class="{cls}"/>')
    def _circle(self, layer, cx, cy, r, cls):
        self.layers[layer].append(f'<circle cx="{P(cx)}" cy="{P(cy)}" r="{P(r)}" class="{cls}"/>')
    def _ellipse(self, layer, cx, cy, rx, ry, cls):
        self.layers[layer].append(f'<ellipse cx="{P(cx)}" cy="{P(cy)}" rx="{P(rx)}" ry="{P(ry)}" class="{cls}"/>')
    def _text(self, layer, x, y, s, cls, anchor="middle", rot=None, dy=0):
        if rot:
            self.layers[layer].append(f'<text transform="translate({P(x)} {P(y)}) rotate({rot})" class="{cls}" text-anchor="{anchor}">{s}</text>')
        else:
            self.layers[layer].append(f'<text x="{P(x)}" y="{P(y)+dy}" class="{cls}" text-anchor="{anchor}">{s}</text>')
    # ---------------------------------------------------------------- building
    def room(self, name, x0, y0, x1, y1, lx=None, ly=None, area=None, sub=None):
        self._rect("floor", x0, y0, x1, y1, "floor", extra='shape-rendering="crispEdges"')
        a = area if area is not None else (x1-x0)*(y1-y0)
        self.rooms.append((name, a))
        cx = (x0+x1)/2 if lx is None else lx
        cy = (y0+y1)/2 if ly is None else ly
        self._text("labels", cx, cy, name, "rname", dy=-4)
        self._text("labels", cx, cy, f"{a:.1f} m²", "rarea", dy=11)
        if sub:
            self._text("labels", cx, cy, sub, "rsub", dy=24)
    def wall(self, x0, y0, x1, y1, new=False):
        self._rect("walls", x0, y0, x1, y1, "wall-new" if new else "wall", extra='shape-rendering="crispEdges"')
        self.wall_boxes.append((x0, y0, x1, y1))
    def removed_wall(self, x0, y0, x1, y1):
        self._rect("diff", x0, y0, x1, y1, "wall-gone")
    def chimney(self, x0, y0, x1, y1):
        self._rect("walls", x0, y0, x1, y1, "chim")
        self.wall_boxes.append((x0, y0, x1, y1))
    def shell(self):
        # exterior wall band: outer rect in wall colour drawn under floors (floor layer first element)
        self.layers["floor"].insert(0, f'<rect x="0" y="0" width="{P(self.W)}" height="{P(self.H)}" class="wall"/>')
        self.wall_boxes += [(0,0,self.W,self.ext),(0,self.H-self.ext,self.W,self.H),(0,0,self.west,self.H),(self.W-self.ext,0,self.W,self.H)]
    def set_back(self, label):
        o = self.outside
        self._rect("outside", o["x0"], o["y0"], o["x1"], o["y1"], "outline")
        # hatch strips: north, east, south
        for (x0,y0,x1,y1) in [(o["x0"], o["y0"], o["x1"], 0), (self.W, 0, o["x1"], self.H), (o["x0"], self.H, o["x1"], o["y1"])]:
            if x1 > x0 and y1 > y0:
                self._rect("outside", x0, y0, x1, y1, "terrace")
        self._text("dims", (o["x0"]+o["x1"])/2, o["y1"]+0.25, label, "note")
    def window(self, side, a, b, note=None, new=False):
        t = self.ext
        if side == "N": r = (a, 0, b, t)
        elif side == "S": r = (a, self.H - t, b, self.H)
        elif side == "E": r = (self.W - t, a, self.W, b)
        else: r = (0, a, self.west, b)
        x0, y0, x1, y1 = r
        self._rect("windows", x0, y0, x1, y1, "win-new" if new else "win")
        if side in "NS":
            for f in (0.35, 0.5, 0.65):
                ym = y0 + (y1-y0)*f; self._line("windows", x0, ym, x1, ym, "winl")
        else:
            for f in (0.35, 0.5, 0.65):
                xm = x0 + (x1-x0)*f; self._line("windows", xm, y0, xm, y1, "winl")
        if note:
            cx, cy = (x0+x1)/2, (y0+y1)/2
            if side == "N": self._text("dims", cx, -0.12, note, "note")
            elif side == "S": self._text("dims", cx, self.H+0.2, note, "note")
            elif side == "E": self._text("dims", self.W+0.22, cy, note, "note", rot=-90)
            else: self._text("dims", -0.22, cy, note, "note", rot=-90)
    def door(self, x0, y0, x1, y1, hinge, swing, kind="swing", new=False):
        """Opening rect in the wall. hinge: N/S/E/W end of the opening. swing: side (N/S/E/W).
        kind: swing | pocket | slide | open (no leaf)."""
        self._rect("openings", x0, y0, x1, y1, "open", extra='shape-rendering="crispEdges"')
        self.openings.append((x0, y0, x1, y1))
        horiz = (x1-x0) > (y1-y0)
        L = (x1-x0) if horiz else (y1-y0)
        tw = (y1-y0) if horiz else (x1-x0)
        if kind == "open":
            return
        if kind in ("pocket", "slide"):
            cls = "leaf-new" if new else "leaf"
            if horiz:
                ym = (y0+y1)/2
                # leaf drawn half open: a thick line across the opening, offset to the pocket side
                self._line("leaves", x0, ym, x1, ym, "slide")
                self._text("leaves", (x0+x1)/2, ym - 0.1 if swing == "N" else ym + 0.2, "⇆" if kind=="slide" else "pocket", "tiny")
            else:
                xm = (x0+x1)/2
                self._line("leaves", xm, y0, xm, y1, "slide")
                self._text("leaves", xm, (y0+y1)/2, "pocket" if kind=="pocket" else "⇅", "tiny", rot=-90)
            return
        # swing door
        if horiz:
            hy = (y0+y1)/2
            hx = x0 if hinge == "W" else x1
            ex = x1 if hinge == "W" else x0
            ty = hy + (L if swing == "S" else -L)
            tip, start = (hx, ty), (ex, hy)
            box = (min(x0,x1), min(hy, ty), max(x0,x1), max(hy, ty))
        else:
            hx = (x0+x1)/2
            hy = y0 if hinge == "N" else y1
            ey = y1 if hinge == "N" else y0
            tx = hx + (L if swing == "E" else -L)
            tip, start = (tx, hy), (hx, ey)
            box = (min(hx, tx), min(y0,y1), max(hx, tx), max(y0,y1))
        self.swings.append(("door swing", *box))
        cls = "leaf-new" if new else "leaf"
        self._line("leaves", hx, hy, tip[0], tip[1], cls)
        r = P(L)
        a0 = math.atan2(start[1]-hy, start[0]-hx); a1 = math.atan2(tip[1]-hy, tip[0]-hx)
        d = (a1 - a0) % (2*math.pi); sweep = 1 if d < math.pi else 0
        self.layers["leaves"].append(f'<path d="M {P(start[0])} {P(start[1])} A {r} {r} 0 0 {sweep} {P(tip[0])} {P(tip[1])}" class="arc"/>')
    # ---------------------------------------------------------------- fixtures
    def _reg(self, room, name, x0, y0, x1, y1, kind="fix"):
        self.fixtures.append((room, name, round(x1-x0,2), round(y1-y0,2)))
        self.boxes.append((name, x0, y0, x1, y1, kind))
    def label(self, x, y, s, cls="flabel", rot=None):
        self._text("labels", x, y, s, cls, rot=rot, dy=3 if not rot else 0)
    def _autolabel(self, x0, y0, x1, y1, s, cls="flabel"):
        if not s: return
        if (y1-y0) > (x1-x0) and (x1-x0) < 1.0:
            self._text("labels", (x0+x1)/2 + 0.05, (y0+y1)/2, s, cls, rot=-90)
        else:
            self._text("labels", (x0+x1)/2, (y0+y1)/2, s, cls, dy=3)
    def bed(self, room, x0, y0, x1, y1, head, label=None):
        self._rect("fixtures", x0, y0, x1, y1, "f-bed")
        w, h = x1-x0, y1-y0
        # headboard bar + pillows + duvet fold
        if head == "W":
            self._rect("fixtures", x0, y0, x0+0.08, y1, "f-head")
            for a,b in ((y0+0.12, (y0+y1)/2-0.05), ((y0+y1)/2+0.05, y1-0.12)):
                self._rect("fixtures", x0+0.15, a, x0+0.6, b, "pillow", rx=3)
            self._line("fixtures", x0+0.85, y0, x0+0.85, y1, "thin")
        elif head == "E":
            self._rect("fixtures", x1-0.08, y0, x1, y1, "f-head")
            for a,b in ((y0+0.12, (y0+y1)/2-0.05), ((y0+y1)/2+0.05, y1-0.12)):
                self._rect("fixtures", x1-0.6, a, x1-0.15, b, "pillow", rx=3)
            self._line("fixtures", x1-0.85, y0, x1-0.85, y1, "thin")
        elif head == "N":
            self._rect("fixtures", x0, y0, x1, y0+0.08, "f-head")
            for a,b in ((x0+0.12, (x0+x1)/2-0.05), ((x0+x1)/2+0.05, x1-0.12)):
                self._rect("fixtures", a, y0+0.15, b, y0+0.6, "pillow", rx=3)
            self._line("fixtures", x0, y0+0.85, x1, y0+0.85, "thin")
        else:
            self._rect("fixtures", x0, y1-0.08, x1, y1, "f-head")
            for a,b in ((x0+0.12, (x0+x1)/2-0.05), ((x0+x1)/2+0.05, x1-0.12)):
                self._rect("fixtures", a, y1-0.6, b, y1-0.15, "pillow", rx=3)
            self._line("fixtures", x0, y1-0.85, x1, y1-0.85, "thin")
        if label is None: label = f"Bed {w:.1f} × {h:.1f}" if head in "NS" else f"Bed {h:.1f} × {w:.1f}"
        self._text("labels", (x0+x1)/2 + (0.35 if head=="W" else -0.35 if head=="E" else 0), (y0+y1)/2 + (0.35 if head=="N" else -0.35 if head=="S" else 0), label, "flabel", dy=3)
        self._reg(room, label, x0, y0, x1, y1, "bed")
    def nightstand(self, room, x0, y0, x1, y1):
        self._rect("fixtures", x0, y0, x1, y1, "f-furn")
        self._reg(room, "Night table", x0, y0, x1, y1)
    def tub(self, room, x0, y0, x1, y1, label="Tub"):
        self._rect("fixtures", x0, y0, x1, y1, "f-wet", rx=5)
        self._rect("fixtures", x0+0.08, y0+0.08, x1-0.08, y1-0.08, "f-wet-in", rx=8)
        horiz = (x1-x0) >= (y1-y0)
        if horiz: self._circle("fixtures", x1-0.25, (y0+y1)/2, 0.04, "drain")
        else: self._circle("fixtures", (x0+x1)/2, y0+0.25, 0.04, "drain")
        self._autolabel(x0, y0, x1, y1, f"{label} {max(x1-x0,y1-y0):.1f}×{min(x1-x0,y1-y0):.1f}")
        self._reg(room, f"{label} {max(x1-x0,y1-y0):.2f} × {min(x1-x0,y1-y0):.2f}", x0, y0, x1, y1, "wet")
    def shower(self, room, x0, y0, x1, y1, glass=(), label="Shower"):
        self._rect("fixtures", x0, y0, x1, y1, "f-wet")
        self._circle("fixtures", (x0+x1)/2, (y0+y1)/2, 0.05, "drain")
        # tray falls
        self._line("fixtures", x0, y0, (x0+x1)/2, (y0+y1)/2, "hair"); self._line("fixtures", x1, y0, (x0+x1)/2, (y0+y1)/2, "hair")
        self._line("fixtures", x0, y1, (x0+x1)/2, (y0+y1)/2, "hair"); self._line("fixtures", x1, y1, (x0+x1)/2, (y0+y1)/2, "hair")
        for g in glass:
            if g == "N": self._line("fixtures", x0, y0, x1, y0, "glass")
            if g == "S": self._line("fixtures", x0, y1, x1, y1, "glass")
            if g == "E": self._line("fixtures", x1, y0, x1, y1, "glass")
            if g == "W": self._line("fixtures", x0, y0, x0, y1, "glass")
        self._autolabel(x0, y0, x1, y1, f"{label} {max(x1-x0,y1-y0):.1f}×{min(x1-x0,y1-y0):.1f}")
        self._reg(room, f"Walk-in shower {max(x1-x0,y1-y0):.2f} × {min(x1-x0,y1-y0):.2f}", x0, y0, x1, y1, "wet")
    def vanity(self, room, x0, y0, x1, y1, basins=2, wall="N", label=None):
        self._rect("fixtures", x0, y0, x1, y1, "f-wet")
        horiz = (x1-x0) >= (y1-y0)
        L = (x1-x0) if horiz else (y1-y0)
        for i in range(basins):
            f = (i+1)/(basins+1)
            if horiz:
                cx = x0 + L*f; cy = (y0+y1)/2
                self._ellipse("fixtures", cx, cy, 0.21, 0.17, "basin")
                self._circle("fixtures", cx, y0+0.08 if wall=="N" else y1-0.08, 0.03, "drain")
            else:
                cy = y0 + L*f; cx = (x0+x1)/2
                self._ellipse("fixtures", cx, cy, 0.17, 0.21, "basin")
                self._circle("fixtures", x0+0.08 if wall=="W" else x1-0.08, cy, 0.03, "drain")
        name = label or (f"{basins} basins {L:.1f} m" if basins > 1 else f"Basin {L:.1f} m")
        if horiz: self._text("labels", (x0+x1)/2, y1+0.16 if wall=="N" else y0-0.08, name, "flabel", dy=0)
        else: self._text("labels", x1+0.1 if wall=="W" else x0-0.1, (y0+y1)/2, name, "flabel", rot=-90)
        self._reg(room, (f"Double vanity {L:.2f} m" if basins == 2 else f"Vanity {L:.2f} m, {basins} basin"), x0, y0, x1, y1, "wet")
    def wc(self, room, x0, y0, x1, y1, facing="E"):
        # tank at the wall side, bowl toward 'facing'
        if facing in "EW":
            tx0, tx1 = (x0, x0+0.18) if facing == "E" else (x1-0.18, x1)
            self._rect("fixtures", tx0, y0, tx1, y1, "f-wet")
            bx = (x0+0.18, x1) if facing == "E" else (x0, x1-0.18)
            self._ellipse("fixtures", (bx[0]+bx[1])/2, (y0+y1)/2, (bx[1]-bx[0])/2, (y1-y0)/2 - 0.02, "bowl")
        else:
            ty0, ty1 = (y0, y0+0.18) if facing == "S" else (y1-0.18, y1)
            self._rect("fixtures", x0, ty0, x1, ty1, "f-wet")
            by = (y0+0.18, y1) if facing == "S" else (y0, y1-0.18)
            self._ellipse("fixtures", (x0+x1)/2, (by[0]+by[1])/2, (x1-x0)/2 - 0.02, (by[1]-by[0])/2, "bowl")
        self._text("labels", (x0+x1)/2, (y0+y1)/2, "WC", "flabel", dy=3)
        self._reg(room, "WC", x0, y0, x1, y1, "wet")
    def wardrobe(self, room, x0, y0, x1, y1, label=None):
        self._rect("fixtures", x0, y0, x1, y1, "f-ward")
        horiz = (x1-x0) >= (y1-y0)
        if horiz:
            ym = (y0+y1)/2; self._line("fixtures", x0+0.05, ym, x1-0.05, ym, "rail")
            n = int((x1-x0)/0.12)
            for i in range(1, n):
                x = x0 + (x1-x0)*i/n; self._line("fixtures", x, ym-0.12, x, ym+0.12, "hair")
        else:
            xm = (x0+x1)/2; self._line("fixtures", xm, y0+0.05, xm, y1-0.05, "rail")
            n = int((y1-y0)/0.12)
            for i in range(1, n):
                y = y0 + (y1-y0)*i/n; self._line("fixtures", xm-0.12, y, xm+0.12, y, "hair")
        L = max(x1-x0, y1-y0)
        self._autolabel(x0, y0, x1, y1, label if label is not None else f"Wardrobe {L:.1f} m")
        self._reg(room, (label if label else f"Wardrobe {L:.2f} m rail"), x0, y0, x1, y1, "ward")
    def furn(self, room, x0, y0, x1, y1, label="", kind="furn"):
        self._rect("fixtures", x0, y0, x1, y1, "f-furn")
        self._autolabel(x0, y0, x1, y1, label)
        self._reg(room, label or "Furniture", x0, y0, x1, y1, kind)
    def sofa(self, room, x0, y0, x1, y1, back="N", label="Sofa"):
        self._rect("fixtures", x0, y0, x1, y1, "f-furn", rx=3)
        b = 0.22
        if back == "N": self._rect("fixtures", x0, y0, x1, y0+b, "f-furn-dark", rx=3); self._line("fixtures", (x0+x1)/2, y0+b, (x0+x1)/2, y1, "hair")
        if back == "S": self._rect("fixtures", x0, y1-b, x1, y1, "f-furn-dark", rx=3); self._line("fixtures", (x0+x1)/2, y0, (x0+x1)/2, y1-b, "hair")
        if back == "W": self._rect("fixtures", x0, y0, x0+b, y1, "f-furn-dark", rx=3); self._line("fixtures", x0+b, (y0+y1)/2, x1, (y0+y1)/2, "hair")
        if back == "E": self._rect("fixtures", x1-b, y0, x1, y1, "f-furn-dark", rx=3); self._line("fixtures", x0, (y0+y1)/2, x1-b, (y0+y1)/2, "hair")
        self._autolabel(x0, y0, x1, y1, f"{label} {max(x1-x0,y1-y0):.1f}×{min(x1-x0,y1-y0):.1f}")
        self._reg(room, f"{label} {max(x1-x0,y1-y0):.1f} × {min(x1-x0,y1-y0):.1f}", x0, y0, x1, y1)
    def table(self, room, x0, y0, x1, y1, chairs=(2,2,0,0), label="Table"):
        # chairs: (N,S,E,W) counts
        self._rect("fixtures", x0, y0, x1, y1, "f-furn")
        c = 0.45; g = 0.08
        n,s,e,w = chairs
        for i in range(n):
            cx = x0 + (x1-x0)*(i+1)/(n+1); self._rect("fixtures", cx-c/2, y0-g-c, cx+c/2, y0-g, "f-chair", rx=3)
        for i in range(s):
            cx = x0 + (x1-x0)*(i+1)/(s+1); self._rect("fixtures", cx-c/2, y1+g, cx+c/2, y1+g+c, "f-chair", rx=3)
        for i in range(e):
            cy = y0 + (y1-y0)*(i+1)/(e+1); self._rect("fixtures", x1+g, cy-c/2, x1+g+c, cy+c/2, "f-chair", rx=3)
        for i in range(w):
            cy = y0 + (y1-y0)*(i+1)/(w+1); self._rect("fixtures", x0-g-c, cy-c/2, x0-g, cy+c/2, "f-chair", rx=3)
        self._autolabel(x0, y0, x1, y1, f"{label} {x1-x0:.1f}×{y1-y0:.1f}")
        self._reg(room, f"{label} {x1-x0:.1f} × {y1-y0:.1f}", x0-(c+g if w else 0), y0-(c+g if n else 0), x1+(c+g if e else 0), y1+(c+g if s else 0))
    def kitchen(self, room, x0, y0, x1, y1, sink=None, hob=None, label="Kitchen run"):
        self._rect("fixtures", x0, y0, x1, y1, "f-furn")
        horiz = (x1-x0) >= (y1-y0)
        if sink is not None:
            if horiz: self._rect("fixtures", sink-0.4, y0+0.1, sink+0.4, y1-0.1, "f-wet", rx=2); self._circle("fixtures", sink, (y0+y1)/2, 0.03, "drain")
        if hob is not None:
            if horiz:
                for dx,dy in ((-0.15,-0.12),(0.15,-0.12),(-0.15,0.12),(0.15,0.12)):
                    self._circle("fixtures", hob+dx, (y0+y1)/2+dy, 0.08, "hob")
        self._autolabel(x0, y0, x1, y1, f"{label} {max(x1-x0,y1-y0):.1f} m")
        self._reg(room, f"{label} {max(x1-x0,y1-y0):.2f} m", x0, y0, x1, y1)
    def appliance(self, room, x0, y0, x1, y1, label):
        self._rect("fixtures", x0, y0, x1, y1, "f-furn")
        self._circle("fixtures", (x0+x1)/2, (y0+y1)/2, min(x1-x0,y1-y0)*0.32, "f-ring")
        self._autolabel(x0, y0, x1, y1, label)
        self._reg(room, label, x0, y0, x1, y1)
    def radiator(self, room, x0, y0, x1, y1):
        self._rect("fixtures", x0, y0, x1, y1, "f-rad")
    def stairs(self, x0, y0, x1, y1, n=13, up="N"):
        self._rect("fixtures", x0, y0, x1, y1, "stairs")
        for i in range(1, n):
            y = y0 + (y1-y0)*i/n; self._line("fixtures", x0, y, x1, y, "hair")
        xm = (x0+x1)/2
        if up == "N":
            self._line("fixtures", xm, y1-0.1, xm, y0+0.1, "arrow"); self._text("labels", xm, y1-0.15, "up", "tiny")
        else:
            self._line("fixtures", xm, y0+0.1, xm, y1-0.1, "arrow"); self._text("labels", xm, y0+0.3, "up", "tiny")
        self.boxes.append(("stairs", x0, y0, x1, y1, "stairs"))
    def void(self, x0, y0, x1, y1, label="void / railing"):
        self._rect("fixtures", x0, y0, x1, y1, "void")
        self._autolabel(x0, y0, x1, y1, label, "tiny")
    def zone(self, name, x0, y0, x1, y1, label=None, kind="clear"):
        """Required movement area; drawn as a tinted dashed box. Checked against fixtures and walls."""
        self._rect("zones", x0, y0, x1, y1, "zone" if kind=="clear" else "zone-path", rx=2)
        if label: self._text("zones", x0+0.10, y0+0.18, label, "ztext", anchor="start")
        self.zones.append((name, x0, y0, x1, y1))
    def path(self, pts, label=None):
        d = " ".join(("M" if i == 0 else "L") + f" {P(x)} {P(y)}" for i,(x,y) in enumerate(pts))
        self.layers["zones"].append(f'<path d="{d}" class="walk"/>')
        L = sum(math.hypot(pts[i+1][0]-pts[i][0], pts[i+1][1]-pts[i][1]) for i in range(len(pts)-1))
        return L
    def callout(self, n, x, y):
        self._circle("labels", x, y, 0.17, "callout")
        self._text("labels", x, y, str(n), "callout-t", dy=4)
    def dim(self, kind, a, b, pos, label=None):
        label = label if label is not None else f"{abs(b-a):.2f}"
        if kind == "h":
            self._line("dims", a, pos, b, pos, "dim"); self._line("dims", a, pos-0.07, a, pos+0.07, "dim"); self._line("dims", b, pos-0.07, b, pos+0.07, "dim")
            self._text("dims", (a+b)/2, pos-0.07, label, "dimt")
        else:
            self._line("dims", pos, a, pos, b, "dim"); self._line("dims", pos-0.07, a, pos+0.07, a, "dim"); self._line("dims", pos-0.07, b, pos+0.07, b, "dim")
            self._text("dims", pos-0.08, (a+b)/2, label, "dimt", rot=-90)
    def north(self, x, y):
        self.layers["dims"].append(f'<g transform="translate({P(x)} {P(y)})"><polygon points="0,-14 5,6 0,2 -5,6" class="northp"/><text y="-18" class="dimt" text-anchor="middle">N</text></g>')
    def scalebar(self, x, y=None):
        if y is None: y = self.H + self.extra["b"] + 0.55
        for i in range(4):
            self._rect("dims", x+i*0.5, y, x+(i+1)*0.5, y+0.08, "sb-a" if i%2==0 else "sb-b")
        self._text("dims", x, y-0.06, "0", "dimt"); self._text("dims", x+1, y-0.06, "1 m", "dimt"); self._text("dims", x+2, y-0.06, "2 m", "dimt")
    # ---------------------------------------------------------------- checks
    @staticmethod
    def _ov(a, b, tol=0.02):
        return not (a[2] <= b[0]+tol or b[2] <= a[0]+tol or a[3] <= b[1]+tol or b[3] <= a[1]+tol)
    def check(self):
        """Return a list of conflicts: fixture/fixture, zone/fixture, swing/fixture, fixture/wall."""
        issues = []
        fx = [(n, (x0,y0,x1,y1), k) for (n,x0,y0,x1,y1,k) in self.boxes]
        for i in range(len(fx)):
            for j in range(i+1, len(fx)):
                if self._ov(fx[i][1], fx[j][1]): issues.append(f"fixture overlap: {fx[i][0]} / {fx[j][0]}")
        for (n,x0,y0,x1,y1) in self.zones:
            for (fn, fb, fk) in fx:
                if self._ov((x0,y0,x1,y1), fb): issues.append(f"clearance '{n}' blocked by {fn}")
            for wb in self.wall_boxes:
                if self._ov((x0,y0,x1,y1), wb): issues.append(f"clearance '{n}' hits a wall")
        for (n,x0,y0,x1,y1) in self.swings:
            for (fn, fb, fk) in fx:
                if fk == "stairs": continue
                if self._ov((x0,y0,x1,y1), fb): issues.append(f"door swing hits {fn}")
        for (fn, fb, fk) in fx:
            for wb in self.wall_boxes:
                if self._ov(fb, wb, tol=0.01): issues.append(f"{fn} overlaps a wall")
        return issues
    # ---------------------------------------------------------------- output
    def svg(self):
        ex = self.extra
        w = P(self.W + ex["l"] + ex["r"]) + PAD["l"] + PAD["r"]
        h = P(self.H + ex["t"] + ex["b"]) + PAD["t"] + PAD["b"]
        body = "\n".join("\n".join(self.layers[k]) for k in ("outside","floor","zones","fixtures","walls","windows","openings","leaves","diff","labels","dims"))
        return (f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="{self.title}" class="plan">'
                f'<g transform="translate({PAD["l"]+P(ex["l"])} {PAD["t"]+P(ex["t"])})">{body}</g></svg>')
