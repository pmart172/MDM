import importlib, plancss, subprocess, sys, os
floors = importlib.import_module(os.environ.get("FLOORS", "floors2"))
css = "<style>" + plancss.TOKENS + plancss.PLAN_CSS + "body{background:var(--paper);padding:10px;margin:0} .plan{width:900px}</style>"
defs = '<svg width="0" height="0" style="position:absolute"><defs><marker id="ah" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="context-stroke"/></marker></defs></svg>'
keys = sys.argv[1:] or list(floors.ALL)
for k in keys:
    p = floors.ALL[k]()
    open(f"one_{k}.html","w").write(f'<!DOCTYPE html><html><head><meta charset="utf-8">{css}</head><body>{defs}{p.svg()}</body></html>')
    subprocess.run(["/opt/pw-browsers/chromium-1194/chrome-linux/chrome","--headless=new","--no-sandbox","--disable-gpu","--hide-scrollbars","--window-size=940,1500",f"--screenshot=one_{k}.png",f"file://{os.getcwd()}/one_{k}.html"], capture_output=True)
print("rendered", keys)
