"""Fourth edition: adds the two-storey version (T1 same plate, T2 master down) in front of the three-storey review."""
import build3, floors2, floors3, floors4, floors, siteplan
from build3 import table, OK, WARN, BAD, LEGEND, n

plans2 = {k: f() for k, f in list(floors2.ALL.items()) + list(floors3.ALL.items()) + list(floors4.ALL.items())}
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

cur_net = net(["eg_current", "og_current", "dg_current"]); t1_net = net(["t1_eg", "t1_og"]); t2_net = net(["t2_eg", "t2_og"]); t3_net = net(["t3_eg", "t3_og"]); t3_kg_net = net(["t3_kg"]); t4_net = net(["t4_eg", "t4_og"]); t4_kg_net = net(["t4_kg"])
cur_gross = 8.29*11.04*2 + 7.13*8.20; t1_gross = 8.29*11.04*2; t2_gross = 10.29*12.04*2; t3_gross = 12.29*12.04*2; t4_gross = 8.29*14.07*2
site_svg, site_dist = siteplan.svg()
site_svg_v, site_dist_v = siteplan.svg(offset=1.93, depth=13.07)

section = f"""
<div class="col">
<h2 id="two">0 · Two storeys instead of three</h2>
<p>You asked for a two-storey version: one stair instead of two, no set-back storey, fewer windows, the plot's GRZ and GFZ used to the full, and a basement kept. The briefing for Altkönigstraße 122 gives the envelope: a 966.6 m² plot for the mirrored pair, GRZ 0.25 and GFZ 0.50 from the Bebauungsplan as applied in the approved Bauantrag, a Baufenster from 5.00 to 20.00 m behind the street, garages on the side boundaries beside the front part of each house, and the brief per house of four bedrooms (one on the ground floor with its own shower and WC), two full bathrooms plus a guest WC, 45 m² or more of open kitchen-dining-living, a dressing at the master bedroom, a utility room and about 190 m² of Wohnfläche. Two options are drawn to that envelope. <b>T1</b> keeps today's plate of 8.29 × 11.04 m and shows what two storeys give without growing. <b>T4</b> is the maximum: the garages fix the width at 8.29 m, so the house grows in depth to 14.07 m, the last 0.5 m of the allowed 120.8 m² being blocked by the 3 m Abstandsfläche at the east rear corner, and the utility goes into a WU basement. Two earlier studies, T2 and T3, were drawn before the briefing arrived and are kept at the end of the section for the record; neither fits this plot.</p>
{table(["", "Today, 3 storeys", "T1 · same plate", "T4 · plot maximum + basement"], [
 ["Plate (outside)", "8.29 × 11.04 · DG 7.13 × 8.20", "8.29 × 11.04", "8.29 × 14.07 + WU basement"],
 ["Gross floor area per house", f"#:{cur_gross:.0f} m²", f"#:{t1_gross:.0f} m²", f"#:{t4_gross:.0f} m² + 117 below"],
 ["GRZ use (0.25 → 120.8 m² per house, garages outside)", "#:91.5 m² · 76 %", "#:91.5 m² · 76 %", "#:116.6 m² · 97 %"],
 ["GFZ use (0.50 → 241.7 m² per house)", "#:218 m² with the DG · 90 %", "#:183 m² · 76 %", "#:233 m² · 97 %"],
 ["Net floor area (rooms incl. landings)", f"#:{cur_net:.0f} m²", f"#:{t1_net:.0f} m²", f"#:{t4_net:.0f} m² + {t4_kg_net:.0f} below"],
 ["Wohnfläche, WoFlV estimate", "#:186–192 (Inhouse 12)", "#:about 143", "#:about 187"],
 ["Stairs", "2 flights + DG foyer", "1 flight 1.0 × 4.05 m", "1 flight + cellar flight stacked under it"],
 ["Windows (openings, excl. entrance and garage door)", "#:15", "#:9", "#:10"],
 ["Bedrooms", "4 (13.0 · 17.8 · 19.1 · 13.5)", "3 (14.5 · 12.2 · 14.5)", "4 (EG 10.9 · 13.4 · 15.9 · master 13.7)"],
 ["Master suite", "DG: bed 13.5 · closet 12.1 · bath 12.8", "OG: bed 14.5 · dressing 6.6 · bath 7.9", "OG: bed 13.7 · dressing 8.4 · bath 16.1 with WC room"],
 ["Bathrooms", "DG bath · OG bath (1 basin) · EG WC", "master bath · family bath 2 basins · guest shower bath", "master bath · family bath 9.7 with tub · EG en suite shower · guest WC"],
 ["Utility / laundry", "none drawn", "4.8 m² with heat pump, W+D", "basement: plant 7.8 · laundry 14.9 · stores 34 · hobby 22; OG laundry closet 3.5"],
])}
<p class="small">Net areas are the clear floor areas of the rooms as drawn (landings and open-plan zones included, walls and the stair flight excluded). The Wohnfläche estimate deducts the stair and counts no terrace; the briefing's own estimate for a two-storey pair was 165 to 175 m² per house, which T4 beats because its partitions are 0.12 m and the plate is used to the Abstandsfläche. Today's figures use your three plans as scaled.</p>

<h3>What the two-storey house gains</h3>
<ul>
<li><b>One stair.</b> Today the stair appears three times (EG, OG, DG arrival) and the DG foyer alone is 8.6 m². T1 and T4 have one straight flight on the party wall, 1.0 × 4.05 m, 15 risers of 19.3 cm with 27 cm goings for a 2.90 m storey; in T4 the cellar flight lies under it and is entered from a small lobby at the flight's south end.</li>
<li><b>No set-back storey.</b> The DG's 58.5 m² plate yields 47 m² of rooms and is ringed by roof strips; two full storeys put every square metre under a usable ceiling, and under this Bebauungsplan two full storeys on the GRZ footprint use the GFZ exactly (0.25 × 2 = 0.50), so nothing is left on the table.</li>
<li><b>Fewer windows.</b> Nine openings in T1 and ten in T4 instead of fifteen: the dressing, the guest WC, the laundry and the en suite are internal and mechanically ventilated (the Hessische Bauordnung allows this), the kitchen gets one high-sill window, and the bedrooms get one each. The east wall of the ground floor is blind for its front 7.4 m anyway, because the garage stands there.</li>
<li><b>Stacked plumbing.</b> The guest WC, the laundry and the family bath stand over each other on the party-wall side; the en suite, the master bath and the cellar laundry share the east stack.</li>
</ul>

<h3>Option T1 · same plate, master suite upstairs</h3>
{fig2("t1_eg", "<b>T1 ground floor.</b> Entrance hall with a 1.5 m wardrobe backing onto the kitchen's pantry column; guest shower bath (door hinged so the open leaf screens the WC from the hall) and utility (heat pump, buffer tank, washer-dryer against the bath wall) in the strip beside the stair; kitchen run 4.2 m on the north wall, hob clear of the window, with the 2.4 × 1.2 m island; dining table at the east window; the two 2 × 1 m sofas in the south end facing the 3.0 m lift-slide door to the terrace, TV on a low divider; the south-west nook behind the utility becomes a reading corner with a desk under its own window.")}
{fig2("t1_og", "<b>T1 upper floor.</b> The landing is the stair head plus a shelf; a 1.0 × 1.0 m linen cupboard sits over the hall. Two children's rooms to the north, each with the bed on a solid wall away from the stair, a desk centred under the window and a wardrobe on the landing wall. Family bath with a double vanity (basins 0.73 m apart), shower and WC, lit from the east through a window kept clear of the shower. Master suite to the south: landing → dressing (2.9 m rail plus a 1.0 m end wardrobe, door opening inward) → bedroom, with the bath off the dressing through a swing door so the WC wall carries no pocket cavity. The bed's headboard is on the 4.15 m party wall; the door is at the foot end and visible from the bed; the lane past the dresser is 1.10 m.")}
{rooms("t1_og")}
</div>
{LEGEND}
<div class="col">
<p>T1 meets every rule of the first brief except that the plate has to be shared: the children's rooms are 12.2 and 14.5 m² instead of today's 17.8 and 19.1 m², the master bath is 7.9 m² (tub 1.70, shower 1.2 × 1.0, double vanity 1.45) rather than the 10–12 m² a hotel suite would have, and there is no fourth bedroom and no ground-floor bedroom. Against the Altkönigstraße brief it therefore fails on the bedroom count and on the Wohnfläche (about 143 m²). It stays in the review as the reference for what two storeys give without growing the plate.</p>

<h3>Option T4 · the plot's maximum: 8.29 × 14.07 m, two storeys plus WU basement</h3>
<p>What the maximum is on this plot, in the terms of the BauNVO and the Hessische Bauordnung (HBO). The <b>GRZ</b> of 0.25 (§19 BauNVO) allows 241.65 m² of building on the 966.6 m² plot, 120.8 m² per house; garages and drives were left outside that figure in the approved Bauantrag (BauNVO 1977), so the house itself can use it all. The <b>GFZ</b> of 0.50 (§20 BauNVO) allows 483.3 m² of Geschossfläche, 241.7 m² per house; two full storeys on the GRZ footprint give exactly that, and a basement does not count because it is not a full storey under the HBO (no 2.30 m of clear height over two thirds of its area above the natural ground). The <b>Baufenster</b> runs from 5.00 to 20.00 m behind the street, 15 m deep. The <b>width</b> is fixed by the garages: with a double garage on each side boundary beside the front part of the house (5.41 m on the west, 4.8 to 6.9 m on the east, following the boundary jog) and the party line at s = 13.70 as in both current designs, each house keeps the 8.29 m of today. The <b>depth</b> can grow to 14.07 m: at 14.57 m, which would be the full 120.8 m², the east house's rear corner would stand 2.88 m from the angled east boundary, inside the 3.00 m minimum Abstandsfläche (0.4 H, at least 3.00 m, HBO); at 14.07 m it stands 3.00 m clear. The last 4 m² of GRZ could be won by moving the party line 0.5 m west, which would narrow the west garage to 4.9 m, or by a slight widening at the front only; both are for the Bauamt conversation. The plate therefore is 8.29 × 14.07 m, t = 5.00 to 19.07, mirrored about the party line, both halves at one level (273.40 as in Inhouse 12), with a WU basement under each half because the soil report puts the water at W2.1-E / W2.2-E.</p>
</div>
<div class="one"><figure>{site_svg}<figcaption><b>Site plan, site frame of the briefing</b> (s east from the west boundary, t south from the street). Plot polygon from the briefing's approximate corner coordinates; Baugrenzen at t = 5.00 and 20.00 (dashed); 3 m side setbacks (blue); the mirrored T4 pair at 8.29 × 14.07 m each with the party line at s = 13.70 (accent); boundary garages (dashed, 5.41 m west, 4.8 to 6.9 m east, t = 5.00 to 12.42). The east house's rear corner stands {site_dist:.2f} m from the east boundary. Büttner's survey DXF holds the exact boundary; this drawing is for the arithmetic, not for the Bauantrag.</figcaption></figure></div>
<div class="col">
{table(["Half-plot and ratios", "Value", "Consequence"], [
 ["Plot, pair", "#:966.6 m²", "483.3 m² per half"],
 ["GRZ 0.25, pair", "#:241.65 m²", "120.8 m² per house, garages outside"],
 ["GFZ 0.50, pair", "#:483.3 m²", "241.7 m² per house: two full storeys on 120.8 m² use it exactly"],
 ["Baufenster", "t = 5.00 to 20.00", "depth up to 15 m; side Baugrenzen not in the file, HBO setbacks assumed"],
 ["Width per house", "#:8.29 m", "set by the boundary garages and the party line at s = 13.70"],
 ["Depth", "#:14.07 m", "the east rear corner 3.00 m from the angled boundary; 14.57 m would be 2.88 m"],
 ["!Footprint per house", "#:116.6 m²", "97 % of the GRZ; 233 m² of Geschossfläche, 97 % of the GFZ"],
])}
{fig2("t4_eg", "<b>T4 ground floor, 8.29 × 14.07 m.</b> The party-wall strip holds the entrance hall with a 1.5 m wardrobe, the main stair with the cellar flight under it, the guest WC (door hinged to screen the WC), a cupboard and the cellar-stair lobby with coat hooks. The kitchen runs 4.2 m along the north wall under a high-sill window, with the pantry column, a boot cupboard beside the door from the garage, and the 2.4 × 1.2 m island; the six-seat table sits in the middle. The living room is L-shaped around the ground-floor bedroom: sofas in the south-west, TV on the bedroom wall, a 3.6 m glass front to the garden (3.0 m lift-slide plus a fixed pane) and the party-wall shelves. The bedroom (10.9 m², bed 1.6 × 2.0 with its headboard on the solid part of the east wall, an east window beside the desk and the south window, 2.0 m wardrobe) has its own en suite with a 0.9 × 0.9 shower, WC and basin, reached from the bedroom. The east wall is blind beside the garage and opens with one window at the rear.")}
{fig2("t4_og", "<b>T4 upper floor.</b> Two children's rooms of 13.4 and 15.9 m² with the beds on the partitions, desks under the north windows and wardrobes on the landing wall; a linen cupboard over the hall; a laundry closet with washer-dryer off the landing. The master suite takes the south: landing → dressing (3.5 × 2.39 m, rails on both long walls, 1.19 m aisle) → bedroom (headboard on the 3.90 m party wall, door at the foot end, dresser and TV opposite) → master bath 16.1 m² through the bedroom's east wall: separate WC room, 1.2 × 1.2 shower, double vanity, 1.8 m tub under the south window and an east window. Family bath 9.7 m² off the landing with a tub under the east window, 1.0 × 1.0 shower, double vanity and WC.")}
{fig2("t4_kg", "<b>T4 basement, WU construction.</b> Cellar hall at the foot of the cellar flight, plant room (heat pump indoor unit, buffer tank, electrics), food and bike store, a 14.9 m² laundry with drying space and the Hebeanlage, a 22.4 m² hobby or fitness room with a south light well and a 26.2 m² general store with an east light well. The hobby room needs 2.40 m of clear height and the light well to count as an Aufenthaltsraum; nothing down here counts as Wohnfläche.")}
{rooms("t4_eg")}
{rooms("t4_og")}
<h4>The brief, checked against T4</h4>
{table(["Brief item", "T4", ""], [
 ["4 bedrooms, one on the ground floor with its own shower and WC", "EG 10.9 m² with a 3.8 m² en suite · 13.4 · 15.9 · master 13.7", OK()],
 ["2 full bathrooms plus a guest WC", "master bath 16.1 (tub, 1.2 × 1.2 shower, 2 basins, WC room) · family bath 9.7 (tub, shower, 2 basins, WC) · guest WC 2.3", OK()],
 ["Open kitchen-dining-living ≥ 45 m², kitchen 4.2 m, island 2.4 × 1.2, table 2 × 1, two sofas 2 × 1", "67.6 m² in an L, all pieces placed with their walkways", OK()],
 ["Dressing at the master bedroom", "8.4 m² walk-through, two-sided", OK()],
 ["Master bedroom headboard wall ≥ 3.5 m, door not behind the bed", "3.90 m party wall, door at the foot end", OK()],
 ["Utility room (HWR)", "cellar laundry 14.9 m² and plant room 7.8 m²; laundry closet upstairs", OK()],
 ["Double garage", "on the boundary beside the house, door into the kitchen, outside the GRZ as approved", OK()],
 ["Barrier-free ground floor", "step-free entrance at one level for both halves, 0.90 m doors, bedroom and shower on the ground floor; the guest WC is not a wheelchair WC", WARN("largely")],
 ["Wohnfläche ≥ 190 m²", "about 187 m² before the terrace quarter; 165 to 175 m² was the briefing's expectation", WARN("98 %")],
 ["Mirrored pair, one level", "yes: the west half is the mirror; its garage is 5.41 m wide, its east wall is the party wall", OK()],
])}
<p>T4 is the house this envelope allows: everything on the brief is there, the living room keeps the whole garden front, the master suite upstairs is the best suite of all the versions (a 16 m² bath with daylight and a WC room, a two-sided dressing), and the ground-floor bedroom with its shower makes the house usable on one level. Its compromises are a 13.7 m² master bedroom, 10.9 m² for the ground-floor room, and a windowless dressing and laundry. Two things to settle before anyone draws further: the side Baugrenzen and the Vollgeschoss count in the Bebauungsplan text, and the WU basement itself, which the briefing prices at about 295.000 € for the pair and which the water classes make mandatory if a basement is built at all.</p>

<h3>Inspired by the Rötha design Doppelhaus: the offset pair (T4v)</h3>
<p>You sent bauWerk Leipzig's design Doppelhaus in Rötha. Read from its plans: two halves of 7.10 m width and 11.00 m depth, offset against each other by 2.50 m, with a 3.00 m single garage at the outer front corner of each; 130.5 m² of Wohnfläche per half, which is 63.0 m² on the ground floor (Flur 4.9, Garderobe 2.0, WC 1.7, HWR 4.3, Kochen 7.6 and a 42.5 m² Wohnen/Essen across the full width behind a fully glazed garden wall) and 67.5 m² upstairs (two 10.75 m² children's rooms at the street, a 9.6 m² <em>Tageslichtflur</em> with the straight stair across the house, a 9.7 m² master bath with a freestanding round tub at the window, a 7.6 m² Ankleide, and a 19.1 m² bedroom across the garden front under a full-width window band). The terrace is a wooden deck that wraps from the garden round the outer side of each half, so the offset gives every terrace a corner sheltered by the neighbour's wall. The elevations show white upper boxes over a dark, largely glazed ground floor, flat roofs, the upper storey projecting over the garden glazing, and the garages as low cubes in front.</p>
<p>What it shares with the Altkönigstraße house is almost everything in the programme: entrance, cloakroom and WC in the front corner, kitchen at the street side, living room across the garden wall, children at the street upstairs and the master suite over the garden. What differs is size (our halves are 8.29 × 14.07 m with 187 m² against their 130 m², and ours carry a fourth bedroom, a second full bath and a basement) and the three design moves that make the Rötha pair look like two houses. Those three transfer as follows. <b>Large glazing</b> is in T4 now: the living room's garden wall is a 3.6 m glass element (3.0 m lift-slide plus a fixed pane) beside the bedroom's 2.2 m window, 5.8 of the 7.71 m of south façade, and the master bedroom and bath above repeat the openings; a full-width band like Rötha's on the upper floor would need the partition between the master bedroom and the master bath to stop at a fixed glass pane, a detail rather than a plan change. <b>The wrap-around terrace</b> works on the rear outer side of each half, behind the garage: on the east half it becomes a private patio for the ground-floor bedroom, on the west half a second terrace for the living room. <b>The offset</b> is the move the Abstandsfläche decides, below. Rötha's daylit stair hall does not transfer, because our stair sits on the party wall; the flat roof gives the landing a rooflight instead. The upper floor projecting over the garden glazing is possible only in the offset version, where the GRZ has 8 m² of slack per house: a 1.0 m cantilever along the 8.29 m garden wall counts as Grundfläche and uses exactly that slack.</p>
</div>
<div class="one"><figure>{site_svg_v}<figcaption><b>T4v, the offset pair.</b> Both halves keep the same plan, 8.29 × 13.07 m, but the west half (the rental) stands 1.93 m further south: east half t = 5.00 to 18.07, west half t = 6.93 to 20.00, the full Baufenster depth. The east half cannot be the one that steps back: at t = 20.00 its rear corner would stand 2.77 m from the angled east boundary, under the 3.00 m minimum, while at 18.07 m it stands {site_dist_v:.2f} m clear. The offset exposes 1.93 m of the party wall on each half: at the front of the east half, where it lights the entrance hall and the stair through a west window, and at the rear of the west half, where it gives its living room an east window and a terrace corner screened by the neighbour's wall.</figcaption></figure></div>
<div class="col">
{table(["", "T4 · aligned pair", "T4v · offset 1.93 m", "Rötha offset 2.50 m"], [
 ["Plate per house", "8.29 × 14.07", "8.29 × 13.07, west half 1.93 m further south", "8.29 × 12.50, west half 2.50 m further south"],
 ["Footprint per house, GRZ use", "#:116.6 m² · 97 %", "#:108.4 m² · 90 %", "#:103.6 m² · 86 %"],
 ["Geschossfläche per house, GFZ use", "#:233 m² · 97 %", "#:217 m² · 90 %", "#:207 m² · 86 %"],
 ["Wohnfläche, estimate", "#:about 187 m²", "#:about 174 m²", "#:about 166 m²"],
 ["East rear corner to the boundary", "#:3.00 m", "#:3.25 m", "#:3.39 m"],
 ["Terrace privacy", "open along the party line; a 2 m screen needed", "the east terrace sits in the corner of the west half's rear wall; the west terrace needs a screen on its east side only", "as T4v, with 0.57 m more corner"],
 ["Side light", "none on the party wall", "a west window in the east half's hall and stair; an east window in the west half's living room", "as T4v, 2.50 m wide"],
 ["Street and garden façades", "one 16.6 m front per façade", "two 8.3 m volumes stepped by 1.93 m; the garage walls stay on the boundaries", "Rötha's proportion; the upper floor may cantilever 1.0 m over the garden wall within the GRZ"],
 ["Doppelhaus character", "unchanged", "kept: courts accept offset halves as one building while they read as a unit; a 1.93 m step on 13 m is modest, but the Bebauungsplan's Gestaltung rules must be read", "kept, as Rötha"],
 ["Mirrored plan", "identical halves", "identical halves shifted; only the side windows differ", "identical halves shifted"],
])}
<p>The offset costs 8 m² of footprint per house at 1.93 m, which is 13 m² of Wohnfläche and takes T4 from 187 to about 174 m², the figure the briefing itself expected for a two-storey pair; Rötha's full 2.50 m costs 13 m² of footprint and lands at about 166 m². What it buys is the thing a Doppelhaus usually lacks: a terrace that is not shared with the neighbour's, side light in the hall, and a street front that reads as two houses. If the 190 m² target matters more than the offset, T4 stands; if the house you live in should feel like a detached house from the garden, T4v is the better pair, and the plans drawn above apply to it unchanged apart from the two side windows and the 1.0 m shorter rooms on the south. Rötha's façade language, a white upper box over a dark glazed base, sits well with your own concept of dark Klinker on the garden and side walls under a white street front; the difference is that in Rötha the dark base is mostly glass.</p>

<h3>Which one</h3>
{table(["", "T1 · same plate", "T4 · plot maximum", "T4v · offset pair"], [
 ["Planning risk", "none beyond today's design", "depth to the Abstandsfläche; side Baugrenzen to confirm; WU basement in pressing water", "as T4 plus the Gestaltung rules on offset halves"],
 ["Brief", "3 bedrooms, no ground-floor bedroom, about 143 m² Wohnfläche", "all items, about 187 m² Wohnfläche", "all items, about 174 m² Wohnfläche"],
 ["Master suite", "14.5 + 6.6 + 7.9 m²", "13.7 + 8.4 + 16.1 m² with WC room and daylight", "as T4, 1.0 m shorter rooms on the south"],
 ["Children", "12.2 and 14.5 m²", "13.4 and 15.9 m² plus the ground-floor room", "as T4"],
 ["Living", "49.6 m² + 9.6 m² nook, terrace to the south", "48.7 m² + 18.9 m² lounge, 3.6 m glass front to the south", "as T4, 1.0 m shorter, plus a side window and a private terrace corner"],
 ["Cost direction", "cheapest: fewest m², one stair, slab on grade", "233 m² above ground plus a 117 m² WU basement per house", "217 m² above ground plus a 108 m² WU basement per house"],
 ["Recommendation", "only if the plate must not grow", "build this if 190 m² is the target", "build this if the garden should feel private and the stair should have daylight"],
])}
<details><summary>Earlier studies T2 and T3, drawn before the briefing (not buildable here)</summary>
<p class="small">T2 (10.29 × 12.04 m, master suite on the ground floor) and T3 (12.29 × 12.04 m with basement, drawn for an assumed 370 m² half-plot at GRZ 0.4) were drawn before the plot data arrived. Both are wider than 8.29 m, which the boundary garages do not allow, and T3 exceeds the GRZ by 27 m². Their planning ideas (hotel sequence, acoustic wall, furniture walkways) are carried into T4; the drawings stay here for the record.</p>
{fig2("t2_eg", "<b>T2 ground floor</b>, 10.29 × 12.04 m: living room with an east terrace door, master suite across the south.")}
{fig2("t2_og", "<b>T2 upper floor</b>: two children's rooms, family bath with tub, third bedroom, laundry, study.")}
{fig2("t3_eg", "<b>T3 ground floor</b>, 12.29 × 12.04 m: master suite along the north, living across the garden front.")}
{fig2("t3_og", "<b>T3 upper floor</b>: three bedrooms, family bath, shower room, family room, study.")}
{fig2("t3_kg", "<b>T3 basement</b>: plant, laundry, stores, hobby room, guest/office with light wells.")}
</details>
<details><summary>Free depth in front of every fixture, T1 and T4 (VDI 6000)</summary>{clear2("t1_eg")}{clear2("t1_og")}{clear2("t4_eg")}{clear2("t4_og")}</details>
<p class="small">All drawings pass the geometry script (no partition within 0.15 m of a window reveal, every room with a door inside a wall, no door swing onto a fixture, no overlaps, every fixture at or above the VDI minimum free depth). T1 and T2 were also read by an independent architectural reviewer, whose 47 items (three blockers) were all corrected. The T4 drawings were checked by the script and by a second pass of my own over the dumped geometry (one fault found and corrected: the ground-floor bedroom's east window stood behind the headboard); their independent review is still open and will be added when it completes.</p>
</div>
"""

