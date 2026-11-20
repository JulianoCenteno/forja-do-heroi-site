#!/usr/bin/env python3
"""Lista fragmentos de texto visível (pt) de um HTML/JS, para montar o dicionário de tradução.
Uso: python3 tools/i18n_frags.py app/index.html > /tmp/frags.txt"""
import re, sys, json

PTW = re.compile(r"[ãõçéêáíóúâôàÃÕÇÉÊÁÍÓÚÂÔ]|\b(você|seu|sua|seus|suas|não|treino|treinar|dia|dias|de|do|da|dos|das|com|para|pra|por|em|no|na|um|uma|os|as|o|a|e|é|ao|mais|sem|até|cada|hoje|agora|nível|série|séries|missão|chefe|chefes|caçador)\b", re.I)

def frags(src):
    s = re.sub(r'<style.*?</style>', ' ', src, flags=re.S)
    s = re.sub(r'<!--.*?-->', ' ', s, flags=re.S)
    s = re.sub(r'/\*.*?\*/', ' ', s, flags=re.S)
    s = re.sub(r'(?m)^\s*//.*$', ' ', s)
    out = []
    seen = set()
    def add(t):
        t = t.strip()
        if len(t) < 2 or t in seen: return
        if not re.search(r'[A-Za-zÀ-ÿ]', t): return
        if re.fullmatch(r'[\w\-.:/#?=&%@]+', t) and not re.search(r'[À-ÿ]', t) and not (t[:1].isupper() and len(t) > 2 and t.isalpha()): return
        if re.search(r'^(https?:|/|#|\.)|\.(webp|png|jpg|svg|js|css|json|mp3|mp4)\b|=>|function\b|\breturn\b|\bconst\b|document\.|\$\(', t): return
        if not PTW.search(t) and not (t[:1].isupper() and t.isalpha()): return
        seen.add(t); out.append(t)
    # literais de string
    for m in re.finditer(r"'((?:[^'\\\n]|\\.)*)'|\"((?:[^\"\\\n]|\\.)*)\"|`((?:[^`\\]|\\.)*)`", s, flags=re.S):
        lit = next((g for g in m.groups() if g is not None), '')
        for part in re.split(r'\$\{(?:[^{}]|\{[^{}]*\})*\}|<[^>]*>|\n', lit):
            add(part)
    # texto entre tags fora de scripts
    body = re.sub(r'<script.*?</script>', ' ', s, flags=re.S)
    for m in re.finditer(r'>([^<>]+)<', body):
        add(m.group(1))
    return out

if __name__ == '__main__':
    src = open(sys.argv[1], encoding='utf-8').read()
    for f in frags(src):
        print(json.dumps(f, ensure_ascii=False))
