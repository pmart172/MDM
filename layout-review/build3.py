import floors, plancss, math

plans = {k: f() for k, f in floors.ALL.items()}
issues = {k: p.check() for k, p in plans.items()}
svg = {k: p.svg() for k, p in plans.items()}
pathlen = {"dg_A": 11.0, "dg_B": 5.5, "dg_C": 5.0}

PAGE_CSS = r"""
<style>
/* Layout: one 72ch reading column; plan pairs and wide tables break out to the 1120px grid. */
""" + plancss.TOKENS + plancss.PLAN_CSS + r"""
body{background:var(--paper);color:var(--ink);font-family:var(--body);font-size:17px;line-height:1.5;padding-inline:16px;padding-block:8px 56px}
.wrap{max-width:1120px;margin:0 auto}
.col{max-width:72ch}
h1,h2,h3,h4{font-family:var(--display);text-wrap:balance;line-height:1.15;margin:0}
h1{font-size:clamp(30px,5vw,46px);font-weight:600;letter-spacing:-.01em}
h2{font-size:clamp(23px,3.2vw,30px);font-weight:600;margin-top:60px;padding-top:18px;border-top:2px solid var(--ink)}
h3{font-size:21px;font-weight:600;margin-top:36px}
h4{font-size:17px;font-weight:600;margin-top:22px;font-family:var(--body)}
p{margin:12px 0}
.eyebrow{font-family:var(--mono);font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);margin:0 0 10px}
.lede{font-size:20px;margin-top:14px}
.meta{color:var(--muted);font-size:15px}
ul,ol{padding-left:22px;margin:10px 0} li{margin:5px 0}
strong{font-weight:600}
.pair{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:22px;align-items:start;margin:18px 0}
.pair figure,.one figure{margin:0;min-width:0}
figcaption{font-size:14.5px;color:var(--muted);margin-top:8px;line-height:1.45}
figcaption b{color:var(--ink);font-weight:600}
.one{margin:18px 0;max-width:940px} .one figure{margin:0;min-width:0}
.legend{display:flex;flex-wrap:wrap;gap:8px 18px;font-size:13.5px;color:var(--muted);margin:8px 0 0}
.legend span::before{content:"";display:inline-block;width:12px;height:12px;border:1px solid var(--ink);margin-right:6px;vertical-align:-1px}
.legend .lw::before{background:var(--wetfill)} .legend .lb::before{background:var(--bedfill)} .legend .lc::before{background:var(--wardfill)}
.legend .lf::before{background:var(--furnfill)} .legend .lwin::before{background:var(--winfill)} .legend .lz::before{background:var(--zonefill);border-style:dashed}
.legend .lp::before{background:var(--pathfill);border-style:dashed} .legend .lnew::before{background:var(--accent);border:none}
.legend .lgone::before{background:none;border:1.5px dashed var(--bad)} .legend .lsl::before{border:none;border-top:3px dashed var(--accent);height:0;vertical-align:3px}
.legend .lwalk::before{border:none;border-top:2px dashed var(--bad);height:0;vertical-align:3px}
.tbl{overflow-x:auto;margin:14px 0}
table{border-collapse:collapse;width:100%;font-size:15px;font-variant-numeric:tabular-nums}
th,td{text-align:left;padding:8px 10px;border-bottom:1px solid var(--rule);vertical-align:top}
th{font-family:var(--mono);font-size:11.5px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);font-weight:500}
td.n{text-align:right;font-family:var(--mono);font-size:13.5px;white-space:nowrap}
td.c{text-align:center}
tr.total td{font-weight:600;border-top:2px solid var(--ink)}
.pill{display:inline-block;font-family:var(--mono);font-size:11.5px;padding:2px 8px;border-radius:999px;white-space:nowrap}
.ok{background:var(--ok-soft);color:var(--ok)} .warn{background:var(--warn-soft);color:var(--warn)} .bad{background:var(--bad-soft);color:var(--bad)}
.callout{border-left:3px solid var(--accent);background:var(--accent-soft);padding:12px 16px;margin:18px 0;border-radius:0 6px 6px 0}
.callout p{margin:6px 0}
.kv{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:12px;margin:18px 0}
.kv div{border-top:1px solid var(--rule);padding-top:8px}
.kv b{display:block;font-family:var(--mono);font-size:19px;font-weight:500;color:var(--accent)}
.kv span{font-size:14px;color:var(--muted)}
.small{font-size:14.5px;color:var(--muted)}
.score{font-family:var(--mono);font-size:17px;font-weight:600;color:var(--accent)}
.num{display:inline-block;width:20px;height:20px;border-radius:50%;background:var(--accent);color:var(--paper2);font-family:var(--mono);font-size:11.5px;font-weight:600;text-align:center;line-height:20px;margin-right:6px}
a{color:var(--accent)} a:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.src{font-size:14px} .src li{margin:4px 0}
@media (prefers-reduced-motion:no-preference){ html{scroll-behavior:smooth} }
</style>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@500;600&family=Source+Sans+3:ital,wght@0,400;0,600;1,400&family=IBM+Plex+Mono:wght@400;500;600&display=swap">
<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs><marker id="ah" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="context-stroke"/></marker></defs></svg>
"""

def pill(kind, text): return f'<span class="pill {kind}">{text}</span>'
OK = lambda t="meets": pill("ok", t); WARN = lambda t="partly": pill("warn", t); BAD = lambda t="fails": pill("bad", t)

def table(head, rows, cls=""):
    h = "".join(f"<th>{c}</th>" for c in head)
    body = ""
    for r in rows:
        tr_cls = ""
        if r and isinstance(r[0], str) and r[0].startswith("!"):
            tr_cls = ' class="total"'; r = [r[0][1:]] + list(r[1:])
        cells = ""
        for c in r:
            if isinstance(c, str) and c.startswith("#:"): cells += f'<td class="n">{c[2:]}</td>'
            elif isinstance(c, str) and c.startswith("c:"): cells += f'<td class="c">{c[2:]}</td>'
            else: cells += f"<td>{c}</td>"
        body += f"<tr{tr_cls}>{cells}</tr>"
    return f'<div class="tbl {cls}"><table><thead><tr>{h}</tr></thead><tbody>{body}</tbody></table></div>'

def fig(key, caption):
    return f'<figure>{svg[key]}<figcaption>{caption}</figcaption></figure>'

def n(i): return f'<span class="num">{i}</span>'

LEGEND = ('<p class="legend"><span class="lb">bed</span><span class="lw">wet fixtures</span><span class="lc">wardrobes</span><span class="lf">furniture</span>'
          '<span class="lwin">window</span><span class="lnew">new wall · new leaf · glass screen</span><span class="lgone">wall removed</span></p>'
          '<p class="small">Door symbols: a swing door shows the leaf at 90° and a dashed quarter arc; a pocket door shows the leaf half across the opening, the dashed cavity inside the wall it slides into, and an arrow for the direction. Numbered circles are keyed notes, explained in the caption. North is up on every plan; the scale bar is 2 m.</p>')

def schedule(key, rooms):
    p = plans[key]
    rows = []
    for f in p.fx:
        if f["room"] in rooms and f["kind"] not in ("nightstand", "chair", "stairs", "bench"):
            x0,y0,x1,y1 = f["box"]
            rows.append([f["room"], f["label"], f"#:{x1-x0:.2f} × {y1-y0:.2f}"])
    return table(["Room", "Item", "Footprint (m, as drawn)"], rows)

def clearances(key, rooms=None):
    p = plans[key]
    rows = []
    for (room, label, facing, dep, mn, cf) in p.clearances:
        if rooms and room not in rooms: continue
        status = OK("comfort") if dep >= cf-0.005 else (WARN("above minimum") if dep >= mn-0.005 else BAD("below minimum"))
        rows.append([room, label, facing, f"#:{min(dep,3):.2f}", f"#:{mn:.2f} / {cf:.2f}", status])
    return table(["Room", "Fixture", "Free side", "Free depth m", "VDI min / comfort", "Status"], rows)

