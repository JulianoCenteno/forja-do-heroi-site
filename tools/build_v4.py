import re,sys
src=open('index.html',encoding='utf-8').read() if len(sys.argv)<2 else open(sys.argv[1],encoding='utf-8').read()
def between(a,b,s=src):
    i=s.index(a);j=s.index(b,i);return s[i:j]
head=src[:src.index('<link rel="stylesheet" href="site.css')]
head=head.replace('<link rel="preload" as="image" href="img/v3/hero-d.webp" media="(min-width:761px)"><link rel="preload" as="image" href="img/v3/hero-m.webp" media="(max-width:760px)">','<link rel="preload" as="image" href="/img/v3/char-paladino.webp">')
head+='<link rel="stylesheet" href="/v4-base.css?v=1">\n<link rel="stylesheet" href="/taverna.css?v=4">\n<link rel="stylesheet" href="/popup.css?v=1">\n<link rel="stylesheet" href="/v4.css?v=5">\n'
rest=src[src.index('<!-- Meta Pixel'):src.index('</head>')]
nav=between('<svg width="0" height="0"','<!-- 1. HERO -->')
mestres=between('<!-- 6a. MESTRES + CORRIDA -->','<!-- 6b. TAVERNA')
mxrow=between('<div class="mx-row">','<a class="tx-btn"',mestres)
taverna=between('<!-- 6b. TAVERNA','<!-- 7. GARANTIA')
faqitems=re.findall(r'<details class="fq".*?</details>',src,re.S)
faqitems=[f.replace('class="fq" ','').replace(' open>','>') for f in faqitems]
faqitems=[re.sub(r'<svg.*?</svg>','',f,flags=re.S) for f in faqitems]
footer=src[src.index('<!-- 10. RODAPÉ -->'):src.index('<script src="site.js')]
ARR='<svg viewBox="0 0 24 20" aria-hidden="true"><path d="M2 10h17M12 3l7 7-7 7" fill="none" stroke="currentColor" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/></svg>'
SB='https://lpdicrpetxqnoxceozfa.supabase.co/storage/v1/object/public/fh/art/evo/'
body=f'''<main class="v4">

<!-- 1. HERO -->
<section class="s hero" id="topo">
 <span class="hudt big r" style="bottom:4%">ARISE</span><span class="hudt l" style="bottom:30px">PLAYER.STATUS // NV 01</span>
 <div class="s-in grid2">
  <div class="txt">
   <span class="pill">⚔️ App de treino em RPG</span>
   <h1><span class="w">Seu treino virou</span><span class="g">um RPG.</span></h1>
   <p class="p">Treine na vida real, ganhe <b>XP a cada série</b>, cumpra missões diárias, derrote chefes com os seus recordes e veja o seu herói evoluir junto com você.</p>
   <div class="ctas"><a class="cta" href="#planos">Despertar meu herói {ARR}</a><a class="cta ghost" href="#classes">Escolher minha classe</a></div>
   <div class="chips"><span><img src="/img/v3/ic-xp.webp" alt="">XP imediato</span><span><img src="/img/v3/ic-scroll.webp" alt="">Missões diárias</span><span><img src="/img/v3/ic-demon.webp" alt="">Chefes épicos</span></div>
  </div>
  <div class="squad" aria-label="Monge, Paladino e Guerreiro">
   <img class="m" src="/img/v3/char-monge.webp" alt="Monge das Barras" width="768" height="1152" fetchpriority="high">
   <img class="g" src="/img/v3/char-guerreiro.webp" alt="Guerreiro do Ferro" width="768" height="1136" fetchpriority="high">
   <img class="p" src="/img/v3/char-paladino.webp" alt="Paladino Híbrido" width="768" height="1125" fetchpriority="high">
   <div class="badge"><span class="ic"><img src="/img/v3/ic-xp.webp" alt=""></span><div><b>+50 XP</b><small>a cada série</small></div></div>
   <div class="badge bd2"><span class="ic">⬆️</span><div><b>NÍVEL 12</b><small>subiu de nível!</small></div></div>
  </div>
 </div>
</section>

<!-- 2. APP POR DENTRO -->
<section class="s alt" id="app">
 <span class="hudt l" style="top:34px">[ SISTEMA ] · APP.TOUR</span><span class="hudt r" style="top:34px">REC ●</span>
 <div class="s-in c">
  <span class="pill cy">📱 O app por dentro</span>
  <h2 class="h"><span class="w">Veja o Forja</span> <span class="g">funcionando</span></h2>
  <p class="p">É assim que fica o seu treino: cada série vira XP, você sobe de nível, cumpre missões e enfrenta chefes. Tudo no celular, sem baixar nada da loja.</p>
  <div class="appg">
   <div class="phone rv"><video src="/quiz/tour.mp4?v=3" poster="/quiz/tour-poster.webp?v=2" muted loop playsinline autoplay preload="metadata"></video><span class="live">▶ O APP POR DENTRO</span></div>
   <div class="feats">
    <div class="card feat rv"><span class="ic">⚔️</span><div><h3>Treino que vira XP</h3><p>Registre as séries, o peso e as repetições. O Sistema converte tudo em XP e ouro na hora.</p></div></div>
    <div class="card feat rv"><span class="ic">📜</span><div><h3>Missões diárias</h3><p>Missões novas todo dia e missões de emergência surpresa. Quem falha cai na Zona de Penalidade.</p></div></div>
    <div class="card feat rv"><span class="ic">👹</span><div><h3>Chefes e dungeon</h3><p>Derrote os 10 chefes com os seus recordes e encare a Dungeon de 30 dias.</p></div></div>
    <div class="card feat rv"><span class="ic">🏆</span><div><h3>Ranking e Taverna</h3><p>Dispute a temporada, desafie amigos para duelos e poste o treino do dia.</p></div></div>
   </div>
  </div>
 </div>
</section>

<!-- 3. LACUNA -->
<section class="s lac" id="problema">
 <div class="s-in grid2">
  <div class="txt">
   <span class="pill">🧠 O verdadeiro problema</span>
   <h2 class="h"><span class="w">A lacuna da</span> <span class="g">recompensa</span></h2>
   <p class="p">Nos jogos, o seu cérebro é recompensado em segundos. No treino, os resultados levam meses, e é aí que quase todo mundo desiste. O Forja do Herói fecha essa lacuna com <b>feedback instantâneo</b> a cada série.</p>
   <div class="vs"><div class="bad"><b>Treino comum</b>Resultado só depois de meses. Motivação some na 3ª semana.</div><div class="good"><b>Forja do Herói</b>XP, nível e recompensa no mesmo dia. Vontade de voltar amanhã.</div></div>
  </div>
  <div class="loop">
   <div class="card rv"><span class="ic"><img src="/img/v3/ic-xp.webp" alt=""></span><div><h3>Recompensa imediata</h3><p>Ganhe XP a cada série concluída.</p></div></div>
   <div class="card rv"><span class="ic"><img src="/img/v3/ic-scroll.webp" alt=""></span><div><h3>Recompensa diária</h3><p>Complete missões e mantenha a sua sequência.</p></div></div>
   <div class="card rv"><span class="ic"><img src="/img/v3/ic-demon.webp" alt=""></span><div><h3>Recompensa épica</h3><p>Enfrente chefes e supere os seus recordes pessoais.</p></div></div>
  </div>
 </div>
</section>

<!-- 4. SISTEMA -->
<section class="s alt" id="sistema">
 <div class="s-in c">
  <span class="pill cy">🖥️ Veja o sistema</span>
  <h2 class="h"><span class="w">Seu treino,</span> <span class="g">como num jogo</span></h2>
  <p class="p">Acompanhe o seu herói, entre em dungeons e cumpra missões diárias sem sair do treino.</p>
  <div class="shots">
   <figure class="rv"><div class="frame"><img src="/img/v3/sys-ph1.webp" alt="Tela do Herói e status no app" loading="lazy" width="371" height="650"></div><figcaption>Herói e status<small>Nível, atributos e patente</small></figcaption></figure>
   <figure class="rv"><div class="frame"><img src="/img/v3/sys-ph2.webp" alt="Tela da Dungeon no app" loading="lazy" width="385" height="650"></div><figcaption>Dungeons<small>Incursões com recompensas</small></figcaption></figure>
   <figure class="rv"><div class="frame"><img src="/img/v3/sys-ph3.webp" alt="Tela de Missões no app" loading="lazy" width="384" height="650"></div><figcaption>Missões<small>Diárias e de emergência</small></figcaption></figure>
  </div>
  <span class="swipe">← arraste para ver as telas →</span>
 </div>
</section>

<!-- 5. CLASSES -->
<section class="s" id="classes">
 <span class="hudt l" style="top:40px">CLASS.SELECT // 03</span><span class="hudt r" style="top:40px">FORJA · ARISE</span>
 <div class="s-in c">
  <span class="pill">🛡️ Escolha sua classe</span>
  <h2 class="h"><span class="w">Escolha quem você</span> <span class="g">vai se tornar</span></h2>
  <p class="p">Cada classe muda a fantasia da sua jornada. Escolha jogar com <b>herói ou heroína</b>; a evolução acontece no treino real.</p>
  <div class="cls2">
   <a class="c2" href="#planos" style="--cc:#35e0b4"><span class="slash"></span><img src="/img/v3/char-monge.webp" alt="Monge das Barras" loading="lazy" width="768" height="1152"><span class="lb">Monge das Barras<small>CALISTENIA</small></span></a>
   <a class="c2" href="#planos" style="--cc:#ffc83a"><span class="slash"></span><img src="/img/v3/char-paladino.webp" alt="Paladino Híbrido" loading="lazy" width="768" height="1125"><span class="lb">Paladino Híbrido<small>HÍBRIDO</small></span></a>
   <a class="c2" href="#planos" style="--cc:#ff4d6a"><span class="slash"></span><img src="/img/v3/char-guerreiro.webp" alt="Guerreiro do Ferro" loading="lazy" width="768" height="1136"><span class="lb">Guerreiro do Ferro<small>MUSCULAÇÃO</small></span></a>
  </div>
  <span class="swipe">← arraste para ver as classes →</span>
  <div class="cls2-d">
   <div class="card" style="--cc:#35e0b4"><h3>Monge das Barras</h3><p>Treina com o peso do corpo, em casa ou no parque. Barra, argolas e muita agilidade.</p></div>
   <div class="card" style="--cc:#ffc83a"><h3>Paladino Híbrido</h3><p>Barra e ferro no mesmo treino: força e definição juntas, na academia ou em casa.</p></div>
   <div class="card" style="--cc:#ff4d6a"><h3>Guerreiro do Ferro</h3><p>Musculação na academia. Cada quilo levantado vira XP para o seu herói.</p></div>
  </div>
  <p style="margin-top:30px"><a class="cta" href="#planos">Escolher minha classe {ARR}</a></p>
 </div>
</section>

<!-- 6. EVOLUÇÃO -->
<section class="s alt" id="evolucao">
 <span class="hudt big l" style="top:8%">LEVEL UP</span>
 <div class="s-in c">
  <span class="pill">✨ Novo · seu herói evolui</span>
  <h2 class="h"><span class="w">Suba de nível e</span> <span class="g">veja a transformação</span></h2>
  <p class="p">Conforme você treina, libera formas cada vez mais fortes do seu herói: aura, armadura, capa e, no nível 50, asas de energia.</p>
  <div class="evo">
   <figure class="rv" style="--ec:#7fe0ff"><img src="{SB}guerreiro_m_10.webp" alt="Guerreiro na Forma Desperta, nível 10" loading="lazy"><figcaption><b>NÍVEL 10</b><span>Desperta</span></figcaption></figure>
   <figure class="rv" style="--ec:#b98aff"><img src="{SB}monge_f_20.webp" alt="Monja na Forma Veterana, nível 20" loading="lazy"><figcaption><b>NÍVEL 20</b><span>Veterana</span></figcaption></figure>
   <figure class="rv" style="--ec:#ff8a5a"><img src="{SB}guerreiro_f_30.webp" alt="Guerreira na Forma Lendária, nível 30" loading="lazy"><figcaption><b>NÍVEL 30</b><span>Lendária</span></figcaption></figure>
   <figure class="rv" style="--ec:#ffd84a"><img src="{SB}paladino_m_50.webp" alt="Paladino na Forma Ascendida, nível 50" loading="lazy"><figcaption><b>NÍVEL 50</b><span>Ascendida</span></figcaption></figure>
  </div>
  <div class="shop"><span>🛡️ Ícones de perfil premium</span><span>🖼️ Papéis de parede em HD</span><span>⚔️ Banners que evoluem</span></div>
 </div>
</section>

<!-- 7. ARQUIVO DOS MESTRES -->
<section class="s arq" id="mestres">
 <span class="hudt l" style="top:28px">ARQUIVO.MESTRES // NUM 0241</span><span class="hudt r" style="bottom:28px">SISTEMA · FORJA DO HERÓI</span>
 <div class="s-in">
  <div class="c"><span class="pill">🧙 Mestres do Forja</span>
  <h2 class="h"><span class="w">Conheça cada</span> <span class="g">mestre</span></h2>
  <p class="p" style="color:#e6dcff">Três mestres passam o seu treino, <b>dia após dia</b>, cada um com fichas exclusivas. Escolha o seu e troque quando quiser.</p></div>
  <div class="ar ar-wrap" id="arq" style="--mc:#3fe08a">
   <div class="ar-t"><div class="k">Arquivo do mestre</div><span class="nm" id="arNm">Mestre Kaito</span><span class="tt" id="arTt">Mestre da Calistenia</span><p id="arTx"></p><q id="arQ"></q><div class="wk" id="arWk"></div></div>
   <div class="ar-p"><img id="arImg" src="/img/mestres/monge.webp" alt="Mestre Kaito" width="560" height="700"></div>
   <div class="ar-n" id="arN">KAI<br>TO<small>FORJA // MASTER FILE</small></div>
  </div>
  <div class="ar-th" id="arTh" role="tablist" aria-label="Escolha o mestre">
   <button class="on" data-i="0" aria-label="Mestre Kaito"><img src="/img/mestres/monge.webp" alt=""></button>
   <button data-i="1" aria-label="Mestre Brutus"><img src="/img/mestres/guerreiro.webp" alt=""></button>
   <button data-i="2" aria-label="Mestra Aurora"><img src="/img/mestres/paladino.webp" alt=""></button>
  </div>
  {mxrow.replace('class="mx-row"','class="mx-row ar-x"',1)}</div>
  <p class="c" style="margin-top:30px"><a class="cta" href="#planos">Quero treinar com um mestre {ARR}</a></p>
  <p class="note c" style="color:#c7b8ff">Mestres e corrida inclusos no plano Caçador Elite.</p>
 </div>
</section>

<!-- 8. ALQUIMIA -->
<section class="s alq" id="alquimia">
 <div class="s-in grid2">
  <div class="frame rv"><img src="/img/v3/alq-scene.webp" alt="Paladino com shake proteico e mesa de receitas anabólicas" loading="lazy" width="940" height="940"></div>
  <div class="txt">
   <span class="pill">🎁 Bônus extra</span>
   <h2 class="h"><span class="w">Alquimia do Herói:</span> <span class="g">50 receitas anabólicas</span></h2>
   <p class="p">Receitas práticas e ricas em proteína, com ingredientes do supermercado, para alimentar o treino, apoiar a recuperação e ajudar o herói a evoluir de verdade. Com cálculo de proteína e água para o seu corpo.</p>
   <div class="chipg"><span>🥤 Shakes proteicos</span><span>🥞 Panquecas</span><span>🍫 Mousses</span><span>🍗 Comida de verdade</span><span>⏱️ Fácil de fazer</span><span>💪 Ricas em proteína</span></div>
   <a class="cta" href="#planos">Quero evoluir com a dieta {ARR}</a>
  </div>
 </div>
</section>

<!-- 9. RANKING -->
<section class="s alt" id="ranking">
 <div class="s-in c">
  <span class="pill">🏆 Ranking da temporada</span>
  <h2 class="h"><span class="w">Suba no</span> <span class="g">ranking da temporada</span></h2>
  <p class="p">Ganhe XP, conclua missões e dispute com outros heróis por prestígio e recompensas mensais.</p>
  <div class="pod rv"><img src="/img/v3/rk-p2.webp" alt="2º lugar: Rafael, 1.033.420 XP" loading="lazy"><img src="/img/v3/rk-p1.webp" alt="1º lugar: Juliano, 1.248.750 XP" loading="lazy"><img src="/img/v3/rk-p3.webp" alt="3º lugar: Caio, 987.230 XP" loading="lazy"></div>
  <div class="rew">
   <div class="card rv"><span class="ic">👑</span><div><h3>Título exclusivo</h3><p>Destaque o seu status de herói.</p></div></div>
   <div class="card rv"><span class="ic">🪙</span><div><h3>Bônus de ouro</h3><p>Moedas especiais da temporada.</p></div></div>
   <div class="card rv"><span class="ic">⭐</span><div><h3>Prestígio</h3><p>Reconhecimento e benefícios únicos.</p></div></div>
  </div>
  <a class="cta" href="#planos">Quero subir no ranking {ARR}</a>
  <p class="note">Exemplo ilustrativo do ranking.</p>
 </div>
</section>

{taverna}
<!-- 11. GARANTIA -->
<section class="s" id="garantia">
 <div class="s-in gar">
  <img class="rv" src="/img/v3/gar-badge.webp" alt="Selo de garantia incondicional de 7 dias" loading="lazy" width="710" height="760">
  <div>
   <span class="pill cy">🛡️ Risco zero</span>
   <h2 class="h"><span class="w">Garantia incondicional</span> <span class="g">de 7 dias</span></h2>
   <p class="p">Teste o Forja do Herói por 7 dias completos. Se sentir que o app não é para você, peça o reembolso e receba <b>100% do valor</b>, sem burocracia e sem perguntas.</p>
   <div class="gpts"><div class="card"><b>7 dias</b><span>para testar tudo</span></div><div class="card"><b>100%</b><span>do valor de volta</span></div><div class="card"><b>Sem</b><span>burocracia</span></div></div>
  </div>
 </div>
</section>

<!-- 12. PLANOS -->
<section class="s alt" id="planos">
 <span class="hudt l" style="top:34px">QUEST.ACCEPT? // Y/N</span>
 <div class="s-in c">
  <span class="pill">⚔️ Planos</span>
  <h2 class="h"><span class="w">Escolha sua</span> <span class="g">jornada</span></h2>
  <p class="p">Pagamento único, sem mensalidade. Acesso imediato no celular.</p>
  <div class="plans">
   <div class="plan rv"><img class="top" src="/img/v3/ico-shield.webp" alt=""><h3>Recruta</h3><span class="for">O essencial para começar</span>
    <ul><li>App completo, com heróis e heroínas</li><li>Mais de 90 exercícios e aeróbico por tempo</li><li>Missões diárias e de emergência</li><li>Chefes e Zona de Penalidade</li><li>Loja: ícones, banners e wallpapers</li></ul>
    <span class="old">R$ 39,90</span><span class="pr"><small>R$</small>9<sup>,90</sup></span><span class="once">pagamento único</span>
    <a class="cta ghost" data-plan="recruta" href="https://appdigitalhub.com.br/c/43752C6D">Começar como Recruta</a></div>
   <div class="plan el rv"><img class="top" src="/img/v3/ico-crown.webp" alt=""><span class="rib">Mais escolhido</span><h3>Caçador Elite</h3><span class="for">A experiência completa</span>
    <ul><li>Tudo do plano Recruta</li><li>Os 3 Mestres, com 4 fichas de treino (inclui Glúteos e Pernas)</li><li>Dungeon de 30 dias e planilha de cargas</li><li>Corrida com GPS valendo XP</li><li>Taverna: a comunidade dentro do app</li><li>Alquimia: 50 receitas anabólicas</li></ul>
    <span class="old">R$ 79,90</span><span class="pr"><small>R$</small>26<sup>,90</sup></span><span class="once">pagamento único</span>
    <a class="cta" data-plan="elite" href="https://appdigitalhub.com.br/c/1C7E51FE">Evoluir para Elite {ARR}</a></div>
  </div>
 </div>
</section>

<!-- 13. FAQ -->
<section class="s" id="faq">
 <div class="s-in c">
  <span class="pill cy">❓ Dúvidas</span>
  <h2 class="h"><span class="w">Perguntas</span> <span class="g">frequentes</span></h2>
  <div class="faq">
{chr(10).join('   '+f for f in faqitems)}
  </div>
 </div>
</section>
</main>

'''
popup_and_tail=src[src.index('<!-- 10. RODAPÉ -->'):src.index('<script src="site.js')]
JS=open('/home/claude/arqjs.html',encoding='utf-8').read()
out=head+rest+'</head>\n<body>\n'+nav+body+popup_and_tail+'<script src="/v4.js?v=2"></script>\n<script src="/ab.js?v=1"></script>\n'+JS+'</body>\n</html>\n'
# absolute paths for any remaining relative img/ refs
out=re.sub(r'(src|href|srcset)="img/',r'\1="/img/',out)
dst=sys.argv[2] if len(sys.argv)>2 else 'site-v2/index.html'
if 'site-v2' in dst: out=out.replace('<meta charset="utf-8">','<meta charset="utf-8"><meta name="robots" content="noindex">',1)
import os;os.makedirs(os.path.dirname(dst) or '.',exist_ok=True)

