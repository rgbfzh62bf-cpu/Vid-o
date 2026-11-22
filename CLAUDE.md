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

## Output format (always)
Every video = Instagram Reel, unless user says otherwise.
- 4K vertical master: 2160×3840, 9:16, 30 fps. Keep source footage at full res end to end (never downscale raw to 1080p).
- Composition stays 1080×1920; render with `--resolution portrait-4k --quality delivery`.
- Safe zones (in 1080×1920 composition px): keep text/stickers out of top 250, bottom 420, right 140 (IG UI).
- Export: H.264 High L5.1, yuv420p, ~40 Mbps, AAC 48 kHz 192k, loudness -14 LUFS, `+faststart`.

## Audience (fiche avatar)
All topics, scripts, on-screen words: written for this person, spoken to directly ("tu").
- 20-35 ans.
- Veut perdre du poids, ne sait pas comment s'y prendre.
- Stagne malgré ses efforts.
Speak to their frustration and confusion; simple, concrete, no jargon.

## Skill choice
- Only free skills: no paid API, no paid account, no credits. Local tools or free tiers only.
- Pick the best performers: high install count (1K+), reputable source, active repo.
- No free option? Say so and propose a local workaround. Never install a paid one without asking.

## Token rules
- Reuse registry blocks over custom code.
- Read only needed file parts. No full-file dumps in chat.
- Report results in 1-3 lines.
