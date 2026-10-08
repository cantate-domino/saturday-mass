# Saturday English Mass

Static page (GitHub Pages) with the three songs for the Saturday English Mass:
Entrance, Offertory, Recessional. Each song shows a YouTube recording and the
sheet music from the ICLA Song Book.

## Files
- `index.html` – the page (no build step)
- `data.js` – the weekly song list (newest week first)
- `sheets/<no>.png` – sheet music cut from the ICLA Song Book, named by song number
- `icons/` – Dominican seal icons
- `tools/crop.py` – cuts one song from `ICLA-SONG-BOOK.pdf` into `sheets/<no>.png`
- `tools/icla-index.json` – song number → page/position in the PDF

## Weekly update
1. Add a new block at the top of `WEEKS` in `data.js` (date, three songs, YouTube links).
2. Cut any new sheet: `python3 tools/crop.py ICLA-SONG-BOOK.pdf tools/icla-index.json 177 sheets/177.png`
3. Change `SITE.updated`, commit and push.

The page opens the next upcoming Saturday automatically (Vietnam time);
older weeks stay available in the "Week" menu.
