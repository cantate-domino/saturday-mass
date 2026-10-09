/* Saturday English Mass – song list
   Newest week FIRST. Each week has three songs: entrance, offertory, recessional.
   no      = song number as printed in the community's own (older) ICLA book – see tools/book-index.json
   sheet   = sheet image file (named after the song title)
   youtube = any YouTube link (watch, youtu.be, shorts) – leave "" if none yet;
             the round play button next to the title only appears when there is a link
   start   = optional start time in seconds
   feast   = optional celebration of the day, shown under the date
   presider / reader = from the monthly liturgy duty roster (chủ tế / BĐ)
   A song left as {} shows "To be announced".
*/
window.SITE = {
  updated: "09 Oct 2026, 08:59 (UTC+7)"
};

window.WEEKS = [
  {
    date: "2026-10-24",
    feast: "Saturday Memorial of the Blessed Virgin Mary",
    presider: "fr. Khải Hoàn",
    reader: "fr. Công Hàm",
    note: "",
    songs: {
      entrance:    { no: 135, title: "Greetings to Jerusalem", composer: "R. Reboud", youtube: "https://youtu.be/ISEmh1jEYH0", start: 13, sheet: "sheets/greetings-to-jerusalem.png" },
      offertory:   { no: 155, title: "We Offer Our Lives", composer: "Tina Benitez", youtube: "https://youtu.be/pGQ7JHICTu4", start: 15, sheet: "sheets/we-offer-our-lives.png" },
      recessional: { no: 177, title: "Mary's Song", composer: "Tune: New Britain", youtube: "https://youtu.be/WQZVsXF-F_k", start: 16, sheet: "sheets/marys-song.png" }
    }
  },
  {
    date: "2026-10-17",
    feast: "Saint Ignatius of Antioch, Bishop and Martyr",
    presider: "fr. Công Hàm",
    reader: "fr. Trần Hiệu",
    note: "",
    songs: {
      entrance:    { no: 106, title: "When I Survey the Wondrous Cross", composer: "Tune: Hamburg", youtube: "https://youtu.be/RuyypOiCVag", start: 17, sheet: "sheets/when-i-survey-the-wondrous-cross.png" },
      offertory:   { no: 192, title: "Seed, Scattered and Sown", composer: "Dan Feiten", youtube: "https://youtu.be/b3wm1ZEXaiM", start: 13, sheet: "sheets/seed-scattered-and-sown.png" },
      recessional: { no: 176, title: "Here I Am, Lord", composer: "Dan Schutte, S.J.", youtube: "https://youtu.be/cDdniihKBzI", start: 12, sheet: "sheets/here-i-am-lord.png" }
    }
  },
  {
    date: "2026-10-10",
    presider: "fr. Trị An",
    reader: "fr. Công Hàm",
    note: "",
    songs: {
      entrance:    { no: 127, title: "All the Ends of the Earth", composer: "Bob Dufford, S.J.", youtube: "https://youtu.be/WURSnRG-bkQ", sheet: "sheets/all-the-ends-of-the-earth.png" },
      offertory:   { no: 173, title: "Christians, Let Us Love One Another", composer: "Tune: Picardy", youtube: "https://www.youtube.com/watch?v=zGnJ1C-zYCo", start: 17, sheet: "sheets/christians-let-us-love.png" },
      recessional: { no: 216, title: "Hail, Holy Queen", composer: "", youtube: "https://youtu.be/pSImGYMPNSU", start: 15, sheet: "sheets/hail-holy-queen.png" }
    }
  }
];
