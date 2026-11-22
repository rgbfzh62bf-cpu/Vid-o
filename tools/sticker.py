# Cut out an object photo with local RMBG-1.4 and add a white sticker outline. Usage: sticker.py in.jpg out.png [crop x0,y0,x1,y1 as fractions]
import sys,cv2,numpy as np,torch,glob
sys.path.insert(0,'/home/user/IC-Light'); from briarmbg import BriaRMBG
rm=BriaRMBG.from_pretrained(glob.glob('/root/.cache/huggingface/hub/models--briaai--RMBG-1.4/snapshots/*')[0]).eval()
im=cv2.imread(sys.argv[1])[:,:,::-1]
if len(sys.argv)>3:
  x0,y0,x1,y1=map(float,sys.argv[3].split(',')); H,W=im.shape[:2]; im=im[int(y0*H):int(y1*H),int(x0*W):int(x1*W)]
H,W=im.shape[:2]; s=1600/max(H,W); im=cv2.resize(im,(int(W*s),int(H*s)),interpolation=cv2.INTER_CUBIC if s>1 else cv2.INTER_AREA); H,W=im.shape[:2]
f=cv2.resize(im,(1024,1024)).astype(np.float32)/127.5-1
with torch.inference_mode(): a=rm(torch.from_numpy(f).permute(2,0,1)[None])[0][0][0,0].numpy()
a=cv2.resize(a.clip(0,1),(W,H)); a=np.where(a>0.5,1.0,a*0.0).astype(np.float32)
n,lab,st,_=cv2.connectedComponentsWithStats((a>0.5).astype(np.uint8))
if n>1:
  keep=[k for k in range(1,n) if st[k,4]>0.04*st[1:,4].max()]; a=a*np.isin(lab,keep)
a=cv2.GaussianBlur(a,(0,0),1.2)
P=60; im=cv2.copyMakeBorder(im,P,P,P,P,cv2.BORDER_CONSTANT,value=(255,255,255)); a=cv2.copyMakeBorder(a,P,P,P,P,cv2.BORDER_CONSTANT,value=0)
R=26; k=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(2*R+1,2*R+1))
o=cv2.GaussianBlur(cv2.dilate((a>0.3).astype(np.float32),k),(0,0),1.5)
rgb=im.astype(np.float32)*a[...,None]+255*(1-a[...,None]); al=np.maximum(a,o)
ys,xs=np.where(al>0.02); y0,y1,x0,x1=ys.min(),ys.max()+1,xs.min(),xs.max()+1
out=np.dstack([rgb,al*255]).clip(0,255).astype(np.uint8)[y0:y1,x0:x1]
cv2.imwrite(sys.argv[2],cv2.cvtColor(out,cv2.COLOR_RGBA2BGRA)); print('ok',sys.argv[2],out.shape)
