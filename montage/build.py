#!/usr/bin/env python3
"""Motion-design edit: animated word-by-word captions, punch-in zooms,
flashes, hook title and progress bar. Usage: python3 build.py SRC OUT"""
import json, subprocess, sys, os

SRC, OUT = sys.argv[1], sys.argv[2]
HERE = os.path.dirname(os.path.abspath(__file__))
cap = json.load(open(os.path.join(HERE, "captions.json"), encoding="utf-8"))
DUR = float(subprocess.check_output(
    ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", SRC]))
W, H, FPS = 1080, 1920, 30


def ts(t):
    t = max(0, t)
    return f"{int(t // 3600)}:{int(t % 3600 // 60):02d}:{t % 60:05.2f}"


ass = [f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Inter Black,104,&H00FFFFFF,&H00FFFFFF,&H00000000,&H90000000,0,0,0,0,100,100,0,0,1,9,6,5,60,60,0,1
Style: Hook,Inter Black,82,&H00FFFFFF,&H00FFFFFF,&H003C14E6,&H003C14E6,0,0,0,0,100,100,2,0,3,22,0,8,60,60,0,1
Style: Fx,Inter,10,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,7,0,0,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"""]
ev = ass.append

# Hook title: drops in from the top with an overshoot, then fades out
ev(f"Dialogue: 5,{ts(0.15)},{ts(2.9)},Hook,,0,0,0,,"
   f"{{\\move(540,-120,540,300,0,260)\\fad(0,300)\\frz-3\\fscx80\\fscy80"
   f"\\t(0,260,\\fscx112\\fscy112)\\t(260,420,\\fscx100\\fscy100)}}{cap['hook']}")

YELLOW = "&H001EE6FF&"
punches = []
for ph in cap["phrases"]:
    words = ph["words"]
    start = words[0][0]
    punches.append((start, ph["end"]))
    # white flash on the beat
    ev(f"Dialogue: 4,{ts(start)},{ts(start + 0.22)},Fx,,0,0,0,,"
       f"{{\\an7\\pos(0,0)\\1a&H70&\\fad(0,200)\\p1}}m 0 0 l {W} 0 {W} {H} 0 {H}{{\\p0}}")
    for i, (t, _) in enumerate(words):
        t_end = words[i + 1][0] if i + 1 < len(words) else ph["end"]
        parts = []
        for j, (_, w) in enumerate(words[: i + 1]):
            if j == i:  # current word: yellow, pops from 135% back to 100%
                parts.append(f"{{\\1c{YELLOW}\\fscx135\\fscy135\\t(0,130,\\fscx100\\fscy100)}}{w}"
                             f"{{\\1c&HFFFFFF&\\fscx100\\fscy100}}")
            else:
                parts.append(w)
        # break long phrases on two lines
        if len(words) > 3 and i >= 2:
            parts.insert(2, "\\N")
            text = " ".join(parts).replace(" \\N ", "\\N")
        else:
            text = " ".join(parts)
        intro = "\\fad(120,0)" if i == 0 else ""
        outro = "\\fad(0,180)" if i == len(words) - 1 else ""
        ev(f"Dialogue: 3,{ts(t)},{ts(t_end)},Cap,,0,0,0,,{{\\pos(540,1400){intro}{outro}}}{text}")

# Progress bar along the bottom
ev(f"Dialogue: 6,{ts(0)},{ts(DUR)},Fx,,0,0,0,,"
   f"{{\\an7\\pos(0,{H - 14})\\1c{YELLOW}\\fscx0\\t(0,{int(DUR * 1000)},\\fscx100)\\p1}}"
   f"m 0 0 l {W} 0 {W} 14 0 14{{\\p0}}")

ass_path = os.path.join(HERE, "motion.ass")
open(ass_path, "w", encoding="utf-8").write("\n".join(ass) + "\n")

# Zoom curve: slow push-in + punch-in on each spoken line
t = f"(on/{FPS})"
z = f"1+0.05*{t}/{DUR:.2f}"
for a, b in punches:
    z += (f"+0.16*clip(({t}-{a})/0.12,0,1)*clip(({b}+0.35-{t})/0.35,0,1)")
# small shake while laughing on the last line
la, lb = punches[-1]
shake = f"(between({t},{la},{lb})*14*sin({t}*45))"

vf = (f"fps={FPS},scale=1440:2560:flags=lanczos,"
      f"zoompan=z='{z}':d=1:s={W}x{H}:fps={FPS}:"
      f"x='iw/2-iw/zoom/2+{shake}':y='ih/2-ih/zoom/2',"
      f"eq=contrast=1.07:saturation=1.18:gamma=0.97,vignette=PI/5,"
      f"ass={ass_path}")

subprocess.run(["ffmpeg", "-y", "-v", "error", "-stats", "-i", SRC, "-vf", vf,
                "-map", "0:v:0", "-map", "0:a:0",
                "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p",
                "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", OUT], check=True)
print("OK", OUT)
