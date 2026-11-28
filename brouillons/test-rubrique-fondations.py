"""TEST rubrique « Programmes » (aperçu seulement, le vrai site n'est pas modifié).
Usage : python3 test-rubrique-fondations.py <dossier site> <dossier sortie>
"""
import re, base64, os, mimetypes, sys

mimetypes.add_type('font/woff2', '.woff2')
HERE = os.path.dirname(os.path.abspath(__file__))
site, out = sys.argv[1], sys.argv[2]
os.chdir(site)


def inline(h):
    def rep(m):
        p = m.group(2)
        if p.startswith(('http', 'data:', '#', 'mailto', 'tel')) or not os.path.isfile(p):
            return m.group(0)
        t = mimetypes.guess_type(p)[0] or ''
        if not t.startswith(('image', 'font')):
            return m.group(0)
        return m.group(1) + 'data:' + t + ';base64,' + base64.b64encode(open(p, 'rb').read()).decode() + m.group(3)
    h = re.sub(r'''((?:src|href|content)=["'])([^"']+)(["'])''', rep, h)
    h = re.sub(r'''(url\(["']?)([^"')]+)(["']?\))''', rep, h)
    return re.sub(r'<link rel="preload"[^>]*>\n?', '', h)



LISTE = """          <li>Tes séances prêtes sur l'appli Athlyse, jour par jour</li>
          <li>Tes charges calculées à partir de tes 1RM</li>
          <li>La charge monte chaque semaine, sans que tu aies à calculer</li>
          <li>Les consignes de chaque exercice et de chaque variante</li>
          <li>Tu notes tes charges et ton ressenti à chaque séance</li>"""

INFO = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="M12 8v4M12 16h.01"/></svg>'

SECTION = f"""<section id="programmes">
  <div class="wrap">
    <div class="head reveal">
      <div><p class="eyebrow ath-eb"><img src="athlyse-logo-blanc.png" alt="Logo Athlyse" width="57" height="47"><span>Programmes à acheter · force athlétique · sur l'appli Athlyse</span></p><h2 style="margin-top:10px">Fondations :<br>ton programme de force athlétique.</h2></div>
      <p>Deux programmes de 4 semaines sur le squat, le développé couché et le soulevé de terre. Tu choisis selon ton rythme et tu le suis seul sur l'appli Athlyse.</p>
    </div>
    <div class="prog-grid">
      <div class="prog-cards reveal">
        <article class="prog-row">
          <div><p class="eyebrow">Programme Fondations</p><h3>3 séances / semaine</h3></div>
          <div class="prog-buy"><div class="price">29 €<small>paiement unique</small></div><a class="btn" href="#programmes">Acheter</a></div>
        </article>
        <article class="prog-row">
          <div><p class="eyebrow">Programme Fondations</p><h3>4 séances / semaine</h3></div>
          <div class="prog-buy"><div class="price">29 €<small>paiement unique</small></div><a class="btn" href="#programmes">Acheter</a></div>
        </article>
      </div>
      <div class="prog-more reveal">
        <ul class="prog-inc">
          <li><b>Tout se passe sur l'appli Athlyse</b><span>Tes séances jour par jour, avec les consignes de chaque exercice.</span></li>
          <li><b>Tes charges calculées selon tes 1RM</b><span>Elles montent chaque semaine, sans calcul de ta part.</span></li>
        </ul>
        <p class="prog-auto">{INFO}<span>En autonomie : ni suivi, ni retour sur ta technique, ni échange avec moi. Accès sans limite de durée.</span></p>
      </div>
    </div>
    <p class="prog-note reveal">Envie d'aller plus loin avec un suivi personnalisé ? <a href="#appel">On en parle →</a></p>
  </div>
</section>

"""

