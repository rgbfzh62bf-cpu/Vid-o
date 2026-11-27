"""mofu-erreurs: face cam + overlays. Generates index.html + compositions/*.html from raw/edl.json."""
import json, re, subprocess

E = json.load(open("raw/edl.json"))
D = 38.68
LIME, RED = "#c8ff2e", "#ff4d4d"

# ---- words (fix tokens) ----
W = []
for e in E:
    for s, t, w in e["words"]:
        if W and (w.startswith("'") or w.startswith("-")):
            W[-1][1] = t; W[-1][2] += w; continue
        W.append([s, t, w])
for i, x in enumerate(W):
    if x[2] == "mi": W[i - 1][2] = "8 000"; W[i - 1][1] = x[1]; x[2] = None
W = [x for x in W if x[2]]
W[0][0] = 0.12  # first caption not at 0

def at(word, after=0.0):
    for s, t, w in W:
        if s >= after and re.sub(r"[^\wéè']", "", w.lower()) == word: return s
    raise SystemExit("word? " + word)

seg = [e["t"] for e in E]
T_E1, T_E2, T_E3, T_CTA = seg[1], seg[4], seg[6], seg[7]
T_3ERR = at("trois")
T_S1 = at("ajoute", T_E1)
T_S2 = at("mieux", T_E2)
T_S3 = at("vise", T_E3)

KEY = {"balance", "bouge", "trois", "erreurs", "cardio", "muscle", "renforcement", "muscu", "craques", "week-end",
       "compenses", "déficit", "bouges", "assis", "8 000", "pas", "changement", "privé", "7"}

# ---- caption groups ----
groups, cur = [], []
for i, x in enumerate(W):
    cur.append(x)
    gap = W[i + 1][0] - x[1] if i + 1 < len(W) else 9
    if re.search(r"[,.?!]$", x[2]) or gap > 0.15 or len(cur) >= 4 or len(" ".join(c[2] for c in cur)) >= 17 or (i + 1 < len(W) and W[i + 1][0] in seg):
        groups.append(cur); cur = []
if cur: groups.append(cur)

cap_html, cap_js = [], []
for g, ws in enumerate(groups):
    s = ws[0][0]; e = (groups[g + 1][0][0] if g + 1 < len(groups) else D) - 0.02
    e = min(e, ws[-1][1] + 0.6)
    spans = []
    for k, (ws_, we_, w) in enumerate(ws):
        txt = w.rstrip(",.")
        key = re.sub(r"[^\wéè' -]", "", txt.lower()) in KEY
        spans.append(f'<span id="c{g}w{k}" class="w{" k" if key else ""}">{txt}</span>')
        cap_js.append(f'tl.fromTo("#c{g}w{k}", {{opacity:0.35}}, {{opacity:1, duration:0.08}}, {ws_ - s:.2f} + {s:.2f});')
        if key: cap_js.append(f'tl.fromTo("#c{g}w{k}", {{scale:1}}, {{scale:1.12, duration:0.12, ease:"back.out(3)", yoyo:true, repeat:1}}, {ws_:.2f});')
    cap_html.append(f'<div id="cg{g}" class="cg">{" ".join(spans)}</div>')
    cap_js.append(f'tl.set("#cg{g}", {{opacity:1, visibility:"visible"}}, {s:.2f}); tl.fromTo("#cg{g}", {{y:18}}, {{y:0, duration:0.18, ease:"expo.out"}}, {s:.2f});')
    cap_js.append(f'tl.set("#cg{g}", {{opacity:0, visibility:"hidden"}}, {e:.2f});')

caps = f"""<template>
  <style>
    #caps {{ position:absolute; inset:0; }}
    .cg {{ position:absolute; left:0; width:1080px; top:1096px; text-align:center; opacity:0; visibility:hidden; overflow:visible;
      font-family:"Archivo Black",sans-serif; font-size:58px; line-height:1.05; text-transform:uppercase; color:#fff; padding:0 200px 0 180px;
      text-shadow:0 4px 0 #000, 0 0 18px rgba(0,0,0,0.85); }}
    .cg .w {{ display:inline-block; }}
    .cg .k {{ color:{LIME}; }}
  </style>
  <div id="caps" data-composition-id="caps" data-width="1080" data-height="1920" data-layout-allow-overlap>
    {chr(10).join(cap_html)}
  </div>
  <script>(function(){{ var tl = gsap.timeline({{paused:true}});
    {chr(10).join(cap_js)}
    tl.set({{}}, {{}}, {D});
    window.__timelines["caps"] = tl; }})();</script>
</template>
"""
open("compositions/caps.html", "w").write(caps)

