# Vid-o — projets vidéo

Goal: professional video editing, minimum tokens.

## Always
- Caveman mode ON from first reply, every session. Follow the `caveman` skill. Off only if user says "stop caveman" / "normal mode".
- Answer user in French.

## Video work
Any video task (make, edit, cut, animate, caption, render, convert): load skills before acting.
1. `hyperframes` first — render contract + work loop.
2. `hyperframes-cli` for scaffold, preview, timeline edits, render.
3. `hyperframes-registry` before hand-building any effect, transition, title, caption, chart. Reuse blocks; don't rewrite.
4. `media-use` for music, SFX, voiceover, images, transcripts, colour grade.
5. `reverse-any-video` when user gives a video to copy or recreate.
New skill needed? Use `find-skills`.

## Token rules
- Reuse registry blocks over custom code.
- Read only needed file parts. No full-file dumps in chat.
- Report results in 1-3 lines.

## Légende Instagram (toujours)
- Structure validée (pour toutes les vidéos) : phrase 1 = question liée au sujet ;
  phrase 2 = « Commente « CHANGEMENT » et je t'envoie ma méthode. » Ne jamais commencer par « Commente ».
  Ex. : « Tu veux fondre, couper ton appétit et tenir sur le long terme ? Commente « CHANGEMENT » et je t'envoie ma méthode. »
- Légende courte : 1 ou 2 phrases, 20 mots max (hors hashtags), « Commente « CHANGEMENT » » compris dans les 20.
- Écrire la légende dans `caption.txt` du projet.

## Autonomie (toutes les vidéos)
- Reproduction d'un réel : copier à l'identique (typo, tailles, couleurs, trait, détourage, liseré, transitions, rythme), seul le sujet/la personne change.
- Agir en autonomie sur tout ce qui rend bien et reste qualitatif ; ne pas faire ce qui rendrait faux ou moche (ex. incruster l'utilisateur dans un fond d'une autre vidéo) et garder la version propre.
- Skills gratuits autorisés si besoin ; jamais de skills payants.
- Animations : garder la même mécanique/le même style que la vidéo de référence, mais adapter le contenu au sujet de l'utilisateur
  (ex. référence = bio Instagram qui se remplit → nous = checklist perte de poids qui se remplit). Jamais copier un visuel hors sujet.
- Prises : toujours face caméra. Tête baissée/sur le côté = l'utilisateur lit sa tablette → prise à rejeter, prendre une autre prise.
- Montage : couper les blancs/hésitations > 0,25 s à l'intérieur des phrases (petit jump cut OK), pour que ça enchaîne.
