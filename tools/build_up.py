#!/usr/bin/env python3
"""Gera as páginas de upsell/downsell em /up/<slug>/index.html."""
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LINKS = {
    'recruta': ('https://appdigitalhub.com.br/c/43752C6D?up=sim', 'https://appdigitalhub.com.br/c/43752C6D?up=nao'),
    'elite': ('https://appdigitalhub.com.br/c/1D6785B5?up=sim', 'https://appdigitalhub.com.br/c/1D6785B5?up=nao'),
}

PAGES = [
  dict(slug='elite', buyer='recruta', theme='gold', step='ETAPA 1 DE 2 · NÃO FECHE ESTA PÁGINA',
    kicker='ALERTA DO SISTEMA', title='Recruta, o Sistema abriu uma brecha',
    sub='Seu acesso foi liberado. Mas antes de entrar, o Sistema tem uma proposta que só aparece agora, nesta tela.',
    img='/img/bumps/elite-medalha.png', imgcls='medal',
    lead='Você vai começar com o básico. Quem começa como <b>Caçador Elite</b> chega no mesmo lugar em metade do tempo, porque não treina no escuro.',
    perks=[('🧙','3 Mestres de treino','Calistenia, Ferro e Híbrido. Cada dia já vem montado: você abre e treina.'),
           ('🕳️','Dungeon de 30 dias','Um plano que sobe de nível sozinho, com chefe no final de cada semana.'),
           ('🍖','Taverna e Alquimia','Receitas e o cálculo de proteína e água pro seu corpo, sem planilha.'),
           ('🏆','Ranking e títulos raros','Suba no ranking dos caçadores e desbloqueie títulos que o Recruta não vê.')],
    old='R$ 26,90', price='R$ 14,90', note='Pagamento único. Entra na mesma conta, na hora.',
    yes='👑 SIM, QUERO VIRAR ELITE · R$ 14,90', no='Não, vou continuar como Recruta e treinar sozinho',
    warn='Essa condição some quando você sair desta página. Dentro do app o upgrade custa o preço cheio.'),
  dict(slug='elite-2', buyer='recruta', theme='gold', step='ÚLTIMA CHANCE · NÃO FECHE ESTA PÁGINA',
    kicker='O SISTEMA INSISTE', title='Tudo bem. Então pelo menor preço que existe',
    sub='O Sistema baixou o valor uma única vez. Depois daqui, a brecha fecha.',
    img='/img/bumps/elite-medalha.png', imgcls='medal',
    lead='É o mesmo <b>Caçador Elite</b> completo: 3 Mestres, Dungeon de 30 dias, Taverna, Alquimia e Ranking. Só que por menos do que um lanche.',
    perks=[('⚔️','Treino pronto todo dia','Sem precisar pensar no que fazer. Abre, segue o Mestre, ganha XP.'),
           ('🕳️','Dungeon com chefes','30 dias que ficam mais difíceis conforme você evolui.'),
           ('🍖','Nutrição do herói','Receitas e cálculo de proteína e água feitos pra você.')],
    old='R$ 26,90', price='R$ 9,90', note='Pagamento único. Liberado na mesma conta.',
    yes='👑 QUERO O ELITE POR R$ 9,90', no='Não, prefiro ficar só com o Recruta',
    warn='Este é o menor valor que o Elite vai ter. Não aparece de novo.'),
  dict(slug='abismo', buyer='elite', theme='red', step='ETAPA 1 DE 2 · NÃO FECHE ESTA PÁGINA',
    kicker='UM PORTAL SE ABRIU', title='Caçador, existe um andar abaixo da Dungeon',
    sub='Seu acesso Elite foi liberado. Mas o Sistema detectou que você não veio aqui pra ficar no básico.',
    img='/img/chefe.webp', imgcls='wide',
    lead='A <b>Dungeon do Abismo</b> é a fase 2 do Forja do Herói: 60 dias de treino avançado, para quando os 30 dias ficarem fáceis. E vão ficar.',
    perks=[('🔥','60 dias de treino avançado','Mais séries, exercícios mais pesados, progressão que não deixa você estagnar.'),
           ('👹','4 chefes do Abismo','Guardião dos Portões, Ceifador das Sombras, Rei do Trono Profundo e o Imperador do Abismo.'),
           ('🧔','Mestre Ragnar, o Lendário','Um mestre que só aparece lá embaixo, com orientação a cada dia.'),
           ('👑','Título "Imperador do Abismo"','O título mais raro do ranking, mais +2.500 XP de recompensa final.')],
    old='R$ 39,90', price='R$ 19,90', note='Pagamento único. Aparece direto na aba Dungeon do app.',
    yes='🕳️ SIM, QUERO ENTRAR NO ABISMO · R$ 19,90', no='Não, vou parar na Dungeon de 30 dias',
    warn='Depois desta página, o Abismo só abre pelo preço cheio.'),
  dict(slug='abismo-2', buyer='elite', theme='red', step='ÚLTIMA CHANCE · NÃO FECHE ESTA PÁGINA',
    kicker='O PORTAL ESTÁ FECHANDO', title='Entre só nos primeiros 30 dias do Abismo',
    sub='60 dias pareceu muito? O Sistema libera a primeira metade por um valor menor.',
    img='/img/chefe.webp', imgcls='wide',
    lead='Você recebe os <b>30 primeiros dias do Abismo</b>, com os 2 primeiros chefes e o Mestre Ragnar. É o próximo passo natural depois da Dungeon.',
    perks=[('🔥','30 dias de treino avançado','O dobro de intensidade da Dungeon comum.'),
           ('👹','2 chefes do Abismo','Guardião dos Portões e Ceifador das Sombras.'),
           ('🧔','Mestre Ragnar','Orientação diária do mestre lendário.')],
    old='R$ 19,90', price='R$ 9,90', note='Pagamento único. Liberado na aba Dungeon do app.',
    yes='🕳️ QUERO OS 30 DIAS POR R$ 9,90', no='Não, obrigado. Quero ir direto para o app',
    warn='O portal fecha quando você sair daqui.'),
]

