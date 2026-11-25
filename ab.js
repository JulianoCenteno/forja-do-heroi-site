/* Teste A/B Brasil: métricas da página nova (site-v2) na mesma tabela do quiz */
(function(){try{
var q=new URLSearchParams(location.search),ab=(q.get('fh_ab')||'').slice(0,12)||null;
var K='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxwZGljcnBldHhxbm94Y2VvemZhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTM4NDIxNDEsImV4cCI6MjEwOTQxODE0MX0.aUhV98QVe4ju8aklOErBYMX_6VbYejVQpvd-cR_RoAs';
var sid;try{sid=sessionStorage.getItem('fh_pag_sid');if(!sid){sid='p'+Date.now().toString(36)+Math.random().toString(36).slice(2,9);sessionStorage.setItem('fh_pag_sid',sid)}}catch(e){sid='p'+Math.random().toString(36).slice(2,12)}
var mob=/Mobi|Android|iPhone/i.test(navigator.userAgent),seen={};
function log(ev,step,val){if(ev==='view'){if(seen[step])return;seen[step]=1}
try{fetch('https://lpdicrpetxqnoxceozfa.supabase.co/rest/v1/fh_quiz_events',{method:'POST',keepalive:true,headers:{apikey:K,Authorization:'Bearer '+K,'Content-Type':'application/json',Prefer:'return=minimal'},
body:JSON.stringify({sid:sid,ev:ev,step:step,val:val||null,ab:ab,utm_source:(q.get('utm_source')||'').slice(0,120)||null,utm_campaign:(q.get('utm_campaign')||'').slice(0,200)||null,utm_content:(q.get('utm_content')||'').slice(0,200)||null,ua_mobile:mob})}).catch(function(){})}catch(e){}}
log('view','pag');
var ps=document.getElementById('planos');
if(ps&&'IntersectionObserver' in window){var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){log('view','pag_planos');io.disconnect()}})});io.observe(ps)}
document.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('a[href*="appdigitalhub.com.br/c/"]');if(!a)return;
var m=a.href.match(/\/c\/([A-Z0-9]+)/);log('ck','pag_checkout',m?m[1]:null)},true);
}catch(e){}})();
