"""Sixth edition: three views on one page: Index (all versions with their key figures), Compare (pick two or three versions,
plans side by side plus a facts table) and the full review (the fifth-edition page, unchanged)."""
import json, re
import build5, build3
from build3 import table, OK, WARN, BAD

html5 = build5.html
cut = html5.index('<div class="wrap">')
head_part, read_body = html5[:cut], html5[cut:]
read_body = read_body.replace('<p class="eyebrow">Fifth edition · two-storey version on the Altkönigstraße 122 envelope', '<p class="eyebrow">Seventh edition · full review · two-storey version on the Altkönigstraße 122 envelope', 1)

# ---- tag every plan SVG with an id so the compare view can clone it
all_svgs = {}
all_svgs.update(build3.svg); all_svgs.update(build5.svg2)
all_svgs["site"] = build5.site_svg; all_svgs["site_v"] = build5.site_svg_v
for key, s in all_svgs.items():
    tagged = s.replace('<svg ', f'<svg id="svg-{key}" ', 1)
    assert s in read_body, key
    read_body = read_body.replace(s, tagged, 1)
# ---- anchors on the option headings
for old, new in [('<h3>Option A ·', '<h3 id="opt-A">Option A ·'), ('<h3>Option B ·', '<h3 id="opt-B">Option B ·'), ('<h3>Option C ·', '<h3 id="opt-C">Option C ·'),
                 ('<h3>Option O1 ·', '<h3 id="opt-O1">Option O1 ·'), ('<h3>Option O2 ·', '<h3 id="opt-O2">Option O2 ·'), ('<h3>Option E1', '<h3 id="opt-E1">Option E1'),
                 ('<h3>Option T1 ·', '<h3 id="opt-T1">Option T1 ·'), ('<h3>Option T4 ·', '<h3 id="opt-T4">Option T4 ·'), ('<h3>Inspired by the Rötha', '<h3 id="opt-T4v">Inspired by the Rötha')]:
    if old in read_body: read_body = read_body.replace(old, new, 1)

P3, P2 = build3.plans, build5.plans2
def net3(keys): return sum(v[4] for k in keys for v in P3[k].rooms.values())
def net2(keys): return sum(v[4] for k in keys for v in P2[k].rooms.values())

LEVELS = ["Site", "Ground floor", "Upper floor", "Top floor", "Basement"]
CONFIGS = {
 "today":   dict(label="Today · Inhouse 12, three storeys", group="three", levels={"Ground floor": "eg_current", "Upper floor": "og_current", "Top floor": "dg_current"}, read="#read/verdict"),
 "rework":  dict(label="Three-storey rework · A + O1 + E1", group="three", levels={"Ground floor": "eg_E1", "Upper floor": "og_O1", "Top floor": "dg_A"}, read="#read/dg"),
 "reworkB": dict(label="Three-storey with top-floor option B", group="three", levels={"Ground floor": "eg_E1", "Upper floor": "og_O1", "Top floor": "dg_B"}, read="#read/opt-B"),
 "reworkC": dict(label="Three-storey with top-floor option C", group="three", levels={"Ground floor": "eg_E1", "Upper floor": "og_O1", "Top floor": "dg_C"}, read="#read/opt-C"),
 "reworkO2":dict(label="Three-storey with upper-floor option O2", group="three", levels={"Ground floor": "eg_E1", "Upper floor": "og_O2", "Top floor": "dg_A"}, read="#read/opt-O2"),
 "t1":      dict(label="T1 · two storeys, same plate", group="two", levels={"Ground floor": "t1_eg", "Upper floor": "t1_og"}, read="#read/opt-T1"),
 "t4":      dict(label="T4 · two storeys, plot maximum + basement", group="two", levels={"Site": "site", "Ground floor": "t4_eg", "Upper floor": "t4_og", "Basement": "t4_kg"}, read="#read/opt-T4"),
 "t4v":     dict(label="T4v · offset pair (Rötha)", group="two", levels={"Site": "site_v", "Ground floor": "t4_eg", "Upper floor": "t4_og", "Basement": "t4_kg"}, read="#read/opt-T4v"),
 "t5":      dict(label="T5 · Rötha stair parallel to the street", group="two", levels={"Site": "site", "Ground floor": "t5_eg", "Upper floor": "t5_og", "Basement": "t5_kg"}, read="#read/opt-T5"),
 "t2":      dict(label="T2 · earlier study, not buildable here", group="study", levels={"Ground floor": "t2_eg", "Upper floor": "t2_og"}, read="#read/opt-T4v"),
 "t3":      dict(label="T3 · earlier study, not buildable here", group="study", levels={"Ground floor": "t3_eg", "Upper floor": "t3_og", "Basement": "t3_kg"}, read="#read/opt-T4v"),
}
n_today = net3(["eg_current","og_current","dg_current"]); n_rework = net3(["eg_E1","og_O1","dg_A"]); n_B = net3(["eg_E1","og_O1","dg_B"]); n_C = net3(["eg_E1","og_O1","dg_C"]); n_O2 = net3(["eg_E1","og_O2","dg_A"])
n_t1 = net2(["t1_eg","t1_og"]); n_t2 = net2(["t2_eg","t2_og"]); n_t3 = net2(["t3_eg","t3_og"]); n_t4 = net2(["t4_eg","t4_og"]); n_t4k = net2(["t4_kg"]); n_t5 = net2(["t5_eg","t5_og"]); n_t5k = net2(["t5_kg"]); n_t3k = net2(["t3_kg"])

