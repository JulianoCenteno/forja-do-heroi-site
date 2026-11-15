import cv2,numpy as np,sys
from PIL import Image
R='/home/claude/forja-do-heroi-site/img/'
d=np.array(Image.open(R+'v3/gar-d.webp').convert('RGB')).astype(np.float32)
b0=Image.open(R+'v3/gar-badge.webp').convert('RGBA')
best=None
for s in np.arange(0.80,1.10,0.01):
    w,h=int(710*s),int(760*s)
    t=np.array(b0.resize((w,h)).convert('RGB')).astype(np.float32)
    # só a região central (texto/escudo), menos afetada pelo fundo
    tc=t[int(h*.2):int(h*.8),int(w*.2):int(w*.8)]
    r=cv2.matchTemplate(d[:,:1000],tc,cv2.TM_CCOEFF_NORMED);_,mx,_,loc=cv2.minMaxLoc(r)
    if not best or mx>best[0]: best=(mx,s,loc[0]-int(w*.2),loc[1]-int(h*.2))
print(best)
mx,s,x,y=best
for lang in sys.argv[1:]:
    b=Image.open(R+f'{lang}/gar-badge.webp').convert('RGBA')
    # diferença entre o selo traduzido e o original: só cola onde mudou
    diff=np.abs(np.array(b).astype(int)-np.array(b0).astype(int)).sum(axis=2)
    m=(diff>30).astype(np.uint8)*255
    m=cv2.dilate(m,np.ones((5,5),np.uint8),iterations=3);m=cv2.GaussianBlur(m,(9,9),0)
    w,h=int(710*s),int(760*s)
    bs=b.resize((w,h),Image.LANCZOS);ms=Image.fromarray(m).resize((w,h))
    out=Image.open(R+'v3/gar-d.webp').convert('RGB');out.paste(bs.convert('RGB'),(x,y),ms)
    out.save(R+f'{lang}/gar-d.webp',quality=90);print('ok',lang)
