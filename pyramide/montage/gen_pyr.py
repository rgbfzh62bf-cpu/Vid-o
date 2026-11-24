import json
S=[21.90,50.65,88.25,108.95,123.70,198.15,284.70,407.55]
F=[135,146,205,104,117,220,285,238]
O=[];c=0
for f in F: O.append(c/30); c+=f
TOT=c/30
def m(b,t): return round(max(O[b], O[b]+(t-S[b])),3)
def end(b): return round(O[b]+F[b]/30,3)
caps=[
 (0,[(None,"Si tu bois tous les jours"),(22.78,"un litre et demi d'eau,"),(23.86,"ne t'emballe pas trop"),(24.54,"car ça te met juste"),(25.20,"dans le top 90 %.")]),
 (1,[(None,"Si tu manges des protéines"),(51.64,"à chaque repas,"),(52.38,"même au petit-déj,"),(53.32,"félicitations,"),(54.04,"t'es maintenant dans le top 80 %.")]),
 (2,[(None,"Si tu marches tous les jours"),(89.10,"8 000 pas,"),(90.24,"même les jours où il pleut,"),(91.12,"et même quand tu rentres"),(91.74,"tard du boulot,"),(92.88,"félicitations,"),(93.64,"t'es dans le top 70 %.")]),
 (3,[(None,"Si tu dors au moins"),(109.62,"sept heures par nuit,"),(110.68,"félicitations,"),(111.34,"t'es dans le top 45 %.")]),
 (4,[(None,"Si tu fais de la musculation"),(124.71,"trois fois par semaine,"),(125.79,"félicitations,"),(126.65,"t'es dans le top 30 %.")]),
 (5,[(None,"Si tu cuisines tous tes repas"),(199.23,"à l'avance le dimanche"),(199.93,"pour tes cinq jours suivants"),(200.95,"et que ton seul resto,"),(201.95,"c'est ton repas plaisir"),(202.69,"de la semaine,"),(203.65,"félicitations,"),(204.47,"t'es dans le top 15 %.")]),
 (6,[(None,"Si tu as trois réflexes simples,"),(286.11,"d'abord manger des légumes"),(287.05,"à chaque repas,"),(288.13,"un café après manger"),(289.03,"et prendre une photo de toi"),(290.37,"chaque mois pour voir"),(291.01,"tes vrais progrès,"),(292.05,"félicitations,"),(292.99,"tu es dans le top 5 %.")]),
 (7,[(None,"Si tu t'abonnes à mon compte"),(408.54,"dès maintenant"),(408.98,"et que tu commentes « CHANGEMENT »,"),(410.24,"et je t'envoie ma méthode complète"),(411.38,"pour perdre du poids"),(412.28,"sans régime extrême,"),(413.26,"félicitations,"),(414.26,"t'es maintenant dans le top 1 %.")]),
]
pyr_in=[23.86,53.32,92.88,110.68,125.79,203.65,292.05,413.26]
fill=[25.44,54.54,93.88,111.58,126.97,204.71,293.31,414.86]
# profile fills: (block, src time, target id)
pf=[(0,22.40,'l1'),(1,51.24,'l2'),(2,89.10,'l3'),(3,109.24,'l4'),(4,124.27,'l5'),(5,198.60,'l6'),(5,201.95,'l7'),(6,286.85,'p1'),(6,288.27,'p2'),(6,289.95,'p3')]
capel=[];k=0
for b,lst in caps:
  for i,(t,txt) in enumerate(lst):
    st=O[b] if t is None else m(b,t)
    en=(m(b,lst[i+1][0]) if i+1<len(lst) else end(b))
    capel.append((k,round(st,3),round(en-st,3),txt.replace(' %','\u00a0%').replace('« ','«\u00a0').replace(' »','\u00a0»').replace('8 000','8\u00a0000'),b)); k+=1
tiers=["90","80","70","45","30","15","5","1"]
cols=["#e62828","#fd8e20","#fee326","#78fe1e","#2fe2bb","#29b4fc","#a647fb","#e040fb"]
W,H=667,571; apexH=67; pitch=(H-apexH)/7; g=3
def xat(y): # half-width at y
  return (W/2)*y/H
