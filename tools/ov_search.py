import sys,json,urllib.request,urllib.parse,os
q=sys.argv[1]; tag=sys.argv[2]
u="https://api.openverse.org/v1/images/?"+urllib.parse.urlencode({"q":q,"license_type":"commercial,modification","page_size":8,"extension":"jpg,png",**({"source":sys.argv[3]} if len(sys.argv)>3 else {})})
d=json.load(urllib.request.urlopen(urllib.request.Request(u,headers={"User-Agent":"video-tool"}),timeout=30))
out=[]
for k,r in enumerate(d.get("results",[])):
  out.append({"k":k,"id":r["id"],"title":r["title"],"url":r["url"],"thumb":r["thumbnail"],"lic":r["license"],"creator":r.get("creator"),"w":r.get("width"),"h":r.get("height"),"src":r.get("source")})
json.dump(out,open(f"{tag}.json","w"),indent=1)
for r in out: print(tag,r["k"],r["lic"],r["w"],r["h"],r["src"],r["title"][:50])
