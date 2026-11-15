import re,json,sys
src=open('/home/claude/forja-do-heroi-site/app/index.html').read()
# separa <style> (ignora) e o resto
body=re.sub(r'<style>.*?</style>','',src,flags=re.S)
out=[]
# JS: literais '..' ".." e partes estáticas de `..`
i=0;n=len(body)
def add(s,pos):
    s2=s.strip()
    if len(s2)<2: return
    if not re.search(r'[A-Za-zÀ-ú]{2}',s2): return
    out.append((pos,s))
# varredura simples de literais em todo o arquivo (HTML inclusive)
for m in re.finditer(r"'((?:[^'\\\n]|\\.)*)'|\"((?:[^\"\\\n]|\\.)*)\"|`((?:[^`\\]|\\.)*)`",body):
    s=m.group(1) if m.group(1) is not None else (m.group(2) if m.group(2) is not None else None)
    if s is not None: add(s,m.start());continue
    t=m.group(3)
    # tira ${...} (aninhamento simples)
    parts=re.split(r'\$\{(?:[^{}]|\{[^{}]*\})*\}',t)
    for p in parts:
        for seg in re.split(r'<[^>]*>',p): add(seg,m.start())
# texto entre tags fora de literais (HTML estático)
for m in re.finditer(r'>([^<>]{2,})<',body):
    add(m.group(1),m.start())
# filtra código provável
def codey(s):
    t=s.strip()
    if re.fullmatch(r'[\w\-\.#:\[\]=\s/,()%>+*~^$|!&?@]*',t) and not re.search(r'[À-ú]',t) and (' ' not in t or re.search(r'[=:;{}()]',t)): return True
    if re.match(r'^(https?:|/|\.|#|data:)',t): return True
    if re.search(r'[{};]\s*$',t) and not re.search(r'[À-ú]',t): return True
    return False
uniq={}
for pos,s in out:
    if codey(s): continue
    uniq.setdefault(s.strip(),pos)
json.dump(sorted(uniq,key=lambda k:uniq[k]),open('strings.json','w'),ensure_ascii=False,indent=0)
print(len(uniq), sum(len(k) for k in uniq))
