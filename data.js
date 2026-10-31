/* English Mass · St. Joseph Convent – song list
   Newest Mass FIRST (usually Saturday; any date works – the label follows the weekday).
   Each Mass has three songs: entrance, offertory, recessional (a communion song may be added: communion: {...}).
   no      = song number as printed in the community's own (older) ICLA book – see tools/book-index.json
   sheet   = sheet image file (named after the song title)
   youtube = any YouTube link (watch, youtu.be, shorts) – leave "" if none yet;
             the round play button next to the title only appears when there is a link
   start   = optional start time in seconds
   verses  = optional note on which verses to sing, shown under the title (e.g. "Sing verse 4");
             a sheet with those verses highlighted can be given as a separate image (e.g. sheets/i-go-my-merry-way-v4-ipa.png)
   feast   = optional celebration of the day, shown under the date
   A song left as {} shows "To be announced".
   mass    = optional sung Mass parts (Kyrie, Gloria, Alleluia, Holy, Mystery of Faith, Amen, Lamb of God), e.g. for a Sunday or solemnity:
             mass: { name, composer, kyrie: {title, youtube, start?, sheet, narrow?, text?}, gloria: {...}, alleluia, holy, mystery, amen, lamb }
             composer in a part overrides the setting's name ("" = none); text = a line shown under the title (e.g. the Alleluia verse).
             They are shown in the order of the Mass between the songs. narrow = optional sheet image for phones.
*/
window.SITE = {
  updated: "31 Oct 2026, 17:33 (UTC+7)"
};