ROWS = ["Storeys", "Plate per house", "Footprint · GRZ use (0.25 → 120.8 m²)", "Gross floor area above ground", "Net floor area of the rooms", "Wohnfläche, estimate", "Stairs", "Windows", "Bedrooms", "Master suite (bed · dressing · bath)", "Bathrooms", "Living · dining · kitchen", "Utility", "Planning status", "Altkönigstraße brief", "Verdict"]
def facts(**kw): return {r: kw.get(r, "") for r in ROWS}
FACTS = {
 "today": facts(**{"Storeys": "2 + set-back storey", "Plate per house": "8.29 × 11.04 · DG 7.13 × 8.20", "Footprint · GRZ use (0.25 → 120.8 m²)": "91.5 m² · 76 %", "Gross floor area above ground": "242 m²", "Net floor area of the rooms": f"{n_today:.0f} m²", "Wohnfläche, estimate": "186–192 m²", "Stairs": "2 flights + DG foyer 8.6 m²", "Windows": "15", "Bedrooms": "4 · 13.0 · 17.8 · 19.1 · 13.5", "Master suite (bed · dressing · bath)": "DG 13.5 · closet room 12.1 · 12.8", "Bathrooms": "DG bath · OG bath 4.7 (1 basin) · EG WC 3.1", "Living · dining · kitchen": "60.0 m² open hall", "Utility": "none drawn", "Planning status": "the current design; the set-back storey counts toward the GFZ as in the approved sheet", "Altkönigstraße brief": "4 bedrooms, but no en suite at the EG bedroom, OG bath with one basin, no HWR", "Verdict": "the baseline; its top floor wastes the suite"}),
 "rework": facts(**{"Storeys": "2 + set-back storey", "Plate per house": "as today", "Footprint · GRZ use (0.25 → 120.8 m²)": "91.5 m² · 76 %", "Gross floor area above ground": "242 m²", "Net floor area of the rooms": f"{n_rework:.0f} m²", "Wohnfläche, estimate": "186–192 m²", "Stairs": "as today", "Windows": "15", "Bedrooms": "4 · EG 10.3 · 17.8 · 19.1 · DG 16.5", "Master suite (bed · dressing · bath)": "DG 16.5 · 10.5 · 11.3 (option A)", "Bathrooms": "DG bath 11.3 · family bath 12.1 with WC room · guest bath 4.5", "Living · dining · kitchen": "46.7 m² + hall 11.6", "Utility": "laundry column in the family bath", "Planning status": "partition changes inside the approved envelope; no facade or stack change in A, O1, E1", "Altkönigstraße brief": "4 bedrooms, 2 full baths with two basins, guest bath; EG bedroom without en suite; no HWR", "Verdict": "the best three-storey house: build A, O1, E1"}),
 "reworkB": facts(**{"Storeys": "2 + set-back storey", "Plate per house": "as today", "Footprint · GRZ use (0.25 → 120.8 m²)": "91.5 m² · 76 %", "Gross floor area above ground": "242 m²", "Net floor area of the rooms": f"{n_B:.0f} m²", "Wohnfläche, estimate": "186–192 m²", "Stairs": "as today", "Windows": "14 (one DG window infilled)", "Bedrooms": "4 · EG 10.3 · 17.8 · 19.1 · DG 17.1", "Master suite (bed · dressing · bath)": "DG 17.1 · 9.1 · 12.1 (option B)", "Bathrooms": "as the rework", "Living · dining · kitchen": "46.7 m² + hall 11.6", "Utility": "as the rework", "Planning status": "B moves a bath stack and infills a window: facade change, permit", "Altkönigstraße brief": "as the rework", "Verdict": "scores 3.75 of 5 against A's 4.30: bath as the hub, bedroom reached through it"}),
 "reworkC": facts(**{"Storeys": "2 + set-back storey", "Plate per house": "as today", "Footprint · GRZ use (0.25 → 120.8 m²)": "91.5 m² · 76 %", "Gross floor area above ground": "242 m²", "Net floor area of the rooms": f"{n_C:.0f} m²", "Wohnfläche, estimate": "186–192 m²", "Stairs": "as today", "Windows": "15", "Bedrooms": "4 · EG 10.3 · 17.8 · 19.1 · DG 14.6", "Master suite (bed · dressing · bath)": "DG 14.6 · 12.1 · 11.5 (option C)", "Bathrooms": "as the rework", "Living · dining · kitchen": "46.7 m² + hall 11.6", "Utility": "as the rework", "Planning status": "one partition, two swing doors; bath stack moves east", "Altkönigstraße brief": "as the rework", "Verdict": "scores 3.40: the bath takes the two-window corner the bedroom should have"}),
 "reworkO2": facts(**{"Storeys": "2 + set-back storey", "Plate per house": "as today", "Footprint · GRZ use (0.25 → 120.8 m²)": "91.5 m² · 76 %", "Gross floor area above ground": "242 m²", "Net floor area of the rooms": f"{n_O2:.0f} m²", "Wohnfläche, estimate": "186–192 m²", "Stairs": "as today", "Windows": "15 (two OG windows moved)", "Bedrooms": "4 + study · EG 10.3 · 17.8 · 19.1 · DG 16.5", "Master suite (bed · dressing · bath)": "DG 16.5 · 10.5 · 11.3", "Bathrooms": "DG bath · two 3.4 m² en suites with closets · guest bath 4.5", "Living · dining · kitchen": "46.7 m² + hall 11.6", "Utility": "laundry closet on the landing", "Planning status": "two OG windows move 0.5 m: facade change, permit", "Altkönigstraße brief": "as the rework, with en suites instead of a family bath", "Verdict": "scores 3.45 against O1's 4.05: hotel bays, but no bath with two basins"}),
 "t1": facts(**{"Storeys": "2", "Plate per house": "8.29 × 11.04", "Footprint · GRZ use (0.25 → 120.8 m²)": "91.5 m² · 76 %", "Gross floor area above ground": "183 m²", "Net floor area of the rooms": f"{n_t1:.0f} m²", "Wohnfläche, estimate": "about 143 m²", "Stairs": "1 flight 1.0 × 4.05", "Windows": "9", "Bedrooms": "3 · 14.5 · 12.2 · 14.5", "Master suite (bed · dressing · bath)": "OG 14.5 · 6.6 · 7.9", "Bathrooms": "master bath 7.9 · family bath 6.2 (2 basins) · guest shower bath 4.0", "Living · dining · kitchen": "49.6 m² + 9.6 reading nook", "Utility": "4.8 m² with heat pump, W+D", "Planning status": "no change of plate; nothing to approve beyond today's design", "Altkönigstraße brief": "fails: three bedrooms, no EG bedroom, 143 m²", "Verdict": "the reference for two storeys without growing"}),
 "t4": facts(**{"Storeys": "2 + WU basement", "Plate per house": "8.29 × 14.07", "Footprint · GRZ use (0.25 → 120.8 m²)": "116.6 m² · 97 %", "Gross floor area above ground": "233 m² (+117 below)", "Net floor area of the rooms": f"{n_t4:.0f} m² (+{n_t4k:.0f} below)", "Wohnfläche, estimate": "about 189 m²", "Stairs": "1 flight + cellar flight under it", "Windows": "10", "Bedrooms": "4 · EG 14.2 incl. its bay · 13.4 · 15.9 · master 14.9", "Master suite (bed · dressing · bath)": "OG 14.9 · 8.4 two-sided · 17.5 with WC room", "Bathrooms": "master bath 17.5 · family bath 9.7 with tub · EG en suite 3.8 · guest WC 2.1", "Living · dining · kitchen": "40.7 m² + 21.2 lounge, 3.6 m glass wall", "Utility": "basement: laundry 14.9, plant 7.8, stores 35, hobby 24; laundry closet upstairs", "Planning status": "97 % of GRZ and GFZ; depth capped by the 3.00 m Abstandsfläche at the east rear corner; side Baugrenzen and Vollgeschosse to confirm; WU basement in pressing water", "Altkönigstraße brief": "all items; 189 of 190 m²; corrected after the independent review", "Verdict": "build this if 190 m² is the target"}),
 "t4v": facts(**{"Storeys": "2 + WU basement", "Plate per house": "8.29 × 13.07, west half 1.93 m further south", "Footprint · GRZ use (0.25 → 120.8 m²)": "108.4 m² · 90 %", "Gross floor area above ground": "217 m² (+108 below)", "Net floor area of the rooms": f"about {n_t4*13.07/14.07:.0f} m²", "Wohnfläche, estimate": "about 176 m²", "Stairs": "as T4", "Windows": "10 + a side window per half", "Bedrooms": "4, as T4 with 1.0 m shorter south rooms", "Master suite (bed · dressing · bath)": "as T4, 1.0 m shorter", "Bathrooms": "as T4", "Living · dining · kitchen": "as T4, 1.0 m shorter, east or west side window", "Utility": "as T4", "Planning status": "as T4 plus the Gestaltung rules on offset halves; east rear corner 3.25 m clear", "Altkönigstraße brief": "all items; 176 of 190 m²", "Verdict": "build this if the garden should feel private and the stair have daylight"}),
 "t5": facts(**{"Storeys": "2 + WU basement", "Plate per house": "8.29 × 14.07", "Footprint · GRZ use (0.25 → 120.8 m²)": "116.6 m² · 97 %", "Gross floor area above ground": "233 m² (+117 below)", "Net floor area of the rooms": f"{n_t5:.0f} m² (+{n_t5k:.0f} below)", "Wohnfläche, estimate": "about 186 m²", "Stairs": "1 straight flight across the house, parallel to the street; cellar flight under it", "Windows": "11 incl. the gallery window", "Bedrooms": "4 · EG 12.0 · 13.2 · 14.8 · master 30.0 with sitting area", "Master suite (bed · dressing · bath)": "OG 30.0 · 6.0 · 8.9, bath and dressing in one band", "Bathrooms": "master bath 8.9 · family bath 8.8 with tub and W+D · EG en suite 3.8 · guest WC 2.4", "Living · dining · kitchen": "45.3 m² in one room behind the open stair, kitchen east, 3.6 m glass wall", "Utility": "13 m² mudroom-pantry (HWR) with the garage door; basement laundry 14.8, plant 13.2, stores 29, hobby 26", "Planning status": "as T4", "Altkönigstraße brief": "all items; HWR above ground; 186 of 190 m²", "Verdict": "the Rötha plan on this plate: daylit gallery and one wide living room, smaller master bath"}),
 "t2": facts(**{"Storeys": "2", "Plate per house": "10.29 × 12.04", "Footprint · GRZ use (0.25 → 120.8 m²)": "123.9 m² · 103 %", "Gross floor area above ground": "248 m²", "Net floor area of the rooms": f"{n_t2:.0f} m²", "Wohnfläche, estimate": "about 190 m²", "Stairs": "1 flight", "Windows": "11", "Bedrooms": "4 + study · EG 19.1 · 16.8 · 18.2 · 18.0", "Master suite (bed · dressing · bath)": "EG 19.1 · 9.4 · 10.2", "Bathrooms": "master 10.2 · family 7.4 with tub · guest shower bath 4.0", "Living · dining · kitchen": "48.5 m², terrace to the east", "Utility": "5.4 m² + laundry upstairs 3.3", "Planning status": "not buildable here: 2.0 m too wide for the boundary garages, 3 m² over the GRZ", "Altkönigstraße brief": "all items on paper", "Verdict": "study only; its ideas went into T4"}),
 "t3": facts(**{"Storeys": "2 + basement", "Plate per house": "12.29 × 12.04", "Footprint · GRZ use (0.25 → 120.8 m²)": "148 m² · 122 %", "Gross floor area above ground": "296 m² (+148 below)", "Net floor area of the rooms": f"{n_t3:.0f} m² (+{n_t3k:.0f} below)", "Wohnfläche, estimate": "about 183 m²", "Stairs": "1 flight + cellar flight", "Windows": "14", "Bedrooms": "4 + study + family room", "Master suite (bed · dressing · bath)": "EG 15.4 · 7.3 · 9.8", "Bathrooms": "master 9.8 · family 11.2 · shower room 3.9 · guest WC 2.2", "Living · dining · kitchen": "81 m² across the garden front", "Utility": "basement", "Planning status": "not buildable here: 27 m² over the GRZ, 4 m too wide", "Altkönigstraße brief": "all items on paper", "Verdict": "study only; drawn for an assumed 370 m² half-plot"}),
}

