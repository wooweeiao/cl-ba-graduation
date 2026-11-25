"""Wrap site/index.html (artifact page body) into a standalone document for GitHub Pages.
usage: make_pages.py site/index.html docs/index.html"""
import sys,os
src=open(sys.argv[1],encoding='utf-8').read()
cut=src.index('<div class="wrap">')
head,body=src[:cut],src[cut:]
reset='<style>:root{color-scheme:light;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>'
doc=('<!doctype html>\n<html lang="zh-CN">\n<head>\n<meta charset="utf-8">\n'
     '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
     +'<meta name="description" content="Early leaving and graduation rates of the Computational Linguistics BA at the University of Tübingen, by entry cohort. 图宾根计算语言学本科各入学届的中途离开与毕业比例。">\n'
     +reset+'\n'+head+'</head>\n<body>\n'+body+'</body>\n</html>\n')
os.makedirs(os.path.dirname(sys.argv[2]),exist_ok=True)
open(sys.argv[2],'w',encoding='utf-8').write(doc)
print('wrote',sys.argv[2],len(doc),'bytes')
