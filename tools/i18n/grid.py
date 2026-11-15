import sys
from PIL import Image,ImageDraw
f,x0,y0,x1,y1,sc,out=sys.argv[1],*map(int,sys.argv[2:7]),sys.argv[7]
im=Image.open(f).convert('RGB').crop((x0,y0,x1,y1));im=im.resize((im.width*sc,im.height*sc))
d=ImageDraw.Draw(im)
for y in range(0,im.height,10*sc): d.line([(0,y),(6,y)],fill='red'); d.text((8,y-5),str(y0+y//sc),fill='red')
for x in range(0,im.width,20*sc): d.line([(x,0),(x,6)],fill='yellow'); d.text((x,8),str(x0+x//sc),fill='yellow')
im.save(out)
