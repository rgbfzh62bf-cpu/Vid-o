from gradio_client import Client
import shutil, sys, json
c=Client("https://black-forest-labs-flux-1-schnell.hf.space", headers={"Authorization":"Bearer proxy-injected"}, verbose=False)
B="Semi-realistic anatomy fitness illustration of a lean athletic young man in his twenties with light olive tanned skin, voluminous dark brown curly hair, curls on top with shorter sides, short dark beard, lean defined muscles with visible abs, defined chest and round shoulders, wearing only plain heather grey athletic shorts, barefoot. Pure white background, entire body visible from head to feet with margin, centered, soft studio lighting, clean digital painting, no text, no logo. Pose: "
P=json.load(open(sys.argv[1]))
for name,pose,seeds in P:
    for s in seeds:
        try:
            r=c.predict(prompt=B+pose,seed=s,randomize_seed=False,width=768,height=1344,num_inference_steps=4,api_name="/infer")
            shutil.copy(r[0],f"{name}_{s}.webp"); print("ok",name,s,flush=True)
        except Exception as e: print("ERR",name,s,str(e)[:150],flush=True)
