"""crop.py BOOK.pdf INDEX.json PDF_SONG_NO OUT.png [dpi]
PDF_SONG_NO is the number in the PDF, not the printed book. Name OUT after the song title.
Cut one song from the ICLA Song Book into a single tall image."""
import pymupdf, json, sys
from PIL import Image, ImageOps
book, idx, no, out = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4]
dpi = int(sys.argv[5]) if len(sys.argv) > 5 else 200
doc = pymupdf.open(book); S = json.load(open(idx))
i = next(k for k, s in enumerate(S) if s["no"] == no)
a = S[i]; b = S[i+1] if i+1 < len(S) else {"page": doc.page_count+1, "y": 0}
TOP, BOT = 6, 40           # page margins in pt (skip page number footer)
parts = []
for p in range(a["page"], b["page"]+1):
    if p > doc.page_count: break
    page = doc[p-1]; H = page.rect.height; W = page.rect.width
    y0 = a["y"]-8 if p == a["page"] else TOP
    if p == b["page"]:
        # next song's header (title may sit above its number): stop above it
        near = [w[1] for w in page.get_text("words") if b["y"]-45 < w[3] <= b["y"]+20 and w[1] < b["y"]+5]
        y1 = min([b["y"]] + near) - 8
    else:
        y1 = H-BOT
    if y1 - y0 < 20: continue
    pix = page.get_pixmap(dpi=dpi, clip=pymupdf.Rect(0, y0, W, y1), colorspace=pymupdf.csGRAY)
    im = Image.frombytes("L", (pix.width, pix.height), pix.samples)
    bbox = ImageOps.invert(im).point(lambda v: 255 if v > 40 else 0).getbbox()
    if bbox: parts.append(im.crop((0, bbox[1], im.width, bbox[3])))
# common horizontal trim
boxes = [ImageOps.invert(p).point(lambda v: 255 if v > 40 else 0).getbbox() for p in parts]
x0 = max(0, min(bx[0] for bx in boxes) - 20); x1 = min(parts[0].width, max(bx[2] for bx in boxes) + 20)
gap = int(dpi*0.15)
Hh = sum(p.height for p in parts) + gap*(len(parts)+1)
canvas = Image.new("L", (x1-x0, Hh), 255); y = gap
for p in parts:
    canvas.paste(p.crop((x0, 0, x1, p.height)), (0, y)); y += p.height + gap
# blank the PDF song number (the community's printed book is numbered differently)
from PIL import ImageDraw
ImageDraw.Draw(canvas).rectangle((0, 0, int(dpi*0.82)+20, int(dpi*0.54)), fill=255)
canvas = canvas.quantize(8, dither=Image.Dither.NONE)
canvas.save(out, optimize=True)
print(out, canvas.size, "pages", a["page"], "->", b["page"], "|", a["title"])