CSS = """
/* TEST rubrique programmes */
.prog-grid{display:grid;grid-template-columns:minmax(0,1.2fr) minmax(0,.8fr);gap:14px 56px;align-items:center}
.prog-cards{grid-column:1;grid-row:1;display:grid;gap:14px;min-width:0}
.prog-more{grid-column:1;grid-row:2;display:grid;gap:14px;min-width:0}
.prog-shot{grid-column:2;grid-row:1/3}
.prog-row{display:flex;justify-content:space-between;align-items:center;gap:16px;background:var(--surface);border:1px solid var(--line);border-radius:18px;padding:18px 20px}
.prog-row h3{font-size:1.7rem;font-weight:800;margin:2px 0 4px}.prog-row .muted{margin:0;font-size:.9rem}
.prog-buy{display:grid;gap:8px;justify-items:center;flex:none}
.prog-buy .price{font-size:2.4rem}.prog-buy .btn{padding:10px 22px}
.prog-steps{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px}
.prog-steps li{display:flex;gap:10px;align-items:center;background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:12px}
.prog-steps b{flex:none;width:30px;height:30px;border-radius:50%;background:var(--accent);color:var(--on-accent);display:grid;place-items:center;font-family:var(--f-display);font-size:1.1rem}
.prog-steps span{font-size:.85rem;line-height:1.35}
.prog-buy .price small{display:block;font-family:var(--f-body);font-size:.7rem;font-weight:600;opacity:.7;text-align:center}
.prog-buy .price{display:grid;justify-items:center}
@media (max-width:600px){.prog-steps{grid-template-columns:1fr;gap:8px}.prog-steps li{padding:10px 12px}}
.prog-tabs{display:flex;flex-wrap:wrap;justify-content:center;gap:6px}
.prog-tabs button{font:inherit;font-size:.82rem;font-weight:700;padding:7px 14px;border-radius:999px;border:1px solid var(--line);background:var(--surface);color:var(--muted);cursor:pointer}
.prog-tabs button.on{background:var(--accent);border-color:var(--accent);color:var(--on-accent)}
.prog-tabs.days{display:grid;grid-template-columns:repeat(4,auto);justify-content:center}
.prog-tabs.days button{font-size:.76rem;padding:6px 11px}
.prog-inc{list-style:none;margin:6px 0 0;padding:0;display:grid;gap:12px}.prog-inc li{display:grid;gap:2px;padding-left:16px;border-left:3px solid var(--accent)}.prog-inc span{color:var(--muted);font-size:.92rem}
.prog-shot{margin:0;display:grid;gap:10px;justify-items:center;min-width:0}
.prog-shot img{width:min(300px,100%);height:auto;display:block;border-radius:44px;border:10px solid #1C2B42;box-shadow:0 0 0 2px var(--line),0 50px 90px -30px rgba(0,0,0,.8),0 0 120px -20px color-mix(in srgb,var(--accent) 45%,transparent)}
.prog-shot figcaption{font-size:.78rem;color:var(--muted);text-align:center;max-width:300px}
.prog-auto{display:flex;gap:10px;align-items:flex-start;margin:0;padding:12px 14px;border:1px solid var(--accent);border-radius:12px;background:color-mix(in srgb,var(--accent) 10%,transparent);color:var(--ink);font-size:.88rem;line-height:1.45}
.prog-auto svg{width:20px;height:20px;color:var(--accent);flex:none;margin-top:1px}
.prog-pay{margin:0;font-size:.8rem;color:var(--muted)}
.prog-note{margin-top:22px;text-align:center;color:var(--muted);font-size:.95rem}
.prog-note a{color:var(--accent);font-weight:700;text-decoration:none;white-space:nowrap}
@media (max-width:820px){
.prog-grid{grid-template-columns:minmax(0,1fr) minmax(0,40%);gap:0 14px}
.prog-cards{gap:10px}.prog-more{grid-column:1/-1;margin-top:22px}
.prog-shot{grid-row:1}
.prog-row{flex-direction:column;align-items:stretch;gap:8px;padding:12px;border-radius:14px}
.prog-row .eyebrow{font-size:.58rem;letter-spacing:.06em}
.prog-row h3{font-size:1.2rem;margin:2px 0}.prog-row .muted{font-size:.76rem;line-height:1.35}
.prog-buy{display:flex;align-items:center;justify-content:space-between;gap:8px}
.prog-buy{display:grid;justify-items:stretch;gap:6px}.prog-buy .price{font-size:1.6rem;white-space:nowrap;justify-items:start}.prog-buy .price small{text-align:left}.prog-buy .btn{padding:8px 12px;font-size:.82rem;justify-content:center;width:100%}
.prog-tabs{gap:4px}.prog-tabs button{font-size:.66rem;padding:5px 8px}.prog-tabs.days{grid-template-columns:repeat(2,minmax(0,1fr));width:100%}.prog-tabs.days button{font-size:.62rem;padding:4px 6px}
@media (max-width:360px){.prog-buy .btn{flex:1 1 100%;justify-content:center}}
.prog-shot img{width:100%;border-radius:24px;border-width:5px}
.prog-shot figcaption{font-size:.6rem;line-height:1.3}
}
@media (min-width:600px) and (max-width:820px){.prog-grid{grid-template-columns:minmax(0,1fr) 250px;gap:0 32px}.prog-row{padding:16px}.prog-row h3{font-size:1.5rem}.prog-row .muted{font-size:.88rem}.prog-buy .price{font-size:2rem}.prog-buy .btn{padding:9px 18px;font-size:.9rem}.prog-shot img{border-width:8px;border-radius:36px}.prog-shot figcaption{font-size:.72rem}}

/* Alignement strict : cartes et téléphone partagent exactement la même hauteur */
.prog-grid{grid-template-columns:minmax(0,1fr) auto;align-items:stretch;gap:28px 40px}
.prog-cards{grid-row:1;grid-column:1;display:grid;grid-template-rows:1fr 1fr;gap:16px}
.prog-shot{grid-row:1;grid-column:2;align-content:space-between;justify-items:center;gap:12px}
.prog-shot img{width:270px}

.prog-row{flex-direction:column;align-items:stretch;justify-content:space-between;gap:16px;padding:24px}
.prog-row h3{font-size:2rem}
.prog-buy{display:flex;align-items:flex-end;justify-content:space-between;gap:12px}
.prog-buy .price{display:grid;justify-items:start;font-size:2.8rem}.prog-buy .price small{text-align:left}
.prog-buy .btn{width:auto;padding:12px 28px}
.prog-grid{grid-template-rows:1fr auto}
.prog-shot{grid-row:1/3}
.prog-more{grid-row:2;grid-column:1;display:grid;grid-template-columns:1fr;gap:14px;align-content:end}
.prog-row{padding:22px 24px}
@media (max-width:820px){
.prog-grid{grid-template-columns:minmax(0,1fr) minmax(0,40%);gap:0 14px}
.prog-cards{gap:10px}
.prog-shot img{width:100%}
.prog-grid{grid-template-rows:auto auto}.prog-shot{grid-row:1}.prog-more{grid-column:1/-1;margin-top:22px;gap:14px}
.prog-row{padding:12px;gap:8px}.prog-row h3{font-size:1.2rem}
.prog-buy{display:grid;justify-items:stretch;gap:6px}.prog-buy .price{font-size:1.6rem}.prog-buy .btn{width:100%;padding:8px 12px}
}
@media (min-width:600px) and (max-width:820px){.prog-grid{grid-template-columns:minmax(0,1fr) 240px;gap:0 24px}.prog-shot img{width:240px;border-width:8px;border-radius:36px}.prog-row{padding:20px;gap:10px}.prog-row h3{font-size:1.6rem}.prog-row .muted{font-size:.9rem}.prog-buy{display:flex;align-items:flex-end;justify-content:space-between}.prog-buy .price{font-size:2.4rem}.prog-buy .btn{width:auto;padding:10px 22px;font-size:.9rem}.prog-tabs.days{grid-template-columns:repeat(4,auto);width:auto;gap:4px}.prog-tabs.days button{font-size:.7rem;padding:5px 8px}.prog-tabs button{font-size:.78rem;padding:6px 12px}.prog-steps{grid-template-columns:repeat(3,minmax(0,1fr));gap:10px}.prog-shot figcaption{font-size:.72rem}}
/* Sans visuel : les deux programmes côte à côte, détails dessous */
.prog-grid{grid-template-columns:repeat(2,minmax(0,1fr));grid-template-rows:auto auto;gap:16px}
.prog-cards{grid-column:1/-1;grid-row:1;grid-template-columns:repeat(2,minmax(0,1fr));grid-template-rows:none;gap:16px}
.prog-more{grid-column:1/-1;grid-row:2;margin-top:8px;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px;align-content:start}
.prog-more .prog-inc{grid-column:1/-1;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px;margin:0}
.prog-more .prog-auto,.prog-more .prog-pay{grid-column:1/-1}
.prog-row{padding:24px;gap:18px}
@media (max-width:820px){
.prog-grid,.prog-cards{gap:10px}
.prog-more{margin-top:12px}
.prog-row{padding:14px;gap:10px}
}
@media (max-width:600px){.prog-more .prog-inc{grid-template-columns:1fr;gap:12px}.prog-buy{display:grid;grid-template-columns:minmax(0,1fr);grid-auto-flow:row;justify-items:stretch}.prog-buy .btn{width:100%;justify-content:center}}
.prog-inc li{align-content:start}
/* Titre des cartes sur une seule ligne, taille ajustée à la carte */
.prog-row{container-type:inline-size}
.prog-row h3{white-space:nowrap;font-size:min(2rem,12.4cqi)}
@media (max-width:820px){.prog-row h3{font-size:min(1.2rem,12.4cqi)}}
@media (min-width:600px) and (max-width:820px){.prog-row h3{font-size:min(1.6rem,12.4cqi)}}

@media (min-width:600px) and (max-width:820px){.prog-grid,.prog-cards{gap:14px}.prog-row{padding:20px}}
"""