def tierpoly(i): # i=0 bottom (90) .. 7 apex
  if i==7: y0,y1=0,apexH
  else:
    y1=H-i*pitch; y0=y1-pitch
  a=y0+(g if i!=7 else 0); bb=y1-g
  cx=W/2
  return f"{cx-xat(a):.1f},{a:.1f} {cx+xat(a):.1f},{a:.1f} {cx+xat(bb):.1f},{bb:.1f} {cx-xat(bb):.1f},{bb:.1f}" if i!=7 else f"{cx:.1f},{0} {cx+xat(bb):.1f},{bb:.1f} {cx-xat(bb):.1f},{bb:.1f}", (a+bb)/2+ (8 if i==7 else 0)
def svg(pid,fs):
  s=[f'<svg viewBox="0 0 {W} {H}" width="{W}" height="{H}"><defs><linearGradient id="{pid}g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f7f4f7"/><stop offset="0.55" stop-color="#d9d6d9"/><stop offset="1" stop-color="#8f8c8f"/></linearGradient></defs>',
     f'<polygon points="{W/2},-4 {W+6},{H+3} -6,{H+3}" fill="#000"/>']
  for i in range(8):
    pts,cy=tierpoly(i)
    s.append(f'<polygon points="{pts}" fill="url(#{pid}g)"/>')
    s.append(f'<g id="{pid}t{i}" opacity="0"><polygon points="{pts}" fill="{cols[i]}"/><text x="{W/2}" y="{cy:.1f}" dominant-baseline="central" text-anchor="middle" font-size="{fs if i!=7 else int(fs*0.62)}">{tiers[i]}%</text></g>')
  s.append('</svg>'); return "".join(s)
