import sys, importlib.util, openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side, Protection
from openpyxl.drawing.image import Image
from openpyxl.chart import BarChart, LineChart, Reference
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.utils import get_column_letter as L
spec=importlib.util.spec_from_file_location('bp',sys.argv[3]); bp=importlib.util.module_from_spec(spec)
src=open(sys.argv[3]).read().split('# ---------- PROGRAMMES ----------')[1].split('def build(')[0]
exec(src,bp.__dict__)
P3,P4,WEEKS,rpe_for=bp.P3,bp.P4,bp.WEEKS,bp.rpe_for

BLACK='111111'; DEEP='1E3350'; BLUE='4772A3'; LIGHT='C9DAF8'; PALE='EEF3FC'; GREY='F3F3F3'; MUTED='6B7A90'; WHITE='FFFFFF'; CYAN='2BB3E3'
F='Arial'
def fl(c): return PatternFill('solid',fgColor=c)
def fn(sz=10,b=False,c='1A2333',i=False): return Font(name=F,size=sz,bold=b,color=c,italic=i)
hair=Side(style='thin',color='D5DEEB'); blue=Side(style='medium',color=BLUE)
BOX=Border(left=hair,right=hair,top=hair,bottom=hair)
INBOX=Border(left=Side(style='thin',color=BLUE),right=Side(style='thin',color=BLUE),top=Side(style='thin',color=BLUE),bottom=Side(style='thin',color=BLUE))
C=Alignment(horizontal='center',vertical='center',wrap_text=True)
LFT=Alignment(horizontal='left',vertical='center',wrap_text=True,indent=1)
UNL=Protection(locked=False)
def paint(ws,r1,r2,c1,c2,color):
    for r in range(r1,r2+1):
        for c in range(c1,c2+1): ws.cell(r,c).fill=fl(color)

# colonnes semaine
COLS=[('',2),('JOUR',13),('EXERCICE',30),('SÉRIES',8),('RÉPS',8),('% 1RM',8),('CHARGE\nCONSEILLÉE',12),('RPE\nCIBLE',8),('REPOS',9),('CONSIGNE',34),('CHARGE\nFAITE (kg)',12),('RPE\nFAIT',8),('OBSERVATIONS',30),('',2),('t',1)]
NC=13
REPS_NUM='IFERROR(VALUE(LEFT(E{r},FIND("-",E{r}&"-")-1)),0)'


# ===== ADN alexis-coaching.fr =====
NAVY='0B1628'; SURF='12223A'; SURF2='16305A'; ROW2='0F1E35'; ACC='5B9BEF'; ACC2='8EC0FF'; MUT='A9B6C9'; LINE='22385A'; INK='FFFFFF'
FB='Manrope'; FD='Big Shoulders Display'
INKD='0B1628'; MUTD='5F6E85'; ACCD='2F6BC4'; PALE2='F4F7FC'; LIGHT2='E3ECFA'
FILLMAP={BLACK:NAVY,BLUE:ACC,LIGHT:LIGHT2,PALE:PALE2,GREY:PALE2,WHITE:WHITE}
def _rgb(c):
    try: return c.rgb[-6:].upper() if c is not None and isinstance(c.rgb,str) else None
    except Exception: return None
def _side(sd):
    if sd is None or sd.style is None: return sd
    col=_rgb(sd.color); col={BLUE:ACC}.get(col,col)
    return Side(style=sd.style,color=col)