AVIS_LIST = [
    # (prénom, depuis quand, accompagnement, avis mot pour mot)
    ("[Prénom]", "septembre 2026", "Renforcement musculaire",
     "Super coach ! Je fais du renfo avec lui depuis septembre et j'ai déjà bien progressé. Il est pédagogue, motivant, et il sait adapter les séances à mes besoins. Je le recommande vivement."),
]
Q_SVG = '<svg class="q" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M3 21v-7.5C3 8.6 5.4 5.3 10.2 3.6l1 1.9C8.4 6.7 7 8.6 6.8 11H10v10H3zm11 0v-7.5c0-4.9 2.4-8.2 7.2-9.9l1 1.9c-2.8 1.2-4.2 3.1-4.4 5.5H21v10h-7z"/></svg>'
def carte(a, cache):
    prenom, depuis, type_, txt = a
    h = ' aria-hidden="true"' if cache else ''
    return (f'<figure class="avis"{h}>{Q_SVG}<blockquote>{txt}</blockquote>'
            f'<figcaption><b>{prenom}</b><span>{type_} · depuis {depuis}</span></figcaption></figure>')
import os as _os
if _os.environ.get('AVIS_DEMO'):  # test local uniquement, jamais publié
    AVIS_LIST = AVIS_LIST * 4
