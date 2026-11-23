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
- Chaque légende/titre de réel contient « Commente « CHANGEMENT » » (mot-clé de l'utilisateur), suivi de la promesse liée au sujet.
  Ex. : « Commente « CHANGEMENT » si tu veux fondre, couper ton appétit et tenir sur le long terme. »
- Légende courte : 1 ou 2 phrases, 20 mots max (hors hashtags).
- Écrire la légende dans `caption.txt` du projet.
