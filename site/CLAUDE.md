# Alexis Coaching — règles du site

S'applique à TOUTE demande sur le site, la page de liens, les textes, les visuels.

## Ton et posture (toujours)
- Professionnel, rassurant, humain. Le visiteur doit penser : « je suis au bon endroit, c'est le coach qu'il me faut ».
- Tutoiement, phrases simples, chaleureuses, jamais agressives ni « vendeuses ».
- Toujours lever les peurs : débutant, manque de temps, pathologie, motivation, budget.
- Mettre en avant : sur-mesure, accompagnement, disponibilité 6/7, expérience terrain, diplôme vérifiable.

## Garde-fous
- Ne jamais inventer de chiffres, avis clients, résultats ou garanties.
- Santé : « adapter », « avec l'avis de ton médecin / kiné ». Jamais « soigner » ou « guérir » (CQP Instructeur Fitness).
- Pas de numéro de téléphone sur le site (seulement mentions légales).

## Faits validés
- Bilan chaque semaine : confirmé par Alexis.
- Alexis Bloqué, coach sportif, auto-entrepreneur. SIRET 990 253 981 00015.
- CQP Instructeur Fitness. Carte pro 07825ED0287 (préf. Yvelines, exp. 18/09/2030).
- Parcours sportif : golf 7 ans, foot 5-6 ans, volley 1 an, tennis 1 an, aïkido 1 an, puis musculation 8 ans (depuis 2018), force athlétique 3 ans. Disponible 6/7. Recontact sous 24 h.
- Photo d’accueil : coach.jpg (en salle, casque, t-shirt SPC ; crédit photographe en filigrane coupé).
- Avant / après RÉACTIVÉ (26/11) : parcours.jpg = 2018, 52 kg ; maintenant.jpg = 2026, 73 kg (miroir, recadrée 600×800 depuis la photo d’Alexis, métadonnées retirées) ; pastille +21 kg.
- Formule 1 Programmation sur mesure : 160 €/mois. Formule 2 Programmation + Nutrition : 200 €/mois.
- Suivi sur l'appli Athlyse (App Store : https://apps.apple.com/fr/app/athlyse/id6759957694 ; Google Play : https://play.google.com/store/apps/details?id=com.athlyseapp).
- Appel découverte gratuit, 30 min, visio Google Meet via Calendly : https://calendly.com/alexisbloquecoaching/30min
- Instagram : @alexisblq_coaching.
- Médiateur de la consommation : CM2C (www.cm2c.net), adhésion payée.
- Paiement : virement bancaire uniquement, mensuel à l’avance. Sans engagement, chaque mois commencé dû, pas de remboursement. Rétractation 14 j (prorata si démarrage anticipé). CGV : cgv.html.
- Domaine : alexis-coaching.fr (Hostinger, payé 3 ans, jusqu’en 2029).
- E-mail pro : alexis.bloquecoaching@gmail.com .

## Design
- RÈGLE D’ALEXIS (26/11) : le site doit être fait pour ordinateur, tablette ET téléphone, avec RIEN qui change d’une version à l’autre : même contenu, mêmes textes, mêmes boutons, mêmes infos partout (jamais de contenu caché ou raccourci sur une taille d’écran). Seule la disposition s’adapte à la largeur. Toujours vérifier les 3 (téléphone 320-430 px, tablette 768 et 1024 px, ordinateur 1440 px).
- Gras : uniquement pour les titres (ex. intitulés de la liste « L’appli », noms de sports). Jamais une ligne isolée en gras au milieu d’une liste ou d’un texte.
- PHOTOS : à CHAQUE photo reçue (site, vidéo, autre), la recadrer soi-même et vérifier le rendu sur téléphone ET ordinateur avant de proposer.
- TOUJOURS vérifier le rendu téléphone (320, 375, 390, 430 px) en plus de l’ordinateur : aucun débordement horizontal, boutons faciles à toucher.
- Logo : logo.png (transparent, NON utilisé dans l’en-tête : Alexis préfère le nom en texte) / logo.jpg (haltère bleue + ALEXIS COACHING). Favicon « AC » au centre de l’haltère (disques bleus de chaque côté) favicon*.png / apple-touch-icon.png, partage réseaux partage.jpg.
- Bleu nuit #0B1628, blanc, accent bleu #5B9BEF. Polices : Big Shoulders Display / Manrope / JetBrains Mono.
- Ordre de page : Qui suis-je → Approche → Appli → Tarifs → FAQ → Appel (= « Commencer », fin de page). Formulaire de contact SUPPRIMÉ (26/11, choix d’Alexis : doublon avec le bloc appel) ; boutons « Choisir cette formule » → #appel. FAQ réduite à 6 questions.