CARTES = ''.join(carte(a, False) for a in AVIS_LIST)
AVIS = f"""<section id="avis">
  <div class="wrap">
    <div class="head reveal"><div><p class="eyebrow">Avis clients</p><h2 style="margin-top:10px">Ce qu'ils en disent</h2></div><p>Les retours des personnes que j'accompagne, publiés tels quels.</p></div>
    <div class="avis-car"><div class="avis-piste" tabindex="0" aria-label="Avis clients, faire glisser pour voir les autres">{CARTES}</div></div>
    <div class="avis-dots" role="group" aria-label="Choisir un avis"></div>
  </div>
</section>
<script>
(function(){{
var car=document.querySelector('.avis-car'),pi=car.querySelector('.avis-piste'),dots=document.querySelector('.avis-dots'),cs=[].slice.call(pi.children),
pause=false,vu=false,n=0,cur=0,red=matchMedia('(prefers-reduced-motion: reduce)').matches;
function pas(){{return cs.length>1?cs[1].offsetLeft-cs[0].offsetLeft:pi.clientWidth}}
function pages(){{return Math.max(1,cs.length-Math.round(pi.clientWidth/pas())+1)}}
function va(k,inst){{cur=(k+n)%n;majDots();pi.scrollTo({{left:cur*pas(),behavior:inst||red?'auto':'smooth'}})}}
function majDots(){{[].forEach.call(dots.children,function(d,k){{d.classList.toggle('on',k===cur);d.setAttribute('aria-current',k===cur)}})}}
function construire(){{n=pages();car.classList.toggle('seul',n<2);dots.innerHTML='';if(n<2)return;
for(var k=0;k<n;k++){{var b=document.createElement('button');b.type='button';b.setAttribute('aria-label','Avis '+(k+1));(function(k){{b.onclick=function(){{va(k);redemarre()}}}})(k);dots.appendChild(b)}}
cur=Math.min(cur,n-1);majDots()}}
var st;pi.addEventListener('scroll',function(){{clearTimeout(st);st=setTimeout(function(){{var k=Math.min(n-1,Math.round(pi.scrollLeft/pas()));if(k!==cur){{cur=k;majDots()}}}},80)}},{{passive:true}});
var t;function redemarre(){{clearInterval(t);if(red)return;t=setInterval(function(){{if(!pause&&vu&&n>1&&!document.hidden)va(cur+1)}},7000)}}
car.addEventListener('pointerenter',function(e){{if(e.pointerType==='mouse')pause=true}});car.addEventListener('pointerleave',function(e){{if(e.pointerType==='mouse'){{pause=false;redemarre()}}}});
car.addEventListener('touchstart',function(){{pause=true}},{{passive:true}});car.addEventListener('touchend',function(){{setTimeout(function(){{pause=false;redemarre()}},4000)}});
var dx=null,sl=0;pi.addEventListener('pointerdown',function(e){{if(e.pointerType!=='mouse'||n<2)return;dx=e.clientX;sl=pi.scrollLeft;pi.classList.add('glisse')}});
addEventListener('pointermove',function(e){{if(dx===null)return;pi.scrollLeft=sl-(e.clientX-dx)}});
addEventListener('pointerup',function(e){{if(dx===null)return;var d=e.clientX-dx,k=Math.round(sl/pas());dx=null;pi.classList.remove('glisse');
if(d<-40)k++;else if(d>40)k--;va(Math.max(0,Math.min(n-1,k)))}});
new IntersectionObserver(function(es){{vu=es[0].isIntersecting}},{{threshold:.4}}).observe(car);
construire();redemarre();var rt;addEventListener('resize',function(){{clearTimeout(rt);rt=setTimeout(function(){{construire();va(cur,true)}},150)}});
}})();
</script>

"""
AVIS_CSS = """
/* TEST rubrique avis : un avis à la fois, points pour choisir */
.avis-piste{display:flex;gap:16px;overflow-x:auto;scroll-snap-type:x mandatory;scrollbar-width:none;overscroll-behavior-x:contain;cursor:grab;align-items:stretch;outline:none}
.avis-piste::-webkit-scrollbar{display:none}
.avis-piste.glisse{scroll-snap-type:none;cursor:grabbing;user-select:none}
.avis-car.seul .avis-piste{justify-content:center;cursor:auto}
.avis{flex:0 0 calc((100% - 32px)/3);scroll-snap-align:start;margin:0;display:grid;grid-template-rows:auto 1fr auto;gap:14px;background:var(--surface);border:1px solid var(--line);border-radius:18px;padding:26px;min-width:0}
.avis .q{width:30px;height:30px;color:var(--accent)}
.avis blockquote{margin:0;font-weight:700;font-size:1.05rem;line-height:1.55}
.avis figcaption{display:grid;gap:2px;padding-top:14px;border-top:1px solid var(--line)}
.avis figcaption b{font-size:1rem}.avis figcaption span{font-size:.82rem;color:var(--muted)}
.avis-dots{display:flex;justify-content:center;gap:4px;margin-top:16px}
.avis-dots:empty{display:none}
.avis-dots button{width:28px;height:28px;padding:0;border:0;background:none;cursor:pointer;display:grid;place-items:center}
.avis-dots button::before{content:"";width:8px;height:8px;border-radius:999px;background:var(--line);transition:width .3s,background .3s}
.avis-dots button.on::before{width:26px;background:var(--accent)}
@media (max-width:1023px){.avis{flex-basis:calc((100% - 16px)/2)}}
@media (max-width:700px){.avis-piste{gap:10px}.avis{flex-basis:100%;padding:18px;gap:10px;border-radius:14px}.avis .q{width:24px;height:24px}.avis blockquote{font-size:.98rem}.avis-dots{margin-top:12px}}
"""

