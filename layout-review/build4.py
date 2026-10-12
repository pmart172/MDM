"""Fourth edition: adds the two-storey version (T1 same plate, T2 master down) in front of the three-storey review."""
import build3, floors2, floors3, floors
from build3 import table, OK, WARN, BAD, LEGEND, n

plans2 = {k: f() for k, f in list(floors2.ALL.items()) + list(floors3.ALL.items())}
issues2 = {k: p.check() for k, p in plans2.items()}
svg2 = {k: p.svg() for k, p in plans2.items()}

def fig2(key, caption): return f'</div>\n<div class="one"><figure>{svg2[key]}<figcaption>{caption}</figcaption></figure></div>\n<div class="col">'
def net(keys): return sum(v[4] for k in keys for v in (build3.plans if k in build3.plans else plans2)[k].rooms.values())
def rooms(key):
    p = plans2[key]; rows = []
    for name, (x0, y0, x1, y1, a) in p.rooms.items():
        rows.append([name, f"#:{a:.1f}", f"#:{x1-x0:.2f} × {y1-y0:.2f}"])
    rows.append([f"!net floor area", f"#:{sum(v[4] for v in p.rooms.values()):.1f}", ""])
    return table(["Room", "m²", "clear size (m)"], rows)
def clear2(key):
    p = plans2[key]; rows = []
    for (room, label, facing, dep, mn, cf) in p.clearances:
        status = OK("comfort") if dep >= cf-0.005 else (WARN("above minimum") if dep >= mn-0.005 else BAD("below minimum"))
        rows.append([room, label, facing, f"#:{min(dep,3):.2f}", f"#:{mn:.2f} / {cf:.2f}", status])
    return table(["Room", "Fixture", "Free side", "Free depth m", "VDI min / comfort", "Status"], rows)

cur_net = net(["eg_current", "og_current", "dg_current"]); t1_net = net(["t1_eg", "t1_og"]); t2_net = net(["t2_eg", "t2_og"]); t3_net = net(["t3_eg", "t3_og"]); t3_kg_net = net(["t3_kg"])
cur_gross = 8.29*11.04*2 + 7.13*8.20; t1_gross = 8.29*11.04*2; t2_gross = 10.29*12.04*2; t3_gross = 12.29*12.04*2