# teste grátis (só na página nova do Brasil): bloco abaixo dos planos + pop-up de saída
TRIAL_BLK="""<!--fh-trial-->
<section style="position:relative;z-index:2;max-width:640px;margin:26px auto 40px;padding:0 16px">
 <div style="background:linear-gradient(160deg,rgba(20,60,40,.92),rgba(6,20,16,.95));border:2px solid #5dffa0;border-radius:16px;box-shadow:0 0 26px rgba(93,255,160,.22);padding:22px 20px;text-align:center;font-family:Jost,system-ui,sans-serif;color:#eafff2">
  <div style="font-weight:800;letter-spacing:.14em;font-size:12px;color:#5dffa0">[ SISTEMA ] · AINDA EM DÚVIDA?</div>
  <h3 style="margin:8px 0 6px;font-size:28px;font-weight:900">🎁 Teste grátis</h3>
  <p style="margin:0 auto 14px;max-width:440px;font-size:15.5px;line-height:1.5;color:#cfeedd">Use o <b>app completo</b> antes de pagar: Dungeon, chefes, os 3 Mestres e todas as fichas. Sem cartão, só e-mail e senha. Gostou? Escolha o seu plano e continue de onde parou.</p>
  <a href="/teste/" onclick="this.href='/teste/'+location.search;try{fbq('trackCustom','TrialClick',{src:'pagina'})}catch(e){}" style="display:inline-block;background:#5dffa0;color:#04140c;font-weight:900;font-size:17px;padding:14px 30px;border-radius:999px;text-decoration:none;box-shadow:0 6px 0 #1f8a52">Quero testar grátis</a>
 </div>
</section>
<!--/fh-trial-->"""
if 'site-v2' in dst:
    _a='</section>\n\n<!-- 13. FAQ -->'
    assert _a in out
    out=out.replace(_a,'</section>\n'+TRIAL_BLK+'\n\n<!-- 13. FAQ -->',1)
    out=out.replace('</body>','<script src="/exit-trial.js?v=1"></script>\n</body>',1)
open(dst,'w',encoding='utf-8').write(out);print('ok',dst,len(out))
