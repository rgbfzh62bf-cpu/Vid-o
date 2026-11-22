import time,numpy as np
from PIL import Image
import iclib as L
K='/home/user/Vid-o/work/key/k%d.png'; O='/home/user/Vid-o/work/relit/r%d_%s.png'
S='handsome man, detailed face, '
N='lowres, bad anatomy, worst quality, cartoon, butterfly, insect, lamp, sun flare, neon, colorful lights, pink light, green light, purple light'
jobs=[(1, 'c', 'hard light, direct harsh light, crisp shadows, neutral daylight', 'Left Light'),(2, 'c', 'golden hour, warm low sunlight from the side, warm tones', 'Right Light'),(3, 'b', 'soft natural daylight from a window on the side, neutral', 'Right Light'),(3, 'c', 'rembrandt lighting, warm key light from upper left, dark background, cinematic', 'Left Light'),(4, 'b', 'soft light, large diffused key light in front, even flattering light, neutral white', 'None'),(4, 'c', 'single spotlight from above on the face, dark surroundings', 'Top Light'),(5, 'b', 'rim lighting, backlight outlining hair and shoulders, soft fill on face, dark room', 'None'),(5, 'c', 'beauty dish light above camera, soft shadow under nose and chin, symmetrical frontal top light', 'Top Light'),(6, 'b', 'three point studio lighting, key light, fill light, rim light, neutral tones', 'None'),(6, 'c', 'warm light glowing up from the table below, underlighting on hands and face, dark room', 'Bottom Light'),(7, 'b', 'rembrandt lighting, warm key light from upper left, dark background, cinematic', 'Left Light'),(7, 'c', 'golden hour, warm low sunlight from the side, warm tones', 'Right Light'),(8, 'b', 'soft natural daylight from a window on the side, neutral', 'Right Light'),(8, 'c', 'single spotlight from above on the face, dark surroundings', 'Top Light'),(9, 'b', 'side lighting, hard light from the right, half of face in shadow', 'Right Light'),(9, 'c', 'soft light, large diffused key light in front, even flattering light, neutral white', 'None'),(10, 'b', 'rim lighting, backlight outlining hair and shoulders, soft fill on face, dark room', 'None'),(10, 'c', 'golden hour, warm low sunlight from the side, warm tones', 'Right Light')]
for i,t,p,bg in jobs:
  s=time.time();img=np.array(Image.open(K%i).convert('RGB'))
  fg,a=L.run_rmbg(img)
  r=L.process(fg,S+p,512,896,1,2000+i*7+ord(t),20,'best quality, realistic photo, detailed face',N,2.0,1.0,0.5,0.9,bg)
  Image.fromarray(r[0]).save(O%(i,t)); print('done',i,t,round(time.time()-s),flush=True)
