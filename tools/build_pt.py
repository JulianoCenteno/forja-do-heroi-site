#!/usr/bin/env python3
"""Gera a versão de Portugal (pt-PT, EUR) do quiz em /pt/index.html a partir de /quiz/index.html.
Rodar de novo sempre que o quiz brasileiro mudar."""
import os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = open(os.path.join(ROOT, 'quiz', 'index.html'), encoding='utf-8').read()
s = src

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
rep("https://appdigitalhub.com.br/c/B2535DA8", "https://appdigitalhub.com.br/c/BB7244F6")
rep("https://appdigitalhub.com.br/c/43752C6D", "https://appdigitalhub.com.br/c/9F9A8A75")
rep("https://appdigitalhub.com.br/c/E3082716", "https://appdigitalhub.com.br/c/124FED57")
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
    ('👑 Quero o plano completo por R$ 18,90', '👑 Quero o plano completo por 10,90 €'),
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
arep("https://appdigitalhub.com.br/c/1C7E51FE", "https://appdigitalhub.com.br/c/BB7244F6")
arep("https://appdigitalhub.com.br/c/E61E69D0", "https://appdigitalhub.com.br/c/D113479A")
arep("https://appdigitalhub.com.br/c/B04D52D9", "https://appdigitalhub.com.br/c/D2BFBAEE")
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
