# DA — vidéos coach fitness (à appliquer à toutes les vidéos)

Objectif : vues → abonnés → prospects (DM) → clients. Rétention max.
Règle n°1 : copier à l'identique le format de la vidéo de référence (Brian Mark « Full blueprint », voir NOTES.md). Seuls le sujet et la tête changent.
Projet modèle : `balance/montage/` (copier le projet, changer rush + textes + timings).

## Mise en page (1080x1920)
- Haut 0-860 : face cam plein cadre.
- Bas 860-1920 : tableau blanc quadrillé (fond `#fff`, lignes `#eef0f4` 2px tous les 44px, style Freeform).
  La caméra se déplace de carte en carte, flèches vertes `#22c35e` (11px, tête en chevron), dézoom vue d'ensemble, carte finale = résultat.
- Titre d'étape en haut du tableau : Inter 800, 46px, MAJUSCULES, `#111`, centré.

## Cartes du tableau (façon Notes / post-it)
- Radius 18px, bordure 2px `#ece7d8`, ombre douce, padding 30px. En-tête gris 26px (« Erreur 1 ») avec rond coché jaune `#e3a400`, trait de séparation, puis texte Inter 700 42px en minuscules.
- Teintes pastel : jaune `#fff6c7`, pêche `#ffe6d4`, bleu `#e3f3fd`, lavande `#efe9ff`, départ blanc. Finale : jaune + drapeau vert + bandeau vert « Résultat : … ».

## Titre d'accroche (0-3,6 s)
- Encadré blanc, radius 18px, texte noir Inter 800 60px sur une ligne, posé en bas de la face cam (top 600px).
  Sous-titre blanc avec ombre, 48px, entre parenthèses (ex. « (les 5 raisons) »). Pas de sous-titres pendant le titre.

## Sous-titres
- Inter 700 58px, blanc, casse normale, ombre noire (0 2px 6px .85 + halo 18px), pas de surlignage. Groupes de 3 mots max, en bas de la face cam (top 690px).
- Bloc registry `caption-highlight` avec le fond rouge désactivé.

## CTA (2-3 minimum, idéalement 3 : début / milieu / fin)
- Même langage que le titre : encadré blanc, radius 18px, texte noir Inter 800 38px, mot-clé en vert `#22c35e`, ombre, top 800px (à cheval face cam / tableau).
- CTA 1 (≈ 4 s) rétention : « Reste jusqu'à la fin : la raison n°5 va te surprendre ».
- CTA 2 (milieu) sauvegarde : « Enregistre la vidéo, tu vas en avoir besoin ».
- CTA 3 (fin, jusqu'au bout) conversion : 56px, « Commente « MOT » » + petite ligne grise « je regarde avec toi ce qui bloque » → DM → appel.
- Anim : entrée back.out(2), 4 pulsations scale 1.05, sortie fondu. Son : `ping`.
- Option : CTA abonnement quand la vidéo fait partie d'une série.

## Cartes mot-clé plein cadre (masquer un regard vers le script)
- Couvrent la face cam (0-860) : quadrillage sombre `#1c1c1e`/`#2a2a2e`, post-it jaune centré, sur-titre gris 34px + mot-clé Inter 800 96px. Cut net. Son : `whoosh-short`.

## Montage et son
- Coupe serrée : blancs > 0,25 s retirés, ratés supprimés, regard vers le script détecté (mediapipe) → rogné ou masqué.
- Voix loudnorm -14 LUFS.
- Musique de fond continue (comme la référence), environ 15 dB sous la voix.
- SFX volume 0,3 : `pop` (carte), `whoosh-short` (carte mot-clé / dézoom), `ping` (CTA).
