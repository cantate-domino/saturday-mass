import csv,re,sys,difflib
sys.path.insert(0,'/tmp/ipa/tools')
import importlib
from PIL import Image,ImageDraw,ImageFont
src,tsv,out,mod=sys.argv[1:5]
M=importlib.import_module(mod); LINES,LINKS=M.LINES,M.LINKS
im=Image.open(src).convert('RGB'); W,H=im.size
toks=[]
for r in csv.DictReader(open(tsv),delimiter='\t',quoting=csv.QUOTE_NONE):
    t=(r.get('text') or '').strip().replace('|','I')
    if not t or float(r['conf'])<0: continue
    x,y,w,h=int(r['left']),int(r['top']),int(r['width']),int(r['height'])
    parts=[p for p in re.split(r'-',t) if p]
    n=max(1,len(parts)); 
    for k,p in enumerate(parts):
        q=re.sub(r"[^a-z']","",p.lower())
        if q: toks.append(dict(x=x+w*k/n,w=w/n,y=y,t=q))
norm=lambda s:re.sub(r"[^a-z']","",s.lower())
layout={}
for ly,words in LINES.items():
    lt=sorted([t for t in toks if abs(t['y']-ly)<=12],key=lambda t:t['x'])
    syl=[(wi,s) for wi,(ss,_) in enumerate(words) for s in ss]
    pos=[None]*len(syl); j=0
    for i,(wi,s) in enumerate(syl):
        best=None
        for k in range(j,min(j+4,len(lt))):
            a,b=norm(s),lt[k]['t']
            sc=1 if (a==b or (len(a)>2 and (a in b or b in a))) else (0 if len(a)<=2 or len(b)<=2 else difflib.SequenceMatcher(None,a,b).ratio())
            if sc>=0.66: best=k;break
        if best is not None: pos[i]=(lt[best]['x'],lt[best]['x']+lt[best]['w']); j=best+1
    # interpolate
    known=[i for i,p in enumerate(pos) if p]
    for i,p in enumerate(pos):
        if p: continue
        lft=max([k for k in known if k<i],default=None); rgt=min([k for k in known if k>i],default=None)
        if lft is not None and rgt is not None:
            f=(i-lft)/(rgt-lft); x=pos[lft][1]+(pos[rgt][0]-pos[lft][1])*f; pos[i]=(x-12,x+12)
        elif lft is not None: x=pos[lft][1]+40; pos[i]=(x,x+24)
        else: x=pos[rgt][0]-40; pos[i]=(x-24,x)
    spans={}
    for (wi,_),p in zip(syl,pos):
        a,b=spans.get(wi,(p[0],p[1])); spans[wi]=(min(a,p[0]),max(b,p[1]))
    layout[ly]=spans
    print(ly,'matched',len(known),'/',len(syl))
# build stretched image: insert gap below each lyric line
G=26
cuts=sorted(ly+25 for ly in LINES)
out_h=H+G*len(cuts); new=Image.new('RGB',(W,out_h),'white')
prev=0; off=0; offs={}
for c in cuts:
    new.paste(im.crop((0,prev,W,c)),(0,prev+off)); offs[c]=off; prev=c; off+=G
new.paste(im.crop((0,prev,W,H)),(0,prev+off))
d=ImageDraw.Draw(new); f=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',15)
fl=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',22)
RED=(160,30,40); BLUE=(30,80,160)
for ly,words in LINES.items():
    o=offs[ly+25]; base=ly+25+o
    for wi,(ss,ipa) in enumerate(words):
        a,b=layout[ly][wi]; cx=(a+b)/2; tw=d.textlength(ipa,font=f)
        d.text((cx-tw/2,base+3),ipa,font=f,fill=RED)
    for wi in LINKS.get(ly,[]):
        a=layout[ly][wi][1]; b=layout[ly][wi+1][0]; cx=(a+b)/2
        d.text((cx-7,ly+o+8),'‿',font=fl,fill=BLUE)
new.save(out)
print(out,new.size)
