# DA — vidéos coach fitness (à appliquer à toutes les vidéos)

Objectif : vues → abonnés → prospects → clients. Rétention max.
Modèle de référence : `balance/montage/` (copier le projet, changer rush + textes + timings).

## Mise en page (1080x1920)
- Haut 0-860 : face cam (crop serré, punch-in 1 plan sur 2).
- Bas 860-1920 : tableau blanc `#fbfaf7`, points `#dedbd3` (36px), bord haut 6px `#111`.
  Carte qui se construit case par case, liens verts, dézoom vue d'ensemble, case finale verte = résultat.
- Titre d'étape en haut du tableau : Inter 900, 46px, majuscules, `#1d1d1d`.

## Couleurs
- Rouge CTA `#e24b3b` · Vert résultat/CTA final `#2bb673` · Noir `#1d1d1d` · Blanc.
- Cases : jaune `#f4dc5a`, pêche `#f7c4a1`, bleu `#a9d9f2`, lavande `#d6c8fa`, départ blanc bord noir.

## Typo
- Inter 900 (titres, cases, CTA). Sous-titres : Montserrat 800, 64px, majuscules, mot actif surligné rouge (bloc registry `caption-highlight`), top 600px dans la zone face cam.

## CTA (2-3 minimum, idéalement 3 : début / milieu / fin)
- CTA 1 (≈ 4 s) — rétention : pilule rouge `#e24b3b`, radius 999px, Inter 900 34px, blanc, ombre, top 790px (à cheval face cam / tableau). Ex. « RESTE JUSQU'À LA FIN · LA RAISON N°5 VA TE SURPRENDRE ».
- CTA 2 (≈ milieu) — sauvegarde : même pilule rouge. Ex. « ENREGISTRE LA VIDÉO · TU VAS EN AVOIR BESOIN ».
- CTA 3 (fin) — conversion DM : gros bloc vert `#2bb673`, radius 28px, 54px + sous-ligne 32px, top 770px, reste jusqu'à la fin.
  Ex. « COMMENTE « MOT » » + « je regarde avec toi ce qui bloque » → DM → appel.
- Anim : entrée back.out(2) (y+30, scale 0.9→1), 4 pulsations scale 1.05 yoyo, sortie fondu vers le haut. Son : `ping` à l'entrée.
- Option : CTA abonnement (« ABONNE-TOI POUR LA SUITE ») quand la vidéo fait partie d'une série.

## Cartes mot-clé plein cadre (masquer regards / ratés)
- Couvrent 0-860 (face cam), fond plein couleur de la case en cours, petit sur-titre 44px + mot-clé Inter 900 120px. Cut net, punch scale 1.06→1. Son : `whoosh-short`.

## Montage
- Coupe serrée : blancs > 0,25 s retirés, ratés supprimés, regard vers le script détecté (mediapipe) → rogné ou masqué par carte mot-clé.
- Voix loudnorm -14 LUFS. SFX : `pop` (case), `whoosh-short` (carte/dézoom), `ping` (CTA), volume 0,3.
- Musique de fond : légère, très basse sous la voix (si dispo).
