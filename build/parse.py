import re,glob,json,sys,os
txt=sys.argv[1]
def key(f):
    y=re.search(r'-(\d{4})',f).group(1); return (int(y), 0 if '-ss-' in f else 1)
COLS=['0','1','2','3','4','5','6','7','8','9','10','11','12','>12','Ges']
out=[]
for f in sorted(glob.glob(os.path.join(txt,'*.txt')), key=key):
    name=os.path.basename(f)[:-4]
    y=int(re.search(r'-(\d{4})',name).group(1))
    sem=('SS%d'%y) if '-ss-' in name else 'WS%d/%02d'%(y,(y+1)%100)
    for p in open(f).read().split('\f'):
        if 'Fachsemesterzahlen' not in p: continue
        lines=p.split('\n')
        hi=next(i for i,l in enumerate(lines) if 'Fachsemesterzahlen' in l)
        title=[l.strip() for l in lines[:hi] if l.strip()][-1]
        if not re.search(r'Computerlinguistik|Computational Ling',title): continue
        fs=re.search(r'Fachschlüssel (\d+)',lines[hi]).group(1)
        ges=next(l for l in lines if 'Ges.HF' in l)
        ends=[m.end() for m in re.finditer(r'\d+',ges.split('Ges.HF')[1])]
        off=len(ges.split('Ges.HF')[0])+len('Ges.HF')
        ends=[e+off for e in ends]; assert len(ends)==15,(name,title,ges)
        gesvals=[int(x) for x in re.findall(r'\d+',ges.split('Ges.HF')[1])]
        deg=None; rows=[]
        for l in lines[hi+2:]:
            if 'Ges.HF' in l: break
            s=l.strip()
            if not s: continue
            m=re.match(r'\s*(HF|NF)\b(.*)',l)
            if m:
                pre=len(l)-len(l.lstrip())+2
                vals={}
                for n in re.finditer(r'\d+',l[pre:]):
                    e=n.end()+pre
                    j=min(range(15),key=lambda k:abs(ends[k]-e))
                    assert COLS[j] not in vals,(name,title,l)
                    vals[COLS[j]]=int(n.group())
                tot=sum(v for k,v in vals.items() if k!='Ges')
                ok = tot==vals.get('Ges')
                rows.append(dict(sem=sem,title=title,fs=fs,deg=deg,kind=m.group(1),vals=vals,ok=ok))
            else: deg=s
        # column check for HF
        for j,c in enumerate(COLS):
            sm=sum(r['vals'].get(c,0) for r in rows if r['kind']=='HF')
            if sm!=gesvals[j]: print('COLMISMATCH',sem,title,c,sm,gesvals[j])
        for r in rows:
            if not r['ok']: print('ROWMISMATCH',r)
        out+=rows
json.dump(out,open(sys.argv[2],'w'),ensure_ascii=False,indent=0)
for r in out:
    if r['deg'] and r['deg'].startswith('Bachelor'):
        print(r['sem'].ljust(10),r['fs'],r['deg'][:12].ljust(12),r['kind'],' '.join(str(r['vals'].get(c,'.')).rjust(3) for c in COLS))
