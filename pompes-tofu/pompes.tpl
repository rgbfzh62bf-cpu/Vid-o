<template>
  <style>
    #pompes { position: absolute; inset: 0; overflow: hidden; font-family: "Archivo Black", sans-serif; color: #fff;
      background: radial-gradient(ellipse 80% 55% at 50% 52%, #1d1f24 0%, #0b0b0d 70%); }
    #pompes .full { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; }
    .ttl { position: absolute; left: 150px; width: 780px; text-align: center; line-height: 0.95; text-transform: uppercase; }
    .ttl .a { color: #c8ff2e; }
    .big { font-size: 72px; letter-spacing: -0.02em; }
    .mid { font-size: 76px; }
    .num { display: block; font-size: 44px; color: #c8ff2e; letter-spacing: 0.12em; margin-bottom: 14px; }
    .chips { position: absolute; left: 150px; width: 780px; top: 520px; display: flex; justify-content: center; flex-wrap: wrap; gap: 16px; }
    .chip { font-family: "Montserrat", sans-serif; font-weight: 800; font-size: 34px; padding: 12px 26px; border-radius: 999px;
      background: rgba(200,255,46,0.14); border: 3px solid #c8ff2e; color: #c8ff2e; letter-spacing: 0.04em; }
    .inset-lbl { font-family: "Montserrat", sans-serif; font-weight: 800; font-size: 28px; fill: #c4c4cc; letter-spacing: 2px; }
    .grid5 { position: absolute; left: 170px; width: 740px; top: 590px; display: grid; gap: 12px; }
    .row { display: flex; align-items: center; gap: 24px; font-size: 40px; padding: 8px 22px; border-radius: 22px; background: #17181c; border: 3px solid #2a2c33; }
    .row b { color: #0b0b0d; background: #c8ff2e; border-radius: 14px; width: 52px; height: 52px; display: flex; align-items: center; justify-content: center; font-size: 34px; }
    .save { position: absolute; left: 150px; width: 780px; top: 1040px; text-align: center; }
    .save span { display: inline-block; font-family: "Montserrat", sans-serif; font-weight: 800; font-size: 34px; color: #0b0b0d; background: #c8ff2e; border-radius: 999px; padding: 14px 30px; }
    #flash { background: #fff; opacity: 0; }
  </style>
  <div id="pompes" data-composition-id="pompes" data-width="1080" data-height="1920" data-layout-allow-overlap>
    <svg id="fig-svg" class="clip full" data-start="0" data-duration="/*D*/" data-track-index="0" viewBox="0 0 1080 1920">
      <defs>
        <filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="9" result="b" /><feMerge><feMergeNode in="b" /><feMergeNode in="SourceGraphic" /></feMerge></filter>
      </defs>
      <g id="figwrap" transform="matrix(1.45,0,0,1.45,-243,-430.5)">
        <g id="fig">
          <line x1="180" y1="1090" x2="900" y2="1090" stroke="#2d2f36" stroke-width="4" />
          <ellipse id="shadow" cx="520" cy="1094" rx="220" ry="10" fill="#000" opacity="0.5" />
          <g id="bench" opacity="0"><rect x="230" y="990" width="190" height="22" rx="7" fill="#3a3d46" /><rect x="250" y="1012" width="14" height="78" fill="#3a3d46" /><rect x="386" y="1012" width="14" height="78" fill="#3a3d46" /></g>
          <g id="body" stroke-linecap="round" stroke-linejoin="round" fill="none">
            <polyline id="arm-far" stroke="#6d6f78" stroke-width="16" />
            <polyline id="leg-far" stroke="#6d6f78" stroke-width="22" />
            <polyline id="leg" stroke="#fff" stroke-width="25" />
            <line id="torso" stroke="#fff" stroke-width="32" />
            <line id="m-chest" stroke="#c8ff2e" stroke-width="20" opacity="0" filter="url(#glow)" />
            <circle id="m-delt" r="17" fill="#c8ff2e" stroke="none" opacity="0" filter="url(#glow)" />
            <polyline id="arm" stroke="#fff" stroke-width="18" />
            <line id="m-tri" stroke="#c8ff2e" stroke-width="16" opacity="0" filter="url(#glow)" />
            <circle id="head" r="31" fill="#fff" stroke="none" />
          </g>
        </g>
      </g>
    </svg>
    /*CLIPS*/
    <div id="flash" class="clip full" data-start="0" data-duration="/*D*/" data-track-index="9"></div>
  </div>
  <script>
    (function () {
      var G = 1090, L = 395, LK = 275, UA = 82, FA = 78, HAND = [700, G - 8];
      var P = { d: 0, mode: "classic", show: 1 };
      var A = { chest: 0, delt: 0, tri: 0 };
      function $(id) { return document.getElementById(id); }
      function ik(h, a, l1, l2, dir) {
        var dx = a[0] - h[0], dy = a[1] - h[1], dd = Math.min(Math.hypot(dx, dy), l1 + l2 - 0.01);
        var base = Math.atan2(dy, dx), c = (l1 * l1 + dd * dd - l2 * l2) / (2 * l1 * dd);
        var ang = Math.acos(Math.max(-1, Math.min(1, c)));
        return [h[0] + l1 * Math.cos(base - dir * ang), h[1] + l1 * Math.sin(base - dir * ang)];
      }
      function pts(a) { return a.map(function (p) { return p[0].toFixed(1) + "," + p[1].toFixed(1); }).join(" "); }
      function lerp(p, q, t) { return [p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t]; }
      function L2(id, p, q) { var e = $(id); e.setAttribute("x1", p[0]); e.setAttribute("y1", p[1]); e.setAttribute("x2", q[0]); e.setAttribute("y2", q[1]); }
      function render() {
        var m = P.mode, d = P.d, depth = (m === "diamond" ? 100 : 92);
        var shY = G - (157 - depth * d), base, len, sh, hip, knee, ankle, toe;
        if (m === "knees") {
          base = [430, G - 12]; len = LK;
          sh = [base[0] + Math.sqrt(len * len - Math.pow(base[1] - shY, 2)), shY];
          hip = lerp(base, sh, 125 / 275); knee = base; ankle = [base[0] - 105, base[1] - 50]; toe = [ankle[0] - 22, ankle[1] + 6];
        } else {
          base = m === "decline" ? [330, G - 112] : [328, G - 10]; len = L;
          sh = [base[0] + Math.sqrt(len * len - Math.pow(base[1] - shY, 2)), shY];
          ankle = base; knee = lerp(base, sh, 120 / 395); hip = lerp(base, sh, 245 / 395); toe = [ankle[0] - 8, ankle[1] + 10];
          if (m === "bad") { var sag = 30 + 22 * d; hip = [hip[0], hip[1] + sag]; knee = [knee[0], knee[1] + sag * 0.45]; }
        }
        var dx = sh[0] - hip[0], dy = sh[1] - hip[1], n = Math.hypot(dx, dy), ux = dx / n, uy = dy / n;
        var hd = [sh[0] + ux * 44 - uy * -6, sh[1] + uy * 44 - 10];
        if (m === "bad") hd = [hd[0] + 6, hd[1] + 16];
        var el = ik(sh, HAND, UA, FA, -1);
        $("leg").setAttribute("points", pts([toe, ankle, knee, hip]));
        $("leg-far").setAttribute("points", pts([[toe[0] - 6, toe[1]], [ankle[0] - 6, ankle[1]], [knee[0] - 6, knee[1] + 2], [hip[0] - 4, hip[1]]]));
        L2("torso", hip, sh);
        $("arm").setAttribute("points", pts([sh, el, HAND]));
        $("arm-far").setAttribute("points", pts([[sh[0] - 6, sh[1] + 2], [el[0] - 8, el[1] + 2], [HAND[0] - 10, HAND[1]]]));
        $("head").setAttribute("cx", hd[0]); $("head").setAttribute("cy", hd[1]);
        var cs = lerp(hip, sh, 0.55), ce = lerp(hip, sh, 0.92);
        L2("m-chest", [cs[0] - uy * -14, cs[1] + ux * 14], [ce[0] - uy * -14, ce[1] + ux * 14]);
        $("m-delt").setAttribute("cx", sh[0]); $("m-delt").setAttribute("cy", sh[1]);
        L2("m-tri", lerp(sh, el, 0.15), lerp(sh, el, 0.9));
        var k = 0.35 + 0.65 * d;
        ["chest", "delt", "tri"].forEach(function (x) { $("m-" + x).setAttribute("opacity", A[x] * k); });
        $("bench").setAttribute("opacity", m === "decline" ? 1 : 0);
        $("fig").setAttribute("opacity", P.show);
      }
      var tl = gsap.timeline({ paused: true, onUpdate: render });
      function reps(t0, t1, mode, per) {
        tl.set(P, { mode: mode, d: 0 }, t0);
        for (var t = t0 + 0.2; t + per * 0.9 < t1; t += per + 0.1) {
          tl.to(P, { d: 1, duration: per * 0.5, ease: "power2.inOut" }, t);
          tl.to(P, { d: 0, duration: per * 0.42, ease: "power2.out" }, t + per * 0.56);
        }
      }
      function lights(t, list) {
        tl.set(A, { chest: 0, delt: 0, tri: 0 }, t);
        var o = { duration: 0.3 }; list.forEach(function (x) { o[x] = 1; });
        tl.to(A, o, t + 0.6);
      }
      /*JS*/
      tl.set({}, {}, /*D*/);
      render();
      window.__timelines["pompes"] = tl;
    })();
  </script>
</template>
