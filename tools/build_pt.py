#!/usr/bin/env python3
"""Gera a versão de Portugal (pt-PT, EUR) do quiz em /pt/index.html a partir de /quiz/index.html.
Rodar de novo sempre que o quiz brasileiro mudar."""
import os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = open(os.path.join(ROOT, 'quiz', 'index.html'), encoding='utf-8').read()
s = src

# teste grátis e pop-up de saída são só do Brasil
s = re.sub(r"<!--fh-trial-->.*?<!--/fh-trial-->\n?", '', s, flags=re.S)
s = re.sub(r'<script src="/exit-trial\.js[^>]*></script>\n?', '', s)
s = re.sub(r"<script>/\* back redirect:.*?</script>\n", '', s, flags=re.S)
s = s.replace("window.TRY_URL=()=>'/teste/'+location.search;\n", '')
# a página de saída /quiz/back/ é só do Brasil (R$ e checkout BR): tirar do quiz de Portugal
s = re.sub(r"<script>/\* back redirect:.*?</script>\n", '', s, flags=re.S)

def rep(a, b, count=None, required=True):
    global s
    n = s.count(a)
    if required and n == 0:
        raise SystemExit('não encontrado: ' + a[:80])
    s = s.replace(a, b) if count is None else s.replace(a, b, count)

# ---------- moeda, preços e checkouts ----------
rep("const FULL=69, FINAL=29.90, TOTAL=+(FULL-FINAL).toFixed(2); // 39,10 de desconto em moedas",
    "const FULL=39, FINAL=16.90, TOTAL=+(FULL-FINAL).toFixed(2); // 22,10 € de crédito")
rep("const brl=v=>'R$ '+v.toFixed(2).replace('.',',');", "const brl=v=>v.toFixed(2).replace('.',',')+' €';")
# Checkout de Portugal. HOTMART=True troca para a Hotmart (MB WAY + Multibanco).
# Só ligar depois de os produtos 9030425 (Elite) e 9030504 (Recruta) estarem publicados na Hotmart.
HOTMART = False
if HOTMART:
    rep("https://appdigitalhub.com.br/c/B2535DA8", "https://pay.hotmart.com/D108593797I")           # Elite 16,90 €
    rep("https://appdigitalhub.com.br/c/43752C6D", "https://pay.hotmart.com/D108593797I?off=04y6zmzs")  # pop-up 10,90 €
    rep("https://appdigitalhub.com.br/c/E3082716", "https://pay.hotmart.com/W108593932U")           # Recruta 5,90 €
    rep('data-checkout="appdigitalhub.com.br/c/"', 'data-checkout="pay.hotmart,hotmart.com,pay.cakto,cakto.com.br"')
else:
    rep("https://appdigitalhub.com.br/c/B2535DA8", "https://pay.cakto.com.br/ujynffk_1345498")
    rep("https://appdigitalhub.com.br/c/43752C6D", "https://pay.cakto.com.br/6m4zcn2")
    rep("https://appdigitalhub.com.br/c/E3082716", "https://pay.cakto.com.br/38tgw96")
    rep('data-checkout="appdigitalhub.com.br/c/"', 'data-checkout="pay.cakto,cakto.com.br"')