# ---------------------------------------------------------------- section drawing (N–S)
def section_svg():
    S = 46; x0 = 40; yb = 440
    def X(v): return x0 + v*S
    def Y(h): return yb - h*S
    parts = []
    # floors: EG 0-2.8, OG 2.8-5.6, DG 5.6-8.4 ; N at left
    for (h0, h1, a, b, name) in [(0,2.8,0,11.04,"EG"),(2.8,5.6,0,11.04,"OG"),(5.6,8.4,1.23,9.43,"DG")]:
        parts.append(f'<rect x="{X(a)}" y="{Y(h1)}" width="{(b-a)*S}" height="{(h1-h0)*S}" class="floor" stroke="var(--ink)" stroke-width="1.6"/>')
        parts.append(f'<text x="{X((a+b)/2)}" y="{Y(h0)-S*1.2}" class="rname">{name}</text>')
    # strips
    for (a,b,lab) in [(0,1.23,"1.23 m"),(9.43,11.04,"1.53 m")]:
        parts.append(f'<rect x="{X(a)}" y="{Y(5.6)-10}" width="{(b-a)*S}" height="10" class="terrace" stroke="var(--ink)" stroke-width=".8"/>')
        parts.append(f'<text x="{X((a+b)/2)}" y="{Y(5.6)-16}" class="dimt">{lab}</text>')
    # parapet
    for a in (0, 11.04):
        parts.append(f'<rect x="{X(a)-2}" y="{Y(5.6)-S*0.9-10}" width="4" height="{S*0.9}" fill="var(--accent)"/>')
    parts.append(f'<text x="{X(11.04)+8}" y="{Y(5.6)-S*0.45}" class="note" text-anchor="start">parapet ≥ 0.90 m</text>')
    parts.append(f'<text x="{X(0)}" y="{yb+22}" class="dimt" text-anchor="start">north facade</text>')
    parts.append(f'<text x="{X(11.04)}" y="{yb+22}" class="dimt" text-anchor="end">south facade (garden)</text>')
    parts.append(f'<line x1="{X(0)}" y1="{yb+6}" x2="{X(11.04)}" y2="{yb+6}" class="dim"/><text x="{X(5.52)}" y="{yb+36}" class="dimt">11.04 m</text>')
    parts.append(f'<text x="{X(5.52)}" y="{Y(8.4)-12}" class="note" text-anchor="middle">set-back storey 7.13 × 8.20 m on an 8.29 × 11.04 m plate · east strip 1.16 m not in this cut</text>')
    return (f'<svg viewBox="0 0 720 490" role="img" aria-label="North–south section: the top floor is set back 1.23 m from the north facade and 1.53 m from the south facade, leaving two roof strips" class="plan" style="max-width:720px">'
            + "".join(parts) + '</svg>')

