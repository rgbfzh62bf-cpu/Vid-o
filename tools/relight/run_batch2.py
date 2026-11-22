import time,numpy as np
from PIL import Image
import iclib as L
K='/home/user/Vid-o/work/key/k%d.png'; O='/home/user/Vid-o/work/relit/r%d_%s.png'
S='handsome man, detailed face, '
N='lowres, bad anatomy, worst quality, cartoon, butterfly, insect, lamp, sun flare'
jobs=[(1,'b','soft light, large softbox in front, even flattering light, dark room','None'),
(1,'c','neon light, pink and blue neon glow, night, cyberpunk','Left Light'),
(2,'b','split lighting, hard light from the right side, half face dark','Right Light'),
(2,'c','blue hour, cool blue twilight light, moody','None'),
(3,'b','candle light, warm flickering low light, dark room','Bottom Light'),
(3,'c','sunset, red orange light from the left, warm','Left Light'),
(4,'b','moonlight, cold blue light from window, night','Right Light'),
(4,'c','top light, overhead hard light, dark background','Top Light'),
(5,'b','teal and orange cinematic grade, warm key light, cool shadows','Left Light'),
(5,'c','low key lighting, dark background, single soft key light','Left Light'),
(6,'b','backlight, strong light behind, glowing hair edges, dark face','None'),
(6,'c','red neon light, red glow, dark room','Right Light'),
(7,'b','loop lighting, soft key light above and to the side, studio','Left Light'),
(7,'c','fireplace light, warm orange glow from the side, cozy','Right Light'),
(8,'b','broad lighting, bright key light on camera side, soft shadows','Left Light'),
(8,'c','silhouette, strong backlight, face mostly in shadow','None'),
(9,'b','studio lighting, clean white key light, professional','None'),
(9,'c','green neon glow, sci-fi light, dark room','Left Light'),
(10,'b','practical lights, warm lamps in the room, cozy evening','Right Light'),
(10,'c','cinematic lighting, dramatic contrast, film look','Left Light')]
for i,t,p,bg in jobs:
  s=time.time();img=np.array(Image.open(K%i).convert('RGB'))
  fg,a=L.run_rmbg(img)
  r=L.process(fg,S+p,512,896,1,2000+i*7+ord(t),20,'best quality, realistic photo, detailed face',N,2.0,1.0,0.5,0.9,bg)
  Image.fromarray(r[0]).save(O%(i,t)); print('done',i,t,round(time.time()-s),flush=True)
