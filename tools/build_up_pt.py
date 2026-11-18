#!/usr/bin/env python3
"""Páginas de upsell/downsell da versão de Portugal (pt-PT, euro) em /pt/up/<slug>/."""
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = open(os.path.join(ROOT, 'tools', 'build_up.py'), encoding='utf-8').read()
ns = {'__file__': os.path.join(ROOT, 'tools', 'build_up.py')}
exec(src.split('\nfor p in PAGES:')[0], ns)  # pega TPL e THEMES sem gerar as páginas BR
TPL, THEMES = ns['TPL'], ns['THEMES']
TPL = (TPL.replace('<html lang="pt-BR">', '<html lang="pt-PT">')
          .replace('⚡ Liberação imediata', '⚡ Acesso imediato')
          .replace("this.textContent='Processando…'", "this.textContent='A processar…'")
          .replace("'fh_up_{SLUG}'", "'fh_up_pt_{SLUG}'"))

LINKS = {
    'recruta': ('https://appdigitalhub.com.br/c/9F9A8A75?up=sim', 'https://appdigitalhub.com.br/c/9F9A8A75?up=nao'),
    'elite': ('https://appdigitalhub.com.br/c/BB7244F6?up=sim', 'https://appdigitalhub.com.br/c/BB7244F6?up=nao'),
}
MEDAL = 'https://jsituyuqfzacyszpevkj.supabase.co/storage/v1/object/public/vendas-img/1912394d-acf0-42d3-b6ac-89d2cf25059c/mwk5dhir-k4njou.webp'
PAGES = [
  dict(slug='elite', buyer='recruta', theme='gold', step='ETAPA 1 DE 2 · NÃO FECHES ESTA PÁGINA',
    kicker='ALERTA DO SISTEMA', title='Recruta, o Sistema abriu uma brecha',
    sub='O teu acesso foi libertado. Mas antes de entrares, o Sistema tem uma proposta que só aparece agora, neste ecrã.',
    img='/img/bumps/elite-medalha.png', imgcls='medal',
    lead='Vais começar com o básico. Quem começa como <b>Caçador Elite</b> chega ao mesmo sítio em metade do tempo, porque não treina às cegas.',
    perks=[('🧙','3 Mestres de treino','Calistenia, Ferro e Híbrido. Cada dia já vem montado: abres e treinas.'),
           ('🕳️','Dungeon de 30 dias','Um plano que sobe de nível sozinho, com um chefe no fim de cada semana.'),
           ('🍖','Taverna e Alquimia','A comunidade dos caçadores, receitas e o cálculo de proteína e água para o teu corpo.'),
           ('🏆','Ranking e títulos raros','Sobe no ranking dos caçadores e desbloqueia títulos que o Recruta não vê.')],
    old='16,90 €', price='8,90 €', note='Pagamento único. Entra na mesma conta, na hora.',
    yes='👑 SIM, QUERO SER ELITE · 8,90 €', no='Não, vou continuar como Recruta e treinar sozinho',
    warn='Esta condição desaparece quando saíres desta página. Dentro da app o upgrade custa o preço cheio.'),
  dict(slug='elite-2', buyer='recruta', theme='gold', step='ÚLTIMA OPORTUNIDADE · NÃO FECHES ESTA PÁGINA',
    kicker='O SISTEMA INSISTE', title='Está bem. Então pelo preço mais baixo que existe',
    sub='O Sistema baixou o valor uma única vez. Depois daqui, a brecha fecha.',
    img='/img/bumps/elite-medalha.png', imgcls='medal',
    lead='É o mesmo <b>Caçador Elite</b> completo: 3 Mestres, Dungeon de 30 dias, Taverna, Alquimia e Ranking. Por menos do que um café e um pastel de nata.',
    perks=[('⚔️','Treino pronto todos os dias','Sem teres de pensar no que fazer. Abres, segues o Mestre, ganhas XP.'),
           ('🕳️','Dungeon com chefes','30 dias que ficam mais difíceis à medida que evoluis.'),
           ('🍖','Nutrição do herói','Receitas e cálculo de proteína e água feitos para ti.')],
    old='16,90 €', price='5,90 €', note='Pagamento único. Libertado na mesma conta.',
    yes='👑 QUERO O ELITE POR 5,90 €', no='Não, prefiro ficar só com o Recruta',
    warn='Este é o valor mais baixo que o Elite vai ter. Não volta a aparecer.'),
  dict(slug='abismo', buyer='elite', theme='red', step='ETAPA 1 DE 2 · NÃO FECHES ESTA PÁGINA',
    kicker='ABRIU-SE UM PORTAL', title='Caçador, existe um piso abaixo da Dungeon',
    sub='O teu acesso Elite foi libertado. Mas o Sistema detetou que não vieste aqui para ficar no básico.',
    img=MEDAL, imgcls='medal',
    lead='A <b>Dungeon do Abismo</b> é a fase 2 do Forja do Herói: 60 dias de treino avançado, para quando os 30 dias ficarem fáceis. E vão ficar.',
    perks=[('🔥','60 dias de treino avançado','Mais séries, exercícios mais pesados, progressão que não te deixa estagnar.'),
           ('👹','4 chefes do Abismo','Guardião dos Portões, Ceifador das Sombras, Rei do Trono Profundo e o Imperador do Abismo.'),
           ('🧔','Mestre Ragnar, o Lendário','Um mestre que só aparece lá em baixo, com orientação a cada dia.'),
           ('👑','Título "Imperador do Abismo"','O título mais raro do ranking, mais +2.500 XP de recompensa final.')],
    old='19,90 €', price='10,90 €', note='Pagamento único. Aparece diretamente no separador Dungeon da app.',
    yes='🕳️ SIM, QUERO ENTRAR NO ABISMO · 10,90 €', no='Não, vou parar na Dungeon de 30 dias',
    warn='Depois desta página, o Abismo só abre pelo preço cheio.'),
  dict(slug='abismo-2', buyer='elite', theme='red', step='ÚLTIMA OPORTUNIDADE · NÃO FECHES ESTA PÁGINA',
    kicker='O PORTAL ESTÁ A FECHAR', title='Entra só nos primeiros 30 dias do Abismo',
    sub='60 dias pareceu muito? O Sistema liberta a primeira metade por um valor mais baixo.',
    img=MEDAL, imgcls='medal',
    lead='Recebes os <b>30 primeiros dias do Abismo</b>, com os 2 primeiros chefes e o Mestre Ragnar. É o passo natural depois da Dungeon.',
    perks=[('🔥','30 dias de treino avançado','O dobro da intensidade da Dungeon comum.'),
           ('👹','2 chefes do Abismo','Guardião dos Portões e Ceifador das Sombras.'),
           ('🧔','Mestre Ragnar','Orientação diária do mestre lendário.')],
    old='10,90 €', price='5,90 €', note='Pagamento único. Libertado no separador Dungeon da app.',
    yes='🕳️ QUERO OS 30 DIAS POR 5,90 €', no='Não, obrigado. Quero ir diretamente para a app',
    warn='O portal fecha quando saíres daqui.'),
]
for p in PAGES:
    yes_url, no_url = LINKS[p['buyer']]
    perks = ''.join(f'<div class="pk"><div class="e">{e}</div><div><b>{t}</b><span>{d}</span></div></div>' for e, t, d in p['perks'])
    rep = dict(THEMES[p['theme']])
    rep.update(STEP=p['step'], KICKER=p['kicker'], TITLE=p['title'], SUB=p['sub'], IMG=p['img'], IMGCLS=p['imgcls'],
               LEAD=p['lead'], PERKS=perks, OLD=p['old'], PRICE=p['price'], NOTE=p['note'], YES=p['yes'], NO=p['no'],
               WARN=p['warn'], YES_URL=yes_url, NO_URL=no_url, SLUG=p['slug'],
               BGLAYER='',
               PORTAL=('<div class="portal"><picture><source media="(min-width:761px)" srcset="https://lpdicrpetxqnoxceozfa.supabase.co/storage/v1/object/public/fh-public/quiz/abismo-bg-d.webp"><img src="/img/abismo-bg.webp" alt="Portal do Abismo"></picture></div>' if p['theme'] == 'red' else ''),
               CCLS=(' up' if p['theme'] == 'red' else ''), BODYCLS=(' class="has-bg"' if p['theme'] == 'red' else ''),
               HEROIMG=('' if p['theme'] == 'red' else f'<img class="hero {p["imgcls"]}" src="{p["img"]}" alt="">'),
               PROG='50%' if not p['slug'].endswith('-2') else '85%', BARP=' p' if p['slug'].endswith('-2') else '')
    html = TPL
    for k, v in rep.items():
        html = html.replace('{' + k + '}', v)
    html = html.replace('⏳ Oferta válida por', '⏳ Oferta válida por').replace('de ' + p['old'], 'de ' + p['old'])
    d = os.path.join(ROOT, 'pt', 'up', p['slug'])
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, 'index.html'), 'w', encoding='utf-8').write(html)
    print('ok pt', p['slug'])
