import time,numpy as np
from PIL import Image
import iclib as L
K='/home/user/Vid-o/work/key/k%d.png'; O='/home/user/Vid-o/work/relit/r%d.png'
S='handsome man, detailed face, '
jobs=[(1,'rim lighting, strong backlight outlining hair and shoulders, dark moody room, cinematic','None'),
(2,'single spotlight from above, pitch black background, dramatic theatre spotlight','Top Light'),
(3,'golden hour, warm orange sunset sunlight through window, cozy room','Right Light'),
(4,'down lighting, light from above head, dark room, moody shadows under eyes','Top Light'),
(5,'hard light, direct harsh sunlight, sharp shadows, bright daylight room','Left Light'),
(6,'side lighting, half of face in deep shadow, dark room, cinematic','Right Light'),
(7,'butterfly lighting, soft beauty light from above front, dark studio background','Top Light'),
(9,'soft cool daylight from large window, natural window light, airy room','Right Light'),
(10,'three point studio lighting, key light, fill light, rim light, dark background, cinematic','None')]
for i,p,bg in jobs:
  t=time.time();img=np.array(Image.open(K%i).convert('RGB'))
  fg,a=L.run_rmbg(img)
  r=L.process(fg,S+p,512,896,1,1000+i,20,'best quality, realistic photo, detailed face','lowres, bad anatomy, worst quality, cartoon',2.0,1.0,0.5,0.9,bg)
  Image.fromarray(r[0]).save(O%i);np.save((O%i).replace('.png','_alpha.npy'),a)
  print('done',i,round(time.time()-t),flush=True)
