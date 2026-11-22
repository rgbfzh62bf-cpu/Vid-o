import sys,time,numpy as np
from PIL import Image
import iclib as L
src,out,prompt,bg,seed=sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],int(sys.argv[5])
W,H=512,896
img=np.array(Image.open(src).convert('RGB'))
t=time.time()
fg,alpha=L.run_rmbg(img)
res=L.process(fg,prompt,W,H,1,seed,int(sys.argv[6]) if len(sys.argv)>6 else 20,'best quality, realistic photo, detailed face','lowres, bad anatomy, worst quality, cartoon',2.0,1.0,0.5,0.9,bg)
Image.fromarray(res[0]).save(out)
np.save(out.replace('.png','_alpha.npy'),alpha)
print('done',round(time.time()-t),'s')
