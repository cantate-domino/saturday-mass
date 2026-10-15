"""ipa_auto.py SHEET.png BANDS_JSON OUT.png [--dry]
Reads the lyric words from the sheet itself (tesseract OCR), looks up each word in CMUdict,
converts to American IPA (stress marks + syllable dots) and writes IPA + linking marks (consonant -> vowel)
under every lyric line. Nothing is typed in by hand except a few overrides for words missing from CMUdict.
BANDS_JSON = list of [ytop, ybottom] bands of the lyric rows (OCR 'top' values)."""
import csv, json, re, subprocess, sys, cmudict
from PIL import Image, ImageDraw, ImageFont

src, bands_s, out = sys.argv[1:4]
dry = '--dry' in sys.argv
SUBS = json.loads(sys.argv[sys.argv.index('--subs') + 1]) if '--subs' in sys.argv else []
bands = json.loads(bands_s)
D = cmudict.dict()

VOW = {'AA': 'ɑ', 'AE': 'æ', 'AH': 'ʌ', 'AO': 'ɔ', 'AW': 'aʊ', 'AY': 'aɪ', 'EH': 'ɛ', 'ER': 'ɝ', 'EY': 'eɪ',
       'IH': 'ɪ', 'IY': 'i', 'OW': 'oʊ', 'OY': 'ɔɪ', 'UH': 'ʊ', 'UW': 'u'}
CON = {'B': 'b', 'CH': 'tʃ', 'D': 'd', 'DH': 'ð', 'F': 'f', 'G': 'ɡ', 'HH': 'h', 'JH': 'dʒ', 'K': 'k', 'L': 'l',
       'M': 'm', 'N': 'n', 'NG': 'ŋ', 'P': 'p', 'R': 'r', 'S': 's', 'SH': 'ʃ', 'T': 't', 'TH': 'θ', 'V': 'v',
       'W': 'w', 'Y': 'j', 'Z': 'z', 'ZH': 'ʒ'}
LEGAL2 = {('P','R'),('B','R'),('T','R'),('D','R'),('K','R'),('G','R'),('F','R'),('TH','R'),('SH','R'),
          ('P','L'),('B','L'),('K','L'),('G','L'),('F','L'),('S','L'),('S','P'),('S','T'),('S','K'),('S','M'),
          ('S','N'),('S','W'),('T','W'),('K','W'),('D','W'),('TH','W'),('G','W'),('HH','Y'),('K','Y'),('P','Y'),('B','Y'),('M','Y'),('F','Y'),('V','Y'),('D','Y'),('N','Y'),('T','Y'),('S','Y'),('L','Y'),('TH','Y')}
WEAK = {'of': 'əv', 'the': 'ðə', 'a': 'ə', 'and': 'ænd', 'to': 'tu', 'is': 'ɪz', 'are': 'ɑr', 'our': 'aʊɚ', 'was': 'wʌz',
        'his': 'hɪz', 'her': 'hɝ', 'he': 'hi', 'we': 'wi', 'be': 'bi', 'who': 'hu', 'my': 'maɪ', 'for': 'fɔr', 'with': 'wɪð',
        'from': 'frʌm', 'that': 'ðæt', 'in': 'ɪn', 'by': 'baɪ', 'you': 'ju', 'on': 'ɑn'}
# CMUdict gaps (pieces are pronounced by hand once; everything else comes from the dictionary)
OVR = {'reechoes': ['R','IY0','EH1','K','OW0','Z'], 'courtyards': ['K','AO1','R','T','Y','AA2','R','D','Z'],
       'undefiled': ['AH2','N','D','IH0','F','AY1','L','D'], 'gladness': ['G','L','AE1','D','N','AH0','S'], 'forevermore': ['F','ER0','EH1','V','ER0','M','AO2','R']}
OVRIPA = {'enduring': 'ɪn.ˈdʊ.rɪŋ', 'blessed': 'ˈblɛ.sɪd', 'calvary': 'ˈkæl.və.ri', 'courtyards': 'ˈkɔrt.ˌjɑrdz'}
STOP = {'a','or','is','are','we','the','and','of','for','our','his','her','he','by','at','as','it','so','you','who','my','me','us','all','no','go','do','to'}


