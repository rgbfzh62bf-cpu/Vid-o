"""Montages Athlyse des séances Fondations (semaine 1, 1RM d'exemple 100/70/120).
Usage : python3 montage_fondations.py <xlsx 3j recalculé> <xlsx 4j recalculé> <dossier travail>
Sortie : brouillons/athlyse/fondations-{3,4}j-jour{n}.jpg
"""
import sys, os, html, subprocess, shutil, openpyxl
HERE=os.path.dirname(os.path.abspath(__file__)); SITE=os.path.join(HERE,'..','site')
x3,x4,work=sys.argv[1:4]
os.makedirs(work,exist_ok=True)
shutil.copy(os.path.join(SITE,'ath-seance.jpg'),work); shutil.copy(os.path.join(SITE,'fonts','manrope.woff2'),work)

def days(path):
    ws=openpyxl.load_workbook(path,data_only=True)['SEMAINE 1']; out=[]; cur=None
    for r in ws.iter_rows(min_row=1,max_row=ws.max_row):
        c={openpyxl.utils.get_column_letter(i+1):x.value for i,x in enumerate(r)}
        if c.get('C')=='EXERCICE': cur={'ex':[],'tot':0}; out.append(cur); continue
        if cur is None: continue
        if c.get('C')=='TOTAL SÉANCE': cur['tot']=c.get('G') or 0; continue
        if c.get('C') and isinstance(c.get('D'),(int,float)): cur['ex'].append(c)
    return out

def fmt(v):
    s=('%g'%v).replace('.',','); return s
def name(ex):
    m=[]
    for e in ex:
        n=e['C'].lower()
        k='Squat' if n.startswith('squat') else 'DC' if n.startswith('développé') else 'SDT' if (n.startswith('soulevé') or n.startswith('deadlift') or n=='rdl') else None
        if k and k not in m: m.append(k)
    return ' · '.join(m)

CSS='''@font-face{font-family:M;src:url(manrope.woff2);font-weight:400 800}
body{margin:0;width:600px;height:1304px;background:url(ath-seance.jpg);position:relative;font-family:M,sans-serif;color:#151515;-webkit-font-smoothing:antialiased}
.w{position:absolute;background:#fff}.t{position:absolute;white-space:nowrap}
.k{font-size:13px;letter-spacing:.12em;color:#77756f;font-weight:600}.big{font-size:22px;font-weight:800}
.lab{font-size:13px;letter-spacing:.1em;color:#55534e;font-weight:600}
.ex{font-size:19px;font-weight:700}.tag{font-size:12px;letter-spacing:.1em;color:#77756f;font-weight:700;margin-left:6px}
.d{font-size:17px;color:#8a8883;font-weight:500}
.l{position:absolute;width:48px;height:48px;border-radius:50%;background:#f1f0ec;display:grid;place-items:center;font-weight:700;font-size:18px}
.ch{position:absolute;color:#b9b7b1;font-size:26px}
.vl{position:absolute;width:1px;background:#e6e4df}
.fab{position:absolute;left:497px;top:1055px;width:78px;height:78px;border-radius:50%;background:url(ath-seance.jpg) -497px -1055px;box-shadow:0 8px 24px rgba(91,72,230,.35)}'''

def page(ver,n,d):
    ex=d['ex']; sets=sum(int(e['D']) for e in ex)
    h=[f'<!doctype html><meta charset="utf-8"><style>{CSS}</style>']
    h.append('<div class="w" style="left:128px;top:580px;width:360px;height:52px"></div>')
    h.append(f'<div class="t k" style="left:130px;top:583px">FONDATIONS · {ver} JOURS · SEM. 1</div>')
    h.append(f'<div class="t big" style="left:130px;top:601px">Jour {n} — {html.escape(name(ex))}</div>')
    h.append('<div class="w" style="left:50px;top:672px;width:500px;height:64px"></div>')
    for x,lab,val in [(52,'EXERCICES',len(ex)),(229,'SÉRIES',sets),(404,'VOLUME',fmt(d['tot']).replace(',',' ') if float(d['tot']).is_integer() else fmt(d['tot']))]:
        if lab=='VOLUME':
            v=d['tot']; val=(f'{v:,.1f}'.rstrip('0').rstrip('.')).replace(',',' ').replace('.',',')+' kg'
        h.append(f'<div class="t lab" style="left:{x}px;top:679px">{lab}</div><div class="t big" style="left:{x}px;top:702px;font-size:21px">{val}</div>')
    h.append('<div class="vl" style="left:212px;top:690px;height:36px"></div><div class="vl" style="left:388px;top:690px;height:36px"></div>')
    h.append('<div class="w" style="left:30px;top:858px;width:540px;height:312px"></div>')
    y=872
    for i,e in enumerate(ex[:3]):
        main=isinstance(e['G'],(int,float))
        h.append(f'<div class="l" style="left:46px;top:{y+26}px">{"ABC"[i]}</div><div class="ch" style="left:534px;top:{y+20}px">›</div>')
        tag='<span class="tag">⤡ FORCE</span>' if main else ''
        h.append(f'<div class="t ex" style="left:112px;top:{y}px">{html.escape(e["C"])}{tag}</div>')
        if main:
            l1=f'{int(e["D"])}x{e["E"]}@{fmt(e["G"])}kg · {round(e["F"]*100)}% de 1RM'
            l2=f'RPE {e["H"]} · repos {e["I"]}'
            h.append(f'<div class="t d" style="left:112px;top:{y+32}px">{html.escape(l1)}</div><div class="t d" style="left:112px;top:{y+58}px">{html.escape(l2)}</div>'); y+=112
        else:
            rpe='' if e['H'] in ('—',None) else f'@RPE{e["H"]}'
            h.append(f'<div class="t d" style="left:112px;top:{y+32}px">{int(e["D"])}x({html.escape(str(e["E"]).replace("-"," - "))}){rpe}</div>'); y+=96
    h.append('<div class="fab"></div>')
    return '\n'.join(h)

import json
files=[]
for ver,path in (('3',x3),('4',x4)):
    for n,d in enumerate(days(path),1):
        p=os.path.join(work,f'{ver}j{n}.html'); open(p,'w').write(page(ver,n,d)); files.append((ver,n,p))
js="const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:600,height:1304}});for(const [f,o] of %s){await p.goto('file://'+f);await p.waitForTimeout(300);await p.screenshot({path:o,type:'jpeg',quality:86})}await b.close()})()" % json.dumps([[p,os.path.join(HERE,'athlyse',f'fondations-{v}j-jour{n}.jpg')] for v,n,p in files])
subprocess.run(['node','-e',js],check=True)
print([f'{v}j{n}' for v,n,_ in files])