section = f"""
<div class="col">
<h2 id="two">0 · Two storeys instead of three</h2>
<p>You asked for a two-storey version: one stair instead of two, no set-back storey, fewer windows, and the master suite downstairs if the dressing and bath can be made properly. Two options are drawn below. <b>T1</b> keeps your plate of 8.29 × 11.04 m exactly, so the Baufenster question does not arise; the master suite goes upstairs because the plate cannot hold the living room, the guest bath and a full master suite on one floor. <b>T2</b> enlarges the plate to 10.29 × 12.04 m, which is the size at which a garden-side master suite with a 10 m² bath and a two-sided 9 m² dressing fits beside a 48 m² living room whose furniture still has real walkways; its gross floor area is about that of today's three storeys. T2 only works if your Baufenster, the site-coverage ratio (GRZ) and the distance to the east boundary allow a plate 2.0 m wider and 1.0 m deeper; those three numbers decide between the two options, and I do not have them. <b>T3</b>, added on your note that the plot's GRZ and GFZ may be used to the full and that a basement stays, is the version at the limit: it is drawn for a 370 m² half-plot at GRZ 0.4 and GFZ 0.8 (plate 12.29 × 12.04 m) with a full basement, and because the utility, laundry and stores go down, the ground floor can give the living room the whole garden front and still keep the master suite downstairs.</p>
{table(["", "Today, 3 storeys", "T1 · same plate", "T2 · master down", "T3 · limit + basement"], [
 ["Plate (outside)", "8.29 × 11.04 · DG 7.13 × 8.20", "8.29 × 11.04", "10.29 × 12.04", "12.29 × 12.04 + basement"],
 ["Gross floor area", f"#:{cur_gross:.0f} m²", f"#:{t1_gross:.0f} m²", f"#:{t2_gross:.0f} m²", f"#:{t3_gross:.0f} m² + 148 below"],
 ["Net floor area (sum of rooms, incl. landings)", f"#:{cur_net:.0f} m²", f"#:{t1_net:.0f} m²", f"#:{t2_net:.0f} m²", f"#:{t3_net:.0f} m² + {t3_kg_net:.0f} below"],
 ["Net ÷ gross", f"#:{cur_net/cur_gross:.0%}", f"#:{t1_net/t1_gross:.0%}", f"#:{t2_net/t2_gross:.0%}", f"#:{t3_net/t3_gross:.0%}"],
 ["Stairs", "2 flights + DG foyer", "1 flight, 1.0 × 4.05 m", "1 flight, 1.0 × 4.05 m", "1 flight + cellar flight stacked under it"],
 ["Windows (openings, excl. entrance)", "#:15", "#:9", "#:11", "#:14"],
 ["Bedrooms", "4 (13.0 · 17.8 · 19.1 · 13.5)", "3 (14.5 · 12.2 · 14.5)", "4 (19.1 · 16.8 · 18.2 · 18.0) + study", "4 (15.4 · 15.9 · 15.6 · 18.0) + study + TV room"],
 ["Master suite", "DG: bed 13.5 · closet 12.1 · bath 12.8", "OG: bed 14.5 · dressing 6.6 · bath 7.9", "EG: bed 19.1 · dressing 9.4 · bath 10.2", "EG: bed 15.4 · dressing 7.3 · bath 9.8"],
 ["Bathrooms", "DG bath · OG bath (1 basin) · EG WC", "master bath · family bath 2 basins · guest shower bath", "master bath · family bath with tub · guest shower bath", "master bath · family bath 11.2 with tub · shower room · guest WC"],
 ["Utility / laundry", "none drawn", "4.8 m² with heat pump, W+D", "5.4 m² with heat pump, W+D, plus a 3.3 m² laundry upstairs", "basement: plant 7.6 · laundry 7.5 · stores 41 · hobby 15.6 · guest/office 24.7"],
])}
<p class="small">Net areas are the clear floor areas of the rooms as drawn (landings and open-plan zones included, walls and the stair flight excluded); today's figures use your three plans as scaled. The gross figure for today counts the set-back storey at its own 7.13 × 8.20 m plate.</p>

<h3>What the two-storey house gains</h3>
<ul>
<li><b>One stair.</b> Today the stair appears three times (EG, OG, DG arrival) and the DG foyer alone is 8.6 m². T1 and T2 have one straight flight on the party wall, 1.0 × 4.05 m, 15 risers of 19.3 cm with 27 cm goings for a 2.90 m storey, and a landing that doubles as the upper hall.</li>
<li><b>No set-back storey.</b> The DG's 58.5 m² plate yields 47 m² of rooms and is ringed by roof strips you can only use from a door that does not exist yet; two full storeys put every square metre under a usable ceiling.</li>
<li><b>Fewer windows.</b> Nine openings in T1 and eleven in T2 instead of fifteen: the dressing rooms, the guest bath, the utility and the T1 family bath are internal and mechanically ventilated (the Hessische Bauordnung allows this), the kitchen gets one high-sill window, and the bedrooms get one each. Fewer, larger openings also help the wall-to-window ratio on a north facade.</li>
<li><b>Stacked plumbing.</b> In both options the guest bath sits under the landing wall and the utility under the family bath wall, so soil stacks run in two partitions rather than four.</li>
</ul>

<h3>Option T1 · same plate, master suite upstairs</h3>
{fig2("t1_eg", "<b>T1 ground floor.</b> Entrance hall with a 1.5 m wardrobe backing onto the kitchen's pantry column; guest shower bath (door hinged so the open leaf screens the WC from the hall) and utility (heat pump, buffer tank, washer-dryer against the bath wall) in the strip beside the stair; kitchen run 4.2 m on the north wall, hob clear of the window, with the 2.4 × 1.2 m island; dining table at the east window; the two 2 × 1 m sofas in the south end facing the 3.0 m lift-slide door to the terrace, TV on a low divider; the south-west nook behind the utility becomes a reading corner with a desk under its own window.")}
{fig2("t1_og", "<b>T1 upper floor.</b> The landing is the stair head plus a shelf; a 1.0 × 1.0 m linen cupboard sits over the hall. Two children's rooms to the north, each with the bed on a solid wall away from the stair, a desk centred under the window and a wardrobe on the landing wall. Family bath with a double vanity (basins 0.73 m apart), shower and WC, lit from the east through a window kept clear of the shower. Master suite to the south: landing → dressing (2.9 m rail plus a 1.0 m end wardrobe, door opening inward) → bedroom, with the bath off the dressing through a swing door so the WC wall carries no pocket cavity. The bed's headboard is on the 4.15 m party wall; the door is at the foot end and visible from the bed; the lane past the dresser is 1.10 m.")}
{rooms("t1_og")}
</div>
{LEGEND}
<div class="col">
<p>T1 meets every rule on the list except that the plate has to be shared: the children's rooms are 12.2 and 14.5 m² instead of today's 17.8 and 19.1 m², the master bath is 7.9 m² (tub 1.70, shower 1.2 × 1.0, double vanity 1.45) rather than the 10–12 m² a hotel suite would have, and the ground floor has no spare bedroom. That is the honest capacity of 2 × 79.6 m² of clear floor: a 10 m² master bath plus a family bath with two basins plus two 15 m² children's rooms plus a 6 m² dressing does not fit on one 79.6 m² storey with the landing and the stair, and I would rather show you the real sizes than squeeze them. Two upgrades cost nothing in plan: a rooflight over the stair head, which is the only way to light the landing, and, if you want the bigger bath, 0.20 m taken from the bedroom's width (3.50 → 3.30 m; its 4.15 m headboard wall is unaffected) and given to the bath.</p>

<h3>Option T2 · 10.29 × 12.04 m plate, master suite on the ground floor</h3>
{fig2("t2_eg", "<b>T2 ground floor.</b> Same entrance strip as T1 (hall, guest shower bath, utility). Kitchen run 5.6 m plus a fridge-and-oven column at the east end, the island, the dining table by the east window and the two sofas around the TV; the 1.0 m lane east of the table leads to the terrace door, which is on the east wall because the whole south band is the master suite. The suite door sits at the end of the free strip that runs from the hall past the utility, so nobody crosses the living room to reach it, and it opens into the dressing. The suite reads like a hotel bay: living → dressing (two 2.3 m rails, a 1.1 m end wardrobe, 1.10 m aisle) → bedroom, with the bath off the dressing through a pocket door that opens onto free floor. Bath 10.2 m²: tub under the south window, 1.2 × 1.2 shower in the north-west corner, 1.5 m double vanity on the party wall, WC on the dressing wall between the door and the tub. Bedroom 19.1 m² with the bed on the solid 4.08 m east wall (no window behind the headboard), garden window, bench, dresser and a desk. The wall between the living room and the suite is specified as a 0.25 m double-stud acoustic wall; the TV hangs on it, so that matters.")}
{fig2("t2_og", "<b>T2 upper floor.</b> Two children's rooms of 16.8 and 18.2 m², a family bath with tub, shower, double vanity and WC (its door opens outward, hinged so the leaf folds away from the bedroom door), a third bedroom or guest room of 18.0 m², a 17.4 m² study that doubles as the TV room (TV on the laundry wall, day bed opposite, wardrobe against the bath wall), a 3.3 m² laundry and a linen cupboard over the hall. The landing is 12.2 m² including the stair head; a rooflight over the stair is the one thing it lacks.")}
{rooms("t2_eg")}
{rooms("t2_og")}
<p>T2 is the version in which the master suite is actually nicer than any of the three top-floor options: the bath is a true five-fixture room with daylight, the dressing is a two-sided walk-in with 5.7 m of rail, and the bedroom is 19 m² with a garden window. The price is 32 m² more plate per storey and a living room that opens east rather than south. If your garden is to the south and the plot has no usable east side, the living band and the suite band can be swapped (suite north, living south) only by moving the entrance to the east wall, which needs a side path of at least 1.2 m; tell me the plot and I will draw that variant.</p>


<h3>Option T3 · the plot's limit, two storeys plus basement</h3>
<p>What "the maximum" means for a two-storey house with a basement, in the terms of the BauNVO and the Hessische Bauordnung (HBO): the <b>GRZ</b> (Grundflächenzahl, §19 BauNVO) is the share of the plot the building may cover; the house's footprint counts in full, while garages, driveways and terraces may exceed the figure by up to 50 % (never beyond 0.8), so the house itself can normally use the whole GRZ. The <b>GFZ</b> (Geschossflächenzahl, §20 BauNVO) is the gross floor area of the full storeys divided by the plot area. A basement is not a full storey under the HBO when it does not have 2.30 m of clear height over at least two thirds of the floor area above the natural ground, in practice when it sits below ground, so it costs no GFZ unless your Bebauungsplan says it counts all storeys (§20 (3) BauNVO allows that). For two full storeys the footprint is therefore limited to the smaller of GRZ × plot and GFZ ÷ 2 × plot; with the usual pairing of GRZ 0.4 and GFZ 0.8 both limits coincide at 0.4 × plot. The plot is your half of the Doppelhaus plot. The Baufenster and the distance to the east boundary (0.4 H, at least 3 m under the HBO, which for two storeys with a flat roof is about 3 m) cap the plate independently, and the groundwater level decides whether the basement is sensible at all.</p>
{table(["Half-plot", "GRZ 0.4 → footprint", "Plate at 12.04 m depth", "What it buys over T2"], [
 ["#:280 m²", "#:112 m²", "9.3 × 12.04", "nothing: T2 (124 m²) is already over; build T1"],
 ["#:310 m²", "#:124 m²", "10.29 × 12.04", "T2 exactly"],
 ["#:340 m²", "#:136 m²", "11.3 × 12.04", "T3's parti with a 2.8 m bedroom bay: tight"],
 ["!#:370 m²", "#:148 m²", "12.29 × 12.04", "T3 as drawn: living room across the garden front, suite with daylight, basement"],
 ["#:400 m²", "#:160 m²", "13.3 × 12.04", "T3 with a 4.8 m bedroom and a two-sided dressing"],
])}
<p class="small">Footprints are the house only; the driveway, garage and terrace sit in the 50 % margin. If your GFZ is lower than twice the GRZ (for example GRZ 0.4 with GFZ 0.6), the GFZ binds and the footprint is GFZ ÷ 2 × plot. Send me the Bebauungsplan's three figures and the half-plot's size and I will re-cut T3 to the exact plate.</p>
{fig2("t3_eg", "<b>T3 ground floor, 12.29 × 12.04 m.</b> Entrance, main stair and the cellar flight (stacked under it, entered from a small lobby at the flight's south end next to the kitchen) on the party wall; guest WC and a 1.5 m wardrobe in the hall. The master suite runs along the north: bath 9.8 m² with the tub under an obscured street window, 1.6 m double vanity, 1.2 × 1.2 shower and WC; dressing 7.3 m² with a 2.8 m rail and a 1.2 m end wardrobe; bedroom 15.4 m² with the headboard on the solid north wall (no street window), an east window, bench, dresser and armchair, entered from the dressing at the foot end. The living room is 81 m² across the whole garden front: kitchen run 4.2 m on the party wall with the fridge column in the corner, 2.4 × 1.2 island, six-seat table under the suite wall, lounge in the south-east with the two sofas, TV on the east wall, a 3.0 m lift-slide door and two further south windows.")}
{fig2("t3_og", "<b>T3 upper floor.</b> Two children's rooms of 15.9 and 15.6 m² with beds on the partitions and desks under the windows, family bath 11.2 m² with tub, 1.6 m double vanity, 1.2 × 1.2 shower and WC, an 18.0 m² guest room, a 3.9 m² shower room, a 16.0 m² family room with the sofa and TV you asked for upstairs, a 16.9 m² study and a linen cupboard. The 21 m² landing is the price of the width; a rooflight over the stair turns it into the house's brightest spot.")}
{fig2("t3_kg", "<b>T3 basement.</b> Plant room (heat pump, buffer tank, electrics) and laundry next to the cellar hall, a food store, a hobby or fitness room with an east light well, a 24.7 m² guest room or office with a south light well, and 30 m² of general storage. The habitable rooms need 2.40 m of headroom and daylight through the light wells to count as Aufenthaltsräume.")}
{rooms("t3_eg")}
{rooms("t3_og")}
<p>T3 is the plan a 5-star planner would draw for this brief if the plot allows it: the garden belongs to the living room, the suite is private behind the entrance hall with its own daylight, every service function is below ground, and the upper floor has a full programme including the family room. Its master bedroom is the smallest of the three (15.4 m²) because the north band is shared four ways; the 400 m² row in the table above is where it grows to 4.8 m wide. The two things to decide before anyone draws further are the Bebauungsplan figures and the groundwater level.</p>
<h3>Which one</h3>
{table(["", "T1 · same plate", "T2 · master down", "T3 · limit + basement"], [
 ["Planning risk", "none beyond today's design: same plate, same height class minus the set-back storey", "needs Baufenster, GRZ and east Abstandsfläche (0.4 H, at least 3 m under the HBO) to allow 10.29 × 12.04", "needs the plot's full GRZ and GFZ, the Baufenster and a basement-friendly groundwater level; drawn for a 370 m² half-plot"],
 ["Master suite", "14.5 + 6.6 + 7.9 m², all rules met, bath on the small side", "19.1 + 9.4 + 10.2 m², hotel-grade, daylight in the bath", "15.4 + 7.3 + 9.8 m², daylight in the bath, suite at the street side"],
 ["Children", "12.2 and 14.5 m²", "16.8 and 18.2 m² plus an 18 m² third bedroom and a study", "15.9 and 15.6 m² plus an 18 m² guest room, study, family room and shower room"],
 ["Living", "49.6 m² + 9.6 m² reading nook, terrace to the south", "48.5 m², terrace to the east, garden belongs to the suite", "81 m² across the whole garden front, three south openings"],
 ["Cost direction", "cheapest version of all: fewest m², fewest windows, one stair", "about today's gross area, one stair, fewer windows, larger foundation and roof", "largest: 296 m² above ground plus a 148 m² basement"],
 ["Recommendation", "build this if the plate is fixed", "build this if the Baufenster allows it and you want the suite downstairs", "build this if the plot allows it: the only version where the living room and the suite both get what they need"],
])}
<details><summary>Free depth in front of every fixture, T1, T2 and T3 (VDI 6000)</summary>{clear2("t1_eg")}{clear2("t1_og")}{clear2("t2_eg")}{clear2("t2_og")}{clear2("t3_eg")}{clear2("t3_og")}</details>
<p class="small">All seven drawings pass the geometry script (no partition within 0.15 m of a window reveal, every room with a door inside a wall, no door swing onto a fixture, no overlaps, every fixture at or above the VDI minimum free depth). An independent architectural reviewer then read the rendered drawings against a defect checklist and the rules above and returned 47 items, three of them blockers (a wardrobe standing in front of the T2 bath door, the T2 headboard against a window, a study door reduced to 0.43 m by a wardrobe); every blocker and every should-fix item was corrected in the drawings you see, and the nits that were not drawn (rooflight, acoustic wall build-up, bath window sills) are stated in the captions.</p>
</div>
"""

