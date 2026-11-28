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
- First reply of every session (new or resumed): end with one line suggesting the user type `/compact` (resumed chat) or `/clear` before a new topic.
- When the chat grows long or changes topic: suggest `/compact` again, in one line.
- Resumed chat: trust the summary. Do not re-read files already seen unless they changed.
- Load only the skills the current task needs.
- Search with grep, read file excerpts, never whole files unless required.
- Keep project state in `NOTES.md` (short). Read it on resume instead of rebuilding context; update it after each finished task.

## Format Instagram (toutes les vidéos)
- Livrer en 1080×1920 (9:16), 30 fps.
- Zones sûres du Reel ouvert (plein écran, interface IG par-dessus) : rien d'important (texte, vignettes, visage) au-dessus de y=220, en dessous de y=1500, ni à droite de x=950 (boutons). Marge gauche ≥ 60 px.
- L'aperçu de la grille du profil recadre en 3:4 au centre (y≈240–1680) : le sujet doit y rester lisible.
- Vérifier chaque rendu avec une image de contrôle où les zones sûres sont tracées.

## Légende Instagram (toutes les vidéos)
- But = aider, rien à vendre ni à envoyer : jamais « je t'envoie ma méthode / mon plan ».
- Structure : phrase 1 = question liée au sujet ; phrase 2 = « Commente « CHANGEMENT » si tu t'y mets dès aujourd'hui. » (ou variante sans promesse). 20 mots max hors hashtags. Écrire dans `caption.txt` du projet.
