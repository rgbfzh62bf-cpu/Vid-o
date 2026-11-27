"""mofu-erreurs — DA « STUDIO » (vidéos face caméra du coach).
DA « ÉDITO » : cartes papier crème / encre, accent doré, Inter 900 + EB Garamond italique.
Pas de ding, pas de flash, musique lo-fi originale. Génère index.html + compositions/*.html depuis raw/edl.json."""
import json, re, subprocess

E = json.load(open("raw/edl.json"))
D = 38.68
CREAM, INK, SOFT, ACC, ACCD = "#F4EFE6", "#141414", "#8A8174", "#E0A458", "#B8742E"  # DA ÉDITO

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
W[0][0] = 0.12

def at(word, after=0.0):
    for s, t, w in W:
        if s >= after and re.sub(r"[^\wéè']", "", w.lower()) == word: return s
    raise SystemExit("word? " + word)

seg = [e["t"] for e in E]
T_E1, T_E2, T_E3, T_CTA = seg[1], seg[4], seg[6], seg[7]
T_3ERR = at("trois")
T_S1, T_S2, T_S3 = at("ajoute", T_E1), at("mieux", T_E2), at("vise", T_E3)

KEY = {"balance", "erreurs", "cardio", "muscle", "muscu", "craques", "week-end", "déficit", "assis", "8 000",
       "changement", "privé"}

# ---- captions: sentence case, 2-3 words, keyword in serif italic gradient ----
groups, cur = [], []
for i, x in enumerate(W):
    cur.append(x)
    gap = W[i + 1][0] - x[1] if i + 1 < len(W) else 9
    if re.search(r"[,.?!]$", x[2]) or gap > 0.15 or len(cur) >= 3 or len(" ".join(c[2] for c in cur)) >= 16 \
            or (i + 1 < len(W) and W[i + 1][0] in seg):
        groups.append(cur); cur = []
if cur: groups.append(cur)

cap_html, cap_js = [], []
for g, ws in enumerate(groups):
    s = ws[0][0]; e = (groups[g + 1][0][0] if g + 1 < len(groups) else D) - 0.02
    e = min(e, ws[-1][1] + 0.6)
    spans = []
    for k, (ws_, we_, w) in enumerate(ws):
        txt = w.rstrip(",.")
        if g == 0 and k == 0: txt = txt[0].upper() + txt[1:]
        key = re.sub(r"[^\wéè' -]", "", txt.lower()) in KEY
        spans.append(f'<span id="c{g}w{k}" class="w{" k" if key else ""}"><span>{txt}</span></span>')
        cap_js.append(f'tl.fromTo("#c{g}w{k}", {{opacity:0, y:14, filter:"blur(6px)"}}, {{opacity:1, y:0, filter:"blur(0px)", duration:0.22, ease:"power3.out"}}, {max(s, ws_ - 0.04):.2f});')
    cap_html.append(f'<div id="cg{g}" class="cg">{" ".join(spans)}</div>')
    cap_js.append(f'tl.set("#cg{g}", {{opacity:1, visibility:"visible"}}, {s:.2f});')
    cap_js.append(f'tl.to("#cg{g}", {{opacity:0, duration:0.1, ease:"power2.in"}}, {e - 0.1:.2f}); tl.set("#cg{g}", {{visibility:"hidden"}}, {e:.2f});')

