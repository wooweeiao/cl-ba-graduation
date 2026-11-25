"""Wrap site/index.html (page body without a document shell) into a standalone document for GitHub Pages,
and write robots.txt and sitemap.xml next to it.
usage: make_pages.py site/index.html docs/index.html"""
import sys,os,re,datetime
URL='https://wooweeiao.github.io/cl-ba-graduation/'
TITLE='Tübingen Computational Linguistics BA: graduation rates · 图宾根大学计算语言学本科毕业率'
DESC=('Early leaving and graduation rates of the Computational Linguistics BA at the University of Tübingen, '
      'by entry cohort and semester, from the university’s enrolment statistics. '
      '图宾根大学计算语言学本科各入学届逐学期的中途离开与毕业比例。')
src=open(sys.argv[1],encoding='utf-8').read()
cut=src.index('<div class="wrap">')
head,body=src[:cut],src[cut:]
head=re.sub(r'<title>.*?</title>','<title>'+TITLE+'</title>',head,count=1)
reset='<style>:root{color-scheme:light;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>'
meta=('<meta name="description" content="%s">\n<link rel="canonical" href="%s">\n'
      '<meta property="og:type" content="website">\n<meta property="og:url" content="%s">\n'
      '<meta property="og:title" content="%s">\n<meta property="og:description" content="%s">\n')%(DESC,URL,URL,TITLE,DESC)
doc=('<!doctype html>\n<html lang="zh-CN">\n<head>\n<meta charset="utf-8">\n'
     '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
     +meta+reset+'\n'+head+'</head>\n<body>\n'+body+'</body>\n</html>\n')
out=os.path.dirname(sys.argv[2]); os.makedirs(out,exist_ok=True)
open(sys.argv[2],'w',encoding='utf-8').write(doc)
open(os.path.join(out,'robots.txt'),'w').write('User-agent: *\nAllow: /\nSitemap: %ssitemap.xml\n'%URL)
open(os.path.join(out,'sitemap.xml'),'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n  <url><loc>%s</loc><lastmod>%s</lastmod></url>\n</urlset>\n'%(URL,datetime.date.today().isoformat()))
print('wrote',sys.argv[2],len(doc),'bytes')