def phones(word):
    w = re.sub(r"[^a-z']", '', word.lower())
    if w in OVR: return OVR[w]
    if w in D: return D[w][0]
    if w.endswith("'s") and w[:-2] in D: return D[w[:-2]][0] + ['Z']
    return None


def syllabify(ph):
    """returns list of syllables, each = (stress, [phones])"""
    nuclei = [i for i, p in enumerate(ph) if p[-1].isdigit()]
    if not nuclei: return [(None, ph)]
    bounds = [0]
    for a, b in zip(nuclei, nuclei[1:]):
        cl = ph[a + 1:b]
        if len(cl) == 1 and cl[0] == 'NG': cut = b
        elif len(cl) <= 1: cut = a + 1 + 0
        elif len(cl) >= 2 and (cl[-2], cl[-1]) in LEGAL2: cut = b - 2
        else: cut = b - 1
        if len(cl) == 0: cut = b
        bounds.append(cut)
    bounds.append(len(ph))
    syl = []
    for k, n in enumerate(nuclei):
        seg = ph[bounds[k]:bounds[k + 1]]
        syl.append((int(ph[n][-1]), seg))
    return syl


def ipa_of(word):
    lw = re.sub(r"[^a-z']", '', word.lower())
    if lw in WEAK: return WEAK[lw], None
    if lw in OVRIPA: return OVRIPA[lw], phones(word)
    ph = phones(word)
    if ph is None: return None, None
    syl = syllabify(ph)
    outs = []
    for st, seg in syl:
        s = ''
        for p in seg:
            b = re.sub(r'\d', '', p)
            if p[-1:].isdigit() or b in VOW and p[-1:].isdigit():
                if b == 'AH': s += 'ʌ' if p[-1] in '12' else 'ə'
                elif b == 'ER': s += 'ɝ' if p[-1] in '12' else 'ɚ'
                else: s += VOW[b]
            else:
                s += CON[b]
        mark = 'ˈ' if st == 1 and len(syl) > 1 else ('ˌ' if st == 2 and len(syl) > 2 else '')
        outs.append(mark + s)
    return '.'.join(outs), ph


# ---------- OCR ----------
base = re.sub(r'\.png$', '', src)
subprocess.run(['tesseract', src, base, '--psm', '11', 'tsv'], stderr=subprocess.DEVNULL, check=True)
toks = []
for r in csv.DictReader(open(base + '.tsv'), delimiter='\t', quoting=csv.QUOTE_NONE):
    t = (r.get('text') or '').strip()
    if not t or float(r['conf']) < 0: continue
    toks.append(dict(t=t, x=int(r['left']), y=int(r['top']), w=int(r['width']), h=int(r['height'])))
im = Image.open(src).convert('RGB'); W, H = im.size