TEASER = """<section id="prog-teaser" class="pt-sec">
  <div class="wrap">
    <a class="pt reveal" href="programmes.html">
      <span class="pt-logo"><img src="athlyse-logo-blanc.png" alt="" width="57" height="47"></span>
      <span class="pt-txt"><span class="eyebrow">Tu préfères t'entraîner seul ?</span><b>Programmes de force athlétique Fondations</b><small>3 ou 4 séances par semaine · sur l'appli Athlyse · 29 €</small></span>
      <span class="btn pt-btn">Voir les programmes <span class="arr">→</span></span>
    </a>
  </div>
</section>

"""
TEASER_CSS = """
/* TEST bandeau programmes (page d'accueil) */
.pt-sec{padding-block:0 8px}
.pt{display:grid;grid-template-columns:auto minmax(0,1fr) auto;align-items:center;gap:20px;padding:22px 26px;border:1px solid var(--accent);border-radius:18px;background:color-mix(in srgb,var(--accent) 8%,var(--surface));color:var(--ink);text-decoration:none;transition:transform .2s}
.pt:hover{transform:translateY(-2px)}
.pt-logo{width:56px;height:56px;border-radius:14px;display:grid;place-items:center;background:color-mix(in srgb,var(--accent) 18%,transparent)}
.pt-logo img{width:32px;height:auto;display:block}
.pt-txt{display:grid;gap:4px;min-width:0}
.pt-txt b{font-family:var(--f-display);font-size:clamp(1.3rem,2.4vw,1.9rem);font-weight:800;text-transform:uppercase;line-height:1.05}
.pt-txt small{color:var(--muted);font-size:.88rem}
.pt-btn{white-space:nowrap}
@media (max-width:820px){.pt{grid-template-columns:auto minmax(0,1fr);gap:12px 14px;padding:16px}.pt-btn{grid-column:1/-1;justify-content:center}.pt-logo{width:48px;height:48px}.pt-logo img{width:28px}.pt-txt small{font-size:.8rem}.pt{align-items:start}}
/* TEST page programmes */
.pg-top{padding-top:clamp(28px,5vw,56px);padding-bottom:clamp(24px,4vw,40px)}
.pg-top + main, main + .call{margin-top:0}
main + section.call{padding-top:clamp(16px,3vw,32px)}
.head h1{font-size:clamp(2.4rem,6vw,4.4rem);font-weight:900}
"""

