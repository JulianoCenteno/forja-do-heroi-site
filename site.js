/* ===================== FORJA DO HERÓI · site v3 ===================== */
/* ====== LINKS DE PAGAMENTO ====== */
const CHECKOUT = {
  recruta: 'https://appdigitalhub.com.br/c/43752C6D',     // Recruta R$ 9,90
  elite: 'https://appdigitalhub.com.br/c/1C7E51FE',       // Caçador Elite R$ 19,90
  elitePopup: 'https://appdigitalhub.com.br/c/1D6785B5'   // Caçador Elite R$ 14,90 (oferta do pop-up)
};
const withQs=u=>{try{const q=location.search;if(!q||!u)return u;const x=new URL(u);new URLSearchParams(q).forEach((v,k)=>{if(!x.searchParams.has(k))x.searchParams.set(k,v)});return x.toString()}catch(e){return u}};
/* Digital Hub Tracker (tracker.js): leva UTMs + ID do visitante ao checkout e já envia o InitiateCheckout
   (pixel + servidor, sem duplicar). Só disparamos o nosso se o tracker não carregou. */
const RT=()=>window.Rastreio&&window.Rastreio.loaded?window.Rastreio:null;
const dec=u=>{const r=RT();return r?r.decorate(withQs(u)):withQs(u)};
const ic=(v,n,u)=>{const r=RT();if(r){r.initiateCheckout(u);return}try{fbq('track','InitiateCheckout',{value:v,currency:'BRL',content_name:n})}catch(e){}};
const go=(u,v,n)=>{if(u){ic(v||9.9,n||'Forja do Heroi',u);location.href=dec(u)}};
document.querySelectorAll('[data-plan="elite"]').forEach(a=>{a.href=withQs(CHECKOUT.elite);a.addEventListener('click',()=>{if(!RT())ic(19.9,'Cacador Elite')})});
/* o botão do Recruta só abre o pop-up: tira o link do checkout para o tracker não contar o clique como início de compra */
document.querySelectorAll('[data-plan="recruta"]').forEach(a=>a.setAttribute('href','#planos'));
const pop=document.getElementById('pop');let lastFocus=null;
function openPop(){lastFocus=document.activeElement;pop.hidden=false;document.body.style.overflow='hidden';document.getElementById('popYes').focus()}
function closePop(){pop.hidden=true;document.body.style.overflow='';lastFocus&&lastFocus.focus()}
document.querySelectorAll('[data-plan="recruta"]').forEach(a=>a.addEventListener('click',e=>{e.preventDefault();openPop()}));
document.getElementById('popYes').addEventListener('click',e=>{e.preventDefault();go(CHECKOUT.elitePopup||CHECKOUT.elite,14.9,'Cacador Elite popup')});
document.getElementById('popNo').addEventListener('click',e=>{e.preventDefault();go(CHECKOUT.recruta,9.9,'Recruta')});
document.getElementById('popX').addEventListener('click',closePop);
pop.addEventListener('click',e=>{if(e.target===pop)closePop()});
addEventListener('keydown',e=>{if(e.key==='Escape'&&!pop.hidden)closePop()});

/* ====== DADOS DO RODAPÉ (preencha) ====== */
const EMPRESA = { nome: '', documento: '', suporte: '' };
(()=>{const p=[EMPRESA.nome,EMPRESA.documento,EMPRESA.suporte&&('Suporte: '+EMPRESA.suporte)].filter(Boolean);if(p.length)document.getElementById('footInfo').textContent='© 2026 Forja do Herói · '+p.join(' · ')})();

/* ====== navegação ====== */
const nav=document.getElementById('nav'),links=document.getElementById('links');
addEventListener('scroll',()=>nav.classList.toggle('solid',scrollY>40),{passive:true});
document.getElementById('burger').onclick=()=>links.classList.toggle('open');
links.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>links.classList.remove('open')));
const spy=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting)links.querySelectorAll('a').forEach(a=>a.classList.toggle('on',a.getAttribute('href')==='#'+e.target.id))}),{rootMargin:'-45% 0px -50% 0px'});
['topo','classes','sistema','planos','faq'].forEach(id=>{const s=document.getElementById(id);s&&spy.observe(s)});