# ---- index tables
def idx_rows():
    rows = []
    for cid, c in CONFIGS.items():
        f = FACTS[cid]
        rows.append([f'<b>{c["label"]}</b>', f["Storeys"], f["Plate per house"], f["Footprint · GRZ use (0.25 → 120.8 m²)"], f["Wohnfläche, estimate"], f["Bedrooms"], f["Master suite (bed · dressing · bath)"], f["Altkönigstraße brief"],
                     f'<a class="btn" href="#version/{cid}">View</a> <button class="btn" data-cmp="{cid}">Compare</button> <a class="btn btn-link" href="{c["read"]}">Read</a>'])
    return rows
index_html = table(["Version", "Storeys", "Plate", "Footprint · GRZ", "Wohnfläche", "Bedrooms", "Master suite", "Brief", ""], idx_rows(), cls="idx")
floor_rows = [
 ["Top floor A", "hotel sequence foyer → dressing → bedroom, bath off the foyer", "16.5 · 10.5 · 11.3", "#:4.30", "build", '<a class="btn btn-link" href="#read/opt-A">Read</a>'],
 ["Top floor B", "bath as the hub, one window infilled", "17.1 · 9.1 · 12.1", "#:3.75", "no", '<a class="btn btn-link" href="#read/opt-B">Read</a>'],
 ["Top floor C", "bath in the two-window corner", "14.6 · 12.1 · 11.5", "#:3.40", "no", '<a class="btn btn-link" href="#read/opt-C">Read</a>'],
 ["Upper floor O1", "family bath 12.1 with WC room, wardrobe walls, laundry", "bedrooms 17.8 · 19.1", "#:4.05", "build", '<a class="btn btn-link" href="#read/opt-O1">Read</a>'],
 ["Upper floor O2", "two 3.4 m² en suites, study, two windows moved", "bedrooms 17.8 · 19.1", "#:3.45", "no", '<a class="btn btn-link" href="#read/opt-O2">Read</a>'],
 ["Ground floor E1", "guest bath 4.5 off the hall, 1.17 m corridor, slim wardrobe", "bedroom 10.3 · living 46.7", "#:—", "build", '<a class="btn btn-link" href="#read/opt-E1">Read</a>'],
]
floors_html = table(["Floor option (three-storey house)", "Idea", "Rooms m²", "Score / 5", "Advice", ""], floor_rows, cls="idx")