## Avant mise en ligne
Voir `MISE-EN-LIGNE.md` (médiateur de la consommation obligatoire, hébergeur, formulaire Netlify, Calendly, adresse mail coaching).

## Aperçu claude.ai
Images en fichiers séparés = cassées dans l’appli d’Alexis. Publier un aperçu avec images inlinées (data URI) depuis le scratchpad vers les URL existantes : site https://claude.ai/artifact/RrFDYNC85ithxauYMMkANm , liens https://claude.ai/artifact/1XBNvJcfkLxQxs3YXXKiZj . Le repo garde les chemins relatifs.

## Mise en ligne
RÈGLE D’ALEXIS : ne rien envoyer (push = mise en ligne Netlify) tant qu’il n’a pas dit que la série de modifications est terminée. Montrer en aperçu, committer en local, puis UN push à son feu vert.
IMPORTANT : crédits Netlify limités. 25/11/2026 : quota gratuit épuisé, Alexis est passé sur l’offre Personal (9 $/mois, 1 000 crédits) pour débloquer ; résilié, repasse en gratuit le 24/12/2026. REGROUPER les modifs, demander validation, puis UN SEUL push par série de changements.
Hébergeur définitif : Netlify (choix d’Alexis : sécurité avant tout, badge « Powered by Netlify » accepté). En-têtes de sécurité via _headers (build.py).
Netlify déploie le dossier `site-en-ligne/` depuis la branche `claude/exciting-newton-swewu8`. Après CHAQUE modif du site : `python3 site/build.py`, commit, push.

## État en cours (pour une nouvelle discussion)
- 26/11 (soir, EN LIGNE au « go ») : relecture juridique faite par Claude à la demande d’Alexis (« je te fais confiance ») : mentions légales (EI, adresse Netlify d’après ses contrats : 101 2nd Street Suite 575 SF CA 94105 ; Netlify ne publie pas de téléphone ; RGPD complet prospects/clients, données santé = consentement explicite, prestataires + transferts US, droits) ; CGV (nutrition ≠ médecin/diététicien, majeurs, facture, Athlyse tiers, photos/vidéos confidentielles). Polices auto-hébergées (site/fonts, copiées par build.py) : plus aucun appel à Google. RC Pro : oui (confirmé par Alexis), mentionnée dans les CGV art. 7 sans nom d’assureur.
- 26/11/2026 : TOUT EN LIGNE (commit 035f23a), vérifié par Alexis sur son téléphone. Reste côté Alexis : relecture mentions légales (paragraphe données réécrit : Calendly + mails), lien bio Instagram, 2FA.
- Modifs NON en ligne sauvegardées sur la branche `claude/sauvegarde-alexis` (Netlify ne la déploie pas). Nouvelle discussion : `git fetch origin claude/sauvegarde-alexis && git merge FETCH_HEAD` sur `claude/exciting-newton-swewu8`, puis push UNIQUEMENT au feu vert d'Alexis.
- Contenu : maquettes téléphone Athlyse dans les formules, boutons App Store + Google Play, gras harmonisé, sports en étiquettes, règles /compact. Page liens : vrais logos (Apple, Google Play, Athlyse, Instagram, Mail, appel), formules sans prix (« 2 formules · sans engagement »), photo avatar.jpg = tête entière découpée dans coach.jpg.
- Lien Google Play d'Athlyse ajouté (https://play.google.com/store/apps/details?id=com.athlyseapp). Attendre les autres retours du créateur d'Athlyse (call avec son pote), puis tout envoyer en UN push au « go ».
- Netlify : environ 925 crédits au dernier relevé ; passage à l'offre gratuite le 24/12/2026.

