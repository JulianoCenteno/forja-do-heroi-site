import re,os,sys
sys.path.insert(0,os.path.dirname(__file__))
from site_tr import T
R='/home/claude/forja-do-heroi-site'
src=open(f'{R}/index.html').read()
CFG={
 'es':"""<script>window.FH={cur:'USD',name:'La Forja del Heroe',brand:'La Forja del Héroe',playing:'Reproduciendo',track:'Banda sonora',num:'es',price:{recruta:4.9,elite:9.9,popup:6.9},
 checkout:{recruta:'https://appdigitalhub.com.br/c/ES_RECLUTA',elite:'https://appdigitalhub.com.br/c/ES_ELITE',elitePopup:'https://appdigitalhub.com.br/c/ES_ELITE_POPUP'}};</script>""",
 'en':"""<script>window.FH={cur:'USD',name:'Heros Forge',brand:"Hero's Forge",playing:'Now playing',track:'Soundtrack',num:'en-US',price:{recruta:7.99,elite:14.99,popup:10.99},
 checkout:{recruta:'https://appdigitalhub.com.br/c/EN_RECRUIT',elite:'https://appdigitalhub.com.br/c/EN_ELITE',elitePopup:'https://appdigitalhub.com.br/c/EN_ELITE_POPUP'}};</script>"""}
FIT='''<script>/* textos traduzidos dentro de pílulas, placas e botões: reduz a letra até caber (mesma proporção do PT) */
(function(){const C=[['.lx-pill2 span','C',.37],['.sx-pill span','C',.80],['.sx-lb span','R',.885],['.p-pill span','C',.82],['.g-pill span','C',.74],['.f-pill span','C',.82],['.k-pill span','R',.91],['.ibtn span','C',.70]];
const tw=e=>{const r=document.createRange();r.selectNodeContents(e);return r.getBoundingClientRect()};
function run(){C.forEach(([sel,m,k])=>document.querySelectorAll(sel).forEach(el=>{const p=el.parentElement;el.style.fontSize='';
 let fs=parseFloat(getComputedStyle(el).fontSize),i=0;const ok=()=>{const q=p.getBoundingClientRect();if(!q.width)return true;const r=tw(el);return m==='C'?r.width<=q.width*k:(r.right-q.left)<=q.width*k};
 while(!ok()&&fs>8&&i++<60){fs*=.96;el.style.fontSize=fs+'px'}}));
 ['.sx-lb span'].forEach(sel=>{const L=[...document.querySelectorAll(sel)].filter(e=>e.offsetParent);const mn=Math.min(...L.map(e=>parseFloat(getComputedStyle(e).fontSize)));L.forEach(e=>e.style.fontSize=mn+'px')});
 document.querySelectorAll('.hx-feat.m').forEach(box=>{const sp=[...box.querySelectorAll('span')];sp.forEach(e=>e.style.fontSize='');let fs=parseFloat(getComputedStyle(sp[0]).fontSize),i=0;
  const over=()=>box.scrollWidth>box.clientWidth+1||sp.some(e=>e.scrollWidth>e.clientWidth+1);while(over()&&fs>8&&i++<40){fs*=.95;sp.forEach(e=>e.style.fontSize=fs+'px')}})}
addEventListener('load',run);addEventListener('resize',()=>{clearTimeout(window.__f2);window.__f2=setTimeout(run,150)});document.fonts&&document.fonts.ready.then(run)})();</script>
<script>/* encaixa títulos longos (ES/EN) na largura da tela */
(function(){const sel='.hx-h1 .l1,.hx-h1 .l2 b,.lx-h span,.sx-h,.cx-h,.ap-h span,.k-h,.tx-h,.p-h,.f-h';
function fit(){document.querySelectorAll(sel).forEach(el=>{el.style.fontSize='';if(innerWidth>=760)return;const max=Math.min(el.parentElement.clientWidth,innerWidth-44);let fs=parseFloat(getComputedStyle(el).fontSize),i=0;
 el.style.whiteSpace=el.style.whiteSpace||'';const W=()=>Math.max(el.scrollWidth,el.getBoundingClientRect().width);while(W()>max&&fs>12&&i++<40){fs*=0.95;el.style.fontSize=fs+'px'}})}
addEventListener('load',fit);addEventListener('resize',()=>{clearTimeout(window.__ft);window.__ft=setTimeout(fit,150)});document.fonts&&document.fonts.ready.then(fit)})();</script>
'''
for li,lang in ((1,'es'),(2,'en')):
    s=src;miss=[]
    for row in T:
        pt,tr=row[0],row[li]
        if pt not in s: miss.append(pt[:70]);continue
        s=s.replace(pt,tr)
    if miss: print(lang,'MISSING',*miss,sep='\n  ')
    # caminhos absolutos + imagens localizadas quando existirem em /img/<lang>/
    def fix(m):
        attr,path=m.group(1),m.group(2)
        loc=f'img/{lang}/'+os.path.basename(path)
        if path.startswith('img/') and os.path.exists(f'{R}/{loc}'): path=loc
        return f'{attr}="/{path}'
    s=re.sub(r'(src|href|srcset)="((?:img/|app/)[^"]*|[a-z]+\.(?:css|js)[^"]*)',fix,s)
    s=s.replace('<script src="/site.js',CFG[lang]+'\n'+FIT+'<script src="/site.js')
    # checkout links estáticos (o JS também sobrescreve)
    alt='<link rel="alternate" hreflang="pt-BR" href="https://forjadoheroi.com/"><link rel="alternate" hreflang="es" href="https://forjadoheroi.com/es/"><link rel="alternate" hreflang="en" href="https://forjadoheroi.com/en/">'
    s=s.replace('<meta name="theme-color"',alt+'\n<meta name="theme-color"')
    s=s.replace('content="https://forjadoheroi.com/img/v2/logo-full.webp"',f'content="https://forjadoheroi.com/img/{lang}/logo-full.webp"' if os.path.exists(f'{R}/img/{lang}/logo-full.webp') else 'content="https://forjadoheroi.com/img/v2/logo-full.webp"')
    s=re.sub(r'<span><svg viewBox="0 0 24 24" fill="#32bcad">.*?</svg>pix</span>','',s)
    os.makedirs(f'{R}/{lang}',exist_ok=True)
    open(f'{R}/{lang}/index.html','w').write(s)
    # sobras em português
    left=[w for w in ['ção','ões','você','Herói','Forja do','R$','Caçador','Treino','Missões'] if w in re.sub(r'<script.*?</script>','',s,flags=re.S)]
    print(lang,'ok; restos PT:',left)
