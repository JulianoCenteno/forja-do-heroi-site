import cv2,numpy as np
from PIL import Image
R='/home/claude/forja-do-heroi-site'
g=lambda a:cv2.cvtColor(a,cv2.COLOR_RGB2GRAY)
L=lambda p:np.array(Image.open(p).convert('RGB'))
d=L(f'{R}/img/v3/lac-d.webp');m=L(f'{R}/img/v3/lac-m.webp');pt=L('/tmp/lac-pt.png')
s=cv2.SIFT_create(8000)
def H(a,b,ra=None):
    k1,d1=s.detectAndCompute(g(a),ra);k2,d2=s.detectAndCompute(g(b),None)
    mm=[x for x,y in cv2.BFMatcher().knnMatch(d1,d2,k=2) if x.distance<.72*y.distance]
    h,inl=cv2.findHomography(np.float32([k1[x.queryIdx].pt for x in mm]),np.float32([k2[x.trainIdx].pt for x in mm]),cv2.RANSAC,3.0);return h,len(mm),int(inl.sum())
# PT -> desktop (já funcionou), desktop -> mobile (só a área do celular)
mask=np.zeros(d.shape[:2],np.uint8);mask[0:520,1050:1480]=255
Hpd,a1,b1=H(pt,d);Hdm,a2,b2=H(d,m,mask);print(a1,b1,a2,b2)
Hpm=Hdm@Hpd
h,w=pt.shape[:2]
sm=np.zeros((h,w),np.uint8);cv2.rectangle(sm,(0,0),(w,808),255,-1)
def comp(base,Hx,out_name):
    wm=cv2.warpPerspective(sm,Hx,(base.shape[1],base.shape[0]))
    mk=cv2.GaussianBlur(cv2.erode(wm,np.ones((3,3),np.uint8)),(5,5),0).astype(np.float32)[...,None]/255
    # o fim do conteúdo some suavemente (como no original)
    for l in ['es','en']:
        tr=L(f'/tmp/lac-{l}.png');wp=cv2.warpPerspective(tr,Hx,(base.shape[1],base.shape[0]),flags=cv2.INTER_AREA)
        Image.fromarray((wp*mk+base*(1-mk)).astype(np.uint8)).save(f'{R}/img/{l}/{out_name}.webp',quality=90)
src=np.float32([[0,0],[w,0],[w,808],[0,808]])
dst=np.float32([[1060,34],[1428,40],[1392,500],[1034,512]])
Hq=cv2.getPerspectiveTransform(src,dst)
comp(d,Hq,'lac-d');comp(m,Hdm@Hq,'lac-m')