TPL = r'''<!doctype html>
<html lang="pt-BR"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>Forja do Herói · Oferta liberada</title>
<link rel="icon" href="/img/v2/logo-square.webp">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@800;900&family=Exo+2:ital,wght@0,400;0,500;0,600;0,700;0,800;1,700;1,800&display=swap" rel="stylesheet">
<style>
*{box-sizing:border-box;margin:0;padding:0}
:root{--a:{A};--a2:{A2};--glow:{GLOW}}
body{background:#050a1c radial-gradient(ellipse 120% 60% at 50% 0%,{BG} 0%,#050a1c 70%) no-repeat;color:#e6ecff;font-family:'Exo 2',system-ui,sans-serif;font-size:17px;line-height:1.5;min-height:100vh}
.w{max-width:620px;margin:0 auto;padding:18px 18px 40px}
.bar{background:#ff3b5c;color:#fff;font-weight:800;font-size:12.5px;letter-spacing:.12em;text-align:center;padding:9px 10px}
.bar.p{background:linear-gradient(90deg,#ff3b5c,#ff6a3d)}
.prog{height:6px;background:#1a2244;border-radius:6px;overflow:hidden;margin:14px 0 22px}
.prog i{display:block;height:100%;width:{PROG};background:linear-gradient(90deg,var(--a2),var(--a))}
.logo{display:block;width:150px;margin:0 auto 14px}
.k{display:inline-block;border:1px solid var(--a);color:var(--a);font-weight:800;letter-spacing:.3em;font-size:12px;padding:6px 14px 6px 18px;border-radius:30px;background:rgba(0,0,0,.35);box-shadow:0 0 18px var(--glow)}
.c{text-align:center}
h1{font-family:Cinzel,serif;font-weight:900;text-transform:uppercase;font-size:clamp(26px,7vw,40px);line-height:1.08;margin:16px 0 10px;background:linear-gradient(180deg,#fff 0%,#fff 45%,var(--a) 100%);-webkit-background-clip:text;background-clip:text;color:transparent;filter:drop-shadow(0 2px 0 rgba(0,0,0,.6))}
.sub{color:#b8c3e6;font-size:17px;max-width:520px;margin:0 auto}
.hero{margin:22px auto 6px;display:block}
.hero.medal{width:min(230px,60vw);filter:drop-shadow(0 0 40px var(--glow))}
.hero.wide{width:100%;border-radius:16px;border:1px solid rgba(255,255,255,.12);box-shadow:0 0 50px var(--glow)}
.lead{background:rgba(255,255,255,.04);border-left:3px solid var(--a);padding:14px 16px;border-radius:8px;margin:20px 0;font-size:17.5px}
.lead b{color:var(--a)}
.perks{display:grid;gap:10px;margin:18px 0}
.pk{display:flex;gap:14px;align-items:flex-start;background:linear-gradient(180deg,rgba(25,34,70,.85),rgba(14,20,44,.85));border:1px solid rgba(255,255,255,.09);border-radius:14px;padding:14px}
.pk .e{font-size:26px;line-height:1;flex:0 0 auto;width:42px;height:42px;display:grid;place-items:center;border-radius:10px;background:rgba(0,0,0,.35);border:1px solid var(--a2)}
.pk b{display:block;font-size:16.5px;color:#fff}
.pk span{font-size:15px;color:#a9b4d9}
.offer{margin:24px 0 10px;text-align:center;background:linear-gradient(180deg,rgba(0,0,0,.25),rgba(0,0,0,.5));border:2px solid var(--a);border-radius:18px;padding:22px 16px;box-shadow:0 0 40px var(--glow) inset,0 0 30px var(--glow)}
.old{color:#8d97bd;text-decoration:line-through;font-size:18px}
.price{font-family:'Exo 2';font-weight:800;font-style:italic;font-size:54px;line-height:1;color:#fff;margin:4px 0 6px;text-shadow:0 0 22px var(--glow)}
.note{font-size:14px;color:#a9b4d9}
.yes{display:block;width:100%;margin:18px 0 0;padding:19px 14px;border-radius:14px;border:0;font:800 18px/1.2 'Exo 2';letter-spacing:.02em;color:{BTNTXT};text-decoration:none;background:linear-gradient(180deg,var(--a) 0%,var(--a2) 100%);box-shadow:0 6px 0 rgba(0,0,0,.45),0 0 30px var(--glow);animation:pulse 1.8s ease-in-out infinite}
.yes:active{transform:translateY(3px);box-shadow:0 3px 0 rgba(0,0,0,.45)}
@keyframes pulse{50%{transform:scale(1.025)}}
.warn{font-size:13.5px;color:#ffb3a6;margin-top:12px}
.no{display:block;text-align:center;margin:22px auto 0;color:#7e89b3;font-size:14.5px;text-decoration:underline;max-width:420px}
.sec{display:flex;justify-content:center;gap:16px;flex-wrap:wrap;margin-top:18px;font-size:13px;color:#7e89b3}
.timer{font-weight:800;color:#fff;font-variant-numeric:tabular-nums}
</style></head><body>
<div class="bar{BARP}">{STEP}</div>
<div class="w">
<div class="prog"><i></i></div>
<img class="logo" src="/img/v2/logo-full.webp" alt="Forja do Herói">
<div class="c"><span class="k">{KICKER}</span>
<h1>{TITLE}</h1>
<p class="sub">{SUB}</p>
<img class="hero {IMGCLS}" src="{IMG}" alt=""></div>
<p class="lead">{LEAD}</p>
<div class="perks">{PERKS}</div>
<div class="offer">
<div class="old">de {OLD}</div>
<div class="price">{PRICE}</div>
<div class="note">{NOTE}</div>
<a class="yes" href="{YES_URL}" id="yes">{YES}</a>
<p class="warn">⏳ Oferta válida por <span class="timer" id="t">10:00</span> · {WARN}</p>
</div>
<a class="no" href="{NO_URL}" id="no">{NO}</a>
<div class="sec"><span>🔒 Pagamento seguro</span><span>🛡️ Garantia de 7 dias</span><span>⚡ Liberação imediata</span></div>
</div>
<script>
(function(){var k='fh_up_{SLUG}',e;try{e=+sessionStorage.getItem(k)}catch(_){}if(!e){e=Date.now()+6e5;try{sessionStorage.setItem(k,e)}catch(_){}}
var t=document.getElementById('t');function f(){var s=Math.max(0,Math.round((e-Date.now())/1e3));t.textContent=String(Math.floor(s/60)).padStart(2,'0')+':'+String(s%60).padStart(2,'0')}f();setInterval(f,1000);
var q=location.search.slice(1);if(q){['yes','no'].forEach(function(id){var a=document.getElementById(id);a.href+=(a.href.indexOf('?')>-1?'&':'?')+q.replace(/(^|&)up=[^&]*/g,'').replace(/^&/,'')});}
document.getElementById('yes').addEventListener('click',function(){this.style.opacity=.7;this.textContent='Processando…'});
})();
</script>
</body></html>'''

