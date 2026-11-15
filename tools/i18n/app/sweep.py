import asyncio, json, time, subprocess, sys
from playwright.async_api import async_playwright
st=json.load(open('/home/claude/tav/state.json'))
LANGS=sys.argv[1:] or ['es','en']
VIEWS=['heroi','treinar','dungeon','missoes','chefes','taverna','mais','loja','diario','temporada','progressao','planilha','alquimia','mestres','corrida']
MODALS=["settingsSheet()","exerciseSheet('flexao')","exerciseSheet('prancha')","exerciseSheet('supino')","levelModal(5,true)","bossModal(BOSSES[0],100)","S.nov1=0;S.nov2=0;novModal&&novModal()","eliteModal&&eliteModal()","horaSheet&&horaSheet()","avSheet&&avSheet()","duelNew&&duelNew()","installSheet&&installSheet()"]
async def main():
    srv=subprocess.Popen(['python3','-m','http.server','8783','-d','/home/claude/forja-do-heroi-site'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);time.sleep(1)
    left={}
    try:
      async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        for lang in LANGS:
          for plan in ['elite','recruta']:
            ctx=await b.new_context(viewport={'width':392,'height':760})
            pg=await ctx.new_page()
            errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
            await pg.add_init_script(f"localStorage.setItem('forja_heroi_v1', {json.dumps(json.dumps(st))});localStorage.setItem('fh_install_hide','1');")
            await pg.route('https://fonts.googleapis.com/**',lambda r:r.fulfill(body=open('/home/claude/fonts.css').read(),content_type='text/css'))
            await pg.goto(f'http://localhost:8783/{lang}/app/',wait_until='domcontentloaded');await pg.wait_for_timeout(2500)
            await pg.evaluate(f"window.__FH_PLAN='{plan}';try{{SFX.on=false}}catch(e){{}}")
            S=set()
            for v in VIEWS:
                try:
                    await pg.evaluate(f"closeModal();tab='{v}';render();scrollTo(0,0)");await pg.wait_for_timeout(350)
                    for x in await pg.evaluate("__FH_PT_LEFT()"): S.add((v,x))
                    if plan=='elite': await pg.screenshot(path=f'/tmp/sw-{lang}-{v}.png',full_page=True)
                except Exception as e: errs.append(v+': '+str(e)[:100])
            for m in MODALS:
                try:
                    await pg.evaluate(f"try{{{m}}}catch(e){{}}");await pg.wait_for_timeout(300)
                    for x in await pg.evaluate("__FH_PT_LEFT()"): S.add(('modal '+m[:20],x))
                    await pg.evaluate("closeModal()")
                except Exception as e: errs.append(m+': '+str(e)[:100])
            left[(lang,plan)]=S
            print(lang,plan,'errors',errs[:5])
            await ctx.close()
        await b.close()
    finally: srv.terminate()
    allv={}
    for k,S in left.items():
        for v,x in S: allv.setdefault(x,set()).add(v)
    json.dump(sorted(allv),open('/tmp/left.json','w'),ensure_ascii=False,indent=0)
    for x,v in sorted(allv.items()): print(repr(x)[:170],'|',','.join(sorted(v))[:60])
asyncio.run(main())
