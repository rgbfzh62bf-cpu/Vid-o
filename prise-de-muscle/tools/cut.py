import subprocess,sys,math
src,out=sys.argv[1],sys.argv[2]
seg=[(5.86,6.63),(7.41,8.38),(9.08,9.87),(10.62,11.45),(12.01,13.00),(13.60,14.51),(15.17,16.05),(16.73,17.75),(18.32,19.15)]
pre,post=0.07,0.12
fr=1/30
parts=[]
for i,(a,b) in enumerate(seg):
    a=max(0,a-pre); b=b+post
    n=round((b-a)/fr); d=n*fr
    p=f"p{i}.mp4"; parts.append((p,d))
    subprocess.run(["ffmpeg","-v","error","-y","-ss",f"{a:.4f}","-i",src,"-t",f"{d:.4f}",
      "-vf","scale=1080:1920:flags=lanczos,fps=30","-af",f"apad,atrim=0:{d:.4f},afade=t=in:d=0.01,afade=t=out:st={d-0.015:.4f}:d=0.015",
      "-c:v","libx264","-crf","14","-preset","fast","-pix_fmt","yuv420p","-c:a","pcm_s16le","-ar","48000",p.replace('.mp4','.mov')],check=True)
open("list.txt","w").write("".join(f"file '{p.replace('.mp4','.mov')}'\n" for p,_ in parts))
subprocess.run(["ffmpeg","-v","error","-y","-f","concat","-i","list.txt","-c:v","copy","-af","loudnorm=I=-14:TP=-1.5:LRA=7","-c:a","aac","-b:a","192k","-ar","48000",out],check=True)
t=0
for i,(p,d) in enumerate(parts): print(i,round(t,3),round(d,3)); t+=d
print("total",round(t,3))
