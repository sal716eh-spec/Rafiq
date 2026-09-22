/* The reading starter (unit 0): the 28 letters in groups that share a shape,
   then the vowel marks. Each letter: [letter, name, how it sounds, example word,
   example meaning]. Letters marked * never join to the letter after them. */
const ALPHABET_GROUPS = [
  {title:'Letters 1: the "boat" shapes', letters:[
    ['ا','أَلِف','A long "aa", or a seat for a glottal stop (the catch in "uh-oh") *','أَسَد','lion'],
    ['ب','باء','"b" as in "bed" — one dot below','بَيْت','house'],
    ['ت','تاء','"t" as in "tea" — two dots above','تَمْر','dates'],
    ['ث','ثاء','"th" as in "think" — three dots above','ثَلاثَة','three']]},
  {title:'Letters 2: the "hook" shapes', letters:[
    ['ج','جِيم','"j" as in "jam" — dot inside','جَمَل','camel'],
    ['ح','حاء','A breathy "h" from deep in the throat — no dot','حَلِيب','milk'],
    ['خ','خاء','"kh" as in Scottish "loch" — dot above','خُبْز','bread']]},
  {title:'Letters 3: small letters that don\'t join', letters:[
    ['د','دال','"d" as in "door" *','دَرْس','lesson'],
    ['ذ','ذال','"th" as in "this" *','ذَهَب','gold'],
    ['ر','راء','A rolled "r" *','رَجُل','man'],
    ['ز','زاي','"z" as in "zoo" *','زَيْت','oil']]},
  {title:'Letters 4: the "teeth" shapes', letters:[
    ['س','سِين','"s" as in "sun"','سَمَك','fish'],
    ['ش','شِين','"sh" as in "ship" — three dots','شَمْس','sun'],
    ['ص','صاد','A heavy "s", said with the tongue low','صَدِيق','friend'],
    ['ض','ضاد','A heavy "d" — the letter Arabic is famous for','ضَيْف','guest']]},
  {title:'Letters 5: tall letters and the throat', letters:[
    ['ط','طاء','A heavy "t"','طالِب','student'],
    ['ظ','ظاء','A heavy "th" as in "this"','ظُهْر','noon'],
    ['ع','عَيْن','ʿayn: a squeeze deep in the throat — no English sound like it','عَيْن','eye'],
    ['غ','غَيْن','"gh", like a French "r"','غُرْفَة','room']]},
  {title:'Letters 6: loops and hooks', letters:[
    ['ف','فاء','"f" as in "fish" — one dot above','فِيل','elephant'],
    ['ق','قاف','"q": a "k" from far back in the throat — two dots','قَلَم','pen'],
    ['ك','كاف','"k" as in "kite"','كِتاب','book'],
    ['ل','لام','"l" as in "lamp"','لَيْل','night']]},
  {title:'Letters 7: the last five', letters:[
    ['م','مِيم','"m" as in "moon"','ماء','water'],
    ['ن','نُون','"n" as in "noon" — one dot above','نُور','light'],
    ['ه','هاء','"h" as in "hat"','هِلال','crescent moon'],
    ['و','واو','"w", or a long "oo" *','وَلَد','boy'],
    ['ي','ياء','"y", or a long "ee" — two dots below','يَد','hand']]},
];
/* Vowel marks, shown on ب. [written, sound, what it is] */
const VOWEL_MARKS = [
  ['بَ','ba','Fatha — a small stroke above: a short "a"'],
  ['بِ','bi','Kasra — a small stroke below: a short "i"'],
  ['بُ','bu','Damma — a small curl above: a short "u"'],
  ['بْ','b','Sukun — a small circle: no vowel after the letter'],
  ['بّ','bb','Shadda — a small "w": the letter is doubled'],
  ['با','baa','Alif after fatha — a long "aa"'],
  ['بي','bii','Ya after kasra — a long "ee"'],
  ['بو','buu','Waw after damma — a long "oo"'],
  ['بٌ','bun','Tanwin — a doubled mark: adds "n" at the end of a word'],
];
