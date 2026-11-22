# Clean per-shot lighting looks: global colour temperature, exposure, soft directional gradient.
# No masks, no AI maps -> no halos, blobs or blur. Usage: grade.py <shot> <style>
import sys,subprocess,numpy as np
W='/home/user/Vid-o/work/'; i=int(sys.argv[1]); st=sys.argv[2]
# style: exposure, rgb gains, gradient (dx,dy,strength), vignette strength, gamma
S={'rim':(0.97,(0.92,0.98,1.10),(1,0,0.16),0.14,1.05),
   'side':(1.0,(1.0,1.0,1.0),(-1,0,0.26),0.0,1.03),
   'window':(1.07,(0.95,1.0,1.06),(-1,-0.4,0.16),0.0,0.97),
   'down':(1.0,(1.03,1.0,0.97),(0,-1,0.22),0.0,1.03),
   'butterfly':(1.07,(1.01,1.0,0.99),(0,-0.6,0.08),0.06,0.97),
   'three':(1.05,(1.0,1.0,1.0),(0.6,-0.4,0.07),0.0,1.04),
   'rembrandt':(1.0,(1.08,1.0,0.89),(-1,-0.3,0.24),0.06,1.05),
   'spot':(1.02,(1.0,0.99,0.98),(0,0,0),0.28,1.02),
   'soft':(1.07,(1.02,1.0,0.98),(0,-0.3,0.05),0.0,0.94),
   'golden':(1.04,(1.15,1.03,0.80),(1,-0.4,0.10),0.04,1.0)}[st]
E_,g,(dx,dy,s),v,gam=S
import os,json
SEG=os.environ.get('SEG','seg'); OUT=os.environ.get('OUT','out')
h,w=map(int,subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=height,width','-of','csv=p=0:s=x',W+f'{SEG}/s{i}.mp4']).decode().strip().split('x')[::-1]); y,x=np.mgrid[0:h,0:w].astype(np.float32); xn=(x/w-0.5)*2; yn=(y/h-0.5)*2
n=max(1e-6,(dx*dx+dy*dy)**0.5); M=1-s*(dx*xn+dy*yn)/n*0.5 if s else np.ones_like(xn)
if v: M=M*(1-v*np.clip(((xn/1.3)**2+((yn+0.4)/1.5)**2),0,1))
M=(M*E_)[...,None]*np.float32(g)
lut=lambda a:255*np.clip(a/255,0,1)**gam
r=subprocess.Popen(['ffmpeg','-v','error','-i',W+f'seg/s{i}.mp4','-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE)
p=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{w}x{h}','-r','30','-i','-','-c:v','libx264','-crf','14','-preset','slow','-pix_fmt','yuv420p',W+f'{OUT}/o{i}.mp4'],stdin=subprocess.PIPE)
while True:
  b=r.stdout.read(h*w*3)
  if len(b)<h*w*3: break
  fr=np.frombuffer(b,np.uint8).reshape(h,w,3).astype(np.float32)
  p.stdin.write(np.clip(lut(fr*M),0,255).astype(np.uint8).tobytes())
p.stdin.close();p.wait();print('ok',i,st)
