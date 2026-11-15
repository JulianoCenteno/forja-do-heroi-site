import sys
from PIL import Image
from rembg import remove,new_session
lang=sys.argv[1];R='/home/claude/forja-do-heroi-site/'
src=Image.open(f'/home/claude/i18n/emb-{lang}.png').convert('RGB')
src.resize((1400,933),Image.LANCZOS).save(R+f'img/{lang}/logo-full.webp',quality=90)
import os;os.makedirs(R+f'{lang}/app/img',exist_ok=True)
src.resize((720,480),Image.LANCZOS).save(R+f'{lang}/app/img/logo.webp',quality=90)
o=remove(src,session=new_session('isnet-general-use'))
bb=o.getchannel('A').point(lambda v:255 if v>20 else 0).getbbox();c=o.crop(bb);c.thumbnail((750,747),Image.LANCZOS)
cv=Image.new('RGBA',(750,747),(0,0,0,0));cv.alpha_composite(c,((750-c.width)//2,(747-c.height)//2))
cv.save(R+f'img/{lang}/logo-emblem.webp',quality=90);print('ok',lang)