# ---- camera: punch-ins per cut ----
cam_js = []
scales = []
for i, t in enumerate(seg):
    sc = 1.0 if i % 2 == 0 else 1.12
    if t in (T_E1, T_E2, T_E3): sc = 1.2
    if i == 7: sc = 1.06
    scales.append(sc)
    cam_js.append(f'tl.set("#camw", {{scale:{sc}}}, {t:.2f});')
cam_js.insert(1, 'tl.fromTo("#camw", {scale:1.0}, {scale:1.08, duration:%.2f, ease:"none"}, 0.01);' % (seg[1] - 0.05))
cam_js.append(f'tl.to("#camw", {{scale:1.16, duration:{D - T_CTA - 0.1:.2f}, ease:"power1.inOut"}}, {T_CTA + 0.05:.2f});')
cam = f"""<template>
  <style>
    #cam {{ position:absolute; inset:0; overflow:hidden; background:#000; }}
    #camw {{ position:absolute; inset:0; transform-origin:50% 40%; }}
    #th {{ position:absolute; left:0; top:0; width:1080px; height:1920px; object-fit:cover; }}
    #vig {{ position:absolute; inset:0; background:linear-gradient(180deg, rgba(0,0,0,0.55) 0%, rgba(0,0,0,0) 34%, rgba(0,0,0,0) 52%, rgba(0,0,0,0.5) 100%); }}
  </style>
  <div id="cam" data-composition-id="cam" data-width="1080" data-height="1920">
    <div id="camw"><video id="th" class="clip" src="assets/th.mp4" data-start="0" data-duration="{D}" data-track-index="0" muted playsinline></video></div>
    <div id="vig"></div>
  </div>
  <script>(function(){{ var tl = gsap.timeline({{paused:true}});
    {chr(10).join(cam_js)}
    tl.set({{}}, {{}}, {D});
    window.__timelines["cam"] = tl; }})();</script>
</template>
"""
open("compositions/cam.html", "w").write(cam)

# ---- overlays (top band) ----
chap = [(1, T_E1, T_S1, T_E2, "QUE DU CARDIO", "+ 2 À 3 SÉANCES", "DE MUSCU / SEMAINE"),
        (2, T_E2, T_S2, T_E3, "TROP PEU, PUIS CRAQUAGE", "PETIT DÉFICIT", "TENU 7 JOURS / 7"),
        (3, T_E3, T_S3, T_CTA, "ASSIS TOUTE LA JOURNÉE", "8 000 PAS", "MINIMUM PAR JOUR")]
ov_html, ov_js = [], []
ov_html.append(f'''<div id="hook" class="blk"><div class="h1">LA BALANCE</div><div class="h2">NE BOUGE PAS ?</div>
      <div id="hchip" class="chip">3 ERREURS QUI TE BLOQUENT</div></div>''')
ov_js.append(f'''tl.fromTo("#hook .h1", {{y:-40, opacity:0}}, {{y:0, opacity:1, duration:0.35, ease:"expo.out"}}, 0.0);
    tl.fromTo("#hook .h2", {{scale:1.6, opacity:0}}, {{scale:1, opacity:1, duration:0.4, ease:"back.out(2)"}}, 0.18);
    tl.fromTo("#hchip", {{scale:0, opacity:0}}, {{scale:1, opacity:1, duration:0.35, ease:"back.out(2.4)"}}, {T_3ERR:.2f});
    tl.to("#hook", {{opacity:0, y:-30, duration:0.2, ease:"power2.in"}}, {T_E1 - 0.2:.2f});''')
for n, t0, ts, t1, lab, s1, s2 in chap:
    ov_html.append(f'''<div id="ch{n}" class="blk">
      <div class="tag">ERREUR <b>{n}</b><i>/3</i></div>
      <div id="lab{n}" class="lab"><span class="x">✕</span>{lab}</div>
      <div id="fix{n}" class="fix"><div class="ok">LA SOLUTION</div><div class="s1">{s1}</div><div class="s2">{s2}</div></div>
    </div>''')
    ov_js.append(f'''tl.set("#ch{n}", {{opacity:1}}, {t0:.2f});
    tl.fromTo("#ch{n} .tag", {{scale:2.2, opacity:0}}, {{scale:1, opacity:1, duration:0.35, ease:"expo.out"}}, {t0:.2f});
    tl.fromTo("#lab{n}", {{x:-60, opacity:0}}, {{x:0, opacity:1, duration:0.3, ease:"expo.out"}}, {t0 + 0.35:.2f});
    tl.to("#lab{n}", {{x:60, opacity:0, duration:0.2, ease:"power2.in"}}, {ts - 0.2:.2f});
    tl.fromTo("#fix{n}", {{scale:0.6, opacity:0}}, {{scale:1, opacity:1, duration:0.4, ease:"back.out(2)"}}, {ts:.2f});
    tl.to("#ch{n}", {{opacity:0, duration:0.2, ease:"power2.in"}}, {t1 - 0.2:.2f});''')