chips = "".join(f'<button class="chip" data-id="{cid}" data-group="{c["group"]}">{c["label"]}</button>' for cid, c in CONFIGS.items())
cfg_json = json.dumps({cid: dict(label=c["label"], levels=c["levels"], read=c["read"]) for cid, c in CONFIGS.items()}, ensure_ascii=False)
facts_json = json.dumps(FACTS, ensure_ascii=False); rows_json = json.dumps(ROWS, ensure_ascii=False); levels_json = json.dumps(LEVELS)

NAV_CSS = r"""
<style>
.topnav{position:sticky;top:0;z-index:20;background:var(--paper);border-bottom:1px solid var(--line);padding:10px 16px;display:flex;gap:8px;align-items:center;flex-wrap:wrap}
.topnav .brand{font-family:var(--display);font-weight:600;font-size:15px;margin-right:auto;color:var(--ink)}
.tab{font:600 13px/1 var(--mono);letter-spacing:.04em;text-transform:uppercase;padding:9px 13px;border:1px solid var(--line);border-radius:999px;background:var(--paper2);color:var(--ink);cursor:pointer}
.tab[aria-selected="true"]{background:var(--ink);color:var(--paper);border-color:var(--ink)}
.view{display:none}.view.on{display:block}
.btn{font:500 12px/1 var(--mono);padding:6px 9px;border:1px solid var(--line);border-radius:6px;background:var(--paper2);color:var(--ink);cursor:pointer;text-decoration:none;display:inline-block;white-space:nowrap}
.btn:hover{border-color:var(--ink)}
.btn-link{background:transparent}
.tbl.idx td{vertical-align:top;font-size:13px}.tbl.idx td b{white-space:normal}
.chips{display:flex;flex-wrap:wrap;gap:8px;margin:12px 0 4px}
.chip{font:500 12.5px/1.2 var(--mono);padding:8px 11px;border:1px solid var(--line);border-radius:999px;background:var(--paper2);color:var(--ink);cursor:pointer;text-align:left}
.chip[data-group="study"]{opacity:.7}
.chip[aria-pressed="true"]{background:var(--accent);color:#fff;border-color:var(--accent)}
.cmp-note{font-size:13px;color:var(--muted);margin:4px 0 14px}
.cmp-grid{display:grid;gap:14px;align-items:start}
.cmp-grid figure{margin:0;background:var(--paper2);border:1px solid var(--line);border-radius:10px;padding:8px;min-width:0}
.cmp-grid figure svg{width:100%;height:auto;display:block}
.cmp-lvl{font:600 11px/1 var(--mono);letter-spacing:.08em;text-transform:uppercase;color:var(--muted);margin:16px 0 8px}
.cmp-grid .cap{font:500 12.5px/1.35 var(--mono);margin:0 0 6px;color:var(--ink)}
.cmp-grid .none{display:flex;align-items:center;justify-content:center;min-height:120px;color:var(--muted);font:500 12px var(--mono)}
.cmp-head{display:grid;gap:14px;margin:10px 0}
.cmp-head div{font:600 14px var(--display);color:var(--ink);padding:8px 10px;border-left:4px solid var(--accent);background:var(--paper2);border-radius:0 8px 8px 0}
.view-wrap{max-width:1100px;margin:0 auto;padding:18px 16px 40px}
.ver-head{font:600 22px var(--display);color:var(--ink);margin:6px 0 10px;letter-spacing:-.01em}
.ver-fig{margin:18px 0;background:var(--paper2);border:1px solid var(--line);border-radius:10px;padding:10px}
.ver-fig svg{width:100%;height:auto;display:block;max-width:940px;margin:0 auto}
.ver-fig figcaption{font-size:14px;line-height:1.5;color:var(--ink);padding:8px 4px 2px;max-width:none}
.ver-fig .cap{font:600 11px/1 var(--mono);letter-spacing:.08em;text-transform:uppercase;color:var(--muted);margin:0 0 6px}
#ver-select{max-width:100%}
@media (max-width:700px){.cmp-grid,.cmp-head{grid-template-columns:1fr !important}}
</style>
"""

