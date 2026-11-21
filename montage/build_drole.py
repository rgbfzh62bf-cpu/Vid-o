#!/usr/bin/env python3
"""Meme-style funny edit: freeze frames, crash zooms, shake, boom sounds, captions.
Usage: python3 build_drole.py SRC OUT"""
import subprocess, sys, os

SRC, OUT = sys.argv[1], sys.argv[2]
HERE = os.path.dirname(os.path.abspath(__file__))
W, H, FPS = 1080, 1920, 30

# Source cut points (seconds) and freeze lengths
F1_AT, F1_LEN = 4.25, 1.0   # scream
F2_AT, F2_LEN = 6.00, 1.2   # the guy shows up
END = float(subprocess.check_output(
    ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", SRC]))
# output timeline
o_f1 = F1_AT
o_b = o_f1 + F1_LEN
o_f2 = o_b + (F2_AT - F1_AT)
o_c = o_f2 + F2_LEN
TOTAL = o_c + (END - F2_AT)


def ts(t):
    return f"0:{int(t // 60):02d}:{t % 60:05.2f}"


RED, YEL = "&H002020FF&", "&H001EE6FF&"
ass = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Top,Inter Black,70,&H00000000,&H00000000,&H00FFFFFF,&H00FFFFFF,0,0,0,0,100,100,0,0,3,24,0,8,70,70,170,1
Style: Cap,Inter Black,92,&H00FFFFFF,&H00FFFFFF,&H00000000,&H90000000,0,0,0,0,100,100,0,0,1,9,6,2,60,60,330,1
Style: Big,Inter Black,190,&H002020FF,&H00FFFFFF,&H00FFFFFF,&H00000000,0,0,0,0,100,100,0,0,1,12,0,5,0,0,0,1
Style: Stamp,Inter Black,120,&H002020FF,&H00FFFFFF,&H002020FF,&H00000000,0,0,0,0,100,100,6,0,1,0,0,5,0,0,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 5,{ts(0.1)},{ts(3.1)},Top,,0,0,0,,{{\\fad(150,150)\\fscx90\\fscy90\\t(0,150,\\fscx100\\fscy100)}}ELLE VOULAIT JUSTE FAIRE\\NUNE VIDÉO STYLÉE...
Dialogue: 5,{ts(3.2)},{ts(o_f1)},Cap,,0,0,0,,{{\\fscx130\\fscy130\\t(0,120,\\fscx100\\fscy100)}}ÇA A DURÉ {{\\1c{YEL}}}3 SECONDES
Dialogue: 6,{ts(o_f1)},{ts(o_b)},Big,,0,0,0,,{{\\pos(540,1350)\\frz-8\\fscx40\\fscy40\\t(0,90,\\fscx115\\fscy115)\\t(90,160,\\fscx100\\fscy100)\\t(160,1000,\\frz8)}}AAAAAH
Dialogue: 5,{ts(o_b + 0.1)},{ts(o_f2)},Cap,,0,0,0,,{{\\fad(80,0)}}PÉTAGE DE CÂBLE\\N{{\\1c{YEL}}}EN DIRECT
Dialogue: 6,{ts(o_f2)},{ts(o_c)},Cap,,0,0,0,,{{\\fs110\\fscx40\\fscy40\\t(0,110,\\fscx105\\fscy105)\\t(110,180,\\fscx100\\fscy100)}}ET LUI IL SORT\\N{{\\1c{YEL}}}D'OÙ ???
Dialogue: 5,{ts(o_c + 0.8)},{ts(o_c + 3.9)},Cap,,0,0,0,,{{\\fad(100,0)}}BON.\\N{{\\1c{YEL}}}PERSONNE N'A RIEN VU.
Dialogue: 7,{ts(o_c + 4.0)},{ts(TOTAL)},Stamp,,0,0,0,,{{\\pos(540,960)\\frz12\\bord10\\3c{RED}\\1a&HFF&\\fscx300\\fscy300\\alpha&HFF&\\t(0,180,\\fscx100\\fscy100\\alpha&H00&\\1a&HFF&)}}TOURNAGE\\NANNULÉ
"""
ass_path = os.path.join(HERE, "drole.ass")
open(ass_path, "w", encoding="utf-8").write(ass)

n1, n2 = round(F1_LEN * FPS), round(F2_LEN * FPS)
# guy's face sits around (40%, 33%) of the frame at F2_AT
fx, fy, fz = 0.36 * W, 0.30 * H, 1.45
cw, ch = int(W / fz) // 2 * 2, int(H / fz) // 2 * 2
cx = max(0, min(W - cw, int(fx - cw / 2)))
cy = max(0, min(H - ch, int(fy - ch / 2)))

fc = (
    f"[0:v]fps={FPS},scale={W}:{H}:flags=lanczos,setsar=1,"
    f"eq=brightness=0.06:gamma=1.35:contrast=1.08:saturation=1.25,split=5[v1][v2][v3][v4][v5];"
    # A: normal start with a slow push-in
    f"[v1]trim=0:{F1_AT},setpts=PTS-STARTPTS,"
    f"zoompan=z='1+0.06*on/({F1_AT}*{FPS})':d=1:s={W}x{H}:fps={FPS}:"
    f"x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2',setsar=1[A];"
    # freeze 1: crash zoom + red tint + shake
    f"[v2]trim=start={F1_AT}:duration={1 / FPS},setpts=PTS-STARTPTS,loop={n1 - 1}:1:0,"
    f"setpts=N/{FPS}/TB,crop={int(W / 1.4) // 2 * 2}:{int(H / 1.4) // 2 * 2}:"
    f"x='(iw-ow)/2+28*sin(t*70)':y='(ih-oh)/2+28*cos(t*57)',scale={W}:{H},"
    f"colorchannelmixer=rr=1.25:gg=0.75:bb=0.75,setsar=1[F1];"
    # B
    f"[v3]trim={F1_AT}:{F2_AT},setpts=PTS-STARTPTS[B];"
    # freeze 2: zoom on the guy, black & white
    f"[v4]trim=start={F2_AT}:duration={1 / FPS},setpts=PTS-STARTPTS,loop={n2 - 1}:1:0,"
    f"setpts=N/{FPS}/TB,crop={cw}:{ch}:{cx}:{cy},scale={W}:{H},hue=s=0,"
    f"eq=contrast=1.3,setsar=1[F2];"
    # C
    f"[v5]trim={F2_AT}:{END},setpts=PTS-STARTPTS[C];"
    f"[A][F1][B][F2][C]concat=n=5:v=1:a=0,ass={ass_path},format=yuv420p[vout];"
    # audio: music pauses during the freezes, boom on each freeze
    f"[0:a]asplit=3[a1][a2][a3];"
    f"[a1]atrim=0:{F1_AT},asetpts=PTS-STARTPTS[aA];"
    f"[a2]atrim={F1_AT}:{F2_AT},asetpts=PTS-STARTPTS[aB];"
    f"[a3]atrim={F2_AT}:{END},asetpts=PTS-STARTPTS[aC];"
    f"anullsrc=r=48000:cl=stereo,atrim=0:{F1_LEN}[s1];"
    f"anullsrc=r=48000:cl=stereo,atrim=0:{F2_LEN}[s2];"
    f"[aA][s1][aB][s2][aC]concat=n=5:v=0:a=1,aformat=sample_rates=48000:channel_layouts=stereo[music];"
    f"aevalsrc='0.9*sin(2*PI*(45+90*exp(-9*t))*t)*exp(-2.5*t)+0.25*(random(0)-0.5)*exp(-30*t)':"
    f"s=48000:d=1.2,aformat=channel_layouts=stereo,asplit=2[b1][b2];"
    f"[b1]adelay={int(o_f1 * 1000)}:all=1[bb1];"
    f"[b2]adelay={int(o_f2 * 1000)}:all=1[bb2];"
    f"[music][bb1][bb2]amix=inputs=3:normalize=0:duration=first,alimiter=limit=0.95[aout]"
)

subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", SRC, "-filter_complex", fc,
                "-map", "[vout]", "-map", "[aout]",
                "-c:v", "libx264", "-preset", "medium", "-crf", "19",
                "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", OUT], check=True)
print("OK", OUT, f"{TOTAL:.2f}s")