ov_js.append('tl.fromTo("#fix3 .s1 b", {innerText:0}, {innerText:8000, duration:0.9, ease:"power2.out", snap:{innerText:100}, '
             'onUpdate:function(){ var e=document.querySelector("#fix3 .s1 b"); e.textContent=Math.round(+e.textContent||0).toLocaleString("fr-FR").replace(/\\u202f|\\u00a0/g," "); }}, %.2f);' % T_S3)
ov_html[-1] = ov_html[-1].replace('<div class="s1">8 000 PAS</div>', '<div class="s1"><b>8 000</b> PAS</div>')
ov_html.append('''<div id="cta" class="blk"><div class="c1">COMMENTE</div><div id="ctap" class="pill">CHANGEMENT</div>
      <div class="c3">JE T'ÉCRIS EN PRIVÉ</div></div>''')
ov_js.append(f'''tl.set("#cta", {{opacity:1}}, {T_CTA:.2f});
    tl.fromTo("#cta .c1", {{y:-30, opacity:0}}, {{y:0, opacity:1, duration:0.3, ease:"expo.out"}}, {T_CTA:.2f});
    tl.fromTo("#ctap", {{scale:0, rotation:-6}}, {{scale:1, rotation:-3, duration:0.45, ease:"back.out(2.6)"}}, {at("changement") - 0.1:.2f});
    tl.to("#ctap", {{scale:1.08, duration:0.3, ease:"sine.inOut", yoyo:true, repeat:3}}, {at("changement") + 0.5:.2f});
    tl.fromTo("#cta .c3", {{opacity:0, y:20}}, {{opacity:1, y:0, duration:0.3, ease:"expo.out"}}, {at("t'écris") - 0.2:.2f});''')
# progress dots
ov_html.append('<div id="prog">' + "".join(f'<i id="pd{n}"></i>' for n in (1, 2, 3)) + '</div>')
ov_js.append(f'tl.fromTo("#prog", {{opacity:0}}, {{opacity:1, duration:0.3}}, {T_E1:.2f}); tl.to("#prog", {{opacity:0, duration:0.2}}, {T_CTA - 0.2:.2f});')
for n, t0, *_ in chap:
    ov_js.append(f'tl.to("#pd{n}", {{backgroundColor:"{LIME}", scaleX:1, duration:0.3}}, {t0:.2f});')
# flash on chapters
ov_js.append('tl.set("#flash", {opacity:0}, 0);'); ov_js += [f'tl.fromTo("#flash", {{opacity:0.55}}, {{opacity:0, duration:0.25, ease:"power2.out"}}, {t:.2f});' for t in (T_E1, T_E2, T_E3, T_CTA)]

