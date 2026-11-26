# Builds compositions/anat.html + index.html + captions data from timing.json
# usage: python3 build.py timing.json
import json, sys
T = json.load(open(sys.argv[1]))
L = {l["id"]: l for l in T["lines"]}
def st(i): return L[f"l{i}"]["start"]
def en(i): return round(L[f"l{i}"]["start"] + L[f"l{i}"]["dur"], 2)
D = T["D"]
# scene windows: [start, end)
S = [("hook", 0, st(2) - 0.1), ("classic", st(2) - 0.1, st(3) - 0.1), ("four", st(3) - 0.1, st(4) - 0.1),
     ("sumo", st(4) - 0.1, st(6) - 0.1), ("bulgare", st(6) - 0.1, st(8) - 0.1), ("goblet", st(8) - 0.1, st(10) - 0.1),
     ("narrow", st(10) - 0.1, st(12) - 0.1), ("outro", st(12) - 0.1, D)]
S = [(n, round(a, 2), round(b, 2)) for n, a, b in S]
W = {n: (a, b) for n, a, b in S}
cuts = [a for _, a, _ in S[1:]]

# per-scene config: title, figure mode, labels [muscle, name, level, x, y] (label anchor box position), loupe
CFG = {
 "classic": dict(num="", title="Classique", mode="classic", lab_at=st(2) + 0.9,
   labels=[["quad", "Quadriceps", 1, 610, 690], ["glute", "Fessiers", 1, 140, 700], ["ham", "Ischios", 0, 150, 900], ["abs", "Gainage", 0, 610, 560]]),
 "sumo": dict(num="1", title="Sumo", mode="sumo", lab_at=st(5), feet=(180, 34),
   labels=[["add", "Adducteurs", 1, 610, 700], ["glute", "Fessiers", 1, 140, 700], ["quad", "Quadriceps", 0, 610, 880]],
   loupe=("add", en(5) - 2.3, "Très bon choix pour l'intérieur des cuisses")),
 "bulgare": dict(num="2", title="Bulgare", mode="bulgare", lab_at=st(7),
   labels=[["glute", "Fessiers", 1, 140, 640], ["quad", "Quadriceps", 1, 610, 700]],
   loupe=("glute", en(7) - 1.9, "À garder pour les fessiers")),
 "goblet": dict(num="3", title="Goblet", mode="goblet", lab_at=st(9),
   labels=[["abs", "Gainage", 1, 610, 600], ["quad", "Quadriceps", 1, 610, 820], ["glute", "Fessiers", 0, 140, 760]],
   loupe=("abs", en(9) - 2.3, "Idéal pour apprendre le mouvement")),
 "narrow": dict(num="4", title="Pieds serrés", mode="narrow", lab_at=st(11), feet=(40, 0),
   labels=[["quad", "Quadriceps", 1, 610, 700], ["glute", "Fessiers", 0, 140, 720]],
   loupe=("quad", en(11) - 2.3, "Mon choix pour l'avant des cuisses")),
}

clips, js = [], []
for n, a, b in S:
    if n not in CFG: continue
    c = CFG[n]; dur = round(b - a, 2)
    num = f'<span class="circ">{c["num"]}</span>' if c["num"] else ""
    clips.append(f'<div id="t-{n}" class="clip ttl" data-start="{a}" data-duration="{dur}" data-track-index="1">{num}{c["title"]}</div>')
    la = round(c["lab_at"], 2)
    labs = []
    for k, (m, name, lvl, x, y) in enumerate(c["labels"]):
        cls = "lab main" if lvl else "lab sec"
        sub = "principal" if lvl else "secondaire"
        labs.append(f'<g id="lb-{n}-{k}" class="{cls}" data-m="{m}" data-x="{x}" data-y="{y}"><line class="ld" stroke-dasharray="7 7"/><circle class="ad" r="7"/><rect x="{x}" y="{y}" width="270" height="104" rx="12"/><text x="{x+20}" y="{y+46}" class="ln">{name}</text><text x="{x+20}" y="{y+86}" class="ls">{sub}</text></g>')
    clips.append(f'<svg id="labs-{n}" class="clip full" data-start="{la}" data-duration="{round(b-la,2)}" data-track-index="2" viewBox="0 0 1080 1920">{"".join(labs)}</svg>')
    js.append(f'labs("{n}", {la}, {len(labs)});')
    if "feet" in c:
        g, ang = c["feet"]
        clips.append(f'<svg id="ft-{n}" class="clip full" data-start="{a}" data-duration="{round(min(la,b)-a,2)}" data-track-index="3" viewBox="0 0 1080 1920"><g id="ftg-{n}"><rect x="630" y="470" width="250" height="170" rx="18" class="ibox"/><g transform="translate({755-g*0.4},545) rotate({-ang})"><rect x="-15" y="-34" width="30" height="68" rx="15" class="foot"/></g><g transform="translate({755+g*0.4},545) rotate({ang})"><rect x="-15" y="-34" width="30" height="68" rx="15" class="foot"/></g><text x="755" y="625" text-anchor="middle" class="ilbl">vue de dessus</text></g></svg>')
        js.append(f'tl.from("#ftg-{n}", {{ opacity: 0, y: 30, duration: 0.3, ease: "power3.out" }}, {a + 0.4});')
    if "loupe" in c:
        m, t0, txt = c["loupe"]; t0 = round(max(t0, la + 0.6), 2)
        clips.append(f'<svg id="lp-{n}" class="clip full" data-start="{t0}" data-duration="{round(b-t0,2)}" data-track-index="4" viewBox="0 0 1080 1920"><defs><clipPath id="cp-{n}"><circle cx="540" cy="760" r="190"/></clipPath></defs><g id="lpg-{n}" style="transform-origin:540px 760px"><circle cx="540" cy="760" r="196" fill="#fff"/><g clip-path="url(#cp-{n})"><rect x="340" y="560" width="400" height="400" fill="#f3efe8"/><use id="lu-{n}" href="#body" data-m="{m}"/></g><circle cx="540" cy="760" r="193" fill="none" stroke="#1b1b1b" stroke-width="7"/><g id="bn-{n}"><rect x="190" y="975" width="700" height="76" rx="12" fill="#b8352a"/><text x="540" y="1025" text-anchor="middle" class="bn">{txt}</text></g></g></svg>')
        js.append(f'loupe("{n}", {t0});')
    js.append(f'reps({a}, {b}, "{c["mode"]}");')

