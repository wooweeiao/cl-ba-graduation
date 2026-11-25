"""Tübingen CL BA (Hauptfach) cohort analysis from the Studierendenstatistik stock tables.
usage: analyze.py parsed.json outdir"""
import json,csv,sys,os,re
EXCLUDE={'SS2016'}   # semesters left out of the analysis
rows=[r for r in json.load(open(sys.argv[1])) if r['sem'] not in EXCLUDE]; out=sys.argv[2]
T=21; TMIN=1; KMAX=12   # sem_index 0 = SS2016 (excluded), 1 = WS2016/17, ..., 20 = SS2026
def tidx(s): return 2*(int(s[2:6])-2016)+(0 if s.startswith('SS') else 1)
def tname(t):
    y=2016+t//2
    return 'SS%d'%y if t%2==0 else 'WS%d/%02d'%(y,(y+1)%100)
COLS=[str(i) for i in range(13)]+['>12']
# ---------- 1. stock_long.csv : every row of the three Fachschlüssel, tidy
with open(os.path.join(out,'stock_long.csv'),'w',newline='') as f:
    w=csv.writer(f); w.writerow(['semester','sem_index','fachschluessel','fach','abschluss','hf_nf','fachsemester','count'])
    for r in rows:
        for c in COLS:
            if c in r['vals']: w.writerow([r['sem'],tidx(r['sem']),r['fs'],r['title'],r['deg'],r['kind'],c,r['vals'][c]])
# ---------- 2. BA-HF stock matrix summed over 160/161/162
M=[[0]*14 for _ in range(T)]
for r in rows:
    if r['deg'] and r['deg'].startswith('Bachelor') and r['kind']=='HF':
        for j,c in enumerate(COLS): M[tidx(r['sem'])][j]+=r['vals'].get(c,0)
def diag(t0): return [(M[t0+k-1][k] if TMIN<=t0+k-1<T else None) for k in range(1,KMAX+1)]
def add(a,b): return [None if (x is None or y is None) else x+y for x,y in zip(a,b)]
cohorts={'academic_year':{}, 'ws_only':{}}
for t0 in range(-11,T,2):   # WS entry semesters
    cohorts['ws_only'][tname(t0)]=diag(t0)
    cohorts['academic_year'][tname(t0)]=add(diag(t0),diag(t0+1)) if t0+1<T else diag(t0)
# WS2025/26 academic-year: SS2026 FS1 is observed (t=20), fine.
def event(k): return 'left_early' if k<=5 else 'graduation'
# ---------- 3. cohort_long.csv
recs=[]
for d,cs in cohorts.items():
    for name,N in cs.items():
        if all(x is None for x in N): continue
        entry=N[0] is not None and N[0]>0
        for k in range(1,KMAX):
            nk,nn=N[k-1],N[k]
            if nk is None: continue
            left=None if nn is None else nk-nn
            recs.append(dict(cohort_def=d,cohort=name,entry_observed=int(entry),n_entry=N[0] if entry else '',
                fachsemester=k,event=event(k),n_at_k=nk,n_at_k_plus_1='' if nn is None else nn,
                left_after_k='' if left is None else left,
                share_of_entrants='' if (left is None or not entry) else round(left/N[0],4),
                hazard='' if (left is None or nk==0) else round(left/nk,4)))
        if N[KMAX-1] is not None:
            recs.append(dict(cohort_def=d,cohort=name,entry_observed=int(entry),n_entry=N[0] if entry else '',fachsemester=KMAX,event='still_enrolled',
                n_at_k=N[KMAX-1],n_at_k_plus_1='',left_after_k='',share_of_entrants=round(N[KMAX-1]/N[0],4) if entry else '',hazard=''))
with open(os.path.join(out,'cohort_long.csv'),'w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(recs[0].keys())); w.writeheader(); w.writerows(recs)
# ---------- 4. pooled life table (cohorts with observed entry)
life={}
for d,cs in cohorts.items():
    S=1.0; tab=[]
    for k in range(1,KMAX):
        use=[(n,N) for n,N in cs.items() if N[0] not in (None,0) and N[k] is not None]
        a=sum(N[k-1] for _,N in use); b=sum(N[k] for _,N in use)
        h=(a-b)/a
        tab.append(dict(cohort_def=d,fachsemester=k,event=event(k),n_cohorts=len(use),cohorts=use[0][0]+'–'+use[-1][0],
            at_risk=a,left=a-b,hazard=round(h,4),surviving_before=round(S,4),share_of_entrants=round(S*h,4)))
        S*=1-h
    tab.append(dict(cohort_def=d,fachsemester=KMAX,event='still_enrolled',n_cohorts='',cohorts='',at_risk='',left='',hazard='',surviving_before=round(S,4),share_of_entrants=round(S,4)))
    life[d]=tab
with open(os.path.join(out,'lifetable.csv'),'w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(life['ws_only'][0].keys())); w.writeheader()
    for d in life: w.writerows(life[d])
json.dump(dict(semesters=[tname(t) for t in range(TMIN,T)],fachsemester_cols=COLS,stock_ba_hf=M[TMIN:],cohorts=cohorts,lifetable=life,
    rules=dict(left_early='leaves after Fachsemester 1-5',graduation='leaves after Fachsemester >=6')),
    open(os.path.join(out,'cl_ba.json'),'w'),ensure_ascii=False,indent=1)
# ---------- print
for d in ('academic_year','ws_only'):
    print('\n#####',d)
    print('cohort      N1 | left after FS1..5 (% of entrants)      | reach6 | grad after FS6..11 (% of entrants)        | cum<=6 <=7 <=8')
    for name,N in cohorts[d].items():
        if N[0] in (None,0): continue
        f=lambda k: '   . ' if N[k] is None else '%5.1f'%(100*(N[k-1]-N[k])/N[0])
        c=lambda m: '   . ' if N[m] is None else '%5.1f'%(100*(N[5]-N[m])/N[0])
        print(name.ljust(10),'%3d'%N[0],'|',' '.join(f(k) for k in range(1,6)),'|', '   . ' if N[5] is None else '%5.1f'%(100*N[5]/N[0]),'|',' '.join(f(k) for k in range(6,12)),'|',c(6),c(7),c(8))
    print('life table:')
    cum=0
    for r in life[d]:
        if r['event']=='graduation': cum+=r['share_of_entrants']
        print('  FS%2d %-14s hazard=%s share=%5.1f%%  S_before=%5.1f%%  at_risk=%s left=%s (%s cohorts %s)%s'%(r['fachsemester'],r['event'],('%5.1f%%'%(100*r['hazard'])) if r['hazard']!='' else '   -  ',100*r['share_of_entrants'],100*r['surviving_before'],r['at_risk'],r['left'],r['n_cohorts'],r['cohorts'],('  cumgrad=%.1f%%'%(100*cum)) if r['event']=='graduation' else ''))
