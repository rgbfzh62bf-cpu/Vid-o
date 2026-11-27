# Image-based anatomy explainer. usage: python3 build2.py timing.json cfg.json
import json, sys
T = json.load(open(sys.argv[1])); C = json.load(open(sys.argv[2]))
L = {l["id"]: l for l in T["lines"]}
st = lambda i: L[f"l{i}"]["start"]; en = lambda i: round(L[f"l{i}"]["start"] + L[f"l{i}"]["dur"], 2)
D = T["D"]
S = [("hook", 0, st(2) - 0.1), ("five", st(2) - 0.1, st(3) - 0.1), ("classic", st(3) - 0.1, st(4) - 0.1),
     ("sumo", st(4) - 0.1, st(5) - 0.1), ("narrow", st(5) - 0.1, st(6) - 0.1), ("bulgare", st(6) - 0.1, st(7) - 0.1),
     ("jump", st(7) - 0.1, st(8) - 0.1), ("outro", st(8) - 0.1, D)]
S = [(n, round(a, 2), round(b, 2)) for n, a, b in S]
W = {n: (a, b) for n, a, b in S}
cuts = [a for _, a, _ in S[1:]]
# image box on screen
IW, IH, X0, Y0 = 743, 1300, 168, 420
def scr(fx, fy): return (round(X0 + fx * IW), round(Y0 + fy * IH))
LAB_AT = {n: W[n][0] + 0.7 for n in ["classic", "sumo", "narrow", "bulgare", "jump"]}
LOUPE_AT = {n: W[n][1] - 1.6 for n in ["classic", "sumo", "narrow", "bulgare", "jump"]}
TITLE = {"classic": ("1", "Classique"), "sumo": ("2", "Sumo"), "narrow": ("3", "Pieds serrés"), "bulgare": ("4", "Bulgare"), "jump": ("5", "Sauté")}

h, js = [], []
def clip(id_, a, b, inner, cls="", style="", track=1):
    h.append(f'<div id="{id_}" class="clip {cls}" data-start="{a}" data-duration="{round(b-a,2)}" data-track-index="{track}" style="{style}">{inner}</div>')

def figure(n, a, b, img, extra="", dim_at=None):
    clip(f"im-{n}", a, b, f'<div id="iw-{n}" class="iw"><img src="{img}" alt="" />{extra}</div>', "imbox", track=0)
    js.append(f'tl.fromTo("#iw-{n}", {{ scale: 1.05 }}, {{ scale: 1, duration: 0.7, ease: "power2.out" }}, {a});')
    js.append(f'tl.to("#iw-{n}", {{ scale: 1.015, duration: {round(max(0.5,b-a-0.75),2)}, ease: "none" }}, {round(a+0.7,2)});')
    if dim_at: js.append(f'tl.to("#iw-{n} img, #iw-{n} .kb", {{ opacity: 0.28, duration: 0.3 }}, {dim_at});')

def hl(n, m, fx, fy, w=150, hgt=110, rot=0):
    # highlight div positioned inside image wrapper (percent coords)
    return f'<div class="hl{" g" if m=="glute" else ""}" id="hl-{n}-{m}" style="left:{fx*100:.1f}%;top:{fy*100:.1f}%;width:{w}px;height:{hgt}px;transform:translate(-50%,-50%) rotate({rot}deg)"></div>'

def title(n, a, b, num, txt, size=92):
    c = f'<span class="circ">{num}</span>' if num else ""
    clip(f"t-{n}", a, b, f"{c}{txt}", "ttl", f"font-size:{size}px")
    js.append(f'tl.from("#t-{n}", {{ y: -24, opacity: 0, duration: 0.35, ease: "power3.out" }}, {a + 0.05});')