ov = f"""<template>
  <style>
    #ov {{ position:absolute; inset:0; font-family:"Archivo Black",sans-serif; color:#fff; text-transform:uppercase; }}
    .blk {{ position:absolute; left:150px; width:760px; top:300px; text-align:center; opacity:0; }}
    #hook {{ opacity:1; }}
    .h1 {{ font-size:66px; line-height:1; text-shadow:0 5px 0 #000, 0 0 24px rgba(0,0,0,0.7); }}
    .h2 {{ font-size:72px; line-height:1; color:{LIME}; margin-top:6px; text-shadow:0 5px 0 #000, 0 0 24px rgba(0,0,0,0.7); }}
    .chip {{ display:inline-block; margin-top:22px; font-family:"Montserrat",sans-serif; font-weight:800; font-size:34px; color:#0b0b0d;
      background:{LIME}; border-radius:999px; padding:12px 28px; }}
    .tag {{ display:inline-block; font-size:44px; letter-spacing:0.08em; background:{RED}; color:#fff; padding:10px 26px 12px; border-radius:14px;
      box-shadow:0 8px 24px rgba(0,0,0,0.45); }}
    .tag b {{ font-size:56px; margin-left:6px; }} .tag i {{ font-style:normal; font-size:30px; opacity:0.75; }}
    .lab, .fix {{ position:absolute; left:0; width:760px; top:110px; }}
    .lab {{ font-size:50px; line-height:1.02; text-shadow:0 5px 0 #000, 0 0 24px rgba(0,0,0,0.8); }}
    .lab .x {{ color:{RED}; margin-right:14px; }}
    .fix {{ opacity:0; }}
    .fix .ok {{ display:inline-block; font-family:"Montserrat",sans-serif; font-weight:800; font-size:30px; letter-spacing:0.12em; color:#0b0b0d;
      background:{LIME}; border-radius:999px; padding:8px 24px; }}
    .fix .s1 {{ margin-top:12px; font-size:70px; line-height:1; color:{LIME}; text-shadow:0 5px 0 #000, 0 0 24px rgba(0,0,0,0.8); }}
    .fix .s2 {{ margin-top:6px; font-family:"Montserrat",sans-serif; font-weight:800; font-size:38px; text-shadow:0 3px 0 #000, 0 0 18px rgba(0,0,0,0.9); }}
    #cta {{ top:290px; }}
    .c1 {{ font-size:70px; text-shadow:0 5px 0 #000, 0 0 24px rgba(0,0,0,0.8); }}
    .pill {{ display:inline-block; margin-top:14px; font-size:72px; color:#0b0b0d; background:{LIME}; border-radius:24px; padding:10px 34px 14px;
      box-shadow:0 0 40px rgba(200,255,46,0.55), 0 10px 0 #000; }}
    .c3 {{ margin-top:22px; font-family:"Montserrat",sans-serif; font-weight:800; font-size:36px; text-shadow:0 3px 0 #000, 0 0 18px rgba(0,0,0,0.9); }}
    #prog {{ position:absolute; left:390px; width:300px; top:258px; display:flex; gap:12px; opacity:0; }}
    #prog i {{ flex:1; height:10px; border-radius:5px; background:rgba(255,255,255,0.3); }}
    #flash {{ position:absolute; inset:0; background:#fff; opacity:0; }}
  </style>
  <div id="ov" data-composition-id="ov" data-width="1080" data-height="1920" data-layout-allow-overlap>
    {chr(10).join(ov_html)}
    <div id="flash"></div>
  </div>
  <script>(function(){{ var tl = gsap.timeline({{paused:true}});
    {chr(10).join(ov_js)}
    tl.set({{}}, {{}}, {D});
    window.__timelines["ov"] = tl; }})();</script>
</template>
"""
open("compositions/ov.html", "w").write(ov)

# ---- audio ----
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", "21.36", "-i", "assets/music/beat.mp3", "-t", str(D + 0.3),
                "-af", f"lowpass=f=2600,afade=t=in:d=0.3,afade=t=out:st={D - 1.5}:d=1.5", "assets/music/bed.mp3"], check=True)
sfx = []
for i, t in enumerate((T_E1, T_E2, T_E3, T_CTA)):
    sfx.append(f'<audio id="wh{i}" class="clip" src="assets/sfx/whoosh.mp3" data-start="{max(0, t - 0.2):.2f}" data-duration="0.45" data-track-index="4" data-volume="0.22"></audio>')
for i, t in enumerate((T_3ERR, T_S1, T_S2, T_S3)):
    sfx.append(f'<audio id="dg{i}" class="clip" src="assets/sfx/ding.mp3" data-start="{t:.2f}" data-duration="0.52" data-track-index="5" data-volume="0.12"></audio>')

idx = f"""<!doctype html>
<html lang="fr">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: #000; }}
      #root {{ position: relative; width: 100%; height: 100%; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{D}" data-width="1080" data-height="1920">
      <div id="cam" data-composition-id="cam" data-composition-src="compositions/cam.html" data-start="0" data-duration="{D}" data-track-index="0" data-track-kind="graphics" data-width="1080" data-height="1920"></div>
      <div id="ov" data-composition-id="ov" data-composition-src="compositions/ov.html" data-start="0" data-duration="{D}" data-track-index="1" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index:2"></div>
      <div id="caps" data-composition-id="caps" data-composition-src="compositions/caps.html" data-start="0" data-duration="{D}" data-track-index="2" data-track-kind="captions" data-width="1080" data-height="1920" style="z-index:3"></div>
      <audio id="vo" class="clip" src="assets/voice.wav" data-start="0" data-duration="{D}" data-track-index="6" data-volume="1"></audio>
      <audio id="music" class="clip" src="assets/music/bed.mp3" data-start="0" data-duration="{D}" data-track-index="7" data-volume="0.07"></audio>
      {chr(10).join("      " + s for s in sfx).strip()}
    </div>
    <script>window.__timelines = window.__timelines || {{}};</script>
  </body>
</html>
"""
open("index.html", "w").write(idx)
print("ok groups", len(groups), "E1", T_E1, "S1", T_S1, "E2", T_E2, "S2", T_S2, "E3", T_E3, "S3", T_S3, "CTA", T_CTA)
