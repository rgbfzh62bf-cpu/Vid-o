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
      <div><p class="eyebrow ath-eb"><img src="athlyse-logo-blanc.png" alt="Logo Athlyse" width="57" height="47"><span>Programmes à acheter · force athlétique · sur l'appli Athlyse</span></p><h2 style="margin-top:10px">Pas prêt pour un coaching ?<br>Achète ton programme.</h2></div>
      <p>Fondations, ce sont deux programmes de force athlétique tout prêts, de 4 semaines, sur squat, développé couché et soulevé de terre. Tu en achètes un, une seule fois à 29 €, et tu le suis seul sur l'appli Athlyse.</p>
    </div>
    <div class="prog-grid">
      <div class="prog-cards reveal">
        <article class="prog-row">
          <div><p class="eyebrow">Programme Fondations</p><h3>3 jours / semaine</h3><p class="muted">Squat et développé couché, une séance légère, une séance lourde.</p></div>
          <div class="prog-buy"><div class="price">29 €<small>paiement unique</small></div><a class="btn" href="#programmes">Acheter</a></div>
        </article>
        <article class="prog-row">
          <div><p class="eyebrow">Programme Fondations</p><h3>4 jours / semaine</h3><p class="muted">Plus de séances pour travailler chaque mouvement plus souvent.</p></div>
          <div class="prog-buy"><div class="price">29 €<small>paiement unique</small></div><a class="btn" href="#programmes">Acheter</a></div>
        </article>
      </div>
      <figure class="prog-shot reveal"><img src="{IMG}" alt="Le programme Fondations dans l'appli Athlyse : jour 1 de la semaine 1"><figcaption>Exemple : jour 1, semaine 1 (1RM squat 100 kg, développé couché 70 kg)</figcaption></figure>
      <div class="prog-more reveal">
        <ol class="prog-steps"><li><b>1</b><span>Tu achètes le programme : paiement unique de 29 €</span></li><li><b>2</b><span>Tu le reçois sur l'appli Athlyse</span></li><li><b>3</b><span>Tu t'entraînes seul, à ton rythme</span></li></ol>
        <ul class="prog-inc">
          <li><b>Tout se passe sur l'appli Athlyse</b><span>Tu télécharges l'appli et tu retrouves tes séances jour par jour, avec les consignes de chaque exercice et de chaque variante.</span></li>
          <li><b>Tes charges calculées à partir de tes 1RM</b><span>Et la charge monte chaque semaine, sans que tu aies à calculer.</span></li>
        </ul>
        <p class="prog-auto">{INFO}<span>En autonomie, sans suivi : après l'achat, il n'y a ni retour sur ta technique, ni échange avec moi. Tout est expliqué dans l'appli.</span></p>
        <p class="prog-pay">Une fois acheté, le programme reste accessible sans limite de durée</p>
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
@media (max-width:360px){.prog-buy .btn{flex:1 1 100%;justify-content:center}}
.prog-shot img{width:100%;border-radius:24px;border-width:5px}
.prog-shot figcaption{font-size:.6rem;line-height:1.3}
}
@media (min-width:600px) and (max-width:820px){.prog-grid{grid-template-columns:minmax(0,1fr) 250px;gap:0 32px}.prog-row{padding:16px}.prog-row h3{font-size:1.5rem}.prog-row .muted{font-size:.88rem}.prog-buy .price{font-size:2rem}.prog-buy .btn{padding:9px 18px;font-size:.9rem}.prog-shot img{border-width:8px;border-radius:36px}.prog-shot figcaption{font-size:.72rem}}
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
