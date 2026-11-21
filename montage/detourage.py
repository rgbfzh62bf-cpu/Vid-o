#!/usr/bin/env python3
"""Re-cut the person in the bottom half onto pure black, then sharpen the whole video.
Usage: python3 detourage.py SRC OUT [--test FRAME_SECONDS]

- Bottom half (y >= 1920 on a 2160x3840 frame): the person mask is rebuilt from the
  existing cut-out (old background = 0), holes filled, leftover wall removed,
  outline smoothed, then composited onto pure black.
- Captions sitting at the top of the bottom half (white text) are preserved.
- The final encode applies light denoise + contrast-adaptive sharpening.
"""
import argparse, subprocess, sys, time
import numpy as np, cv2

ap = argparse.ArgumentParser()
ap.add_argument("src"); ap.add_argument("out")
ap.add_argument("--test", type=float, default=None)
a = ap.parse_args()

W, H = 2160, 3840
Y0 = 1920              # start of the bottom half
TEXT_BAND = 230        # rows (from Y0) where captions can live
RH = H - Y0



def matte(region):
    """Alpha from the existing cut-out: the old background is exactly 0,
    so every non-zero pixel connected to the body is the person."""
    mx = region.max(axis=2)
    m = (mx > 0).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((7, 7), np.uint8))
    # fill holes (dark pixels inside the body, e.g. black shirt / hair)
    ff = m.copy()
    mask = np.zeros((m.shape[0] + 2, m.shape[1] + 2), np.uint8)
    for x in range(0, m.shape[1], 40):  # flood the background from the edges
        for y in (0, m.shape[0] - 1):
            if ff[y, x] == 0:
                cv2.floodFill(ff, mask, (x, y), 2)
    for y in range(0, m.shape[0], 40):
        for x in (0, m.shape[1] - 1):
            if ff[y, x] == 0:
                cv2.floodFill(ff, mask, (x, y), 2)
    m = (ff != 2).astype(np.uint8)
    # keep only the main body
    n, lab, st, _ = cv2.connectedComponentsWithStats(m)
    if n > 2:
        m = (lab == 1 + np.argmax(st[1:, cv2.CC_STAT_AREA])).astype(np.uint8)
    # remove leftover wall (bright, colourless pixels) stuck to the outline
    dist = cv2.distanceTransform(m, cv2.DIST_L2, 5)
    mn = region.min(axis=2).astype(np.int16)
    wall = ((mn > 135) & ((mx.astype(np.int16) - mn) < 35) & (dist < 90)).astype(np.uint8)
    wall = cv2.dilate(cv2.morphologyEx(wall, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8)),
                      np.ones((9, 9), np.uint8))
    al = m.astype(np.float32)
    al[wall > 0] = 0
    # smooth the staircase outline: blur then re-sharpen around 0.5,
    # slightly inset so no old edge pixels leak
    al = cv2.GaussianBlur(al, (0, 0), 7)
    al = np.clip((al - 0.55) * 3.0 + 0.5, 0, 1)
    return al


def process(frame):
    reg = frame[Y0:].copy()
    al = matte(reg)[..., None]
    out = (reg.astype(np.float32) * al).astype(np.uint8)
    # keep white captions in the top band of the bottom half
    band = reg[:TEXT_BAND]
    lum = band.max(axis=2)
    keep = (lum > 120)[..., None]
    out[:TEXT_BAND] = np.where(keep, band, out[:TEXT_BAND])
    frame[Y0:] = out
    return frame


SHARP = "hqdn3d=1.5:1.5:3:3,cas=0.55"

if a.test is not None:
    raw = subprocess.check_output(["ffmpeg", "-v", "error", "-ss", str(a.test), "-i", a.src,
                                   "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"])
    fr = np.frombuffer(raw, np.uint8).reshape(H, W, 3).copy()
    cv2.imwrite(a.out, cv2.cvtColor(process(fr), cv2.COLOR_RGB2BGR))
    sys.exit()

dec = subprocess.Popen(["ffmpeg", "-v", "error", "-i", a.src, "-f", "rawvideo",
                        "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
                        "-s", f"{W}x{H}", "-r", "30", "-i", "-", "-i", a.src,
                        "-map", "0:v", "-map", "1:a", "-vf", SHARP + ",format=yuv420p",
                        "-c:v", "libx264", "-preset", "medium", "-crf", "16",
                        "-c:a", "copy", "-movflags", "+faststart", a.out], stdin=subprocess.PIPE)
n, t0 = 0, time.time()
fs = W * H * 3
while True:
    buf = dec.stdout.read(fs)
    if len(buf) < fs:
        break
    enc.stdin.write(process(np.frombuffer(buf, np.uint8).reshape(H, W, 3).copy()).tobytes())
    n += 1
    if n % 60 == 0:
        print(f"{n} images, {n / (time.time() - t0):.1f} img/s", flush=True)
enc.stdin.close(); enc.wait(); dec.wait()
print("OK", a.out, n, "images")
