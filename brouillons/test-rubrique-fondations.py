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


IMG = 'data:image/jpeg;base64,' + base64.b64encode(open(os.path.join(HERE, 'fondations-athlyse.jpg'), 'rb').read()).decode()

LISTE = """          <li>Tes séances prêtes sur l'appli Athlyse, jour par jour</li>
          <li>Tes charges calculées à partir de tes 1RM</li>
          <li>La charge monte chaque semaine, sans que tu aies à calculer</li>
          <li>Les consignes de chaque exercice et de chaque variante</li>
          <li>Tu notes tes charges et ton ressenti à chaque séance</li>"""

INFO = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="M12 8v4M12 16h.01"/></svg>'

SECTION = f"""<section id="programmes">
  <div class="wrap">
    <div class="head reveal">
      <div><p class="eyebrow">Programme de force athlétique · en autonomie</p><h2 style="margin-top:10px">Fondations :<br>la force athlétique en autonomie.</h2></div>
      <p>Un programme de 4 semaines sur squat, développé couché et soulevé de terre, à suivre seul et à ton rythme, directement sur l'appli Athlyse.</p>
    </div>
    <article class="plan prog-card reveal">
      <figure class="prog-shot"><img src="{IMG}" alt="Le programme Fondations dans l'appli Athlyse : jour 1 de la semaine 1"><figcaption>Exemple : jour 1, semaine 1 (1RM squat 100 kg, développé couché 70 kg)</figcaption></figure>
      <div class="prog-side">
        <p class="eyebrow">Ce que tu reçois</p>
        <ul>
{LISTE}
        </ul>
        <p class="prog-auto">{INFO}<span>En autonomie, sans suivi : après l'achat, il n'y a ni retour sur ta technique, ni échange avec moi. Tout est expliqué dans l'appli.</span></p>
        <div class="prog-opts">
          <div class="prog-opt"><p class="eyebrow">3 jours / semaine</p><div class="price">29 €</div><p class="muted">Squat et développé couché, une séance légère, une séance lourde.</p><a class="btn" href="#programmes">Acheter</a></div>
          <div class="prog-opt"><p class="eyebrow">4 jours / semaine</p><div class="price">29 €</div><p class="muted">Plus de séances pour travailler chaque mouvement plus souvent.</p><a class="btn" href="#programmes">Acheter</a></div>
        </div>
        <p class="prog-pay">Paiement unique · accès illimité · programme sur l'appli Athlyse</p>
      </div>
    </article>
    <p class="prog-note reveal">Envie d'aller plus loin avec un suivi personnalisé ? <a href="#appel">On en parle →</a></p>
  </div>
</section>

"""

CSS = """
/* TEST rubrique programmes */
#programmes .prog-card{display:grid;grid-template-columns:minmax(0,.8fr) minmax(0,1.2fr);gap:28px;align-items:center}
.prog-shot{margin:0;display:grid;gap:10px;min-width:0;justify-items:center}
.prog-shot img{width:min(280px,100%);height:auto;display:block;border-radius:40px;border:8px solid #1C2B42;box-shadow:0 0 0 2px var(--line),0 30px 60px -25px rgba(0,0,0,.8)}
.prog-shot figcaption{font-size:.78rem;color:var(--muted);text-align:center}
.prog-side{display:grid;gap:14px;min-width:0}
.prog-side ul{margin:0}
.prog-auto{display:flex;gap:10px;align-items:flex-start;margin:0;padding:12px 14px;border:1px solid var(--accent);border-radius:12px;background:color-mix(in srgb,var(--accent) 10%,transparent);color:var(--ink);font-size:.88rem;line-height:1.45}
.prog-auto svg{width:20px;height:20px;color:var(--accent);flex:none;margin-top:1px}
.prog-opts{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}
.prog-opt{display:flex;flex-direction:column;gap:6px;border:1px solid var(--line);border-radius:14px;padding:14px;background:color-mix(in srgb,var(--bg) 45%,transparent)}
.prog-opt .price{font-size:2.4rem}.prog-opt .muted{font-size:.82rem;margin:0}
.prog-opt .btn{margin-top:auto;justify-content:center;align-self:stretch;padding-inline:10px}
.prog-pay{margin:0;font-size:.78rem;color:var(--muted);text-align:center}
.prog-note{margin-top:18px;text-align:center;color:var(--muted);font-size:.95rem}
.prog-note a{color:var(--accent);font-weight:700;text-decoration:none;white-space:nowrap}
@media (max-width:900px){#programmes .prog-card{grid-template-columns:1fr}}
@media (max-width:600px){.prog-shot img{width:220px;border-radius:32px;border-width:6px}.prog-opts{gap:8px}.prog-opt{padding:12px 10px}.prog-opt .price{font-size:2rem}.prog-opt .eyebrow{font-size:.6rem;letter-spacing:.06em}.prog-opt .muted{font-size:.78rem}}
"""

h = open('index.html').read()
i = h.index('<section id="faq">')
h = h[:i] + SECTION + h[i:]
k = h.index('</style>', h.index('/* Tablette'))
h = h[:k] + CSS + h[k:]
h = (h.replace('<a href="#formules"><small>04</small>Tarifs</a>',
               '<a href="#formules"><small>04</small>Tarifs</a>\n    <a href="#programmes"><small>05</small>Programmes</a>')
      .replace('<small>05</small>FAQ', '<small>06</small>FAQ')
      .replace('<small>06</small>Commencer', '<small>07</small>Commencer'))
open(os.path.join(out, 'index.html'), 'w').write(inline(h))

l = open('liens.html').read()
ic = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18M3 15h18M9 3v18"/></svg>'
btn = f'    <a class="l" href="index.html#programmes"><span class="i">{ic}</span><span>Programme force athlétique<small>Sur Athlyse · en autonomie · 29 €</small></span><span class="go">→</span></a>\n'
j = l.index('    <a class="l" href="https://calendly.com')
l = l[:j] + btn + l[j:]
open(os.path.join(out, 'liens.html'), 'w').write(inline(l))
print('ok')
