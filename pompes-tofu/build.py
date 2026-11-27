# Builds compositions/pompes.html + index.html + captions words from assets/voice/l*.wav
# usage: python3 build.py   (needs librosa)
import json, re, librosa
CAP = ["Tu fais toujours les mêmes pompes ? Grosse erreur !",
       "Il en existe 5. Et chacune travaille un muscle différent.",
       "Numéro 1 : la classique. Pecs, épaules, triceps.",
       "Numéro 2 : mains écartées. Encore plus de pecs.",
       "Numéro 3 : mains serrées, en diamant. Les triceps prennent cher !",
       "Numéro 4 : les déclinées, pieds surélevés. Le haut des pecs et les épaules. Tout le monde les zappe… mais ce sont les plus sous-cotées.",
       "Numéro 5 : sur les genoux. Les mêmes muscles, en plus facile. Parfait pour débuter sans tricher.",
       "Alors, tu fais laquelle ? Dis-le en commentaire, et enregistre la vidéo pour ta prochaine séance !"]
t = 0.12; lines = []; words = []
for i, cap in enumerate(CAP, 1):
    y, sr = librosa.load(f"assets/voice/l{i}.wav", sr=None); d = len(y) / sr
    iv = librosa.effects.split(y, top_db=30); s0, s1 = iv[0][0] / sr, iv[-1][1] / sr
    ws = cap.split(); Lc = sum(len(w) + 2 for w in ws); c = t + s0
    for w in ws:
        dw = (len(w) + 2) / Lc * (s1 - s0)
        if i > 1: words.append({"text": w, "start": round(c, 2), "end": round(c + dw, 2)})
        c += dw
    lines.append({"id": f"l{i}", "start": round(t, 2), "dur": round(d, 2)}); t += d + 0.25
C = [0] + [round(l["start"] - 0.1, 2) for l in lines[1:]]
D = round(t + 0.9, 2); LOOP = 0.4
W = {n: (C[k], C[k + 1] if k + 1 < len(C) else D) for k, n in enumerate(["hook", "intro", "classic", "wide", "diamond", "decline", "knees", "outro"])}
VAR = [("classic", "01", "CLASSIQUE", ["PECS", "ÉPAULES", "TRICEPS"], (110, 0)), ("wide", "02", "MAINS ÉCARTÉES", ["PECTORAUX"], (200, 0)),
       ("diamond", "03", "DIAMANT", ["TRICEPS"], (22, 38)), ("decline", "04", "DÉCLINÉES", ["HAUT DES PECS", "ÉPAULES"], None),
       ("knees", "05", "SUR LES GENOUX", ["DÉBUTANT"], None)]
HL = {"classic": ["chest", "delt", "tri"], "wide": ["chest"], "diamond": ["tri"], "decline": ["chest", "delt"], "knees": ["chest", "tri"]}
clips, js = [], []
def clip(id_, a, b, inner, cls, track, style=""):
    clips.append(f'<div id="{id_}" class="clip {cls}" data-start="{a}" data-duration="{round(b-a,2)}" data-track-index="{track}" style="{style}">{inner}</div>')
hook_html = 'TU FAIS TOUJOURS<br />LES MÊMES <span class="a">POMPES</span> ?'
clip("t-hook", 0, W["hook"][1], hook_html, "ttl big", 1, "top:306px;font-size:64px")
clips.append(f'<svg id="x-stamp" class="clip full" data-start="1.4" data-duration="{round(W["hook"][1]-1.4,2)}" data-track-index="2" viewBox="0 0 1080 1920"><g id="x-g" style="transform-origin:540px 960px"><circle cx="540" cy="960" r="200" fill="none" stroke="#ff3b3b" stroke-width="22" /><path d="M425 845 L655 1075 M655 845 L425 1075" stroke="#ff3b3b" stroke-width="28" stroke-linecap="round" /></g></svg>')
js.append('tl.from("#t-hook", { scale: 1.12, duration: 0.35, ease: "power3.out" }, 0);')
js.append('tl.fromTo("#x-g", { scale: 2.2, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.22, ease: "back.out(2.4)" }, 1.4);')
js.append('tl.to("#x-g", { rotation: 8, duration: 0.08, yoyo: true, repeat: 3 }, 1.62);')
js.append(f'reps(0, {W["hook"][1]}, "bad", 0.95);')
a, b = W["intro"]
clip("t-intro", a, b, '<div id="i-a" class="big" style="font-size:118px"><span class="a">5</span> POMPES</div><div id="i-b" class="mid" style="margin-top:20px">5 RÉSULTATS</div>', "ttl", 1, "top:300px")
js.append(f'tl.from("#i-a", {{ scale: 0.4, opacity: 0, duration: 0.3, ease: "back.out(2)" }}, {a+0.05});')
js.append(f'tl.from("#i-b", {{ y: 60, opacity: 0, duration: 0.25, ease: "power3.out" }}, {a+0.5});')
js.append(f'reps({a}, {b}, "classic", 1.0);')
for n, num, title, chips, hands in VAR:
    a, b = W[n]
    clip(f"t-{n}", a, b, f'<span class="num">{num}</span>{title}', "ttl big", 1, "top:300px")
    clip(f"c-{n}", a, b, "".join(f'<span class="chip">{c}</span>' for c in chips), "chips", 2)
    js.append(f'tl.from("#t-{n}", {{ x: -120, opacity: 0, duration: 0.25, ease: "power3.out" }}, {a+0.02});')
    js.append(f'tl.from("#c-{n} .chip", {{ y: 40, opacity: 0, duration: 0.22, stagger: 0.1, ease: "back.out(2)" }}, {a+0.25});')
    js.append(f'reps({a}, {b}, "{n}", {1.05 if n!="diamond" else 1.15});')
    js.append(f'lights({a}, {json.dumps(HL[n])});')
    if hands:
        g, ang = hands
        clips.append(f'<svg id="in-{n}" class="clip full" data-start="{a}" data-duration="{round(b-a,2)}" data-track-index="3" viewBox="0 0 1080 1920"><g id="ig-{n}"><rect x="130" y="640" width="230" height="190" rx="20" fill="#15161a" stroke="#2a2c33" stroke-width="3" /><g transform="translate({245-g/2},718) rotate({ang})"><rect x="-17" y="-34" width="34" height="68" rx="16" fill="#c8ff2e" /></g><g transform="translate({245+g/2},718) rotate({-ang})"><rect x="-17" y="-34" width="34" height="68" rx="16" fill="#c8ff2e" /></g><text x="245" y="812" text-anchor="middle" class="inset-lbl">ÉCART MAINS</text></g></svg>')
        js.append(f'tl.from("#ig-{n}", {{ opacity: 0, x: -40, duration: 0.25 }}, {a+0.1});')
