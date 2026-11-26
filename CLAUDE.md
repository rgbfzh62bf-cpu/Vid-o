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

## Photos (règle d’Alexis)
- Recadrage photos : à chaque photo reçue (site, vidéo, autre), toujours la recadrer et vérifier le rendu sur téléphone ET ordinateur.
- Proposer « /compact » à Alexis dès que la conversation s’allonge (il veut économiser un maximum de tokens).
- Discussion longue : proposer soit /compact, soit une nouvelle discussion. Avant une nouvelle discussion, sauvegarder le travail non envoyé (les commits locaux sont perdus avec le conteneur) et noter l'état en cours dans site/CLAUDE.md.