def apply_theme(wb):
    # version claire : fond blanc, bleu nuit pour les bandeaux, accent bleu par touches
    for ws in wb.worksheets:
        mr=ws.max_row+40
        for r in range(1,mr+1):
            for c in range(1,27):
                cell=ws.cell(r,c)
                old=_rgb(cell.fill.fgColor) if cell.fill and cell.fill.fill_type=='solid' else None
                new=FILLMAP.get(old,WHITE)
                if cell.protection.locked is False and hasattr(cell,'value'): new=WHITE
                cell.fill=fl(new)
                f=cell.font; fc=_rgb(f.color) if f and f.color is not None else None
                if new==NAVY: col=ACC2 if fc in(BLUE,CYAN) else WHITE
                elif new==ACC: col=NAVY
                else: col={BLUE:ACCD,MUTED:MUTD,CYAN:ACCD,WHITE:INKD}.get(fc,INKD)
                sz=f.sz or 10; big=f.b and sz>=14
                cell.font=Font(name=FD if big else FB,size=round(sz*1.3) if big else sz,bold=f.b,italic=f.i,color=col)
                b=cell.border
                if b and any(s is not None and s.style for s in (b.left,b.right,b.top,b.bottom)):
                    cell.border=Border(left=_side(b.left),right=_side(b.right),top=_side(b.top),bottom=_side(b.bottom))
        ws.sheet_properties.tabColor=NAVY if ws.title in('COMMENCER ICI','MES 1RM','BILAN') else ACC
        import os; TH=os.environ.get('THEME','C')
        if TH in('B','C'):
            # bandeau d'en-tête bleu nuit, comme le site
            for r in range(1,5):
                for c in range(1,NC+2):
                    cell=ws.cell(r,c); cell.fill=fl(NAVY); f=cell.font
                    cell.font=Font(name=f.name,size=f.sz,bold=f.b,italic=f.i,color=MUT if r==3 else WHITE)
            ta,tb=(5,6) if ws.title=='MES 1RM' else (10,13)
            for c in range(ta,tb+1): ws.cell(2,c).fill=fl(SURF2); ws.cell(3,c).fill=fl(SURF2)
            if ws.title.startswith('SEMAINE'):
                for r in (6,7):
                    for c in range(2,NC+1):
                        cell=ws.cell(r,c); cell.fill=fl(SURF); f=cell.font
                        cell.font=Font(name=f.name,size=f.sz,bold=f.b,italic=f.i,color=ACC2 if r==6 else WHITE)
        if TH=='C':
            for r in range(1,ws.max_row+41):
                for c in range(1,27):
                    cell=ws.cell(r,c)
                    if _rgb(cell.fill.fgColor)==WHITE and cell.value is None and cell.protection.locked is not False and not (cell.border and cell.border.left and cell.border.left.style): cell.fill=fl(NAVY)

def header(ws,title,sub,logo,tc=(10,13)):
    a,b=tc
    for r in range(1,5): paint(ws,r,r,1,NC+1,WHITE)
    ws.row_dimensions[1].height=10; ws.row_dimensions[2].height=42; ws.row_dimensions[3].height=26; ws.row_dimensions[4].height=10
    im=Image(logo); im.width,im.height=110,52; ws.add_image(im,'B2')
    ws.merge_cells(start_row=2,start_column=3,end_row=2,end_column=a-1); ws['C2']='FONDATIONS · FORCE ATHLÉTIQUE'; ws.column_dimensions['B'].width=max(ws.column_dimensions['B'].width or 0,17); ws['C2'].font=Font(name=F,size=13,bold=True,color=BLACK); ws['C2'].alignment=Alignment(vertical='bottom',indent=1)
    ws.merge_cells(start_row=3,start_column=3,end_row=3,end_column=a-1); ws['C3']=sub; ws['C3'].font=fn(10,c=MUTED); ws['C3'].alignment=Alignment(vertical='top',indent=1)
    ws.merge_cells(start_row=2,start_column=a,end_row=3,end_column=b); ws.cell(2,a,title).font=Font(name=F,size=22,bold=True,color=WHITE); ws.cell(2,a).alignment=C
    paint(ws,2,3,a,b,BLACK)
    for c in range(2,b+1): ws.cell(4,c).border=Border(bottom=Side(style='thick',color=BLUE))

