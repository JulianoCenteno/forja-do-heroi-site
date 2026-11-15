import asyncio,json,time,subprocess,sys
sys.path.insert(0,'/home/claude/i18n')
from mock import place
from playwright.async_api import async_playwright
R='/home/claude/forja-do-heroi-site'
st=json.load(open('/home/claude/tav/state.json'));st.update(nov1=1,nov2=1)
PREP="S.log=[];S.bonusXP=0;S.goldBonus=50;S.goldSpent=0;S.titles=[];S.title='';S.bosses={};S.q={};S.qTotal=0;S.cls='paladino';S.name='Juliano';S.horaHide=1;S.avHide=1;"
async def main():
    srv=subprocess.Popen(['python3','-m','http.server','8792','-d',R],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);time.sleep(1)
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        for path,key in [('app/','pt'),('es/app/','es'),('en/app/','en')]:
            pg=await b.new_page(viewport={'width':392,'height':760},device_scale_factor=2)
            await pg.add_init_script(f"localStorage.setItem('forja_heroi_v1', {json.dumps(json.dumps(st))});localStorage.setItem('fh_install_hide','1');")
            await pg.route('https://fonts.googleapis.com/**',lambda r:r.fulfill(body=open('/home/claude/fonts.css').read(),content_type='text/css'))
            await pg.route('**/*supabase.co/rest/**',lambda r:r.abort())
            await pg.goto(f'http://localhost:8792/{path}',wait_until='domcontentloaded');await pg.wait_for_timeout(2500)
            await pg.evaluate("window.__FH_PLAN='elite';try{SFX.on=false}catch(e){};closeModal();"+PREP+"tab='heroi';render();scrollTo(0,0)")
            await pg.wait_for_timeout(1200);await pg.screenshot(path=f'/tmp/lac-{key}.png');await pg.close()
        await b.close()
    srv.terminate()
asyncio.run(main())
for n in ['lac-d','lac-m']:
    for l in ['es','en']:
        print(n,l,place(f'{R}/img/v3/{n}.webp','/tmp/lac-pt.png',f'/tmp/lac-{l}.png',f'{R}/img/{l}/{n}.webp'))