a, b = W["outro"]
clip("t-outro", a, round(D - LOOP, 2), 'ALORS,<br /><span class="a">LAQUELLE</span><br />TU FAIS ?', "ttl big", 1, "top:300px")
rows = "".join(f'<div class="row"><b>{i}</b>{t}</div>' for i, t in enumerate(["CLASSIQUE", "MAINS ÉCARTÉES", "DIAMANT", "DÉCLINÉES", "SUR LES GENOUX"], 1))
clip("grid", a, round(D - LOOP, 2), rows, "grid5", 2)
clip("save", a, round(D - LOOP, 2), '<span>ENREGISTRE-LA POUR TA SÉANCE</span>', "save", 3)
clip("t-hook2", round(D - LOOP, 2), D, hook_html, "ttl big", 1, "top:306px;font-size:64px")
js.append(f'tl.to(P, {{ show: 0, duration: 0.15 }}, {a});')
js.append(f'tl.from("#grid .row", {{ x: 160, opacity: 0, duration: 0.25, stagger: 0.12, ease: "power3.out" }}, {a+0.3});')
js.append(f'tl.from("#save span", {{ scale: 0.6, opacity: 0, duration: 0.3, ease: "back.out(2)" }}, {a+1.6});')
js.append(f'tl.set(P, {{ show: 1, mode: "bad", d: 0 }}, {round(D-LOOP,2)});')
js.append(f'tl.set(A, {{ chest: 0, delt: 0, tri: 0 }}, {round(D-LOOP,2)});')
js.append(f'{json.dumps(C[1:])}.forEach(function (c) {{ tl.fromTo("#flash", {{ opacity: 0.35 }}, {{ opacity: 0, duration: 0.18, ease: "power2.out", immediateRender: false }}, c); }});')
tpl = open("pompes.tpl").read()
open("compositions/pompes.html", "w").write(tpl.replace("/*CLIPS*/", "\n    ".join(clips)).replace("/*JS*/", "\n      ".join(js)).replace("/*D*/", str(D)))
aud = "".join(f'\n      <audio id="vo-{l["id"]}" class="clip" src="assets/voice/{l["id"]}.wav" data-start="{l["start"]}" data-duration="{l["dur"]}" data-track-index="2" data-volume="1"></audio>' for l in lines)
sfx = "".join(f'\n      <audio id="sfx-{i}" class="clip" src="assets/sfx/whoosh.mp3" data-start="{c-0.15:.2f}" data-duration="0.45" data-track-index="{4+i%2}" data-volume="0.3"></audio>' for i, c in enumerate(C[1:]))
open("index.html", "w").write(f'''<!doctype html>
<html lang="fr">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: #0b0b0d; }}
      #root {{ position: relative; width: 100%; height: 100%; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{D}" data-width="1080" data-height="1920">
      <div id="pompes" data-composition-id="pompes" data-composition-src="compositions/pompes.html" data-start="0" data-duration="{D}" data-track-index="0" data-track-kind="graphics" data-width="1080" data-height="1920"></div>
      <div id="captions" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="{D}" data-track-index="1" data-track-kind="captions" data-width="1080" data-height="1920"></div>{aud}
      <audio id="music" class="clip" src="assets/music/beat.mp3" data-start="0" data-duration="{D}" data-track-index="3" data-volume="0.12" data-fade-out="1.2"></audio>{sfx}
    </div>
    <script>
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
''')
G = []; g = []
for k, w in enumerate(words):
    g.append(k)
    if len(g) == 3 or w["text"][-1] in ".?!,:…" or k == len(words) - 1 or (k + 1 < len(words) and words[k + 1]["start"] - w["end"] > 0.15): G.append([g[0], g[-1]]); g = []
c = open("compositions/captions.html").read()
c = re.sub(r"var WORDS = \[.*?\];", "var WORDS = " + json.dumps(words, ensure_ascii=False) + ";", c, flags=re.S)
c = re.sub(r"var RAW_GROUPS = \[.*?\];", "var RAW_GROUPS = " + json.dumps(G) + ";", c, flags=re.S)
open("compositions/captions.html", "w").write(c)
print(W, "D", D)
