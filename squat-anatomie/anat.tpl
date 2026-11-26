<template>
  <style>
    #anat { position: absolute; inset: 0; overflow: hidden; background: #f3efe8; color: #1b1b1b; }
    #anat .full { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; }
    .ttl { position: absolute; left: 140px; width: 800px; top: 300px; text-align: center; font-family: "Playfair Display", serif;
      font-style: italic; font-weight: 800; font-size: 92px; line-height: 1; color: #1b1b1b; }
    .ttl .circ { display: inline-flex; width: 78px; height: 78px; border: 5px solid #1b1b1b; border-radius: 50%; align-items: center;
      justify-content: center; font-style: normal; font-family: "Montserrat", sans-serif; font-weight: 800; font-size: 46px; margin-right: 22px; vertical-align: 10px; }
    .lab rect { stroke-width: 3; }
    .lab.main rect { fill: #b8352a; stroke: #b8352a; } .lab.main text { fill: #fff; }
    .lab.sec rect { fill: #fff; stroke: #b8352a; } .lab.sec text { fill: #b8352a; }
    .lab .ln { font-family: "Montserrat", sans-serif; font-weight: 800; font-size: 36px; }
    .lab .ls { font-family: "Montserrat", sans-serif; font-weight: 600; font-size: 28px; }
    .lab .ld { stroke: #1b1b1b; stroke-width: 3; }
    .lab .ad { fill: #1b1b1b; }
    .ibox { fill: #fff; stroke: #1b1b1b; stroke-width: 3; }
    .foot { fill: #b8352a; }
    .ilbl { font-family: "Montserrat", sans-serif; font-weight: 700; font-size: 28px; fill: #1b1b1b; }
    .bn { font-family: "Playfair Display", serif; font-style: italic; font-weight: 800; font-size: 36px; fill: #fff; }
    .rows { position: absolute; left: 190px; width: 700px; top: 560px; display: grid; gap: 18px; }
    .row { display: flex; align-items: center; gap: 24px; font-family: "Playfair Display", serif; font-style: italic; font-weight: 800; font-size: 52px;
      padding: 12px 26px; border-radius: 16px; background: #fff; border: 3px solid #1b1b1b; }
    .row b { font-style: normal; font-family: "Montserrat", sans-serif; width: 60px; height: 60px; border-radius: 50%; background: #b8352a; color: #fff;
      display: flex; align-items: center; justify-content: center; font-size: 34px; }
    .nums { position: absolute; left: 190px; width: 700px; top: 470px; display: flex; justify-content: space-between; }
    .nums span { width: 120px; height: 120px; border-radius: 50%; border: 5px solid #1b1b1b; display: flex; align-items: center; justify-content: center;
      font-family: "Montserrat", sans-serif; font-weight: 800; font-size: 56px; background: #fff; }
  </style>
  <div id="anat" data-composition-id="anat" data-width="1080" data-height="1920" data-layout-allow-overlap>
    <svg id="fig-svg" class="clip full" data-start="0" data-duration="/*D*/" data-track-index="0" viewBox="0 0 1080 1920">
      <g id="fig">
        <line x1="170" y1="1090" x2="910" y2="1090" stroke="#1b1b1b" stroke-width="4" />
        <ellipse id="shadow" cx="540" cy="1094" rx="120" ry="11" fill="#000" opacity="0.12" />
        <g id="bench" opacity="0"><rect x="300" y="995" width="170" height="26" rx="8" fill="#6d6d72" /><rect x="318" y="1021" width="16" height="69" fill="#6d6d72" /><rect x="436" y="1021" width="16" height="69" fill="#6d6d72" /></g>
        <g id="body" stroke-linecap="round" stroke-linejoin="round" fill="none">
          <polyline id="arm-far" stroke="#c48a5c" stroke-width="17" />
          <line id="fthigh" stroke="#c48a5c" stroke-width="34" /><line id="fshin" stroke="#c48a5c" stroke-width="25" />
          <polyline id="ffoot" stroke="#3a3a3a" stroke-width="16" />
          <line id="torso" stroke="#e2b48a" stroke-width="56" />
          <line id="back-def" stroke="#c99467" stroke-width="4" /><line id="abs-def" stroke="#c99467" stroke-width="4" />
          <line id="thigh" stroke="#e2b48a" stroke-width="40" /><line id="shin" stroke="#e2b48a" stroke-width="28" />
          <line id="quad-def" stroke="#c99467" stroke-width="4" /><line id="calf-def" stroke="#c99467" stroke-width="4" />
          <circle id="hipball" r="31" fill="#1b1b1b" stroke="none" /><line id="shorts" stroke="#1b1b1b" stroke-width="44" />
          <polyline id="foot" stroke="#2a2a2a" stroke-width="17" />
          <g id="reds">
            <line id="m-quad" stroke="#d63b2c" stroke-width="17" opacity="0" /><line id="m-ham" stroke="#d63b2c" stroke-width="15" opacity="0" />
            <line id="m-add" stroke="#d63b2c" stroke-width="13" opacity="0" /><line id="m-calf" stroke="#d63b2c" stroke-width="14" opacity="0" />
            <line id="m-abs" stroke="#d63b2c" stroke-width="18" opacity="0" />
            <ellipse id="m-glute" rx="30" ry="27" fill="#d63b2c" stroke="none" opacity="0" />
          </g>
          <polyline id="arm-near" stroke="#e2b48a" stroke-width="19" />
          <g id="kb" opacity="0"><circle id="kb-b" r="24" fill="#2f2f33" stroke="none" /><path id="kb-h" stroke="#2f2f33" stroke-width="7" /></g>
          <circle id="head" r="31" fill="#e2b48a" stroke="none" />
          <path id="hair" fill="#3b2a20" stroke="none" />
        </g>
      </g>
    </svg>
    /*CLIPS*/
  </div>
  <script>
    (function () {
      var G = 1090, SHIN = 120, THIGH = 125, TORSO = 150, NECK = 16, HEAD = 31, UA = 82, FA = 78;
      var P = { d: 0, mode: "classic", show: 1 };
      var A = { quad: 0, ham: 0, add: 0, calf: 0, abs: 0, glute: 0 };
      var ANCH = {};
      var MODES = {
        classic: { ax: 560, hip: [-95, 140], lean: 38, arm: 82 },
        sumo: { ax: 560, hip: [-55, 148], lean: 16, arm: 70 },
        narrow: { ax: 560, hip: [-60, 120], lean: 26, arm: 85 },
        goblet: { ax: 560, hip: [-70, 150], lean: 14, goblet: 1 },
        bulgare: { ax: 615, hip: [-10, 115], lean: 12, arm: 40, rear: [425, 992], stand: [525, 862] }
      };
      function $(id) { return document.getElementById(id); }
      function ik(h, a, l1, l2, dir) {
        var dx = a[0] - h[0], dy = a[1] - h[1], dd = Math.min(Math.hypot(dx, dy), l1 + l2 - 0.01);
        var base = Math.atan2(dy, dx), c = (l1 * l1 + dd * dd - l2 * l2) / (2 * l1 * dd);
        var ang = Math.acos(Math.max(-1, Math.min(1, c)));
        return [h[0] + l1 * Math.cos(base - dir * ang), h[1] + l1 * Math.sin(base - dir * ang)];
      }
      function pts(a) { return a.map(function (p) { return p[0].toFixed(1) + "," + p[1].toFixed(1); }).join(" "); }
      function L(id, p, q) { var e = $(id); e.setAttribute("x1", p[0]); e.setAttribute("y1", p[1]); e.setAttribute("x2", q[0]); e.setAttribute("y2", q[1]); }
      // segment p->q, keep t0..t1 of it, shifted by off along normal (side=+1 front of a down-pointing limb)
      function seg(p, q, t0, t1, off, side) {
        var dx = q[0] - p[0], dy = q[1] - p[1], n = Math.hypot(dx, dy) || 1, nx = side * dy / n, ny = -side * dx / n;
        return [[p[0] + dx * t0 + nx * off, p[1] + dy * t0 + ny * off], [p[0] + dx * t1 + nx * off, p[1] + dy * t1 + ny * off]];
      }
      function mid(s) { return [(s[0][0] + s[1][0]) / 2, (s[0][1] + s[1][1]) / 2]; }
      function render() {
        var m = MODES[P.mode], d = P.d;
        var ank = [m.ax, G - 8];
        var hip = m.stand ? [m.stand[0] + m.hip[0] * d, m.stand[1] + m.hip[1] * d] : [m.ax - 5 + m.hip[0] * d, G - SHIN - THIGH + 4 + m.hip[1] * d];
        var knee = ik(hip, ank, THIGH, SHIN, 1);
        var heel = [ank[0] - 16, G - 4], toe = [m.ax + 46, G - 4];
        var fk, fa, ff;
        if (m.rear) { fa = m.rear; fk = ik(hip, fa, THIGH, SHIN, 1); ff = [fa, [fa[0] - 42, fa[1] - 8]]; }
        else { fk = [knee[0] - 8, knee[1] + 2]; fa = [ank[0] - 10, ank[1]]; ff = [[heel[0] - 10, heel[1]], [toe[0] - 10, toe[1]]]; }
        var lean = m.lean * d * Math.PI / 180;
        var sh = [hip[0] + TORSO * Math.sin(lean), hip[1] - TORSO * Math.cos(lean)];
        var hd = [hip[0] + (TORSO + NECK + HEAD) * Math.sin(lean), hip[1] - (TORSO + NECK + HEAD) * Math.cos(lean)];
        var el, hn;
        if (m.goblet) {
          hn = [sh[0] + 46 * Math.cos(lean) + 34 * Math.sin(lean), sh[1] + 46 * Math.sin(lean) + 34 * Math.cos(lean) + 18];
          el = ik(sh, hn, UA, FA, -1);
        } else {
          var aa = (m.arm * d + 8) * Math.PI / 180;
          el = [sh[0] + UA * Math.sin(aa), sh[1] + UA * Math.cos(aa)];
          hn = [el[0] + FA * Math.sin(aa + 0.25), el[1] + FA * Math.cos(aa + 0.25)];
        }
        L("thigh", hip, knee); L("shin", knee, ank); L("fthigh", [hip[0] - 4, hip[1]], fk); L("fshin", fk, fa);
        $("foot").setAttribute("points", pts([[heel[0], heel[1]], ank, toe]));
        $("ffoot").setAttribute("points", pts(m.rear ? ff : [ff[0], [fa[0], fa[1]], ff[1]]));
        L("torso", hip, sh); L("shorts", hip, seg(hip, knee, 0, 0.3, 0, 1)[1]);
        $("hipball").setAttribute("cx", hip[0] - 2); $("hipball").setAttribute("cy", hip[1] + 2);
        $("arm-near").setAttribute("points", pts([sh, el, hn]));
        $("arm-far").setAttribute("points", pts([[sh[0] - 5, sh[1] + 2], [el[0] - 8, el[1] + 3], [hn[0] - 6, hn[1] + 2]]));
        $("head").setAttribute("cx", hd[0]); $("head").setAttribute("cy", hd[1]);
        var hx = hd[0], hy = hd[1], lr = lean;
        $("hair").setAttribute("d", "M" + (hx - 31 * Math.cos(lr)) + "," + (hy - 31 * Math.sin(lr) - 2) + " A31,31 0 0 1 " + (hx + 28 * Math.cos(lr)) + "," + (hy + 28 * Math.sin(lr) - 10) + " Z");
        var kb = $("kb"); kb.setAttribute("opacity", m.goblet ? 1 : 0);
        $("kb-b").setAttribute("cx", hn[0] + 14); $("kb-b").setAttribute("cy", hn[1] + 22);
        $("kb-h").setAttribute("d", "M" + (hn[0] - 2) + "," + (hn[1] + 10) + " Q" + (hn[0] + 14) + "," + (hn[1] - 18) + " " + (hn[0] + 30) + "," + (hn[1] + 10));
        // muscles
        var q = seg(hip, knee, 0.18, 0.85, 10, 1), h = seg(hip, knee, 0.2, 0.85, 10, -1), ad = seg(hip, knee, 0.35, 0.8, 2, -1);
        var c = seg(knee, ank, 0.12, 0.6, 7, -1), ab = seg(hip, sh, 0.12, 0.7, 15, -1), bk = seg(hip, sh, 0.15, 0.85, 17, 1);
        L("m-quad", q[0], q[1]); L("m-ham", h[0], h[1]); L("m-add", ad[0], ad[1]); L("m-calf", c[0], c[1]); L("m-abs", ab[0], ab[1]);
        L("quad-def", q[0], q[1]); L("calf-def", c[0], c[1]); L("abs-def", ab[0], ab[1]); L("back-def", bk[0], bk[1]);
        var gb = seg(hip, knee, 0.02, 0.02, 17, -1)[0];
        $("m-glute").setAttribute("cx", gb[0]); $("m-glute").setAttribute("cy", gb[1]);
        ANCH = { quad: mid(q), ham: mid(h), add: mid(ad), calf: mid(c), abs: mid(ab), glute: gb };
        ["quad", "ham", "add", "calf", "abs", "glute"].forEach(function (k) { $("m-" + k).setAttribute("opacity", A[k] * 0.9); });
        $("shadow").setAttribute("cx", m.ax - 10);
        $("bench").setAttribute("opacity", m.rear ? 1 : 0);
        $("fig").setAttribute("opacity", P.show);
        // label leaders
        document.querySelectorAll("#anat .lab").forEach(function (g) {
          var a = ANCH[g.getAttribute("data-m")], x = +g.getAttribute("data-x"), y = +g.getAttribute("data-y");
          var ex = x < 540 ? x + 270 : x, ln = g.querySelector(".ld"), dot = g.querySelector(".ad");
          ln.setAttribute("x1", ex); ln.setAttribute("y1", y + 52); ln.setAttribute("x2", a[0]); ln.setAttribute("y2", a[1]);
          if (dot) { dot.setAttribute("cx", a[0]); dot.setAttribute("cy", a[1]); }
        });
        document.querySelectorAll("#anat use[data-m]").forEach(function (u) {
          var a = ANCH[u.getAttribute("data-m")], s = 2.4;
          u.setAttribute("transform", "translate(" + (540 - s * a[0]) + "," + (760 - s * a[1]) + ") scale(" + s + ")");
        });
      }
      var tl = gsap.timeline({ paused: true, onUpdate: render });
      var W = /*W*/;
      function reps(t0, t1, mode) {
        tl.set(P, { mode: mode, d: 0 }, t0);
        for (var t = t0 + 0.3; t + 1.2 < t1; t += 1.6) {
          tl.to(P, { d: 1, duration: 0.7, ease: "power2.inOut" }, t);
          tl.to(P, { d: 0, duration: 0.65, ease: "power2.inOut" }, t + 0.85);
        }
      }
      function lightsOff(t) { tl.to(A, { quad: 0, ham: 0, add: 0, calf: 0, abs: 0, glute: 0, duration: 0.2 }, t); }
      function labs(n, t, k) {
        for (var i = 0; i < k; i++) {
          var g = "#lb-" + n + "-" + i, el = document.querySelector(g), mm = el.getAttribute("data-m"), o = {};
          o[mm] = el.classList.contains("main") ? 1 : 0.45; o.duration = 0.25;
          tl.from(g + " rect, " + g + " text", { opacity: 0, x: (+el.getAttribute("data-x") < 540 ? -30 : 30), duration: 0.3, ease: "power3.out" }, t + i * 0.45);
          tl.from(g + " .ld", { opacity: 0, duration: 0.2 }, t + i * 0.45 + 0.15);
          tl.to(A, o, t + i * 0.45);
        }
      }
      function loupe(n, t) {
        tl.to("#labs-" + n + " g", { opacity: 0, duration: 0.2 }, t);
        tl.to(P, { show: 0.18, duration: 0.25 }, t);
        tl.from("#lpg-" + n, { scale: 0.3, opacity: 0, duration: 0.35, ease: "back.out(1.8)" }, t);
        tl.from("#bn-" + n, { y: 40, opacity: 0, duration: 0.3, ease: "power3.out" }, t + 0.35);
        tl.to(P, { show: 1, duration: 0.01 }, W[n][1]);
      }
      /*JS*/
      // scene resets
      Object.keys(W).forEach(function (n) { if (n !== "hook") lightsOff(W[n][0] - 0.2); });
      tl.set({}, {}, /*D*/);
      render();
      window.__timelines["anat"] = tl;
    })();
  </script>
</template>
