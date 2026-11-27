"""Original lo-fi bed for face-cam DA (generated, no third-party samples)."""
import numpy as np, soundfile as sf, subprocess
SR=48000; BPM=84; B=60/BPM; DUR=40.0
t=np.arange(int(SR*DUR))/SR; out=np.zeros((len(t),2))
def note(f,start,dur,amp,pan=0.0):
    n=int(dur*SR); s=int(start*SR)
    if s>=len(t): return
    n=min(n,len(t)-s); tt=np.arange(n)/SR
    env=np.minimum(1,tt/0.02)*np.exp(-tt*1.6)
    w=(np.sin(2*np.pi*f*tt)+0.35*np.sin(2*np.pi*2*f*tt)*np.exp(-tt*4)+0.12*np.sin(2*np.pi*3*f*tt)*np.exp(-tt*6))
    w*=env*amp*(1+0.003*np.sin(2*np.pi*5*tt))
    out[s:s+n,0]+=w*(1-pan)*0.5*2**0.5; out[s:s+n,1]+=w*(1+pan)*0.5*2**0.5
m=lambda x:440*2**((x-69)/12)
chords=[[53,57,60,64],[52,55,59,62],[50,53,57,60],[48,52,55,59]]  # Fmaj7 Em7 Dm7 Cmaj7
bass=[41,40,38,36]
bar=4*B; k=0; st=0.0
while st<DUR:
    c=chords[k%4]
    for j,x in enumerate(c): note(m(x),st+0.012*j,bar*1.1,0.09,pan=(j-1.5)*0.25)
    note(m(c[-1]+12),st+2*B+0.5*B,B*1.5,0.04,0.3)
    note(m(bass[k%4]),st,bar*0.9,0.13); note(m(bass[k%4]),st+2.5*B,B*1.2,0.08)
    for q in range(4):  # soft kick on 1,3 ; shaker on offbeats
        s=int((st+q*B)*SR)
        if s>=len(t): break
        if q in (0,2):
            n=int(0.25*SR); tt=np.arange(min(n,len(t)-s))/SR
            kk=np.sin(2*np.pi*(50+70*np.exp(-tt*30))*tt)*np.exp(-tt*14)*0.28; out[s:s+len(kk)]+=kk[:,None]
        s2=int((st+q*B+B/2)*SR)
        if s2<len(t):
            rng=np.random.default_rng(k*10+q); n=min(int(0.06*SR),len(t)-s2)
            hh=rng.standard_normal(n)*np.exp(-np.arange(n)/SR*60)*0.035; out[s2:s2+n]+=hh[:,None]
    st+=bar; k+=1
out/=np.abs(out).max()*1.1
sf.write("assets/music/_bed_raw.wav",out,SR)
subprocess.run(["ffmpeg","-loglevel","error","-y","-i","assets/music/_bed_raw.wav","-af","lowpass=f=3200,aecho=0.8:0.5:60|120:0.25|0.15,afade=t=in:d=1.0,afade=t=out:st=37.2:d=1.5,loudnorm=I=-18","-ar","48000","assets/music/lofi.mp3"],check=True)
