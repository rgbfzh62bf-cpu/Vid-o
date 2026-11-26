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
          <li>Tes charges calculées automatiquement à partir de tes maxi</li>
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
    <div class="plans">
      <article class="plan reveal">
        <div><p class="eyebrow">Fondations</p><h3>3 jours<br>par semaine</h3></div>
        <div class="price">29 €<small>paiement unique</small></div>
        <p class="muted">Pour t'entraîner 3 fois par semaine : une séance squat et développé couché, une séance légère et une séance lourde sur les trois mouvements.</p>
        <ul>
{common}
        </ul>
        <a class="btn" href="#programmes">Acheter le programme <span class="arr">→</span></a>
      </article>
      <article class="plan reveal">
        <div><p class="eyebrow">Fondations</p><h3>4 jours<br>par semaine</h3></div>
        <div class="price">29 €<small>paiement unique</small></div>
        <p class="muted">Pour t'entraîner 4 fois par semaine, avec plus de séances pour travailler chaque mouvement plus souvent.</p>
        <ul>
{common}
        </ul>
        <a class="btn" href="#programmes">Acheter le programme <span class="arr">→</span></a>
      </article>
    </div>
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
#programmes .price small{margin-left:8px}
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
