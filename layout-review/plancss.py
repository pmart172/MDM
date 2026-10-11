PLAN_CSS = r"""
.plan{display:block;width:100%;max-width:100%;height:auto;background:var(--paper2);border:1px solid var(--rule)}
.plan .wall{fill:var(--wall)} .plan .wall-new{fill:var(--accent)} .plan .wall-gone{fill:none;stroke:var(--bad);stroke-width:1.4;stroke-dasharray:4 3}
.plan .floor{fill:var(--floor)} .plan .outline{fill:none;stroke:var(--muted);stroke-width:1;stroke-dasharray:6 4}
.plan .terrace{fill:var(--terrace)}
.plan .win{fill:var(--winfill)} .plan .win-new{fill:var(--winfill);stroke:var(--accent);stroke-width:1.2}
.plan .winl{stroke:var(--ink);stroke-width:.8}
.plan .open{fill:var(--floor)} .plan .leaf{stroke:var(--ink);stroke-width:1.8} .plan .leaf-new{stroke:var(--accent);stroke-width:1.8}
.plan .arc{fill:none;stroke:var(--ink);stroke-width:.7;stroke-dasharray:3 2}
.plan .slide{stroke:var(--accent);stroke-width:3.5;stroke-dasharray:7 3}
.plan .glass{stroke:var(--accent);stroke-width:2}
.plan .f-bed{fill:var(--bedfill);stroke:var(--ink);stroke-width:.8} .plan .f-head{fill:var(--ink)}
.plan .pillow{fill:var(--floor);stroke:var(--ink);stroke-width:.6}
.plan .f-wet{fill:var(--wetfill);stroke:var(--ink);stroke-width:.8} .plan .f-wet-in{fill:var(--floor);stroke:var(--ink);stroke-width:.5}
.plan .basin{fill:var(--floor);stroke:var(--ink);stroke-width:.7} .plan .bowl{fill:var(--floor);stroke:var(--ink);stroke-width:.8}
.plan .drain{fill:var(--ink)} .plan .hob{fill:none;stroke:var(--ink);stroke-width:.7}
.plan .f-ward{fill:var(--wardfill);stroke:var(--ink);stroke-width:.8} .plan .rail{stroke:var(--ink);stroke-width:1}
.plan .f-furn{fill:var(--furnfill);stroke:var(--ink);stroke-width:.8} .plan .f-furn-dark{fill:var(--furndark)} .plan .f-chair{fill:var(--furnfill);stroke:var(--ink);stroke-width:.6}
.plan .f-ring{fill:none;stroke:var(--ink);stroke-width:.8}
.plan .f-rad{fill:var(--accent)}
.plan .stairs{fill:var(--floor);stroke:var(--ink);stroke-width:.8} .plan .void{fill:var(--voidfill);stroke:var(--ink);stroke-width:.5;stroke-dasharray:2 2}
.plan .chim{fill:var(--chim)}
.plan .thin{stroke:var(--ink);stroke-width:.6} .plan .hair{stroke:var(--ink);stroke-width:.35;opacity:.7}
.plan .arrow{stroke:var(--ink);stroke-width:1.2;marker-end:url(#ah)}
.plan .zone{fill:var(--zonefill);stroke:var(--zoneline);stroke-width:.7;stroke-dasharray:3 2}
.plan .zone-path{fill:var(--pathfill);stroke:var(--zoneline);stroke-width:.7;stroke-dasharray:3 2}
.plan .ztext{font-family:var(--mono);font-size:8.5px;fill:var(--zonetext);text-anchor:middle}
.plan .walk{fill:none;stroke:var(--bad);stroke-width:1.4;stroke-dasharray:5 3;opacity:.85}
.plan .callout{fill:var(--accent)} .plan .callout-t{font-family:var(--mono);font-size:11px;font-weight:600;fill:var(--paper2);text-anchor:middle}
.plan .rname{font-family:var(--display);font-size:12.5px;font-weight:600;fill:var(--ink);text-anchor:middle}
.plan .rarea{font-family:var(--mono);font-size:11px;fill:var(--accent);text-anchor:middle}
.plan .rsub{font-family:var(--mono);font-size:8.5px;fill:var(--muted);text-anchor:middle}
.plan .flabel{font-family:var(--body);font-size:8.5px;fill:var(--ink);text-anchor:middle}
.plan .tiny{font-family:var(--mono);font-size:7.5px;fill:var(--muted);text-anchor:middle}
.plan .note{font-family:var(--mono);font-size:9px;fill:var(--muted)}
.plan .dim{stroke:var(--muted);stroke-width:.7} .plan .dimt{font-family:var(--mono);font-size:9.5px;fill:var(--muted);text-anchor:middle}
.plan .northp{fill:var(--ink)} .plan .sb-a{fill:var(--ink)} .plan .sb-b{fill:var(--paper2);stroke:var(--ink);stroke-width:.6}
"""
TOKENS = r"""
:root{
  --paper:#f4f3ef; --paper2:#fbfaf7; --floor:#fffefb; --ink:#1c2230; --muted:#687080; --rule:#d8d5cc;
  --accent:#2b5c8a; --accent-soft:#e0e9f2; --bad:#b23b2f; --ok:#2f7a4f; --warn:#a86a0c;
  --ok-soft:#e2f0e7; --warn-soft:#f6ecd7; --bad-soft:#f6e1de;
  --wall:#262b36; --winfill:#cfe2f2; --voidfill:#ece8dd; --chim:#8f98a6; --terrace:#ebe6d6;
  --bedfill:#ebe5d6; --wetfill:#d8e8f3; --wardfill:#ece6d8; --furnfill:#f2eee4; --furndark:#ded7c6;
  --zonefill:rgba(43,92,138,.10); --pathfill:rgba(168,106,12,.12); --zoneline:#2b5c8a; --zonetext:#2b5c8a;
  --display:"Bricolage Grotesque","Avenir Next",system-ui,sans-serif;
  --body:"Source Sans 3","Source Sans Pro",system-ui,sans-serif;
  --mono:"IBM Plex Mono",ui-monospace,Menlo,monospace;
}
@media (prefers-color-scheme: dark){ :root:not([data-theme="light"]){
  --paper:#14171d; --paper2:#1a1e26; --floor:#20252e; --ink:#e9e7e0; --muted:#9ca3ae; --rule:#2f343e;
  --accent:#8fb8de; --accent-soft:#1f2e3d; --bad:#ef8b80; --ok:#80cf9c; --warn:#e6b55e;
  --ok-soft:#1b3326; --warn-soft:#3a2d14; --bad-soft:#3d1f1d;
  --wall:#cfd3db; --winfill:#2e4d66; --voidfill:#272b34; --chim:#5e6876; --terrace:#2a2d33;
  --bedfill:#3b3629; --wetfill:#233746; --wardfill:#383327; --furnfill:#2b303a; --furndark:#3b414d;
  --zonefill:rgba(143,184,222,.14); --pathfill:rgba(230,181,94,.14); --zoneline:#8fb8de; --zonetext:#b7d2ea;
  color-scheme:dark }}
:root[data-theme="dark"]{
  --paper:#14171d; --paper2:#1a1e26; --floor:#20252e; --ink:#e9e7e0; --muted:#9ca3ae; --rule:#2f343e;
  --accent:#8fb8de; --accent-soft:#1f2e3d; --bad:#ef8b80; --ok:#80cf9c; --warn:#e6b55e;
  --ok-soft:#1b3326; --warn-soft:#3a2d14; --bad-soft:#3d1f1d;
  --wall:#cfd3db; --winfill:#2e4d66; --voidfill:#272b34; --chim:#5e6876; --terrace:#2a2d33;
  --bedfill:#3b3629; --wetfill:#233746; --wardfill:#383327; --furnfill:#2b303a; --furndark:#3b414d;
  --zonefill:rgba(143,184,222,.14); --pathfill:rgba(230,181,94,.14); --zoneline:#8fb8de; --zonetext:#b7d2ea;
  color-scheme:dark }
"""
