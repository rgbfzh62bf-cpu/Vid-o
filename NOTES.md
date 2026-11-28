# NOTES

## Fondations · Force athlétique (Google Sheets)
- 4 jours: 1asLSPusmlUe-kSLbifOTyEoNqGRvt38thjciWOrOkKE · 3 jours: 1E0UkcjXFiR4KBE55Hm_lQpc2iQAFIuLuRmTiAITR1_M
- Sources (blocs de départ seulement): Paul B1-B2 (4j) + B3 (3j), Ciel Block 1 Getting started + Bloc 2-3.
- 3 blocs × 4 sem: B1 Bases (orig, offsets kg/sem), B2 Peaufiner, B3 Intensifier.
- B2/B3: % = base + 2%×semaine, semaine index caché en O1 (0-3), RPE via CHOOSE($O$1+1;…).
- MES 1RM D14 = NUMÉRO DU CYCLE (+2,5 kg/cycle). BILAN 12 lignes. VARIANTES +4 fiches.
- 2026-11-27: blocs 2 et 3 ajoutés dans les deux fichiers, testés (1RM test effacés).
- 2026-11-27 v2: B2/B3 réécrits d'après les blocs génériques de Paul/Ciel (tempo 3-1-3, SDT pause 2 CT, singles RPE, face pull, belt squat). Déficit retiré.
- 2026-11-27 v3 : protections ajoutées (32 plages, mode avertissement) sur les 2 fichiers. Cases libres : K:N des lignes d'exercices, MES 1RM D7:D9 + D14. Le passage en mode avertissement est voulu, parce que celui qui copie le fichier en devient propriétaire et pourrait sinon tout modifier sans alerte. Vérifié : S1 B2 > S1 B1 (ex. 3j squat principale 75→78 %, couché 77→80 %).
- 2026-11-27 v4 : « série principale / séries allégées » → « top set / back-off » partout (2 fichiers). Définition ajoutée dans LEXIQUE, étape 3.
- 2026-11-27 v5 : noms remis en simple (« Squat », « Développé couché »), « Top set : » / « Back-off : » placés en tête de CONSIGNE (2 fichiers, 24 semaines).
- 2026-11-28 v6 : colonnes A→G (exercice à charge conseillée) figées sur les 24 semaines. Fusions de D2/D3/D6/D7 réduites de D:I à D:G (sinon Sheets refuse de figer).
- 2026-11-28 v7 : 3j BILAN, le graphique (id 1016337248) cachait les semaines B2 S3 → B3 S4 ; déplacé sous le tableau (ligne 20). Lignes 11-18 passées à 34 px (2 fichiers). Onglet COMMENCER ICI renommé LEXIQUE. Pas de graphique dans le BILAN 4j.
- 2026-11-28 v8 : étiquettes du graphique BILAN (O7:O18) passées de S1..S4 à B1 S1..B3 S4. Graphique ajouté au BILAN 4j (id 1586681600, ligne 20).
- 2026-11-28 v9 : BILAN, graphiques déplacés à droite du tableau (H6, 560 px) dans les 2 fichiers. Sur mobile, un graphique au-dessus ou en dessous du tableau capte le défilement.
- 2026-11-28 v10 : graphique BILAN aligné sur le tableau (ancré à H6, hauteur 445 px = lignes 6 à 18), 2 fichiers.
- 2026-11-28 v11 : BILAN, ligne bleue sous le titre prolongée jusqu'à la colonne O ; graphique ramené à 510 px de large (H à O), 2 fichiers.
- Règle : tout doit être esthétique, rendu vérifié visuellement avant de livrer (ajoutée à CLAUDE.md).
- 2026-11-28 v12 : vraie cause du blocage BILAN 4j = ancien graphique (1096971635) posé sur le tableau. Déplacé en H6 (420×445), il est maintenant superposé à 1586681600, qui est identique : il faudra en supprimer un (suppression refusée par le contrôle auto). Rendu vérifié par export PDF pour les 2 fichiers.
- 2026-11-28 v13 : BILAN restylé (2 fichiers). Graphique sur fond blanc (texte lisible), prévu bleu #2F6FD6, réalisé ambre #F5B942, étiquettes S1–S12, axe à partir de 0, largeur 423 px. Tableau : séparateurs bleus entre les blocs, en-tête SEMAINE aligné à gauche, 0 affiché « — ». Rendu vérifié par export PDF. Doublon de graphique 4j toujours là (1096971635 + 1586681600).
- 2026-11-28 v14 : en-tête BILAN (2 fichiers). Badge BILAN déplacé en L2:N3, aligné sur le bord droit du graphique. 2 chiffres clés en H2:K3 : total prévu (=SUM(D7:D18)) et total réalisé (=SUM(E7:E18)), en blanc 16 pt avec une étiquette bleue 8 pt. E2:F3 vidé. Rendu vérifié par export PDF.
- 2026-11-28 v15 : zone figée A:G passée de 497 à 324 px sur les 24 semaines (A6 B24 C124 D36 E36 F40 G58), pour qu'elle tienne sur un écran de téléphone : trop large, Sheets annule le figement. En-têtes raccourcis : SÉR., CHARGE CONSEIL. ; sous-titre « N jours · … ». VARIANTES : « SÉRIE PRINCIPALE ET SÉRIES ALLÉGÉES » remplacé par « TOP SET ET BACK-OFF ». Rendu vérifié par export PDF.
- 2026-11-28 v16 : zone figée A:G ramenée à 276 px (A2 B20 C106 D28 E32 F34 G54) sur les 24 semaines, pour qu'elle tienne entière sur un téléphone. Polices : en-têtes 7, exercices 9, charge 9 au format 0.0 (sans kg). En-têtes SÉR / RÉP / %RM / KG, « ressenti » au lieu de « au ressenti », titre « FONDATIONS · FORCE », sous-titre en 8 pt sur 2 lignes. Lignes d'exercice à 46 px, ligne Tractions à 64. Semaine 1 mise en forme puis copiée (PASTE_FORMAT) sur les autres. Rendu vérifié par export PDF.
- 2026-11-28 v17 : « au ressenti » remis en entier (colonne KG, 2 fichiers, 24 semaines), sur 2 lignes (retour à la ligne + centré verticalement). Ne plus raccourcir les textes des athlètes sans demander. Rendu vérifié par export PDF.
