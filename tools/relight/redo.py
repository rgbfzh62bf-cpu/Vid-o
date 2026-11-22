import sys,numpy as np
from PIL import Image
import iclib as L
i=int(sys.argv[1]);p=sys.argv[2];bg=sys.argv[3];seed=int(sys.argv[4])
img=np.array(Image.open(f'/home/user/Vid-o/work/key/k{i}.png').convert('RGB'))
fg,a=L.run_rmbg(img)
r=L.process(fg,'handsome man, detailed face, '+p,512,896,1,seed,20,'best quality, realistic photo, detailed face','lowres, bad anatomy, worst quality, cartoon, butterfly, insect, lamp, sun flare',2.0,1.0,0.5,0.9,bg)
Image.fromarray(r[0]).save(f'/home/user/Vid-o/work/relit/r{i}.png');print('done',i)
