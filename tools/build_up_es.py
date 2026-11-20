#!/usr/bin/env python3
"""Páginas de upsell/downsell da versão em espanhol (US$, Cakto) em /es/up/<slug>/."""
import os, sys, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
from es_links import ES_OFFERS
src = open(os.path.join(ROOT, 'tools', 'build_up.py'), encoding='utf-8').read()
ns = {'__file__': os.path.join(ROOT, 'tools', 'build_up.py')}
exec(src.split('\nfor p in PAGES:')[0], ns)
TPL, THEMES = ns['TPL'], ns['THEMES']
TPL = (TPL.replace('<html lang="pt-BR">', '<html lang="es">')
          .replace('Forja do Herói · Oferta liberada', 'Forja do Herói · Oferta liberada')
          .replace('⏳ Oferta válida por', '⏳ Oferta válida por')
          .replace('🔒 Pagamento seguro', '🔒 Pago seguro')
          .replace('🛡️ Garantia de 7 dias', '🛡️ Garantía de 7 días')
          .replace('⚡ Liberação imediata', '⚡ Acceso inmediato')
          .replace("this.textContent='Processando…'", "this.textContent='Procesando…'")
          .replace("'fh_up_{SLUG}'", "'fh_up_es_{SLUG}'"))
_a = TPL.index('<a class="yes" href="{YES_URL}" id="yes">{YES}</a>')
_b = TPL.index('<a class="no" href="{NO_URL}" id="no">{NO}</a>') + len('<a class="no" href="{NO_URL}" id="no">{NO}</a>')
_warn = TPL[TPL.index('<p class="warn">', _a):TPL.index('</p>', _a) + 4]
TPL = TPL[:_a] + ('<cakto-upsell-buttons>\n<cakto-upsell-accept bg-color="{A2}" text-color="{BTNTXT}" upsell-accept-url="members_area" offer-id="{OFFER}" app-base-url="https://app.cakto.com.br" offer-type="{OTYPE}" upsell-reject-url="{REJ}">{YES}</cakto-upsell-accept>\n'
    + _warn + '\n</div>\n<cakto-upsell-reject upsell-reject-url="{REJ}">{NO}</cakto-upsell-reject>\n</cakto-upsell-buttons>') + TPL[_b:]
TPL = re.sub(r"var q=location\.search\.slice\(1\);if\(q\)\{\['yes','no'\][^\n]*\n", '', TPL)
TPL = re.sub(r"document\.getElementById\('yes'\)\.addEventListener[^\n]*\n", '', TPL)
TPL = TPL.replace('</style>', 'cakto-upsell-buttons{display:block}cakto-upsell-accept{display:block;margin-top:18px}cakto-upsell-accept::part(button){width:100%;padding:19px 14px;border-radius:14px;border:0;font:800 18px/1.2 "Exo 2",sans-serif;letter-spacing:.02em;background:linear-gradient(180deg,var(--a) 0%,var(--a2) 100%);box-shadow:0 6px 0 rgba(0,0,0,.45),0 0 30px var(--glow);animation:pulse 1.8s ease-in-out infinite;cursor:pointer}cakto-upsell-reject{display:block;text-align:center;margin:22px auto 0;max-width:420px}cakto-upsell-reject::part(button){background:none;border:0;color:#7e89b3;font-size:14.5px;text-decoration:underline;cursor:pointer}\n</style>', 1)
TPL = TPL.replace('</body>', '<script src="https://caktoscripts.nyc3.cdn.digitaloceanspaces.com/upsell.js"></script>\n</body>', 1)

