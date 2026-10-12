"""Floor-plan engine v3: architectural symbols, automatic geometry checks, dimension strings.
Metres in (origin: outer north-west corner), inline SVG out.
"""
import math

S = 64.0
PAD = dict(l=70, t=56, r=40, b=64)

def P(v): return round(v * S, 1)
def ov(a, b, tol=0.005):
    return not (a[2] <= b[0] + tol or b[2] <= a[0] + tol or a[3] <= b[1] + tol or b[3] <= a[1] + tol)
def inside(a, b, tol=0.02):  # a inside b
    return a[0] >= b[0]-tol and a[1] >= b[1]-tol and a[2] <= b[2]+tol and a[3] <= b[3]+tol

VDI = {  # (minimum, comfort) free depth in metres in front of the fixture
    "wc": (0.60, 0.90), "vanity": (0.55, 0.90), "shower": (0.75, 0.90), "tub": (0.75, 0.90),
    "bed_side": (0.60, 0.75), "bed_foot": (0.50, 0.90), "wardrobe": (0.70, 0.90),
}

class Plan:
    def __init__(self, W, H, title, ext=0.36, west=0.22, outside=None):
        self.W, self.H, self.title, self.ext, self.west = W, H, title, ext, west
        self.L = {k: [] for k in ("outside","floor","fix","walls","win","open","leaf","diff","lab","dim")}
        self.rooms = {}          # name -> (x0,y0,x1,y1, area)
        self.walls = []          # boxes
        self.windows = []        # (side, box)
        self.doors = []          # dict(box, room_a, room_b, kind, swing box)
        self.fx = []             # dict(room, kind, box, facing, label)
        self.outside = outside
        self.extra = dict(l=0, t=0, r=0, b=0)
        if outside:
            self.extra = dict(l=max(0, -outside["x0"]), t=max(0, -outside["y0"]), r=max(0, outside["x1"]-W), b=max(0, outside["y1"]-H))
        self.L["floor"].append(f'<rect x="0" y="0" width="{P(W)}" height="{P(H)}" class="wall"/>')
        self.walls += [(0,0,W,ext),(0,H-ext,W,H),(0,0,west,H),(W-ext,0,W,H)]
        self.notes = []
    # ------------------------------------------------------------ primitives
    def _r(self, layer, x0, y0, x1, y1, cls, rx=0, crisp=False):
        self.L[layer].append(f'<rect x="{P(x0)}" y="{P(y0)}" width="{P(x1-x0)}" height="{P(y1-y0)}" class="{cls}"' + (f' rx="{rx}"' if rx else "") + (' shape-rendering="crispEdges"' if crisp else "") + "/>")
    def _l(self, layer, x0, y0, x1, y1, cls):
        self.L[layer].append(f'<line x1="{P(x0)}" y1="{P(y0)}" x2="{P(x1)}" y2="{P(y1)}" class="{cls}"/>')
    def _c(self, layer, cx, cy, r, cls):
        self.L[layer].append(f'<circle cx="{P(cx)}" cy="{P(cy)}" r="{P(r)}" class="{cls}"/>')
    def _e(self, layer, cx, cy, rx, ry, cls):
        self.L[layer].append(f'<ellipse cx="{P(cx)}" cy="{P(cy)}" rx="{P(rx)}" ry="{P(ry)}" class="{cls}"/>')
    def _t(self, layer, x, y, s, cls, anchor="middle", rot=None, dy=0):
        if rot: self.L[layer].append(f'<text transform="translate({P(x)} {P(y)}) rotate({rot})" class="{cls}" text-anchor="{anchor}">{s}</text>')
        else: self.L[layer].append(f'<text x="{P(x)}" y="{P(y)+dy}" class="{cls}" text-anchor="{anchor}">{s}</text>')
    # ------------------------------------------------------------ building
    def room(self, name, x0, y0, x1, y1, lx=None, ly=None, area=None, sub=None):
        self._r("floor", x0, y0, x1, y1, "floor", crisp=True)
        a = area if area is not None else (x1-x0)*(y1-y0)
        self.rooms[name] = (x0, y0, x1, y1, a)
        cx = (x0+x1)/2 if lx is None else lx; cy = (y0+y1)/2 if ly is None else ly
        self._t("lab", cx, cy, name, "rname", dy=-5)
        self._t("lab", cx, cy, f"{a:.1f} m²", "rarea", dy=10)
        if sub != "": self._t("lab", cx, cy, sub if sub else f"{x1-x0:.2f} × {y1-y0:.2f}", "rsub", dy=23)
    def floor(self, x0, y0, x1, y1): self._r("floor", x0, y0, x1, y1, "floor", crisp=True)
    def wall(self, x0, y0, x1, y1, new=False):
        self._r("walls", x0, y0, x1, y1, "wall-new" if new else "wall", crisp=True); self.walls.append((x0,y0,x1,y1))
    def screen(self, x0, y0, x1, y1, h=1.2):
        self._r("walls", x0, y0, x1, y1, "wall-new", crisp=True); self.walls.append((x0,y0,x1,y1))
        if (x1-x0) < (y1-y0): self._t("lab", (x0+x1)/2 + 0.14, (y0+y1)/2, f"screen h {h}", "tiny", rot=-90)
        else: self._t("lab", (x0+x1)/2, y0 - 0.08, f"screen h {h}", "tiny")
    def removed(self, x0, y0, x1, y1): self._r("diff", x0, y0, x1, y1, "wall-gone")
    def chimney(self, x0, y0, x1, y1):
        self._r("walls", x0, y0, x1, y1, "chim"); self.walls.append((x0,y0,x1,y1))
        self.L["walls"].append(f'<line x1="{P(x0)}" y1="{P(y0)}" x2="{P(x1)}" y2="{P(y1)}" class="hair"/><line x1="{P(x1)}" y1="{P(y0)}" x2="{P(x0)}" y2="{P(y1)}" class="hair"/>')
    def set_back(self, label):
        o = self.outside
        self._r("outside", o["x0"], o["y0"], o["x1"], o["y1"], "outline")
        for (x0,y0,x1,y1) in [(o["x0"], o["y0"], o["x1"], 0), (self.W, 0, o["x1"], self.H), (o["x0"], self.H, o["x1"], o["y1"])]:
            if x1 > x0 and y1 > y0: self._r("outside", x0, y0, x1, y1, "terrace")
        self._t("dim", (o["x0"]+o["x1"])/2, o["y1"]+0.26, label, "note")
    def infill(self, side, a, b, note="window infilled (facade change, permit)"):
        t = self.ext
        box = {"N": (a, 0, b, t), "S": (a, self.H-t, b, self.H), "E": (self.W-t, a, self.W, b), "W": (0, a, self.west, b)}[side]
        self._r("win", *box, "wall-new", crisp=True)
        if side == "S": self._t("dim", (a+b)/2, self.H + self.extra["b"]*0.45 + 0.24, note, "note")
        if side == "N": self._t("dim", (a+b)/2, -0.14, note, "note")
    def window(self, side, a, b, note=None, new=False):
        t = self.ext
        box = {"N": (a, 0, b, t), "S": (a, self.H-t, b, self.H), "E": (self.W-t, a, self.W, b), "W": (0, a, self.west, b)}[side]
        x0, y0, x1, y1 = box
        self._r("win", x0, y0, x1, y1, "win-new" if new else "win", crisp=True)
        if side in "NS":
            for f in (0.3, 0.5, 0.7):
                ym = y0 + (y1-y0)*f; self._l("win", x0, ym, x1, ym, "winl" if f == 0.5 else "winf")
        else:
            for f in (0.3, 0.5, 0.7):
                xm = x0 + (x1-x0)*f; self._l("win", xm, y0, xm, y1, "winl" if f == 0.5 else "winf")
        self.windows.append((side, box))
        if note:
            cx, cy = (x0+x1)/2, (y0+y1)/2
            if side == "N": self._t("dim", cx, -0.14, note, "note")
            elif side == "S": self._t("dim", cx, self.H+0.24, note, "note")
            elif side == "E": self._t("dim", self.W+0.22, cy, note, "note", rot=-90)
            else: self._t("dim", -0.22, cy, note, "note", rot=-90)
    def door(self, x0, y0, x1, y1, hinge, swing, kind="swing", new=False, rooms=()):
        """Opening box inside a wall. hinge = end of the opening carrying the hinge (N/S/E/W); swing = side the leaf opens to.
        kind: swing | pocket (slides into the wall toward 'hinge' end) | open."""
        self._r("open", x0, y0, x1, y1, "open", crisp=True)
        horiz = (x1-x0) > (y1-y0)
        Lw = (x1-x0) if horiz else (y1-y0)
        d = dict(box=(x0,y0,x1,y1), kind=kind, rooms=rooms, swing=None, pocket=None)
        cls = "leaf-new" if new else "leaf"
        if kind == "open":
            self.doors.append(d); return
        if kind == "pocket":
            # leaf shown half open: thin rect covering half the opening, pocket cavity dashed inside the wall beyond the hinge end
            ay = 0.24
            if horiz:
                ym = (y0+y1)/2; yy = ym + (ay if swing == "S" else -ay)
                if hinge == "W":   # slides west into the wall left of the opening
                    self._r("leaf", x0 - Lw, y0+0.015, x0, y1-0.015, "pocket")
                    self._r("leaf", x0 - Lw*0.5, ym-0.025, x0 + Lw*0.5, ym+0.025, cls)
                    self.L["leaf"].append(f'<line x1="{P(x1-0.05)}" y1="{P(yy)}" x2="{P(x0+0.15)}" y2="{P(yy)}" class="arrow"/>')
                    d["pocket"] = (x0-Lw, y0, x0, y1)
                else:
                    self._r("leaf", x1, y0+0.015, x1 + Lw, y1-0.015, "pocket")
                    self._r("leaf", x1 - Lw*0.5, ym-0.025, x1 + Lw*0.5, ym+0.025, cls)
                    self.L["leaf"].append(f'<line x1="{P(x0+0.05)}" y1="{P(yy)}" x2="{P(x1-0.15)}" y2="{P(yy)}" class="arrow"/>')
                    d["pocket"] = (x1, y0, x1+Lw, y1)
            else:
                xm = (x0+x1)/2; xx = xm + (ay if swing == "E" else -ay)
                if hinge == "N":
                    self._r("leaf", x0+0.015, y0 - Lw, x1-0.015, y0, "pocket")
                    self._r("leaf", xm-0.025, y0 - Lw*0.5, xm+0.025, y0 + Lw*0.5, cls)
                    self.L["leaf"].append(f'<line x1="{P(xx)}" y1="{P(y1-0.05)}" x2="{P(xx)}" y2="{P(y0+0.15)}" class="arrow"/>')
                    d["pocket"] = (x0, y0-Lw, x1, y0)
                else:
                    self._r("leaf", x0+0.015, y1, x1-0.015, y1 + Lw, "pocket")
                    self._r("leaf", xm-0.025, y1 - Lw*0.5, xm+0.025, y1 + Lw*0.5, cls)
                    self.L["leaf"].append(f'<line x1="{P(xx)}" y1="{P(y0+0.05)}" x2="{P(xx)}" y2="{P(y1-0.15)}" class="arrow"/>')
                    d["pocket"] = (x0, y1, x1, y1+Lw)
            self.doors.append(d); return
        # swing door: leaf as thin rect at 90°, quarter arc
        if horiz:
            hy = (y0+y1)/2; hx = x0 if hinge == "W" else x1; ex = x1 if hinge == "W" else x0
            ty = hy + (Lw if swing == "S" else -Lw)
            lx0, lx1 = (hx, hx+0.045) if hinge == "W" else (hx-0.045, hx)
            self._r("leaf", lx0, min(hy, ty), lx1, max(hy, ty), cls)
            start, tip = (ex, hy), (hx + (0.025 if hinge=="W" else -0.025), ty)
            box = (min(x0,x1), min(hy,ty), max(x0,x1), max(hy,ty))
        else:
            hx = (x0+x1)/2; hy = y0 if hinge == "N" else y1; ey = y1 if hinge == "N" else y0
            tx = hx + (Lw if swing == "E" else -Lw)
            ly0, ly1 = (hy, hy+0.045) if hinge == "N" else (hy-0.045, hy)
            self._r("leaf", min(hx, tx), ly0, max(hx, tx), ly1, cls)
            start, tip = (hx, ey), (tx, hy + (0.025 if hinge=="N" else -0.025))
            box = (min(hx,tx), min(y0,y1), max(hx,tx), max(y0,y1))
        r = P(Lw)
        a0 = math.atan2(start[1]-hy, start[0]-hx); a1 = math.atan2(tip[1]-hy, tip[0]-hx)
        dd = (a1 - a0) % (2*math.pi); sweep = 1 if dd < math.pi else 0
        self.L["leaf"].append(f'<path d="M {P(start[0])} {P(start[1])} A {r} {r} 0 0 {sweep} {P(tip[0])} {P(tip[1])}" class="arc"/>')
        d["swing"] = box; self.doors.append(d)
    # ------------------------------------------------------------ fixtures
    def _reg(self, room, kind, box, facing=None, label=None, tall=False):
        self.fx.append(dict(room=room, kind=kind, box=box, facing=facing, label=label or kind, tall=tall))
    def _lab(self, x0, y0, x1, y1, s, cls="flabel"):
        if not s: return
        if (y1-y0) > (x1-x0) and (x1-x0) < 0.9: self._t("lab", (x0+x1)/2 + 0.05, (y0+y1)/2, s, cls, rot=-90)
        else: self._t("lab", (x0+x1)/2, (y0+y1)/2, s, cls, dy=3)
    def bed(self, room, x0, y0, x1, y1, head, label=None):
        self._r("fix", x0, y0, x1, y1, "f-bed")
        w, h = x1-x0, y1-y0
        if head == "W":
            self._r("fix", x0, y0, x0+0.07, y1, "f-head")
            for a,b in ((y0+0.1, (y0+y1)/2-0.04), ((y0+y1)/2+0.04, y1-0.1)): self._r("fix", x0+0.14, a, x0+0.58, b, "pillow", rx=3)
            self._l("fix", x0+0.9, y0+0.04, x0+0.9, y1-0.04, "thin")
        elif head == "E":
            self._r("fix", x1-0.07, y0, x1, y1, "f-head")
            for a,b in ((y0+0.1, (y0+y1)/2-0.04), ((y0+y1)/2+0.04, y1-0.1)): self._r("fix", x1-0.58, a, x1-0.14, b, "pillow", rx=3)
            self._l("fix", x1-0.9, y0+0.04, x1-0.9, y1-0.04, "thin")
        elif head == "N":
            self._r("fix", x0, y0, x1, y0+0.07, "f-head")
            for a,b in ((x0+0.1, (x0+x1)/2-0.04), ((x0+x1)/2+0.04, x1-0.1)): self._r("fix", a, y0+0.14, b, y0+0.58, "pillow", rx=3)
            self._l("fix", x0+0.04, y0+0.9, x1-0.04, y0+0.9, "thin")
        else:
            self._r("fix", x0, y1-0.07, x1, y1, "f-head")
            for a,b in ((x0+0.1, (x0+x1)/2-0.04), ((x0+x1)/2+0.04, x1-0.1)): self._r("fix", a, y1-0.58, b, y1-0.14, "pillow", rx=3)
            self._l("fix", x0+0.04, y1-0.9, x1-0.04, y1-0.9, "thin")
        lab = label if label is not None else (f"Bed {w:.1f} × {h:.1f}" if head in "NS" else f"Bed {h:.1f} × {w:.1f}")
        off = dict(W=(0.3,0), E=(-0.3,0), N=(0,0.3), S=(0,-0.3))[head]
        self._t("lab", (x0+x1)/2+off[0], (y0+y1)/2+off[1], lab, "flabel", dy=3)
        self._reg(room, "bed", (x0,y0,x1,y1), facing=head, label=lab)
    def nightstand(self, room, x0, y0, x1, y1):
        self._r("fix", x0, y0, x1, y1, "f-furn"); self._c("fix", (x0+x1)/2, (y0+y1)/2, 0.09, "lamp")
        self._reg(room, "nightstand", (x0,y0,x1,y1), label="Night table")
    def tub(self, room, x0, y0, x1, y1, label="Tub"):
        self._r("fix", x0, y0, x1, y1, "f-wet", rx=4)
        self._r("fix", x0+0.08, y0+0.08, x1-0.08, y1-0.08, "f-wet-in", rx=9)
        horiz = (x1-x0) >= (y1-y0)
        if horiz: self._c("fix", x1-0.24, (y0+y1)/2, 0.04, "drain"); self._l("fix", x1-0.12, (y0+y1)/2-0.08, x1-0.12, (y0+y1)/2+0.08, "thin")
        else: self._c("fix", (x0+x1)/2, y0+0.24, 0.04, "drain"); self._l("fix", (x0+x1)/2-0.08, y0+0.12, (x0+x1)/2+0.08, y0+0.12, "thin")
        self._lab(x0, y0, x1, y1, f"{label} {max(x1-x0,y1-y0):.2f} × {min(x1-x0,y1-y0):.2f}")
        self._reg(room, "tub", (x0,y0,x1,y1), label=f"Tub {max(x1-x0,y1-y0):.2f} × {min(x1-x0,y1-y0):.2f}")
    def shower(self, room, x0, y0, x1, y1, glass=(), entry="S", label="Walk-in shower"):
        self._r("fix", x0, y0, x1, y1, "f-wet")
        self._c("fix", x0+0.22, y0+0.22, 0.05, "drain")
        for g in glass:
            if isinstance(g, tuple):
                side, a, b = g
                if side == "E": self._l("fix", x1, a, x1, b, "glass")
                if side == "W": self._l("fix", x0, a, x0, b, "glass")
                if side == "N": self._l("fix", a, y0, b, y0, "glass")
                if side == "S": self._l("fix", a, y1, b, y1, "glass")
            else:
                if g == "N": self._l("fix", x0, y0, x1, y0, "glass")
                if g == "S": self._l("fix", x0, y1, x1, y1, "glass")
                if g == "E": self._l("fix", x1, y0, x1, y1, "glass")
                if g == "W": self._l("fix", x0, y0, x0, y1, "glass")
        self._lab(x0, y0, x1, y1, "Shower")
        self._reg(room, "shower", (x0,y0,x1,y1), facing=entry, label=f"{label} {max(x1-x0,y1-y0):.2f} × {min(x1-x0,y1-y0):.2f}")
    def vanity(self, room, x0, y0, x1, y1, basins=2, wall="N", label=None):
        self._r("fix", x0, y0, x1, y1, "f-furn")
        horiz = (x1-x0) >= (y1-y0); Lw = (x1-x0) if horiz else (y1-y0)
        for i in range(basins):
            f = (0.27, 0.73)[i] if basins == 2 else (i+1)/(basins+1)
            if horiz:
                cx = x0 + Lw*f; cy = (y0+y1)/2
                self._r("fix", cx-0.23, cy-0.17, cx+0.23, cy+0.17, "basin", rx=7)
                self._c("fix", cx, y0+0.09 if wall=="N" else y1-0.09, 0.03, "drain")
            else:
                cy = y0 + Lw*f; cx = (x0+x1)/2
                self._r("fix", cx-0.17, cy-0.23, cx+0.17, cy+0.23, "basin", rx=7)
                self._c("fix", x0+0.09 if wall=="W" else x1-0.09, cy, 0.03, "drain")
        # mirror on the wall side
        if wall == "N": self._l("fix", x0+0.05, y0+0.02, x1-0.05, y0+0.02, "mirror")
        if wall == "S": self._l("fix", x0+0.05, y1-0.02, x1-0.05, y1-0.02, "mirror")
        if wall == "W": self._l("fix", x0+0.02, y0+0.05, x0+0.02, y1-0.05, "mirror")
        if wall == "E": self._l("fix", x1-0.02, y0+0.05, x1-0.02, y1-0.05, "mirror")
        name = (label if label is not None else (f"Double vanity {Lw:.2f}" if basins == 2 else f"Vanity {Lw:.2f}"))
        if name:
            if horiz: self._t("lab", (x0+x1)/2, y1+0.17 if wall=="N" else y0-0.08, name, "flabel")
            else: self._t("lab", x1+0.1 if wall=="W" else x0-0.1, (y0+y1)/2, name, "flabel", rot=-90)
        name = name or (f"Double vanity {Lw:.2f}" if basins == 2 else f"Vanity {Lw:.2f}")
        self._reg(room, "vanity", (x0,y0,x1,y1), facing={"N":"S","S":"N","W":"E","E":"W"}[wall], label=name)
    def wc(self, room, cx, wall_y_or_x, facing, room_box=None):
        """Standard WC: 0.38 wide, 0.66 long incl. cistern. facing = direction the user faces (away from the wall)."""
        w, l, c = 0.38, 0.66, 0.18
        if facing == "S":   x0,y0,x1,y1 = cx-w/2, wall_y_or_x, cx+w/2, wall_y_or_x+l; self._r("fix", x0, y0, x1, y0+c, "f-wet"); self._e("fix", cx, y0+c+(l-c)/2, w/2-0.02, (l-c)/2-0.01, "bowl")
        elif facing == "N": x0,y0,x1,y1 = cx-w/2, wall_y_or_x-l, cx+w/2, wall_y_or_x; self._r("fix", x0, y1-c, x1, y1, "f-wet"); self._e("fix", cx, y0+(l-c)/2, w/2-0.02, (l-c)/2-0.01, "bowl")
        elif facing == "E": x0,y0,x1,y1 = wall_y_or_x, cx-w/2, wall_y_or_x+l, cx+w/2; self._r("fix", x0, y0, x0+c, y1, "f-wet"); self._e("fix", x0+c+(l-c)/2, cx, (l-c)/2-0.01, w/2-0.02, "bowl")
        else:               x0,y0,x1,y1 = wall_y_or_x-l, cx-w/2, wall_y_or_x, cx+w/2; self._r("fix", x1-c, y0, x1, y1, "f-wet"); self._e("fix", x0+(l-c)/2, cx, (l-c)/2-0.01, w/2-0.02, "bowl")
        self._t("lab", (x0+x1)/2, (y0+y1)/2, "WC", "flabel", dy=3)
        self._reg(room, "wc", (x0,y0,x1,y1), facing=facing, label="WC")
    def wardrobe(self, room, x0, y0, x1, y1, label=None):
        self._r("fix", x0, y0, x1, y1, "f-ward")
        horiz = (x1-x0) >= (y1-y0)
        if horiz:
            ym = (y0+y1)/2; self._l("fix", x0+0.05, ym, x1-0.05, ym, "rail")
            n = int((x1-x0)/0.25)
            for i in range(1, n): x = x0 + (x1-x0)*i/n; self._l("fix", x, ym-0.1, x, ym+0.1, "hair")
        else:
            xm = (x0+x1)/2; self._l("fix", xm, y0+0.05, xm, y1-0.05, "rail")
            n = int((y1-y0)/0.25)
            for i in range(1, n): y = y0 + (y1-y0)*i/n; self._l("fix", xm-0.1, y, xm+0.1, y, "hair")
        Lw = max(x1-x0, y1-y0)
        lab = label if label is not None else f"Wardrobe {Lw:.1f} m"
        if lab:
            if horiz: self._t("lab", (x0+x1)/2, (y0+y1)/2 + 0.2, lab, "flabel")
            else: self._t("lab", (x0+x1)/2 + 0.2, (y0+y1)/2, lab, "flabel", rot=-90)
        self._reg(room, "wardrobe", (x0,y0,x1,y1), facing=None, label=label or f"Wardrobe {Lw:.2f} m rail", tall=True)
    def furn(self, room, x0, y0, x1, y1, label="", kind="furniture", tall=False):
        self._r("fix", x0, y0, x1, y1, "f-furn")
        self._lab(x0, y0, x1, y1, label)
        self._reg(room, kind, (x0,y0,x1,y1), label=label or kind, tall=tall)
    def chair(self, room, cx, cy, r=0.23):
        self._r("fix", cx-r, cy-r, cx+r, cy+r, "f-chair", rx=4)
        self._reg(room, "chair", (cx-r,cy-r,cx+r,cy+r), label="Chair")
    def sofa(self, room, x0, y0, x1, y1, back="N", label="Sofa"):
        self._r("fix", x0, y0, x1, y1, "f-furn", rx=4)
        b = 0.22
        if back == "N": self._r("fix", x0, y0, x1, y0+b, "f-furn-dark", rx=4); self._r("fix", x0, y0, x0+0.14, y1, "f-furn-dark", rx=3); self._r("fix", x1-0.14, y0, x1, y1, "f-furn-dark", rx=3)
        if back == "S": self._r("fix", x0, y1-b, x1, y1, "f-furn-dark", rx=4); self._r("fix", x0, y0, x0+0.14, y1, "f-furn-dark", rx=3); self._r("fix", x1-0.14, y0, x1, y1, "f-furn-dark", rx=3)
        if back == "W": self._r("fix", x0, y0, x0+b, y1, "f-furn-dark", rx=4); self._r("fix", x0, y0, x1, y0+0.14, "f-furn-dark", rx=3); self._r("fix", x0, y1-0.14, x1, y1, "f-furn-dark", rx=3)
        if back == "E": self._r("fix", x1-b, y0, x1, y1, "f-furn-dark", rx=4); self._r("fix", x0, y0, x1, y0+0.14, "f-furn-dark", rx=3); self._r("fix", x0, y1-0.14, x1, y1, "f-furn-dark", rx=3)
        self._lab(x0, y0, x1, y1, f"{label} {max(x1-x0,y1-y0):.1f} × {min(x1-x0,y1-y0):.1f}")
        self._reg(room, "sofa", (x0,y0,x1,y1), label=f"{label} {max(x1-x0,y1-y0):.1f} × {min(x1-x0,y1-y0):.1f}")
    def table(self, room, x0, y0, x1, y1, chairs=(2,2,0,0), label="Table"):
        self._r("fix", x0, y0, x1, y1, "f-furn")
        c = 0.45; g = 0.08; n_,s,e,w = chairs
        for i in range(n_): cx = x0 + (x1-x0)*(i+1)/(n_+1); self._r("fix", cx-c/2, y0-g-c, cx+c/2, y0-g, "f-chair", rx=4)
        for i in range(s): cx = x0 + (x1-x0)*(i+1)/(s+1); self._r("fix", cx-c/2, y1+g, cx+c/2, y1+g+c, "f-chair", rx=4)
        for i in range(e): cy = y0 + (y1-y0)*(i+1)/(e+1); self._r("fix", x1+g, cy-c/2, x1+g+c, cy+c/2, "f-chair", rx=4)
        for i in range(w): cy = y0 + (y1-y0)*(i+1)/(w+1); self._r("fix", x0-g-c, cy-c/2, x0-g, cy+c/2, "f-chair", rx=4)
        self._lab(x0, y0, x1, y1, f"{label} {x1-x0:.1f} × {y1-y0:.1f}")
        self._reg(room, "table", (x0-(c+g if w else 0), y0-(c+g if n_ else 0), x1+(c+g if e else 0), y1+(c+g if s else 0)), label=f"{label} {x1-x0:.1f} × {y1-y0:.1f} with chairs")
    def kitchen(self, room, x0, y0, x1, y1, sink=None, hob=None, label="Kitchen run"):
        self._r("fix", x0, y0, x1, y1, "f-furn")
        if sink is not None:
            self._r("fix", sink-0.4, y0+0.1, sink+0.4, y1-0.1, "basin", rx=3); self._c("fix", sink, (y0+y1)/2, 0.03, "drain")
        if hob is not None:
            for dx,dy in ((-0.15,-0.13),(0.15,-0.13),(-0.15,0.13),(0.15,0.13)): self._c("fix", hob+dx, (y0+y1)/2+dy, 0.08, "hob")
        self._lab(x0, y0, x1, y1, f"{label} {max(x1-x0,y1-y0):.1f} m")
        self._reg(room, "kitchen", (x0,y0,x1,y1), label=f"{label} {max(x1-x0,y1-y0):.2f} m", tall=False)
    def appliance(self, room, x0, y0, x1, y1, label):
        self._r("fix", x0, y0, x1, y1, "f-furn"); self._c("fix", (x0+x1)/2, (y0+y1)/2, min(x1-x0,y1-y0)*0.3, "f-ring")
        self._lab(x0, y0, x1, y1, label); self._reg(room, "appliance", (x0,y0,x1,y1), label=label, tall=True)
    def radiator(self, room, x0, y0, x1, y1):
        self._r("fix", x0, y0, x1, y1, "f-rad")
    def stairs(self, x0, y0, x1, y1, n=13, up="S", label="existing stair, as drawn"):
        self._r("fix", x0, y0, x1, y1, "stairs")
        if up in ("S", "N"):
            for i in range(1, n): y = y0 + (y1-y0)*i/n; self._l("fix", x0, y, x1, y, "hair")
            xm = (x0+x1)/2
            if up == "S": self._l("fix", xm, y0+0.12, xm, y1-0.12, "arrow"); self._t("lab", xm, y0+0.32, "up", "tiny")
            else: self._l("fix", xm, y1-0.12, xm, y0+0.12, "arrow"); self._t("lab", xm, y1-0.2, "up", "tiny")
            self._t("lab", xm, (y0+y1)/2 + 0.05, label, "tiny", rot=-90)
        else:
            for i in range(1, n): x = x0 + (x1-x0)*i/n; self._l("fix", x, y0, x, y1, "hair")
            ym = (y0+y1)/2
            if up == "E": self._l("fix", x0+0.12, ym, x1-0.12, ym, "arrow"); self._t("lab", x0+0.3, ym-0.12, "up", "tiny")
            else: self._l("fix", x1-0.12, ym, x0+0.12, ym, "arrow"); self._t("lab", x1-0.3, ym-0.12, "up", "tiny")
            self._t("lab", (x0+x1)/2, y1+0.2, label, "tiny")
        self.fx.append(dict(room="stairs", kind="stairs", box=(x0,y0,x1,y1), facing=None, label="stairs", tall=False))
    def void(self, x0, y0, x1, y1, label="void"):
        self._r("fix", x0, y0, x1, y1, "void"); self._lab(x0, y0, x1, y1, label, "tiny")
    def callout(self, n, x, y):
        self._c("lab", x, y, 0.18, "callout"); self._t("lab", x, y, str(n), "callout-t", dy=4)
    def dimstring(self, kind, breaks, pos, labels=None):
        """kind h: breaks are x positions, string drawn at y=pos; kind v: y positions at x=pos."""
        for i in range(len(breaks)-1):
            a, b = breaks[i], breaks[i+1]
            lab = labels[i] if labels and labels[i] is not None else f"{b-a:.2f}"
            if kind == "h":
                self._l("dim", a, pos, b, pos, "dim"); self._l("dim", a, pos-0.08, a, pos+0.08, "dim"); self._l("dim", b, pos-0.08, b, pos+0.08, "dim")
                if lab: self._t("dim", (a+b)/2, pos-0.06, lab, "dimt")
            else:
                self._l("dim", pos, a, pos, b, "dim"); self._l("dim", pos-0.08, a, pos+0.08, a, "dim"); self._l("dim", pos-0.08, b, pos+0.08, b, "dim")
                if lab: self._t("dim", pos-0.07, (a+b)/2, lab, "dimt", rot=-90)
    def north(self, x, y):
        self.L["dim"].append(f'<g transform="translate({P(x)} {P(y)})"><polygon points="0,-15 5,6 0,2 -5,6" class="northp"/><text y="-19" class="dimt" text-anchor="middle">N</text></g>')
    def scalebar(self, x, y=None):
        if y is None: y = self.H + self.extra["b"] + 0.62
        for i in range(4): self._r("dim", x+i*0.5, y, x+(i+1)*0.5, y+0.09, "sb-a" if i%2==0 else "sb-b")
        self._t("dim", x, y-0.07, "0", "dimt"); self._t("dim", x+1, y-0.07, "1 m", "dimt"); self._t("dim", x+2, y-0.07, "2 m", "dimt")
    # ------------------------------------------------------------ checks
    def _free_depth(self, box, facing, width_box=None, limit=3.0, ignore=()):
        """Free distance in front of a box in direction 'facing' until a wall or fixture (ignoring soft overlaps)."""
        x0,y0,x1,y1 = box
        obstacles = [w for w in self.walls] + [f["box"] for f in self.fx if f["box"] != box and f["kind"] not in ("stairs",) + tuple(ignore)]
        best = limit
        for (ox0,oy0,ox1,oy1) in obstacles:
            if facing == "S":
                if ox1 > x0+0.01 and ox0 < x1-0.01 and oy0 >= y1-0.01: best = min(best, oy0 - y1)
            elif facing == "N":
                if ox1 > x0+0.01 and ox0 < x1-0.01 and oy1 <= y0+0.01: best = min(best, y0 - oy1)
            elif facing == "E":
                if oy1 > y0+0.01 and oy0 < y1-0.01 and ox0 >= x1-0.01: best = min(best, ox0 - x1)
            elif facing == "W":
                if oy1 > y0+0.01 and oy0 < y1-0.01 and ox1 <= x0+0.01: best = min(best, x0 - ox1)
        return max(best, 0.0)
    def check(self):
        issues, clear = [], []
        # 1 walls vs windows
        for (side, wb) in self.windows:
            for w in self.walls[4:]:
                if ov(w, wb, tol=0.0): issues.append(f"wall {w} meets window on {side} wall {wb}")
                # pier check: wall touching exterior band within 0.12 m of a window edge
                if side in "NS" and (ov(w, (wb[0]-0.12, wb[1], wb[2]+0.12, wb[3]), tol=0.0)): issues.append(f"wall {w} lands within 0.12 m of window edge ({side} {wb[0]:.2f}–{wb[2]:.2f})")
                if side in "EW" and (ov(w, (wb[0], wb[1]-0.12, wb[2], wb[3]+0.12), tol=0.0)): issues.append(f"wall {w} lands within 0.12 m of window edge ({side} {wb[1]:.2f}–{wb[3]:.2f})")
        # 2 rooms need a door
        for name, (x0,y0,x1,y1,a) in self.rooms.items():
            if name.lower().startswith(("hall","landing","entrance","suite foyer","living","corridor")): continue
            touch = False
            for d in self.doors:
                b = d["box"]; exp = (x0-0.15, y0-0.15, x1+0.15, y1+0.15)
                if ov(b, exp, tol=0.0) and not inside(b, (x0+0.05,y0+0.05,x1-0.05,y1-0.05)): touch = True
            if not touch: issues.append(f"room '{name}' has no door on its boundary")
        # 3 doors inside walls
        for d in self.doors:
            b = d["box"]
            if not any(inside(b, w, tol=0.02) for w in self.walls): issues.append(f"door {b} is not inside a wall")
        # 4 fixtures inside rooms; tall fixtures in front of windows; overlaps
        for f in self.fx:
            if f["kind"] == "stairs": continue
            r = self.rooms.get(f["room"])
            if r and not inside(f["box"], r[:4], tol=0.03): issues.append(f"{f['label']} sticks out of room '{f['room']}'")
            if f["tall"]:
                for (side, wb) in self.windows:
                    probe = {"N": (wb[0], wb[3], wb[2], wb[3]+0.05), "S": (wb[0], wb[1]-0.05, wb[2], wb[1]), "E": (wb[0]-0.05, wb[1], wb[0], wb[3]), "W": (wb[2], wb[1], wb[2]+0.05, wb[3])}[side]
                    if ov(f["box"], probe, tol=0.0): issues.append(f"{f['label']} stands in front of the {side} window")
        boxes = [f for f in self.fx if f["kind"] != "stairs"]
        for i in range(len(boxes)):
            for j in range(i+1, len(boxes)):
                if ov(boxes[i]["box"], boxes[j]["box"]): issues.append(f"overlap: {boxes[i]['label']} / {boxes[j]['label']}")
        for f in boxes:
            for w in self.walls:
                if ov(f["box"], w, tol=0.01): issues.append(f"{f['label']} overlaps a wall")
        # 5 door swings vs fixtures; pocket cavities free
        for d in self.doors:
            if d["swing"]:
                for f in boxes:
                    if ov(d["swing"], f["box"]): issues.append(f"door swing at {d['box']} hits {f['label']}")
            if d["pocket"]:
                if not any(inside(d["pocket"], w, tol=0.03) for w in self.walls): issues.append(f"pocket cavity {d['pocket']} not inside a wall")
                for o in self.doors:
                    if o is not d and ov(d["pocket"], o["box"]): issues.append(f"pocket cavity {d['pocket']} collides with another opening")
        # 6 clearances (VDI 6000) by ray-cast
        for f in self.fx:
            k = f["kind"]
            if k in ("wc","vanity","shower","tub") and f["facing"]:
                if k in ("tub", "vanity"):
                    # VDI: 0.90 m wide zone somewhere along the fixture, not over its full length
                    x0,y0,x1,y1 = f["box"]; best = 0.0
                    if f["facing"] in "NS":
                        s = x0
                        while s + 0.9 <= x1 + 0.001:
                            best = max(best, self._free_depth((s, y0, s+0.9, y1), f["facing"])); s += 0.05
                    else:
                        s = y0
                        while s + 0.9 <= y1 + 0.001:
                            best = max(best, self._free_depth((x0, s, x1, s+0.9), f["facing"])); s += 0.05
                    dep = best if best else self._free_depth(f["box"], f["facing"])
                else:
                    dep = self._free_depth(f["box"], f["facing"])
                mn, cf = VDI[k]
                clear.append((f["room"], f["label"], f["facing"], dep, mn, cf))
                if dep + 0.005 < mn: issues.append(f"{f['label']} in {f['room']}: only {dep:.2f} m free in front (VDI min {mn:.2f})")
            if k == "bed":
                x0,y0,x1,y1 = f["box"]; head = f["facing"]
                sides = {"W": ("N","S","E"), "E": ("N","S","W"), "N": ("W","E","S"), "S": ("W","E","N")}[head]
                for s_ in sides:
                    sub = {"N": (x0+0.55 if head=="W" else x0, y0, x1-0.55 if head=="E" else x1, y1), "S": (x0+0.55 if head=="W" else x0, y0, x1-0.55 if head=="E" else x1, y1),
                           "W": (x0, y0+0.55 if head=="N" else y0, x1, y1-0.55 if head=="S" else y1), "E": (x0, y0+0.55 if head=="N" else y0, x1, y1-0.55 if head=="S" else y1)}[s_]
                    foot = (s_ == {"W":"E","E":"W","N":"S","S":"N"}[head])
                    dep = self._free_depth(sub, s_, ignore=("bench",) if foot else ())
                    if foot:
                        for g in self.fx:
                            if g["kind"] == "bench":
                                gb = g["box"]
                                if ov((sub[0], sub[1], sub[2], sub[3]), (gb[0]-3 if s_=="W" else gb[0], gb[1]-3 if s_=="N" else gb[1], gb[2]+3 if s_=="E" else gb[2], gb[3]+3 if s_=="S" else gb[3]), tol=0.0):
                                    dep -= (gb[2]-gb[0]) if s_ in "EW" else (gb[3]-gb[1])
                    mn, cf = VDI["bed_foot"] if foot else VDI["bed_side"]
                    clear.append((f["room"], f["label"], ("foot " if foot else "side ") + s_, dep, mn, cf))
                    if dep + 0.005 < mn: issues.append(f"{f['label']} in {f['room']}: {dep:.2f} m on the {s_} side (min {mn:.2f})")
        self.clearances = clear
        return issues
    # ------------------------------------------------------------ output
    def svg(self):
        ex = self.extra
        w = P(self.W + ex["l"] + ex["r"]) + PAD["l"] + PAD["r"]; h = P(self.H + ex["t"] + ex["b"]) + PAD["t"] + PAD["b"]
        body = "\n".join("\n".join(self.L[k]) for k in ("outside","floor","diff","fix","walls","win","open","leaf","lab","dim"))
        return (f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="{self.title}" class="plan"><g transform="translate({PAD["l"]+P(ex["l"])} {PAD["t"]+P(ex["t"])})">{body}</g></svg>')