lines = []
for (y0, y1) in bands:
    tk = sorted([t for t in toks if y0 <= t['y'] <= y1], key=lambda t: t['x'])
    pieces = []
    for t in tk:
        for part in re.split(r'[-–—_]+', t['t']):
            orig = part
            part = re.sub(r"^[\d.,]+", '', part)
            q = re.sub(r"[^A-Za-z']", '', part)
            if part.strip() in ('(0)', '(O)', '0'): q = 'O'
            if part.strip() == '|': q = 'I'
            if re.fullmatch(r'\d\.[1lI|]', orig.strip()): q = 'I'
            if not q: continue
            n = len(re.split(r'[-–—_]+', t['t']))
            pieces.append(dict(q=q, x=t['x'], x2=t['x'] + t['w'], y=t['y'], b=t['y'] + t['h']))
    # drop one-letter junk (OCR noise), keep real one-letter words a/I/O
    keep = []
    for k, p in enumerate(pieces):
        ok = len(p['q']) > 1 or p['q'] in ('a', 'A', 'I', 'O')
        if p['q'].lower() == 'y' and keep and p['x'] - keep[-1]['x2'] < 60: ok = True
        if ok: keep.append(p)
    pieces = keep
    for (ln, old, new, nx, nx2) in SUBS:
        if ln == len(lines) and old == '+':
            pieces.append(dict(q=new, x=nx, x2=nx2, y=0, b=max(p['b'] for p in pieces)))
    pieces.sort(key=lambda p: p['x'])
    for (ln, old, new, nx, nx2) in SUBS:
        if ln == len(lines) and old != '+':
            for p in pieces:
                if p['q'] == old: p['q'] = new; p['x'] = nx or p['x']; p['x2'] = nx2 or p['x2']
        np_ = []
        for p in pieces:
            if ' ' in p['q']:
                ws = p['q'].split(); tot = sum(len(w) for w in ws); x = p['x']
                for w in ws:
                    wd = (p['x2'] - p['x']) * len(w) / tot
                    np_.append(dict(q=w, x=int(x), x2=int(x + wd - 3), y=p['y'], b=p['b'])); x += wd
            else: np_.append(p)
        pieces = [p for p in np_ if p['q']]
    # greedy merge of adjacent pieces that form a dictionary word
    words = []; i = 0
    while i < len(pieces):
        done = False
        for j in range(min(len(pieces), i + 4), i + 1, -1):
            grp = pieces[i:j]
            if any(grp[k + 1]['x'] - grp[k]['x2'] > 110 for k in range(len(grp) - 1)): continue
            if grp[0]['q'].lower() in STOP and len(grp) == 2 and ''.join(p['q'] for p in grp).lower() not in ('into','unto','without','became','ascends','forget','orphaned'): continue
            if ''.join(p['q'] for p in grp).lower() in ('littlechild',): continue
            if any(p['q'] == 'I' for p in grp[1:]): continue
            cat = ''.join(p['q'] for p in grp).lower()
            if cat in OVR or cat in D:
                words.append(dict(q=cat, x=grp[0]['x'], x2=grp[-1]['x2'], b=max(p['b'] for p in grp), raw=[p['q'] for p in grp]))
                i = j; done = True; break
        if not done:
            p = pieces[i]; words.append(dict(q=p['q'], x=p['x'], x2=p['x2'], b=p['b'], raw=[p['q']])); i += 1
    lines.append(words)

# IPA + links
res = []
for words in lines:
    L = []
    for w in words:
        ipa, ph = ipa_of(w['q'])
        if ipa is None:
            print('!! no dictionary entry:', w['q'], w['raw'])
            ipa = '?'
        L.append((w, ipa, ph))
    res.append(L)

VOWELS = set(VOW)
def starts_vowel(ph, q):
    if ph: return re.sub(r'\d', '', ph[0]) in VOWELS
    return q[0] in 'aeiou'
def ends_cons(ph, q):
    if ph: return re.sub(r'\d', '', ph[-1]) not in VOWELS
    return False

for n, L in enumerate(res):
    s = ' | '.join(f"{w['q']}[{ipa}]" for w, ipa, ph in L)
    print(n, s)
if dry: sys.exit()

G = 26
cuts = []
for L in res:
    cuts.append(max(w['b'] for w, _, _ in L) + 5)
out_h = H + G * len(cuts); new = Image.new('RGB', (W, out_h), 'white')
prev = 0; off = 0; offs = []
for c in cuts:
    new.paste(im.crop((0, prev, W, c)), (0, prev + off)); offs.append(off); prev = c; off += G
new.paste(im.crop((0, prev, W, H)), (0, prev + off))
d = ImageDraw.Draw(new)
f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 15)
fl = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 22)
RED = (160, 30, 40); BLUE = (30, 80, 160)
nlinks = 0
for L, c, o in zip(res, cuts, offs):
    base_y = c + o
    for k, (w, ipa, ph) in enumerate(L):
        cx = (w['x'] + w['x2']) / 2; tw = d.textlength(ipa, font=f)
        d.text((cx - tw / 2, base_y + 3), ipa, font=f, fill=RED)
        if k + 1 < len(L):
            w2, _, ph2 = L[k + 1]
            if ends_cons(ph, w['q']) and starts_vowel(ph2, w2['q']):
                cx2 = (w['x2'] + w2['x']) / 2
                d.text((cx2 - 7, c - 19 + o), '‿', font=fl, fill=BLUE); nlinks += 1
new = new.quantize(32, dither=Image.Dither.NONE)
new.save(out, optimize=True)
print(out, new.size, 'links', nlinks)
