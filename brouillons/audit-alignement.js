const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();
const groups=['.stat-row > .stat','.steps > .step','.plans > .plan','.ways > .way','.ba > figure','.prog-steps > li','.stores > .store'];
const btns=[['.plans > .plan','.btn'],['.ways > .way','.acts']];
for(const w of [320,390,768,1024,1440]){const p=await b.newPage({viewport:{width:w,height:900}});await p.goto('file://'+process.argv[2]);
await p.evaluate(()=>document.querySelectorAll('.reveal').forEach(x=>{x.classList.add('in');x.style.transform='none'}));await p.waitForTimeout(500);
const r=await p.evaluate(([groups,btns])=>{const out=[];
 for(const g of groups){const els=[...document.querySelectorAll(g)];const rows={};els.forEach(e=>{const b=e.getBoundingClientRect();const k=Math.round(b.top);(rows[k]=rows[k]||[]).push(b)});
  for(const k in rows){const a=rows[k];if(a.length<2)continue;const hs=a.map(x=>Math.round(x.height));if(Math.max(...hs)-Math.min(...hs)>1)out.push(g+' hauteurs '+hs.join('/'))}}
 for(const [g,s] of btns){const els=[...document.querySelectorAll(g)];const rows={};els.forEach(e=>{const k=Math.round(e.getBoundingClientRect().top);const bb=e.querySelector(s);if(bb)(rows[k]=rows[k]||[]).push(Math.round(bb.getBoundingClientRect().top))});
  for(const k in rows){const a=rows[k];if(a.length>1&&Math.max(...a)-Math.min(...a)>1)out.push(g+' '+s+' décalés '+a.join('/'))}}
 // hero/appli/parcours two-column bottoms
 const pairs=[['.hero .wrap > div:first-child','.hero .wrap > figure, .hero .wrap > .photo'],['.app-txt','.phone-wrap']];
 for(const [x,y] of pairs){const A=document.querySelector(x),B=document.querySelector(y);if(A&&B){const a=A.getBoundingClientRect(),c=B.getBoundingClientRect();if(Math.abs(a.top-c.top)<300&&a.left!=c.left)out.push(x+' vs '+y+' haut '+Math.round(a.top-c.top)+' bas '+Math.round(a.bottom-c.bottom))}}
 return out},[groups,btns]);
console.log(w,r.length?r:'OK')}await b.close()})()
