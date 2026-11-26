import sys, openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.drawing.image import Image
from openpyxl.chart import BarChart, Reference
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import FormulaRule

NAVY='0B1628'; SURF='12223A'; ACC='5B9BEF'; ACC2='8EC0FF'; LINE='C9D6E8'; INPUT='E3EEFD'; PALE='F4F7FB'; MUTED='5A6B85'; WHITE='FFFFFF'
F='Arial'
def fill(c): return PatternFill('solid',fgColor=c)
thin=Side(style='thin',color=LINE); B=Border(left=thin,right=thin,top=thin,bottom=thin)
def font(sz=10,b=False,c='1A2333',i=False): return Font(name=F,size=sz,bold=b,color=c,italic=i)
CENTER=Alignment(horizontal='center',vertical='center',wrap_text=True)
LEFT=Alignment(horizontal='left',vertical='center',wrap_text=True)

# ---------- PROGRAMMES ----------
# (type, exercice, séries, reps, %1RM S1, RPE cible, repos, consigne)
# type S/B/D = mouvement compté dans le bilan ; '' = renfo (charge libre, RPE 8)
P4={
 'JOUR 1 · SQUAT & DÉVELOPPÉ COUCHÉ':[
  ('S','Squat pause 2 temps',4,4,.65,'6','3-4 min','Pause 2 s en bas, gainage serré, sans te relâcher.'),
  ('B','Développé couché',4,6,.67,'6-7','3 min','Fesses posées, omoplates serrées, barre touche la poitrine.'),
  ('','Tirage vertical poulie',3,'10-12',None,'8','2 min','Tire vers le haut de la poitrine, buste fixe.'),
  ('','Élévations latérales haltères',3,'12-15',None,'8','1-2 min','Coudes légèrement fléchis, monte à hauteur d’épaules.')],
 'JOUR 2 · SOULEVÉ DE TERRE':[
  ('B','Développé couché pause 3 temps',3,3,.65,'6','3 min','Pause 3 s sur la poitrine, barre immobile.'),
  ('D','Soulevé de terre',4,3,.70,'6','3-4 min','Remets-toi en place à chaque répétition. Dos neutre.'),
  ('D','Soulevé de terre jambes tendues (RDL)',3,8,.45,'6','2-3 min','Sans ceinture. Descends en reculant les hanches, dos plat.'),
  ('','Leg curl assis ou allongé',3,'10-15',None,'8','1-2 min','Contrôle la descente.'),
  ('','Gainage planche',3,'30-45 s',None,'—','1 min','Bassin aligné, respire normalement.')],
 'JOUR 3 · VOLUME HAUT DU CORPS':[
  ('S','Squat',3,6,.65,'6','3 min','Même descente à chaque répétition.'),
  ('B','Développé couché pieds levés',3,6,.58,'6','2-3 min','Pieds en l’air : le buste travaille seul, trajectoire propre.'),
  ('','Développé militaire barre debout',3,'6-8',None,'8','2 min','Fessiers serrés, ne cambre pas.'),
  ('','Rowing haltère un bras',3,'10-12',None,'8','1-2 min','Tire le coude vers la hanche.'),
  ('','Extension triceps poulie au-dessus de la tête',3,'12',None,'8','1-2 min','Coudes fixes.'),
  ('','Curl biceps au choix',2,'12',None,'8','1 min','')],
 'JOUR 4 · SÉRIE PRINCIPALE + SÉRIES ALLÉGÉES':[
  ('S','Squat · série principale',1,3,.75,'7','4 min','Monte en charge jusqu’à cette série.'),
  ('S','Squat · séries allégées',3,3,.70,'6','3 min','Même technique que la série principale.'),
  ('B','Développé couché · série principale',1,3,.77,'7','4 min','Monte en charge jusqu’à cette série.'),
  ('B','Développé couché · séries allégées',3,5,.68,'6','3 min',''),
  ('D','Soulevé de terre arrêt mi-tibia',3,3,.62,'6','3 min','Arrêt 1 s sous les genoux, puis termine le mouvement.'),
  ('','Extension lombaire au banc',3,'12',None,'8','1-2 min','Mouvement lent et contrôlé.')],
}
P3={
 'JOUR 1 · SQUAT & DÉVELOPPÉ COUCHÉ':[
  ('S','Squat',5,5,.67,'6','3-4 min','Même descente à chaque répétition.'),
  ('B','Développé couché',5,5,.67,'6-7','3 min','Fesses posées, omoplates serrées, barre touche la poitrine.'),
  ('','Tirage vertical poulie',3,'10-12',None,'8','2 min','Tire vers le haut de la poitrine, buste fixe.'),
  ('','Leg curl assis ou allongé',3,'10-15',None,'8','1-2 min','Contrôle la descente.')],
 'JOUR 2 · SBD LÉGER':[
  ('S','Squat pause 2 temps',5,3,.60,'6','3 min','Pause 2 s en bas, gainage serré, sans te relâcher.'),
  ('B','Développé couché pause 3 temps',5,3,.62,'6','3 min','Pause 3 s sur la poitrine, barre immobile.'),
  ('D','Soulevé de terre jambes tendues (RDL)',4,6,.50,'6','2-3 min','Sans ceinture. Descends en reculant les hanches, dos plat.'),
  ('','Rowing haltère un bras',3,'10-12',None,'8','1-2 min','Tire le coude vers la hanche.'),
  ('','Gainage planche',3,'30-45 s',None,'—','1 min','Bassin aligné, respire normalement.')],
 'JOUR 3 · SBD LOURD':[
  ('S','Squat · série principale',1,3,.75,'7','4 min','Monte en charge jusqu’à cette série.'),
  ('S','Squat · séries allégées',3,3,.70,'6','3 min','Même technique que la série principale.'),
  ('B','Développé couché · série principale',1,3,.77,'7','4 min','Monte en charge jusqu’à cette série.'),
  ('B','Développé couché · séries allégées',3,4,.70,'6','3 min','Même trajectoire, même pause sur la poitrine.'),
  ('D','Soulevé de terre · série principale',1,3,.72,'7','4 min','Monte en charge jusqu’à cette série. Dos neutre.'),
  ('D','Soulevé de terre · séries allégées',3,3,.67,'6','3 min','Remets-toi en place à chaque répétition.'),
  ('','Extension triceps poulie au-dessus de la tête',3,'12',None,'8','1-2 min','Coudes fixes.')],
}
WEEKS=[('SEMAINE 1','Prise en main',0.0,0),('SEMAINE 2','Progression',.025,0),('SEMAINE 3','Montée en charge',.05,0),('SEMAINE 4','Semaine la plus lourde',.075,0)]
RPE_UP={0:None,1:None,2:'+1',3:'-1'}
def rpe_for(r,wi):
    if r in('—',) or r.startswith('RIR'): return r
    if wi==2: return {'6':'7','6-7':'7-8','7':'8'}.get(r,r)
    if wi==3: return {'6':'7-8','6-7':'8','7':'8'}.get(r,r)
    return r

