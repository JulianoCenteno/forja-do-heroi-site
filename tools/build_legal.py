# Gera /privacidade/, /termos/ e /excluir-conta/ (páginas legais exigidas pela Google Play e App Store)
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EMP = "DIGITAL MAKER LTDA"
CNPJ = "57.021.478/0001-15"
END = "Av. Doutor Urias Lugon, 114 – Columbia City, Guaíba/RS, CEP 92717-425, Brasil"
MAIL = "contato@digitalmakeroficial.com.br"
DATA = "20 de novembro de 2026"

TPL = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} · Forja do Herói</title>
<meta name="description" content="{desc}">
<link rel="icon" type="image/png" href="/app/icons/favicon-64.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@800&family=Fira+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<style>
:root{{--bg:#060914;--ink:#eef4ff;--mute:#c3d0e4;--cy:#4fd2ff;--gd:#ffcc4d;--line:rgba(79,210,255,.18)}}
*{{box-sizing:border-box}}
html,body{{margin:0;background:var(--bg);color:var(--ink);font:400 16px/1.65 "Fira Sans",system-ui,sans-serif}}
body{{background:radial-gradient(900px 420px at 50% -120px,rgba(79,210,255,.12),transparent 70%),var(--bg)}}
.wrap{{max-width:760px;margin:0 auto;padding:28px 20px 64px}}
.top{{display:flex;align-items:center;gap:12px;margin-bottom:28px}}
.top a{{color:var(--ink);text-decoration:none;font:800 18px "Cinzel",serif;letter-spacing:.04em}}
.top img{{width:36px;height:36px;border-radius:8px}}
h1{{font:800 clamp(26px,5vw,34px)/1.2 "Cinzel",serif;color:var(--gd);margin:0 0 6px}}
.upd{{color:var(--mute);font-size:14px;margin:0 0 28px}}
h2{{font:600 19px/1.35 "Fira Sans",sans-serif;color:var(--cy);margin:34px 0 8px}}
p,li{{color:var(--mute)}}
strong{{color:var(--ink)}}
a{{color:var(--cy)}}
ul{{padding-left:20px}}
li{{margin:4px 0}}
table{{width:100%;border-collapse:collapse;margin:12px 0;font-size:15px}}
th,td{{text-align:left;vertical-align:top;padding:10px 12px;border-bottom:1px solid var(--line)}}
th{{color:var(--ink);font-weight:600}}
.box p{{margin:0}}
.box{{border:1px solid var(--line);border-radius:12px;padding:16px 18px;background:rgba(79,210,255,.05);margin:18px 0}}
.foot{{margin-top:48px;padding-top:18px;border-top:1px solid var(--line);font-size:14px;color:var(--mute)}}
.foot a{{margin-right:16px}}
</style>
</head>
<body>
<div class="wrap">
<div class="top"><img src="/app/icons/favicon-64.png" alt=""><a href="/">Forja do Herói</a></div>
<h1>{title}</h1>
<p class="upd">Última atualização: {data}</p>
{body}
<div class="foot">
<p><a href="/privacidade/">Política de privacidade</a><a href="/termos/">Termos de uso</a><a href="/excluir-conta/">Excluir conta</a></p>
<p>Forja do Herói é um produto da {emp} · CNPJ {cnpj} · {end} · <a href="mailto:{mail}">{mail}</a></p>
</div>
</div>
</body>
</html>
"""

PRIV = f"""
<p>Esta política explica quais dados o <strong>Forja do Herói</strong> (site, quiz e aplicativo, inclusive as versões da Google Play e da App Store) coleta, por que coleta e o que você pode fazer com eles. O responsável pelo tratamento dos dados (controlador) é a <strong>{EMP}</strong>, CNPJ {CNPJ}, {END}.</p>

<h2>1. Dados que coletamos</h2>
<table>
<tr><th>Dado</th><th>Para quê</th></tr>
<tr><td>Nome e e-mail</td><td>Criar e identificar sua conta e liberar o plano que você comprou ou assinou.</td></tr>
<tr><td>Dados do herói e dos treinos (classe, peso corporal informado, exercícios, séries, repetições, cargas, XP, conquistas)</td><td>Fazer o app funcionar, calcular sua evolução e guardar o backup do seu progresso.</td></tr>
<tr><td>Localização aproximada e precisa, só durante a corrida com GPS</td><td>Medir distância, tempo e ritmo da corrida. A localização não é coletada fora da corrida nem em segundo plano.</td></tr>
<tr><td>Posts, comentários e mensagens na Taverna</td><td>Mostrar seu conteúdo para outros usuários na comunidade do app.</td></tr>
<tr><td>Respostas do quiz</td><td>Montar o resultado do teste e a recomendação de plano.</td></tr>
<tr><td>Dados da compra (produto, valor, data, status)</td><td>Liberar o acesso, cumprir obrigações fiscais e atender reembolsos. Os dados do cartão ficam com a plataforma de pagamento e nunca passam por nós.</td></tr>
<tr><td>Dados de navegação e cookies no site e no quiz (páginas vistas, origem do anúncio, identificadores de cookie)</td><td>Medir os resultados dos nossos anúncios.</td></tr>
<tr><td>Mensagens de feedback que você envia no app</td><td>Melhorar o app e, se você autorizar, exibir o depoimento.</td></tr>
</table>

<h2>2. Bases legais</h2>
<p>Tratamos seus dados para executar o contrato com você (fazer o app funcionar e liberar o plano), cumprir obrigações legais (registros fiscais), com base no nosso legítimo interesse (segurança, prevenção de fraude e melhoria do produto) e com o seu consentimento (cookies de anúncios no site, localização da corrida e uso de depoimentos). Esta política segue a Lei Geral de Proteção de Dados (Lei 13.709/2018) e, para usuários na União Europeia, o Regulamento Geral sobre a Proteção de Dados (RGPD).</p>

<h2>3. Com quem compartilhamos</h2>
<p>Não vendemos seus dados. Compartilhamos apenas o necessário com fornecedores que nos ajudam a operar o Forja do Herói:</p>
<ul>
<li><strong>Hospedagem e banco de dados:</strong> Vercel e Supabase.</li>
<li><strong>Pagamentos:</strong> Digital Hub Vendas e Cakto (compras feitas no site), Google Play e Apple App Store (assinaturas feitas nos aplicativos das lojas).</li>
<li><strong>Medição de anúncios:</strong> Meta (Facebook e Instagram) e Digital Hub Tracker, que recebem eventos de navegação e de compra para medir campanhas.</li>
<li><strong>Autoridades:</strong> quando a lei ou uma ordem judicial exigir.</li>
</ul>
<p>Alguns desses fornecedores guardam dados fora do Brasil. Nesses casos, exigimos garantias de proteção compatíveis com a LGPD e o RGPD.</p>

<h2>4. Por quanto tempo guardamos</h2>
<p>Guardamos os dados da conta e do progresso enquanto a conta estiver ativa. Quando você pede a exclusão, apagamos esses dados em até 15 dias. Registros de compra são mantidos pelo prazo exigido pela legislação fiscal (até 5 anos).</p>

<h2>5. Seus direitos</h2>
<p>Você pode, a qualquer momento: confirmar se tratamos seus dados, acessá-los, corrigi-los, pedir uma cópia (portabilidade), pedir a exclusão, revogar um consentimento e se opor a um tratamento. Para isso, escreva para <a href="mailto:{MAIL}">{MAIL}</a>. Para apagar sua conta, veja <a href="/excluir-conta/">Excluir conta</a>. Você também pode reclamar à Autoridade Nacional de Proteção de Dados (ANPD) ou, na União Europeia, à autoridade do seu país (em Portugal, a CNPD).</p>

<h2>6. Segurança</h2>
<p>Usamos conexão criptografada (HTTPS), controle de acesso ao banco de dados e acesso restrito à equipe. Nenhum sistema é 100% seguro: se houver um incidente que afete seus dados, avisaremos você e as autoridades conforme a lei.</p>

<h2>7. Idade mínima</h2>
<p>O Forja do Herói é destinado a pessoas a partir de 16 anos. Menores de 18 anos devem usar o app com autorização e acompanhamento de um responsável. Se soubermos que coletamos dados de uma criança sem autorização, apagaremos esses dados.</p>

<h2>8. Mudanças nesta política</h2>
<p>Podemos atualizar esta política. A data no topo mostra a última versão. Se a mudança for importante, avisaremos no app ou por e-mail.</p>

<h2>9. Contato</h2>
<p>{EMP} · <a href="mailto:{MAIL}">{MAIL}</a></p>
"""

TERMOS = f"""
<p>Estes termos regem o uso do <strong>Forja do Herói</strong> (site, quiz e aplicativo, inclusive as versões da Google Play e da App Store), oferecido pela <strong>{EMP}</strong>, CNPJ {CNPJ}. Ao criar uma conta ou usar o app, você concorda com estes termos e com a <a href="/privacidade/">Política de privacidade</a>.</p>

<h2>1. O que é o Forja do Herói</h2>
<p>Um aplicativo de treino gamificado: seus treinos geram pontos de experiência (XP), níveis, missões, chefes e rankings. O app organiza e motiva seus treinos, mas <strong>não é um serviço médico</strong> e não substitui a orientação de um médico, nutricionista ou profissional de educação física.</p>

<h2>2. Saúde e segurança</h2>
<ul>
<li>Antes de começar qualquer programa de exercícios, consulte um médico, principalmente se tiver doença, lesão, gestação ou estiver sem treinar há muito tempo.</li>
<li>Respeite seus limites. Pare imediatamente se sentir dor, tontura, falta de ar ou mal-estar.</li>
<li>As receitas da Alquimia e os materiais em PDF são informativos. Verifique alergias e restrições alimentares.</li>
<li>Na corrida com GPS, fique atento ao trânsito e ao ambiente. Não use o celular enquanto atravessa ruas.</li>
</ul>

<h2>3. Conta</h2>
<p>Você é responsável pelas informações da sua conta e pelo que acontece nela. A conta é pessoal e não pode ser compartilhada ou revendida. Podemos suspender contas que violem estes termos.</p>

<h2>4. Planos, pagamentos e cancelamento</h2>
<p><strong>Compras no site</strong> (pagamento único, processado pela Digital Hub Vendas ou pela Cakto): o acesso ao plano comprado é liberado no e-mail da compra e não tem mensalidade. Você tem <strong>7 dias de garantia</strong>: se pedir o reembolso nesse prazo, devolvemos o valor integral.</p>
<p><strong>Assinaturas nos aplicativos da Google Play e da App Store:</strong></p>
<ul>
<li>O plano Caçador Elite é oferecido como assinatura mensal ou anual, com <strong>7 dias de teste grátis</strong> para quem ainda não usou o teste.</li>
<li>Ao fim do teste, a assinatura é cobrada na sua conta da loja e <strong>renova automaticamente</strong> a cada período, pelo preço mostrado na hora da compra, até você cancelar.</li>
<li>A renovação é cobrada nas 24 horas antes do fim do período atual. Para não ser cobrado, cancele até 24 horas antes do fim do teste ou do período.</li>
<li>O cancelamento é feito nos ajustes da loja: na Google Play, em Pagamentos e assinaturas; no iPhone, em Ajustes › seu nome › Assinaturas. Ao cancelar, o acesso continua até o fim do período já pago.</li>
<li>Reembolsos de assinaturas feitas nas lojas seguem a política da Google Play ou da Apple.</li>
</ul>
<p>Quem comprou um plano no site entra no app da loja com o mesmo e-mail e mantém o acesso comprado, sem precisar assinar.</p>

<h2>5. Taverna e conteúdo dos usuários</h2>
<p>Você é responsável pelo que publica na Taverna. É proibido publicar conteúdo ofensivo, discriminatório, sexual, violento, ilegal, spam, propaganda ou dados pessoais de outras pessoas. Podemos remover conteúdo e suspender contas que descumpram estas regras. Você pode denunciar um post ou bloquear um usuário dentro do app ou pelo e-mail <a href="mailto:{MAIL}">{MAIL}</a>. Ao publicar, você nos autoriza a exibir esse conteúdo dentro do app.</p>

<h2>6. Ranking e jogo limpo</h2>
<p>Registros impossíveis ou falsos podem ser bloqueados, e o XP ganho com eles pode ser removido. Ouro, XP, títulos e itens do jogo não têm valor em dinheiro e não podem ser trocados ou transferidos.</p>

<h2>7. Propriedade intelectual</h2>
<p>A marca Forja do Herói, os personagens, as artes, os textos, os treinos e o software pertencem à {EMP} ou a seus licenciadores. Você pode usar o app para uso pessoal, mas não pode copiar, revender ou distribuir o conteúdo.</p>

<h2>8. Disponibilidade e responsabilidade</h2>
<p>Trabalhamos para manter o app no ar, mas ele pode ficar indisponível por manutenção ou falhas. O app é oferecido como está. Na medida permitida pela lei, não respondemos por lesões causadas por exercícios feitos sem orientação adequada, nem por perdas indiretas. Nada nestes termos limita os direitos garantidos pelo Código de Defesa do Consumidor ou pela legislação de consumo do seu país.</p>

<h2>9. Mudanças nos termos</h2>
<p>Podemos atualizar estes termos. A data no topo mostra a última versão. Se a mudança for importante, avisaremos no app ou por e-mail antes de ela valer.</p>

<h2>10. Lei aplicável</h2>
<p>Estes termos seguem a lei brasileira. Fica eleito o foro do domicílio do consumidor. Consumidores na União Europeia mantêm os direitos garantidos pela lei do seu país.</p>

<h2>11. Contato</h2>
<p>{EMP} · CNPJ {CNPJ} · <a href="mailto:{MAIL}">{MAIL}</a></p>
"""

EXCL = f"""
<p>Você pode pedir a exclusão da sua conta do <strong>Forja do Herói</strong> e dos dados ligados a ela a qualquer momento.</p>

<div class="box">
<p><strong>Como pedir:</strong> envie um e-mail para <a href="mailto:{MAIL}?subject=Excluir%20conta%20Forja%20do%20Her%C3%B3i">{MAIL}</a> a partir do e-mail cadastrado na sua conta, com o assunto <strong>“Excluir conta Forja do Herói”</strong>. Respondemos confirmando o pedido e concluímos a exclusão em até 15 dias.</p>
</div>

<h2>O que é apagado</h2>
<ul>
<li>Nome, e-mail e dados da conta.</li>
<li>Dados do herói e todo o histórico de treinos, XP, conquistas e corridas.</li>
<li>Posts, comentários e mensagens na Taverna.</li>
<li>Mensagens de feedback.</li>
</ul>

<h2>O que é mantido</h2>
<p>Registros de compra (produto, valor, data e e-mail da compra) ficam guardados pelo prazo exigido pela legislação fiscal (até 5 anos) e depois são apagados. Eles não são usados para nenhuma outra finalidade.</p>

<h2>Assinaturas</h2>
<p>Excluir a conta <strong>não cancela</strong> uma assinatura feita na Google Play ou na App Store. Cancele antes nos ajustes da loja: na Google Play, em Pagamentos e assinaturas; no iPhone, em Ajustes › seu nome › Assinaturas.</p>

<h2>Dados salvos no aparelho</h2>
<p>O app também guarda uma cópia do seu progresso no próprio aparelho. Para apagá-la, desinstale o app ou limpe os dados do site no navegador.</p>
"""

PAGES = [
    ("privacidade", "Política de privacidade", "Como o Forja do Herói coleta, usa e protege seus dados.", PRIV),
    ("termos", "Termos de uso", "Regras de uso do app Forja do Herói, planos, assinaturas e cancelamento.", TERMOS),
    ("excluir-conta", "Excluir conta", "Como pedir a exclusão da sua conta e dos seus dados do Forja do Herói.", EXCL),
]

for slug, title, desc, body in PAGES:
    d = os.path.join(ROOT, slug)
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f:
        f.write(TPL.format(title=title, desc=desc, data=DATA, body=body, emp=EMP, cnpj=CNPJ, end=END, mail=MAIL))
    print("ok", slug)
