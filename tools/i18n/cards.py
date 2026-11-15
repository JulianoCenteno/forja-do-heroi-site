import sys;sys.path.insert(0,'/home/claude/i18n')
import retext as R
import numpy as np
from PIL import Image
SRC='/home/claude/forja-do-heroi-site/img/v3/'
STATS={'es':['FUERZA','RESISTENCIA','AGILIDAD'],'en':['STRENGTH','ENDURANCE','AGILITY']}
CARDS={
 'monge':dict(title=(90,255,460,298),pill=(232,308,335,338),
   es=('MONJE DE LAS BARRAS','Calistenia'),en=('BAR MONK','Calisthenics')),
 'guerreiro':dict(title=(65,255,460,298),pill=(230,310,338,342),
   es=('GUERRERO DEL HIERRO','Gimnasio'),en=('IRON WARRIOR','Weightlifting')),
 'paladino':dict(title=(70,280,490,322),pill=(262,335,345,360),
   es=('PALADÍN HÍBRIDO','Híbrido'),en=('HYBRID PALADIN','Hybrid')),
}
def rows(img):
    a=np.array(img.convert('RGB')).astype(float)[355:520,105:232].mean(axis=2)
    m=(a>150).sum(axis=1)>2
    out=[];y=None
    for i,v in enumerate(m):
        if v and y is None:y=i
        if not v and y is not None:
            if i-y>8:out.append((355+y,355+i))
            y=None
    return out
for c,cfg in CARDS.items():
    for lang in ['es','en']:
        im=Image.open(SRC+f'cls-card-{c}.webp')
        rs=rows(im)
        t,p=cfg[lang]
        im=R.retext(im,cfg['title'],t,font='mi',align='center',fit_w=cfg['title'][2]-cfg['title'][0]-10)
        im=R.retext(im,cfg['pill'],p,font='ei',align='center',fit_w=118,size=19)
        # tamanho dos stats a partir de AGILIDADE (sem acento)
        a0,a1=rs[2]
        _=R.retext(im,(105,a0-3,232,a1+3),STATS[lang][2],font='e7'); fs=R.LAST_FS
        for (y0,y1),s in zip(rs[:3],STATS[lang]):
            im=R.retext(im,(105,y0-3,232,y1+3),s,font='e7',size=fs,fit_w=120)
        import os;os.makedirs(f'/home/claude/forja-do-heroi-site/img/{lang}',exist_ok=True)
        im.save(f'/home/claude/forja-do-heroi-site/img/{lang}/cls-card-{c}.webp',quality=90)
        print(c,lang,rs)
