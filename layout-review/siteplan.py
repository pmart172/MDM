"""Site plan for Altkönigstraße 122: plot polygon from the briefing's approximate corner coordinates (site frame: s east from
the west boundary, t south from the street boundary), Baufenster t = 5 to 20 m, 3 m side setbacks, the mirrored T4 pair with the
boundary garages, and the Abstandsfläche check at the east rear corner."""
import math
S = 12.0  # px per metre
PLOT = [(0.0, 0.0), (30.3, 0.0), (28.5, 6.2), (26.8, 12.4), (21.0, 35.0), (0.0, 33.9)]
HOUSE_W, HOUSE_D, T0, PARTY = 8.29, 14.07, 5.0, 13.70
WEST_GAR_W, GAR_D = 5.41, 7.42

def east_boundary_s(t):
    """s of the east boundary at depth t (piecewise linear)."""
    pts = [(0.0, 30.3), (6.2, 28.5), (12.4, 26.8), (35.0, 21.0)]
    for (t0, s0), (t1, s1) in zip(pts, pts[1:]):
        if t0 <= t <= t1: return s0 + (s1 - s0) * (t - t0) / (t1 - t0)
    return pts[-1][1]

def P(s, t): return f"{s*S+40:.1f},{t*S+30:.1f}"

def svg(offset=0.0, depth=HOUSE_D):
    parts = []
    plot = " ".join(P(s, t) for s, t in PLOT)
    parts.append(f'<polygon points="{plot}" fill="var(--terrace)" stroke="var(--ink)" stroke-width="1.6"/>')
    # Baufenster
    for t in (5.0, 20.0):
        parts.append(f'<line x1="{P(0,t).split(",")[0]}" y1="{P(0,t).split(",")[1]}" x2="{P(east_boundary_s(t),t).split(",")[0]}" y2="{P(east_boundary_s(t),t).split(",")[1]}" class="arc"/>')
    parts.append(f'<text x="{6.0*S+40:.1f}" y="{5*S+30-4:.1f}" class="tiny" text-anchor="start">Baugrenze t = 5.00</text>')
    parts.append(f'<text x="{6.0*S+40:.1f}" y="{20*S+30+12:.1f}" class="tiny" text-anchor="start">Baugrenze t = 20.00</text>')
    # 3 m setbacks (dashed): west x = 3; east: boundary minus 3 perpendicular, approximated by s - 3.1
    parts.append(f'<line x1="{3*S+40:.1f}" y1="{30:.1f}" x2="{3*S+40:.1f}" y2="{33.9*S+30:.1f}" class="glass"/>')
    east_off = " ".join(P(east_boundary_s(t) - 3.1, t) for t in (0.0, 6.2, 12.4, 35.0))
    parts.append(f'<polyline points="{east_off}" fill="none" class="glass"/>')
    # houses: west = mirror of east about the party line
    for (s0, s1, name, t0) in ((PARTY - HOUSE_W, PARTY, "west half · to let", T0 + offset), (PARTY, PARTY + HOUSE_W, "east half · own", T0)):
        parts.append(f'<rect x="{s0*S+40:.1f}" y="{t0*S+30:.1f}" width="{HOUSE_W*S:.1f}" height="{depth*S:.1f}" class="floor" stroke="var(--ink)" stroke-width="2"/>')
        parts.append(f'<text x="{(s0+s1)/2*S+40:.1f}" y="{(t0+depth/2)*S+30:.1f}" class="rname">{name}</text>')
        parts.append(f'<text x="{(s0+s1)/2*S+40:.1f}" y="{(t0+depth/2)*S+30+14:.1f}" class="tiny">{HOUSE_W:.2f} × {depth:.2f} m</text>')
        parts.append(f'<text x="{(s0+s1)/2*S+40:.1f}" y="{(t0+depth/2)*S+30+26:.1f}" class="tiny">{HOUSE_W*depth:.1f} m²</text>')
    parts.append(f'<line x1="{PARTY*S+40:.1f}" y1="{(T0+offset)*S+30:.1f}" x2="{PARTY*S+40:.1f}" y2="{(T0+depth)*S+30:.1f}" stroke="var(--accent)" stroke-width="3"/>')
    if offset:
        parts.append(f'<text x="{0.5*S+40:.1f}" y="{(T0+depth+offset+2.6)*S+30:.1f}" class="tiny" text-anchor="start">offset {offset:.2f} m: the west half stands {offset:.2f} m further south</text>')
    # garages
    wg = f'{P(0,T0)} {P(WEST_GAR_W,T0)} {P(WEST_GAR_W,T0+GAR_D)} {P(0,T0+GAR_D)}'
    eg = f'{P(PARTY+HOUSE_W,T0)} {P(east_boundary_s(T0),T0)} {P(east_boundary_s(6.2),6.2)} {P(east_boundary_s(T0+GAR_D),T0+GAR_D)} {P(PARTY+HOUSE_W,T0+GAR_D)}'
    for g, lab in ((wg, "garage 5.41"), (eg, "garage 4.8–6.9")):
        parts.append(f'<polygon points="{g}" fill="var(--furnfill)" stroke="var(--ink)" stroke-width="1.2" stroke-dasharray="4 3"/>')
    parts.append(f'<text x="{2.7*S+40:.1f}" y="{(T0+GAR_D/2)*S+30:.1f}" class="tiny">garage 5.41</text>')
    parts.append(f'<text x="{(PARTY+HOUSE_W+2.4)*S+40:.1f}" y="{(T0+GAR_D/2)*S+30:.1f}" class="tiny">garage 4.8–6.9</text>')
    # Abstandsfläche check at the east rear corner
    t_c = T0 + depth; s_c = PARTY + HOUSE_W
    gap = east_boundary_s(t_c) - s_c; ang = math.atan2(5.8, 22.6); dist = gap * math.cos(ang)
    parts.append(f'<line x1="{s_c*S+40:.1f}" y1="{t_c*S+30:.1f}" x2="{(s_c+gap)*S+40:.1f}" y2="{t_c*S+30:.1f}" class="dim"/>')
    parts.append(f'<text x="{(s_c-0.3)*S+40:.1f}" y="{t_c*S+30-6:.1f}" class="dimt" text-anchor="end">{dist:.2f} m to the east boundary</text>')
    # street, north arrow, labels
    parts.append(f'<text x="{15*S+40:.1f}" y="{18:.1f}" class="dimt">Altkönigstraße · street boundary · north</text>')
    parts.append(f'<text x="{10*S+40:.1f}" y="{30*S+30:.1f}" class="rsub">garden</text>')
    parts.append(f'<text x="{40-6:.1f}" y="{17*S+30:.1f}" class="tiny" transform="rotate(-90 {40-6:.1f} {17*S+30:.1f})">west boundary · no. 124</text>')
    parts.append(f'<text x="{(east_boundary_s(29)+1.0)*S+40:.1f}" y="{29*S+30:.1f}" class="tiny" transform="rotate(-76 {(east_boundary_s(29)+1.0)*S+40:.1f} {29*S+30:.1f})">east boundary · 5865/31</text>')
    parts.append(f'<g transform="translate({33*S+40:.1f} {60:.1f})"><polygon points="0,-15 5,6 0,2 -5,6" class="northp"/><text y="-19" class="dimt" text-anchor="middle">N</text></g>')
    # scale bar 10 m
    parts.append(f'<rect x="{40}" y="{36*S+30:.1f}" width="{5*S:.1f}" height="5" class="sb-a"/><rect x="{40+5*S:.1f}" y="{36*S+30:.1f}" width="{5*S:.1f}" height="5" class="sb-b"/><text x="{40}" y="{36*S+30-4:.1f}" class="dimt">0</text><text x="{40+10*S:.1f}" y="{36*S+30-4:.1f}" class="dimt">10 m</text>')
    w = 36*S + 80; h = 37.5*S + 30
    return (f'<svg viewBox="0 0 {w:.0f} {h:.0f}" role="img" aria-label="Site plan of Altkönigstraße 122 with the Baufenster, the mirrored T4 pair and the boundary garages" class="plan" style="max-width:520px">' + "".join(parts) + "</svg>"), dist

if __name__ == "__main__":
    s, d = svg(); print(len(s), f"{d:.2f}")
    s2, d2 = svg(offset=1.93, depth=13.07); print(len(s2), f"{d2:.2f}")
