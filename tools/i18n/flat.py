import asyncio,json,time,subprocess
import numpy as np
from PIL import Image,ImageDraw
from playwright.async_api import async_playwright
R='/home/claude/forja-do-heroi-site';M='/home/claude/bumps/mock/'
st=json.load(open('/home/claude/tav/state.json'));st.update(nov1=1,nov2=1)
X0,X1,Y0,Y1,YS=76,864,76,1804,150
VW=392;VH=round(VW*(Y1-YS)/(X1-X0))
async def main():
    srv=subprocess.Popen(['python3','-m','http.server','8793','-d',R],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);time.sleep(1)
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        for lang in ['es','en']:
            for name,tab,plan in [('flat-status','heroi','elite'),('flat-status-r','heroi','recruta'),('flat-dungeon','dungeon','elite')]:
                pg=await b.new_page(viewport={'width':VW,'height':VH},device_scale_factor=2.5)
                await pg.add_init_script(f"localStorage.setItem('forja_heroi_v1', {json.dumps(json.dumps(st))});localStorage.setItem('fh_install_hide','1');")
                await pg.route('https://fonts.googleapis.com/**',lambda r:r.fulfill(body=open('/home/claude/fonts.css').read(),content_type='text/css'))
                await pg.route('**/*supabase.co/rest/**',lambda r:r.abort())
                await pg.goto(f'http://localhost:8793/{lang}/app/',wait_until='domcontentloaded');await pg.wait_for_timeout(2500)
                await pg.evaluate(f"window.__FH_PLAN='{plan}';try{{SFX.on=false}}catch(e){{}};closeModal();S.horaHide=1;S.avHide=1;tab='{tab}';render();scrollTo(0,0);document.querySelectorAll('#toasts>*').forEach(e=>e.remove())")
                await pg.wait_for_timeout(1200);await pg.screenshot(path='/tmp/fl.png');await pg.close()
                fr=Image.open(M+name+'.png').convert('RGBA');a=np.array(fr)
                sc=Image.open('/tmp/fl.png').convert('RGBA').resize((X1-X0,Y1-YS),Image.LANCZOS)
                # máscara da tela = pixels do miolo (dentro da moldura) — usa o alfa e a área retangular arredondada
                m=Image.new('L',fr.size,0);ImageDraw.Draw(m).rounded_rectangle((X0,Y0,X1,Y1),radius=95,fill=255)
                base=fr.copy();bg=Image.new('RGBA',fr.size,(5,7,13,255));base.paste(bg,(0,0),m)
                base.paste(sc,(X0,YS),Image.new('L',sc.size,255).crop((0,0,sc.width,sc.height)))
                # recorta o conteúdo pela máscara arredondada
                out=fr.copy();out.paste(base,(0,0),m)
                # barra de status original (hora, sinal, bateria, notch)
                strip=a[Y0:YS,X0:X1].copy();lum=strip[:,:,:3].astype(int).sum(axis=2)
                keep=(lum>560)|(lum<25)
                o=np.array(out);reg=o[Y0:YS,X0:X1]
                reg[keep]=strip[keep];reg[~keep]=[5,7,13,255]
                o[Y0:YS,X0:X1]=reg
                Image.fromarray(o).putalpha(fr.getchannel('A')) if False else None
                res=Image.fromarray(o);res.putalpha(fr.getchannel('A'))
                import os;os.makedirs(f'/home/claude/i18n/bumps/mock/{lang}',exist_ok=True)
                res.save(f'/home/claude/i18n/bumps/mock/{lang}/{name}.png');print(lang,name)
        await b.close()
    srv.terminate()
asyncio.run(main())
