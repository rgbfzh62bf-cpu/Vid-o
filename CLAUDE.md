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

## Budget
- 100% GRATUIT, toujours. Jamais d'outil/IA/abonnement payant (pas HeyGen payant, pas RunComfy, pas Pro). Seulement free tiers, local, libres de droits.

## Légal
- Tout doit être 100% en règle : droits d'auteur, licences, droit à l'image, règles plateformes.
- Médias uniquement libres de droits avec licence vérifiée (CC0/domaine public de préférence ; CC BY = créditer). Jamais de vidéos/musiques d'autres créateurs, jamais de CC NC/ND pour usage pro.
- Garder la source + licence de chaque média dans `CREDITS.md` du projet.
- Contenu IA réaliste : activer l'étiquette "contenu IA" à la publication. Pas de promesses santé trompeuses.

## Légendes Instagram (tous les reels)
- Toujours fournir une légende avec le mot-clé **CHANGEMENT** (ex. « Commente CHANGEMENT … »).
- Courte : 1-2 lignes max + 5 hashtags ciblés sur le sujet de la vidéo (mix large + niche FR, ex. #legday #musculationfrance).

## DA (2 identités distinctes)
- Vidéos faites par Claude sans footage du coach (silhouettes, série « 5 X ») : DA vert #c8ff2e, Archivo Black, dings/taps, beat CC0.
- Vidéos où on voit le coach (face caméra) : DA « ÉDITO » = cartes papier crème #F4EFE6 (erreur/hook) qui basculent en encre #141414 (solution/CTA), accent doré #E0A458 (foncé #B8742E), Inter 900 + EB Garamond italique pour les mots forts, sous-titres phrase Inter blanc + mot-clé Garamond doré. Cartes en haut sans toucher la tête, pas de ding/flash, musique lo-fi maison. Gabarit : mofu-erreurs/build.py. Voix : débruiter DeepFilterNet3. Pas basé sur le t-shirt ni sur le site (user n'aime pas sa charte).
- RÈGLE voix off : formats IA (pompes, tractions, dos, abdos…) = vraie voix du user enregistrée (Drive VIDÉOS, 1 fichier m4a). JAMAIS de voix clonée. Découpe phrases via whisper + silences, débruitage, -16 LUFS → assets/voice/l*.wav, puis build.py + render.
