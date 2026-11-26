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
- Avant / après MASQUÉ pour l’instant (seule la photo 2018 « Mes débuts » est affichée, bloc à remettre dans index.html via le commentaire AVANT/APRÈS). photo miroir (parcours.jpg) = 2018, 52 kg. Maintenant = 73 kg ; photo actuelle à recevoir.
- Formule 1 Programmation sur mesure : 160 €/mois. Formule 2 Programmation + Nutrition : 200 €/mois.
- Suivi sur l'appli Athlyse (App Store : https://apps.apple.com/fr/app/athlyse/id6759957694 ; Google Play : https://play.google.com/store/apps/details?id=com.athlyseapp).
- Appel découverte gratuit, 30 min, visio Google Meet via Calendly : https://calendly.com/alexisbloquecoaching/30min
- Instagram : @alexisblq_coaching.
- Médiateur de la consommation : CM2C (www.cm2c.net), adhésion payée.
- Paiement : virement bancaire uniquement, mensuel à l’avance. Sans engagement, chaque mois commencé dû, pas de remboursement. Rétractation 14 j (prorata si démarrage anticipé). CGV : cgv.html.
- Domaine : alexis-coaching.fr (Hostinger, payé 3 ans, jusqu’en 2029).
- E-mail pro : alexis.bloquecoaching@gmail.com (formulaire Netlify à envoyer ici).

## Design
- Gras : uniquement pour les titres (ex. intitulés de la liste « L’appli », noms de sports). Jamais une ligne isolée en gras au milieu d’une liste ou d’un texte.
- PHOTOS : à CHAQUE photo reçue (site, vidéo, autre), la recadrer soi-même et vérifier le rendu sur téléphone ET ordinateur avant de proposer.
- TOUJOURS vérifier le rendu téléphone (320, 375, 390, 430 px) en plus de l’ordinateur : aucun débordement horizontal, boutons faciles à toucher.
- Logo : logo.png (transparent, NON utilisé dans l’en-tête : Alexis préfère le nom en texte) / logo.jpg (haltère bleue + ALEXIS COACHING). Favicon « AC » au centre de l’haltère (disques bleus de chaque côté) favicon*.png / apple-touch-icon.png, partage réseaux partage.jpg.
- Bleu nuit #0B1628, blanc, accent bleu #5B9BEF. Polices : Big Shoulders Display / Manrope / JetBrains Mono.
- Ordre de page : Qui suis-je → Approche → Appli → Tarifs → Appel → FAQ → Commencer.

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
- Modifs NON en ligne sauvegardées sur la branche `claude/sauvegarde-alexis` (Netlify ne la déploie pas). Nouvelle discussion : `git fetch origin claude/sauvegarde-alexis && git merge FETCH_HEAD` sur `claude/exciting-newton-swewu8`, puis push UNIQUEMENT au feu vert d'Alexis.
- Contenu : maquettes téléphone Athlyse dans les formules, boutons App Store + Google Play, gras harmonisé, sports en étiquettes, règles /compact. Page liens : vrais logos (Apple, Google Play, Athlyse, Instagram, Mail, appel), formules sans prix (« 2 formules · sans engagement »), photo avatar.jpg = tête entière découpée dans coach.jpg.
- Lien Google Play d'Athlyse ajouté (https://play.google.com/store/apps/details?id=com.athlyseapp). Attendre les autres retours du créateur d'Athlyse (call avec son pote), puis tout envoyer en UN push au « go ».
- Netlify : environ 925 crédits au dernier relevé ; passage à l'offre gratuite le 24/12/2026.