rep("currency:'BRL'", "currency:'EUR'")
rep("value:18.9,", "value:10.9,")
rep("value:9.9,", "value:5.9,")
rep("'elite_29_90'", "'elite_16_90_eur'")
rep("'elite_popup_18_90'", "'elite_popup_10_90_eur'")
rep("'recruta_9_90'", "'recruta_5_90_eur'")
# crédito por pergunta proporcional (o total fecha sozinho na última pergunta)
s = re.sub(r"rw:(\d+)", lambda m: 'rw:%d' % (round(int(m.group(1)) * 2210 / 3910 / 10) * 10 if int(m.group(1)) else 0), s)
# textos com preço
for a, b in [
    ('⚔️ Resgatar por R$ 29,90', '⚔️ Resgatar por 16,90 €'),
    ('⚔️ Resgatar meu plano por R$ 29,90', '⚔️ Resgatar o meu plano por 16,90 €'),
    ('⚔️ Quero começar agora · R$ 29,90', '⚔️ Quero começar agora · 16,90 €'),
    ('<s>R$ 39,90</s><b>R$ 9,90</b>', '<s>14,90 €</s><b>5,90 €</b>'),
    ('Começar como Recruta · R$ 9,90', 'Começar como Recruta · 5,90 €'),
    ('<s>R$ 29,90</s><b>R$ 18,90</b>', '<s>16,90 €</s><b>10,90 €</b>'),
    ('Só R$ 9 a mais que o Recruta, pra ter o plano completo', 'Só 5 € a mais que o Recruta, para ter o plano completo'),
    ('✅ Sim, quero o completo por R$ 18,90', '✅ Sim, quero o completo por 10,90 €'),
    ('Não, quero só o Recruta por R$ 9,90', 'Não, quero só o Recruta por 5,90 €'),
    ('Elite por R$ 29,90 com o seu crédito aplicado, ou Recruta por R$ 9,90', 'Elite por 16,90 € com o seu crédito aplicado, ou Recruta por 5,90 €'),
    ('É pagamento único de R$ 29,90', 'É pagamento único de 16,90 €'),
]:
    rep(a, b, required=False)
rep('<span id="walv">R$ 0,00</span>', '<span id="walv">0,00 €</span>')
rep('<span id="coinv">− R$ 0,00</span>', '<span id="coinv">− 0,00 €</span>')
rep('<small>R$</small><span id="bigp">${FULL},00</span>', '<span id="bigp">${FULL},00</span><small style="margin-left:4px">€</small>')
rep("$('#bigp').textContent='29,90'", "$('#bigp').textContent='16,90'")
if 'R$' in s:
    left = re.findall(r'.{0,40}R\$.{0,40}', s)
    print('ATENÇÃO, ainda tem R$:', left[:8])

# ---------- métricas: marca o mercado ----------
rep("ua_mobile:MOB})", "ua_mobile:MOB,mkt:'pt'})")
rep("sessionStorage.getItem('fh_quiz_sid')", "sessionStorage.getItem('fh_quiz_sid_pt')")
rep("sessionStorage.setItem('fh_quiz_sid',v)", "sessionStorage.setItem('fh_quiz_sid_pt',v)")
rep("sessionStorage.getItem('fh_quiz')", "sessionStorage.getItem('fh_quiz_pt')")
rep("sessionStorage.setItem('fh_quiz',JSON.stringify(v))", "sessionStorage.setItem('fh_quiz_pt',JSON.stringify(v))")

# ---------- português de Portugal ----------
PT = [
    ('<html lang="pt-BR">', '<html lang="pt-PT">'),
    ('Calculando seus atributos', 'A calcular os teus atributos'),
    ('Lendo suas respostas', 'A ler as tuas respostas'),
    ('Definindo sua classe de herói', 'A definir a tua classe de herói'),
    ('Escolhendo o seu Mestre', 'A escolher o teu Mestre'),
    ('Montando a ficha de treino', 'A montar a ficha de treino'),
    ('Convertendo moedas em crédito', 'A converter moedas em crédito'),
    ('Forjando o seu plano', 'A forjar o teu plano'),
    ('Classe sendo forjada para', 'Classe a ser forjada para'),
    ('Missão registrada', 'Missão registada'),
    ('Registro do jogador', 'Registo do jogador'),
    ('Ficar com o shape marcado', 'Ficar com o corpo definido'),
    ('Na academia', 'No ginásio'),
    ('Preciso de academia?', 'Preciso de ginásio?'),
    ('academia', 'ginásio'),
    ('Academia', 'Ginásio'),
    ('celular', 'telemóvel'),
    ('Celular', 'Telemóvel'),
    ('CELULAR', 'TELEMÓVEL'),
    ('na tela de confirmação', 'no ecrã de confirmação'),
    ('Sem baixar nada da loja', 'Sem descarregar nada da loja'),
    ('Entrou, treinou e não curtiu?', 'Entrou, treinou e não gostou?'),
    ('Você curte games, anime ou RPG?', 'Gosta de videojogos, anime ou RPG?'),
    ('Funciona pra iniciante?', 'Funciona para principiantes?'),
    ('⚡ Pix ou cartão', '💳 Cartão de crédito ou débito'),
    ('Muito! Sou viciado', 'Muito! Sou viciado'),
    ('Já treinei, mas estou parado', 'Já treinei, mas estou parado'),
    (' pra ', ' para '),
    (' pro seu ', ' para o seu '),
    (' pro ', ' para o '),
    ('Pra começar', 'Para começar'),
    ('Seu primeiro nome', 'O seu primeiro nome'),
    ('Teste do Despertar · Forja do Herói', 'Teste do Despertar · Forja do Herói'),
]
for a, b in PT:
    s = s.replace(a, b)