html=[]
html.append(f'''<!doctype html>
<html lang="fr"><head><meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" />
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<style>
:root {{ --top-bg:#0d0a0d; --bot-bg:#131013; --line:#b8b5b8; --bar:#949194; --link:#a3a8ff; --cap-font:"Figtree",sans-serif; }}
@font-face{{font-family:"Figtree";src:url('assets/fonts/figtree-700.woff2') format('woff2');font-weight:700;}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden;background:var(--top-bg)}}
#root{{position:relative;width:1080px;height:1920px;font-family:Arial,Helvetica,sans-serif;overflow:hidden}}
#tophalf{{position:absolute;left:0;top:0;width:1080px;height:960px;background:var(--top-bg);overflow:hidden}}
#profile{{position:absolute;left:0;top:0;width:1080px;height:1600px}}
#av{{position:absolute;left:147px;top:310px;width:164px;height:164px;border-radius:50%;background:#3a383a;overflow:hidden}}
#av img{{width:100%;height:100%;object-fit:cover;opacity:0}}
.bar{{position:absolute;left:190px;height:39px;background:var(--bar);box-shadow:0 0 0 1px #000}}
.txt{{position:absolute;left:190px;height:39px;line-height:39px;color:#fff;font-weight:700;font-size:35px;white-space:nowrap;opacity:0}}
#nmbar{{left:356px;top:344px;width:551px;height:33px}}
#nmtxt{{left:356px;top:340px;font-size:33px;height:41px;line-height:41px}}
#ring{{position:absolute;left:147px;top:310px;width:164px;height:164px}}
#ringtxt{{position:absolute;inset:0}}
#ringtxt span{{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;color:#fff;font:700 40px/1 Arial,sans-serif}}
.chk{{position:absolute;left:139px;width:35px;height:35px;border-radius:50%;border:3px solid #949194}}
.chk i{{position:absolute;inset:-3px;border-radius:50%;background:#78fe1e;opacity:0}}
.chk i::after{{content:"";position:absolute;left:11px;top:6px;width:9px;height:17px;border:solid #0d0a0d;border-width:0 4px 4px 0;transform:rotate(45deg)}}
#ghead{{position:absolute;left:78px;top:884px;color:#fff;font:700 34px/1 Arial,sans-serif;letter-spacing:2px}}
#gline{{position:absolute;left:78px;top:930px;width:924px;height:2px;background:#3a383a}}
#tabs{{position:absolute;left:78px;top:812px;width:924px;height:60px}}
.tab{{position:absolute;top:0;width:308px;height:60px;display:flex;align-items:center;justify-content:center}}
.tab i{{display:block;width:30px;height:30px;border:3px solid #cfcfcf;border-radius:4px}}
#tabline{{position:absolute;left:0;top:64px;width:308px;height:3px;background:#fff}}
.tile{{position:absolute;top:952px;width:302px;height:400px;background:#050505;overflow:hidden}}
.tile b{{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;color:#fff;font:900 230px/1 Arial,sans-serif}}
.tile img{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:0}}
.pin{{position:absolute;right:14px;top:12px;width:22px;height:22px;border-radius:50% 50% 50% 0;transform:rotate(-45deg);background:#fff;z-index:2}}
.pyr{{position:absolute;opacity:0}}
.pyr text{{fill:#fff;font-family:"Nunito",Arial,sans-serif;font-weight:900;stroke:#000;stroke-width:5px;paint-order:stroke;}}
#pyrA{{left:207px;top:191px;width:667px;height:571px}}
#pyrB{{left:206px;top:1335px;width:667px;height:571px;transform-origin:50% 0;}}
#sep{{position:absolute;left:0;top:959px;width:1080px;height:2px;background:var(--line);box-shadow:0 2px 0 #010001;z-index:4}}
#bottom{{position:absolute;left:0;top:961px;width:1080px;height:960px;object-fit:cover}}
#final{{position:absolute;left:0;top:0;width:1080px;height:1920px;object-fit:cover}}
.cap{{position:absolute;left:130px;width:820px;top:900px;text-align:center;color:#fff;font-family:var(--cap-font);font-weight:700;font-size:64px;line-height:64px;z-index:6;
 text-shadow:0 0 2px #000,0 0 2px #000,1px 1px 2px #000,-1px -1px 2px #000;}}
</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{TOT:.6f}" data-width="1080" data-height="1920" data-fps="30" data-layout-allow-overlap="true" data-layout-allow-overflow="true">
<audio id="voice" src="assets/voice.wav" data-start="0" data-duration="{TOT:.6f}" data-track-index="0"></audio>
<video id="bottom" class="clip" src="assets/bottom.mp4" data-start="0" data-duration="{O[7]:.6f}" data-track-index="1" muted playsinline></video>
<div id="tophalf" class="clip" data-start="0" data-duration="{O[7]:.6f}" data-track-index="2">
 <div id="profile">
''')
html.append('''  <div id="ring"><svg viewBox="0 0 164 164" width="164" height="164"><circle cx="82" cy="82" r="70" fill="none" stroke="#3a383a" stroke-width="14"/><circle id="ringarc" cx="82" cy="82" r="70" fill="none" stroke="#78fe1e" stroke-width="14" stroke-linecap="round" stroke-dasharray="439.8" stroke-dashoffset="439.8" transform="rotate(-90 82 82)"/></svg><div id="ringtxt">'''+''.join(f'<span id="rc{i}" style="opacity:{1 if i==0 else 0}">{i}/7</span>' for i in range(8))+'''</div></div>
  <div class="txt" id="title" style="left:356px;top:340px;font-size:36px;height:41px;line-height:41px;opacity:1">Ma checklist minceur</div>
''')
lines=[("l1",502,620,"💧 1,5 L d'eau par jour"),("l2",554,700,"🍗 Protéines à chaque repas"),("l3",606,560,"👟 8 000 pas par jour"),("l4",658,640,"😴 7 h de sommeil minimum"),("l5",710,660,"🏋️ Muscu 3 fois par semaine"),("l6",762,700,"🍱 Repas préparés le dimanche"),("l7",814,640,"🍕 1 repas plaisir / semaine")]
for i,(lid,y,w,t) in enumerate(lines):
  html.append(f'  <div class="chk" id="{lid}chk" style="top:{y+2}px"><i></i></div><div class="bar" id="{lid}bar" style="top:{y}px;width:{w}px"></div><div class="txt" id="{lid}txt" style="top:{y}px">{t}</div>\n')
html.append('  <div id="grid" style="opacity:0">\n  <div id="ghead">MES 3 RÉFLEXES</div><div id="gline"></div>\n')
for i,(x,img) in enumerate([(78,'b1a3'),(389,'b3a3'),(700,'b1t3')]):
  html.append(f'  <div class="tile" style="left:{x}px"><div class="pin"></div><b>?</b><img id="p{i+1}img" src="assets/img/{img}.jpg" alt=""/></div>\n')
