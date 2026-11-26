import re,base64,os,mimetypes,sys
mimetypes.add_type('font/woff2','.woff2')
site,out=sys.argv[1],sys.argv[2]
os.chdir(site)
def inline(h):
  def rep(m):
    p=m.group(2)
    if p.startswith(('http','data:','#','mailto','tel')) or not os.path.isfile(p): return m.group(0)
    t=mimetypes.guess_type(p)[0] or ''
    if not t.startswith(('image','font')): return m.group(0)
    return m.group(1)+'data:'+t+';base64,'+base64.b64encode(open(p,'rb').read()).decode()+m.group(3)
  h=re.sub(r'''((?:src|href|content)=["'])([^"']+)(["'])''',rep,h)
  h=re.sub(r'''(url\(["']?)([^"')]+)(["']?\))''',rep,h)
  return re.sub(r'<link rel="preload"[^>]*>\n?','',h)
common='''          <li>Programme de force athlétique : squat, développé couché, soulevé de terre</li>
          <li>Tes charges calculées automatiquement à partir de tes 1RM</li>
          <li>4 semaines de progression : la charge monte chaque semaine</li>
          <li>Chaque exercice et chaque variante expliqués pas à pas</li>
          <li>Guide de séance, lexique et questions fréquentes</li>
          <li>Sur Google Sheets : téléphone, tablette ou ordinateur</li>'''
sec=f'''<section id="programmes">
  <div class="wrap">
    <div class="head reveal">
      <div><p class="eyebrow">Programme de force athlétique · en autonomie</p><h2 style="margin-top:10px">Fondations :<br>la force athlétique en autonomie.</h2></div>
      <p>Fondations est un programme de force athlétique de 4 semaines sur les trois mouvements : squat, développé couché et soulevé de terre. Tu le suis seul, à ton rythme, dans un tableur qui calcule tes charges pour toi.</p>
    </div>
    <div class="auto-box reveal"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="M12 8v4M12 16h.01"/></svg><p><b>Programme en autonomie, sans suivi.</b> Après l'achat, tu reçois ton fichier et tu t'entraînes seul : il n'y a ni retour sur ta technique, ni échange avec moi, ni ajustement personnalisé. Tout est expliqué dans le tableur.</p></div>
    <article class="plan prog-card reveal">
      <div><p class="eyebrow">Fondations · force athlétique</p><h3>4 semaines<br>de programme</h3></div>
      <ul>
{common}
      </ul>
      <div class="prog-opts">
        <div class="prog-opt"><p class="eyebrow">3 jours / semaine</p><div class="price">29 €</div><p class="muted">Squat et développé couché, une séance légère, une séance lourde.</p><a class="btn" href="#programmes">Acheter</a></div>
        <div class="prog-opt"><p class="eyebrow">4 jours / semaine</p><div class="price">29 €</div><p class="muted">Plus de séances pour travailler chaque mouvement plus souvent.</p><a class="btn" href="#programmes">Acheter</a></div>
      </div>
    </article>
    <p class="prog-note reveal">Paiement unique · accès illimité · tu reçois ton tableur par e-mail juste après l'achat. Tu veux un programme fait pour toi, des retours sur ta technique et des échanges avec moi ? C'est le <a href="#formules">coaching</a>.</p>
  </div>
</section>

'''
css='''
/* TEST rubrique programmes */
.prog-note{margin-top:20px;color:var(--muted);font-size:.92rem;text-align:center;max-width:62ch;margin-inline:auto}
.prog-note a{color:var(--accent)}
.auto-box{display:flex;gap:12px;align-items:flex-start;border:1px solid var(--accent);background:color-mix(in srgb,var(--accent) 10%,transparent);border-radius:16px;padding:14px 18px;margin-bottom:20px;max-width:820px}
.auto-box svg{width:22px;height:22px;color:var(--accent);flex:none;margin-top:2px}
.auto-box p{margin:0;color:var(--muted);font-size:.95rem}.auto-box b{display:block;color:var(--ink);margin-bottom:2px}
#programmes .prog-card{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.1fr);gap:20px 32px;align-items:start}
#programmes .prog-card ul{grid-column:1}#programmes .prog-card>div:first-child{grid-column:1}#programmes .prog-opts{grid-column:2;grid-row:1/3;align-self:center}
@media (max-width:820px){#programmes .prog-card{grid-template-columns:1fr}#programmes .prog-opts{grid-column:1;grid-row:auto}}
.prog-opts{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}
.prog-opt{display:flex;flex-direction:column;gap:8px;border:1px solid var(--line);border-radius:16px;padding:16px;background:color-mix(in srgb,var(--bg) 45%,transparent)}
.prog-opt .price{font-size:2.6rem}.prog-opt .muted{font-size:.85rem;margin:0}
.prog-opt .btn{margin-top:auto;justify-content:center;align-self:stretch;padding-inline:10px}
.auto-box{max-width:none}
@media (max-width:600px){.prog-opts{gap:8px}.prog-opt{padding:12px 10px}.prog-opt .price{font-size:2rem}.prog-opt .eyebrow{font-size:.6rem;letter-spacing:.06em}.prog-opt .muted{font-size:.78rem}}
'''
h=open('index.html').read()
i=h.index('<section id="faq">');h=h[:i]+sec+h[i:]
k=h.index('</style>',h.index('/* Tablette'));h=h[:k]+css+h[k:]
h=h.replace('<a href="#formules"><small>04</small>Tarifs</a>','<a href="#formules"><small>04</small>Tarifs</a>\n    <a href="#programmes"><small>05</small>Programmes</a>').replace('<small>05</small>FAQ','<small>06</small>FAQ').replace('<small>06</small>Commencer','<small>07</small>Commencer')
open(os.path.join(out,'index.html'),'w').write(inline(h))
l=open('liens.html').read()
ic='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18M3 15h18M9 3v18"/></svg>'
btn=f'    <a class="l" href="index.html#programmes"><span class="i">{ic}</span><span>Programme force athlétique<small>En autonomie · sans suivi · 29 €</small></span><span class="go">→</span></a>\n'
j=l.index('    <a class="l" href="https://calendly.com');l=l[:j]+btn+l[j:]
open(os.path.join(out,'liens.html'),'w').write(inline(l))
# version non inlinée pour tests
open(os.path.join(out,'raw-index.html'),'w').write(h);open(os.path.join(out,'raw-liens.html'),'w').write(l)
print('ok')