# ---------- pt-PT a sério: forma "tu" (como nos aceleradores e no app PT) ----------
# Frases inteiras primeiro (a ordem importa). Cada uma tem de existir: se o quiz BR mudar, o build avisa.
TU = [
    # meta / partilha
    ('Responda o Teste do Despertar, descubra sua classe de herói e ganhe moedas que viram crédito no seu plano de treino.',
     'Faz o Teste do Despertar, descobre a tua classe de herói e ganha moedas que se tornam crédito no teu plano de treino.'),
    ('Descubra sua classe de herói e ganhe crédito no seu plano de treino.', 'Descobre a tua classe de herói e ganha crédito no teu plano de treino.'),
    # primeiro ecrã (sexo)
    ("q:()=>'Descubra sua <em>classe de herói</em>'", "q:()=>'Descobre a tua <em>classe de herói</em>'"),
    ("sub:'Responda em 2 minutos, ganhe <b style=\"color:#ffd767\">crédito em cada resposta</b> e receba um plano de treino feito para você. <b>Para começar, você é:</b>'",
     "sub:'Responde em 2 minutos, ganha <b style=\"color:#ffd767\">crédito em cada resposta</b> e recebe um plano de treino feito para ti. <b>Para começar, és:</b>'"),
    # nome
    ("q:()=>'Como o Sistema deve te chamar?'", "q:()=>'Como queres que o Sistema te chame?'"),
    ("sub:'Seu nome vai aparecer na sua ficha de '", "sub:'O teu nome vai aparecer na tua ficha de '"),
    ("ph:'O seu primeiro nome'", "ph:'O teu primeiro nome'"),
    # perguntas
    ("q:()=>'Qual é a sua idade?',sub:'O Sistema ajusta a intensidade ao seu corpo.'", "q:()=>'Que idade tens?',sub:'O Sistema ajusta a intensidade ao teu corpo.'"),
    ("q:()=>'Qual é a sua missão principal, '", "q:()=>'Qual é a tua missão principal, '"),
    ("q:()=>'Onde você vai treinar?',sub:'Isso define qual Mestre vai cuidar do seu treino.'", "q:()=>'Onde vais treinar?',sub:'Isto define que Mestre vai tratar do teu treino.'"),
    ("q:()=>'Como está o seu treino hoje?'", "q:()=>'Como está o teu treino hoje?'"),
    ("'Já treinei, mas estou parado'", "'Já treinei, mas parei'"),
    ("q:()=>'Quantos dias por semana você consegue treinar?'", "q:()=>'Quantos dias por semana consegues treinar?'"),
    ("q:()=>'Quanto tempo você tem por treino?'", "q:()=>'Quanto tempo tens para cada treino?'"),
    ("q:()=>'O que mais te atrapalha hoje?',sub:'Pode marcar mais de um.'", "q:()=>'O que mais te atrapalha hoje?',sub:'Podes escolher mais do que um.'"),
    ("'Não sei montar um treino certo'", "'Não sei montar um bom treino'"),
    ("q:()=>'Quantas vezes você já começou a treinar e parou?'", "q:()=>'Quantas vezes já começaste a treinar e desististe?'"),
    ("q:()=>'Quantas flexões você faz seguidas, sem parar?',sub:'Seja sincero: isso define seu rank inicial.'", "q:()=>'Quantas flexões consegues fazer seguidas?',sub:'Sê sincero: isto define o teu rank inicial.'"),
    ("q:()=>'Gosta de videojogos, anime ou RPG?'", "q:()=>'Gostas de videojogos, anime ou RPG?'"),
    ("q:()=>'Como está sua alimentação?'", "q:()=>'Como está a tua alimentação?'"),
    ("'Bem bagunçada'", "'Uma desgraça'"),
    ("'Tento comer bem, mas escorrego'", "'Tento comer bem, mas falho'"),
    ("q:()=>'Quantas horas você dorme por noite?'", "q:()=>'Quantas horas dormes por noite?'"),
    ("', se o Sistema te entregar um plano pronto, feito para você, você aceita a missão?'", "', se o Sistema te entregar um plano pronto, feito para ti, aceitas a missão?'"),
    ("'O Sistema vai te cobrar todo dia'", "'O Sistema vai puxar por ti todos os dias'"),
    ('🔒 Ninguém além do Sistema vê suas respostas.', '🔒 Só o Sistema vê as tuas respostas.'),
    # ecrã de entrada
    ('<h1>Descubra sua <em>classe de herói</em></h1>', '<h1>Descobre a tua <em>classe de herói</em></h1>'),
    ('Responda o <b>Teste do Despertar</b> e o Sistema monta um plano de treino feito para o seu corpo, seu objetivo e sua rotina.',
     'Faz o <b>Teste do Despertar</b> e o Sistema monta um plano de treino feito para o teu corpo, o teu objetivo e a tua rotina.'),
    ('No final, elas viram <b>crédito de verdade</b> para usar no seu plano.', 'No final, tornam-se <b>crédito a sério</b> para usares no teu plano.'),
    # intermédios
    ('deixa de improvisar na ginásio e passa a evoluir toda semana. Pra essa missão,', 'deixa de improvisar no ginásio e passa a evoluir todas as semanas. Para esta missão,'),
    ("'O problema nunca foi você'", "'O problema nunca foste tu'"),
    ('quem começa e para várias vezes não tem falta de força de vontade.', 'quem começa e desiste várias vezes não tem falta de força de vontade.'),
    ('<b>cada série vira XP</b>, você sobe de nível, enfrenta chefes e vê sua evolução todo dia.', '<b>cada série vale XP</b>, sobes de nível, enfrentas chefes e vês a tua evolução todos os dias.'),
    ('<li>✕ Para em 3 semanas</li>', '<li>✕ Desistes em 3 semanas</li>'),
    # resultado
    ("'Missões diárias, XP e chefes semanais te puxam de volta todo dia'", "'Missões diárias, XP e chefes semanais puxam por ti todos os dias'"),
    ("'Planilha de cargas e progressão automática: você vê a evolução em números'", "'Registo de cargas e progressão automática: vês a evolução em números'"),
    ("'x por semana, encaixados na sua rotina'", "'x por semana, encaixados na tua rotina'"),
    ("'Taverna e Alquimia: receitas e cálculo de proteína e água para o seu corpo'", "'Taverna e Alquimia: receitas e cálculo de proteína e água para o teu corpo'"),
    ("'Tudo no seu telemóvel, no seu ritmo, começando do nível certo para você'", "'Tudo no teu telemóvel, ao teu ritmo, a começar no nível certo para ti'"),
    ('${nm()}, sua ficha de herói está pronta', '${nm()}, a tua ficha de herói está pronta'),
    ('<small>SEU MESTRE</small>', '<small>O TEU MESTRE</small>'),
    ('SEUS INIMIGOS, DERROTADOS', 'OS TEUS INIMIGOS, DERROTADOS'),
    ('VEJA O APP POR DENTRO', 'VÊ A APP POR DENTRO'),
    ('É assim que fica o treino de ${nm()}: cada série vira XP, você sobe de nível e derrota chefes.', 'É assim que fica o treino de ${nm()}: cada série vale XP, sobes de nível e derrotas chefes.'),
    ('▶ O APP POR DENTRO', '▶ A APP POR DENTRO'),
    ('ESCOLHA SUA JORNADA', 'ESCOLHE A TUA JORNADA'),
    ('Acesso ao app com sistema de treino em RPG', 'Acesso à app com sistema de treino em RPG'),
    ('Seu crédito do teste não vale neste plano', 'O teu crédito do teste não conta neste plano'),
    ('🪙 SEU CRÉDITO FOI APLICADO · RECOMENDADO', '🪙 O TEU CRÉDITO FOI APLICADO · RECOMENDADO'),
    ('Começa com <b>${p.C[1]}</b> na sua ficha de', 'Começas com <b>${p.C[1]}</b> na tua ficha de'),
    ('escolha o seu mestre, cada um com fichas de treino exclusivas, e troque quando quiser', 'escolhe o teu mestre, cada um com fichas de treino exclusivas, e troca quando quiseres'),
    ('<b>Peso de cada série e planilha de cargas</b>: veja sua força subir', '<b>Peso de cada série e registo de cargas</b>: vê a tua força a subir'),
    ('para conversar, trocar dicas e mostrar sua evolução', 'para conversar, trocar dicas e mostrar a tua evolução'),
    ('<b>Alquimia</b>: receitas anabólicas e cálculo de proteína e água para o seu corpo', '<b>Alquimia</b>: receitas anabólicas e cálculo de proteína e água para o teu corpo'),
    ('🪙 Seu crédito do teste', '🪙 O teu crédito do teste'),
    ('<span>Você paga</span>', '<span>Pagas</span>'),
    ('pagamento único · acesso imediato no app', 'pagamento único · acesso imediato na app'),
    ('⏳ Seu crédito expira em', '⏳ O teu crédito expira em'),
    ('O QUE TE ESPERA NO APP', 'O QUE TE ESPERA NA APP'),
    ('converse, troque dicas, mostre seu treino e desafie outros heróis para um duelo.', 'conversa, troca dicas, mostra o teu treino e desafia outros heróis para um duelo.'),
    ('direto no app.', 'diretamente na app.'),
    ('Receitas anabólicas e o cálculo de proteína e água feitos para o seu corpo.', 'Receitas anabólicas e o cálculo de proteína e água feitos para o teu corpo.'),
    ('Desafios semanais que testam sua força e te dão recompensas raras.', 'Desafios semanais que testam a tua força e te dão recompensas raras.'),
    ('Entrou, treinou e não gostou? Pede o reembolso em até 7 dias e você recebe 100% de volta.', 'Entraste, treinaste e não gostaste? Pede o reembolso até 7 dias depois e recebes 100% de volta.'),
    ('<b>1. Entre no app</b>Acesso na hora, pelo telemóvel.', '<b>1. Entra na app</b>Acesso imediato, pelo telemóvel.'),
    ('<b>2. Escolha o seu Mestre</b>', '<b>2. Escolhe o teu Mestre</b>'),
    ('ou troque por outro dos 3 mestres', 'ou troca por outro dos 3 mestres'),
    ('O Sistema indicou ${p.C[1]} para você, mas você pode trocar quando quiser.', 'O Sistema indicou-te ${p.C[1]}, mas podes trocar quando quiseres.'),
    ('No Elite você treina com os 3 mestres.', 'No Elite treinas com os 3 mestres.'),
    ('<em>indicado para você</em>', '<em>indicado para ti</em>'),
    ('Comece com ${p.C[1]} na ficha de ${p.ficha}', 'Começa com ${p.C[1]} na ficha de ${p.ficha}'),
    ('<b>3. Suba de nível</b>Cada série vira XP. Derrote os chefes e veja seu corpo mudar.', '<b>3. Sobe de nível</b>Cada série vale XP. Derrota os chefes e vê o teu corpo mudar.'),
    ('Não. O app tem treino de calistenia', 'Não. A app tem treino de calistenia'),
    ('já foi escolhido pelo lugar onde você treina.', 'já foi escolhido pelo sítio onde treinas.'),
    ('É mensalidade?', 'É uma mensalidade?'),
    ('Elite por 16,90 € com o seu crédito aplicado', 'Elite por 16,90 € com o teu crédito aplicado'),
    ('No Recruta você registra seus próprios treinos e o app transforma tudo em XP, missões e chefes.', 'No Recruta registas os teus próprios treinos e a app transforma tudo em XP, missões e chefes.'),
    ('No Elite você escolhe um dos 3 mestres, cada um com fichas de treino exclusivas, e recebe o treino do dia pronto (o Sistema indicou ${p.C[1]} na ficha de ${p.ficha}), e você ganha a Dungeon de 30 dias, a planilha de cargas,',
     'No Elite escolhes um dos 3 mestres, cada um com fichas de treino exclusivas, e recebes o treino do dia pronto (o Sistema indicou-te ${p.C[1]} na ficha de ${p.ficha}), e ganhas a Dungeon de 30 dias, o registo de cargas,'),
    ('Assim que o pagamento é aprovado, você recebe o link do app no e-mail', 'Assim que o pagamento é aprovado, recebes o link da app no e-mail'),
    ('É só entrar com o e-mail da compra.', 'Basta entrares com o e-mail da compra.'),
    ('O Sistema começa do seu rank atual (${p.rank}) e aumenta a dificuldade conforme você evolui.', 'O Sistema começa no teu rank atual (${p.rank}) e aumenta a dificuldade à medida que evoluis.'),
    # pop-up
    ('No Recruta você treina <b>sem Mestre, sem ficha pronta e sem a Dungeon</b>. Sozinho, sem plano, é bem mais difícil de manter.',
     'No Recruta treinas <b>sem Mestre, sem ficha pronta e sem a Dungeon</b>. Sozinho, sem plano, é muito mais difícil manter.'),
    ('<span>Treino por sua conta</span>', '<span>Treinas por tua conta</span>'),
    ('monta seu treino</span>', 'monta o teu treino</span>'),
    ('ÚLTIMA OFERTA DO SISTEMA · SÓ NESTA TELA', 'ÚLTIMA OFERTA DO SISTEMA · SÓ NESTE ECRÃ'),
    ('aeróbico por tempo e exercícios criados por você', 'aeróbico por tempo e exercícios criados por ti'),
    ('Banners de classe que evoluem com você', 'Banners de classe que evoluem contigo'),
    ('Conforme você sobe de nível, libera formas mais fortes do seu herói', 'À medida que sobes de nível, desbloqueias formas mais fortes do teu herói'),
]
miss = [a for a, b in TU if a not in s]
if miss:
    raise SystemExit('pt-PT: não encontrado (o quiz BR mudou?):\n  ' + '\n  '.join(m[:90] for m in miss))