THEMES = {
  'gold': dict(A='#ffc83a', A2='#e08a00', GLOW='rgba(255,180,40,.35)', BG='#2a1d05', BTNTXT='#2a1500'),
  'red': dict(A='#ff4d4d', A2='#a3122e', GLOW='rgba(255,60,80,.35)', BG='#2a0712', BTNTXT='#fff'),
}

for p in PAGES:
    yes_url, no_url = LINKS[p['buyer']]
    perks = ''.join(f'<div class="pk"><div class="e">{e}</div><div><b>{t}</b><span>{d}</span></div></div>' for e, t, d in p['perks'])
    rep = dict(THEMES[p['theme']])
    rep.update(STEP=p['step'], KICKER=p['kicker'], TITLE=p['title'], SUB=p['sub'], IMG=p['img'], IMGCLS=p['imgcls'],
               LEAD=p['lead'], PERKS=perks, OLD=p['old'], PRICE=p['price'], NOTE=p['note'], YES=p['yes'], NO=p['no'],
               WARN=p['warn'], YES_URL=yes_url, NO_URL=no_url, SLUG=p['slug'],
               PROG='50%' if not p['slug'].endswith('-2') else '85%', BARP=' p' if p['slug'].endswith('-2') else '')
    html = TPL
    for k, v in rep.items():
        html = html.replace('{' + k + '}', v)
    d = os.path.join(ROOT, 'up', p['slug'])
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, 'index.html'), 'w').write(html)
    print('ok', p['slug'])
