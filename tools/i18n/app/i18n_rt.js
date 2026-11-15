/* Tradução em tempo de execução: troca os textos em português da tela pelo idioma da página.
   O código do app continua o mesmo; só o que aparece para o usuário muda. */
(function(){
  const D=window.FH_DICT||{};
  const keys=Object.keys(D).filter(k=>k.trim().length>1).sort((a,b)=>b.length-a.length);
  if(!keys.length)return;
  const esc=s=>s.replace(/[.*+?^${}()|[\]\\]/g,'\\$&');
  const L0=/^[\p{L}\p{N}]/u,L1=/[\p{L}\p{N}]$/u;
  const RX=new RegExp(keys.map(k=>(L0.test(k)?'(?<![\\p{L}\\p{N}])':'')+esc(k)+(L1.test(k)?'(?![\\p{L}\\p{N}])':'')).join('|'),'gu');
  const PT=/[ãõçêôâÃÕÇÊÔÂ]|(^|[^\p{L}])(você|não|seu|sua|seus|suas|treino|treinos|do|da|dos|das|em|um|uma|com|ouro|missão|nível|ganhe|faça|toque|está|são|até|também|já|só|amanhã|hoje|herói|meu|minha|novo|nova|ao|pelo|pela|mais|seguidos|carga|séries|série)(?![\p{L}])/iu;
  const tr=s=>{if(!s||s.length<2||!/[A-Za-zÀ-ú]/.test(s))return s;const s2=/\n/.test(s)?s.replace(/\s*\n\s*/g,' '):s;const t=s2.replace(RX,m=>D[m]);return t===s2?s:t};
  window.FHT=tr;
  const SKIP='.txt,.nm,.who b,.rn,[data-noi18n],textarea,script,style,input';
  const ATTR=['placeholder','title','aria-label','alt'];
  const done=new WeakMap(),CH=new WeakSet();
  function doText(n){const v=n.nodeValue;if(done.get(n)===v)return;const p=n.parentElement;if(!p||p.closest(SKIP))return;const t=tr(v);done.set(n,t);if(t!==v){CH.add(n);n.nodeValue=t}}
  function doEl(el){
    if(el.closest&&el.closest('[data-noi18n],.txt'))return;
    for(const a of ATTR){if(el.hasAttribute&&el.hasAttribute(a)){const v=el.getAttribute(a),t=tr(v);if(t!==v)el.setAttribute(a,t)}}
  }
  function walk(root){
    if(root.nodeType===3){doText(root);return}
    if(root.nodeType!==1)return;
    doEl(root);
    const w=document.createTreeWalker(root,NodeFilter.SHOW_ELEMENT|NodeFilter.SHOW_TEXT);let n;
    while(n=w.nextNode()){if(n.nodeType===3)doText(n);else doEl(n)}
  }
  let busy=false;
  const mo=new MutationObserver(ms=>{if(busy)return;busy=true;try{for(const m of ms){
    if(m.type==='characterData')doText(m.target);
    else if(m.type==='attributes')doEl(m.target);
    else m.addedNodes.forEach(walk)}}finally{busy=false}});
  const start=()=>{walk(document.documentElement);mo.observe(document.documentElement,{subtree:true,childList:true,characterData:true,attributes:true,attributeFilter:ATTR})};
  start();
  document.title=tr(document.title);
  // diálogos nativos, compartilhamento e links de WhatsApp
  const oc=window.confirm,oa=window.alert,op=window.prompt;
  window.confirm=m=>oc.call(window,tr(String(m)));window.alert=m=>oa.call(window,tr(String(m)));window.prompt=(m,d)=>op.call(window,tr(String(m)),d);
  const oo=window.open;window.open=function(u,...r){try{if(typeof u==='string'&&/wa\.me\/\?text=/.test(u)){const q=u.split('text=');u=q[0]+'text='+encodeURIComponent(tr(decodeURIComponent(q[1])))}}catch(e){}return oo.call(window,u,...r)};
  if(navigator.share){const os=navigator.share.bind(navigator);navigator.share=o=>os(Object.assign({},o,{title:tr(o.title||''),text:tr(o.text||'')}))}
  // notificações locais (timer de descanso etc.)
  if(window.ServiceWorkerRegistration){const sn=ServiceWorkerRegistration.prototype.showNotification;ServiceWorkerRegistration.prototype.showNotification=function(t,o){o=Object.assign({},o||{});if(o.body)o.body=tr(o.body);return sn.call(this,tr(t),o)}}
  if(window.Notification){const N=window.Notification;window.Notification=function(t,o){o=Object.assign({},o||{});if(o.body)o.body=tr(o.body);return new N(tr(t),o)};Object.defineProperty(window.Notification,'permission',{get:()=>N.permission});window.Notification.requestPermission=N.requestPermission.bind(N)}
  window.__FH_PT_LEFT=()=>{const out=new Set();const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);let n;while(n=w.nextNode()){const p=n.parentElement;if(!p||p.closest(SKIP)||p.closest('[data-noi18n]'))continue;const v=n.nodeValue.trim();if(!CH.has(n)&&v.length>2&&/[A-Za-zÀ-ú]{3}/.test(v)&&tr(v)===v)out.add(v)}
    document.querySelectorAll('[placeholder],[title],[aria-label]').forEach(e=>ATTR.forEach(a=>{const v=e.getAttribute(a);if(v&&tr(v)===v&&PT.test(v))out.add('@'+a+': '+v)}));return [...out]};
})();