for a, b in TU:
    s = s.replace(a, b)
# o que ainda soar a Brasil fica listado aqui para rever
import re as _r
vis = _r.sub(r'<script[^>]*src=[^>]*></script>|<style.*?</style>', '', s, flags=_r.S)
left = sorted(set(m.group(0) for m in _r.finditer(r'\b(você|vocês|seu|sua|seus|suas|pra|vira|tela|planilha|registra)\b', vis)))
if left:
    print('pt-PT: ainda aparece', left)

# nomes de arquivos não podem ser traduzidos
s = s.replace('local-ginásio.webp', 'local-academia.webp')
out = os.path.join(ROOT, 'pt', 'index.html')
os.makedirs(os.path.dirname(out), exist_ok=True)
open(out, 'w', encoding='utf-8').write(s)
print('ok', out)

# ======================================================================
# App em português de Portugal: /pt/app/index.html (usa os arquivos de /app/ via <base>)
# ======================================================================
a = open(os.path.join(ROOT, 'app', 'index.html'), encoding='utf-8').read()
def arep(x, y, required=True):
    global a
    if required and x not in a:
        raise SystemExit('app: não encontrado: ' + x[:80])
    a = a.replace(x, y)
arep('<meta charset="utf-8">', '<meta charset="utf-8">\n<base href="/app/">', ) if '<meta charset="utf-8">' in a else arep('<head>', '<head>\n<base href="/app/">')
arep('<html lang="pt-BR">', '<html lang="pt-PT">', required=False)
# checkouts em euro
arep("https://appdigitalhub.com.br/c/1C7E51FE", "https://pay.cakto.com.br/ujynffk_1345498")
arep("https://appdigitalhub.com.br/c/E61E69D0", "https://pay.cakto.com.br/r3vyx2t")
arep("https://appdigitalhub.com.br/c/B04D52D9", "https://pay.cakto.com.br/38hzqdj")
for x, y in [('R$ 26,90', '16,90 €'), ('R$ 14,90', '8,90 €'), ('R$ 39,90', '19,90 €'), ('R$ 19,90', '10,90 €')]:
    a = a.replace(x, y)