# hook / four / outro
a,b=W["hook"]; clips.insert(0,f'<div id="t-hook" class="clip ttl" data-start="0" data-duration="{b}" data-track-index="1" style="font-size:96px">Pas que tes cuisses</div>')
js.append(f'reps(0, {b}, "classic");')
for i,(mm,t) in enumerate([("quad",0.5),("glute",0.8),("ham",1.1),("abs",1.4),("calf",1.7)]):
    js.append(f'tl.to(A, {{ {mm}: 1, duration: 0.15 }}, {t});')
js.append('tl.from("#t-hook", { y: -30, opacity: 0, duration: 0.3, ease: "power3.out" }, 0.05);')
a,b=W["four"]; clips.append(f'<div id="t-four" class="clip ttl" data-start="{a}" data-duration="{round(b-a,2)}" data-track-index="1"><span class="circ">4</span>variantes</div>')
clips.append(f'<div id="nums" class="clip nums" data-start="{a}" data-duration="{round(b-a,2)}" data-track-index="2"><span>1</span><span>2</span><span>3</span><span>4</span></div>')
js.append(f'reps({a}, {b}, "classic");'); js.append(f'tl.from("#nums span", {{ scale: 0, opacity: 0, duration: 0.25, stagger: 0.15, ease: "back.out(2.2)" }}, {a+0.5});')
a,b=W["outro"]; clips.append(f'<div id="t-outro" class="clip ttl" data-start="{a}" data-duration="{round(b-a,2)}" data-track-index="1">Tu fais lequel ?</div>')
clips.append(f'<div id="rows" class="clip rows" data-start="{a}" data-duration="{round(b-a,2)}" data-track-index="2"><div class="row"><b>1</b>Sumo</div><div class="row"><b>2</b>Bulgare</div><div class="row"><b>3</b>Goblet</div><div class="row"><b>4</b>Pieds serrés</div></div>')
js.append(f'tl.to(P, {{ show: 0, duration: 0.2 }}, {a});'); js.append(f'tl.from("#rows .row", {{ x: 120, opacity: 0, duration: 0.3, stagger: 0.12, ease: "power3.out" }}, {a+0.3});')
js.append(f'tl.from("#t-outro", {{ scale: 1.2, opacity: 0, duration: 0.3, ease: "back.out(2)" }}, {a});')
for n in ("classic","sumo","bulgare","goblet","narrow"):
    js.append(f'tl.from("#t-{n}", {{ x: -80, opacity: 0, duration: 0.3, ease: "power3.out" }}, {W[n][0]+0.05});')
TPL = open("anat.tpl").read()
html = (TPL.replace("/*CLIPS*/", "\n    ".join(clips)).replace("/*JS*/", "\n      ".join(js))
        .replace("/*D*/", str(D)).replace("/*W*/", json.dumps(W)).replace("/*CUTS*/", json.dumps(cuts)))
open("compositions/anat.html", "w").write(html)

# root
aud = "".join(f'\n      <audio id="vo-{l["id"]}" class="clip" src="assets/voice/{l["id"]}.wav" data-start="{l["start"]}" data-duration="{l["dur"]}" data-track-index="2" data-volume="1"></audio>' for l in T["lines"])
sfx = "".join(f'\n      <audio id="sfx-{i}" class="clip" src="assets/sfx/whoosh.mp3" data-start="{c-0.15:.2f}" data-duration="0.45" data-track-index="{4+i%2}" data-volume="0.25"></audio>' for i, c in enumerate(cuts))
root = f'''<!doctype html>
<html lang="fr">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: #f3efe8; }}
      #root {{ position: relative; width: 100%; height: 100%; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{D}" data-width="1080" data-height="1920">
      <div id="anat" data-composition-id="anat" data-composition-src="compositions/anat.html" data-start="0" data-duration="{D}" data-track-index="0" data-track-kind="graphics" data-width="1080" data-height="1920"></div>
      <div id="captions" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="{D}" data-track-index="1" data-track-kind="captions" data-width="1080" data-height="1920"></div>{aud}
      <audio id="music" class="clip" src="assets/music/beat.mp3" data-start="0" data-duration="{D}" data-track-index="3" data-volume="0.09" data-fade-out="1.5"></audio>{sfx}
    </div>
    <script>
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
'''
open("index.html", "w").write(root)
print("scenes", S)
