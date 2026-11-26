#!/usr/bin/env python3
"""Gera a versão em espanhol (LatAm/Espanha, US$) do quiz em /es/index.html a partir de /quiz/index.html.
Rodar de novo sempre que o quiz brasileiro mudar. Checkouts: Cakto (USD)."""
import os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
from es_links import ES  # links de checkout da Cakto (preenchidos quando os produtos forem criados)

src = open(os.path.join(ROOT, 'quiz', 'index.html'), encoding='utf-8').read()
s = src

# teste grátis e pop-up de saída são só do Brasil
s = re.sub(r"<!--fh-trial-->.*?<!--/fh-trial-->\n?", '', s, flags=re.S)
s = re.sub(r'<script src="/exit-trial\.js[^>]*></script>\n?', '', s)
s = re.sub(r"<script>/\* back redirect:.*?</script>\n", '', s, flags=re.S)
s = s.replace("window.TRY_URL=()=>'/teste/'+location.search;\n", '')
MISS = []

def rep(a, b, required=True):
    global s
    if a not in s:
        if required:
            MISS.append(a[:90])
        return
    s = s.replace(a, b)

# ---------- moeda, preços, checkouts, métricas ----------
rep("const CHECKOUT='https://appdigitalhub.com.br/c/B2535DA8',CHECKOUT_R='https://appdigitalhub.com.br/c/43752C6D',CHECKOUT_POP='https://appdigitalhub.com.br/c/E3082716';",
    "const CHECKOUT='%s',CHECKOUT_R='%s',CHECKOUT_POP='%s';" % (ES['elite'], ES['recruta'], ES['elite_pop']))
rep('data-checkout="appdigitalhub.com.br/c/"', 'data-checkout="pay.cakto,cakto.com.br"')
rep("const FULL=69, FINAL=29.90, TOTAL=+(FULL-FINAL).toFixed(2); // 39,10 de desconto em moedas",
    "const FULL=29, FINAL=12.90, TOTAL=+(FULL-FINAL).toFixed(2); // US$ 16.10 de crédito")
rep("const brl=v=>'R$ '+v.toFixed(2).replace('.',',');", "const brl=v=>'US$ '+v.toFixed(2);")
rep("currency:'BRL'", "currency:'USD'")
rep("value:18.9,", "value:8.9,")
rep("value:9.9,", "value:4.9,")
rep("'elite_29_90'", "'elite_12_90_usd'")
rep("'elite_popup_18_90'", "'elite_popup_8_90_usd'")
rep("'recruta_9_90'", "'recluta_4_90_usd'")
s = re.sub(r"rw:(\d+)", lambda m: 'rw:%d' % (round(int(m.group(1)) * 1610 / 3910 / 10) * 10 if int(m.group(1)) else 0), s)
rep("ua_mobile:MOB})", "ua_mobile:MOB,mkt:'es'})")
for k in ["'fh_quiz_sid'", "'fh_quiz'", "'fh_quiz_end'", "'fh_quiz_mute'"]:
    rep(k, k[:-1] + "_es'", required=False)
rep('<span id="walv">R$ 0,00</span>', '<span id="walv">US$ 0.00</span>')
rep('<span id="coinv">− R$ 0,00</span>', '<span id="coinv">− US$ 0.00</span>')
rep('<small>R$</small><span id="bigp">${FULL},00</span>', '<small>US$</small><span id="bigp">${FULL}.00</span>')
rep("$('#bigp').textContent=pay.toFixed(2).replace('.',',')", "$('#bigp').textContent=pay.toFixed(2)")
rep("$('#bigp').textContent='29,90'", "$('#bigp').textContent='12.90'")

