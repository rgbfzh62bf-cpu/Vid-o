import sys,cv2,numpy as np,torch,subprocess
from briarmbg import BriaRMBG
torch.set_num_threads(2)
i=int(sys.argv[1]); W='/home/user/Vid-o/work/'
rm=BriaRMBG.from_pretrained(sys.argv[2]).eval()
def mask(rgb):
  f=cv2.resize(rgb,(576,1024),interpolation=cv2.INTER_AREA).astype(np.float32)/127.5-1
  with torch.inference_mode(): a=rm(torch.from_numpy(f).permute(2,0,1)[None])[0][0][0,0].numpy()
  return cv2.resize(a.clip(0,1),(1080,1920),interpolation=cv2.INTER_LINEAR)
key=cv2.imread(W+f'key/k{i}.png')[:,:,::-1].astype(np.float32)
rel=cv2.imread(W+f'relit/r{i}.png')[:,:,::-1]
rel=cv2.resize(rel,(1080,1890),interpolation=cv2.INTER_LANCZOS4)
rel=cv2.copyMakeBorder(rel,15,15,0,0,cv2.BORDER_REPLICATE).astype(np.float32)
ka=mask(key.astype(np.uint8))
m=cv2.GaussianBlur((ka>0.5).astype(np.float32),(0,0),3)
b=lambda x,s:cv2.GaussianBlur(x,(0,0),s)
num=b(rel*m[...,None],7); den=b(key*m[...,None],7); mm=b(m,7)[...,None]+1e-4
G=((num/mm)+4)/((den/mm)+4); G=b(np.clip(G,0.03,4),5)
bg=b(rel,1.2)
ys=np.where(ka.max(1)>0.5)[0]; y0=int(ys[0]); xs=np.where(ka[y0+150]>0.5)[0]; xc=int(xs.mean())
hy0,hy1=max(0,y0-40),min(1920,y0+560); hx0,hx1=max(0,xc-320),min(1080,xc+320)
gray=lambda x:cv2.cvtColor(x.astype(np.uint8),cv2.COLOR_RGB2GRAY)[hy0:hy1,hx0:hx1].astype(np.float32)
kg=gray(key); win=cv2.createHanningWindow(kg.shape[::-1],cv2.CV_32F)
yy=np.arange(1920,dtype=np.float32)[:,None]; wt=np.clip((hy1+150-yy)/300,0,1)[...,None]
sh=np.zeros(2)
import os
LB=float(os.environ.get('LOWBLUR','0'))
GL=b(G,LB) if LB>0 else G
if os.environ.get('LOWFLAT'):
  sel=(m>0.5)&(yy[:,0][:,None]>hy1); GL=np.ones_like(G)*np.median(G[sel],axis=0)
cap=cv2.VideoCapture(W+f'seg/s{i}.mp4')
p=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s','1080x1920','-r','30','-i','-','-c:v','libx264','-crf','16','-preset','medium','-pix_fmt','yuv420p',W+f'out/o{i}.mp4'],stdin=subprocess.PIPE)
prev=None
while True:
  ok,fr=cap.read()
  if not ok: break
  fr=fr[:,:,::-1].astype(np.float32)
  a=mask(fr.astype(np.uint8)); a=a if prev is None else 0.6*a+0.4*prev; prev=a
  (dx,dy),_=cv2.phaseCorrelate(kg,gray(fr),win); d=np.clip([dx,dy],-80,80); sh=0.5*sh+0.5*d
  Gs=cv2.warpAffine(G,np.float32([[1,0,sh[0]],[0,1,sh[1]]]),(1080,1920),borderMode=cv2.BORDER_REPLICATE)
  fg=fr*(wt*Gs+(1-wt)*GL); o=a[...,None]*fg+(1-a[...,None])*bg
  p.stdin.write(np.clip(o,0,255).astype(np.uint8).tobytes())
p.stdin.close();p.wait();print('ok',i)
