# Gera prévias (noindex, sem métricas) do quiz e do site com a opção "Teste grátis".
import re
def common(s, base):
    s=s.replace('<meta charset="utf-8">','<meta charset="utf-8"><base href="%s"><meta name="robots" content="noindex,nofollow">'%base,1)
    s=re.sub(r"fbq\('init','\d+'\);fbq\('track','PageView'\);","",s)          # sem pixel na prévia
    s=s.replace("https://lpdicrpetxqnoxceozfa.supabase.co/rest/v1/fh_quiz_events","about:blank")  # sem métricas
    s=s.replace('<script src="https://tracker.appdigitalhub.com.br/tracker.js"','<script data-off="1" src="about:blank"',1)
    return s
TRY="'/teste/'+location.search"
# ---------- QUIZ ----------
q=open('quiz/index.html',encoding='utf-8').read()
q=common(q,'/quiz/')
card='''
 <div class="offer2" style="border-color:#5dffa0;box-shadow:0 0 22px rgba(93,255,160,.18)"><div class="o2h"><div><b>🎁 Teste grátis</b><small>Ainda em dúvida? Use o app completo antes de pagar</small></div><div class="o2p"><b style="color:#5dffa0">GRÁTIS</b></div></div>
  <div class="inc sm"><div><span>Plano completo liberado: Dungeon, chefes, os 3 Mestres e todas as fichas</span></div><div><span>Sem cartão: só e-mail e senha</span></div><div><span>Gostou? Escolha o seu plano e continue de onde parou</span></div></div>
  <a class="btn ghost" href="/teste/" onclick="this.href=TRY_URL()" style="border-color:#5dffa0;color:#5dffa0">🎁 Quero testar grátis</a></div>'''
a=' <div class="secure"><span>🔒 Pagamento seguro</span>'
assert a in q; q=q.replace(a,card+'\n'+a,1)
q=q.replace("const CHECKOUT=","window.TRY_URL=()=>%s;\nconst CHECKOUT="%TRY,1)
q=q.replace('<title>','<title>[PRÉVIA] ',1)
open('quiz-teste/index.html','w',encoding='utf-8').write(q)
# ---------- SITE ----------
s=open('site-v2/index.html',encoding='utf-8').read()
s=common(s,'/')
s=s.replace('<base href="/">','',1)
blk='''
<section style="position:relative;z-index:2;max-width:640px;margin:26px auto 40px;padding:0 16px">
 <div style="background:linear-gradient(160deg,rgba(20,60,40,.92),rgba(6,20,16,.95));border:2px solid #5dffa0;border-radius:16px;box-shadow:0 0 26px rgba(93,255,160,.22);padding:22px 20px;text-align:center;font-family:Jost,system-ui,sans-serif;color:#eafff2">
  <div style="font-weight:800;letter-spacing:.14em;font-size:12px;color:#5dffa0">[ SISTEMA ] · AINDA EM DÚVIDA?</div>
  <h3 style="margin:8px 0 6px;font-size:28px;font-weight:900">🎁 Teste grátis</h3>
  <p style="margin:0 auto 14px;max-width:440px;font-size:15.5px;line-height:1.5;color:#cfeedd">Use o <b>app completo</b> antes de pagar: Dungeon, chefes, os 3 Mestres e todas as fichas. Sem cartão, só e-mail e senha. Gostou? Escolha o seu plano e continue de onde parou.</p>
  <a href="/teste/" onclick="this.href=%s" style="display:inline-block;background:#5dffa0;color:#04140c;font-weight:900;font-size:17px;padding:14px 30px;border-radius:999px;text-decoration:none;box-shadow:0 6px 0 #1f8a52">Quero testar grátis</a>
 </div>
</section>'''%TRY
a='</section>\n\n<!-- 13. FAQ -->'
assert a in s; s=s.replace(a,'</section>\n'+blk+'\n\n<!-- 13. FAQ -->',1)
s=s.replace('<script src="/ab.js?v=1"></script>','',1)
s=s.replace('<title>','<title>[PRÉVIA] ',1)
open('site-teste/index.html','w',encoding='utf-8').write(s)
print('ok')
