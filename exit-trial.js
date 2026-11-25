/* Pop-up de saída "Faça o teste grátis" (quiz e página nova, só Brasil).
   Computador: mouse saindo pelo topo da janela. Celular: primeiro "voltar".
   Aparece uma vez por visita. window.FHExit.show() abre manualmente. */
(function(){
  if(window.FHExit)return;
  var shown=false;
  function url(){return '/teste/'+location.search}
  function track(n){try{if(window.fbq)fbq('trackCustom',n,{})}catch(e){}}
  function css(){
    if(document.getElementById('fhx-css'))return;
    var s=document.createElement('style');s.id='fhx-css';
    s.textContent='#fhx{position:fixed;inset:0;z-index:2147483000;display:flex;align-items:center;justify-content:center;padding:18px;background:rgba(2,6,18,.78);backdrop-filter:blur(3px);-webkit-backdrop-filter:blur(3px);animation:fhxIn .25s ease}'+
    '@keyframes fhxIn{from{opacity:0}to{opacity:1}}@keyframes fhxPop{from{transform:scale(.88)}to{transform:scale(1)}}'+
    '#fhx .bx{position:relative;max-width:400px;width:100%;background:linear-gradient(165deg,#0f2a22,#06140f 70%);border:2px solid #5dffa0;border-radius:18px;box-shadow:0 0 40px rgba(93,255,160,.28);padding:26px 22px 20px;text-align:center;font-family:Jost,"Exo 2",system-ui,sans-serif;color:#eafff2;animation:fhxPop .3s cubic-bezier(.2,1.4,.4,1)}'+
    '#fhx .x{position:absolute;right:10px;top:8px;background:none;border:0;color:#9fcfb5;font-size:22px;cursor:pointer;padding:4px 8px}'+
    '#fhx .tg{font-weight:800;letter-spacing:.16em;font-size:11.5px;color:#5dffa0}'+
    '#fhx .gf{font-size:52px;line-height:1;margin:10px 0 2px;filter:drop-shadow(0 0 14px rgba(93,255,160,.5))}'+
    '#fhx h3{margin:6px 0 8px;font-size:27px;font-weight:900;line-height:1.1;color:#fff}'+
    '#fhx p{margin:0 0 16px;font-size:15px;line-height:1.5;color:#cfeedd}'+
    '#fhx .go{display:block;background:#5dffa0;color:#04140c;font-weight:900;font-size:17px;padding:15px 18px;border-radius:999px;text-decoration:none;box-shadow:0 6px 0 #1f8a52}'+
    '#fhx .no{display:block;margin-top:12px;background:none;border:0;color:#8fb8a3;font-size:13.5px;text-decoration:underline;cursor:pointer;width:100%}';
    document.head.appendChild(s);
  }
  function close(){var m=document.getElementById('fhx');if(m)m.remove()}
  function show(){
    if(shown||window.__fhGo)return false;shown=true;css();
    var m=document.createElement('div');m.id='fhx';m.setAttribute('role','dialog');m.setAttribute('aria-modal','true');
    m.innerHTML='<div class="bx"><button class="x" aria-label="Fechar">×</button><div class="tg">[ SISTEMA ] · ESPERA, CAÇADOR!</div><div class="gf">🎁</div>'+
      '<h3>Faça o teste grátis</h3><p>Ainda em dúvida? Use o <b>app completo</b> antes de pagar: Dungeon, chefes e os 3 Mestres. Sem cartão, só e-mail e senha.</p>'+
      '<a class="go" href="'+url()+'">🎁 Quero testar grátis</a><button class="no">Não, obrigado</button></div>';
    document.body.appendChild(m);track('ExitTrialPopup');
    m.querySelector('.go').addEventListener('click',function(){track('ExitTrialClick')});
    m.querySelector('.x').addEventListener('click',close);m.querySelector('.no').addEventListener('click',close);
    m.addEventListener('click',function(e){if(e.target===m)close()});
    return true;
  }
  window.FHExit={show:show,isShown:function(){return shown}};
  // computador: mouse saindo pelo topo
  document.addEventListener('mouseout',function(e){if(!e.relatedTarget&&e.clientY<=0&&innerWidth>=760)show()});
  // celular/voltar: se a página não tem a própria saída (data-own-back), cuida do "voltar" aqui
  var me=document.currentScript;
  if(!(me&&me.hasAttribute('data-own-back'))){
    var armed=false;function arm(){if(armed)return;try{history.pushState({fhx:1},'',location.href);armed=true}catch(e){}}
    arm();['pointerdown','touchstart','keydown'].forEach(function(t){addEventListener(t,arm,{once:true,passive:true})});
    addEventListener('popstate',function(){if(show())return;history.back()});
  }
})();