html.append('  </div>\n </div>\n <div id="pyrA" class="pyr">'+svg('A',40)+'</div>\n</div>\n')
html.append(f'<div id="sep" class="clip" data-start="0" data-duration="{O[7]:.6f}" data-track-index="3"></div>\n')
html.append(f'<video id="final" class="clip" src="assets/final.mp4" data-start="{O[7]:.6f}" data-duration="{F[7]/30:.6f}" data-track-index="1" muted playsinline></video>\n')
html.append(f'<div id="pyrBwrap" class="clip" data-start="{O[7]:.6f}" data-duration="{F[7]/30:.6f}" data-track-index="4" style="position:absolute;inset:0;z-index:5"><div id="pyrB" class="pyr">'+svg('B',40)+'</div></div>\n')
for k,st,du,txt,b in capel:
  extra=' style="top:1150px"' if b==7 else ''
  html.append(f'<div id="c{k}" class="clip cap"{extra} data-start="{st:.3f}" data-duration="{du:.3f}" data-track-index="5">{txt}</div>\n')
js=["window.__timelines=window.__timelines||{};","const tl=gsap.timeline({paused:true});"]
for b in range(7):
  ti=m(b,pyr_in[b]); tf=m(b,fill[b]); te=end(b)
  js.append(f'tl.fromTo("#pyrA",{{opacity:0,clipPath:"inset(100% 0% 0% 0%)"}},{{opacity:1,clipPath:"inset(0% 0% 0% 0%)",duration:0.3,ease:"power2.out"}},{ti});')
  js.append(f'tl.to("#profile",{{opacity:0.28,duration:0.3}},{ti});')
  js.append(f'tl.to("#At{b}",{{opacity:1,duration:0.12}},{tf});')
  js.append(f'tl.set("#pyrA",{{opacity:0}},{te-0.001:.3f});tl.set("#profile",{{opacity:1}},{te-0.001:.3f});')
# final pyramid: tiers 0-6 visible at entrance, apex at fill
ti=m(7,pyr_in[7]); tf=m(7,fill[7])
for i in range(7): js.append(f'tl.set("#Bt{i}",{{opacity:1}},{O[7]:.3f});')
js.append(f'tl.set("#pyrB",{{scale:0.8}},{O[7]:.3f});')
js.append(f'tl.fromTo("#pyrB",{{opacity:0,clipPath:"inset(100% 0% 0% 0%)"}},{{opacity:1,clipPath:"inset(0% 0% 0% 0%)",duration:0.3,ease:"power2.out"}},{ti});')
js.append(f'tl.to("#Bt7",{{opacity:1,duration:0.12}},{tf});')
for b,t,tid in pf:
  tt=m(b,t)
  if tid.startswith('p'): js.append(f'tl.to("#{tid}img",{{opacity:1,duration:0.12}},{tt});')
  else:
    js.append(f'tl.to("#{tid}bar",{{backgroundColor:"#ffffff",duration:0.08}},{tt});')
    js.append(f'tl.to("#{tid}bar",{{opacity:0,duration:0.12}},{tt+0.12:.3f});tl.to("#{tid}txt",{{opacity:1,duration:0.12}},{tt+0.12:.3f});')
    k=int(tid[1:])
    js.append(f'tl.to("#{tid}chk i",{{opacity:1,duration:0.12}},{tt+0.12:.3f});tl.to("#{tid}chk",{{borderColor:"#78fe1e",duration:0.12}},{tt+0.12:.3f});')
    js.append(f'tl.to("#ringarc",{{attr:{{"stroke-dashoffset":{439.8*(1-k/7):.1f}}},duration:0.3,ease:"power2.out"}},{tt+0.12:.3f});tl.set("#rc{k-1}",{{opacity:0}},{tt+0.12:.3f});tl.set("#rc{k}",{{opacity:1}},{tt+0.12:.3f});')
js.append(f'tl.set("#profile",{{y:-362}},{O[6]:.3f});tl.set("#grid",{{opacity:1}},{O[6]:.3f});')
js.append(f'tl.set({{}},{{}},{TOT:.6f});')
js.append('window.__timelines["main"]=tl;')
html.append('</div>\n<script>\n'+"\n".join(js)+'\n</script>\n</body></html>\n')
open('/home/user/Vid-o/pyramide/montage/index.html','w').write("".join(html))
json.dump({"O":O,"TOT":TOT},open('/tmp/claude-0/-home-user-Vid-o/0b4e80d1-95b0-51c6-abfd-c28f1a3f9220/scratchpad/tools/pyr_times.json','w'))
print(O,TOT,len(capel))