/* ====== aparecer ao rolar + barras + contadores ====== */
function count(el){const n=+el.dataset.n,t0=performance.now(),D=1800;const f=t=>{const p=Math.min(1,(t-t0)/D),e=1-Math.pow(1-p,3);el.textContent=Math.round(n*e).toLocaleString('pt-BR');if(p<1)requestAnimationFrame(f)};requestAnimationFrame(f)}
const io=new IntersectionObserver(es=>es.forEach(e=>{if(!e.isIntersecting)return;const t=e.target;t.classList.add('in');
  t.querySelectorAll('.tr i').forEach(i=>i.style.width=i.dataset.w+'%');t.querySelectorAll('.cnt').forEach(count);io.unobserve(t)}),{threshold:.14});
document.querySelectorAll('.rv').forEach(el=>io.observe(el));

/* ====== trocar telas do app ====== */
const SETS={a:[['heroi','-46%',15,'Herói e status'],['dungeon','-12%',12,'Dungeons e incursões'],['missoes','-12%',12,'Missões e evolução']],
            b:[['treinar','-55%',18,'Treino e XP'],['chefes','-15%',12,'Batalhas de chefe'],['taverna','-20%',13,'Taverna da comunidade']]};
document.querySelectorAll('.swap button').forEach(b=>b.onclick=()=>{
  document.querySelectorAll('.swap button').forEach(x=>x.classList.toggle('on',x===b));
  document.querySelectorAll('#phones .phc').forEach((c,i)=>{const s=SETS[b.dataset.set][i];const img=c.querySelector('.scr img');img.style.opacity=0;
    setTimeout(()=>{img.src='img/v2/app-'+s[0]+'.webp';img.style.setProperty('--y',s[1]);img.style.setProperty('--d',s[2]+'s');img.style.animation='none';void img.offsetWidth;img.style.animation='';img.style.opacity=1},280);
    c.querySelector('.lbl span').textContent=s[3]})});

/* ====== parallax suave no hero ====== */
const heroBg=document.querySelector('.hero-bg img'),heroCh=document.querySelector('.hero-chars');
let px=0,py=0,tx=0,ty=0;
if(matchMedia('(pointer:fine)').matches){addEventListener('mousemove',e=>{tx=(e.clientX/innerWidth-.5);ty=(e.clientY/innerHeight-.5)},{passive:true})}
(function loop(){px+=(tx-px)*.05;py+=(ty-py)*.05;const s=Math.min(scrollY,900);
  if(heroCh)heroCh.style.transform=`translate3d(${px*-14}px,${py*-8+s*.12}px,0)`;
  if(heroBg)heroBg.parentElement.style.transform=`translate3d(${px*10}px,${py*6+s*.3}px,0)`;
  requestAnimationFrame(loop)})();

/* ====== partículas (brasas, faíscas e fumaça) ====== */
(()=>{
  const cv=document.getElementById('fx');if(!cv||matchMedia('(prefers-reduced-motion:reduce)').matches)return;
  const cx=cv.getContext('2d');let W,H,DPR;const P=[],S=[];
  const mob=innerWidth<760;const NP=mob?46:110,NS=mob?7:14;
  function size(){DPR=Math.min(devicePixelRatio||1,2);W=cv.width=innerWidth*DPR;H=cv.height=innerHeight*DPR}
  size();addEventListener('resize',size);
  const COL=[[255,200,80],[255,170,40],[160,110,255],[90,210,255],[255,230,150]];
  function spark(init){const c=COL[Math.random()*COL.length|0];return{x:Math.random()*W,y:init?Math.random()*H:H+20*DPR,r:(Math.random()*1.8+.6)*DPR,vy:-(Math.random()*.55+.2)*DPR,vx:(Math.random()-.5)*.25*DPR,
    a:0,ma:Math.random()*.7+.3,life:0,ml:400+Math.random()*500,c,w:Math.random()*6.28,ws:Math.random()*.03+.008}}
  function smoke(init){return{x:Math.random()*W,y:init?Math.random()*H:H+200*DPR,r:(120+Math.random()*220)*DPR,vy:-(Math.random()*.18+.05)*DPR,vx:(Math.random()-.5)*.15*DPR,
    a:0,ma:Math.random()*.07+.03,life:0,ml:1600+Math.random()*1400,hue:Math.random()<.6?268:205}}
  for(let i=0;i<NP;i++)P.push(spark(true));for(let i=0;i<NS;i++)S.push(smoke(true));
  let vis=true;document.addEventListener('visibilitychange',()=>vis=!document.hidden);
  function frame(){
    requestAnimationFrame(frame);if(!vis)return;
    cx.clearRect(0,0,W,H);
    cx.globalCompositeOperation='screen';
    for(const s of S){s.life++;s.x+=s.vx;s.y+=s.vy;const t=s.life/s.ml;s.a=s.ma*Math.sin(Math.min(1,t)*Math.PI);
      const g=cx.createRadialGradient(s.x,s.y,0,s.x,s.y,s.r);g.addColorStop(0,`hsla(${s.hue},80%,60%,${s.a})`);g.addColorStop(1,`hsla(${s.hue},80%,50%,0)`);
      cx.fillStyle=g;cx.beginPath();cx.arc(s.x,s.y,s.r,0,6.283);cx.fill();if(s.life>s.ml)Object.assign(s,smoke(false))}
    cx.globalCompositeOperation='lighter';
    for(const p of P){p.life++;p.w+=p.ws;p.x+=p.vx+Math.sin(p.w)*.35*DPR;p.y+=p.vy;const t=p.life/p.ml;p.a=p.ma*Math.min(1,t*4)*(1-Math.max(0,(t-.7)/.3));
      const [r,g,b]=p.c;cx.fillStyle=`rgba(${r},${g},${b},${p.a*.22})`;cx.beginPath();cx.arc(p.x,p.y,p.r*4,0,6.283);cx.fill();
      cx.fillStyle=`rgba(${r},${g},${b},${p.a})`;cx.beginPath();cx.arc(p.x,p.y,p.r,0,6.283);cx.fill();
      if(p.life>p.ml||p.y<-20)Object.assign(p,spark(false))}
    cx.globalCompositeOperation='source-over';
  }
  frame();
})();

