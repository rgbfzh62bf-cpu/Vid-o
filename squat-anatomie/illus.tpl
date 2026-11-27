<template>
  <style>
    #illus { position: absolute; inset: 0; overflow: hidden; background: #ffffff; color: #1b1b1b; }
    #illus .full { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; }
    #illus .layer { position: absolute; inset: 0; }
    #illus .imbox { position: absolute; left: 168px; top: 420px; width: 743px; height: 1300px; }
    .iw { position: relative; width: 100%; height: 100%; transform-origin: 50% 40%; }
    .iw img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: contain; }
    .hl { position: absolute; border-radius: 50%; mix-blend-mode: multiply;
      background: radial-gradient(closest-side, rgba(214, 38, 26, 0.92), rgba(214, 38, 26, 0.55) 55%, rgba(214, 38, 26, 0) 100%); }
    .hl.g { mix-blend-mode: normal; background: radial-gradient(closest-side, rgba(214, 38, 26, 0.8), rgba(214, 38, 26, 0.45) 55%, rgba(214, 38, 26, 0) 100%); }
    .kb { position: absolute; width: 120px; height: 130px; transform: translate(-50%, -30%); }
    .kb i { position: absolute; left: 0; bottom: 0; width: 120px; height: 110px; border-radius: 50%;
      background: radial-gradient(circle at 35% 30%, #5a5a60, #1e1e22 70%); }
    .kb::before { content: ""; position: absolute; left: 22px; top: -4px; width: 76px; height: 60px; border: 13px solid #26262a; border-bottom: none; border-radius: 40px 40px 0 0; }
    .ttl { position: absolute; left: 120px; width: 840px; top: 318px; text-align: center; font-family: "Playfair Display", serif;
      font-style: italic; font-weight: 800; line-height: 1; color: #1b1b1b; }
    .ttl .circ { display: inline-flex; width: 76px; height: 76px; border: 5px solid #1b1b1b; border-radius: 50%; align-items: center;
      justify-content: center; font-style: normal; font-family: "Montserrat", sans-serif; font-weight: 800; font-size: 44px; margin-right: 20px; vertical-align: 12px; }
    .lab { position: absolute; width: 268px; padding: 12px 20px 14px; border-radius: 12px; border: 3px solid #b8352a; box-shadow: 0 8px 22px rgba(0,0,0,0.12); }
    .lab b { display: block; font-family: "Montserrat", sans-serif; font-weight: 800; font-size: 36px; line-height: 1.1; }
    .lab span { display: block; font-family: "Montserrat", sans-serif; font-weight: 600; font-size: 28px; line-height: 1.2; }
    .lab.main { background: #b8352a; color: #fff; }
    .lab.sec { background: #fff; color: #b8352a; }
    .ilbl { font-family: "Montserrat", sans-serif; font-weight: 700; font-size: 28px; fill: #1b1b1b; }
    .loupe { position: absolute; left: 340px; top: 600px; width: 400px; height: 400px; border-radius: 50%; border: 8px solid #1b1b1b; background: #fff;
      box-shadow: 0 18px 50px rgba(0,0,0,0.25); overflow: hidden; }
    .loupe .lin { position: absolute; inset: -8px; }
    .loupe img { position: absolute; }
    .banner { position: absolute; left: 150px; width: 780px; top: 1040px; text-align: center; background: #b8352a; color: #fff; border-radius: 12px;
      padding: 16px 20px; font-family: "Playfair Display", serif; font-style: italic; font-weight: 800; font-size: 40px; line-height: 1.15; box-shadow: 0 10px 28px rgba(0,0,0,0.18); }
    .nums { position: absolute; left: 190px; width: 700px; top: 440px; display: flex; justify-content: space-between; }
    .nums span { width: 120px; height: 120px; border-radius: 50%; border: 5px solid #1b1b1b; display: flex; align-items: center; justify-content: center;
      font-family: "Montserrat", sans-serif; font-weight: 800; font-size: 56px; background: #fff; }
    .rows { position: absolute; left: 190px; width: 700px; top: 520px; display: grid; gap: 22px; }
    .row { display: flex; align-items: center; gap: 24px; font-family: "Playfair Display", serif; font-style: italic; font-weight: 800; font-size: 56px;
      padding: 14px 28px; border-radius: 16px; background: #fff; border: 3px solid #1b1b1b; box-shadow: 0 8px 22px rgba(0,0,0,0.1); }
    .row b { font-style: normal; font-family: "Montserrat", sans-serif; width: 64px; height: 64px; border-radius: 50%; background: #b8352a; color: #fff;
      display: flex; align-items: center; justify-content: center; font-size: 36px; }
  </style>
  <div id="illus" data-composition-id="illus" data-width="1080" data-height="1920" data-layout-allow-overlap>
    /*CLIPS*/
  </div>
  <script>
    (function () {
      var tl = gsap.timeline({ paused: true });
      /*JS*/
      tl.set({}, {}, /*D*/);
      window.__timelines["illus"] = tl;
    })();
  </script>
</template>
