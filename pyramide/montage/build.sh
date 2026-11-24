#!/bin/sh
# Régénère index.html puis réapplique l'étalonnage du plan final.
set -e
cd "$(dirname "$0")"
python3 gen_pyr.py
node ../../.claude/skills/hyperframes/scripts/plugin-cli.mjs media-treatment --selector "#final" --grading '{"adjust":{"exposure":-0.3,"contrast":0.1,"highlights":-0.3,"temperature":0.08,"saturation":-0.05},"details":{"vignette":0.3}}' --apply --json >/dev/null
