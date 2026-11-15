import asyncio
from playwright.async_api import async_playwright
M='file:///home/claude/bumps/mock/'
import sys
L=sys.argv[1];W='file:///home/claude/i18n/bumps/mock/'+L+'/'
C={1:('c1-01.png','rgba(255,198,90,.45)','#5a3e10'),2:('c2-01.png','rgba(79,227,200,.4)','#0d4a42'),3:('c3-01.png','rgba(120,150,255,.4)','#1d2a5a'),4:('c4-01.png','rgba(255,106,90,.42)','#5a1610'),5:('c5-01.png','rgba(255,210,122,.45)','#5a4510')}
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox','--allow-file-access-from-files'])
    for n,(img,g,sp) in C.items():
      if n==5: continue
      pg=await b.new_page(viewport={'width':1000,'height':1000})
      await pg.goto(M+'book.html');await pg.evaluate(f"document.getElementById('st').style.setProperty('--g','{g}')")
      await pg.evaluate("([i,sp])=>book(i,290,190,'rotateY(-22deg) rotateX(4deg)',1,sp,2)",[W+img,sp])
      await pg.wait_for_timeout(400);await pg.screenshot(path=f'/home/claude/i18n/bumps/mock/'+L+f'/bump{n}.png');await pg.close()
    # combo
    pg=await b.new_page(viewport={'width':1000,'height':1000})
    await pg.goto(M+'book.html');await pg.evaluate("document.getElementById('st').style.setProperty('--g','rgba(255,198,90,.4)')")
    seq=[(4,30,330,'rotateY(-12deg)',.55,1),(3,740,330,'rotateY(-12deg)',.55,1),(2,190,290,'rotateY(-14deg)',.62,2),(1,560,290,'rotateY(-14deg)',.62,2),(5,330,210,'rotateY(-16deg) rotateX(3deg)',.8,3)]
    for n,x,y,r,s,z in seq:
      await pg.evaluate("([i,x,y,r,s,sp,z])=>book(i,x,y,r,s,sp,z)",[W+C[n][0],x,y,r,s,C[n][2],z])
    await pg.evaluate("badge('"+('ARSENAL COMPLETO' if L=='es' else 'FULL ARSENAL')+"',300,70,40)")
    await pg.evaluate("badge('"+('5 EN 1' if L=='es' else '5 IN 1')+"',760,820,34)")
    await pg.wait_for_timeout(500);await pg.screenshot(path='/home/claude/i18n/bumps/mock/'+L+'/bump5.png')
    await b.close()
asyncio.run(main())
