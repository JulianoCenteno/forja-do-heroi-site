#!/usr/bin/env python3
"""Extrai as frases visíveis (texto de HTML e strings de JS) de um arquivo, para tradução.
Uso: python3 tools/i18n_extract.py quiz/index.html > /tmp/frases.json"""
import re, sys, json

PT_HINT = re.compile(r'[A-Za-zÀ-ÿ]{2,}')

def phrases(src):
    s = re.sub(r'<style.*?</style>', lambda m: ' ' * len(m.group(0)), src, flags=re.S)
    s = re.sub(r'<!--.*?-->', lambda m: ' ' * len(m.group(0)), s, flags=re.S)
    out = {}
    # 1) runs of text between delimiters that typically bound UI text
    for m in re.finditer(r"(?<=[>'\"`}])([^<>'\"`{}$\\\n]*[A-Za-zÀ-ÿ][^<>'\"`{}$\\\n]*)(?=[<'\"`$])", s):
        t = m.group(1)
        core = t.strip()
        if not core or not PT_HINT.search(core):
            continue
        if re.fullmatch(r'[\w\-./:#=&?%]+', core) and not re.search(r'[À-ÿ]', core) and not core[:1].isupper():
            continue  # identificadores, caminhos, classes css
        if re.search(r'^(https?:|/|\.|#)|\.(webp|png|jpg|svg|js|css|json|mp3)\b|function|=>|;\s*$', core):
            continue
        if re.fullmatch(r'[a-z0-9_\-]+', core):
            continue
        out[core] = out.get(core, 0) + 1
    return out

if __name__ == '__main__':
    src = open(sys.argv[1], encoding='utf-8').read()
    ph = phrases(src)
    items = sorted(ph.items(), key=lambda kv: src.find(kv[0]))
    json.dump([k for k, _ in items], sys.stdout, ensure_ascii=False, indent=0)
