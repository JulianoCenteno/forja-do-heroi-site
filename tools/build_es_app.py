#!/usr/bin/env python3
"""Gera o app em espanhol (/es/app/index.html) a partir de /app/index.html.
Os textos são traduzidos na tela por um tradutor que usa os dicionários de tools/i18n/es_app_*.json
(sem mexer na lógica do app). Preços em US$ e checkouts da Cakto."""
import os, re, json, glob, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
from es_links import ES

a = open(os.path.join(ROOT, 'app', 'index.html'), encoding='utf-8').read()

def rep(x, y):
    global a
    if x not in a:
        raise SystemExit('app es: não encontrado: ' + x[:80])
    a = a.replace(x, y)

rep('<html lang="pt-BR">', '<html lang="es">')
rep('<head>', '<head>\n<base href="/app/">')
rep("https://appdigitalhub.com.br/c/1C7E51FE", ES['elite'])
rep("https://appdigitalhub.com.br/c/E61E69D0", ES['upgrade'])
rep("https://appdigitalhub.com.br/c/B04D52D9", ES['abismo'])
for x, y in [('R$ 26,90', 'US$ 12.90'), ('R$ 14,90', 'US$ 6.90'), ('R$ 39,90', 'US$ 19.90'), ('R$ 19,90', 'US$ 9.90')]:
    a = a.replace(x, y)

D = {}
for f in sorted(glob.glob(os.path.join(ROOT, 'tools', 'i18n', 'es_app_*.json'))):
    D.update(json.load(open(f, encoding='utf-8')))
D = {k: v for k, v in D.items() if k != v}

TR = r"""<script>
/* Tradutor pt→es: troca os textos na tela usando o dicionário (a lógica do app fica intacta) */
(function(){
var D=__DICT__;
var NUM=/\d+(?:[.,:]\d+)*/g, L=/[A-Za-zÀ-ÿ]/;
var RX=[
 [/^E aí, (.+), como estão sendo seus primeiros dias\?$/,function(m){return '¿Qué tal, '+m[1]+'? ¿Cómo van tus primeros días?'}],
 [/^Fala, (.+)!$/,function(m){return '¡Hola, '+m[1]+'!'}],
 [/^Boa, (.+)!$/,function(m){return '¡Bien, '+m[1]+'!'}]
];
function look(t,depth){
 if(Object.prototype.hasOwnProperty.call(D,t))return D[t];
 var nums=t.match(NUM);
 if(nums){var k=t.replace(NUM,'{n}');if(Object.prototype.hasOwnProperty.call(D,k)){var i=0;return D[k].replace(/\{n\}/g,function(){var v=nums[i++];return v==null?'':v})}}
 if(depth>3)return null;
 var pre=(t.match(/^[^A-Za-zÀ-ÿ0-9+]*/)||[''])[0].length, suf=(t.match(/[^A-Za-zÀ-ÿ0-9]*$/)||[''])[0].length;
 for(var a1=0;a1<=pre;a1++){for(var b1=0;b1<=suf;b1++){if(!a1&&!b1)continue;var core=t.slice(a1,t.length-b1);if(!core||!L.test(core))continue;var c=look(core,4);if(c!=null)return t.slice(0,a1)+c+t.slice(t.length-b1)}}
 if(t.charAt(0)==='+'){var c0=look(t.slice(1),4);if(c0!=null)return '+'+c0}
 if(t.indexOf(' · ')>0){var parts=t.split(' · '),any=false,out=parts.map(function(p){var c=look(p,depth+1);if(c!=null){any=true;return c}return p});if(any)return out.join(' · ')}
 for(var j=0;j<RX.length;j++){var mm=t.match(RX[j][0]);if(mm)return RX[j][1](mm)}
 return null}
var VAL={};for(var kk in D)VAL[D[kk]]=1;
function tr(s){if(!s||!L.test(s))return null;var t=s.trim();if(VAL[t])return null;var r=look(t,0);if(r==null||r===t)return null;return s.replace(t,r)}
window.__esTr=function(s){var r=tr(String(s));return r==null?s:r};
var ATTR=['placeholder','title','aria-label'];var DONE=new WeakMap();
function setT(n,r){DONE.set(n,r);n.nodeValue=r}
function doNode(n){
 if(n.nodeType===3){var p=n.parentNode;if(!p||p.nodeName==='SCRIPT'||p.nodeName==='STYLE')return;if(DONE.get(n)===n.nodeValue)return;var r=tr(n.nodeValue);if(r!=null)setT(n,r);return}
 if(n.nodeType!==1||n.nodeName==='SCRIPT'||n.nodeName==='STYLE')return;
 for(var i=0;i<ATTR.length;i++){var v=n.getAttribute&&n.getAttribute(ATTR[i]);if(v){var r2=tr(v);if(r2!=null)n.setAttribute(ATTR[i],r2)}}
 if((n.nodeName==='INPUT'&&(n.type==='button'||n.type==='submit'))&&n.value){var r3=tr(n.value);if(r3!=null)n.value=r3}
 var w=document.createTreeWalker(n,NodeFilter.SHOW_TEXT|NodeFilter.SHOW_ELEMENT),x;
 while(x=w.nextNode()){if(x.nodeType===3){var pp=x.parentNode;if(pp&&pp.nodeName!=='SCRIPT'&&pp.nodeName!=='STYLE'&&DONE.get(x)!==x.nodeValue){var r4=tr(x.nodeValue);if(r4!=null)setT(x,r4)}}
  else{for(var k=0;k<ATTR.length;k++){var vv=x.getAttribute(ATTR[k]);if(vv){var r5=tr(vv);if(r5!=null)x.setAttribute(ATTR[k],r5)}}}}}
var mo=new MutationObserver(function(ms){for(var i=0;i<ms.length;i++){var m=ms[i];
 if(m.type==='characterData')doNode(m.target);
 else if(m.type==='attributes')doNode(m.target);
 else for(var j=0;j<m.addedNodes.length;j++)doNode(m.addedNodes[j])}});
function start(){doNode(document.body);mo.observe(document.body,{subtree:true,childList:true,characterData:true,attributes:true,attributeFilter:ATTR});
 var tt=tr(document.title);if(tt)document.title=tt}
if(document.body)start();else document.addEventListener('DOMContentLoaded',start);
['alert','confirm','prompt'].forEach(function(f){var o=window[f];if(o)window[f]=function(msg){var a=[].slice.call(arguments);a[0]=window.__esTr(msg);return o.apply(window,a)}});
})();
</script>
"""
TR = TR.replace('__DICT__', json.dumps(D, ensure_ascii=False))
# o tradutor entra antes do primeiro script do app, para pegar tudo desde a primeira renderização
i = a.find('<script')
a = a[:i] + TR + a[i:]
out = os.path.join(ROOT, 'es', 'app', 'index.html')
os.makedirs(os.path.dirname(out), exist_ok=True)
open(out, 'w', encoding='utf-8').write(a)
print('ok', out, len(D), 'termos')