html = build3.html
html = html.replace('<p class="eyebrow">Third edition', '<p class="eyebrow">Fifth edition · two-storey version on the Altkönigstraße 122 envelope')
kv_old = html[html.index('<div class="kv">'):html.index('</div>\n\n<div class="col">', html.index('<div class="kv">')) + len('</div>')]
kv_new = ('<div class="kv">\n<div><b>T4 · plot maximum</b><span>8.29 × 14.07 m, two storeys plus WU basement, 97 % of GRZ and GFZ, the whole brief, about 187 m² Wohnfläche</span></div>\n'
          '<div><b>T1 · same plate</b><span>two storeys on 8.29 × 11.04 m, one stair, 9 windows, master suite upstairs, no 4th bedroom</span></div>\n'
          '<div><b>Width 8.29 m</b><span>fixed by the boundary garages and the party line; depth 14.07 m to the 3 m Abstandsfläche at the east rear corner</span></div>\n'
          '<div><b>DG · Option A</b><span>if the three-storey house stays: bedroom 16.5 m², two partitions, no facade change</span></div>\n</div>')
html = html.replace(kv_old, kv_new, 1)
assert '<div class="col">\n<h2 id="verdict">Verdict</h2>' in html
html = html.replace('<div class="col">\n<h2 id="verdict">Verdict</h2>', section + '<div class="col">\n<h2 id="verdict">Verdict on the three-storey plans</h2>', 1)
html = html.replace('<p class="lede">Nine plans drawn', '<p class="lede">Twenty plans drawn', 1)
html = html.replace('the three floors as you drew them, three options for the top floor, two for the upper floor, one for the ground floor.', 'the three floors as you drew them, a two-storey version of the house on the real plot envelope (the same plate, and the maximum the Bebauungsplan allows with a basement), three options for the top floor, two for the upper floor, one for the ground floor.', 1)
open("artifact.html", "w").write(html)
link_end = html.index('>', html.index('<link')) + 1
doc = ('<!DOCTYPE html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
       + html[:link_end] + '</head><body>' + html[link_end:] + '</body></html>')
open("index.html", "w").write(doc)
print(len(html), "chars;", {k: len(v) for k, v in issues2.items()}, f"net cur {cur_net:.1f} t1 {t1_net:.1f} t2 {t2_net:.1f}")
