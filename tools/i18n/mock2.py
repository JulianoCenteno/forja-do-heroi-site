"""Celulares do site com a tela traduzida: preenche a área da tela do mockup com o print novo."""
import asyncio, json, time, subprocess
from PIL import Image, ImageDraw, ImageFilter
from playwright.async_api import async_playwright

R = '/home/claude/forja-do-heroi-site'
st = json.load(open('/home/claude/tav/state.json')); st.update(nov1=1, nov2=1)
# nome: (aba, retângulo da tela no mockup)
JOBS = {'sys-ph1': ('heroi', (22, 22, 342, 626)), 'sys-ph2': ('dungeon', (24, 20, 358, 630)), 'sys-ph3': ('missoes', (19, 19, 355, 630))}
PREP = ("S.log=[];S.bonusXP=0;S.goldBonus=50;S.goldSpent=0;S.titles=[];S.title='';S.bosses={};S.q={};S.qTotal=0;"
        "S.cls='paladino';S.name='Juliano';S.horaHide=1;S.avHide=1;")


async def main():
    srv = subprocess.Popen(['python3', '-m', 'http.server', '8791', '-d', R], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)
    try:
        async with async_playwright() as p:
            b = await p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
            for lang in ['es']:
                for name, (tab, (x0, y0, x1, y1)) in JOBS.items():
                    W = 372; Hh = round(W * (y1 - y0) / (x1 - x0))
                    pg = await b.new_page(viewport={'width': W, 'height': Hh}, device_scale_factor=3)
                    await pg.add_init_script(f"localStorage.setItem('forja_heroi_v1', {json.dumps(json.dumps(st))});localStorage.setItem('fh_install_hide','1');")
                    await pg.route('https://fonts.googleapis.com/**', lambda r: r.fulfill(body=open('/home/claude/fonts.css').read(), content_type='text/css'))
                    await pg.route('**/*supabase.co/rest/**', lambda r: r.abort())
                    await pg.goto(f'http://localhost:8791/{lang}/app/', wait_until='domcontentloaded'); await pg.wait_for_timeout(2500)
                    await pg.evaluate("window.__FH_PLAN='elite';try{SFX.on=false}catch(e){};closeModal();" + PREP +
                                      f"tab='{tab}';render();scrollTo(0,0);document.querySelectorAll('#toasts>*').forEach(e=>e.remove())")
                    await pg.wait_for_timeout(1200)
                    await pg.screenshot(path='/tmp/m2.png'); await pg.close()
                    mk = Image.open(f'{R}/img/v3/{name}.webp').convert('RGB')
                    sc = Image.open('/tmp/m2.png').convert('RGB').resize((x1 - x0, y1 - y0), Image.LANCZOS)
                    m = Image.new('L', sc.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, sc.width - 1, sc.height - 1), radius=34, fill=255)
                    mk.paste(sc, (x0, y0), m.filter(ImageFilter.GaussianBlur(0.8)))
                    d = ImageDraw.Draw(mk); cx = (x0 + x1) // 2
                    pass  # d.rounded_rectangle((cx - 26, y0 + 4, cx + 26, y0 + 15), radius=6, fill=(0, 0, 0))
                    mk.save(f'{R}/img/{lang}/{name}.webp', quality=90)
                    print(lang, name)
            await b.close()
    finally:
        srv.terminate()

asyncio.run(main())
