/* ===================== FORJA DO HERÓI · site v3 ===================== */
/* ====== LINKS DE PAGAMENTO ====== */
const CHECKOUT = {
  recruta: 'https://appdigitalhub.com.br/c/43752C6D',     // Recruta R$ 9,90
  elite: 'https://appdigitalhub.com.br/c/1C7E51FE',       // Caçador Elite R$ 19,90
  elitePopup: 'https://appdigitalhub.com.br/c/1D6785B5'   // Caçador Elite R$ 14,90 (oferta do pop-up)
};
const withQs=u=>{try{const q=location.search;if(!q||!u)return u;const x=new URL(u);new URLSearchParams(q).forEach((v,k)=>{if(!x.searchParams.has(k))x.searchParams.set(k,v)});return x.toString()}catch(e){return u}};
const ic=(v,n)=>{try{fbq('track','InitiateCheckout',{value:v,currency:'BRL',content_name:n})}catch(e){}};
const go=(u,v,n)=>{if(u){ic(v||9.9,n||'Forja do Heroi');location.href=withQs(u)}};
document.querySelectorAll('[data-plan="elite"]').forEach(a=>{a.href=withQs(CHECKOUT.elite);a.addEventListener('click',()=>ic(19.9,'Cacador Elite'))});
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

/* ====== trilha sonora (só toca quando o visitante liga) ====== */
const aud=document.getElementById('aud'),mus=document.getElementById('mus');
aud.volume=.35;
fetch(aud.src,{method:'HEAD'}).then(r=>{if(r.ok)mus.hidden=false}).catch(()=>{});
mus.onclick=()=>{if(aud.paused){aud.play().then(()=>{mus.classList.add('on');mus.setAttribute('aria-pressed','true');document.getElementById('musL').textContent='Tocando'}).catch(()=>{})}else{aud.pause();mus.classList.remove('on');mus.setAttribute('aria-pressed','false');document.getElementById('musL').textContent='Trilha sonora'}};

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