def build(days,label,out,logo):
    wb=openpyxl.Workbook()
    # ===== COMMENCER ICI =====
    ws=wb.active; ws.title='COMMENCER ICI'; ws.sheet_view.showGridLines=False
    for c,w in zip('ABCDEFGHIJKLM',[2,13,30,8,8,8,12,8,9,34,12,8,30]): ws.column_dimensions[c].width=w
    header(ws,'BIENVENUE',f'Version {label.lower()} · 4 semaines · paiement unique, accès illimité',logo)
    blocks=[
     ('COMMENT ÇA MARCHE',[
      ('1','Entre tes 1RM','Onglet MES 1RM : entre ton 1RM au squat, au développé couché et au soulevé de terre. Tout le reste se calcule tout seul.'),
      ('2','Lis ta séance','Chaque exercice a un % de ton 1RM. La CHARGE CONSEILLÉE se calcule toute seule, arrondie à 2,5 kg.'),
      ('3','Note ce que tu fais','Remplis les cases blanches à bord bleu : charge faite, RPE fait, observations. Le reste est verrouillé.'),
      ('4','Suis ta progression','Chaque séance et chaque semaine affichent ton tonnage, au total et par mouvement. L’onglet BILAN montre l’évolution sur le bloc.'),
      ('5','Recommence','Après la semaine 4, tu repars en semaine 1. Dans MES 1RM, passe le NUMÉRO DU BLOC à 2, puis 3… : chaque charge conseillée prend +2,5 kg par bloc.')]),
     ('APRÈS LA SEMAINE 4',[
      ('4','Toujours 4 semaines','Le programme est construit pour 4 semaines : l’intensité monte de la semaine 1 à la semaine 4. Ne continue jamais sur une semaine 5 ou 6.'),
      ('↺','Pourquoi repartir en semaine 1','Quand on débute, on ne connaît pas encore bien sa récupération ni le volume qu’on encaisse. Repartir en semaine 1 te laisse récupérer avant de remonter.'),
      ('+2,5','Un point de départ plus haut','À chaque nouveau bloc, tu repars un peu plus lourd. Exemple : squat 4×4 à 100 kg au bloc 1, 102,5 kg au bloc 2, 105 kg au bloc 3. C’est comme ça que tu progresses de bloc en bloc.')]),
     ('LE RPE EN BREF',[
      ('10','Échec','Impossible de faire une répétition de plus.'),
      ('8','Difficile','Il te reste 2 répétitions en réserve.'),
      ('6-7','Maîtrisé','Il te reste 3 à 4 répétitions. Technique propre.'),
      ('RIR 2','Renfo','Arrête la série quand il te reste 2 répétitions.')]),
     ('TONNAGE',[
      ('kg','C’est quoi ?','Séries × répétitions × charge. C’est ton volume de travail : il augmente de semaine en semaine, c’est la surcharge progressive.'),
      ('S·B·D','Par mouvement','À la fin de chaque séance : ton tonnage au squat, au développé couché et au soulevé de terre (variantes comprises). Les exercices de renfo ne comptent pas : on suit leur charge, pas leur tonnage.'),
      ('prévu','Tonnage prévu','Calculé avec tes charges conseillées.'),
      ('réalisé','Tonnage réalisé','Calculé avec les charges que tu notes.')]),
     ('À LIRE AVANT DE COMMENCER',[
      ('!','Santé','Ce programme est général : il n’est pas fait pour ta situation précise. En cas de douleur, de blessure ou de problème de santé, demande l’avis d’un professionnel de santé avant de commencer, et adapte les charges.'),
      ('→','Aller plus loin','Tu stagnes ou tu bloques sur la technique ? Un suivi personnalisé peut t’aider : alexis-coaching.fr')]),
    ]
    r=6
    for t,items in blocks:
        ws.merge_cells(start_row=r,start_column=2,end_row=r,end_column=13); ws.cell(r,2,t).font=fn(12,True,WHITE); ws.cell(r,2).alignment=LFT
        paint(ws,r,r,2,13,BLACK); ws.row_dimensions[r].height=26; r+=1
        for k,(a,b,c) in enumerate(items):
            ws.cell(r,2,a).font=Font(name=F,size=14,bold=True,color=BLUE); ws.cell(r,2).alignment=C
            ws.cell(r,3,b).font=fn(10,True,BLACK); ws.cell(r,3).alignment=LFT
            ws.merge_cells(start_row=r,start_column=4,end_row=r,end_column=13); ws.cell(r,4,c).font=fn(10); ws.cell(r,4).alignment=LFT
            paint(ws,r,r,2,13,PALE if k%2==0 else WHITE); ws.row_dimensions[r].height=max(26,14*(-(-len(c)//120))+12); r+=1
        r+=1
    ws.protection.sheet=True

    # ===== MES 1RM =====
    mx=wb.create_sheet('MES 1RM'); mx.sheet_view.showGridLines=False
    for c,w in zip('ABCDEFG',[2,17,24,24,13,13,2]): mx.column_dimensions[c].width=w
    header(mx,'MES 1RM','Cases à bord bleu = à remplir',logo,tc=(5,6))
    mx.row_dimensions[5].height=14; mx.row_dimensions[12].height=18
    def cardhead(r,txt,sub):
        mx.row_dimensions[r].height=28; paint(mx,r,r,2,6,BLUE)
        mx.merge_cells(start_row=r,start_column=2,end_row=r,end_column=4); mx.cell(r,2,txt).font=fn(11,True,BLACK); mx.cell(r,2).alignment=LFT
        mx.merge_cells(start_row=r,start_column=5,end_row=r,end_column=6); mx.cell(r,5,sub).font=fn(9,c=BLACK); mx.cell(r,5).alignment=Alignment(horizontal='right',vertical='center',indent=1)
    def line(r,label,val,big=True):
        mx.row_dimensions[r].height=40
        mx.merge_cells(start_row=r,start_column=2,end_row=r,end_column=3); mx.cell(r,2,label).font=fn(12,True,BLACK); mx.cell(r,2).alignment=LFT; paint(mx,r,r,2,3,PALE)
        for cc in (2,3): mx.cell(r,cc).border=Border(bottom=Side(style='thin',color=LIGHT))
        mx.merge_cells(start_row=r,start_column=4,end_row=r,end_column=6)
        for cc in range(4,7): mx.cell(r,cc).border=INBOX; mx.cell(r,cc).protection=UNL
        c=mx.cell(r,4,val); c.font=fn(18,True,BLUE); c.alignment=C
        return c
    def note(r,txt,h):
        mx.row_dimensions[r].height=h; paint(mx,r,r,2,6,PALE)
        mx.merge_cells(start_row=r,start_column=2,end_row=r,end_column=6); mx.cell(r,2,txt).font=fn(9,c=MUTED,i=True); mx.cell(r,2).alignment=LFT
    cardhead(6,'TES 1RM','en kg · 1 répétition')
    for i,name in enumerate(['SQUAT','DÉVELOPPÉ COUCHÉ','SOULEVÉ DE TERRE']): line(7+i,name,None).number_format='0.0" kg"'
    mx.row_dimensions[10].height=34
    mx.merge_cells('B10:C10'); mx['B10']='TOTAL S·B·D'; mx['B10'].font=fn(11,True,BLACK); mx['B10'].alignment=LFT
    mx.merge_cells('D10:F10'); mx['D10']='=IF(COUNT(D7:D9)=3,SUM(D7:D9),"—")'; mx['D10'].font=fn(14,True,BLUE); mx['D10'].alignment=C; mx['D10'].number_format='0.0" kg"'
    paint(mx,10,10,2,6,LIGHT)
    note(11,'Ton 1RM = la charge maximale que tu soulèves sur 1 répétition, avec une technique propre.',30)
    cardhead(13,'BLOC EN COURS','+2,5 kg par bloc')
    bc=line(14,'NUMÉRO DU BLOC',1); bc.font=fn(18,True,BLACK)
    note(15,'1 la première fois, puis 2, 3… Garde les mêmes 1RM : change seulement le numéro du bloc. Chaque bloc ajoute 2,5 kg aux charges conseillées.',40)
    dvb=DataValidation(type='whole',operator='between',formula1='1',formula2='50',allow_blank=False,showErrorMessage=True,error='Entre un numéro de bloc (1, 2, 3…).'); mx.add_data_validation(dvb); dvb.add('D14')
    mx.protection.sheet=True
    BLOC="'MES 1RM'!$D$14"
    REF={'S':"'MES 1RM'!$D$7",'B':"'MES 1RM'!$D$8",'D':"'MES 1RM'!$D$9"}

    week_tot={}
    for wi,(wname,wsub,inc,dset) in enumerate(WEEKS):
        s=wb.create_sheet(wname); s.sheet_view.showGridLines=False
        for i,(h,w) in enumerate(COLS,start=1): s.column_dimensions[L(i)].width=w
        s.column_dimensions['O'].hidden=True
        header(s,wname,f'Version {label.lower()}',logo)
        # tableau de bord semaine (rempli après)
        dash=6; s.row_dimensions[dash].height=18; s.row_dimensions[dash+1].height=34; s.row_dimensions[dash+2].height=10
        r=dash+3; day_rows=[]
        for day,exs in days.items():
            jour,theme=day.split(' · ')
            s.row_dimensions[r].height=30
            for i,(h,_) in enumerate(COLS[2:NC],start=3):
                c=s.cell(r,i,h); c.font=fn(8,True,WHITE); c.alignment=C
            paint(s,r,r,3,NC,BLACK)
            d=s.cell(r,NC,'OBSERVATIONS'); 
            hr=r; r+=1; first=r; rows=[]
            for k,(typ,ex,sets,reps,pct,rpe,rest,tip) in enumerate(exs):
                n=sets+1 if (wi>=1 and typ and sets>=3) else sets
                p=round(pct+inc,3) if pct else None
                vals={3:ex,4:n,5:reps,6:p if p else '—',8:rpe_for(rpe,wi),9:rest,10:tip}
                bg=LIGHT if typ else GREY
                for col in range(3,NC+1):
                    c=s.cell(r,col); c.border=BOX; c.alignment=C; c.font=fn(9)
                    if col<=10: c.fill=fl(bg if col in(3,6,7) else (PALE if typ else WHITE))
                for col,v in vals.items(): s.cell(r,col,v)
                s.cell(r,3).font=fn(10,True,BLACK); s.cell(r,3).alignment=LFT
                s.cell(r,10).font=fn(8,c=MUTED,i=True); s.cell(r,10).alignment=LFT
                if p:
                    s.cell(r,6).number_format='0%'; s.cell(r,6).font=fn(10,True,BLUE)
                    g=s.cell(r,7,f'=IF(ISNUMBER({REF[typ]}),ROUND({REF[typ]}*F{r}/2.5,0)*2.5+(MAX(1,{BLOC})-1)*2.5,"")'); g.number_format='0.0" kg"'; g.font=fn(11,True,BLACK)
                else:
                    s.cell(r,7,'au ressenti').font=fn(8,c=MUTED,i=True)
                for col in (11,12,13):
                    c=s.cell(r,col); c.protection=UNL; c.border=INBOX; c.fill=fl(WHITE); c.font=fn(10,True)
                s.cell(r,13).alignment=LFT; s.cell(r,13).font=fn(9)
                # col O (cachée) : réps prévues de la ligne
                s.cell(r,15,f'=D{r}*{REPS_NUM.format(r=r)}' if 'Gainage' not in ex else 0)
                s.row_dimensions[r].height=32; rows.append((r,typ,ex)); r+=1
            last=r-1
            s.merge_cells(start_row=hr,start_column=2,end_row=last,end_column=2)
            jc=s.cell(hr,2,f'{jour}\n\n{theme}'); jc.font=fn(11,True,WHITE); jc.alignment=C; paint(s,hr,last,2,2,BLACK)
            # pied de séance
            main=[x for x,t,_ in rows if t]
            prev='+'.join(f'IF(ISNUMBER(G{x}),D{x}*E{x}*G{x},0)' for x in main) or '0'
            real='+'.join(f'IF(ISNUMBER(K{x}),O{x}*K{x},0)' for x in main) or '0'
            # récap tonnage par mouvement (variantes comprises)
            for lt,lname in (('S','SQUAT'),('B','DÉVELOPPÉ COUCHÉ'),('D','SOULEVÉ DE TERRE')):
                lr=[x for x,t,_ in rows if t==lt]
                if not lr: continue
                s.row_dimensions[r].height=22
                s.merge_cells(start_row=r,start_column=2,end_row=r,end_column=4); s.cell(r,2,f'TONNAGE {lname}').font=fn(9,True,BLACK); s.cell(r,2).alignment=LFT
                s.merge_cells(start_row=r,start_column=5,end_row=r,end_column=6); s.cell(r,5,'Prévu').alignment=Alignment(horizontal='right',vertical='center')
                s.cell(r,7,'='+'+'.join(f'IF(ISNUMBER(G{x}),D{x}*E{x}*G{x},0)' for x in lr)).number_format='# ##0" kg"'
                s.merge_cells(start_row=r,start_column=8,end_row=r,end_column=10); s.cell(r,8,'Réalisé').alignment=Alignment(horizontal='right',vertical='center')
                s.cell(r,11,'='+'+'.join(f'IF(ISNUMBER(K{x}),O{x}*K{x},0)' for x in lr)).number_format='# ##0" kg"'
                for col in range(2,NC+1):
                    c=s.cell(r,col); c.fill=fl(LIGHT); c.border=BOX
                    if col!=2: c.font=fn(10 if col in(7,11) else 8,col in(7,11),BLACK if col in(7,11) else MUTED)
                    if col in(7,11): c.alignment=C
                r+=1
            s.row_dimensions[r].height=24
            s.merge_cells(start_row=r,start_column=2,end_row=r,end_column=4); s.cell(r,2,'TOTAL SÉANCE').font=fn(9,True,WHITE); s.cell(r,2).alignment=LFT
            s.merge_cells(start_row=r,start_column=5,end_row=r,end_column=6); s.cell(r,5,'Tonnage prévu').alignment=Alignment(horizontal='right',vertical='center')
            s.cell(r,7,'='+prev).number_format='# ##0" kg"'
            s.merge_cells(start_row=r,start_column=8,end_row=r,end_column=10); s.cell(r,8,'Tonnage réalisé').alignment=Alignment(horizontal='right',vertical='center')
            s.cell(r,11,'='+real).number_format='# ##0" kg"'
            for col in range(2,NC+1):
                c=s.cell(r,col); c.fill=fl(BLUE); 
                if col!=2: c.font=fn(10 if col in(7,11) else 8,col in(7,11),WHITE)
                if col in(7,11): c.alignment=C
            day_rows.append(r); r+=2
        # tableau de bord
        tp='+'.join(f'G{x}' for x in day_rows); tr='+'.join(f'K{x}' for x in day_rows)
        cards=[(2,4,'TONNAGE PRÉVU',f'={tp}','# ##0" kg"'),(5,9,'TONNAGE RÉALISÉ',f'={tr}','# ##0" kg"'),
               (10,10,'VS SEMAINE PRÉCÉDENTE',None,'+0%;-0%;0%'),(11,13,'SÉANCES',f'{len(days)} séances',None)]
        week_tot[wname]=(f"'{wname}'!B{dash+1}",f"'{wname}'!E{dash+1}")
        for a,b,t,v,nf in cards:
            if a!=b:
                s.merge_cells(start_row=dash,start_column=a,end_row=dash,end_column=b); s.merge_cells(start_row=dash+1,start_column=a,end_row=dash+1,end_column=b)
            s.cell(dash,a,t).font=fn(8,True,MUTED); s.cell(dash,a).alignment=C
            if t=='VS SEMAINE PRÉCÉDENTE':
                v=f"=IFERROR(B{dash+1}/'{WEEKS[wi-1][0]}'!B{dash+1}-1,\"—\")" if wi else '—'
            c=s.cell(dash+1,a,v); c.font=fn(16 if t!='SÉANCES' else 10,True,BLACK if t!='SÉANCES' else MUTED); c.alignment=C
            if nf: c.number_format=nf
            paint(s,dash,dash+1,a,b,PALE)
        s.freeze_panes=f'C{dash+3}'
        s.protection.sheet=True
        s.page_setup.orientation='landscape'; s.sheet_properties.pageSetUpPr.fitToPage=True; s.page_setup.fitToWidth=1; s.page_setup.fitToHeight=0

    # ===== BILAN =====
    b=wb.create_sheet('BILAN'); b.sheet_view.showGridLines=False
    for c,w in zip('ABCDEFGHIJKLM',[2,13,30,8,8,8,12,8,9,34,12,8,30]): b.column_dimensions[c].width=w
    header(b,'BILAN','Se remplit tout seul · tonnage = séries × réps × charge',logo)
    hd=[(2,3,'SEMAINE'),(4,6,'TONNAGE PRÉVU (kg)'),(7,10,'TONNAGE RÉALISÉ (kg)')]
    for a,c2,h in hd:
        if a!=c2: b.merge_cells(start_row=6,start_column=a,end_row=6,end_column=c2)
        b.cell(6,a,h).font=fn(9,True,WHITE); b.cell(6,a).alignment=C
    paint(b,6,6,2,10,BLACK); b.row_dimensions[6].height=28
    for j,(wname,wsub,*_) in enumerate(WEEKS):
        rr=7+j; b.row_dimensions[rr].height=26
        tp,tr=week_tot[wname]
        for a,c2,v,nf in [(2,3,wname,None),(4,6,'='+tp,'# ##0'),(7,10,'='+tr,'# ##0')]:
            if a!=c2: b.merge_cells(start_row=rr,start_column=a,end_row=rr,end_column=c2)
            c=b.cell(rr,a,v); c.alignment=C if a>2 else LFT; c.font=fn(10,a==2,BLACK)
            if nf: c.number_format=nf
            paint(b,rr,rr,a,c2,PALE if j%2==0 else WHITE)
    # données graphiques (colonnes cachées O:Q)
    b['O6'],b['P6'],b['Q6']='Semaine','Tonnage prévu','Tonnage réalisé'
    for j,(wname,*_) in enumerate(WEEKS):
        b.cell(7+j,15,f'S{j+1}'); b.cell(7+j,16,f'=D{7+j}'); b.cell(7+j,17,f'=G{7+j}')
    for c in 'OPQ': b.column_dimensions[c].hidden=True
    ch=BarChart(); ch.type='col'; ch.title='Tonnage par semaine (kg)'; ch.height=8; ch.width=22; ch.legend.position='b'
    ch.add_data(Reference(b,min_col=16,max_col=17,min_row=6,max_row=10),titles_from_data=True); ch.set_categories(Reference(b,min_col=15,min_row=7,max_row=10))
    for sr,col in zip(ch.series,['5B9BEF','8EC0FF']): sr.graphicalProperties.solidFill=col; sr.graphicalProperties.line.solidFill=col
    from openpyxl.chart.shapes import GraphicalProperties
    from openpyxl.chart.text import RichText
    from openpyxl.drawing.text import Paragraph,ParagraphProperties,CharacterProperties,Font as DF
    def tx(col,sz=900,bold=False): return RichText(p=[Paragraph(pPr=ParagraphProperties(defRPr=CharacterProperties(sz=sz,b=bold,solidFill=col,latin=DF(typeface='Manrope'))),endParaRPr=CharacterProperties())])
    ch.graphical_properties=GraphicalProperties(solidFill='12223A'); ch.graphical_properties.line.solidFill='22385A'
    ch.plot_area.graphicalProperties=GraphicalProperties(solidFill='12223A')
    for ax in (ch.x_axis,ch.y_axis): ax.txPr=tx('A9B6C9'); ax.delete=False
    ch.y_axis.majorGridlines.spPr=GraphicalProperties(); ch.y_axis.majorGridlines.spPr.line.solidFill='22385A'
    ch.legend.txPr=tx('FFFFFF')
    ch.title.tx.rich.p[0].pPr=ParagraphProperties(defRPr=CharacterProperties(sz=1400,b=True,solidFill='FFFFFF',latin=DF(typeface='Manrope')))
    ch.visible_cells_only=False; b.add_chart(ch,'B13')
    b.protection.sheet=True
    for w in wb.worksheets:
        w.page_setup.orientation='landscape'; w.sheet_properties.pageSetUpPr.fitToPage=True; w.page_setup.fitToWidth=1; w.page_setup.fitToHeight=0
        w.sheet_properties.tabColor=BLACK if w.title in('COMMENCER ICI','MES 1RM','BILAN') else BLUE
    apply_theme(wb)
    wb.save(out)

logo,od=sys.argv[1],sys.argv[2]
build(P4,'4 jours',od+'/Fondations-force-athletique-4-jours.xlsx',logo)
build(P3,'3 jours',od+'/Fondations-force-athletique-3-jours.xlsx',logo)
print('ok')
