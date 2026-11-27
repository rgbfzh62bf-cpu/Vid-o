# Builds compositions/tractions.html + index.html + captions words from assets/voice/l*.wav
# usage: python3 build.py   (needs librosa)
import json, re, librosa
CAP = ["Tu n'arrives pas à faire une seule traction ? Normal.",
       "Il en existe 5. Et chacune travaille ton dos différemment.",
       "Numéro 1 : en pronation, la classique. Les dorsaux et les biceps.",
       "Numéro 2 : en supination, paumes vers toi. Encore plus de biceps.",
       "Numéro 3 : prise neutre, paumes face à face. La plus douce pour les épaules.",
       "Numéro 4 : les australiennes, sous une barre basse. Le haut du dos. Parfait pour débuter.",
       "Numéro 5 : les négatives. Tu descends lentement. Tout le monde les zappe… mais c'est la meilleure façon de débloquer ta première traction.",
       "Alors, tu fais laquelle ? Dis-le en commentaire, et enregistre la vidéo pour ta prochaine séance !"]
BEAT = 0.6735; MOFF = 0.0
t = 0.12; lines = []; words = []
for i, cap in enumerate(CAP, 1):
    y, sr = librosa.load(f"assets/voice/l{i}.wav", sr=None); d = len(y) / sr
    iv = librosa.effects.split(y, top_db=30); s0, s1 = iv[0][0] / sr, iv[-1][1] / sr
    ws = cap.split(); Lc = sum(len(w) + 2 for w in ws); c = t + s0
    for w in ws:
        dw = (len(w) + 2) / Lc * (s1 - s0)
        if i > 1: words.append({"text": w, "start": round(c, 2), "end": round(c + dw, 2)})
        c += dw
    lines.append({"id": f"l{i}", "start": round(t, 2), "dur": round(d, 2)}); t += d + 0.15
    if i < len(CAP):
        k = -(-(t - 0.1 - MOFF) // BEAT); t = round(MOFF + k * BEAT + 0.1, 3)
C = [0] + [round(l["start"] - 0.1, 2) for l in lines[1:]]
D = round(t + 0.9, 2); LOOP = 0.4
W = {n: (C[k], C[k + 1] if k + 1 < len(C) else D) for k, n in enumerate(["hook", "intro", "pron", "sup", "neutral", "aus", "neg", "outro"])}
TEASE = 1.5
D = round(D + TEASE, 2)
PER = {"bad": 0.8, "pron": 1.25, "sup": 1.25, "neutral": 1.25, "aus": 1.1, "neg": 2.3}
VAR = [("pron", "01", "PRONATION", ["DORSAUX", "BICEPS"], "pron"), ("sup", "02", "SUPINATION", ["BICEPS", "DORSAUX"], "sup"),
       ("neutral", "03", "PRISE NEUTRE", ["DORSAUX", "ÉPAULES PRÉSERVÉES"], "neutral"), ("aus", "04", "AUSTRALIENNES", ["HAUT DU DOS", "DÉBUTANT"], None),
       ("neg", "05", "NÉGATIVES", ["FORCE", "1RE TRACTION"], None)]
HL = {"pron": ["lat", "bic"], "sup": ["bic", "lat"], "neutral": ["lat", "bic"], "aus": ["trap", "lat"], "neg": ["lat", "bic"]}
clips, js = [], []
def clip(id_, a, b, inner, cls, track, style=""):
    clips.append(f'<div id="{id_}" class="clip {cls}" data-start="{a}" data-duration="{round(b-a,2)}" data-track-index="{track}" style="{style}">{inner}</div>')
hook_html = 'PAS UNE SEULE<br /><span class="a">TRACTION</span> ?'
clip("t-hook", 0, W["hook"][1], hook_html, "ttl big", 1, "top:306px;font-size:64px")
js.append('tl.from("#t-hook", { scale: 1.12, duration: 0.35, ease: "power3.out" }, 0);')
js.append('tl.fromTo("#fig-svg", { scale: 1.3 }, { scale: 1, duration: 0.45, ease: "power3.inOut", immediateRender: true }, 2.0);')
js.append('tl.set("#fig-svg", { transformOrigin: "540px 960px" }, 0);')
js.append('tl.fromTo("#fig-svg", { x: 0 }, { x: 12, duration: 0.04, yoyo: true, repeat: 7, ease: "none" }, 1.4);')
js.append(f'reps(0, {W["hook"][1]}, "bad", 0.8);')
a, b = W["intro"]
clip("t-intro", a, b, '<div id="i-a" class="big" style="font-size:96px"><span class="a">5</span> TRACTIONS</div><div id="i-b" class="mid" style="margin-top:20px">5 RÉSULTATS</div>', "ttl", 1, "top:300px")
js.append(f'tl.from("#i-a", {{ scale: 0.4, opacity: 0, duration: 0.3, ease: "back.out(2)" }}, {a+0.05});')
js.append(f'tl.from("#i-b", {{ y: 60, opacity: 0, duration: 0.25, ease: "power3.out" }}, {a+0.5});')
js.append(f'reps({a}, {b}, "pron", 1.25);')
pb = "".join(f'<div class="seg"><i id="pf-{k}"></i></div>' for k in range(5))
clip("prog", W["pron"][0], W["outro"][0], pb, "prog", 6)
for vi, (n, num, title, chips, hands) in enumerate(VAR):
    a, b = W[n]
    js.append(f'tl.fromTo("#pf-{vi}", {{ scaleX: 0 }}, {{ scaleX: 1, duration: {round(b-a,2)}, ease: "none" }}, {a});')
    clip(f"t-{n}", a, b, f'<span class="num">{num}</span>{title}', "ttl big", 1, "top:330px")
    clip(f"c-{n}", a, b, "".join(f'<span class="chip">{c}</span>' for c in chips), "chips", 2)
    js.append(f'tl.from("#t-{n}", {{ x: -120, opacity: 0, duration: 0.25, ease: "power3.out" }}, {a+0.02});')
    js.append(f'tl.from("#c-{n} .chip", {{ y: 40, opacity: 0, duration: 0.22, stagger: 0.1, ease: "back.out(2)" }}, {a+0.25});')
    js.append(f'reps({a}, {b}, "{n}", {PER[n]});')
    js.append(f'lights({a}, {json.dumps(HL[n])});')
    if n == "neg":
        pt = round(b - 2.2, 2)
        clip("poll", pt, b, '<div class="pq">SOUS-COTÉES ?</div><div class="pr"><span>OUI</span><span>NON</span></div>', "poll", 3)
        js.append(f'tl.from("#poll .pq, #poll .pr span", {{ scale: 0.5, opacity: 0, duration: 0.25, stagger: 0.12, ease: "back.out(2.4)" }}, {pt});')
    if hands:
        ARW = {"pron": (-1, -1), "sup": (1, 1), "neutral": (0, 0)}[hands]
        def hand(x, dirv):
            ar = f'<path d="M{x} {738+dirv*10} l0 {dirv*44} m-12 {-dirv*14} l12 {dirv*14} l12 {-dirv*14}" stroke="#c8ff2e" stroke-width="6" fill="none" stroke-linecap="round"/>' if dirv else ""
            return f'<rect x="{x-17}" y="704" width="34" height="68" rx="16" fill="#c8ff2e" />' + ar
        if hands == "neutral":
            inner = '<rect x="168" y="704" width="34" height="68" rx="16" fill="#c8ff2e" /><path d="M210 738 l30 0 m-12 -12 l12 12 l-12 12" stroke="#c8ff2e" stroke-width="6" fill="none" stroke-linecap="round"/><rect x="288" y="704" width="34" height="68" rx="16" fill="#c8ff2e" /><path d="M280 738 l-30 0 m12 -12 l-12 12 l12 12" stroke="#c8ff2e" stroke-width="6" fill="none" stroke-linecap="round"/>'
        else:
            inner = hand(195, ARW[0]) + hand(295, ARW[1])
        clips.append(f'<svg id="in-{n}" class="clip full" data-start="{a}" data-duration="{round(b-a,2)}" data-track-index="3" viewBox="0 0 1080 1920"><g id="ig-{n}"><rect x="130" y="640" width="230" height="210" rx="20" fill="#15161a" stroke="#2a2c33" stroke-width="3" />{inner}<text x="245" y="832" text-anchor="middle" class="inset-lbl">PAUMES</text></g></svg>')
        js.append(f'tl.from("#ig-{n}", {{ opacity: 0, x: -40, duration: 0.25 }}, {a+0.1});')
        hands = None
    if hands:
        g, ang = hands
        clips.append(f'<svg id="in-{n}" class="clip full" data-start="{a}" data-duration="{round(b-a,2)}" data-track-index="3" viewBox="0 0 1080 1920"><g id="ig-{n}"><rect x="130" y="660" width="230" height="190" rx="20" fill="#15161a" stroke="#2a2c33" stroke-width="3" /><g transform="translate({245-g/2},738) rotate({ang})"><rect x="-17" y="-34" width="34" height="68" rx="16" fill="#c8ff2e" /></g><g transform="translate({245+g/2},738) rotate({-ang})"><rect x="-17" y="-34" width="34" height="68" rx="16" fill="#c8ff2e" /></g><text x="245" y="832" text-anchor="middle" class="inset-lbl">ÉCART MAINS</text></g></svg>')
        js.append(f'tl.from("#ig-{n}", {{ opacity: 0, x: -40, duration: 0.25 }}, {a+0.1});')
a, b = W["outro"]
clip("t-outro", a, round(D - LOOP - TEASE, 2), 'ALORS,<br /><span class="a">LAQUELLE</span><br />TU FAIS ?', "ttl big", 1, "top:300px")
rows = "".join(f'<div class="row"><b>{i}</b>{t}</div>' for i, t in enumerate(["PRONATION", "SUPINATION", "PRISE NEUTRE", "AUSTRALIENNES", "NÉGATIVES"], 1))
clip("grid", a, round(D - LOOP - TEASE, 2), rows, "grid5", 2)
clip("save", a, round(D - LOOP - TEASE, 2), '<span>ENREGISTRE-LA POUR TA SÉANCE</span>', "save", 3)
TS = round(D - LOOP - TEASE, 2)
clip("tease", TS, round(D - LOOP, 2), '<div class="tk">PROCHAIN ÉPISODE</div><div class="tt"><span class="a">5</span> ABDOS<br />5 RÉSULTATS</div>', "tease", 4)
js.append(f'tl.from("#tease .tk, #tease .tt", {{ y: 50, opacity: 0, duration: 0.3, stagger: 0.12, ease: "power3.out" }}, {TS});')
clip("t-hook2", round(D - LOOP, 2), D, hook_html, "ttl big", 1, "top:306px;font-size:64px")
js.append(f'tl.to(P, {{ show: 0, duration: 0.15 }}, {a});')
js.append(f'tl.from("#grid .row", {{ x: 160, opacity: 0, duration: 0.25, stagger: 0.12, ease: "power3.out" }}, {a+0.3});')
js.append(f'tl.from("#save span", {{ scale: 0.6, opacity: 0, duration: 0.3, ease: "back.out(2)" }}, {a+1.6});')
js.append(f'tl.set(P, {{ show: 1, mode: "bad", d: 0 }}, {round(D-LOOP,2)});')
js.append(f'tl.set(A, {{ lat: 0, bic: 0, trap: 0 }}, {round(D-LOOP,2)});')
js.append(f'tl.set("#fig-svg", {{ scale: 1.3 }}, {round(D-LOOP,2)});')
js.append(f'{json.dumps(C[1:])}.forEach(function (c) {{ tl.fromTo("#flash", {{ opacity: 0.35 }}, {{ opacity: 0, duration: 0.18, ease: "power2.out", immediateRender: false }}, c); }});')
tpl = open("tractions.tpl").read()
open("compositions/tractions.html", "w").write(tpl.replace("/*CLIPS*/", "\n    ".join(clips)).replace("/*JS*/", "\n      ".join(js)).replace("/*D*/", str(D)))
aud = "".join(f'\n      <audio id="vo-{l["id"]}" class="clip" src="assets/voice/{l["id"]}.wav" data-start="{l["start"]}" data-duration="{l["dur"]}" data-track-index="2" data-volume="1"></audio>' for l in lines)

taps = []
for n, md in [("hook", "bad"), ("intro", "pron"), ("pron", "pron"), ("sup", "sup"), ("neutral", "neutral"), ("aus", "aus"), ("neg", "neg")]:
    a0, b0 = W[n]; per = PER[md]; tt = a0 + 0.2
    while tt + per * 0.9 < b0: taps.append(round(tt + per * 0.5, 2)); tt += per + 0.1
tapx = "".join(f'\n      <audio id="tap-{k}" class="clip" src="assets/sfx/tap.mp3" data-start="{x}" data-duration="0.18" data-track-index="{7+k%2}" data-volume="0.35"></audio>' for k, x in enumerate(taps))
dingx = "".join(f'\n      <audio id="ding-{k}" class="clip" src="assets/sfx/ding.mp3" data-start="{W[n][0]-0.3:.2f}" data-duration="0.5" data-track-index="9" data-volume="0.18"></audio>' for k, n in enumerate(["pron", "sup", "neutral", "aus", "neg"]))
import subprocess
v0 = W["pron"][0]
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", "21.36", "-i", "assets/music/beat.mp3", "-t", str(D + 0.5), "-af", f"lowpass=f=1100:enable='lt(t,{v0})',volume='0.8+0.35*t/{D}':eval=frame,afade=t=in:d=0.2,afade=t=out:st={D-1.2}:d=1.2", "assets/music/bed.mp3"])
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
      <div id="tractions" data-composition-id="tractions" data-composition-src="compositions/tractions.html" data-start="0" data-duration="{D}" data-track-index="0" data-track-kind="graphics" data-width="1080" data-height="1920"></div>
{aud}
      <audio id="music" class="clip" src="assets/music/bed.mp3" data-start="0" data-duration="{D}" data-track-index="3" data-volume="0.14"></audio>{sfx}{tapx}{dingx}
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
