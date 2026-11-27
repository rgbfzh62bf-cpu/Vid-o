<template>
  <style>
    #tractions { position: absolute; inset: 0; overflow: hidden; font-family: "Archivo Black", sans-serif; color: #fff;
      background: radial-gradient(ellipse 80% 55% at 50% 52%, #1d1f24 0%, #0b0b0d 70%); }
    #tractions .full { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; }
    .ttl { position: absolute; left: 150px; width: 780px; text-align: center; line-height: 0.95; text-transform: uppercase; }
    .ttl .a { color: #c8ff2e; }
    .big { font-size: 72px; letter-spacing: -0.02em; }
    .mid { font-size: 76px; }
    .num { display: block; font-size: 44px; color: #c8ff2e; letter-spacing: 0.12em; margin-bottom: 14px; }
    .chips { position: absolute; left: 150px; width: 780px; top: 548px; display: flex; justify-content: center; flex-wrap: wrap; gap: 16px; }
    .chip { font-family: "Montserrat", sans-serif; font-weight: 800; font-size: 34px; padding: 12px 26px; border-radius: 999px;
      background: rgba(200,255,46,0.14); border: 3px solid #c8ff2e; color: #c8ff2e; letter-spacing: 0.04em; }
    .inset-lbl { font-family: "Montserrat", sans-serif; font-weight: 800; font-size: 28px; fill: #c4c4cc; letter-spacing: 2px; }
    .grid5 { position: absolute; left: 170px; width: 740px; top: 590px; display: grid; gap: 12px; }
    .row { display: flex; align-items: center; gap: 24px; font-size: 40px; padding: 8px 22px; border-radius: 22px; background: #17181c; border: 3px solid #2a2c33; }
    .row b { color: #0b0b0d; background: #c8ff2e; border-radius: 14px; width: 52px; height: 52px; display: flex; align-items: center; justify-content: center; font-size: 34px; }
    .save { position: absolute; left: 150px; width: 780px; top: 1040px; text-align: center; }
    .save span { display: inline-block; font-family: "Montserrat", sans-serif; font-weight: 800; font-size: 34px; color: #0b0b0d; background: #c8ff2e; border-radius: 999px; padding: 14px 30px; }
    #flash { background: #fff; opacity: 0; }
    .prog { position: absolute; left: 190px; width: 700px; top: 292px; height: 14px; display: flex; gap: 10px; }
    .prog .seg { flex: 1; height: 14px; border-radius: 7px; background: #2a2c33; overflow: hidden; }
    .prog .seg i { display: block; width: 100%; height: 100%; background: #c8ff2e; transform-origin: 0 50%; transform: scaleX(0); }
    .poll { position: absolute; left: 70px; width: 330px; top: 700px; text-align: center; }
    .poll .pq { font-size: 46px; line-height: 1.05; color: #fff; }
    .poll .pr { margin-top: 18px; display: flex; flex-direction: column; align-items: center; gap: 14px; }
    .poll .pr span { font-family: "Montserrat", sans-serif; font-weight: 800; font-size: 40px; padding: 12px 40px; border-radius: 999px; border: 4px solid #c8ff2e; color: #c8ff2e; }
    .poll .pr span:last-child { border-color: #ff3b3b; color: #ff3b3b; }
    .tease { position: absolute; left: 150px; width: 780px; top: 640px; text-align: center; }
    .tease .tk { font-family: "Montserrat", sans-serif; font-weight: 800; font-size: 36px; color: #c8ff2e; letter-spacing: 0.14em; }
    .tease .tt { margin-top: 16px; font-size: 96px; line-height: 0.95; }
    .tease .a { color: #c8ff2e; }
  </style>
  <div id="tractions" data-composition-id="tractions" data-width="1080" data-height="1920" data-layout-allow-overlap>
    <div id="figclip" class="clip full" data-start="0" data-duration="/*D*/" data-track-index="0">
    <svg id="fig-svg" class="full" viewBox="0 0 1080 1920">
      <defs>
        <radialGradient id="sh"><stop offset="0" stop-color="#000" stop-opacity="0.75" /><stop offset="1" stop-color="#000" stop-opacity="0" /></radialGradient>
        <filter id="bodyglow" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur in="SourceAlpha" stdDeviation="7" result="b" /><feFlood flood-color="#c8ff2e" flood-opacity="0.28" /><feComposite in2="b" operator="in" result="g" /><feMerge><feMergeNode in="g" /><feMergeNode in="SourceGraphic" /></feMerge></filter>
        <filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="9" result="b" /><feMerge><feMergeNode in="b" /><feMergeNode in="SourceGraphic" /></feMerge></filter>
      </defs>
      <g id="figwrap" transform="matrix(1,0,0,1,0,48)">
        <g id="fig">
          <line x1="180" y1="1200" x2="900" y2="1200" stroke="#2d2f36" stroke-width="4" />
          <ellipse id="shadow" cx="540" cy="1206" rx="160" ry="14" fill="url(#sh)" />
          <g id="rig"><rect x="372" y="612" width="14" height="588" fill="#3a3d46" /><rect x="694" y="612" width="14" height="588" fill="#3a3d46" /><rect x="372" y="634" width="336" height="12" rx="6" fill="#8a8d96" /></g>
          <g id="low" opacity="0"><rect x="612" y="940" width="12" height="260" fill="#3a3d46" /><rect x="740" y="940" width="12" height="260" fill="#3a3d46" /><rect x="600" y="934" width="170" height="12" rx="6" fill="#8a8d96" /></g>
          <g id="body" stroke-linecap="round" stroke-linejoin="round" fill="none" filter="url(#bodyglow)">
            <polyline id="arm-far" stroke="#6d6f78" stroke-width="16" />
            <polyline id="leg-far" stroke="#6d6f78" stroke-width="22" />
            <polyline id="leg" stroke="#fff" stroke-width="25" />
            <line id="torso" stroke="#fff" stroke-width="32" />
            <line id="m-lat" stroke="#c8ff2e" stroke-width="20" opacity="0" filter="url(#glow)" />
            <circle id="m-trap" r="18" fill="#c8ff2e" stroke="none" opacity="0" filter="url(#glow)" />
            <polyline id="arm" stroke="#fff" stroke-width="18" />
            <line id="m-bic" stroke="#c8ff2e" stroke-width="15" opacity="0" filter="url(#glow)" />
            <circle id="head" r="31" fill="#fff" stroke="none" />
          </g>
        </g>
      </g>
    </svg>
    </div>
    /*CLIPS*/
    <div id="flash" class="clip full" data-start="0" data-duration="/*D*/" data-track-index="9"></div>
  </div>
  <script>
    (function () {
      var G = 1200, BAR = [548, 640], LOWBAR = [700, 940], UA = 82, FA = 78, TORSO = 150, THIGH = 125, SHIN = 120;
      var P = { d: 0, mode: "pron", show: 1 };
      var A = { lat: 0, bic: 0, trap: 0 };
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
        var m = P.mode, d = P.d, hand, sh, hip, knee, ank, hd, el;
        if (m === "aus") {
          hand = [LOWBAR[0], LOWBAR[1] + 4]; ank = [330, G - 10];
          var shy = G - (112 + 120 * d), L = 395;
          sh = [ank[0] + Math.sqrt(L * L - Math.pow(ank[1] - shy, 2)), shy];
          knee = lerp(ank, sh, 120 / 395); hip = lerp(ank, sh, 245 / 395);
          var ux = (sh[0] - hip[0]) / 150, uy = (sh[1] - hip[1]) / 150;
          hd = [sh[0] + ux * 44 + 8, sh[1] + uy * 44 - 18];
          el = ik(sh, hand, UA, FA, 1);
        } else {
          hand = [BAR[0] + 6, BAR[1] + 4];
          var lift = m === "bad" ? 0.22 : 1;
          sh = [BAR[0] - 20 - 4 * d * lift, BAR[1] + 160 - 132 * d * lift];
          hip = [sh[0] - 8, sh[1] + TORSO]; knee = [hip[0] + 12, hip[1] + THIGH - 6]; ank = [knee[0] - 42, knee[1] + SHIN - 14];
          hd = [sh[0] - 4, sh[1] - 47];
          el = ik(sh, hand, UA, FA, -1);
        }
        var toe = m === "aus" ? [ank[0] - 6, ank[1] - 18] : [ank[0] - 10, ank[1] + 20];
        $("leg").setAttribute("points", pts([toe, ank, knee, hip]));
        $("leg-far").setAttribute("points", pts([[toe[0] - 6, toe[1]], [ank[0] - 6, ank[1]], [knee[0] - 6, knee[1]], [hip[0] - 4, hip[1]]]));
        L2("torso", hip, sh);
        $("arm").setAttribute("points", pts([sh, el, hand]));
        $("arm-far").setAttribute("points", pts([[sh[0] - 6, sh[1] + 2], [el[0] - 8, el[1]], [hand[0] - 8, hand[1]]]));
        $("head").setAttribute("cx", hd[0]); $("head").setAttribute("cy", hd[1]);
        var a0 = lerp(hip, sh, 0.25), a1 = lerp(hip, sh, 0.85), dx = sh[0] - hip[0], dy = sh[1] - hip[1], n = Math.hypot(dx, dy);
        var nx = -dy / n * 15, ny = dx / n * 15;
        var sd = m === "aus" ? -1 : 1;
        L2("m-lat", [a0[0] - sd * nx, a0[1] - sd * ny], [a1[0] - sd * nx, a1[1] - sd * ny]);
        var tp = lerp(hip, sh, 0.85); $("m-trap").setAttribute("cx", tp[0] - sd * nx * 0.9); $("m-trap").setAttribute("cy", tp[1] - sd * ny * 0.9);
        L2("m-bic", lerp(sh, el, 0.15), lerp(sh, el, 0.9));
        var k = 0.35 + 0.65 * d;
        ["lat", "bic", "trap"].forEach(function (x) { $("m-" + x).setAttribute("opacity", A[x] * k); });
        $("rig").setAttribute("opacity", m === "aus" ? 0.25 : 1);
        $("low").setAttribute("opacity", m === "aus" ? 1 : 0);
        $("fig").setAttribute("opacity", P.show);
      }
      var tl = gsap.timeline({ paused: true, onUpdate: render });
      function reps(t0, t1, mode, per) {
        tl.set(P, { mode: mode, d: 0 }, t0);
        for (var t = t0 + 0.2; t + per * 0.9 < t1; t += per + 0.1) {
          if (mode === "neg") {
            tl.to(P, { d: 1, duration: 0.3, ease: "power2.out" }, t);
            tl.to(P, { d: 0, duration: per * 0.8, ease: "none" }, t + 0.4);
          } else {
            tl.to(P, { d: 1, duration: per * 0.45, ease: "power2.out" }, t);
            tl.to(P, { d: 0, duration: per * 0.45, ease: "power2.inOut" }, t + per * 0.5);
          }
        }
      }
      function lights(t, list) {
        tl.set(A, { lat: 0, bic: 0, trap: 0 }, t);
        var o = { duration: 0.3 }; list.forEach(function (x) { o[x] = 1; });
        tl.to(A, o, t + 0.6);
      }
      /*JS*/
      tl.set({}, {}, /*D*/);
      render();
      window.__timelines["tractions"] = tl;
    })();
  </script>
</template>
