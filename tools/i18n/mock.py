"""Refaz os celulares do site (sys-ph1..3) com as telas traduzidas.
Captura a mesma tela em PT e no idioma, acha a posição da tela PT dentro do mockup
(homografia por pontos SIFT) e aplica a tela traduzida no mesmo lugar."""
import asyncio, json, time, subprocess, sys
import cv2, numpy as np
from PIL import Image
from playwright.async_api import async_playwright

R = '/home/claude/forja-do-heroi-site'
st = json.load(open('/home/claude/tav/state.json'))
st.update(nov1=1, nov2=1)
JOBS = [('sys-ph1', 'heroi'), ('sys-ph2', 'dungeon'), ('sys-ph3', 'missoes')]
PREP = ("S.log=[];S.bonusXP=0;S.goldBonus=0;S.goldSpent=0;S.titles=[];S.title='';S.bosses={};S.q={};S.qTotal=0;"
        "S.cls='paladino';S.name='Juliano';")


async def caps():
    srv = subprocess.Popen(['python3', '-m', 'http.server', '8790', '-d', R], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1)
    out = {}
    try:
        async with async_playwright() as p:
            b = await p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
            for path, key in [('app/', 'pt'), ('es/app/', 'es'), ('en/app/', 'en')]:
                pg = await b.new_page(viewport={'width': 392, 'height': 700}, device_scale_factor=2)
                await pg.add_init_script(f"localStorage.setItem('forja_heroi_v1', {json.dumps(json.dumps(st))});localStorage.setItem('fh_install_hide','1');")
                await pg.route('https://fonts.googleapis.com/**', lambda r: r.fulfill(body=open('/home/claude/fonts.css').read(), content_type='text/css'))
                await pg.route('**/*supabase.co/rest/**', lambda r: r.abort())
                await pg.goto(f'http://localhost:8790/{path}', wait_until='domcontentloaded')
                await pg.wait_for_timeout(2500)
                await pg.evaluate("window.__FH_PLAN='elite';try{SFX.on=false}catch(e){};closeModal();" + PREP)
                for name, tab in JOBS:
                    await pg.evaluate(f"closeModal();tab='{tab}';render();scrollTo(0,0);document.querySelectorAll('.toast,#toasts>*').forEach(e=>e.remove())")
                    await pg.wait_for_timeout(900)
                    f = f'/tmp/mk-{key}-{name}.png'
                    await pg.screenshot(path=f)
                    out[(key, name)] = f
                await pg.close()
            await b.close()
    finally:
        srv.terminate()
    return out


def place(mock_p, pt_p, tr_p, out_p):
    mk = np.array(Image.open(mock_p).convert('RGB'))
    pt = np.array(Image.open(pt_p).convert('RGB'))
    tr = np.array(Image.open(tr_p).convert('RGB'))
    sift = cv2.SIFT_create(6000)
    g = lambda a: cv2.cvtColor(a, cv2.COLOR_RGB2GRAY)
    k1, d1 = sift.detectAndCompute(g(pt), None)
    k2, d2 = sift.detectAndCompute(g(mk), None)
    m = cv2.BFMatcher().knnMatch(d1, d2, k=2)
    good = [a for a, b in m if a.distance < 0.72 * b.distance]
    src = np.float32([k1[a.queryIdx].pt for a in good]); dst = np.float32([k2[a.trainIdx].pt for a in good])
    H, inl = cv2.findHomography(src, dst, cv2.RANSAC, 3.0)
    h, w = pt.shape[:2]
    warped = cv2.warpPerspective(tr, H, (mk.shape[1], mk.shape[0]), flags=cv2.INTER_AREA)
    # máscara = área da tela (cantos arredondados), recortada pela tela visível do mockup
    sm = np.zeros((h, w), np.uint8)
    rad = int(w * 0.07)
    cv2.rectangle(sm, (rad, 0), (w - rad, h), 255, -1); cv2.rectangle(sm, (0, rad), (w, h - rad), 255, -1)
    for cx, cy in [(rad, rad), (w - rad, rad), (rad, h - rad), (w - rad, h - rad)]:
        cv2.circle(sm, (cx, cy), rad, 255, -1)
    wm = cv2.warpPerspective(sm, H, (mk.shape[1], mk.shape[0]))
    # só onde a tela PT aparece no mockup (não pinta a moldura)
    wpt = cv2.warpPerspective(pt, H, (mk.shape[1], mk.shape[0]), flags=cv2.INTER_AREA)
    diff = np.abs(wpt.astype(int) - mk.astype(int)).sum(axis=2)
    vis = ((diff < 120) & (wm > 0)).astype(np.uint8) * 255
    vis = cv2.morphologyEx(vis, cv2.MORPH_CLOSE, np.ones((15, 15), np.uint8))
    # preenche buracos internos
    cnts, _ = cv2.findContours(vis, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    hull = np.zeros_like(vis)
    if cnts:
        c = max(cnts, key=cv2.contourArea)
        cv2.drawContours(hull, [c], -1, 255, -1)
    mask = cv2.erode(np.minimum(hull, wm), np.ones((3, 3), np.uint8))
    mask = cv2.GaussianBlur(mask, (5, 5), 0).astype(np.float32)[..., None] / 255
    res = (warped * mask + mk * (1 - mask)).astype(np.uint8)
    Image.fromarray(res).save(out_p, quality=90)
    return len(good), int(inl.sum())


if __name__ == '__main__':
    c = asyncio.run(caps())
    for name, _ in JOBS:
        for lang in ['es', 'en']:
            r = place(f'{R}/img/v3/{name}.webp', c[('pt', name)], c[(lang, name)], f'{R}/img/{lang}/{name}.webp')
            print(name, lang, r)
