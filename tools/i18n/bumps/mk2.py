import asyncio
from playwright.async_api import async_playwright
import sys
L=sys.argv[1]
M='file:///home/claude/bumps/mock/'
W='file:///home/claude/i18n/bumps/mock/'+L+'/'
B={'es':{'APP FORJA DO HERÓI':'APP LA FORJA DEL HÉROE','RECRUTA':'RECLUTA','CAÇADOR ELITE':'CAZADOR ÉLITE','APP + DUNGEON 30 DIAS':'APP + MAZMORRA 30 DÍAS'},'en':{'APP FORJA DO HERÓI':"HERO'S FORGE APP",'RECRUTA':'RECRUIT','CAÇADOR ELITE':'ELITE HUNTER','APP + DUNGEON 30 DIAS':'APP + 30-DAY DUNGEON'}}[L]
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox','--allow-file-access-from-files'])
    for name,g,phones,badges in [
      ('main-recruta','rgba(79,195,255,.45)',[('flat-status-r.png',300,110,0,1,2)],[('APP FORJA DO HERÓI',250,40,40),('RECRUTA',640,820,38)]),
      ('main-elite','rgba(255,198,90,.45)',[('flat-dungeon.png',470,170,8,0.9,1),('flat-status.png',190,120,-6,1,2)],[('CAÇADOR ELITE',300,40,44),('APP + DUNGEON 30 DIAS',470,840,30)])]:
      pg=await b.new_page(viewport={'width':1000,'height':1000})
      await pg.goto(M+'book.html');await pg.evaluate(f"document.getElementById('st').style.setProperty('--g','{g}')")
      for img,x,y,rot,sc,z in phones:
        await pg.evaluate("""([img,x,y,rot,sc,z])=>{const s=document.getElementById('st');const sh=document.createElement('div');sh.className='shadow';Object.assign(sh.style,{left:(x+40)+'px',top:(y+800*sc)+'px',width:(340*sc)+'px',height:'50px',zIndex:z});s.appendChild(sh);
          const i=document.createElement('img');i.src=img;i.style.cssText=`position:absolute;left:${x}px;top:${y}px;width:${400*sc}px;transform:rotate(${rot}deg);z-index:${z};filter:drop-shadow(0 30px 50px rgba(0,0,0,.6))`;s.appendChild(i)}""",[W+img,x,y,rot,sc,z])
      for t,x,y,sz in badges: await pg.evaluate("([t,x,y,s])=>badge(t,x,y,s)",[B[t],x,y,sz])
      await pg.wait_for_timeout(500);await pg.screenshot(path=f'/home/claude/i18n/bumps/mock/{L}/{name}.png');await pg.close()
    await b.close()
asyncio.run(main())