# ---- hook
a, b = W["hook"]; cut1 = round(min(1.3, b - 0.6), 2)
title("hook", 0, b, "", "Toujours le même squat ?", 72)
figure("hook0", 0, cut1, C["stand"]["img"])
cc = C["classic"]
ex = "".join(hl("hook", m, *cc["anch"][m], *cc.get("hsize", {}).get(m, [150, 110, 0])) for m in ["quad", "glute", "abs"] if m in cc["anch"])
figure("hook1", cut1, b, cc["img"], ex)
for i, m in enumerate([m for m in ["quad", "glute", "abs"] if m in cc["anch"]]):
    js.append(f'tl.from("#hl-hook-{m}", {{ opacity: 0, scale: 0.4, duration: 0.25, ease: "back.out(2)" }}, {cut1 + 0.15 + i * 0.3});')

# ---- variants
for n in ["classic", "sumo", "narrow", "bulgare", "jump"]:
    a, b = W[n]; c = C[n]; la = round(LAB_AT[n], 2); lo = LOUPE_AT.get(n)
    lo = round(max(lo, la + 0.55 * len(c["labels"]) + 0.3), 2) if (lo and "loupe" in c and lo < b - 0.8) else None
    ms = [l[0] for l in c["labels"]]
    ex = "".join(hl(n, m, *c["anch"][m], *c.get("hsize", {}).get(m, [150, 110, 0])) for m in ms)
    if c.get("kb"): ex += f'<div class="kb" style="left:{c["kb"][0]*100:.1f}%;top:{c["kb"][1]*100:.1f}%"><i></i></div>'
    figure(n, a, b, c["img"], ex, lo)
    title(n, a, b, *TITLE[n])
    for m in ms: js.append(f'tl.set("#hl-{n}-{m}", {{ opacity: 0 }}, {a});')
    # labels + leaders (static svg)
    lab_end = lo if lo else b
    svg, divs = [], []
    for k, (m, name, lvl, x, y) in enumerate(c["labels"]):
        ax, ay = scr(*c["anch"][m]); ex_ = x + 270 if x < 540 else x
        svg.append(f'<g id="ld-{n}-{k}"><line x1="{ex_}" y1="{y+50}" x2="{ax}" y2="{ay}" stroke="#1b1b1b" stroke-width="3" stroke-dasharray="7 7"/><circle cx="{ax}" cy="{ay}" r="7" fill="#1b1b1b"/></g>')
        divs.append(f'<div id="lb-{n}-{k}" class="lab {"main" if lvl else "sec"}" style="left:{x}px;top:{y}px"><b>{name}</b><span>{"principal" if lvl else "secondaire"}</span></div>')
        t = round(la + k * 0.4, 2)
        js.append(f'tl.from("#lb-{n}-{k}", {{ opacity: 0, x: {-30 if x < 540 else 30}, duration: 0.3, ease: "power3.out" }}, {t});')
        js.append(f'tl.from("#ld-{n}-{k}", {{ opacity: 0, duration: 0.25 }}, {t + 0.15});')
        js.append(f'tl.to("#hl-{n}-{m}", {{ opacity: {1 if lvl else 0.55}, duration: 0.3 }}, {t});')
    clip(f"labs-{n}", la, lab_end, f'<svg class="full" viewBox="0 0 1080 1920">{"".join(svg)}</svg>{"".join(divs)}', "layer", track=2)
    if "feet" in c:
        g, ang = c["feet"]; fe = round(min(la, b), 2); fx0 = c.get("feetx", 760)
        feet = f'<svg class="full" viewBox="0 0 1080 1920"><g id="fg-{n}"><rect x="{fx0-120}" y="450" width="240" height="190" rx="18" fill="#fff" stroke="#1b1b1b" stroke-width="3"/><g transform="translate({fx0-g/2},535) rotate({-ang})"><rect x="-15" y="-36" width="30" height="72" rx="15" fill="#b8352a"/></g><g transform="translate({fx0+g/2},535) rotate({ang})"><rect x="-15" y="-36" width="30" height="72" rx="15" fill="#b8352a"/></g><text x="{fx0}" y="622" text-anchor="middle" class="ilbl">vue de dessus</text></g></svg>'
        clip(f"ft-{n}", round(a + 0.4, 2), fe, feet, "layer", track=3)
        js.append(f'tl.from("#fg-{n}", {{ opacity: 0, y: 30, duration: 0.3, ease: "power3.out" }}, {a + 0.45});')
    if lo:
        m = c["loupe"][0]; fx, fy = c["anch"][m]; z = c["loupe"][2] if len(c["loupe"]) > 2 else 2.4
        zw, zh = IW * z, IH * z
        ix, iy = 200 - fx * zw, 200 - fy * zh
        hsz = c.get("hsize", {}).get(m, [150, 110, 0])
        lup = (f'<div id="lp-{n}" class="loupe"><div class="lin"><img src="{c["img"]}" alt="" style="left:{ix:.0f}px;top:{iy:.0f}px;width:{zw:.0f}px;height:{zh:.0f}px" />'
               f'<div class="hl on{" g" if m=="glute" else ""}" style="left:200px;top:200px;width:{hsz[0]*z:.0f}px;height:{hsz[1]*z:.0f}px;transform:translate(-50%,-50%) rotate({hsz[2]}deg)"></div></div></div>'
               f'<div id="bn-{n}" class="banner">{c["loupe"][1]}</div>')
        clip(f"lps-{n}", lo, b, lup, "layer", track=4)
        js.append(f'tl.from("#lp-{n}", {{ scale: 0.3, opacity: 0, duration: 0.4, ease: "back.out(1.7)" }}, {lo});')
        js.append(f'tl.from("#bn-{n}", {{ y: 40, opacity: 0, duration: 0.3, ease: "power3.out" }}, {lo + 0.35});')