OUTILS = """<section id="pg-plus">
  <div class="wrap">
    <p class="eyebrow">Comment ça marche</p>
    <ol class="pp-steps reveal">
      <li><b>1</b><div><strong>Tu choisis ton programme</strong><span>3 ou 4 séances par semaine, 29 € en paiement unique.</span></div></li>
      <li><b>2</b><div><strong>Tu entres tes 1RM sur Athlyse</strong><span>Squat, développé couché, soulevé de terre. Tu ne les connais pas ? Estime-les avec le calculateur de la page.</span></div></li>
      <li><b>3</b><div><strong>Tu t'entraînes</strong><span>Tes séances et tes charges sont prêtes, semaine après semaine.</span></div></li>
    </ol>
    <div class="pp-tools">
      <div class="pp-box reveal" id="quiz"><div class="pp-top">
        <p class="eyebrow">Quiz · 3 questions</p>
        <h2 class="pp-h">Quel programme pour toi ?</h2>
        <fieldset class="pp-q" data-q="j"><legend>Combien de jours peux-tu t'entraîner par semaine ?</legend><div class="pp-opt"><button type="button" data-v="3">3 jours</button><button type="button" data-v="4">4 jours ou plus</button></div></fieldset>
        <fieldset class="pp-q" data-q="x"><legend>Depuis combien de temps tu fais de la musculation ?</legend><div class="pp-opt"><button type="button" data-v="0">Moins d'1 an</button><button type="button" data-v="1">1 an ou plus</button></div></fieldset>
        <fieldset class="pp-q" data-q="r"><legend>Tu connais tes 1RM ?</legend><div class="pp-opt"><button type="button" data-v="1">Oui</button><button type="button" data-v="0">Pas vraiment</button></div></fieldset></div>
        <div class="pp-res" id="quizRes" aria-live="polite"><div class="pp-v on" data-k="0"><p>Réponds aux 3 questions pour voir le programme conseillé.</p></div><div class="pp-v" data-k="4"><div><strong>Conseillé : 4 séances / semaine</strong><p>Tu as le temps et l'habitude de t'entraîner.<span class="pp-r"> Estime d'abord tes 1RM.</span></p></div><a class="pp-go" href="#programmes">Voir →</a></div><div class="pp-v" data-k="3d"><div><strong>Conseillé : 3 séances / semaine</strong><p>Tu débutes : tu récupères mieux.<span class="pp-r"> Estime d'abord tes 1RM.</span></p></div><a class="pp-go" href="#programmes">Voir →</a></div><div class="pp-v" data-k="3"><div><strong>Conseillé : 3 séances / semaine</strong><p>Il colle à ton rythme.<span class="pp-r"> Estime d'abord tes 1RM.</span></p></div><a class="pp-go" href="#programmes">Voir →</a></div></div>
      </div>
      <div class="pp-box reveal" id="calcul"><div class="pp-top">
        <p class="eyebrow">Outil gratuit</p>
        <h2 class="pp-h">Estime ton 1RM</h2>
        <p class="pp-lead">Entre une charge que tu as soulevée et le nombre de répétitions faites avec une bonne technique.</p>
        <div class="pp-in">
          <label>Charge (kg)<input id="rmW" type="number" enterkeyhint="next" inputmode="decimal" min="1" max="500" step="0.5" placeholder="ex. 80"></label>
          <label>Répétitions<input id="rmR" type="number" enterkeyhint="done" inputmode="numeric" min="1" max="10" step="1" placeholder="1 à 10"></label>
        </div>
        <p class="pp-note">Estimation (formule d'Epley), fiable surtout entre 1 et 10 répétitions. Fais le calcul pour chacun des 3 mouvements.</p></div>
        <div class="pp-res pp-rm" aria-live="polite"><span>Ton 1RM estimé</span><output id="rmOut">— kg</output></div>
      </div>
    </div>
  </div>
</section>
<script>
(function(){
var a={},res=document.getElementById('quizRes');
document.querySelectorAll('.pp-q').forEach(function(f){f.addEventListener('click',function(e){var b=e.target.closest('button');if(!b)return;
f.querySelectorAll('button').forEach(function(x){x.classList.toggle('on',x===b);x.setAttribute('aria-pressed',x===b)});a[f.dataset.q]=b.dataset.v;show()})});
function show(){if(!('j'in a&&'x'in a&&'r'in a))return;
var k=a.j==='4'&&a.x==='1'?'4':(a.j==='4'?'3d':'3');
res.querySelectorAll('.pp-v').forEach(function(v){v.classList.toggle('on',v.dataset.k===k)});res.classList.toggle('no1rm',a.r==='0')}
var W=document.getElementById('rmW'),R=document.getElementById('rmR'),O=document.getElementById('rmOut');
function rm(){var w=parseFloat(W.value.replace(',','.')),r=parseInt(R.value,10);
if(!(w>0&&w<=500&&r>=1&&r<=10)){O.textContent='— kg';return}
var v=r===1?w:w*(1+r/30);O.textContent=(Math.round(v*2)/2).toString().replace('.',',')+' kg'}
W.addEventListener('input',rm);R.addEventListener('input',rm);
document.addEventListener('pointerdown',function(e){var f=document.activeElement;if(f&&(f===W||f===R)&&e.target!==W&&e.target!==R)f.blur()});
[W,R].forEach(function(i){i.addEventListener('keydown',function(e){if(e.key==='Enter'){e.preventDefault();i===W?R.focus():i.blur()}})});
})();
</script>
"""
OUTILS_CSS = """
/* TEST outils page programmes */
#pg-plus{padding-top:0}
.pp-steps{list-style:none;margin:10px 0 0;padding:0;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}
.pp-steps li{display:flex;gap:14px;align-items:flex-start;background:var(--surface);border:1px solid var(--line);border-radius:18px;padding:20px}
.pp-steps li>b{flex:none;width:36px;height:36px;border-radius:50%;background:var(--accent);color:var(--on-accent);display:grid;place-items:center;font-family:var(--f-display);font-size:1.2rem}
.pp-steps strong{display:block;margin-bottom:4px}.pp-steps span{color:var(--muted);font-size:.9rem;line-height:1.4}
.pp-tools{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px;margin-top:16px;align-items:stretch}
.pp-box{display:flex;flex-direction:column;gap:14px;background:var(--surface);border:1px solid var(--line);border-radius:18px;padding:24px;min-width:0}
.pp-box .eyebrow{margin:0}
.pp-top{display:flex;flex-direction:column;gap:14px;min-width:0}
.pp-tools{grid-template-rows:auto auto;row-gap:0}.pp-box{display:grid;grid-row:span 2;grid-template-rows:subgrid;row-gap:14px}.pp-box .pp-res{margin-top:0}
.pp-h{font-size:clamp(1.6rem,3vw,2.2rem);margin:0}
.pp-q{border:0;margin:0;padding:0;min-width:0}
.pp-q legend{padding:0;margin-bottom:8px;font-weight:700;font-size:.95rem}
.pp-opt{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px}
.pp-opt button{font:inherit;font-size:.9rem;font-weight:700;padding:11px 10px;border-radius:12px;border:1px solid var(--line);background:var(--bg);color:var(--ink);cursor:pointer}
.pp-opt button.on{background:var(--accent);border-color:var(--accent);color:var(--on-accent)}
.pp-res{margin-top:auto;border:1px solid var(--accent);border-radius:12px;background:color-mix(in srgb,var(--accent) 10%,transparent);padding:14px 16px;display:grid;align-content:center}
.pp-res{grid-template-areas:"v"}.pp-v{grid-area:v;display:grid;gap:6px;align-content:center;visibility:hidden}.pp-v.on{visibility:visible}.pp-r{display:inline}.pp-res:not(.no1rm) .pp-v.on .pp-r{visibility:hidden}
.pp-res p{margin:0;font-size:.9rem;color:var(--muted)}
.pp-res .eyebrow{margin:0}
.pp-res strong{font-family:var(--f-display);font-size:1.2rem;line-height:1.15;display:block}
.pp-v[data-k]:not([data-k="0"]){grid-template-columns:minmax(0,1fr) auto;align-items:center;gap:4px 14px}
.pp-go{color:var(--accent);font-weight:700;text-decoration:none;white-space:nowrap;font-size:.92rem}
#quizRes{padding:12px 14px}
@media (max-width:600px){.pp-v[data-k]:not([data-k="0"]){grid-template-columns:minmax(0,1fr)}.pp-go{justify-self:start}}
@media (max-width:374px){.pp-opt button{font-size:.8rem;padding:10px 4px}}
.pp-res .btn{justify-self:start;margin-top:4px;padding:10px 18px;font-size:.88rem}
.pp-lead{margin:0;color:var(--muted);font-size:.92rem}
.pp-in{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}
.pp-in label{display:grid;gap:6px;font-weight:700;font-size:.9rem;min-width:0}
.pp-rm{justify-items:center;text-align:center}
.pp-rm span{color:var(--muted);font-size:.9rem}
.pp-rm output{font-family:var(--f-display);font-size:clamp(2.2rem,5vw,2.8rem);font-weight:900;line-height:1}
.pp-note{margin:0;font-size:.78rem;color:var(--muted)}
@media (max-width:820px){
.pp-steps{grid-template-columns:minmax(0,1fr);gap:10px}.pp-steps li{padding:14px}
.pp-tools{grid-template-columns:minmax(0,1fr);gap:10px;margin-top:10px}
.pp-box{padding:16px;gap:12px;grid-row:auto;grid-template-rows:auto auto;row-gap:12px}.pp-tools{row-gap:10px}.pp-top{gap:12px}
.pp-res{min-height:0}

}
"""

