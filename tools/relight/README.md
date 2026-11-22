# Relighting IA gratuit (IC-Light, CPU)

1. Clone https://github.com/lllyasviel/IC-Light and build `iclib.py` from `gradio_demo.py`
   (UI removed, device cpu, float32, local model paths, low-res pass only).
2. `run_batch.py` / `redo.py`: relight one keyframe per shot (512x896, ~3-4 min each on 4 CPU).
3. `composite.py <shot> <RMBG path>`: transfer the light to every frame
   (smoothed gain map + head tracking + per-frame RMBG mask + relit background).
   `LOWFLAT=1` gives the lower body a flat tint when the hands move a lot.