### Projet « Fondations · force athlétique » (brouillon, pas sur le site)
- RÈGLE : on travaille dessus, RIEN sur le site. Quand Alexis dit que tout est bon, LUI DEMANDER s’il veut le mettre en ligne ou non.
- Nom validé : « Fondations » (jamais le mot « débutant »). Aperçu : brouillons/apercu-programme.html → https://claude.ai/artifact/XedtcFqK8iEr3tjkrsaN8t
- 2 versions 3 jours / 4 jours, 29 € chacune (prix changé par Alexis le 26/11, avant 39 €), pas de pack. Alexis veut une rubrique de vente sur le site. Afficher « Paiement unique · accès illimité », ne jamais parler d'abonnement ni de « à vie ».
- Public : débuter sans s'engager dans un coaching (ne jamais parler d'argent), puis coaching quand on stagne.
- Livraison : fichier Google Sheets / .xlsx (pas Athlyse). Build : brouillons/build_v2.py + build_prog.py → Fondations-force-athletique-{3,4}-jours.xlsx. 1RM saisi une fois, 4 semaines, puis retour S1 avec +2,5 kg par bloc.
- Ne jamais dire publiquement que le programme s'inspire d'autres coachs. Ne jamais modifier les fichiers Drive partagés par d'autres.
- Google Sheets natifs (Drive d’Alexis, privés) : 3 j https://docs.google.com/spreadsheets/d/1E0UkcjXFiR4KBE55Hm_lQpc2iQAFIuLuRmTiAITR1_M/edit · 4 j https://docs.google.com/spreadsheets/d/1asLSPusmlUe-kSLbifOTyEoNqGRvt38thjciWOrOkKE/edit (créés depuis les xlsx ; lien client = remplacer /edit par /copy).
- RÈGLE Drive : à chaque nouvelle version d’un Sheets Fondations, mettre soi-même l’ancienne à la corbeille (accord d’Alexis). Ne jamais toucher aux fichiers partagés par d’autres.
- Tonnage : récap par mouvement (S/B/D, variantes comprises) en fin de séance ; renfo hors tonnage. Pas de compteur de répétitions (seul le tonnage compte). Séries identiques S1→S4 (pas de série en plus, choix d’Alexis) : seule la charge monte, en kg par semaine (règle d’Alexis) : squat +5, développé couché +2,5, soulevé de terre +7,5 (variantes comprises) ; bloc +2,5 kg. Colonne JOUR = « JOUR n » seul (vertical, pas de thème). Partie fixe = JOUR + EXERCICE (colonnes A:C), aucune case fusionnée à cheval sur la limite. RPE = RESSENTI sur 10 (règle d’Alexis), jamais « répétitions en réserve » ni RIR ; renfo = RPE 8. ORDRE dans chaque séance : squat → développé couché → soulevé de terre, puis renfo. 3 jours : J1 squat + DC, J2 SBD léger (volume), J3 SBD lourd (RPE plus haut). Volume calé sur la semaine d’Alexis chez Ciel : ~5 séries par mouvement principal (3 et 4 jours).
- Tableur : MES 1RM resserré (A:G) en 2 cartes : TES 1RM + total S·B·D, BLOC EN COURS (bloc = D14). BILAN resserré pareil (B:F, titre au bout du tableau). RÈGLE : tout aligné (titre, trait bleu, tableaux finissent au même bord), hauteurs de lignes régulières, vérifier téléphone + ordi. Thème C (fond bleu nuit autour, tableaux clairs, en-tête et résumé bleu nuit, accent bleu). THEME=B = fond blanc, en-tête bleu nuit.
- CGV programme : brouillon brouillons/cgv-programme.html (à intégrer au lancement, [PLATEFORME] à remplacer).
- À faire : choix Payhip ou Gumroad, vérifier URSSAF (activité vente de contenu numérique) et CM2C.
