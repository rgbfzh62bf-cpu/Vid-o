import sys,os,cv2,numpy as np,torch,subprocess
from briarmbg import BriaRMBG
torch.set_num_threads(4)
i=int(sys.argv[1]); W='/home/user/Vid-o/work/'
rm=BriaRMBG.from_pretrained(sys.argv[2]).eval()
def mask(rgb):
  f=cv2.resize(rgb,(576,1024),interpolation=cv2.INTER_AREA).astype(np.float32)/127.5-1
  with torch.inference_mode(): a=rm(torch.from_numpy(f).permute(2,0,1)[None])[0][0][0,0].numpy()
  return cv2.resize(a.clip(0,1),(1080,1920),interpolation=cv2.INTER_LINEAR)
b=lambda x,s:cv2.GaussianBlur(x,(0,0),s)
key=cv2.imread(W+f'key/k{i}.png')[:,:,::-1].astype(np.float32)
ka=mask(key.astype(np.uint8)); m=b((ka>0.5).astype(np.float32),3); n=1-m
def load(path):
  rel=cv2.imread(path)[:,:,::-1]
  return cv2.copyMakeBorder(cv2.resize(rel,(1080,1890),interpolation=cv2.INTER_LANCZOS4),15,15,0,0,cv2.BORDER_REPLICATE).astype(np.float32)
def ratio(rel,w,s):
  num=b(rel*w[...,None],s); den=b(key*w[...,None],s); ww=b(w,s)[...,None]+1e-4
  return np.clip(((num/ww)+4)/((den/ww)+4),0.03,3.5)
ys=np.where(ka.max(1)>0.5)[0]; y0=int(ys[0]); xc=int(np.where(ka[y0+150]>0.5)[0].mean())
hy0,hy1=max(0,y0-40),min(1920,y0+560); hx0,hx1=max(0,xc-320),min(1080,xc+320)
gray=lambda x:cv2.cvtColor(x.astype(np.uint8),cv2.COLOR_RGB2GRAY)[hy0:hy1,hx0:hx1].astype(np.float32)
kg=gray(key); win=cv2.createHanningWindow(kg.shape[::-1],cv2.CV_32F)
yy=np.arange(1920,dtype=np.float32)[:,None]; wt=np.clip((hy1+150-yy)/300,0,1)[...,None]
maps=[]
for suf in ['','_b','_c']:
  rel=load(W+f'relit/r{i}{suf}.png'); PS=float(os.environ.get('PS','22')); Gp=np.clip(b(ratio(rel,m,PS),PS*0.7),0.3,2.4); Gb=b(ratio(rel,n,60),40)
  CH=float(os.environ.get('CH','0.4')); neu=lambda G:(G.mean(2,keepdims=True)*(1-CH)+G*CH)
  Gp=neu(Gp); Gb=neu(Gb); GL=Gp
  if os.environ.get('LOWFLAT'):
    sel=(m>0.5)&(yy[:,0][:,None]>hy1); GL=np.ones_like(Gp)*np.median(Gp[sel],axis=0)
  maps.append((Gp,Gb,GL))
nf=int(cv2.VideoCapture(W+f'seg/s{i}.mp4').get(cv2.CAP_PROP_FRAME_COUNT)); cuts=[round(nf/3),round(2*nf/3)]; k=0
sh=np.zeros(2); prev=None
cap=cv2.VideoCapture(W+f'seg/s{i}.mp4')
p=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s','1080x1920','-r','30','-i','-','-c:v','libx264','-crf','14','-preset','slow','-pix_fmt','yuv420p',W+f'out/o{i}.mp4'],stdin=subprocess.PIPE)
while True:
  ok,fr=cap.read()
  if not ok: break
  fr=fr[:,:,::-1].astype(np.float32)
  Gp,Gb,GL=maps[sum(k>=c for c in cuts)]; k+=1
  a=mask(fr.astype(np.uint8)); a=a if prev is None else 0.8*a+0.2*prev; prev=a; a=b(a,4)[...,None]
  (dx,dy),_=cv2.phaseCorrelate(kg,gray(fr),win); sh=0.5*sh+0.5*np.clip([dx,dy],-80,80)
  Gs=cv2.warpAffine(Gp,np.float32([[1,0,sh[0]],[0,1,sh[1]]]),(1080,1920),borderMode=cv2.BORDER_REPLICATE)
  G=a*(wt*Gs+(1-wt)*GL)+(1-a)*Gb
  p.stdin.write(np.clip(fr*G,0,255).astype(np.uint8).tobytes())
p.stdin.close();p.wait();print('ok',i)
