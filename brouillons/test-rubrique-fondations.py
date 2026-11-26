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
      <div><p class="eyebrow ath-eb"><img src="athlyse-logo-blanc.png" alt="Logo Athlyse" width="57" height="47"><span>Programme de force athlétique · sur l'appli Athlyse</span></p><h2 style="margin-top:10px">Fondations :<br>la force athlétique en autonomie.</h2></div>
      <p>Un programme de 4 semaines sur squat, développé couché et soulevé de terre, à suivre seul et à ton rythme, directement sur l'appli Athlyse.</p>
    </div>
    <div class="prog-grid">
      <div class="prog-left reveal">
        <article class="prog-row">
          <div><p class="eyebrow">Sur l'appli Athlyse</p><h3>3 jours / semaine</h3><p class="muted">Squat et développé couché, une séance légère, une séance lourde.</p></div>
          <div class="prog-buy"><div class="price">29 €</div><a class="btn" href="#programmes">Acheter</a></div>
        </article>
        <article class="prog-row">
          <div><p class="eyebrow">Sur l'appli Athlyse</p><h3>4 jours / semaine</h3><p class="muted">Plus de séances pour travailler chaque mouvement plus souvent.</p></div>
          <div class="prog-buy"><div class="price">29 €</div><a class="btn" href="#programmes">Acheter</a></div>
        </article>
        <ul class="prog-inc">
          <li><b>Tout se passe sur l'appli Athlyse</b><span>Tu télécharges l'appli et tu retrouves tes séances jour par jour, avec les consignes de chaque exercice et de chaque variante.</span></li>
          <li><b>Tes charges calculées à partir de tes 1RM</b><span>Et la charge monte chaque semaine, sans que tu aies à calculer.</span></li>
        </ul>
        <p class="prog-auto">{INFO}<span>En autonomie, sans suivi : après l'achat, il n'y a ni retour sur ta technique, ni échange avec moi. Tout est expliqué dans l'appli.</span></p>
        <p class="prog-pay">Paiement unique · accès illimité · programme sur l'appli Athlyse</p>
      </div>
      <figure class="prog-shot reveal"><img src="{IMG}" alt="Le programme Fondations dans l'appli Athlyse : jour 1 de la semaine 1"><figcaption>Exemple : jour 1, semaine 1 (1RM squat 100 kg, développé couché 70 kg)</figcaption></figure>
    </div>
    <p class="prog-note reveal">Envie d'aller plus loin avec un suivi personnalisé ? <a href="#appel">On en parle →</a></p>
  </div>
</section>

"""

CSS = """
/* TEST rubrique programmes */
.prog-grid{display:grid;grid-template-columns:minmax(0,1.2fr) minmax(0,.8fr);gap:56px;align-items:center}
.prog-left{display:grid;gap:14px;min-width:0}
.prog-row{display:flex;justify-content:space-between;align-items:center;gap:16px;background:var(--surface);border:1px solid var(--line);border-radius:18px;padding:18px 20px}
.prog-row h3{font-size:1.7rem;font-weight:800;margin:2px 0 4px}.prog-row .muted{margin:0;font-size:.9rem}
.prog-buy{display:grid;gap:8px;justify-items:center;flex:none}
.prog-buy .price{font-size:2.4rem}.prog-buy .btn{padding:10px 22px}
.prog-inc{list-style:none;margin:6px 0 0;padding:0;display:grid;gap:12px}.prog-inc li{display:grid;gap:2px;padding-left:16px;border-left:3px solid var(--accent)}.prog-inc span{color:var(--muted);font-size:.92rem}
.prog-shot{margin:0;display:grid;gap:10px;justify-items:center;min-width:0}
.prog-shot img{width:min(300px,100%);height:auto;display:block;border-radius:44px;border:10px solid #1C2B42;box-shadow:0 0 0 2px var(--line),0 50px 90px -30px rgba(0,0,0,.8),0 0 120px -20px color-mix(in srgb,var(--accent) 45%,transparent)}
.prog-shot figcaption{font-size:.78rem;color:var(--muted);text-align:center;max-width:300px}
.prog-auto{display:flex;gap:10px;align-items:flex-start;margin:0;padding:12px 14px;border:1px solid var(--accent);border-radius:12px;background:color-mix(in srgb,var(--accent) 10%,transparent);color:var(--ink);font-size:.88rem;line-height:1.45}
.prog-auto svg{width:20px;height:20px;color:var(--accent);flex:none;margin-top:1px}
.prog-pay{margin:0;font-size:.8rem;color:var(--muted)}
.prog-note{margin-top:22px;text-align:center;color:var(--muted);font-size:.95rem}
.prog-note a{color:var(--accent);font-weight:700;text-decoration:none;white-space:nowrap}
@media (max-width:820px){.prog-grid{grid-template-columns:1fr;gap:28px}.prog-shot{order:-1}.prog-shot img{width:230px;border-radius:34px;border-width:7px}}
@media (max-width:420px){.prog-row{padding:14px}.prog-row h3{font-size:1.35rem}.prog-row .muted{font-size:.82rem}.prog-buy .price{font-size:1.9rem}.prog-buy .btn{padding:9px 16px}}
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
