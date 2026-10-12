"""Compact geometry dump of one plan: python3 dump_plan.py t4_eg   (all coordinates in metres from the outer north-west corner)"""
import sys, importlib, os
key = sys.argv[1]
mod = {"t1": "floors2", "t2": "floors2", "t3": "floors3", "t4": "floors4"}.get(key[:2], "floors")
m = importlib.import_module(mod); p = m.ALL[key](); issues = p.check()
print(f"PLAN {key}: plate {p.W} x {p.H} outside; interior x 0.22..{p.W-0.36:.2f}, y 0.36..{p.H-0.36:.2f}; geometry-check issues: {len(issues)} {issues}")
print("ROOMS (x0 y0 x1 y1 area):")
for n, (x0,y0,x1,y1,a) in p.rooms.items(): print(f"  {n}: {x0:.2f} {y0:.2f} {x1:.2f} {y1:.2f}  {a:.1f} m2")
print("WALLS (internal, x0 y0 x1 y1):")
for w in p.walls[4:]: print(f"  {w[0]:.2f} {w[1]:.2f} {w[2]:.2f} {w[3]:.2f}")
print("WINDOWS (side, box):")
for s, b in p.windows: print(f"  {s}: {b[0]:.2f} {b[1]:.2f} {b[2]:.2f} {b[3]:.2f}")
print("DOORS (opening box, kind, swing box):")
for d in p.doors: print(f"  {tuple(round(v,2) for v in d['box'])} {d['kind']} swing={tuple(round(v,2) for v in d['swing']) if d['swing'] else None}")
print("FIXTURES (room | kind | label | box | facing):")
for f in p.fx: print(f"  {f['room']} | {f['kind']} | {f['label']} | {tuple(round(v,2) for v in f['box'])} | {f['facing']}")
print("CLEARANCES (room, fixture, free side, free depth m, VDI min/comfort):")
for c in p.clearances: print(f"  {c[0]} | {c[1]} | {c[2]} | {c[3]:.2f} | {c[4]:.2f}/{c[5]:.2f}")