caps = f"""<template>
  <style>
    #caps {{ position:absolute; inset:0; }}
    .cg {{ position:absolute; left:0; width:1080px; top:1150px; text-align:center; opacity:0; visibility:hidden; overflow:visible; padding:0 190px;
      font-family:"Inter",sans-serif; font-weight:700; font-size:54px; line-height:1.1; color:#fff; letter-spacing:-0.01em;
      text-shadow:0 2px 14px rgba(0,0,0,0.65), 0 1px 2px rgba(0,0,0,0.6); }}
    .cg .w {{ display:inline-block; }}
    .cg .k span {{ font-family:"EB Garamond",serif; font-style:italic; font-weight:600; font-size:64px; color:{ACC}; }}
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

# ---- camera: gentle punch-ins (1.0 / 1.07), slow drift ----
cam_js = []
for i, t in enumerate(seg):
    sc = 1.0 if i % 2 == 0 else 1.05
    if t in (T_E1, T_E2, T_E3): sc = 1.06
    if i == 7: sc = 1.0
    nxt = seg[i + 1] if i + 1 < len(seg) else D
    cam_js.append(f'tl.fromTo("#camw", {{scale:{sc}}}, {{scale:{sc + 0.03:.2f}, duration:{nxt - t - 0.02:.2f}, ease:"none"}}, {t:.2f});')
cam = f"""<template>
  <style>
    #cam {{ position:absolute; inset:0; overflow:hidden; background:#000; }}
    #camw {{ position:absolute; inset:0; transform-origin:50% 40%; }}
    #th {{ position:absolute; left:0; top:0; width:1080px; height:1920px; object-fit:cover; }}
    #vig {{ position:absolute; inset:0; background:radial-gradient(ellipse 85% 70% at 50% 45%, rgba(0,0,0,0) 55%, rgba(0,0,0,0.38) 100%),
      linear-gradient(180deg, rgba(0,0,0,0.62) 0%, rgba(0,0,0,0.38) 18%, rgba(0,0,0,0) 34%, rgba(0,0,0,0) 55%, rgba(0,0,0,0.45) 100%); }}
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
# ---- B-rolls (Pexels) on each solution ----
BR = [(T_S1, "b1"), (T_S2, "b2"), (T_S3, "b3")]
br_html = "".join(f'<video id="{n}" class="clip br" src="assets/broll/{n}.mp4" data-start="{t + 0.1:.2f}" data-duration="2.2" data-track-index="{1 + i}" muted playsinline></video>' for i, (t, n) in enumerate(BR))
br_js = "".join(f'tl.fromTo("#{n}", {{opacity:0, scale:1.08}}, {{opacity:1, scale:1.12, duration:0.25, ease:"power2.out"}}, {t + 0.1:.2f}); tl.to("#{n}", {{scale:1.16, duration:1.7, ease:"none"}}, {t + 0.35:.2f}); tl.to("#{n}", {{opacity:0, duration:0.25, ease:"power2.in"}}, {t + 2.05:.2f});' for t, n in BR)
cam = cam.replace('<div id="vig"></div>', br_html + '<div id="vig"></div>').replace('tl.set({}, {}, ' + str(D) + ');', br_js + 'tl.set({}, {}, ' + str(D) + ');').replace('#vig {', '.br { position:absolute; left:0; top:0; width:1080px; height:1920px; object-fit:cover; opacity:0; }\n    #vig {')
open("compositions/cam.html", "w").write(cam)

# ---- overlays ----
chap = [(1, T_E1, T_S1, T_E2, "Que du cardio", "2 à 3 séances", "de muscu par semaine"),
        (2, T_E2, T_S2, T_E3, "Trop peu, puis le craquage", "Un petit déficit", "tenu 7 jours sur 7"),
        (3, T_E3, T_S3, T_CTA, "Assis toute la journée", "8 000 pas", "minimum par jour")]
H, J = [], []
H.append('''<div id="hook" class="blk"><span class="kick">Perte de poids</span><div class="hk1 t">La balance</div><div class="hk2 t"><span class="it">ne bouge pas</span> ?</div>
      <div id="hsub" class="sub"><i></i>3 erreurs qui te bloquent</div></div>''')
