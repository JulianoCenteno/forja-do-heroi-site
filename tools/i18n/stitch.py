import sys
from PIL import Image
# uso: stitch.py out W_orig H_orig tile0 tile05 tile1   (tiles de 549px, offsets 0, 274.5, 549)
out,W,H,t0,t5,t1=sys.argv[1],int(sys.argv[2]),int(sys.argv[3]),*sys.argv[4:7]
a,b,c=[Image.open(t).convert('RGB') for t in (t0,t5,t1)]
TH=round(1568*H/W)
s=Image.new('RGB',(1568,TH))
s.paste(a.crop((0,0,1568,500)),(0,0))
o=274.5
s.paste(b.crop((0,round(500-o),1568,round(800-o))),(0,500))
s.paste(c.crop((0,800-549,1568,min(549,TH-549))),(0,800))
s.save(out);print(s.size)
