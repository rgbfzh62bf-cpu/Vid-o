"""Génère ../site-en-ligne/ (version publiée sur Netlify). Lancer après chaque modif : python3 site/build.py"""
import os,shutil
here=os.path.dirname(os.path.abspath(__file__)); out=os.path.join(here,'..','site-en-ligne')
shutil.rmtree(out,ignore_errors=True); os.makedirs(out)
desc="Alexis Bloqué, coach sportif diplômé. Programmation sur mesure et suivi nutrition en ligne, sur l'appli Athlyse. Appel découverte gratuit."
icon="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='14' fill='%230B1628'/%3E%3Ctext x='32' y='44' font-family='Arial' font-weight='900' font-size='34' text-anchor='middle' fill='%235B9BEF'%3EA%3C/text%3E%3C/svg%3E"
ICONS='<link rel="icon" type="image/png" sizes="48x48" href="/favicon.png">\n<link rel="icon" type="image/png" sizes="512x512" href="/favicon-512.png">\n<link rel="apple-touch-icon" href="/apple-touch-icon.png">\n<meta name="theme-color" content="#0B1628">'
def wrap(name,split):
    s=open(os.path.join(here,name)).read(); i=s.index(split)
    head=s[:i].replace('<meta name="claude:viewport-fit-sides" content="cover">\n','').strip()
    open(os.path.join(out,name),'w').write(f'''<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="description" content="{desc}">
<meta property="og:title" content="Alexis Coaching · Coach sportif">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="https://alexis-coaching.fr/partage.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta property="og:url" content="https://alexis-coaching.fr/">
{ICONS}
{head}
</head>
<body>
{s[i:].strip()}
</body>
</html>
''')
wrap('index.html','<nav class="nav"'); wrap('liens.html','<main>')
for f in os.listdir(here):
    if f.endswith(('.jpg','.png')): shutil.copy(os.path.join(here,f),out)
    elif f in ('mentions-legales.html','cgv.html'):
        t=open(os.path.join(here,f)).read().replace('</head>',ICONS+'\n</head>',1)
        open(os.path.join(out,f),'w').write(t)
print(sorted(os.listdir(out)))