J.append(f'''tl.fromTo("#hook .hk1", {{y:30, opacity:0, filter:"blur(8px)"}}, {{y:0, opacity:1, filter:"blur(0px)", duration:0.5, ease:"power3.out"}}, 0.0);
    tl.fromTo("#hook .hk2", {{y:30, opacity:0, filter:"blur(8px)"}}, {{y:0, opacity:1, filter:"blur(0px)", duration:0.5, ease:"power3.out"}}, 0.15);
    tl.fromTo("#hsub", {{opacity:0, y:16}}, {{opacity:1, y:0, duration:0.4, ease:"power3.out"}}, {T_3ERR - 0.1:.2f});
    tl.fromTo("#hsub i", {{scaleX:0}}, {{scaleX:1, duration:0.5, ease:"power3.inOut"}}, {T_3ERR - 0.1:.2f});
    tl.to("#hook", {{opacity:0, y:-20, filter:"blur(8px)", duration:0.3, ease:"power2.in"}}, {T_E1 - 0.3:.2f});''')
for n, t0, ts, t1, lab, s1, s2 in chap:
    H.append(f'''<div id="ch{n}" class="blk">
      <div class="num">0{n}</div>
      <div class="stack"><div id="lab{n}" class="lab"><span class="kick">Erreur</span><span class="t">{lab}</span></div>
      <div id="fix{n}" class="fix"><span class="kick">La solution</span><div class="s1">{s1}</div><div class="s2">{s2}</div></div></div>
    </div>''')
    J.append(f'''tl.set("#ch{n}", {{opacity:1}}, {t0:.2f});
    tl.fromTo("#ch{n} .num", {{opacity:0, y:40, filter:"blur(10px)"}}, {{opacity:1, y:0, filter:"blur(0px)", duration:0.55, ease:"power3.out"}}, {t0:.2f});
    tl.fromTo("#lab{n}", {{opacity:0, y:20}}, {{opacity:1, y:0, duration:0.4, ease:"power3.out"}}, {t0 + 0.25:.2f});
    tl.to("#lab{n}", {{opacity:0, y:-14, duration:0.25, ease:"power2.in"}}, {ts - 0.25:.2f});
    tl.fromTo("#ch{n}", {{backgroundColor:"{CREAM}"}}, {{backgroundColor:"{INK}", duration:0.35, ease:"power2.inOut"}}, {ts - 0.15:.2f});
    tl.fromTo("#fix{n}", {{opacity:0, y:20, filter:"blur(8px)"}}, {{opacity:1, y:0, filter:"blur(0px)", duration:0.45, ease:"power3.out"}}, {ts:.2f});
    tl.to("#ch{n}", {{opacity:0, filter:"blur(8px)", duration:0.3, ease:"power2.in"}}, {t1 - 0.3:.2f});''')
H.append('''<div id="cta" class="blk"><div class="c1 t">Commente</div><div id="ctaw" class="c2">CHANGEMENT</div>
      <div class="sub" id="c3"><i></i>je t'écris en privé</div></div>''')
J.append(f'''tl.set("#cta", {{opacity:1}}, {T_CTA:.2f});
    tl.fromTo("#cta .c1", {{opacity:0, y:24, filter:"blur(8px)"}}, {{opacity:1, y:0, filter:"blur(0px)", duration:0.45, ease:"power3.out"}}, {T_CTA:.2f});
    tl.fromTo("#ctaw", {{opacity:0, scale:0.9, filter:"blur(10px)"}}, {{opacity:1, scale:1, filter:"blur(0px)", duration:0.5, ease:"power3.out"}}, {at("changement") - 0.15:.2f});
    tl.fromTo("#ctaw", {{backgroundPosition:"0% 50%"}}, {{backgroundPosition:"100% 50%", duration:2.4, ease:"sine.inOut"}}, {at("changement") + 0.3:.2f});
    tl.fromTo("#c3", {{opacity:0, y:16}}, {{opacity:1, y:0, duration:0.4, ease:"power3.out"}}, {at("t'écris") - 0.2:.2f});
    tl.fromTo("#c3 i", {{scaleX:0}}, {{scaleX:1, duration:0.5, ease:"power3.inOut"}}, {at("t'écris") - 0.2:.2f});''')
H.append('<div id="bar"><i></i></div>')
J.append(f'tl.fromTo("#bar i", {{scaleX:0}}, {{scaleX:1, duration:{D:.2f}, ease:"none"}}, 0);')