/* ====== trilha sonora: tenta tocar 1s após entrar; se o navegador bloquear, começa no 1º toque/clique ====== */
const aud=document.getElementById('aud'),mus=document.getElementById('mus');
aud.volume=.35;
fetch(aud.src,{method:'HEAD'}).then(r=>{if(r.ok)mus.hidden=false}).catch(()=>{});
const musUI=on=>{mus.classList.toggle('on',on);mus.setAttribute('aria-pressed',on?'true':'false');document.getElementById('musL').textContent=on?'Tocando':'Trilha sonora'};
let musOff=false;try{musOff=localStorage.getItem('fhMus')==='off'}catch(e){}
const EV=['pointerdown','touchstart','keydown','click'];
const kick=()=>{if(musOff||!aud.paused)return unhook();aud.play().then(()=>{musUI(true);unhook()}).catch(()=>{})};
const unhook=()=>EV.forEach(e=>removeEventListener(e,kick,true));
mus.onclick=e=>{e.stopPropagation();if(aud.paused){musOff=false;try{localStorage.removeItem('fhMus')}catch(_){}aud.play().then(()=>musUI(true)).catch(()=>{})}else{aud.pause();musOff=true;try{localStorage.setItem('fhMus','off')}catch(_){}musUI(false)}unhook()};
if(!musOff){setTimeout(()=>{aud.play().then(()=>musUI(true)).catch(()=>{EV.forEach(e=>addEventListener(e,kick,{capture:true,passive:true}))})},1000)}

/* Carrossel (celular): Sistema e Classes */
document.querySelectorAll('[data-car]').forEach(car=>{
  const ui=car.parentElement.querySelector(':scope > .car-ui');if(!ui)return;
  const items=[...car.children],dots=[...ui.querySelectorAll('.car-dots button')];let cur=0,user=false,t;
  const go=i=>{i=(i+items.length)%items.length;const el=items[i];car.scrollTo({left:el.offsetLeft-(car.clientWidth-el.offsetWidth)/2,behavior:'smooth'})};
  const mark=()=>{const c=car.scrollLeft+car.clientWidth/2;let b=0,d=1e9;items.forEach((el,i)=>{const x=Math.abs(el.offsetLeft+el.offsetWidth/2-c);if(x<d){d=x;b=i}});cur=b;items.forEach((el,i)=>el.classList.toggle('on',i===b));dots.forEach((el,i)=>el.classList.toggle('on',i===b))};
  car.addEventListener('scroll',()=>{cancelAnimationFrame(t);t=requestAnimationFrame(mark)},{passive:true});
  ['touchstart','pointerdown','wheel'].forEach(e=>car.addEventListener(e,()=>user=true,{passive:true}));
  dots.forEach((d,i)=>d.addEventListener('click',()=>{user=true;go(i)}));
  ui.querySelector('.prev').addEventListener('click',()=>{user=true;go(cur-1)});
  ui.querySelector('.next').addEventListener('click',()=>{user=true;go(cur+1)});
  const mq=matchMedia('(max-width:760px)');
  const start=()=>{if(!mq.matches)return;const i=car.classList.contains('cx-cards')?1:0;car.style.scrollBehavior='auto';const el=items[i];car.scrollLeft=el.offsetLeft-(car.clientWidth-el.offsetWidth)/2;car.style.scrollBehavior='';mark()};
  start();addEventListener('load',start);mq.addEventListener('change',start);
  setInterval(()=>{if(!user&&mq.matches&&document.visibilityState==='visible'){const r=car.getBoundingClientRect();if(r.top<innerHeight&&r.bottom>0)go(cur+1)}},4500);
});