# ---- four
a, b = W["five"]
title("five", a, b, "", "5 squats, 5 résultats", 76)
figure("five", a, b, C["stand"]["img"], "", a + 0.01)
clip("nums", a, b, "".join(f'<span>{i}</span>' for i in range(1, 6)), "nums", track=2)
js.append(f'tl.from("#nums span", {{ scale: 0, opacity: 0, duration: 0.3, stagger: 0.18, ease: "back.out(2.2)" }}, {a + 0.4});')
# ---- outro
a, b = W["outro"]
title("outro", a, b, "", "Tu fais lequel ?")
figure("outro", a, b, C["stand"]["img"], "", a + 0.01)
clip("rows", a, b, "".join(f'<div class="row"><b>{i}</b>{t}</div>' for i, t in enumerate(["Classique", "Sumo", "Pieds serrés", "Bulgare", "Sauté"], 1)), "rows", track=2)
js.append(f'tl.from("#rows .row", {{ x: 120, opacity: 0, duration: 0.3, stagger: 0.12, ease: "power3.out" }}, {a + 0.3});')

tpl = open("illus.tpl").read()
open("compositions/illus.html", "w").write(tpl.replace("/*CLIPS*/", "\n    ".join(h)).replace("/*JS*/", "\n      ".join(js)).replace("/*D*/", str(D)))
aud = "".join(f'\n      <audio id="vo-{l["id"]}" class="clip" src="assets/voice5/{l["id"]}.wav" data-start="{l["start"]}" data-duration="{l["dur"]}" data-track-index="2" data-volume="1"></audio>' for l in T["lines"])
sfx = "".join(f'\n      <audio id="sfx-{i}" class="clip" src="assets/sfx/whoosh.mp3" data-start="{max(0,c-0.12):.2f}" data-duration="0.45" data-track-index="{4+i%2}" data-volume="0.2"></audio>' for i, c in enumerate(cuts))
root = f'''<!doctype html>
<html lang="fr">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: #ffffff; }}
      #root {{ position: relative; width: 100%; height: 100%; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{D}" data-width="1080" data-height="1920">
      <div id="illus" data-composition-id="illus" data-composition-src="compositions/illus.html" data-start="0" data-duration="{D}" data-track-index="0" data-track-kind="graphics" data-width="1080" data-height="1920"></div>{aud}
      <audio id="music" class="clip" src="assets/music/bed.mp3" data-start="0" data-duration="{D}" data-track-index="3" data-volume="0.08" data-fade-in="0.5" data-fade-out="1.5"></audio>{sfx}
    </div>
    <script>
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
'''
open("index.html", "w").write(root)
print(S)