QUESTION = """<section id="question" class="pq-sec">
  <div class="wrap">
    <div class="pq reveal">
      <div class="pq-txt"><p class="eyebrow">Une question avant d'acheter ?</p><h2 class="pp-h">Écris-moi.</h2><p>Ton niveau, ton matériel, le choix entre 3 et 4 séances : je te réponds avant que tu achètes.</p></div>
      <div class="pq-acts"><a class="btn" href="mailto:alexis.bloquecoaching@gmail.com?subject=Question%20sur%20les%20programmes%20Fondations">Écrire un mail</a><a class="btn ghost" href="https://www.instagram.com/alexisblq_coaching/" target="_blank" rel="noopener">Instagram</a></div>
    </div>
  </div>
</section>
"""
QUESTION_CSS = """
/* TEST petit contact page programmes */
.pq-sec{padding-top:0}
.pq{display:grid;grid-template-columns:minmax(0,1fr) auto;align-items:center;gap:20px 40px;background:var(--surface);border:1px solid var(--line);border-radius:18px;padding:24px}
.pq-txt{display:grid;gap:8px;min-width:0}.pq-txt .eyebrow{margin:0}.pq-txt p:last-child{margin:0;color:var(--muted);font-size:.92rem}
.pq-acts{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}
.pq-acts .btn{margin:0;justify-content:center;align-self:stretch}
@media (max-width:820px){.pq{grid-template-columns:minmax(0,1fr);padding:16px;gap:14px}}
@media (max-width:429px){.pq-acts{grid-template-columns:minmax(0,1fr)}}
.pq-acts .btn{white-space:nowrap}
"""