shadow = "text-shadow:0 2px 18px rgba(0,0,0,0.55), 0 1px 2px rgba(0,0,0,0.5);"
ov = f"""<template>
  <style>
    #ov {{ position:absolute; inset:0; font-family:"Inter",sans-serif; color:{INK}; }}
    .blk {{ position:absolute; left:170px; width:740px; top:300px; text-align:center; opacity:0; padding:26px 34px 30px; border-radius:30px;
      background:{CREAM}; color:{INK}; box-shadow:0 24px 60px rgba(0,0,0,0.28), 0 2px 0 rgba(255,255,255,0.4) inset; }}
    #hook {{ opacity:1; }}
    .kick {{ display:block; font-weight:700; font-size:28px; letter-spacing:0.22em; text-transform:uppercase; color:{SOFT}; margin-bottom:8px; }}
    .t {{ font-weight:900; letter-spacing:-0.035em; line-height:0.98; }}
    .it {{ font-family:"EB Garamond",serif; font-style:italic; font-weight:500; letter-spacing:-0.01em; }}
    .hk1 {{ font-size:72px; }}
    .hk2 {{ font-size:72px; }}
    .hk2 .it {{ font-size:86px; color:{ACCD}; }}
    .sub {{ margin-top:16px; font-weight:600; font-size:32px; color:{SOFT}; }}
    .sub i {{ display:block; width:90px; height:4px; margin:0 auto 14px; border-radius:2px; background:{ACC}; transform-origin:50% 50%; }}
    .num {{ font-family:"EB Garamond",serif; font-style:italic; font-weight:500; font-size:110px; line-height:0.85; color:{ACCD}; }}
    .stack {{ display:grid; margin-top:6px; }}
    .lab, .fix {{ grid-area:1/1; }}
    .lab {{ font-size:62px; }}
    .fix {{ opacity:0; color:{CREAM}; }}
    .fix .kick {{ color:{ACC}; }}
    .fix .s1 {{ font-family:"EB Garamond",serif; font-style:italic; font-weight:500; font-size:84px; line-height:0.95; color:{ACC}; }}
    .fix .s2 {{ margin-top:8px; font-weight:700; font-size:34px; color:{CREAM}; }}
    #cta {{ background:{INK}; color:{CREAM}; }}
    .c1 {{ font-size:64px; }}
    .c2 {{ display:inline-block; margin-top:12px; font-weight:900; font-size:80px; letter-spacing:-0.02em; color:{INK}; padding:8px 36px 14px; border-radius:20px; background:{ACC}; }}
    #cta .sub {{ color:rgba(244,239,230,0.75); }}
    #bar {{ position:absolute; left:170px; width:740px; top:282px; height:4px; border-radius:2px; background:rgba(255,255,255,0.3); overflow:hidden; }}
    #bar i {{ display:block; width:100%; height:100%; background:{CREAM}; transform-origin:0 50%; }}
  </style>
  <div id="ov" data-composition-id="ov" data-width="1080" data-height="1920" data-layout-allow-overlap>
    {chr(10).join(H)}
  </div>
  <script>(function(){{ var tl = gsap.timeline({{paused:true}});
    {chr(10).join(J)}
    tl.set({{}}, {{}}, {D});
    window.__timelines["ov"] = tl; }})();</script>
</template>
"""
open("compositions/ov.html", "w").write(ov)

sfx = [f'<audio id="wh{i}" class="clip" src="assets/sfx/whoosh.mp3" data-start="{max(0, t - 0.25):.2f}" data-duration="0.45" data-track-index="4" data-volume="0.1"></audio>'
       for i, t in enumerate((T_E1, T_E2, T_E3, T_CTA))]
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
      <audio id="music" class="clip" src="assets/music/lofi.mp3" data-start="0" data-duration="{D}" data-track-index="7" data-volume="0.1"></audio>
      {chr(10).join("      " + s for s in sfx).strip()}
    </div>
    <script>window.__timelines = window.__timelines || {{}};</script>
  </body>
</html>
"""
open("index.html", "w").write(idx)
print("ok groups", len(groups))