window.WEEKS = [
  {
    date: "2026-11-01",
    feast: "Solemnity of All Saints",
    note: "",
    songs: {
      entrance:    { no: 127, title: "All the Ends of the Earth", composer: "Bob Dufford, S.J.", youtube: "https://youtu.be/WURSnRG-bkQ", sheet: "sheets/all-the-ends-of-the-earth-ipa.png" },
      offertory:   { no: 192, title: "Seed, Scattered and Sown", composer: "Dan Feiten", youtube: "https://youtu.be/b3wm1ZEXaiM", start: 13, sheet: "sheets/seed-scattered-and-sown-ipa.png" },
      communion:   { no: 173, title: "Christians, Let Us Love One Another", composer: "Tune: Picardy", youtube: "https://www.youtube.com/watch?v=zGnJ1C-zYCo", start: 17, sheet: "sheets/christians-let-us-love-ipa.png" },
      recessional: { no: 226, title: "I Go My Merry Way", composer: "Sœur Sourire, O.P.", youtube: "https://www.youtube.com/watch?v=y1TvgMx5fX8", sheet: "sheets/i-go-my-merry-way-v4-ipa.png", verses: "Sing verse 4" }
    },
    mass: {
      name: "Heritage Mass", composer: "Owen Alstott",
      kyrie:   { title: "Lord, Have Mercy",        youtube: "https://youtu.be/leRiEVeYosM", start: 4, sheet: "sheets/heritage-lord-have-mercy.png",        narrow: "sheets/heritage-lord-have-mercy-narrow.png" },
      gloria:  { title: "Glory to God",            youtube: "https://youtu.be/OiytzraJj34", start: 10, sheet: "sheets/heritage-glory-to-god.png",           narrow: "sheets/heritage-glory-to-god-narrow.png" },
      alleluia:{ title: "Sing Halleluia", composer: "", sheet: "sheets/sing-halleluia.png", narrow: "sheets/sing-halleluia-narrow.png",
                 text: "Verse: Come to me, all you who labor and are burdened, and I will give you rest, says the Lord. (Matthew 11:28)" },
      holy:    { title: "Holy",                    youtube: "https://youtu.be/tICAymLC6rY", start: 4, sheet: "sheets/heritage-holy.png",                   narrow: "sheets/heritage-holy-narrow.png" },
      mystery: { title: "We Proclaim Your Death",  youtube: "https://youtu.be/g4alz7JVzWM", start: 4, sheet: "sheets/heritage-we-proclaim-your-death.png", narrow: "sheets/heritage-we-proclaim-your-death-narrow.png" },
      amen:    { title: "Amen",                    youtube: "https://youtu.be/KnpHmv4_mFg", start: 9, sheet: "sheets/heritage-amen.png",                   narrow: "sheets/heritage-amen-narrow.png" },
      lamb:    { title: "Lamb of God",             youtube: "https://youtu.be/VqcB8wn_pgM", start: 5, sheet: "sheets/heritage-lamb-of-god.png",            narrow: "sheets/heritage-lamb-of-god-narrow.png" }
    }
  },
  {
    date: "2026-11-07",
    note: "",
    songs: {
      entrance:    { no: 141, title: "Shine, Jesus, Shine", composer: "Graham Kendrick", youtube: "https://youtu.be/AvMeTWAiUz8", start: 34, sheet: "sheets/shine-jesus-shine-ipa.png" },
      offertory:   { no: 192, title: "Seed, Scattered and Sown", composer: "Dan Feiten", youtube: "https://youtu.be/b3wm1ZEXaiM", start: 13, sheet: "sheets/seed-scattered-and-sown-ipa.png" },
      recessional: { no: 230, title: "Pray for the Departed Souls", composer: "", youtube: "https://youtu.be/Cu0sO8VOruc", start: 20, sheet: "sheets/for-the-departed-souls-ipa.png" }
    }
  },
  {
    date: "2026-10-31",
    feast: "Saturday of the Thirtieth Week in Ordinary Time",
    note: "",
    songs: {
      entrance:    { no: 129, title: "All the Earth", composer: "Lucien Deiss, C.S.Sp.", youtube: "https://youtu.be/j8IqqqajEbU", start: 8, sheet: "sheets/all-the-earth-ipa.png" },
      offertory:   { no: 173, title: "Christians, Let Us Love One Another", composer: "Tune: Picardy", youtube: "https://www.youtube.com/watch?v=zGnJ1C-zYCo", start: 17, sheet: "sheets/christians-let-us-love-ipa.png" },
      recessional: { no: 213, title: "Sing of Mary, Pure and Lowly", composer: "Joshua Leavitt", youtube: "https://youtu.be/dwA-fimg5W4", start: 10, sheet: "sheets/sing-of-mary-pure-and-lowly-ipa.png" }
    }
  },
  {
    date: "2026-10-24",
    feast: "Saturday Memorial of the Blessed Virgin Mary",
    note: "",
    songs: {
      entrance:    { no: 135, title: "Greetings to Jerusalem", composer: "R. Reboud", youtube: "https://youtu.be/ISEmh1jEYH0", start: 13, sheet: "sheets/greetings-to-jerusalem-ipa.png" },
      offertory:   { no: 155, title: "We Offer Our Lives", composer: "Tina Benitez", youtube: "https://youtu.be/pGQ7JHICTu4", start: 15, sheet: "sheets/we-offer-our-lives-ipa.png" },
      recessional: { no: 177, title: "Mary's Song", composer: "Tune: New Britain", youtube: "https://youtu.be/WQZVsXF-F_k", start: 16, sheet: "sheets/marys-song-ipa.png" }
    }
  },
  {
    date: "2026-10-17",
    feast: "Saint Ignatius of Antioch, Bishop and Martyr",
    note: "",
    songs: {
      entrance:    { no: 106, title: "When I Survey the Wondrous Cross", composer: "Tune: Hamburg", youtube: "https://youtu.be/RuyypOiCVag", start: 17, sheet: "sheets/when-i-survey-the-wondrous-cross-ipa.png" },
      offertory:   { no: 192, title: "Seed, Scattered and Sown", composer: "Dan Feiten", youtube: "https://youtu.be/b3wm1ZEXaiM", start: 13, sheet: "sheets/seed-scattered-and-sown-ipa.png" },
      recessional: { no: 176, title: "Here I Am, Lord", composer: "Dan Schutte, S.J.", youtube: "https://youtu.be/cDdniihKBzI", start: 12, sheet: "sheets/here-i-am-lord-ipa.png" }
    }
  },
  {
    date: "2026-10-10",
    note: "",
    songs: {
      entrance:    { no: 127, title: "All the Ends of the Earth", composer: "Bob Dufford, S.J.", youtube: "https://youtu.be/WURSnRG-bkQ", sheet: "sheets/all-the-ends-of-the-earth-ipa.png" },
      offertory:   { no: 173, title: "Christians, Let Us Love One Another", composer: "Tune: Picardy", youtube: "https://www.youtube.com/watch?v=zGnJ1C-zYCo", start: 17, sheet: "sheets/christians-let-us-love-ipa.png" },
      recessional: { no: 216, title: "Hail, Holy Queen", composer: "", youtube: "https://youtu.be/pSImGYMPNSU", start: 15, sheet: "sheets/hail-holy-queen-ipa.png" }
    }
  }
];