# vocabulário pt-PT (só palavras inteiras)
WORDS = [
    ('celular', 'telemóvel'), ('Celular', 'Telemóvel'), ('celulares', 'telemóveis'),
    ('academia', 'ginásio'), ('Academia', 'Ginásio'),
    ('senha', 'palavra-passe'), ('Senha', 'Palavra-passe'),
    ('registrar', 'registar'), ('Registrar', 'Registar'), ('registrou', 'registou'), ('registrado', 'registado'), ('registrada', 'registada'),
    ('registro', 'registo'), ('Registro', 'Registo'), ('registros', 'registos'),
    ('salvar', 'guardar'), ('Salvar', 'Guardar'),
    ('usuário', 'utilizador'), ('Usuário', 'Utilizador'),
    ('geladeira', 'frigorífico'), ('suco', 'sumo'), ('Suco', 'Sumo'),
    ('Carregando', 'A carregar'),
    ('tela', 'ecrã'), ('Tela', 'Ecrã'),
]
import re as _re
for x, y in WORDS:
    a = _re.sub(r'(?<![\w\-./])' + _re.escape(x) + r'(?![\w\-])', y, a)
for x, y in [('café da manhã', 'pequeno-almoço'), ('Café da manhã', 'Pequeno-almoço'), ('Adicionar à Tela de Início', 'Adicionar ao ecrã principal'),
             ('Adicionar à ecrã de Início', 'Adicionar ao ecrã principal'), ('Adicionar à ecrã inicial', 'Adicionar ao ecrã principal'), ('sua ecrã', 'seu ecrã'), ('na ecrã', 'no ecrã'), ('da ecrã', 'do ecrã'), (' a ecrã', ' o ecrã'), ('Compartilhar', 'Partilhar'), ('Fala, caçador!', 'Olá, caçador!'), ('quilômetro', 'quilómetro'), ('Quilômetro', 'Quilómetro'), ('quilômetros', 'quilómetros'), ('em ecrã cheia', 'em ecrã inteiro'), ('ecrã cheia', 'ecrã inteiro')]:
    a = a.replace(x, y)
aout = os.path.join(ROOT, 'pt', 'app', 'index.html')
os.makedirs(os.path.dirname(aout), exist_ok=True)
open(aout, 'w', encoding='utf-8').write(a)
print('ok', aout)