def build(days,label,out,logo):
    wb=openpyxl.Workbook()
    # ---- COMMENCER ICI ----
    ws=wb.active; ws.title='COMMENCER ICI'; ws.sheet_view.showGridLines=False
    ws.column_dimensions['A'].width=3; ws.column_dimensions['B'].width=26; ws.column_dimensions['C'].width=80
    for r in range(1,60):
        for c in range(1,5): ws.cell(r,c).fill=fill(WHITE)
    ws.row_dimensions[1].height=8
    im=Image(logo); im.width,im.height=150,100; ws.add_image(im,'B2')
    ws.row_dimensions[2].height=80
    ws['C2']=f'FONDATIONS\nFORCE ATHLÉTIQUE · {label}'; ws['C2'].font=Font(name=F,size=20,bold=True,color=NAVY); ws['C2'].alignment=LEFT
    rows=[
     ('TITRE','Comment ça marche'),
     ('1. Tes 1RM','Va dans l’onglet MES 1RM et entre ton maximum sur 1 répétition (1RM) au squat, au développé couché et au soulevé de terre. Tu ne le connais pas ? Entre une charge que tu fais proprement pour quelques répétitions : le fichier estime ton 1RM.'),
     ('2. Tes charges','Dans chaque semaine, la colonne CHARGE CONSEILLÉE se calcule toute seule à partir de tes 1RM et du % indiqué. Elle est arrondie à 2,5 kg.'),
     ('3. Tes séances','Remplis les cases bleues : la charge que tu as vraiment faite, le RPE ressenti et tes notes. Le reste est verrouillé.'),
     ('4. Ton bilan','L’onglet BILAN additionne ton volume de la semaine pour chaque mouvement.'),
     ('5. Et ensuite','Après la semaine 4, refais le test (ou garde tes nouvelles charges), mets à jour MES 1RM et recommence le bloc.'),
     ('TITRE','Le RPE en deux minutes'),
     ('RPE 10','Impossible de faire une répétition de plus.'),
     ('RPE 8','Il te reste 2 répétitions en réserve.'),
     ('RPE 6-7','Il te reste 3 à 4 répétitions : charge maîtrisée, technique propre.'),
     ('8','Sur les exercices de renfo : arrête-toi quand il te reste 2 répétitions.'),
     ('TITRE','Les règles du programme'),
     ('Technique d’abord','Si la technique se dégrade, baisse la charge. La charge conseillée est un repère, pas une obligation.'),
     ('Échauffement','Avant le premier exercice, monte progressivement : barre à vide, puis 3 à 4 séries de plus en plus lourdes.'),
     ('Récupération','Laisse au moins un jour entre deux séances quand c’est possible. Dors, mange, bois.'),
     ('TITRE','À lire avant de commencer'),
     ('Santé','Ce programme est général : il n’est pas fait pour ta situation précise. En cas de douleur, de blessure ou de problème de santé, demande l’avis d’un professionnel de santé avant de commencer, et adapte les charges.'),
     ('Aller plus loin','Tu stagnes ou tu bloques sur la technique ? Un suivi personnalisé peut t’aider : alexis-coaching.fr'),
    ]
    r=4
    for k,v in rows:
        if k=='TITRE':
            r+=1; ws.cell(r,2,v.upper()).font=Font(name=F,size=13,bold=True,color=WHITE)
            for c in (2,3): ws.cell(r,c).fill=fill(NAVY)
            ws.row_dimensions[r].height=24; ws.cell(r,2).alignment=LEFT; ws.merge_cells(start_row=r,start_column=2,end_row=r,end_column=3)
        else:
            ws.cell(r,2,k).font=Font(name=F,size=10,bold=True,color=NAVY); ws.cell(r,2).alignment=Alignment(vertical='top',wrap_text=True)
            ws.cell(r,3,v).font=font(10); ws.cell(r,3).alignment=Alignment(vertical='top',wrap_text=True)
            ws.row_dimensions[r].height=15*max(1,-(-len(v)//95))+4
            for c in (2,3): ws.cell(r,c).border=Border(bottom=thin)
        r+=1
    ws.protection.sheet=True

    # ---- MES 1RM ----
    mx=wb.create_sheet('MES 1RM'); mx.sheet_view.showGridLines=False
    for col,w in zip('ABCDEFG',[3,26,16,16,16,18,40]): mx.column_dimensions[col].width=w
    mx['B2']='MES 1RM'; mx['B2'].font=Font(name=F,size=20,bold=True,color=NAVY)
    mx['B3']='Remplis les cases bleues. Si tu connais ton 1RM, la colonne C suffit.'; mx['B3'].font=font(10,c=MUTED,i=True)
    hdr=['MOUVEMENT','MON 1RM (kg)','OU : CHARGE (kg)','× RÉPÉTITIONS','1RM UTILISÉ (kg)','']
    for i,h in enumerate(hdr):
        c=mx.cell(5,2+i,h); c.font=Font(name=F,size=9,bold=True,color=WHITE); c.fill=fill(NAVY); c.alignment=CENTER
    mx.row_dimensions[5].height=30
    lifts=[('S','Squat'),('B','Développé couché'),('D','Soulevé de terre')]
    for i,(code,name) in enumerate(lifts):
        rr=6+i; mx.row_dimensions[rr].height=26
        mx.cell(rr,2,name).font=Font(name=F,size=11,bold=True,color=NAVY)
        for col in (3,4,5):
            c=mx.cell(rr,col); c.fill=fill(INPUT); c.protection=openpyxl.styles.Protection(locked=False); c.alignment=CENTER; c.font=font(11,True); c.border=B
        mx.cell(rr,5).number_format='0'
        f=mx.cell(rr,6,f'=IF(ISNUMBER(C{rr}),C{rr},IF(AND(ISNUMBER(D{rr}),ISNUMBER(E{rr}),E{rr}>=1,E{rr}<=10),ROUND(D{rr}*(1+E{rr}/30)/2.5,0)*2.5,""))')
        f.font=Font(name=F,size=13,bold=True,color=WHITE); f.fill=fill(ACC); f.alignment=CENTER; f.number_format='0.0'; f.border=B
        mx.cell(rr,8,code).font=font(8,c=WHITE)
    mx['B10']='Estimation : charge × (1 + répétitions ÷ 30), valable de 1 à 10 répétitions. C’est une estimation, pas un test : reste prudent.'
    mx['B10'].font=font(9,c=MUTED,i=True); mx.merge_cells('B10:G10'); mx['B10'].alignment=LEFT; mx.row_dimensions[10].height=28
    dv=DataValidation(type='decimal',operator='between',formula1='0',formula2='500',allow_blank=True); mx.add_data_validation(dv); dv.add('C6:D8')
    dv2=DataValidation(type='whole',operator='between',formula1='1',formula2='10',allow_blank=True,error='Entre 1 et 10 répétitions.',showErrorMessage=True); mx.add_data_validation(dv2); dv2.add('E6:E8')
    mx.protection.sheet=True
    REF={'S':"'MES 1RM'!$F$6",'B':"'MES 1RM'!$F$7",'D':"'MES 1RM'!$F$8"}

    # ---- SEMAINES ----
    cols=['','TYPE','EXERCICE','SÉRIES','RÉPS','% 1RM','CHARGE CONSEILLÉE','RPE CIBLE','REPOS','CONSIGNES','CHARGE FAITE (kg)','RPE RESSENTI','MES NOTES']
    widths=[2,6,34,8,8,8,13,9,9,40,13,10,32]
    tonnage_cells={}
    for wi,(wname,wsub,inc,dset) in enumerate(WEEKS):
        s=wb.create_sheet(wname); s.sheet_view.showGridLines=False; s.freeze_panes='C5'
        for i,w in enumerate(widths): s.column_dimensions[openpyxl.utils.get_column_letter(i+1)].width=w
        s['B2']=f'{wname} · {wsub.upper()}'; s['B2'].font=Font(name=F,size=18,bold=True,color=NAVY)
        s['B3']=f'Programme débutant force athlétique · {label}   ·   Cases bleues = à remplir'; s['B3'].font=font(9,c=MUTED,i=True)
        r=5; tc={'S':[],'B':[],'D':[]}
        for day,exs in days.items():
            s.cell(r,2,day); 
            for c in range(2,14): s.cell(r,c).fill=fill(NAVY)
            s.cell(r,2).font=Font(name=F,size=12,bold=True,color=WHITE); s.row_dimensions[r].height=24
            s.cell(r,11,'Date :').font=font(9,c=ACC2); s.cell(r,11).alignment=Alignment(horizontal='right',vertical='center')
            d=s.cell(r,12); d.fill=fill(INPUT); d.protection=openpyxl.styles.Protection(locked=False); d.font=font(9); d.number_format='DD/MM'
            r+=1
            for i,h in enumerate(cols[1:],start=2):
                c=s.cell(r,i,h); c.font=Font(name=F,size=8,bold=True,color=NAVY); c.fill=fill('D6E4F7'); c.alignment=CENTER; c.border=B
            s.row_dimensions[r].height=26; r+=1
            for k,(typ,ex,sets,reps,pct,rpe,rest,tip) in enumerate(exs):
                n_sets=max(1,sets+dset) if (wi==3) else sets
                if wi==3 and sets==1: n_sets=1
                vals=[typ,ex,n_sets,reps,(round(pct+inc,3) if pct else None),None,rpe_for(rpe,wi),rest,tip]
                bg=PALE if k%2==0 else WHITE
                for i,v in enumerate(vals,start=2):
                    c=s.cell(r,i,v); c.fill=fill(bg); c.border=B; c.font=font(9); c.alignment=CENTER
                s.cell(r,3).font=Font(name=F,size=10,bold=True,color=NAVY); s.cell(r,3).alignment=LEFT
                s.cell(r,10).alignment=LEFT; s.cell(r,10).font=font(8,c=MUTED)
                s.cell(r,2).font=font(8,True,ACC)
                if pct:
                    s.cell(r,6).number_format='0%'
                    g=s.cell(r,7,f'=IF(ISNUMBER({REF[typ]}),ROUND({REF[typ]}*F{r}/2.5,0)*2.5,"")')
                    g.number_format='0.0" kg"'; g.font=Font(name=F,size=11,bold=True,color=NAVY); g.fill=fill('C9DCF7')
                    tc[typ].append(r)
                else:
                    s.cell(r,6,'—'); s.cell(r,7,'au ressenti').font=font(8,c=MUTED,i=True)
                for col in (11,12,13):
                    c=s.cell(r,col); c.fill=fill(INPUT); c.protection=openpyxl.styles.Protection(locked=False); c.border=B; c.font=font(10); c.alignment=CENTER
                s.cell(r,13).alignment=LEFT
                s.row_dimensions[r].height=30; r+=1
            r+=1
        # récap tonnage
        r+=1
        s.cell(r,3,'VOLUME DE LA SEMAINE (séries × réps × charge faite)').font=Font(name=F,size=11,bold=True,color=NAVY); r+=1
        tonnage_cells[wname]={}
        for code,name in lifts:
            rows_=tc[code]
            formula='='+('+'.join(f'IF(ISNUMBER(K{x}),D{x}*E{x}*K{x},0)' for x in rows_) if rows_ else '0')
            s.cell(r,3,name).font=font(10,True); s.cell(r,3).border=B
            c=s.cell(r,7,formula); c.number_format='# ##0" kg"'; c.font=font(10,True,NAVY); c.border=B; c.fill=fill('C9DCF7')
            tonnage_cells[wname][code]=f"'{wname}'!G{r}"; r+=1
        s.protection.sheet=True
        s.print_options.horizontalCentered=True; s.page_setup.orientation='landscape'
        s.sheet_properties.pageSetUpPr.fitToPage=True; s.page_setup.fitToWidth=1; s.page_setup.fitToHeight=0

    # ---- BILAN ----
    b=wb.create_sheet('BILAN'); b.sheet_view.showGridLines=False
    for col,w in zip('ABCDE',[3,22,16,20,18]): b.column_dimensions[col].width=w
    b['B2']='BILAN DU BLOC'; b['B2'].font=Font(name=F,size=20,bold=True,color=NAVY)
    b['B3']='Se remplit tout seul à partir des charges que tu notes.'; b['B3'].font=font(9,c=MUTED,i=True)
    for i,h in enumerate(['SEMAINE','SQUAT (kg)','DÉVELOPPÉ COUCHÉ (kg)','SOULEVÉ DE TERRE (kg)']):
        c=b.cell(5,2+i,h); c.font=Font(name=F,size=9,bold=True,color=WHITE); c.fill=fill(NAVY); c.alignment=CENTER
    b.row_dimensions[5].height=28
    for j,(wname,*_) in enumerate(WEEKS):
        rr=6+j; b.cell(rr,2,wname).font=font(10,True,NAVY); b.cell(rr,2).border=B
        for i,code in enumerate('SBD'):
            c=b.cell(rr,3+i,'='+tonnage_cells[wname][code]); c.number_format='# ##0'; c.alignment=CENTER; c.border=B; c.font=font(10)
    ch=BarChart(); ch.type='col'; ch.title='Volume par semaine'; ch.y_axis.title='kg'; ch.height=8; ch.width=18
    data=Reference(b,min_col=3,max_col=5,min_row=5,max_row=9); cats=Reference(b,min_col=2,min_row=6,max_row=9)
    ch.add_data(data,titles_from_data=True); ch.set_categories(cats)
    for sr,col in zip(ch.series,[NAVY,ACC,ACC2]):
        sr.graphicalProperties.solidFill=col; sr.graphicalProperties.line.solidFill=col
    b.add_chart(ch,'B12'); b.protection.sheet=True
    for w in wb.worksheets:
        w.sheet_properties.pageSetUpPr.fitToPage=True; w.page_setup.fitToWidth=1; w.page_setup.fitToHeight=0
    for w in wb.worksheets: w.sheet_properties.tabColor=NAVY if w.title in('COMMENCER ICI','MES 1RM','BILAN') else ACC
    wb.save(out)

logo=sys.argv[1]; od=sys.argv[2]
build(P4,'4 JOURS',od+'/Fondations-force-athletique-4-jours.xlsx',logo)
build(P3,'3 JOURS',od+'/Fondations-force-athletique-3-jours.xlsx',logo)
print('ok')
