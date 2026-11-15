"""Gera /es/app e /en/app a partir do app em português.
Uso: python3 build_app.py   (rodar sempre que o app em PT mudar)"""
import json, glob, os, re

R = '/home/claude/forja-do-heroi-site'
H = os.path.dirname(os.path.abspath(__file__))
clean = json.load(open(f'{H}/clean.json'))

LANG = {
 'es': dict(col=1, html='es', num='es', brand='La Forja del Héroe',
   desc='Tu entrenamiento se volvió un RPG: gana XP, sube de nivel y haz evolucionar a tu héroe.',
   checkout='https://appdigitalhub.com.br/c/ES_ELITE', site='https://forjadoheroi.com/es/#planos'),
 'en': dict(col=2, html='en', num='en-US', brand="Hero's Forge",
   desc='Your workout just became an RPG: earn XP, level up and evolve your hero.',
   checkout='https://appdigitalhub.com.br/c/EN_ELITE', site='https://forjadoheroi.com/en/#planos'),
}


def load_dict(col):
    d = {}
    for f in sorted(glob.glob(f'{H}/tr_*.tsv')):
        for ln in open(f, encoding='utf-8'):
            ln = ln.rstrip('\n')
            if not ln.strip() or ln.startswith('#'):
                continue
            p = ln.split('\t') + ['', '']
            if p[0].isdigit():
                pt = clean[int(p[0])]
                tr = p[col]
            else:               # linhas extras: pt \t es \t en
                pt, tr = p[0], p[col]
            if pt.strip() and tr != pt:
                d[pt.strip()] = tr.strip()
    return d


src = open(f'{R}/app/index.html', encoding='utf-8').read()
rt = open(f'{H}/i18n_rt.js', encoding='utf-8').read()
sw = open(f'{R}/app/sw.js', encoding='utf-8').read()
man = json.load(open(f'{R}/app/manifest.webmanifest'))

for lang, L in LANG.items():
    D = load_dict(L['col'])
    base = f'/{lang}/app/'
    s = src

    def rep(a, b, must=True):
        global s
        if a not in s:
            if must:
                raise SystemExit(f'[{lang}] trecho não encontrado: {a[:80]}')
            return
        s = s.replace(a, b)

    rep('<html lang="pt-BR">', f'<html lang="{L["html"]}">')
    rep('<head>\n', '<head>\n<base href="/app/">\n')
    rep('<link rel="manifest" href="/app/manifest.webmanifest">', f'<link rel="manifest" href="{base}manifest.webmanifest">')
    rep('<meta name="apple-mobile-web-app-title" content="Forja do Herói">', f'<meta name="apple-mobile-web-app-title" content="{L["brand"]}">')
    rep("const CHECKOUT_ELITE='https://appdigitalhub.com.br/c/1C7E51FE';", f"const CHECKOUT_ELITE='{L['checkout']}';")
    rep("const FH_SITE='https://forjadoheroi.com/#planos';", f"const FH_SITE='{L['site']}';")
    rep("const DUEL_URL='https://forjadoheroi.com/app/?duelo=';", f"const DUEL_URL='https://forjadoheroi.com{base}?duelo=';")
    rep("const u=location.origin+'/app/';", f"const u=location.origin+'{base}';")
    rep("location.origin}/app/</p>", "location.origin}"+base+"</p>")
    rep("fetch('/app/?vc='+Date.now()", f"fetch('{base}?vc='+Date.now()")
    rep("navigator.serviceWorker.register('/app/sw.js',{scope:'/app/'})", f"navigator.serviceWorker.register('{base}sw.js',{{scope:'{base}'}})")
    s = s.replace("['D','S','T','Q','Q','S','S']", "['D','L','M','M','J','V','S']" if lang == 'es' else "['S','M','T','W','T','F','S']")
    s = s.replace("toLocaleString('pt-BR')", f"toLocaleString('{L['num']}')").replace("toLocaleDateString('pt-BR')", f"toLocaleDateString('{L['num']}')")
    rep("tz:Intl.DateTimeFormat().resolvedOptions().timeZone||'America/Sao_Paulo',enabled:true,", "tz:Intl.DateTimeFormat().resolvedOptions().timeZone||'America/Sao_Paulo',lang:" + json.dumps(lang) + ",enabled:true,")
    if lang == 'en':
        s = s.replace(".replace('.',',')", "")
    # imagens com texto traduzido (ficam em /xx/app/img/)
    for f in sorted(glob.glob(f'{R}{base}img/*.webp')):
        nm = os.path.basename(f)
        if nm == 'logo.webp':
            s = s.replace('src="img/logo.webp"', f'src="{base}img/logo.webp"')
        else:
            s = s.replace(nm, f'../../..{base}img/{nm}')
    # idioma salvo no aparelho (usado pelas notificações do servidor)
    inject = ('<script>try{localStorage.setItem("fh-lang",' + json.dumps(lang) + ')}catch(e){}window.FH_LANG=' + json.dumps(lang) +
              ';window.FH_DICT=' + json.dumps(D, ensure_ascii=False) + ';</script>\n<script>' + rt + '</script>\n')
    if lang == 'es':
        inject = '<style>.top .brand{font-size:13.5px!important;letter-spacing:.03em!important}.top .brand small{letter-spacing:.22em!important}</style>\n' + inject
    rep('<script src="supabase.js"></script>', inject + '<script src="supabase.js"></script>')
    os.makedirs(f'{R}{base}', exist_ok=True)
    open(f'{R}{base}index.html', 'w', encoding='utf-8').write(s)

    # service worker e manifest próprios (escopo /xx/app/)
    w = sw.replace("'/app/?tab=treinar'", f"'{base}?tab=treinar'").replace("|| '/app/'", f"|| '{base}'").replace("c.url.includes('/app/')", f"c.url.includes('{base}')")
    if lang == 'es':
        w = w.replace("'[SISTEMA] Missão diária'", "'[SISTEMA] Misión diaria'").replace("'Chegou a hora do treino, jogador.'", "'Llegó la hora de entrenar, jugador.'")
    else:
        w = w.replace("'[SISTEMA]'", "'[SYSTEM]'").replace("'[SISTEMA] Missão diária'", "'[SYSTEM] Daily quest'").replace("'Chegou a hora do treino, jogador.'", "'Time to train, player.'")
    open(f'{R}{base}sw.js', 'w', encoding='utf-8').write(w)
    m = dict(man, name=L['brand'], short_name=L['brand'], description=L['desc'], id=base, start_url=base, scope=base, lang=L['html'])
    json.dump(m, open(f'{R}{base}manifest.webmanifest', 'w'), ensure_ascii=False, indent=2)
    print(lang, 'ok', len(D), 'termos')