h = open('index.html').read()
k = h.index('</style>', h.index('/* Tablette'))
h = h[:k] + CSS + AVIS_CSS + TEASER_CSS + OUTILS_CSS + QUESTION_CSS + h[k:]
base = h  # page commune avant les ajouts propres à l'accueil

# ---- Accueil : avis + bandeau, sans la rubrique complète
h = h.replace('<section id="formules">', AVIS + '<section id="formules">', 1)
h = h.replace('<section id="faq">', TEASER + '<section id="faq">', 1)
h = h.replace('<li><a href="#formules">Tarifs</a></li>', '<li><a href="#formules">Tarifs</a></li>\n      <li><a href="programmes.html">Programmes</a></li>', 1)
MENU_OLD = '<a href="#formules"><small>04</small>Tarifs</a>'
MENU_NEW = '<a href="#avis"><small>04</small>Avis</a>\n    <a href="#formules"><small>05</small>Tarifs</a>\n    <a href="programmes.html"><small>06</small>Programmes</a>'
def menu(x):
    return (x.replace(MENU_OLD, MENU_NEW).replace('<small>05</small>FAQ', '<small>07</small>FAQ')
             .replace('<small>06</small>Commencer', '<small>08</small>Commencer'))
h = menu(h)
open(os.path.join(out, 'index.html'), 'w').write(inline(h))

# ---- Page Programmes : même en-tête, même pied, même contact
g = base
top = g[:g.index('<header class="hero"')]
end = g[g.index('<section class="call" id="appel">'):]
end = QUESTION + end[end.index('<footer'):]
body = SECTION.replace('<section id="programmes">', '<section id="programmes" class="pg-top">', 1)
body = re.sub(r'<h2 style="margin-top:10px">(.*?)</h2>', r'<h1 style="margin-top:10px">\1</h1>', body, count=1)
g = top + '<main>\n' + body + OUTILS + '</main>\n' + end
g = menu(g)
g = re.sub(r'<a class="bubble".*?</a>\n?', '', g, count=1, flags=re.S)
for sid in ('top', 'parcours', 'methode', 'appli', 'avis', 'formules', 'faq', 'appel'):
    g = g.replace(f'href="#{sid}"', f'href="index.html#{sid}"')
g = g.replace('href="programmes.html"', 'href="#programmes"')
g = g.replace('<li><a href="index.html#formules">Tarifs</a></li>', '<li><a href="index.html#formules">Tarifs</a></li>\n      <li><a href="#programmes">Programmes</a></li>', 1)
g = g.replace('<title>Alexis Coaching</title>', "<title>Programmes Fondations · Alexis Coaching</title>", 1)
n = g.index('<nav class="nav"')
g = ('<!doctype html>\n<html lang="fr">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n'
     + g[:n].replace('<meta name="claude:viewport-fit-sides" content="cover">\n', '') + '</head>\n<body>\n' + g[n:] + '\n</body>\n</html>\n')
open(os.path.join(out, 'programmes.html'), 'w').write(inline(g))

l = open('liens.html').read()
ic = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18M3 15h18M9 3v18"/></svg>'
btn = f'    <a class="l" href="programmes.html"><span class="i ath"><img src="athlyse-logo-blanc.png" alt="" width="26" height="21"></span><span>Programme force athlétique<small>Sur Athlyse · en autonomie · 29 €</small></span><span class="go">→</span></a>\n'
j = l.index('    <a class="l" href="https://calendly.com')
l = l[:j] + btn + l[j:]
l = l.replace('</style>', '.l .i.ath img{width:26px;height:auto;display:block}\n</style>', 1)
open(os.path.join(out, 'liens.html'), 'w').write(inline(l))
print('ok')