JS = r"""
<script>
(function(){
const CONFIGS = %s, FACTS = %s, ROWS = %s, LEVELS = %s;
const MAX = 3;
let sel = [];
function $(s, r){ return (r||document).querySelector(s); }
function $$(s, r){ return Array.from((r||document).querySelectorAll(s)); }
function parseHash(){
  const h = location.hash.replace(/^#/, '');
  if (!h) return {view:'index'};
  const [view, rest] = h.split('/');
  if (view === 'compare') return {view, sel: rest ? rest.split('+').filter(k => CONFIGS[k]) : []};
  if (view === 'read') return {view, anchor: rest};
  if (view === 'version') return {view, id: CONFIGS[rest] ? rest : Object.keys(CONFIGS)[0]};
  return {view:'index'};
}
function setHash(view, extra){ const v = view + (extra ? '/' + extra : ''); if (location.hash !== '#' + v) history.replaceState(null, '', '#' + v); }
function showView(view){
  $$('.view').forEach(el => el.classList.toggle('on', el.id === 'view-' + view));
  $$('.tab').forEach(t => t.setAttribute('aria-selected', t.dataset.view === view ? 'true' : 'false'));
  window.scrollTo({top:0});
}
function renderCompare(){
  $$('.chip').forEach(c => c.setAttribute('aria-pressed', sel.includes(c.dataset.id) ? 'true' : 'false'));
  const n = sel.length, out = $('#cmp-out');
  if (!n){ out.innerHTML = '<p class="cmp-note">Pick up to three versions above.</p>'; return; }
  let h = '<div class="cmp-head" style="grid-template-columns:repeat(' + n + ',1fr)">' + sel.map(k => '<div>' + CONFIGS[k].label + '</div>').join('') + '</div>';
  // facts table
  h += '<div class="tbl"><table><thead><tr><th></th>' + sel.map(k => '<th>' + CONFIGS[k].label.split(' · ')[0] + '</th>').join('') + '</tr></thead><tbody>';
  ROWS.forEach(r => { h += '<tr><td>' + r + '</td>' + sel.map(k => '<td>' + (FACTS[k][r] || '—') + '</td>').join('') + '</tr>'; });
  h += '</tbody></table></div>';
  // plans by level
  LEVELS.forEach(lvl => {
    if (!sel.some(k => CONFIGS[k].levels[lvl])) return;
    h += '<div class="cmp-lvl">' + lvl + '</div><div class="cmp-grid" style="grid-template-columns:repeat(' + n + ',1fr)">';
    sel.forEach(k => {
      const key = CONFIGS[k].levels[lvl];
      if (!key){ h += '<figure><div class="none">no plan at this level</div></figure>'; return; }
      const src = document.getElementById('svg-' + key);
      const cap = src ? (src.getAttribute('aria-label') || key) : key;
      h += '<figure><p class="cap">' + cap + '</p>' + (src ? src.outerHTML.replace(/ id="svg-[^"]+"/, '') : '') + '</figure>';
    });
    h += '</div>';
  });
  h += '<p class="cmp-note">Plans at one scale per level; the scale bar on each drawing is 2 m. Read the full text of a version through its Read button on the Index.</p>';
  out.innerHTML = h;
}
let cur = Object.keys(CONFIGS)[0];
function renderVersion(){
  const c = CONFIGS[cur], out = $('#ver-out');
  $('#ver-select').value = cur;
  let h = '<div class="ver-head">' + c.label + '</div>';
  h += '<div class="tbl"><table><tbody>' + ROWS.map(r => '<tr><td>' + r + '</td><td>' + (FACTS[cur][r] || '—') + '</td></tr>').join('') + '</tbody></table></div>';
  LEVELS.forEach(lvl => {
    const key = c.levels[lvl]; if (!key) return;
    const src = document.getElementById('svg-' + key); if (!src) return;
    const fig = src.closest('figure'); const fc = fig ? fig.querySelector('figcaption') : null;
    h += '<figure class="ver-fig"><p class="cap">' + lvl + ' · ' + (src.getAttribute('aria-label') || key) + '</p>' + src.outerHTML.replace(/ id="svg-[^"]+"/, '') + (fc ? '<figcaption>' + fc.innerHTML + '</figcaption>' : '') + '</figure>';
  });
  h += '<p class="cmp-note"><a class="btn" href="' + c.read + '">Read the full text of this version</a> <a class="btn" href="#compare/' + cur + '">Compare it with others</a></p>';
  out.innerHTML = h;
}
function route(){
  const p = parseHash();
  if (p.view === 'version'){ cur = p.id; renderVersion(); showView('version'); return; }
  if (p.view === 'compare'){ if (p.sel) sel = p.sel.slice(0, MAX); renderCompare(); showView('compare'); try{ localStorage.setItem('mdm-cmp', JSON.stringify(sel)); }catch(e){} }
  else if (p.view === 'read'){ showView('read'); if (p.anchor){ const el = document.getElementById(p.anchor); if (el) setTimeout(() => el.scrollIntoView({block:'start'}), 30); } }
  else showView('index');
}
document.addEventListener('click', e => {
  const tab = e.target.closest('.tab'); if (tab){ e.preventDefault(); if (tab.dataset.view === 'compare') setHash('compare', sel.join('+')); else if (tab.dataset.view === 'version') setHash('version', cur); else setHash(tab.dataset.view); route(); return; }
  const cmp = e.target.closest('[data-cmp]'); if (cmp){ e.preventDefault(); const id = cmp.dataset.cmp; if (!sel.includes(id)){ sel.push(id); if (sel.length > MAX) sel.shift(); } setHash('compare', sel.join('+')); route(); return; }
  const chip = e.target.closest('.chip'); if (chip){ const id = chip.dataset.id; if (sel.includes(id)) sel = sel.filter(x => x !== id); else { sel.push(id); if (sel.length > MAX) sel.shift(); } setHash('compare', sel.join('+')); renderCompare(); return; }
  const clr = e.target.closest('#cmp-clear'); if (clr){ sel = []; setHash('compare'); renderCompare(); return; }
});
document.addEventListener('change', e => { if (e.target.id === 'ver-select'){ setHash('version', e.target.value); route(); } });
document.addEventListener('click', e => {
  const ids = Object.keys(CONFIGS); const i = ids.indexOf(cur);
  if (e.target.closest('#ver-prev')){ setHash('version', ids[(i - 1 + ids.length) %% ids.length]); route(); }
  if (e.target.closest('#ver-next')){ setHash('version', ids[(i + 1) %% ids.length]); route(); }
});
$('#ver-select').innerHTML = Object.keys(CONFIGS).map(k => '<option value="' + k + '">' + CONFIGS[k].label + '</option>').join('');
window.addEventListener('hashchange', route);
try{ const s = JSON.parse(localStorage.getItem('mdm-cmp') || '[]'); if (Array.isArray(s)) sel = s.filter(k => CONFIGS[k]).slice(0, MAX); }catch(e){}
if (!location.hash && sel.length === 0) sel = ['today','t4'];
route();
})();
</script>
"""