html = build3.html
html = html.replace('<p class="eyebrow">Third edition', '<p class="eyebrow">Fourth edition · two-storey version added')
kv_old = html[html.index('<div class="kv">'):html.index('</div>\n\n<div class="col">', html.index('<div class="kv">')) + len('</div>')]
kv_new = ('<div class="kv">\n<div><b>T1 · same plate</b><span>two storeys on 8.29 × 11.04 m, one stair, 9 windows, master suite upstairs</span></div>\n'
          '<div><b>T2 · master down</b><span>10.29 × 12.04 m plate, garden-side suite with 10.2 m² bath and 9.4 m² walk-in dressing</span></div>\n<div><b>T3 · plot limit + basement</b><span>12.29 × 12.04 m for a 370 m² half-plot at GRZ 0.4: living across the garden front, suite north-east, services below ground</span></div>\n'
          '<div><b>DG · Option A</b><span>if the three-storey house stays: bedroom 16.5 m², two partitions, no facade change</span></div>\n'
          '<div><b>OG O1 · EG E1</b><span>12.1 m² family bath with WC room; 4.5 m² guest bath off the hall</span></div>\n</div>')
html = html.replace(kv_old, kv_new, 1)
assert '<div class="col">\n<h2 id="verdict">Verdict</h2>' in html
html = html.replace('<div class="col">\n<h2 id="verdict">Verdict</h2>', section + '<div class="col">\n<h2 id="verdict">Verdict on the three-storey plans</h2>', 1)
html = html.replace('<p class="lede">Nine plans drawn', '<p class="lede">Sixteen plans drawn', 1)
html = html.replace('the three floors as you drew them, three options for the top floor, two for the upper floor, one for the ground floor.', 'the three floors as you drew them, a two-storey version of the house in three options (same plate; a larger plate with the master suite downstairs; the plot limit with a basement), three options for the top floor, two for the upper floor, one for the ground floor.', 1)
open("artifact.html", "w").write(html)
link_end = html.index('>', html.index('<link')) + 1
doc = ('<!DOCTYPE html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
       + html[:link_end] + '</head><body>' + html[link_end:] + '</body></html>')
open("index.html", "w").write(doc)
print(len(html), "chars;", {k: len(v) for k, v in issues2.items()}, f"net cur {cur_net:.1f} t1 {t1_net:.1f} t2 {t2_net:.1f}")