# ---------------------------------------------------------------- content
html = f"""<title>MDM Floor Plan Review</title>
{PAGE_CSS}
<div class="wrap">
<div class="col">
<p class="eyebrow">Third edition · semi-detached house · EG 8.29 × 11.04 · OG 8.29 × 11.04 · DG 7.13 × 8.20 m</p>
<h1>Floor plan review against 5-star hotel and luxury residential standards</h1>
<p class="lede">Nine plans drawn to one scale with standard architectural symbols: the three floors as you drew them, three options for the top floor, two for the upper floor, one for the ground floor. Every proposal is dimensioned against VDI 6000 movement areas, the hotel planning rules in Penner's <em>Hotel Design, Planning and Development</em> and Marriott's bay standards, and the German luxury-build conventions for a master suite. A geometry script checks each drawing for walls meeting windows, rooms without doors, door swings, fixture overlaps and the free depth in front of every fixture; an independent architectural review of the rendered drawings was run before publishing.</p>
<p class="meta">Dimensions were scaled from your three screenshots at about 106 px per metre, so allow ±5 cm. Exterior walls read as 0.36 m (0.22 m on the shared west wall), the wall with the flue as 0.24 m, partitions as 0.10–0.12 m. Areas are clear floor areas as your tool prints them. New doors are 0.90 m openings for a DIN 18101 885 × 2010 door (0.81 m clear). New partitions keep at least 0.15 m of solid wall between their end and any window reveal.</p>
</div>

<div class="kv">
<div><b>DG · Option A</b><span>bedroom 13.5 → 16.5 m² in the corner room, two partitions, no facade or stack change</span></div>
<div><b>OG · Option O1</b><span>12.1 m² family bath with a WC room, 2.7 m wardrobe walls, laundry upstairs</span></div>
<div><b>EG · Option E1</b><span>4.5 m² guest bath, 1.5 m wardrobe, 1.17 m corridor, kitchen untouched</span></div>
<div><b>1.53 m</b><span>south roof strip beside the DG bedroom: a terrace door is the biggest single upgrade</span></div>
</div>

<div class="col">
<h2 id="verdict">Verdict</h2>
<ol>
<li><strong>Top floor: build Option A.</strong> It keeps your own concept (foyer → walk-through dressing → bedroom, bath off the foyer) and fixes the allocation: the bedroom becomes the largest room at 16.5 m² with a 4.52 m head wall and two windows, the dressing is 2.85 m deep (the hausbaujournal double-sided module is 2.70 m) with 6.3 m of rail, and the bath is a five-fixture room with a 1.8 m double vanity, a 1.4 m walk-in shower, a 1.8 m tub under the window and a screened WC. Two partitions move, both ending 0.15 m clear of the window reveals, and one door becomes a pocket door. Its one real weakness is distance: bed to WC is about {pathlen['dg_A']:.0f} m through the private foyer. If a pocket door beside the bed matters more to you than the corner room and the untouched facade, build Option B (about {pathlen['dg_B']:.0f} m).</li>
<li><strong>Upper floor: build O1.</strong> The 4.7 m² bath fails your two-basin rule and cannot be fixed in place. O1 puts a 12.1 m² family bath in the south-west corner with a closed 1.1 × 1.6 m WC room, a 1.4 m double vanity, a 1.7 m tub under the window, a 1.06 × 1.2 m walk-in shower and the washer-dryer column. Both bedroom doors and the bedroom partition stay where they are; each room gets a 2.7 m wardrobe wall on the partition, a 1.6 × 2.0 m bed on the west wall with night tables on both sides and a desk at the window. A walk-in closet would have to stand in front of a window on this floor (the north and south window piers are only 0.85 m wide), so the wardrobe wall is the honest answer. O2 (two en suites) is drawn and scored.</li>
<li><strong>Ground floor: build E1.</strong> A 4.5 m² guest bath with its door straight off the hall and opening outward, a 1.5 m wardrobe in front of the flue block clear of the entrance door swing, a 1.17 m corridor that gives the bedroom a private door, and the kitchen, island, table and sofas where your rules want them. The laundry moves upstairs into the family bath, where the luxury-residential sources put it.</li>
<li><strong>The set-back storey.</strong> Your top floor is smaller than the floor below and offset from it by 1.23 m (north), 1.16 m (east) and 1.53 m (south). That is a Staffelgeschoss with roof strips on three sides. The south strip is at the 1.50 m threshold the German balcony guides call usable for a bistro table and two chairs. A French door from the DG bedroom onto it is the kind of feature hotel reviews rate above anything inside the room.</li>
</ol>

<h2 id="building">1 · Reading the building</h2>
<p>Before any wall moves, four facts about this house decide what is possible.</p>
</div>
<div class="one"><figure>{section_svg()}<figcaption><b>North–south section.</b> The DG footprint (7.13 × 8.20 m) sits inside the 8.29 × 11.04 m plate of the floors below. The stair positions line up floor to floor, so the offset is real, not a drawing artefact. The DG exterior walls stand mid-span on the OG ceiling, which is normal for a set-back storey on a concrete slab.</figcaption></figure></div>
<div class="col">
<ul>
<li><strong>Party wall west, windows north, east and south.</strong> The 0.22 m west wall is half of a double-leaf party wall. Every daylit room must sit on the east or south face; the south face looks onto the garden. The south-east corner of each floor is the best room in the house, and on the DG it is currently the smallest one.</li>
<li><strong>Stair.</strong> Three straight flights on the west wall, all stacked and all climbing north → south: the EG flight starts at y 1.55 m and arrives on the OG south landing; the OG flight starts at the north end (y 1.37 m) and arrives on the DG south landing at y 2.60 m. The 1.0 × 1.0 m zone at the foot of the DG foyer's south wall is that arrival landing. No door may swing onto it, which is why the DG bath door stays in its present opening in all three options and becomes a pocket door.</li>
<li><strong>Flue.</strong> The green element in your drawing is a flue or shaft. It runs in the 0.24 m wall between the DG foyer and the north-east room, stands free in the OG landing, and sits in the 0.85 × 1.65 m block on the EG. Every proposal keeps that wall and block; on the EG the wardrobe goes in front of it, on the OG the laundry closet (O2) beside it.</li>
<li><strong>Windows set the partition positions.</strong> Window piers on this house are short: 0.85 m beside the OG north and south windows, 0.37 m between the DG south window and the old bath wall. A partition that meets the facade inside a window opening is a construction fault, so every new partition here ends at least 0.15 m clear of a reveal, and the geometry check flags anything closer than 0.12 m.</li>
<li><strong>Structure and stacks.</strong> Nothing proposed touches an exterior wall, the flue wall, the OG bedroom partition (x 4.18–4.30 m) or the EG spine (x 3.51–3.75 m). The partitions that move are the 0.10–0.12 m ones. All three wet rooms today sit on the west party wall between y 5.0 and 9.1 m, so they share one stack; Option A and E1 keep that, O1 extends it 2.5 m south along the same wall. Only DG Options B and C move the master bath off the stack. Ask the structural engineer to confirm which OG partition, if any, carries the DG north wall at y 1.23 m before you remove anything on the OG; O1 and O2 only add walls there.</li>
</ul>

<h2 id="benchmark">2 · Benchmark</h2>
<p>Two sources of discipline. Hotels, because a brand's standard room has to fit bed, bath, closet and desk into a bay that is tested on thousands of rooms. Luxury residential and the German norms, because they set the clearances and the suite sequence a private house is judged by. The third column says where each rule landed in the drawings.</p>
</div>
{table(["What 5-star hotels build","Figure · source","Applied here"],[
 ["<strong>Three critical room dimensions:</strong> net width, length, headboard-wall length", "Penner, Adams &amp; Robson, <em>Hotel Design</em>, ch. 16", "Reported for every bedroom below. DG A: 3.65 × 4.52 m, head wall 4.52 m."],
 ["<strong>Module width.</strong> 3.7 m is the standard; 4.0–4.1 m lets the bed sit on the side wall instead of the end wall; little gain beyond 4.1 m", "Penner ch. 16", "DG bedrooms are 3.65 (A), 4.18 (B) and 3.58 m (C) wide, all with the bed on the side wall and a bench at the foot."],
 ["<strong>Marriott standard king:</strong> 4.0 × 7.5 m net = 30 m²; resort king 4 × 8 m = 34 m²; about 70 % bedroom / 30 % bath", "Marriott CALA guestroom standards; Marriott 'Rules of Thumb' (Cornell)", "DG suite: 8.6 foyer + 10.5 dressing + 16.5 bedroom + 11.3 bath = 47 m², a 60/40 split because the dressing counts as 'bath side'."],
 ["<strong>Luxury bay:</strong> internal width 4.2–5.5 m, 40–60 m² net; 15 × 30 ft (41.8 m²) luxury bay in the Cornell planning tables", "Volant Fitout; Cornell table via sunsgoods", "The whole DG is one 47 m² suite, i.e. junior-suite scale (60–90 m² is a true junior suite per Hidden Door)."],
 ["<strong>Five-fixture bathroom:</strong> two basins, tub, separate shower, separate WC. The Venetian built 10–12 m² five-fixture baths in standard rooms; luxury baths run 7–12 m²; 5-star plans give 25–28 % of the floor plate to bathrooms", "Penner ch. 16; venetianlasvegas.com; Afar (Michael Suomi); Mingsun", "DG baths 11.3 / 12.1 / 11.5 m² = 24–26 % of the DG. OG O1 bath 12.1 m² with a closed WC room."],
 ["<strong>Double vanity ≥ 1.83 m</strong> for luxury suites; walk-in shower 0.9 × 1.5 m 'more luxurious'; tubs 1.7–2.0 m", "georgebuildshop; Mingsun; Horow", "Vanities 1.8 m (A, C), 1.5 m (B); showers 1.4 × 1.0 (A), 1.2 × 1.2 (B), 1.35 × 1.1 (C); tubs 1.8 × 0.8 in the DG, 1.7 × 0.8 in O1."],
 ["<strong>Tub by the window.</strong> Four Seasons Otemachi puts the Deluxe tub beside the window; Aman Tokyo's furo sits at the window; Amanpuri gave the bath the size of the bedroom and light from four sides", "Business Traveller; Mr &amp; Mrs Smith; TopHotel News", "A: tub under the south window. B and C: tub under the east window. O1: tub under the south window."],
 ["<strong>Entry sequence.</strong> Wet and storage zones at the door, bed at the window; vestibule 0.9–1.2 m from door to first fixture; closet ≥ 1.22 m long, 0.66 m deep. Mandarin Oriental Jumeira: foyer → walk-in wardrobe → full bath across the hall. Bulgari Milano: 'the entrance, with an ample walk-in closet, conducts to the bedroom'", "Buildipedia; Homestyler; Marriott CALA; Archello; bulgarihotels.com", "Option A is this sequence: foyer → walk-through dressing → bedroom, bath across the foyer."],
 ["<strong>Dressing between bedroom and bath.</strong> Mandarin Oriental Hong Kong suites run bedroom → walk-in wardrobe → bathroom; Six Senses Yao Noi has a walk-through dressing; Rosewood Hong Kong's corner-suite bath opens from three doors", "The Suite Life HK; Mr &amp; Mrs Smith; The Luxury Traveller", "Option C: foyer → dressing → bath and bedroom → bath. Option B: bedroom → bath and bedroom → dressing. Neither bath has more than two doors; the wall lengths do not allow a third."],
 ["<strong>Headboard wall as a system:</strong> full-height panel, integrated night tables, reading lights, switches, USB and power, acoustic lining", "Volant Fitout; Censo", "Specified for the DG bedroom in every option; in A it also buffers the vanity on the far side."],
 ["<strong>Pocket doors</strong> between bedroom and en suite; obscured glass only around shower and WC", "Grand Designs Magazine", "New en suite and dressing doors are pocket doors where the wall has room for the cavity; the DG bath door becomes one."],
 ["<strong>Bed placement.</strong> Perpendicular to the window, the view the last thing you see; 0.6 m beside the bed minimum, 0.75–0.9 m comfortable; 0.9 m minimum from bed end to the TV cabinet, 1.1–1.4 m comfortable", "Hospitality Institute; Hotelier Academy; Volant Fitout", "0.75 m beside every DG bed; 1.1 m past the bench at the foot (A, B, C)."],
])}
{table(["What luxury residential and the German norms say","Figure · source","Applied here"],[
 ["<strong>Bedroom.</strong> 0.60 m beside the bed minimum, 0.70–0.80 m comfortable, 0.50 m at the foot if nothing stands there; a room of 3.50 × 4.20 m takes a double bed plus a 3 m wardrobe wall; comfort is 16–18 m²; 2.00 × 2.00 m is 'the luxury variant' of the double bed", "hausbaujournal.com (Schlafzimmer); meisterbetten.de", "DG A 16.5 m², B 17.1, C 14.6, all drawn with a 2.0 × 2.0 m bed. OG rooms 16.1 and 17.4 m² net of the wardrobe wall. EG 10.3 m² guest bedroom with 0.6 m beside the bed."],
 ["<strong>Dressing room.</strong> Hanging depth 0.60 m; single-sided 1.60 m wide; double-sided 2.70 m (0.6 + 1.5 + 0.6); comfortable 6–8 m², generous 10–12 m², a couple needs 9–10 m²; 1.5 m of rod per adult; aisle never under 1.0 m; an island needs 3.4 m of width", "hausbaujournal.com (Ankleide); heimwerker.de; Houzz AU", "A's dressing is 2.85 m deep, 10.5 m², 6.3 m of rod, 1.65 m aisle. B 9.1 m², 5.8 m rod, 1.1 m aisle. No island anywhere: no room is 3.4 m wide and free."],
 ["<strong>VDI 6000-1 movement areas:</strong> basin 0.90 × 0.55 m; WC 0.80 wide × 0.60 deep; shower 0.80 × 0.75; tub 0.90 × 0.75; 0.20 m between fixtures; areas may overlap each other but not shrink. Comfort tip: 1.00 × 1.00 m free at basin, WC and shower. DIN 18040-2: 1.20 × 1.20 m, bath doors open outward", "Reuter (VDI table); VDI FAQ; hausbaujournal; baunetzwissen", "Checked by script for every fixture (tables below). The EG guest-bath door and the O1 WC-room door open outward."],
 ["<strong>Double basin.</strong> 1.20 m is too tight for two; 1.30 m minimum (0.65 m per basin centre); NKBA wants 0.91 m between centres", "baunetzwissen; megabad; NKBA bath guidelines", "1.4–1.8 m vanities, basin centres 0.47–0.60 m from each end."],
 ["<strong>Walk-in shower.</strong> 0.90 × 0.90 is the standard tray; a walk-in with one open side needs 1.20 m minimum and 1.40 m is optimal", "hausjournal.net; megabad", "A: 1.40 × 1.00 with a 0.8 m fixed glass panel and the entry at the south end. B: 1.20 × 1.20. O1: 1.20 × 1.06. EG guest bath: 1.00 × 1.00 (a guest shower, not a walk-in)."],
 ["<strong>Separate WC room.</strong> ≥ 0.80 m wide and about 1.20 m deep in a dwelling; DIN 18228 cubicles are 0.85 × 1.25 (door out) or 0.85 × 1.50 (door in); 0.91 × 1.67 m reads as comfortable", "bauredakteur.de; Heinze (DIN 18228); Dwellify", "O1: 1.10 × 1.60 m with the door opening out, 0.94 m in front of the bowl. DG: WC screened by a 1.2 m wall, not enclosed (one couple)."],
 ["<strong>Master bath 10–15 m²;</strong> German 'Elternbad' plans land at about 12 m² with double basin, tub and walk-in shower", "plan7architect; energiesparhaus forum", "11.3 / 12.1 / 11.5 m² (DG A / B / C)."],
 ["<strong>Suite sequence.</strong> Luxury: entry buffer → wardrobe → sleep → bath; no sightline from bed to WC, WC behind a full door. German build forum consensus: <em>Bad → Ankleide → Schlafen</em>, the dressing as the acoustic and moisture buffer, suite width 4.5–4.8 m. One Hyde Park and Chelsea Barracks: his and hers via dressing areas into the bath", "Homestyler; Cohen White Associates; hausbau-forum.de; Tunstall; SheerLuxe", "A follows the German sequence. The WC is out of the bed's sightline and behind a screen in all three DG options."],
 ["<strong>Kitchen and dining.</strong> NKBA work aisle ≥ 1.07 m for one cook, ≥ 1.22 m for two; 0.81 / 0.91 / 1.12 m behind seating for no traffic / edging past / walking past; a 2.0 × 1.0 m table seats six comfortably; 0.60 m per person; 1.00 m behind chairs where people pass", "NKBA kitchen guidelines; tischonkel.de; baur.de", "E1: 1.20 m between run and island, 1.0 m around the table, 4.3 m run."],
 ["<strong>Living.</strong> A three-seater is 1.9–2.2 × 0.9–1.05 m; a 65-inch TV wants 2.0–2.6 m", "Kingscanapé; Samsung; Vebos", "O1 landing nook: 2.0 × 1.0 sofa, 2.6 m to the screen. E1: two 2.0 × 1.0 sofas, TV on the bedroom partition at 2.9 m."],
 ["<strong>Corridors and doors.</strong> DIN 18040-2 corridor ≥ 1.20 m; new-build practice 1.10–1.20 m, 1.40 m with a wardrobe; DIN 18101 885 × 2010 door = 0.86 m leaf, 0.81 m clear; windowless baths allowed with mechanical ventilation (Hessische Bauordnung, HBO)", "grundrisswissen.com; baunetzwissen; lexmea", "E1 corridor 1.17 m. All new openings 0.90 m. Every bath keeps a window; O1's WC room is windowless and needs a fan."],
 ["<strong>Laundry.</strong> 'As close to the master bedroom as possible', on the bedroom floor, with a drain pan; German owners warn a machine inside the dressing room keeps the bedroom awake", "The Columbian (Raquel Mothe); Frank Betz; hausbau-forum.de", "O1 puts the washer-dryer column inside the family bath behind its door, not in a dressing room. E1 drops the ground-floor utility."],
 ["<strong>Set-back storey.</strong> Setbacks of 1.25–3 m are typical; a roof strip is usable from 1.50 m (bistro table and two chairs), 1.20 m is a passage; railings ≥ 0.90 m for drops up to 12 m (HBO, Umwehrungen)", "heid-immobilienbewertung.de; hausbaujournal (Balkon); HBO (Umwehrungen)", "South strip 1.53 m: usable. East 1.16 m and north 1.23 m: passages only."],
 ["<strong>Feng shui (BTB school).</strong> Commanding position first (see the door diagonally, not in line with it), then no feet toward the door, solid headboard on a solid wall, not under a window. A toilet behind the headboard wall is the strongest concern, shower or sink milder. An en suite door at the foot of the bed is the worst case", "Anjie Cho / mindbodygreen; Master Sean Chan; Homes &amp; Gardens", "A: door diagonal, feet to the east window, vanity (not WC) behind the head, WC 1.3 m north of the head zone. B and C: the party wall behind the head, bath doors off the foot axis."],
])}

<div class="col">
<h2 id="audit">3 · Where the current plans stand</h2>
<p>Measured from your drawings and run through the same geometry check as the proposals. The check reports five faults in the current plans: the EG bedroom door swings into the bed, the EG basin has 0.37 m in front of it, the EG bed has 0.58 m on its south side, the OG north bedroom door swings onto the wardrobe front, and the OG shower has 0.65 m in front of its entry.</p>
</div>
{table(["Floor","Rule or standard","Current plan","Status"],[
 ["DG","Walk-in closet ≥ 6 m²","12.1 m² room with 6.3 m of wardrobe. Twice the requirement, in the second-best room of the floor.",OK("meets, oversize")],
 ["DG","Bath with tub, big shower, two basins","12.8 m²: 1.8 m tub, 1.8 × 1.0 m shower, a 2.0 m vanity with two basins. Meets the rule; it is the second-largest room.",OK()],
 ["DG","Bedroom: door not behind the bed, head wall ≥ 3.5 m, feng shui","Head wall 4.10 m, door diagonal at the north-east corner: correct. But the room is 3.30 × 4.10 m, the smallest on the floor, with 1.3 m past a 2.0 m bed and no space for a bench or desk.",WARN("meets, too small")],
 ["DG","Hotel entry sequence","Foyer → closet room → bedroom is already the hotel sequence. Keep it.",OK()],
 ["OG","Bath with two basins or two en suites","4.7 m², one basin, 0.65 m in front of the shower, two WC-type fixtures drawn on the east wall. Two basins need 1.3 m of wall plus 0.9 m standing room; the room has neither. Cannot be fixed inside its walls.",BAD()],
 ["OG","Two bedrooms with wardrobe or walk-in, plus a table","17.8 and 19.1 m² with a 0.57 m wardrobe strip each. The north bedroom door swings onto the wardrobe front. Single beds drawn.",WARN("door conflict")],
 ["OG","Living room, one sofa and TV","Sofa and TV board face each other across 2.6 m in the south-west; the rest of the 34.3 m² is landing.",OK("works, 19 m² landing")],
 ["EG","Bathroom at the entrance","3.1 m² guest WC, reached through a corridor; no shower; 0.37 m in front of the basin.",WARN("WC only")],
 ["EG","Wardrobe in the entrance","None drawn.",BAD("missing")],
 ["EG","1.9 m bed with two night tables","Fits on the 3.13 m west wall with 0.58 m on the south side. The bedroom door swings into the bed's corner, and the bedroom's east wall stands on the reveal of the south window.",WARN("door conflict")],
 ["EG","Kitchen 4.2 m, island 2.4 × 1.2, 2 × 1 table, two 2 × 1 sofas","Run 4.3 m, island 2.4 × 1.2 with a 1.2 m aisle, table and both sofas placed.",OK()],
])}

<div class="col">
<h2 id="dg">4 · Top floor: three options</h2>
<p>All three keep the foyer, the stair arrival, the flue wall and the three existing door openings. They differ in which corner gets the bed.</p>
<h3>Option A · the hotel sequence, refined</h3>
</div>
<div class="one">
{fig("dg_current", "<b>As drawn today.</b> 8.6 foyer · 12.1 closet room · 12.8 bath · 13.5 bedroom. The bedroom is the only room that is too small.")}
</div>
<div class="one">
{fig("dg_A", f"<b>Option A.</b> {n(1)} bath partition moves 0.37 m west to x 2.98–3.10, ending 0.15 m clear of the south window reveal. {n(2)} dressing partition moves 0.44 m north to y 3.20–3.32, 0.15 m below the east window reveal. {n(3)} the bath door keeps its opening and becomes a pocket door sliding west, clear of the stair landing. {n(4)} WC in the north-west corner facing south behind a 1.2 m screen, 0.94 m in front of it, out of sight from the door and 1.3 m north of the bed's head zone.")}
</div>
{LEGEND}
<div class="col">
<p><strong>Bedroom 3.65 × 4.52 m, 16.5 m².</strong> Net width 3.65 m, length 4.52 m, head wall 4.52 m (Penner's three numbers). 2.0 × 2.0 m bed with 0.50 m night tables, 0.75 m beside the bed on both sides, a 0.45 m bench at the foot and 1.1 m past it to the east wall, a 1.2 × 0.6 m desk under the south window. From the pillow you see the dressing door diagonally in the far north-east corner; your feet point at the east window. Behind the headboard wall is the double vanity, not the toilet; a 0.3 m built-in headboard panel with the night tables and reading lights integrated (the hotel bed-wall system) adds the acoustic buffer. If the south roof strip is walkable, the south window becomes a French door and the desk moves to the dressing table.</p>
<p><strong>Dressing 3.69 × 2.85 m, 10.5 m².</strong> 0.60 m wardrobe, 1.65 m aisle, 0.60 m wardrobe: the hausbaujournal double-sided module with 0.15 m to spare. 3.7 m of rod on the north wall, 1.0 m on the west, 1.6 m on the south, 6.3 m in all, against 1.5 m per adult recommended. Dressing table and stool under the east window. The door from the foyer keeps its opening; the door to the bedroom is a pocket door so the dressing reads as a vestibule, not a corridor.</p>
<p><strong>Bath 2.76 × 4.08 m, 11.3 m².</strong> Five fixtures: 1.8 × 0.8 m tub under the south window, 1.4 × 1.0 m walk-in shower on the west wall with a 0.8 m fixed glass panel and the entry at its south end, 1.8 m double vanity on the east wall with 1.21 m between the vanity front and the shower glass, WC in the north-west corner behind a 1.2 m screen with 0.94 m in front of it, 0.3 m open shelving beside the tub, towel radiator on the east wall by the door. A closed WC room does not fit without splitting the south window; for one couple the screened corner is what the hotel sources describe, and the OG gets the full WC room instead. The bath is reached from the foyer only: a door from the bedroom would have to sit in the headboard wall, which your own rule (no door behind the bed) forbids, so B and C carry the direct bedroom door instead.</p>
</div>
{schedule("dg_A", ("Bath","Dressing","Bedroom"))}
<div class="col"><h4>Option A, free depth in front of every fixture (geometry check)</h4></div>
{clearances("dg_A")}
<div class="col">
<h3>Option B · bath as the hub</h3>
</div>
<div class="one">
{fig("dg_B", f"<b>Option B.</b> {n(1)} the bedroom takes the existing foyer opening as its own door. {n(2)} new partition between bedroom and dressing at x 4.40–4.52 m; the south window behind it is infilled (blue), a facade change that needs a permit. {n(3)} swing door from the bedroom into the bath at x 3.45–4.35 m, opening into the bath, so no pocket cavity meets the new partition. {n(4)} WC in the north-west corner behind a 1.2 m screen that hides it from the foyer door; 1.4 m double vanity on the north wall, 1.8 m tub under the east window, 1.2 × 1.2 m walk-in shower in the south-east corner entered from the west. The dressing is entered from the bedroom through a pocket door sliding south into the new partition.")}
</div>
<div class="one">
{fig("dg_C", f"<b>Option C.</b> {n(1)} own bedroom door from the foyer. {n(2)} swing door from the bedroom into the bath at the north end of the new partition, opening into the bath; it sits above the bed line, so the feet do not point at it. {n(3)} swing door from the dressing into the bath, opening into the dressing, so guests reach the bath without crossing the bedroom. The new partition at x 3.80–3.92 m ends 0.18 m clear of the south window. Bath with two windows: 1.35 × 1.1 m walk-in shower in the north-east corner entered from the west, tub under the east window, 1.8 m double vanity and the WC on the partition wall where the pipes run. No facade change, but the bath leaves the west stack.")}
</div>
{LEGEND}
<div class="col">
<p><strong>B</strong> gives the bedroom a dry party wall behind the head, its own door and a second door straight into a 12.1 m² bath with the tub under the east window. It pays with the darkest bedroom of the three (one south window), a bath that now sits over the OG north bedroom and needs a new soil riser through that bedroom, two doors on the bedroom's north wall, and the loss of the south-east window. <strong>C</strong> is B with the bath and dressing swapped: a bright 11.5 m² bath with two windows and a 12.1 m² dressing, reached from the dressing as well as from the bedroom, but the bedroom shrinks to 14.6 m² and the bath still leaves the stack.</p>
<h3>Decision matrix</h3>
<p>Scores 1–5. Weights: bedroom quality 30 % (size, light, feng shui), suite flow 25 % (bed-to-WC distance, hotel sequence, guest access), bath and dressing spec 20 %, cost and risk 25 % (walls, stacks, facade, structure).</p>
</div>
{table(["Criterion","Weight","Option A","Option B","Option C"],[
 ["Bedroom quality","#:30 %","c:<b class='score'>5</b><br><span class='small'>16.5 m², corner room with two windows, diagonal door, vanity behind the head</span>","c:<b class='score'>4</b><br><span class='small'>17.1 m², one window, dry party wall behind the head, feet toward a dresser wall</span>","c:<b class='score'>3</b><br><span class='small'>14.6 m², one window, dry wall behind the head</span>"],
 ["Suite flow","#:25 %",f"c:<b class='score'>3</b><br><span class='small'>hotel sequence; bed → WC about {pathlen['dg_A']:.0f} m through the private foyer</span>",f"c:<b class='score'>5</b><br><span class='small'>pocket door beside the bed, about {pathlen['dg_B']:.0f} m; full loop; guests use the foyer door</span>",f"c:<b class='score'>4</b><br><span class='small'>about {pathlen['dg_C']:.0f} m; dressing reached via foyer or bath</span>"],
 ["Bath and dressing","#:20 %","c:<b class='score'>4</b><br><span class='small'>11.3 m² five fixtures, screened WC; dressing 10.5 m² by the book</span>","c:<b class='score'>4</b><br><span class='small'>12.1 m² with window tub, 1.4 m vanity; dressing 9.1 m², 1.1 m aisle, no south window</span>","c:<b class='score'>5</b><br><span class='small'>11.5 m² with two windows; dressing 12.1 m²</span>"],
 ["Cost and risk","#:25 %","c:<b class='score'>5</b><br><span class='small'>two 0.12 m partitions, one pocket door, stack and facade untouched</span>","c:<b class='score'>2</b><br><span class='small'>new soil riser through the OG bedroom, a window infilled (permit), two new doors</span>","c:<b class='score'>2</b><br><span class='small'>new soil riser through the OG bedroom; two new doors</span>"],
 ["!Weighted score","", "c:<b class='score'>4.30</b>", "c:<b class='score'>3.75</b>", "c:<b class='score'>3.40</b>"],
])}
<div class="col">
<div class="callout"><p><strong>Recommendation: A.</strong> B is the right answer only if you will not accept a bath that is two doors away from the bed.</p></div>

<h4>Option A door schedule</h4>
</div>
{table(["Door","Opening","Type","Note"],[
 ["Foyer → dressing","#:0.90 × 2.01","swing, hinge north, opens into the dressing","existing opening; leaf folds flat against the 1.0 m wardrobe"],
 ["Dressing → bedroom","#:0.90 × 2.01","pocket, slides west into the new partition","new; cavity x 4.80–5.70 m"],
 ["Foyer → bath","#:0.90 × 2.01","pocket, slides west","existing opening; no leaf near the stair landing; cavity x 0.94–1.84 m"],
 ["Bedroom south window","#:—","French door if the roof strip is walkable","parapet ≥ 0.90 m required"],
])}
<div class="col">
<h4>Feng shui check, Option A</h4>
<ul>
<li>Commanding position: from the pillow the dressing door is diagonal in the far north-east corner, 4.3 m away, not in line with the bed.</li>
<li>Feet point east to the window, not to a door. No door on the foot wall.</li>
<li>Solid wall behind the head (the moved partition), window beside the bed, not above it; matching night tables.</li>
<li>Far side of the head wall: vanity and mirror, towel radiator. The WC is on the opposite wall of the bath, 1.3 m north of the head zone. Use the built-in headboard panel if you want the buffer.</li>
<li>No en suite door facing the bed: the bath is entered from the foyer.</li>
</ul>

<h2 id="og">5 · Upper floor: two options</h2>
<p>The bedroom partition at x 4.18 m and both bedroom doors stay where they are in both options. What changes is the south-west corner and the inside of the two bedrooms.</p>
<h3>Option O1 · family bath with a WC room</h3>
</div>
<div class="one">
{fig("og_current", "<b>As drawn today.</b> 34.3 m² hall and living around the stair, a 4.7 m² bath with one basin, two 17.8 and 19.1 m² bedrooms with single beds and a 0.57 m wardrobe strip. The north bedroom door swings onto the wardrobe.")}
</div>
<div class="one">
{fig("og_O1", f"<b>Option O1.</b> {n(1)} new wall at y 7.50 m closes the south-west corner as a 3.96 × 3.06 m bath with its door at x 2.30–3.20 m; the old bath walls go. {n(2)} 0.9 × 1.6 m WC room in the north-west corner on the party wall, the door opening outward into the bath. {n(3)} 1.2 × 1.34 m walk-in shower under the west part of the south window, entered from the east; 1.8 m tub under the east part of the window and the pier; 1.4 m double vanity on the east wall; washer-dryer column in the north-east corner. {n(4)} 0.65 m wardrobe wall (2.7 m of rail) on the partition in each bedroom, bed on the west wall with night tables both sides, desk at the window. {n(5)} the landing becomes the TV nook: 2.0 × 1.0 m sofa, 2.6 m to the screen between the two bedroom doors.")}
</div>
{LEGEND}
<div class="col">
<p><strong>Family bath 3.96 × 3.06 m, 12.1 m².</strong> The south window pier is only 1.16 m wide, so nothing with a wall stands in the south-east corner: the 1.8 × 0.8 m tub runs along the south wall under the east part of the window, the 1.2 × 1.34 m walk-in shower sits under the west part with a 0.6 m fixed panel and a 0.96 m entry between its glass and the tub end, the 0.9 × 1.6 m WC room sits in the north-west corner on the party wall where the soil stack runs, with 0.94 m in front of the bowl and a door opening out into the bath. The 1.4 m double vanity is on the east wall with 2.2 m of floor in front, the washer-dryer column stands in the north-east corner beside the door. Two children can use basin and shower while a third uses the WC. The WC room has no window and needs an extractor (BauO § 43).</p>
<p><strong>Bedrooms 17.8 and 19.1 m² gross, 16.1 and 17.4 m² net.</strong> The north and south window piers are only 0.85 m wide, so a walk-in closet on this floor would stand in front of a window; the integrated wardrobe wall your rule allows is the right answer. Each room gets a 0.65 m deep, 2.7 m wide wardrobe wall on the partition, a 1.6 × 2.0 m bed on the west wall with 0.42 m night tables on both sides (0.62 m clear beside the bed, 0.65 m at the foot to the desk chair), and a 1.4 × 0.6 m desk under the window with the chair between desk and bed. The door swings are clear of everything.</p>
</div>
{schedule("og_O1", ("Family bath",))}
<div class="col"><h4>Option O1, free depth in front of every fixture (geometry check)</h4></div>
{clearances("og_O1")}
<div class="col">
<h3>Option O2 · two en suites, hotel bays</h3>
</div>
<div class="one">
{fig("og_O2", f"<b>Option O2.</b> {n(1)} each bedroom becomes a hotel bay: 1.0 m vestibule from the existing door (the north door is re-hung to open against the partition), 0.65 m reach-in closet with sliding doors (1.8 m of rail), 1.86 × 1.83 m en suite with a 1.0 × 1.0 m shower, WC and 0.8 m basin. {n(2)} the en suite is entered through a pocket door at the foot end of the room, beyond the bed; the bed lies on the west wall with night tables both sides. {n(3)} the south-west corner becomes a 12.1 m² study or guest room with the south window. {n(4)} laundry closet with bifold doors against the flue on the landing. Both east windows move 0.5 m away from the en-suite strips, a facade change that needs a permit; the en suites are windowless and need extractors.")}
</div>
{table(["Criterion","Weight","O1 · family bath","O2 · two en suites"],[
 ["Bedroom quality","#:30 %","c:<b class='score'>4</b><br><span class='small'>16.1 / 17.4 m² net, 2.7 m wardrobe wall, desk at the window, 2.0 m beds possible</span>","c:<b class='score'>3</b><br><span class='small'>10.7–12.0 m² sleeping zone + 1.8 m² vestibule each; hotel feel, 1.6 m beds</span>"],
 ["Bath spec vs your rule","#:25 %","c:<b class='score'>5</b><br><span class='small'>two basins, tub, walk-in shower, WC room, laundry</span>","c:<b class='score'>4</b><br><span class='small'>two 3.4 m² shower rooms; no tub, extractor fans, laundry closet on the landing</span>"],
 ["Privacy and resale","#:20 %","c:<b class='score'>3</b><br><span class='small'>shared bath, separate WC</span>","c:<b class='score'>5</b><br><span class='small'>every bedroom with its own bath; plus a 12 m² bonus room</span>"],
 ["Cost and risk","#:25 %","c:<b class='score'>4</b><br><span class='small'>one wet room on the existing stack, four partitions</span>","c:<b class='score'>2</b><br><span class='small'>two wet rooms off the stack, two windows moved, eight partitions</span>"],
 ["!Weighted score","", "c:<b class='score'>4.05</b>", "c:<b class='score'>3.45</b>"],
])}
<div class="col">
<div class="callout"><p><strong>Recommendation: O1.</strong> Choose O2 only if the rooms are for teenagers or long-stay guests and the bonus room pays for the second wet room.</p></div>

<h2 id="eg">6 · Ground floor</h2>
</div>
<div class="one">
{fig("eg_current", "<b>As drawn today.</b> 60 m² of hall, living and kitchen, a 3.1 m² guest WC behind a 1.3 m corridor, a 13.0 m² L-shaped bedroom whose door swings into the bed.")}
</div>
<div class="one">
{fig("eg_E1", f"<b>Option E1.</b> {n(1)} 1.5 m wardrobe in front of the flue block, clear of the entrance door swing, 0.98 m passage beside the stair, bench opposite. {n(2)} 2.00 × 2.26 m guest bath: 0.9 m basin on the north wall, WC in the south-west corner facing north and out of the door's sightline, 1.0 × 1.0 m shower in the south-east corner behind a fixed panel, entered from the north with 1.26 m in front; the door opens outward into the corridor. {n(3)} 1.17 m corridor, open to the hall. {n(4)} 3.29 × 3.13 m bedroom with a 1.9 × 2.0 m bed, night tables, a 0.48 m slim wardrobe on the pier beside the south window and a door from the corridor. {n(5)} 4.3 m kitchen run, 2.4 × 1.2 m island with a 1.2 m work aisle and 0.93 m to the east wall, 2.0 × 1.0 m table for six, two 2.0 × 1.0 m sofas in an L with the TV on the bedroom wall at 2.9 m.")}
</div>
{LEGEND}
<div class="col">
<p>The ground floor already does what your rules ask of the kitchen and living area, so E1 leaves that side alone apart from drawing the chairs and the aisles to scale. The work is in the 3.4 m strip west of the spine wall: today it holds a WC and a corridor that is wider than it needs to be. E1 uses the same strip for a real guest bath (4.5 m² against the 3.1 m² WC), keeps a corridor at the new-build standard of 1.17 m so the bedroom door stays private, and puts the wardrobe in the hall where the entrance door cannot hit it. The bedroom becomes a clean 3.29 × 3.13 m rectangle: 0.61 m and 0.62 m beside the bed, 0.81 m past the foot to a 0.48 m slim wardrobe that stands on the wall pier east of the south window, not in front of it; it is a guest room, not a primary bedroom. The laundry goes upstairs into the family bath. If you would rather keep a ground-floor utility room, the 3.4 m² version from the first edition fits in the corridor's place, at the price of the bedroom door opening into the living room.</p>
</div>
{schedule("eg_E1", ("Guest bath","Entrance hall","Bedroom"))}
<div class="col"><h4>Option E1, free depth in front of every fixture (geometry check)</h4></div>
{clearances("eg_E1", ("Guest bath","Bedroom"))}

<div class="col">
<h2 id="build">7 · What to build, in order</h2>
<h4>Walls, coordinates from the north-west outside corner of each floor</h4>
</div>
{table(["Floor · option","Remove","Add","Doors and windows"],[
 ["DG · A","Bath/bedroom partition x 3.35–3.45, y 3.74–7.84. Closet/bedroom partition y 3.64–3.74, x 3.10–6.75.","Partition x 2.98–3.10, y 3.76–7.84. Partition y 3.20–3.32, x 3.06–6.75. 1.2 m screen x 1.02–1.14, y 3.76–4.76.","Pocket door in the foyer/bath opening x 1.84–2.74 (cavity x 0.94–1.84). Pocket door dressing/bedroom x 5.70–6.60 (cavity x 4.80–5.70). Optional French door in place of the south window x 4.10–6.14."],
 ["DG · B","Bath/bedroom partition x 3.35–3.45.","Partition x 4.40–4.52, y 3.76–7.84. 1.2 m screen x 3.06–3.70, y 1.75–1.87.","Swing door x 3.45–4.35 in the wall y 3.64–3.76, opens into the bath; pocket door y 3.90–4.80 in the new partition (cavity y 4.80–5.70). South window x 4.10–6.14 infilled (permit)."],
 ["DG · C","Bath/bedroom partition x 3.35–3.45.","Partition x 3.80–3.92, y 3.76–7.84.","Swing door y 4.00–4.90 in the new partition, opens into the bath; swing door x 4.40–5.30 in the wall y 3.64–3.76, opens into the dressing."],
 ["OG · O1","Bath walls y 5.01–5.13 and y 6.94–7.06 (x 0.22–2.93), x 2.81–2.93 (y 5.13–6.94).","Wall y 7.50–7.62, x 0.22–4.18. WC room walls x 1.12–1.24 (y 7.62–9.34) and y 9.22–9.34 (x 0.22–1.24).","Bath door x 2.30–3.20 in the new wall, opens into the bath. WC-room door y 7.95–8.75 in the wall x 1.12–1.24, opens out. Bedroom doors unchanged."],
 ["EG · E1","WC east wall x 1.58–1.70 (y 5.11–7.36). Corridor/bedroom wall x 3.02–3.12 (y 5.11–10.68).","Wall x 2.22–2.34, y 5.10–7.36. Wall x 3.51–3.63, y 5.10–10.68.","Opening x 2.46–3.39 hall → corridor (no door). Bath door y 5.30–6.20 opens into the corridor. Bedroom door x 2.46–3.36 in the existing wall y 7.36–7.55, opens into the bedroom."],
])}
<div class="col">
<ol>
<li><strong>Confirm the two readings this review depends on.</strong> Is the roof around the DG a walkable terrace (railing, drainage, load)? Which OG wall, if any, carries the DG north wall? Both answers change nothing in Option A, O1 or E1; they decide the French door and whether you may ever remove the OG partition.</li>
<li><strong>Plumbing.</strong> Option A, O1 and E1 keep every wet room on the west party wall. O1's bath lies above the EG bedroom, not the EG bath, so its stack runs down the party wall boxed into the EG bedroom's west wall; the WC room sits directly on that wall. Only B or C need a new DG riser through the OG north bedroom.</li>
<li><strong>Order of works.</strong> OG bath first (it is the only rule failure that needs a plumber), then the DG partitions, then the EG strip. The EG kitchen and living side need no work.</li>
<li><strong>Bed wall systems.</strong> Specify the DG headboard panel with integrated night tables, lighting, switches and sockets at 0.3 m depth; the hotel sources treat this as the one element guests notice, and it is the feng shui buffer on the bath side.</li>
<li><strong>Doors.</strong> Pocket doors need a cavity as long as the opening beside it; every pocket door drawn has its cavity inside a straight wall with no other opening in it. Bath doors opening outward (EG guest bath, OG WC room) take a free-occupied indicator lock.</li>
</ol>

<h2 id="method">How the drawings were checked</h2>
<p>Each plan is generated from a list of walls, windows, doors and fixtures in metres. Before rendering, a script tests every drawing: a new partition may not meet a window opening or end within 0.12 m of a reveal; every bath, bedroom, dressing, WC room, corridor and study must have a door on its boundary; every door opening must lie inside a wall; a pocket door's cavity must lie inside a straight wall with no other opening; no fixture may overlap another fixture or a wall; no tall wardrobe may stand in front of a window; no door swing may hit a fixture; and the free depth in front of each WC, basin, shower entry, tub and bed side is measured by ray-casting against walls and fixtures and compared with the VDI 6000 minimum and comfort figures. All six proposals pass; the five faults the script reports are in the current plans. The rendered drawings were then reviewed twice by an independent architectural reviewer against a defect checklist; the first pass found 40 items (among them walls meeting window reveals, pocket cavities crossing wall junctions, a tub standing in front of a door, en-suite doors behind bed heads) and every one was corrected or, where the drawing was right, answered in the captions. The second reviewer pass did not complete (the review service refused the run); the corrections were re-checked by the geometry script and by eye, so that pass remains open.</p>

<h2 id="caveats">What this review could not verify</h2>
<ul>
<li>Dimensions come from screenshots at ±5 cm. Have the partition positions set out from the as-built survey, not from these numbers.</li>
<li>The stair direction was inferred from the arrival-landing logic (a flight cannot arrive flush against the DG north wall). If a flight runs the other way, the only change is that the OG sofa slides 1 m.</li>
<li>Roof slopes, parapets and the walkability of the set-back strips are not visible in the plans.</li>
<li>The stair is drawn as in your plans, a 2.3–2.5 m straight run, which is too short for a 2.8 m storey; it is kept as a schematic. The flue footprint also differs between your three drawings (0.85 × 1.65 m on the EG, 0.23 × 2.55 m on the OG, 0.24 × 1.6 m on the DG); the proposals keep each as drawn.</li>
<li>The research agents could only read search extracts, not full pages; every figure above is tied to the URL that showed it, and VDI 6000-1:2024-07, DIN 18040-2 and Neufert should be checked in the primary text before they go into a tender.</li>
</ul>

<h2 id="sources">Sources</h2>
<h4>Hotel planning</h4>
<ul class="src">
<li>Penner, Adams &amp; Robson, <em>Hotel Design, Planning and Development</em>, 2nd ed., ch. 16 Guestroom and Suite Design (Bloomsbury excerpt): module widths 3.7 / 4.0–4.1 m, three critical dimensions, five-fixture bath.</li>
<li><a href="https://crhotelmanagementgroup.com/wp-content/uploads/2024/10/Guest-Rooms.pdf">Marriott Global Design Strategies, CALA guestroom standards</a>: king 4.0 × 7.5 m, closet 1.22 m / 0.66 m, fixture counts.</li>
<li><a href="https://s3.amazonaws.com/ecornell/content/SHA/SHA626/SHA626_Marriott-Rules-of-Thumb.pdf">Marriott Rules of Thumb (eCornell)</a>: bedroom/bath split, clear width at the foot of the bed.</li>
<li><a href="https://volant-fitout.com/blog/hotel-room-dimensions-guide/">Volant Fitout, hotel room dimensions</a> and <a href="https://volant-fitout.com/blog/15-hotel-headboard-wall-design-ideas/">headboard wall systems</a>: luxury widths 4.2–5.5 m, bed clearances, bed-wall components.</li>
<li><a href="https://www.afar.com/hotels/to-understand-hotel-luxury-look-at-the-bathroom">Afar, "To understand hotel luxury, look at the bathroom"</a>: 25–28 % of the plate for baths.</li>
<li><a href="https://www.mingsungroup.com/article/hotel-bathroom-size-standards-meters.html">Mingsun, hotel bathroom size standards</a>; <a href="https://georgebuildshop.com/what-is-the-standard-double-vanity-length-for-hotels/">George Build Shop, double vanity length</a>; <a href="https://www.venetianlasvegas.com/hotel/the-venetian/luxury-two-queen-suite.html">The Venetian, suite bath</a>.</li>
<li><a href="https://archello.com/project/mandarin-oriental-jumeira">Archello, Mandarin Oriental Jumeira</a>; <a href="https://www.bulgarihotels.com/en_US/milan/the-hotel/the-design">Bulgari Milano, the design</a>; <a href="https://www.thesuitelife.com.hk/mandarin-oriental-hong-kong-hotel-review/">The Suite Life, Mandarin Oriental Hong Kong</a>; <a href="https://theluxurytraveller.com/hotel-reviews/rosewood-hong-kong/">The Luxury Traveller, Rosewood Hong Kong</a>; <a href="https://www.mrandmrssmith.com/luxury-hotels/aman-tokyo/rooms">Mr &amp; Mrs Smith, Aman Tokyo</a>; <a href="https://www.businesstraveller.com/tried-tested/hotel-review-four-seasons-hotel-tokyo-at-otemachi/">Business Traveller, Four Seasons Otemachi</a>; <a href="https://tophotel.news/how-aman-carved-a-niche-in-luxury-hotel-and-resort-design">TopHotel News, Aman</a>; <a href="https://www.hyatt.com/park-hyatt/en-US/tyoph-park-hyatt-tokyo/rooms">Park Hyatt Tokyo rooms</a>.</li>
<li><a href="https://www.granddesignsmagazine.com/bathroom/hotel-bathroom-design/">Grand Designs, hotel bathroom design</a>: pocket doors, obscured glass; <a href="https://www.hotelieracademy.org/amazing-hotel-beds-with-stunning-views/">Hotelier Academy</a>, bed to the view.</li>
</ul>
<h4>Residential standards and German norms</h4>
<ul class="src">
<li><a href="https://hausbaujournal.com/raeume/schlafzimmer/">hausbaujournal, Schlafzimmer</a>, <a href="https://hausbaujournal.com/raeume/ankleidezimmer/">Ankleidezimmer</a>, <a href="https://hausbaujournal.com/raeume/balkon/">Balkon</a>: bed clearances, dressing modules, terrace depths.</li>
<li><a href="https://www.reuter.de/magazin/abmessungen-badezimmer.html">Reuter, VDI 6000 movement areas</a>; <a href="https://www.vdi.de/richtlinien/details/vdi-6000-blatt-1-ausstattung-von-und-mit-sanitaerraeumen-wohnungen">VDI 6000 Blatt 1</a>; <a href="https://www.bauredakteur.de/masse-im-badezimmer-mindestabstaende-im-bad/">bauredakteur, Maße im Bad</a>; <a href="https://www.baunetzwissen.de/bad-und-sanitaer/fachwissen/barrierefreiheit/barrierefreie-sanitaerraeume-nach-din-18040-2-172838">baunetzwissen, DIN 18040-2</a>; <a href="https://www.megabad.com/magazin/ratgeber/badezimmer/dusche-masse/">megabad, Duschmaße</a>; <a href="https://www.hausjournal.net/walk-in-dusche-mindestgroesse">hausjournal, Walk-in Mindestgröße</a>; <a href="https://www.heinze.de/produktserie/trennwaende-fuer-wc-anlagen/10021847/1/">Heinze, DIN 18228 cubicles</a>.</li>
<li><a href="https://media.nkba.org/uploads/2022/05/Kitchen-Planning-Guidelines.pdf">NKBA kitchen planning guidelines</a> and <a href="https://media.nkba.org/uploads/2022/05/Bath-Planning-Guidelines.pdf">bath planning guidelines</a>; <a href="https://www.tischonkel.de/aktuelles/en/how-many-people/">Tischonkel, table seating</a>.</li>
<li><a href="https://grundrisswissen.com/optimale-flurbreite/">grundrisswissen, Flurbreite</a>; <a href="https://www.baunetzwissen.de/fenster-und-tueren/fachwissen/konstruktion-funktion/tuerblattgroessen-nach-din-18101-155263">baunetzwissen, DIN 18101</a>; <a href="https://lexmea.de/en/gesetz/bauo-2018-nrw/43">HBO (fensterlose Bäder)</a>; HBO (Umwehrungen); <a href="https://www.heid-immobilienbewertung.de/immobilienlexikon/staffelgeschoss/">Heid, Staffelgeschoss</a>.</li>
<li><a href="https://www.hausbau-forum.de/posts/529993/">hausbau-forum, Bad → Ankleide → Schlafen</a>; <a href="https://cohenwhiteassoc.com/master-suite-design-for-luxury-buyers/">Cohen White Associates, master suite design</a>; <a href="https://www.homestyler.com/article/luxury-master-suite-designs">Homestyler, luxury master suites</a>; <a href="https://tunstallproperty.co.uk/property/one-hyde-park-sw1-2/">One Hyde Park listing</a>; <a href="https://www.columbian.com/news/2019/oct/15/redo-laundry-room-for-function-style">The Columbian, laundry placement</a>; <a href="https://frankbetzhouseplans.com/house-plan-news/trend-spotlight-laundry-access-from-master-bathroom/">Frank Betz, laundry off the master bath</a>.</li>
<li><a href="https://www.mindbodygreen.com/articles/how-to-position-your-bed-according-to-feng-shui">Anjie Cho, bed position (mindbodygreen)</a>; <a href="https://www.anjiecho.com/holistic-spaces-blog/best-feng-shui-bed-position">anjiecho.com, best bed position</a>; <a href="https://www.masterseanchan.com/feng-shui-bed-against-bathroom-wall/">Master Sean Chan, bed against a bathroom wall</a> and <a href="https://www.masterseanchan.com/feng-shui-en-suite-bathroom-door-facing-bed/">en suite door facing the bed</a>; <a href="https://homesandgardens.com/interior-design/bedrooms/is-it-okay-to-place-a-bed-under-a-window">Homes &amp; Gardens, bed under a window</a>.</li>
</ul>
</div>
</div>
"""
open("artifact.html","w").write(html)
link_end = html.index('>', html.index('<link')) + 1
doc = ('<!DOCTYPE html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
       + html[:link_end] + '</head><body>' + html[link_end:] + '</body></html>')
open("index.html","w").write(doc)
print(len(html), "chars;", {k: len(v) for k, v in issues.items()})
