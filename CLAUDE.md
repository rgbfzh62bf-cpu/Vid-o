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