/* Auras, fumaça e brasas por seção (desktop) */
(()=>{
  if(matchMedia('(prefers-reduced-motion:reduce)').matches)return;
  const G='#ffb21a',T='#22ffc0',R='#ff2a55',P='#8a3dff',B='#2e9bff',GR='#55ff6a',S='#a9c8ff';
  // [x%,y%,tamanho(%largura),cor]
  const C={
    topo:{g:[[27,40,20,T],[52,40,22,G],[77,40,20,R],[51,14,16,B]],f:[[27,42,9,T],[52,44,10,G],[77,42,9,R]],s:[P,B,P],e:[[20,34,60,G],[16,34,62,T],[66,34,62,R]]},
    problema:{g:[[87,25,16,G],[63,48,14,P]],f:[[88,24,8,G]],s:[P],e:[[78,96,30,G]]},
    sistema:{g:[[25,50,14,G],[50,50,14,B],[75,50,14,P]],s:[B,P],e:[[10,80,85,G]]},
    classes:{g:[[20,58,16,T],[50,55,18,G],[80,58,16,P]],f:[[6,40,8,T],[94,40,8,P]],s:[T,P],e:[[8,60,90,G]]},
    alquimia:{g:[[32,32,24,G],[40,22,9,GR],[8,60,10,GR]],f:[[31,30,10,G]],s:[P],e:[[15,10,40,G],[30,10,15,GR]]},
    ranking:{g:[[24,40,13,S],[50,36,17,G],[76,40,13,R]],f:[[50,34,9,G]],s:[P],e:[[40,30,22,G]]},
    garantia:{g:[[21,45,30,B],[21,40,18,G]],f:[[16,40,10,B],[28,55,9,B]],s:[P,P],e:[[8,20,28,G]]},
    planos:{g:[[11,42,24,G],[89,42,24,P],[88,30,10,R]],f:[[12,45,9,G],[90,40,9,P]],s:[P,G],e:[[2,30,20,G],[78,30,20,P]]},
    faq:{g:[[15,45,26,G],[96,30,12,B]],f:[[12,50,10,G]],s:[B],e:[[2,30,24,G]]}
  };
  const r=(a,b)=>a+Math.random()*(b-a);
  for(const id in C){const sec=document.getElementById(id);if(!sec)continue;const c=C[id];const L=document.createElement('div');L.className='fxl';L.setAttribute('aria-hidden','true');let h='';
    (c.s||[]).forEach((col,i)=>h+=`<i class="sm" style="left:${[-10,40,15][i%3]}%;--c:${col};--d:${r(18,28)}s;--dl:-${r(0,20)}s"></i>`);
    (c.g||[]).forEach(([x,y,s,col])=>h+=`<i class="gw" style="left:${x}%;top:${y}%;width:${s}cqw;height:${s}cqw;--c:${col};--d:${r(3.6,5.6)}s;--dl:-${r(0,4)}s"></i>`);
    (c.f||[]).forEach(([x,y,s,col])=>h+=`<i class="fl" style="left:${x}%;top:${y}%;width:${s}cqw;height:${s}cqw;--c:${col};--d:${r(5,9)}s;--dl:-${r(0,8)}s"></i>`);
    (c.e||[]).forEach(([x,y,w,col])=>{for(let k=0;k<Math.round(w/2.2)+4;k++)h+=`<i class="em" style="left:${r(x,x+w)}%;top:${r(y+20,y+55)}%;--s:${r(.15,.42)}cqw;--c:${col};--d:${r(3.5,7)}s;--dl:-${r(0,7)}s;--dx:${r(-3,3)}cqw"></i>`});
    L.innerHTML=h;sec.appendChild(L)}
})();
