import sys;sys.path.insert(0,'/home/claude/i18n')
import retext as R
from PIL import Image
S='/home/claude/forja-do-heroi-site/img/'
A='/home/claude/forja-do-heroi-site/app/img/ui/'
APP={'dg-ban','boss-ban'}
JOBS={
 'pl-c2':[((368,14,512,38),{'es':'MÁS ELEGIDO','en':'MOST POPULAR'},dict(font='m8',dark=True,align='center',fit_w=140))],
 'alq-d':[
((130,480,240,499),{'es':'BATIDOS','en':'PROTEIN'},dict(font='m8',fit_w=110,size=16)),
((130,502,240,520),{'es':'PROTEICOS','en':'SHAKES'},dict(font='m8',fit_w=110,size=16)),
((514,540,640,559),{'es':'PANQUEQUES','en':'BANANA'},dict(font='m8',fit_w=124,size=16)),
((514,560,640,578),{'es':'CON BANANA','en':'PANCAKES'},dict(font='m8',fit_w=124,size=16)),
((801,542,918,560),{'es':None,'en':'CHOCOLATE'},dict(font='m8',fit_w=116,size=16)),
((801,561,918,579),{'es':None,'en':'MOUSSE'},dict(font='m8',fit_w=116,size=16)),
((177,773,240,791),{'es':'AVENA','en':'OATS'},dict(font='m8',fit_w=62,size=16)),
((400,795,466,813),{'es':'HUEVOS','en':'EGGS'},dict(font='m8',fit_w=64,size=14)),
((613,777,715,797),{'es':'POLLO','en':'CHICKEN'},dict(font='m8',fit_w=100,size=16)),
((613,796,715,814),{'es':'CON ARROZ','en':'& RICE'},dict(font='m8',fit_w=100,size=16)),],
 'featbar':[((150,30,300,70),{'es':'XP inmediato','en':'Instant XP'},dict(font='e6i',fit_w=170,size=22)),
   ((468,30,650,72),{'es':'Misiones diarias','en':'Daily quests'},dict(font='e6i',fit_w=190,size=22)),
   ((810,30,975,72),{'es':'Jefes épicos','en':'Epic bosses'},dict(font='e6i',fit_w=170,size=22))],
 'logo-nav':[((78,18,425,52),{'es':'LA FORJA DEL HÉROE','en':"HERO'S FORGE"},dict(font='m7',fit_w=380,glow=(40,190,255),color=(150,240,255),thr=72,pad=3)),
   ((80,58,285,80),{'es':'E N T R E N A M I E N T O   R P G','en':'R P G   T R A I N I N G'},dict(font='m7',fit_w=215,glow=(40,190,255),color=(90,225,240)))],
 'dg-ban':[((305,340,595,372),{'es':'Elige tu incursión','en':'Choose your raid'},dict(font='e5i',align='center',fit_w=300,size=27))],
 'boss-ban':[((280,125,672,160),{'es':'BATALLAS DE JEFES','en':'BOSS BATTLES'},dict(font='ei',align='center',fit_w=400,grad=((255,236,160),(235,150,35)),glow=(255,170,40))),
   ((228,180,712,206),{'es':'TUS RÉCORDS SE VUELVEN MONSTRUOS','en':'YOUR RECORDS BECOME MONSTERS'},dict(font='m8',align='center',fit_w=480,color=(240,240,250)))],
 'pl-d':[((1214,216,1380,238),{'es':'MÁS ELEGIDO','en':'MOST POPULAR'},dict(font='m8',dark=True,fit_w=150))],
 'rk-d':[((718,609,952,633),{'es':'CAMPEÓN DE LA TEMPORADA','en':'SEASON CHAMPION'},dict(font='m8',dark=True,align='center',fit_w=232))],
 'rk-p1':[((125,426,365,450),{'es':'CAMPEÓN DE LA TEMPORADA','en':'SEASON CHAMPION'},dict(font='m8',dark=True,align='center',fit_w=240))],
}
JOBS['alq-art-m']=[((b[0],b[1]-40,b[2],b[3]-40),t,k) for b,t,k in JOBS['alq-d']]
def run(names=None):
    for n,jobs in JOBS.items():
        if names and n not in names: continue
        for lang in ['es','en']:
            im=Image.open((A if n in APP else S+'v3/')+f'{n}.webp')
            for box,txt,kw in jobs:
                if txt[lang]: im=R.retext(im,box,txt[lang],**kw)
            out=f'/home/claude/forja-do-heroi-site/{lang}/app/img/{n}.webp' if n in APP else S+f'{lang}/{n}.webp'
            import os;os.makedirs(os.path.dirname(out),exist_ok=True);im.save(out,quality=90)
if __name__=='__main__': run(sys.argv[1:] or None)