CAKTO = {
    'elite': (ES_OFFERS['upgrade'], 'upsell', 'https://forjadoheroi.com/es/up/elite-2/'),
    'elite-2': (ES_OFFERS['upgrade_down'], 'downsell', 'members_area'),
    'abismo': (ES_OFFERS['abismo'], 'upsell', 'https://forjadoheroi.com/es/up/abismo-2/'),
    'abismo-2': (ES_OFFERS['abismo30'], 'downsell', 'members_area'),
}
MEDAL = 'https://jsituyuqfzacyszpevkj.supabase.co/storage/v1/object/public/vendas-img/1912394d-acf0-42d3-b6ac-89d2cf25059c/mwk5dhir-k4njou.webp'
PAGES = [
  dict(slug='elite', theme='gold', step='PASO 1 DE 2 · NO CIERRES ESTA PÁGINA',
    kicker='ALERTA DEL SISTEMA', title='Recluta, el Sistema abrió una brecha',
    sub='Tu acceso ya fue liberado. Pero antes de entrar, el Sistema tiene una propuesta que solo aparece ahora, en esta pantalla.',
    img='/img/bumps/elite-medalha.png', imgcls='medal',
    lead='Vas a empezar con lo básico. Quien empieza como <b>Cazador Élite</b> llega al mismo lugar en la mitad del tiempo, porque no entrena a ciegas.',
    perks=[('🧙','3 Maestros de entrenamiento','Calistenia, Pesas e Híbrido. Cada día ya viene armado: abres y entrenas.'),
           ('🕳️','Mazmorra de 30 días','Un plan que sube de nivel solo, con un jefe al final de cada semana.'),
           ('🍖','Taberna y Alquimia','La comunidad de cazadores, recetas y el cálculo de proteína y agua para tu cuerpo.'),
           ('🏆','Ranking y títulos raros','Sube en el ranking de cazadores y desbloquea títulos que el Recluta no ve.')],
    old='US$ 12.90', price='US$ 6.90', note='Pago único. Se activa en la misma cuenta, al instante.',
    yes='👑 SÍ, QUIERO SER ÉLITE · US$ 6.90', no='No, voy a seguir como Recluta y entrenar solo',
    warn='Esta condición desaparece cuando salgas de esta página. Dentro de la app la mejora cuesta el precio completo.'),
  dict(slug='elite-2', theme='gold', step='ÚLTIMA OPORTUNIDAD · NO CIERRES ESTA PÁGINA',
    kicker='EL SISTEMA INSISTE', title='Está bien. Entonces al precio más bajo que existe',
    sub='El Sistema bajó el valor una sola vez. Después de aquí, la brecha se cierra.',
    img='/img/bumps/elite-medalha.png', imgcls='medal',
    lead='Es el mismo <b>Cazador Élite</b> completo: 3 Maestros, Mazmorra de 30 días, Taberna, Alquimia y Ranking. Por menos que un café.',
    perks=[('⚔️','Entrenamiento listo todos los días','Sin pensar qué hacer. Abres, sigues al Maestro, ganas XP.'),
           ('🕳️','Mazmorra con jefes','30 días que se vuelven más difíciles a medida que evolucionas.'),
           ('🍖','Nutrición del héroe','Recetas y cálculo de proteína y agua hechos para ti.')],
    old='US$ 12.90', price='US$ 4.90', note='Pago único. Se activa en la misma cuenta.',
    yes='👑 QUIERO EL ÉLITE POR US$ 4.90', no='No, prefiero quedarme solo con el Recluta',
    warn='Este es el valor más bajo que tendrá el Élite. No vuelve a aparecer.'),
  dict(slug='abismo', theme='red', step='PASO 1 DE 2 · NO CIERRES ESTA PÁGINA',
    kicker='SE ABRIÓ UN PORTAL', title='Cazador, existe un piso debajo de la Mazmorra',
    sub='Tu acceso Élite ya fue liberado. Pero el Sistema detectó que no viniste aquí para quedarte en lo básico.',
    img=MEDAL, imgcls='medal',
    lead='La <b>Mazmorra del Abismo</b> es la fase 2 de Forja do Herói: 60 días de entrenamiento avanzado, para cuando los 30 días se vuelvan fáciles. Y se van a volver fáciles.',
    perks=[('🔥','60 días de entrenamiento avanzado','Más series, ejercicios más pesados y una progresión que no te deja estancarte.'),
           ('👹','4 jefes del Abismo','Guardián de las Puertas, Segador de las Sombras, Rey del Trono Profundo y el Emperador del Abismo.'),
           ('🧔','Maestro Ragnar, el Legendario','Un maestro que solo aparece allá abajo, con guía cada día.'),
           ('👑','Título "Emperador del Abismo"','El título más raro del ranking, más +2.500 XP de recompensa final.')],
    old='US$ 19.90', price='US$ 9.90', note='Pago único. Aparece directo en la pestaña Mazmorra de la app.',
    yes='🕳️ SÍ, QUIERO ENTRAR AL ABISMO · US$ 9.90', no='No, me quedo en la Mazmorra de 30 días',
    warn='Después de esta página, el Abismo solo se abre al precio completo.'),
  dict(slug='abismo-2', theme='red', step='ÚLTIMA OPORTUNIDAD · NO CIERRES ESTA PÁGINA',
    kicker='EL PORTAL SE ESTÁ CERRANDO', title='Entra solo a los primeros 30 días del Abismo',
    sub='¿60 días te pareció mucho? El Sistema libera la primera mitad por un valor más bajo.',
    img=MEDAL, imgcls='medal',
    lead='Recibes los <b>primeros 30 días del Abismo</b>, con los 2 primeros jefes y el Maestro Ragnar. Es el paso natural después de la Mazmorra.',
    perks=[('🔥','30 días de entrenamiento avanzado','El doble de intensidad que la Mazmorra común.'),
           ('👹','2 jefes del Abismo','Guardián de las Puertas y Segador de las Sombras.'),
           ('🧔','Maestro Ragnar','Guía diaria del maestro legendario.')],
    old='US$ 9.90', price='US$ 4.90', note='Pago único. Se activa en la pestaña Mazmorra de la app.',
    yes='🕳️ QUIERO LOS 30 DÍAS POR US$ 4.90', no='No, gracias. Quiero ir directo a la app',
    warn='El portal se cierra cuando salgas de aquí.'),
]
for p in PAGES:
    offer, otype, rej = CAKTO[p['slug']]
    perks = ''.join(f'<div class="pk"><div class="e">{e}</div><div><b>{t}</b><span>{d}</span></div></div>' for e, t, d in p['perks'])
    rep = dict(THEMES[p['theme']])
    rep.update(STEP=p['step'], KICKER=p['kicker'], TITLE=p['title'], SUB=p['sub'], IMG=p['img'], IMGCLS=p['imgcls'],
               LEAD=p['lead'], PERKS=perks, OLD=p['old'], PRICE=p['price'], NOTE=p['note'], YES=p['yes'], NO=p['no'],
               WARN=p['warn'], YES_URL='', NO_URL='', SLUG=p['slug'], OFFER=offer, OTYPE=otype, REJ=rej, BGLAYER='',
               PORTAL=('<div class="portal"><picture><source media="(min-width:761px)" srcset="https://lpdicrpetxqnoxceozfa.supabase.co/storage/v1/object/public/fh-public/quiz/abismo-bg-d.webp"><img src="/img/abismo-bg.webp" alt="Portal del Abismo"></picture></div>' if p['theme'] == 'red' else ''),
               CCLS=(' up' if p['theme'] == 'red' else ''), BODYCLS=(' class="has-bg"' if p['theme'] == 'red' else ''),
               HEROIMG=('' if p['theme'] == 'red' else f'<img class="hero {p["imgcls"]}" src="{p["img"]}" alt="">'),
               PROG='50%' if not p['slug'].endswith('-2') else '85%', BARP=' p' if p['slug'].endswith('-2') else '')
    html = TPL
    for k, v in rep.items():
        html = html.replace('{' + k + '}', v)
    left = re.findall(r'[^\n<>]{0,25}(?:\bde R\$|R\$|você|Pagamento)[^\n<>]{0,25}', re.sub(r'<style.*?</style>', '', html, flags=re.S))
    if left:
        print('ATENÇÃO', p['slug'], left[:5])
    d = os.path.join(ROOT, 'es', 'up', p['slug'])
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, 'index.html'), 'w', encoding='utf-8').write(html)
    print('ok es', p['slug'])