T = [
    # ---- head ----
    ('<html lang="pt-BR">', '<html lang="es">'),
    ('<title>Teste do Despertar · Forja do Herói</title>', '<title>Prueba del Despertar · Forja do Herói</title>'),
    ('content="Responda o Teste do Despertar, descubra sua classe de herói e ganhe moedas que viram crédito no seu plano de treino."',
     'content="Responde la Prueba del Despertar, descubre tu clase de héroe y gana monedas que se convierten en crédito para tu plan de entrenamiento."'),
    ('content="Teste do Despertar · Forja do Herói"', 'content="Prueba del Despertar · Forja do Herói"'),
    ('content="Descubra sua classe de herói e ganhe crédito no seu plano de treino."', 'content="Descubre tu clase de héroe y gana crédito para tu plan de entrenamiento."'),
    ('<span class="lvl" id="lvl">NV 1</span>', '<span class="lvl" id="lvl">NV 1</span>'),
    ('← voltar', '← volver'),
    ('aria-label="Som"', 'aria-label="Sonido"'),
    ('⚔️ Resgatar por R$ 29,90', '⚔️ Canjear por US$ 12.90'),
    # ---- nomes ----
    ("fem()?'Caçadora':'Caçador'", "fem()?'Cazadora':'Cazador'"),
    (":'Caçador';", ":'Cazador';"),
    # ---- perguntas ----
    ("cap:'[ SISTEMA ] · Teste do Despertar',q:()=>'Descubra sua <em>classe de herói</em>',sub:'Responda em 2 minutos, ganhe <b style=\"color:#ffd767\">crédito em cada resposta</b> e receba um plano de treino feito pra você. <b>Pra começar, você é:</b>'",
     "cap:'[ SISTEMA ] · Prueba del Despertar',q:()=>'Descubre tu <em>clase de héroe</em>',sub:'Responde en 2 minutos, gana <b style=\"color:#ffd767\">crédito en cada respuesta</b> y recibe un plan de entrenamiento hecho para ti. <b>Para empezar, eres:</b>'"),
    ("['m','Homem',", "['m','Hombre',"), ("['f','Mulher',", "['f','Mujer',"),
    ("cap:'Registro do jogador',q:()=>'Como o Sistema deve te chamar?',sub:'Seu nome vai aparecer na sua ficha de '+(fem()?'heroína':'herói')+'.',ph:'Seu primeiro nome'",
     "cap:'Registro del jugador',q:()=>'¿Cómo debe llamarte el Sistema?',sub:'Tu nombre aparecerá en tu ficha de '+(fem()?'heroína':'héroe')+'.',ph:'Tu nombre'"),
    ("cap:'Ficha do jogador',q:()=>'Qual é a sua idade?',sub:'O Sistema ajusta a intensidade ao seu corpo.',opts:[['18','18 a 24 anos','🗡️'],['25','25 a 34 anos','🛡️'],['35','35 a 44 anos','⚔️'],['45','45 anos ou mais','👑']]",
     "cap:'Ficha del jugador',q:()=>'¿Cuál es tu edad?',sub:'El Sistema ajusta la intensidad a tu cuerpo.',opts:[['18','18 a 24 años','🗡️'],['25','25 a 34 años','🛡️'],['35','35 a 44 años','⚔️'],['45','45 años o más','👑']]"),
    ("cap:'Missão principal',q:()=>'Qual é a sua missão principal, '+nm()+'?',get opts(){const b=[['massa','Ganhar massa muscular','💪','Ficar maior e mais forte'],['emag','Perder gordura','🔥','Secar e ganhar disposição'],['forca','Ficar mais forte','🏋️','Levantar mais peso, ter mais força'],['def','Definir o corpo','⚡','Ficar com o shape marcado']];return fem()?[['glu','Glúteos e pernas','🍑','Pernas fortes e glúteo empinado'],...b]:b}",
     "cap:'Misión principal',q:()=>'¿Cuál es tu misión principal, '+nm()+'?',get opts(){const b=[['massa','Ganar masa muscular','💪','Ser más grande y más fuerte'],['emag','Perder grasa','🔥','Bajar de peso y tener más energía'],['forca','Ser más fuerte','🏋️','Levantar más peso, tener más fuerza'],['def','Definir el cuerpo','⚡','Marcar el abdomen y los músculos']];return fem()?[['glu','Glúteos y piernas','🍑','Piernas fuertes y glúteos firmes'],...b]:b}"),
    ("cap:'Campo de batalha',q:()=>'Onde você vai treinar?',sub:'Isso define qual Mestre vai cuidar do seu treino.',opts:[['acad','Na academia',",
     "cap:'Campo de batalla',q:()=>'¿Dónde vas a entrenar?',sub:'Esto define qué Maestro cuidará de tu entrenamiento.',opts:[['acad','En el gimnasio',"),
    ("['casa','Em casa',", "['casa','En casa',"), ("['parque','No parque / ar livre',", "['parque','En el parque / al aire libre',"), ("['misto','Um pouco de cada',", "['misto','Un poco de cada uno',"),
    ("cap:'Nível de experiência',q:()=>'Como está o seu treino hoje?',opts:[['zero','Nunca treinei de verdade','🌱'],['parado','Já treinei, mas estou parado','⏸️'],['inic','Treino há pouco tempo','📈'],['inter','Treino há mais de 1 ano','🔥']]",
     "cap:'Nivel de experiencia',q:()=>'¿Cómo va tu entrenamiento hoy?',opts:[['zero','Nunca entrené de verdad','🌱'],['parado','Ya entrené, pero lo dejé','⏸️'],['inic','Entreno desde hace poco','📈'],['inter','Entreno desde hace más de 1 año','🔥']]"),
    ("cap:'Disponibilidade',q:()=>'Quantos dias por semana você consegue treinar?',opts:[['2','2 dias','2️⃣'],['3','3 dias','3️⃣'],['4','4 dias','4️⃣'],['5','5 dias ou mais','🔥']]",
     "cap:'Disponibilidad',q:()=>'¿Cuántos días por semana puedes entrenar?',opts:[['2','2 días','2️⃣'],['3','3 días','3️⃣'],['4','4 días','4️⃣'],['5','5 días o más','🔥']]"),
    ("cap:'Tempo de batalha',q:()=>'Quanto tempo você tem por treino?',opts:[['20','Até 20 minutos','⏱️'],['40','30 a 45 minutos','⌛'],['60','1 hora ou mais','🕐']]",
     "cap:'Tiempo de batalla',q:()=>'¿Cuánto tiempo tienes por entrenamiento?',opts:[['20','Hasta 20 minutos','⏱️'],['40','30 a 45 minutos','⌛'],['60','1 hora o más','🕐']]"),
    ("cap:'Inimigos ocultos',q:()=>'O que mais te atrapalha hoje?',sub:'Pode marcar mais de um.',opts:[['motiv','Perco a motivação em poucas semanas','😮‍💨'],['saber','Não sei montar um treino certo','🤷'],['result','Treino e não vejo resultado','📉'],['tempo','Falta de tempo e rotina corrida','⏰'],['comida','Não sei o que comer','🍔'],['vergonha','Vergonha ou insegurança de começar','🙈']]",
     "cap:'Enemigos ocultos',q:()=>'¿Qué es lo que más te frena hoy?',sub:'Puedes marcar más de uno.',opts:[['motiv','Pierdo la motivación en pocas semanas','😮‍💨'],['saber','No sé armar una rutina correcta','🤷'],['result','Entreno y no veo resultados','📉'],['tempo','Falta de tiempo y rutina agitada','⏰'],['comida','No sé qué comer','🍔'],['vergonha','Vergüenza o inseguridad para empezar','🙈']]"),
    ("cap:'Histórico de batalhas',q:()=>'Quantas vezes você já começou a treinar e parou?',opts:[['0','Nunca, vai ser a primeira vez','✨'],['1','1 ou 2 vezes','🔁'],['3','3 a 5 vezes','😅'],['9','Já perdi as contas','💀']]",
     "cap:'Historial de batallas',q:()=>'¿Cuántas veces empezaste a entrenar y lo dejaste?',opts:[['0','Nunca, será la primera vez','✨'],['1','1 o 2 veces','🔁'],['3','3 a 5 veces','😅'],['9','Ya perdí la cuenta','💀']]"),
    ("cap:'Teste de força',q:()=>'Quantas flexões você faz seguidas, sem parar?',sub:'Seja sincero: isso define seu rank inicial.',opts:[['0','Nenhuma ou quase nenhuma','🥚'],['8','De 1 a 10','🐣'],['20','De 11 a 25','🐺'],['30','Mais de 25','🐉']]",
     "cap:'Prueba de fuerza',q:()=>'¿Cuántas flexiones haces seguidas, sin parar?',sub:'Sé sincero: esto define tu rango inicial.',opts:[['0','Ninguna o casi ninguna','🥚'],['8','De 1 a 10','🐣'],['20','De 11 a 25','🐺'],['30','Más de 25','🐉']]"),
    ("cap:'Perfil de jogador',q:()=>'Você curte games, anime ou RPG?',opts:[['muito','Muito! Sou viciado','🎮'],['pouco','Um pouco','🙂'],['nada','Não muito, mas quero resultado','🎯']]",
     "cap:'Perfil de jugador',q:()=>'¿Te gustan los videojuegos, el anime o los RPG?',opts:[['muito','¡Mucho! Soy fanático','🎮'],['pouco','Un poco','🙂'],['nada','No mucho, pero quiero resultados','🎯']]"),
    ("cap:'Nutrição do herói',q:()=>'Como está sua alimentação?',opts:[['bagunca','Bem bagunçada','🍕'],['tento','Tento comer bem, mas escorrego','⚖️'],['ok','Como bem na maior parte do tempo','🥗']]",
     "cap:'Nutrición del héroe',q:()=>'¿Cómo es tu alimentación?',opts:[['bagunca','Bastante desordenada','🍕'],['tento','Intento comer bien, pero fallo','⚖️'],['ok','Como bien la mayor parte del tiempo','🥗']]"),
    ("cap:'Recuperação',q:()=>'Quantas horas você dorme por noite?',opts:[['5','Menos de 6 horas','😵'],['7','6 a 7 horas','😴'],['8','8 horas ou mais','🛌']]",
     "cap:'Recuperación',q:()=>'¿Cuántas horas duermes por noche?',opts:[['5','Menos de 6 horas','😵'],['7','6 a 7 horas','😴'],['8','8 horas o más','🛌']]"),
    ("cap:'Juramento',q:()=>nm()+', se o Sistema te entregar um plano pronto, feito pra você, você aceita a missão?',opts:[['sim','Sim, aceito a missão!','⚔️','Quero começar já'],['talvez','Aceito, mas preciso de ajuda pra manter','🤝','O Sistema vai te cobrar todo dia']]",
     "cap:'Juramento',q:()=>nm()+', si el Sistema te entrega un plan listo, hecho para ti, ¿aceptas la misión?',opts:[['sim','¡Sí, acepto la misión!','⚔️','Quiero empezar ya'],['talvez','Acepto, pero necesito ayuda para no dejarlo','🤝','El Sistema te lo recordará todos los días']]"),
    # ---- HUD / render ----
    ("'<small>DE CRÉDITO</small>'", "'<small>DE CRÉDITO</small>'"),
    ("<small>NÍVEL '", "<small>NIVEL '"),
    ('PERGUNTA ${answered()+1} DE ${QN} · vale <b style="color:#ffd767">${brl(s.rw/100)} de crédito</b>', 'PREGUNTA ${answered()+1} DE ${QN} · vale <b style="color:#ffd767">${brl(s.rw/100)} de crédito</b>'),
    ('id="ok" disabled>Confirmar</button><p class="hint">🔒 Ninguém além do Sistema vê suas respostas.</p>', 'id="ok" disabled>Confirmar</button><p class="hint">🔒 Nadie más que el Sistema ve tus respuestas.</p>'),
    ('<span>⏱️ 2 minutos</span><span>🎯 ${QN} perguntas</span><span>🪙 até ${brl(TOTAL)} em crédito</span>', '<span>⏱️ 2 minutos</span><span>🎯 ${QN} preguntas</span><span>🪙 hasta ${brl(TOTAL)} en crédito</span>'),
    ("'disabled'}>Continuar</button>", "'disabled'}>Continuar</button>"),
    # ---- intro ----
    ('alt="Forja do Herói"', 'alt="Forja do Herói"'),
    ('[ SISTEMA ] · Novo jogador detectado', '[ SISTEMA ] · Nuevo jugador detectado'),
    ('<h1>Descubra sua <em>classe de herói</em></h1>', '<h1>Descubre tu <em>clase de héroe</em></h1>'),
    ('Responda o <b>Teste do Despertar</b> e o Sistema monta um plano de treino feito pro seu corpo, seu objetivo e sua rotina.', 'Responde la <b>Prueba del Despertar</b> y el Sistema arma un plan de entrenamiento hecho para tu cuerpo, tu objetivo y tu rutina.'),
    ('Cada resposta vale <b>moedas de ouro</b>. No final, elas viram <b>crédito de verdade</b> pra usar no seu plano.', 'Cada respuesta vale <b>monedas de oro</b>. Al final, se convierten en <b>crédito real</b> para usar en tu plan.'),
    ('⚔️ Começar o teste', '⚔️ Empezar la prueba'),
    # ---- interstícios ----
    ("massa:['ganhar massa','Mestre Brutus é especialista em hipertrofia'],emag:['perder gordura','o Sistema combina treino e cardio pra acelerar a queima'],forca:['ficar mais forte','a ficha de Força trabalha carga pesada e poucas repetições'],def:['definir o corpo','a ficha certa combina força e gasto calórico'],glu:['fortalecer glúteos e pernas','os mestres criaram uma ficha só de glúteos, pernas e abdômen']}[A.obj]||['evoluir','']",
     "massa:['ganar masa','el Maestro Brutus es especialista en hipertrofia'],emag:['perder grasa','el Sistema combina entrenamiento y cardio para acelerar la quema'],forca:['ser más fuerte','la ficha de Fuerza trabaja carga pesada y pocas repeticiones'],def:['definir el cuerpo','la ficha correcta combina fuerza y gasto calórico'],glu:['fortalecer glúteos y piernas','los maestros crearon una ficha solo de glúteos, piernas y abdomen']}[A.obj]||['evolucionar','']"),
    ('<div class="cap g">Missão registrada</div><h2>Boa escolha, ${nm()}</h2>', '<div class="cap g">Misión registrada</div><h2>Buena elección, ${nm()}</h2>'),
    ('Missão de <b>${o[0]}</b> confirmada. Quem treina com um objetivo claro e um plano pronto deixa de improvisar na academia e passa a evoluir toda semana. Pra essa missão, ${o[1]}.',
     'Misión de <b>${o[0]}</b> confirmada. Quien entrena con un objetivo claro y un plan listo deja de improvisar en el gimnasio y empieza a evolucionar cada semana. Para esta misión, ${o[1]}.'),
    ('Continuar o teste →', 'Continuar la prueba →'),
    ('<div class="cap g">O Sistema analisou</div>', '<div class="cap g">El Sistema analizó</div>'),
    ("${many?'O problema nunca foi você':'Agora vai ser diferente'}", "${many?'El problema nunca fuiste tú':'Esta vez será diferente'}"),
    ('${nm()}, quem começa e para várias vezes não tem falta de força de vontade. Tem falta de <b>recompensa</b>. Treino comum não te dá nada no dia seguinte, e o cérebro desiste.',
     '${nm()}, quien empieza y lo deja varias veces no tiene falta de fuerza de voluntad. Tiene falta de <b>recompensa</b>. Un entrenamiento común no te da nada al día siguiente, y el cerebro se rinde.'),
    ('${nm()}, o maior inimigo de quem começa é a falta de recompensa: o resultado demora a aparecer e a motivação acaba antes.',
     '${nm()}, el mayor enemigo de quien empieza es la falta de recompensa: el resultado tarda en llegar y la motivación se acaba antes.'),
    ('No Forja do Herói, <b>cada série vira XP</b>, você sobe de nível, enfrenta chefes e vê sua evolução todo dia.', 'En Forja do Herói, <b>cada serie se convierte en XP</b>, subes de nivel, enfrentas jefes y ves tu evolución todos los días.'),
    ('<b>TREINO COMUM</b><ul><li>✕ Treino solto, sem plano</li><li>✕ Nada muda no dia seguinte</li><li>✕ Para em 3 semanas</li></ul>', '<b>ENTRENO COMÚN</b><ul><li>✕ Entreno suelto, sin plan</li><li>✕ Nada cambia al día siguiente</li><li>✕ Lo dejas en 3 semanas</li></ul>'),
    ('<b>FORJA DO HERÓI</b><ul><li>✓ Plano pronto por um Mestre</li><li>✓ XP, níveis e chefes</li><li>✓ Missões diárias que te puxam</li></ul>', '<b>FORJA DO HERÓI</b><ul><li>✓ Plan listo de un Maestro</li><li>✓ XP, niveles y jefes</li><li>✓ Misiones diarias que te impulsan</li></ul>'),
    # ---- loading ----
    ('<h2>Forjando o seu plano</h2>', '<h2>Forjando tu plan</h2>'),
    ('Classe sendo forjada para <b>${nm()}</b>…', 'Clase forjándose para <b>${nm()}</b>…'),
    ("['Lendo suas respostas','Calculando seus atributos','Definindo sua classe de herói','Escolhendo o seu Mestre','Montando a ficha de treino','Convertendo moedas em crédito']",
     "['Leyendo tus respuestas','Calculando tus atributos','Definiendo tu clase de héroe','Eligiendo a tu Maestro','Armando tu ficha de entrenamiento','Convirtiendo monedas en crédito']"),
    # ---- perfil ----
    ("guerreiro:['Guerreiro','Mestre Brutus','Mestre do Ferro','musculação com um grupo muscular por dia'],monge:['Monge','Mestre Kaito','Mestre da Calistenia','treino com o peso do corpo, em casa ou no parque'],paladino:['Paladino','Mestra Aurora','Mestra Híbrida','barra e ferro no mesmo treino']",
     "guerreiro:['Guerrero','Maestro Brutus','Maestro del Hierro','pesas con un grupo muscular por día'],monge:['Monje','Maestro Kaito','Maestro de la Calistenia','entrenamiento con el peso del cuerpo, en casa o en el parque'],paladino:['Paladín','Maestra Aurora','Maestra Híbrida','barra y pesas en el mismo entrenamiento']"),
    ("{massa:'Hipertrofia',def:'Hipertrofia',forca:'Força',emag:'Emagrecimento',glu:'Glúteos e Pernas'}[A.obj]||'Hipertrofia'", "{massa:'Hipertrofia',def:'Hipertrofia',forca:'Fuerza',emag:'Pérdida de grasa',glu:'Glúteos y Piernas'}[A.obj]||'Hipertrofia'"),
    ("motiv:['Perde a motivação','Missões diárias, XP e chefes semanais te puxam de volta todo dia']", "motiv:['Pierdes la motivación','Misiones diarias, XP y jefes semanales te traen de vuelta todos los días']"),
    ("saber:['Não sabe montar o treino',p.C[1]+' entrega o treino do dia pronto: séries, repetições e carga']", "saber:['No sabes armar la rutina',p.C[1]+' te da el entrenamiento del día listo: series, repeticiones y carga']"),
    ("result:['Não vê resultado','Planilha de cargas e progressão automática: você vê a evolução em números']", "result:['No ves resultados','Registro de cargas y progresión automática: ves tu evolución en números']"),
    ("tempo:['Falta de tempo','Treinos de '+(A.tempo==='20'?'20':A.tempo==='40'?'30 a 45':'60')+' minutos, '+(A.dias||3)+'x por semana, encaixados na sua rotina']", "tempo:['Falta de tiempo','Entrenamientos de '+(A.tempo==='20'?'20':A.tempo==='40'?'30 a 45':'60')+' minutos, '+(A.dias||3)+' veces por semana, adaptados a tu rutina']"),
    ("comida:['Não sabe o que comer','Taverna e Alquimia: receitas e cálculo de proteína e água pro seu corpo']", "comida:['No sabes qué comer','Taberna y Alquimia: recetas y cálculo de proteína y agua para tu cuerpo']"),
    ("vergonha:['Insegurança de começar','Tudo no seu celular, no seu ritmo, começando do nível certo pra você']", "vergonha:['Inseguridad para empezar','Todo en tu celular, a tu ritmo, empezando desde el nivel correcto para ti']"),
    # ---- resultado ----
    ('[ SISTEMA ] · Análise concluída', '[ SISTEMA ] · Análisis completado'),
    ('<h2>${nm()}, sua ficha de herói está pronta</h2>', '<h2>${nm()}, tu ficha de héroe está lista</h2>'),
    ('· CLASSE ${p.C[0].toUpperCase()}', '· CLASE ${p.C[0].toUpperCase()}'),
    ('RANK INICIAL <b>${p.rank}</b> → meta em 30 dias:', 'RANGO INICIAL <b>${p.rank}</b> → meta en 30 días:'),
    ('<small>SEU MESTRE</small>', '<small>TU MAESTRO</small>'), ('<small>FICHA DE TREINO</small>', '<small>FICHA DE ENTRENO</small>'),
    ('<small>FREQUÊNCIA</small>', '<small>FRECUENCIA</small>'), ("x por semana</b>", " por semana</b>"), ('<small>ESTILO</small>', '<small>ESTILO</small>'),
    ('SEUS INIMIGOS, DERROTADOS', 'TUS ENEMIGOS, DERROTADOS'),
    ('VEJA O APP POR DENTRO', 'MIRA LA APP POR DENTRO'),
    ('É assim que fica o treino de ${nm()}: cada série vira XP, você sobe de nível e derrota chefes.', 'Así se ve el entrenamiento de ${nm()}: cada serie se convierte en XP, subes de nivel y derrotas jefes.'),
    ('▶ O APP POR DENTRO', '▶ LA APP POR DENTRO'),
    ('ESCOLHA SUA JORNADA', 'ELIGE TU AVENTURA'),
    ('<b>Recruta</b><small>O essencial para começar</small></div><div class="o2p"><s>R$ 39,90</s><b>R$ 9,90</b>', '<b>Recluta</b><small>Lo esencial para empezar</small></div><div class="o2p"><s>US$ 14.90</s><b>US$ 4.90</b>'),
    ('<span>Acesso ao app com sistema de treino em RPG</span>', '<span>Acceso a la app con sistema de entrenamiento RPG</span>'),
    ('<span>Missões diárias e de emergência, chefes e evolução de nível</span>', '<span>Misiones diarias y de emergencia, jefes y subida de nivel</span>'),
    ('<span>Mais de 90 exercícios, aeróbico por tempo e exercícios criados por você</span>', '<span>Más de 90 ejercicios, cardio por tiempo y ejercicios creados por ti</span>'),
    ('<span>Loja com ícones, banners que evoluem e papéis de parede</span>', '<span>Tienda con íconos, banners que evolucionan y fondos de pantalla</span>'),
    ('<span>Sem os Mestres, sem fichas prontas e sem a Dungeon</span>', '<span>Sin los Maestros, sin fichas listas y sin la Mazmorra</span>'),
    ('<span>Sem Taverna, Alquimia e Playlist</span>', '<span>Sin Taberna, Alquimia ni Playlist</span>'),
    ('<span>Seu crédito do teste não vale neste plano</span>', '<span>Tu crédito de la prueba no vale en este plan</span>'),
    ('Começar como Recruta · R$ 9,90', 'Empezar como Recluta · US$ 4.90'),
    ('🪙 SEU CRÉDITO FOI APLICADO · RECOMENDADO', '🪙 TU CRÉDITO FUE APLICADO · RECOMENDADO'),
    ('<h3>${hero()} Elite · plano completo</h3>', '<h3>${hero()} Élite · plan completo</h3>'),
    ('<span><b>Os 3 Mestres do Forja</b>: escolha o seu mestre, cada um com fichas de treino exclusivas, e troque quando quiser</span>', '<span><b>Los 3 Maestros del Forja</b>: elige a tu maestro, cada uno con fichas de entrenamiento exclusivas, y cámbialo cuando quieras</span>'),
    ('<span>Começa com <b>${p.C[1]}</b> na sua ficha de <b>${p.ficha}</b>: treino do dia pronto, com séries, repetições e carga</span>', '<span>Empiezas con <b>${p.C[1]}</b> en tu ficha de <b>${p.ficha}</b>: entrenamiento del día listo, con series, repeticiones y carga</span>'),
    ('<span><b>Dungeon de 30 dias</b> com chefes semanais</span>', '<span><b>Mazmorra de 30 días</b> con jefes semanales</span>'),
    ('<span><b>Peso de cada série e planilha de cargas</b>: veja sua força subir</span>', '<span><b>Peso de cada serie y registro de cargas</b>: mira cómo sube tu fuerza</span>'),
    ('<span><b>Taverna</b>: a comunidade dos caçadores, pra conversar, trocar dicas e mostrar sua evolução</span>', '<span><b>Taberna</b>: la comunidad de cazadores, para conversar, compartir consejos y mostrar tu evolución</span>'),
    ('<span><b>Alquimia</b>: receitas anabólicas e cálculo de proteína e água pro seu corpo</span>', '<span><b>Alquimia</b>: recetas altas en proteína y cálculo de proteína y agua para tu cuerpo</span>'),
    ('<span><b>Playlist do Herói</b>: músicas pra treinar no modo monstro</span>', '<span><b>Playlist del Héroe</b>: música para entrenar en modo bestia</span>'),
    ('<span><b>Missões de emergência, Zona de Penalidade, chefes, ranking, duelos e corrida com GPS</b></span>', '<span><b>Misiones de emergencia, Zona de Penalización, jefes, ranking, duelos y carrera con GPS</b></span>'),
    ('<span><b>Mais de 90 exercícios</b>, aeróbico por tempo e exercícios criados por você</span>', '<span><b>Más de 90 ejercicios</b>, cardio por tiempo y ejercicios creados por ti</span>'),
    ('<span><b>Banners de classe que evoluem com você</b>, ícones premium e papéis de parede HD</span>', '<span><b>Banners de clase que evolucionan contigo</b>, íconos premium y fondos de pantalla HD</span>'),
    ('<span><b>4 fichas de treino</b>: Hipertrofia, Força, Emagrecimento e <b>Glúteos e Pernas</b></span>', '<span><b>4 fichas de entrenamiento</b>: Hipertrofia, Fuerza, Pérdida de grasa y <b>Glúteos y Piernas</b></span>'),
    ('<b>⚔️ Seu herói evolui</b><span>Conforme você sobe de nível, libera formas mais fortes do seu herói: armadura, capa e até asas de energia no nível 50.</span>', '<b>⚔️ Tu héroe evoluciona</b><span>A medida que subes de nivel, desbloqueas formas más fuertes de tu héroe: armadura, capa y hasta alas de energía en el nivel 50.</span>'),
    ('<summary>Tem treino pra mulher?</summary><p>Tem. As heroínas têm arte própria e, no Elite, os mestres passam a ficha de <b>Glúteos e Pernas</b>, com dias de glúteo, quadríceps e superior leve, na academia ou em casa. Tem até chefe próprio: a Serpente do Hip Thrust.</p>', '<summary>¿Hay entrenamiento para mujeres?</summary><p>Sí. Las heroínas tienen arte propio y, en Élite, los maestros te dan la ficha de <b>Glúteos y Piernas</b>, con días de glúteo, cuádriceps y tren superior ligero, en el gimnasio o en casa. Hasta tiene jefe propio: la Serpiente del Hip Thrust.</p>'),
    ('<span>Valor do plano</span>', '<span>Valor del plan</span>'), ('<span>🪙 Seu crédito do teste</span>', '<span>🪙 Tu crédito de la prueba</span>'), ('<span>Você paga</span>', '<span>Pagas</span>'),
    ('pagamento único · acesso imediato no app', 'pago único · acceso inmediato en la app'),
    ('⚔️ Resgatar meu plano por R$ 29,90', '⚔️ Canjear mi plan por US$ 12.90'),
    ('⏳ Seu crédito expira em', '⏳ Tu crédito vence en'),
    ('<span>🔒 Pagamento seguro</span><span>⚡ Pix ou cartão</span><span>📱 Funciona no celular</span>', '<span>🔒 Pago seguro</span><span>💳 Tarjeta de crédito o débito</span><span>📱 Funciona en el celular</span>'),
    ('O QUE TE ESPERA NO APP', 'LO QUE TE ESPERA EN LA APP'),
    ('<b>🍺 Taverna</b><span>A comunidade dos caçadores: converse, troque dicas, mostre seu treino e desafie outros heróis pra um duelo.</span>', '<b>🍺 Taberna</b><span>La comunidad de cazadores: conversa, comparte consejos, muestra tu entrenamiento y reta a otros héroes a un duelo.</span>'),
    ('<b>🎧 Playlist do Herói</b><span>Músicas escolhidas pra treinar com a energia lá em cima, direto no app.</span>', '<b>🎧 Playlist del Héroe</b><span>Música elegida para entrenar con la energía al máximo, directo en la app.</span>'),
    ('<b>⚗️ Alquimia</b><span>Receitas anabólicas e o cálculo de proteína e água feitos pro seu corpo.</span>', '<b>⚗️ Alquimia</b><span>Recetas altas en proteína y el cálculo de proteína y agua hechos para tu cuerpo.</span>'),
    ('<b>👹 Chefes e Dungeon</b><span>Desafios semanais que testam sua força e te dão recompensas raras.</span>', '<b>👹 Jefes y Mazmorra</b><span>Desafíos semanales que ponen a prueba tu fuerza y te dan recompensas raras.</span>'),
    ('<b>Garantia de 7 dias.</b> Entrou, treinou e não curtiu? Pede o reembolso em até 7 dias e você recebe 100% de volta.', '<b>Garantía de 7 días.</b> ¿Entraste, entrenaste y no te gustó? Pide el reembolso dentro de los 7 días y recibes el 100% de vuelta.'),
    ('COMO FUNCIONA', 'CÓMO FUNCIONA'),
    ('<b>1. Entre no app</b>Acesso na hora, pelo celular. Sem baixar nada da loja.', '<b>1. Entra a la app</b>Acceso inmediato, desde el celular. Sin descargar nada de la tienda.'),
    ('<b>2. Escolha o seu Mestre</b>Comece com ${p.C[1]} na ficha de ${p.ficha} ou troque por outro dos 3 mestres. Treino novo todo dia.', '<b>2. Elige a tu Maestro</b>Empieza con ${p.C[1]} en la ficha de ${p.ficha} o cámbialo por otro de los 3 maestros. Entrenamiento nuevo cada día.'),
    ('<b>3. Suba de nível</b>Cada série vira XP. Derrote os chefes e veja seu corpo mudar.', '<b>3. Sube de nivel</b>Cada serie se convierte en XP. Derrota a los jefes y mira cómo cambia tu cuerpo.'),
    ('<div class="sec-h">DÚVIDAS</div>', '<div class="sec-h">PREGUNTAS</div>'),
    ('<summary>Preciso de academia?</summary><p>Não. O app tem treino de calistenia (peso do corpo), musculação e híbrido. ${p.C[1]} já foi escolhido pelo lugar onde você treina.</p>', '<summary>¿Necesito gimnasio?</summary><p>No. La app tiene entrenamiento de calistenia (peso del cuerpo), pesas e híbrido. ${p.C[1]} ya fue elegido según el lugar donde entrenas.</p>'),
    ('<summary>É mensalidade?</summary><p>Não. Os dois planos são pagamento único: Elite por R$ 29,90 com o seu crédito aplicado, ou Recruta por R$ 9,90.</p>', '<summary>¿Es una mensualidad?</summary><p>No. Los dos planes son de pago único: Élite por US$ 12.90 con tu crédito aplicado, o Recluta por US$ 4.90. Se cobra en dólares y tu banco lo convierte a tu moneda.</p>'),
    ('<summary>Qual a diferença entre os planos?</summary><p>No Recruta você registra seus próprios treinos e o app transforma tudo em XP, missões e chefes. No Elite você escolhe um dos 3 mestres, cada um com fichas de treino exclusivas, e recebe o treino do dia pronto (o Sistema indicou ${p.C[1]} na ficha de ${p.ficha}), e você ganha a Dungeon de 30 dias, a planilha de cargas, a Taverna e a Alquimia.</p>',
     '<summary>¿Cuál es la diferencia entre los planes?</summary><p>En Recluta registras tus propios entrenamientos y la app convierte todo en XP, misiones y jefes. En Élite eliges uno de los 3 maestros, cada uno con fichas de entrenamiento exclusivas, y recibes el entrenamiento del día listo (el Sistema te recomendó a ${p.C[1]} en la ficha de ${p.ficha}), y además tienes la Mazmorra de 30 días, el registro de cargas, la Taberna y la Alquimia.</p>'),
    ('<summary>Como recebo o acesso?</summary><p>Assim que o pagamento é aprovado, você recebe o link do app no e-mail e na tela de confirmação. É só entrar com o e-mail da compra.</p>', '<summary>¿Cómo recibo el acceso?</summary><p>Apenas se aprueba el pago, recibes el enlace de la app en tu correo y en la pantalla de confirmación. Solo entra con el correo de la compra.</p>'),
    ('<summary>Funciona pra iniciante?</summary><p>Sim. O Sistema começa do seu rank atual (${p.rank}) e aumenta a dificuldade conforme você evolui.</p>', '<summary>¿Funciona para principiantes?</summary><p>Sí. El Sistema empieza desde tu rango actual (${p.rank}) y aumenta la dificultad a medida que evolucionas.</p>'),
    ('⚔️ Quero começar agora · R$ 29,90', '⚔️ Quiero empezar ahora · US$ 12.90'),
    ('<p class="foot">Forja do Herói · Treino RPG</p>', '<p class="foot">Forja do Herói · Entrenamiento RPG</p>'),
    ('<div class="sec-h">ESCOLHA O SEU MESTRE</div>', '<div class="sec-h">ELIGE A TU MAESTRO</div>'),
    ('No Elite você treina com os 3 mestres. Cada um tem as suas fichas de treino exclusivas. O Sistema indicou ${p.C[1]} pra você, mas você pode trocar quando quiser.', 'En Élite entrenas con los 3 maestros. Cada uno tiene sus fichas de entrenamiento exclusivas. El Sistema te recomendó a ${p.C[1]}, pero puedes cambiarlo cuando quieras.'),
    ("[['guerreiro','Mestre Brutus','Mestre do Ferro','Musculação na academia, um grupo muscular por dia'],['monge','Mestre Kaito','Mestre da Calistenia','Peso do corpo, em casa ou no parque'],['paladino','Mestra Aurora','Mestra Híbrida','Barra e ferro no mesmo treino']]", "[['guerreiro','Maestro Brutus','Maestro del Hierro','Pesas en el gimnasio, un grupo muscular por día'],['monge','Maestro Kaito','Maestro de la Calistenia','Peso corporal, en casa o en el parque'],['paladino','Maestra Aurora','Maestra Híbrida','Barra y pesas en el mismo entrenamiento']]"),
    ("<em>indicado pra você</em>", "<em>recomendado para ti</em>"),
    # ---- pop-up ----
    ('aria-label="Fechar"', 'aria-label="Cerrar"'),
    ('<h2 style="font-size:24px">Espera, ${nm()}!</h2>', '<h2 style="font-size:24px">¡Espera, ${nm()}!</h2>'),
    ('No Recruta você treina <b>sem Mestre, sem ficha pronta e sem a Dungeon</b>. Sozinho, sem plano, é bem mais difícil de manter.', 'En Recluta entrenas <b>sin Maestro, sin ficha lista y sin la Mazmorra</b>. Solo y sin plan, es mucho más difícil no abandonar.'),
    ('<b>RECRUTA</b><span>Treino por sua conta</span><span>Sem plano de ${p.ficha}</span><span>Sem Taverna e Playlist</span>', '<b>RECLUTA</b><span>Entrenas por tu cuenta</span><span>Sin plan de ${p.ficha}</span><span>Sin Taberna ni Playlist</span>'),
    ('<b>CAÇADOR ELITE</b><span>${p.C[1]} monta seu treino</span><span>Dungeon de 30 dias pronta</span><span>Taverna, Alquimia e Playlist</span>', '<b>CAZADOR ÉLITE</b><span>${p.C[1]} arma tu entrenamiento</span><span>Mazmorra de 30 días lista</span><span>Taberna, Alquimia y Playlist</span>'),
    ('<small>ÚLTIMA OFERTA DO SISTEMA · SÓ NESTA TELA</small><div><s>R$ 29,90</s><b>R$ 18,90</b></div><span>Só R$ 9 a mais que o Recruta, pra ter o plano completo</span>', '<small>ÚLTIMA OFERTA DEL SISTEMA · SOLO EN ESTA PANTALLA</small><div><s>US$ 12.90</s><b>US$ 8.90</b></div><span>Solo US$ 4 más que Recluta, para tener el plan completo</span>'),
    ('✅ Sim, quero o completo por R$ 18,90', '✅ Sí, quiero el completo por US$ 8.90'),
    ('Não, quero só o Recruta por R$ 9,90', 'No, solo quiero Recluta por US$ 4.90'),
]
for a, b in T:
    rep(a, b)

if MISS:
    print('NÃO ENCONTRADO:'); [print('  -', m) for m in MISS]; raise SystemExit(1)

# checagem de português que sobrou (fora de identificadores)
vis = re.sub(r'<style.*?</style>', '', s, flags=re.S)
left = re.findall(r"[^\n]{0,30}(?:\bvocê\b|\bseu\b|\bsua\b|\bnão\b|\btreino\b|ção\b|ções\b|R\$)[^\n]{0,30}", vis)
if left:
    print('ATENÇÃO, possível português:'); [print('  ~', l) for l in left[:20]]
out = os.path.join(ROOT, 'es', 'index.html')
os.makedirs(os.path.dirname(out), exist_ok=True)
open(out, 'w', encoding='utf-8').write(s)
print('ok', out)
