import json,glob,re,os,asyncio,html
from html.parser import HTMLParser
S=json.load(open('strings.json'))
NAMES={'es':['01 - Grimorio de la Alimentacion del Heroe','02 - Misiones Relampago','03 - Pergamino de la Regeneracion','04 - Diario del Cazador 90 Dias','05 - BONO Protocolo Despertar 7 Dias'],
       'en':["01 - The Hero's Nutrition Grimoire",'02 - Lightning Quests','03 - Scroll of Regeneration',"04 - Hunter's Journal 90 Days",'05 - BONUS 7-Day Awakening Protocol']}
BRAND={'es':'LA FORJA DEL HÉROE','en':"HERO'S FORGE"}
def D(col):
    d={}
    for f in sorted(glob.glob('tr_*.tsv')):
        for ln in open(f,encoding='utf-8'):
            p=ln.rstrip('\n').split('\t')
            if len(p)<3 or not p[0].isdigit(): continue
            d[S[int(p[0])]]=p[col]
    return d
def tr_text(t,d,lang):
    s=t.strip()
    if not s: return t
    if s in d: r=d[s]
    elif s=='FORJA DO HERÓI': r=BRAND[lang]
    elif m:=re.fullmatch(r'FORJA DO HERÓI · (\d+)',s): r=BRAND[lang]+' · '+m.group(1)
    elif m:=re.fullmatch(r'Dia (\d+)',s): r=('Día ' if lang=='es' else 'Day ')+m.group(1)
    elif m:=re.fullmatch(r'Semana (\d+)',s): r=('Semana ' if lang=='es' else 'Week ')+m.group(1)
    else: return t
    lead=t[:len(t)-len(t.lstrip())];trail=t[len(t.rstrip()):]
    return lead+html.escape(r,quote=False)+trail
for lang,col in (('es',1),('en',2)):
    d=D(col);os.makedirs(f'out/{lang}',exist_ok=True)
    for i in range(1,6):
        src=open(f'/home/claude/bumps/out/p{i}.html',encoding='utf-8').read()
        head,body=src.split('<body>',1)
        body=re.sub(r'>([^<>]+)<',lambda m:'>'+tr_text(html.unescape(m.group(1)),d,lang)+'<',body)
        head=re.sub(r'<title>(.*?)</title>',lambda m:'<title>'+tr_text(html.unescape(m.group(1)),d,lang)+'</title>',head)
        head=head.replace('lang="pt-BR"',f'lang="{lang}"')
        open(f'out/{lang}/p{i}.html','w',encoding='utf-8').write(head+'<body>'+body)
    print(lang,'html ok')
from playwright.async_api import async_playwright
async def pdf():
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox','--allow-file-access-from-files'])
    for lang in ('es','en'):
      os.makedirs(f'pdf/{lang}',exist_ok=True)
      for i in range(1,6):
        pg=await b.new_page();await pg.goto(f'file:///home/claude/i18n/bumps/out/{lang}/p{i}.html',wait_until='networkidle');await pg.wait_for_timeout(500)
        await pg.pdf(path=f'pdf/{lang}/{NAMES[lang][i-1]}.pdf',print_background=True,prefer_css_page_size=True)
        ov=await pg.evaluate("[...document.querySelectorAll('.pg')].map((p,i)=>{const r=p.getBoundingClientRect();let m=0;p.querySelectorAll('*').forEach(e=>{if(e.closest('.foot')||e.closest('.art'))return;const b=e.getBoundingClientRect();if(b.bottom-r.top>m)m=b.bottom-r.top});return [i+1,Math.round(m),Math.round(r.height)]}).filter(x=>x[1]>x[2]-38)")
        left=await pg.evaluate("(()=>{const out=[];const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);let n;while(n=w.nextNode()){const v=n.nodeValue.trim();if(/[ãõçêâ]|\\b(você|não|do|da|treino|missão)\\b/i.test(v))out.push(v)}return out.slice(0,5)})()")
        print(lang,i,'overflow',ov,'PT left',left);await pg.close()
    await b.close()
asyncio.run(pdf())
