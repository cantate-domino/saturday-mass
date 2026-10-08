# Saturday English Mass

Static page (GitHub Pages) with the three songs for the Saturday English Mass:
Entrance, Offertory, Recessional. Each song shows a YouTube recording and the
sheet music from the ICLA Song Book.

## Files
- `index.html` – the page (no build step)
- `data.js` – the weekly song list (newest week first)
- `sheets/<no>.png` – sheet music cut from the ICLA Song Book, named by song number
- `icons/` – Dominican seal icons
- `tools/crop.py` – cuts one song from `ICLA-SONG-BOOK.pdf` into `sheets/<song-title>.png`
- `tools/icla-index.json` – PDF song number → page/position in the PDF
- `tools/book-index.json` – index of the community's printed (older) book: title, book number, page, matching PDF number

## Weekly update
1. Add a new block at the top of `WEEKS` in `data.js` (date, three songs, YouTube links).
2. Look up the song in `tools/book-index.json` (book number for the page, `pdf` number for cutting), then
   `python3 tools/crop.py ICLA-SONG-BOOK.pdf tools/icla-index.json <pdf no> sheets/<song-title>.png`
   (the PDF number printed on the sheet is blanked out automatically)
3. Change `SITE.updated`, commit and push.

The page opens the next upcoming Saturday automatically (Vietnam time);
older weeks stay available in the "Week" menu.