page = f"""{head_part}{NAV_CSS}
<nav class="topnav" aria-label="Views"><span class="brand">Altkönigstraße 122 · floor plan review</span>
<button class="tab" data-view="index" aria-selected="true">Index</button><button class="tab" data-view="version" aria-selected="false">Version</button><button class="tab" data-view="compare" aria-selected="false">Compare</button><button class="tab" data-view="read" aria-selected="false">Full review</button></nav>
<section id="view-index" class="view on"><div class="view-wrap">
<div class="col"><p class="eyebrow">Seventh edition · 12 October 2026</p>
<h1>Every version at a glance</h1>
<p class="lede">Eleven whole-house versions and six floor options, drawn to one scale and checked by the same geometry script; T4 and T5 carry the corrections from the independent review of T4 (one blocker, one geometry error, about twenty should-fix items, all closed). Pick versions with <b>Compare</b> to see their plans side by side with a facts table, or open the full text with <b>Read</b>. The envelope for the two-storey versions is the Altkönigstraße 122 briefing: 966.6 m² for the mirrored pair, GRZ 0.25, GFZ 0.50, Baufenster 5.00 to 20.00 m behind the street, boundary garages beside the front of each house.</p></div>
{index_html}
<div class="col"><h3>Floor options for the three-storey house</h3><p class="small">These swap one floor of today's design; the whole-house rows above combine them. Scores are the decision matrices from the review (layout, hotel benchmark, rules, cost, risk).</p></div>
{floors_html}
<div class="col"><p class="small">Net floor areas are the clear areas of the rooms as drawn; the Wohnfläche figures are estimates after WoFlV without terraces. The three earlier studies T2 and T3 stay listed because their ideas carried into T4, but they do not fit this plot.</p></div>
</div></section>
<section id="view-version" class="view"><div class="view-wrap">
<div class="col"><h2 style="margin-top:0">One version</h2><p class="small">Pick a version; its plans follow at full width with their captions, and the facts above them. <button class="btn" id="ver-prev">◀ previous</button> <select id="ver-select" class="btn"></select> <button class="btn" id="ver-next">next ▶</button></p></div>
<div id="ver-out"></div>
</div></section>
<section id="view-compare" class="view"><div class="view-wrap">
<div class="col"><h2 style="margin-top:0">Compare</h2><p class="small">Up to three versions. Plans appear level by level at one scale; the facts table reads across. <button class="btn" id="cmp-clear">Clear</button></p></div>
<div class="chips">{chips}</div>
<div id="cmp-out"></div>
</div></section>
<section id="view-read" class="view">
{read_body}
</section>
{JS % (cfg_json, facts_json, rows_json, levels_json)}"""
open("artifact.html", "w").write(page)
link_end = page.index('>', page.index('<link')) + 1
doc = ('<!DOCTYPE html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
       + page[:link_end] + '</head><body>' + page[link_end:] + '</body></html>')
open("index.html", "w").write(doc)
print(len(page), "chars; configs", len(CONFIGS))
