# The "Your salah" content: the prayer in order, then the short surahs.
# Everything here is AWAITING TEACHER REVIEW: meanings, roots and notes are
# drafts. Build the app data with:  python3 tools/salah/build.py
#
# Prayer phrases (not Quran) are written here word by word: [arabic, meaning, root].
# Quran parts name their ayat; the text and roots come from quran-subset.json
# (Tanzil text, Quranic Arabic Corpus roots) and the meanings from QURAN_WORDS
# below, one entry per word, in order.

PARTS = [
  {"id": "takbir", "title": "Opening takbir", "ar_title": "تَكْبِيرَةُ الإِحْرامِ",
   "what": "Said with raised hands to begin the prayer; also said at every movement.",
   "lines": [{"en": "Allah is the Greatest.",
              "words": [["اللَّهُ", "Allah", "أله"], ["أَكْبَرُ", "is the Greatest", "كبر"]]}]},

  {"id": "opening", "title": "Opening supplication", "ar_title": "دُعاءُ الاسْتِفْتاحِ",
   "what": "Said quietly after the opening takbir, before Al-Fatiha.",
   "review_note": "Several authentic openings exist (e.g. اللَّهُمَّ باعِدْ بَيْنِي وَبَيْنَ خَطاياي...). This is the short one most commonly taught; the teacher chooses.",
   "lines": [{"en": "Glory be to You, O Allah, and with Your praise. Blessed is Your name, exalted is Your majesty, and there is no god other than You.",
              "words": [["سُبْحانَكَ", "Glory be to You", "سبح"], ["اللَّهُمَّ", "O Allah", "أله"],
                        ["وَبِحَمْدِكَ", "and with Your praise", "حمد"], ["وَتَبارَكَ", "and blessed is", "برك"],
                        ["اسْمُكَ", "Your name", "سمو"], ["وَتَعالى", "and exalted is", "علو"],
                        ["جَدُّكَ", "Your majesty", "جدد"], ["وَلا", "and there is no", ""],
                        ["إِلٰهَ", "god", "أله"], ["غَيْرُكَ", "other than You", "غير"]]}]},

  {"id": "refuge", "title": "Seeking refuge", "ar_title": "الاسْتِعاذَةُ",
   "what": "Said quietly before reciting Al-Fatiha.",
   "lines": [{"en": "I seek refuge in Allah from Satan, the outcast.",
              "words": [["أَعُوذُ", "I seek refuge", "عوذ"], ["بِاللَّهِ", "in Allah", "أله"],
                        ["مِنَ", "from", ""], ["الشَّيْطانِ", "Satan", "شطن"], ["الرَّجِيمِ", "the outcast", "رجم"]]}]},

  {"id": "fatiha1", "title": "Al-Fatiha (1)", "ar_title": "الفاتِحَةُ", "quran": ["1:1", "1:2", "1:3", "1:4"],
   "what": "Recited in every rak'ah: praise of Allah."},
  {"id": "fatiha2", "title": "Al-Fatiha (2)", "ar_title": "الفاتِحَةُ", "quran": ["1:5", "1:6", "1:7"],
   "what": "Recited in every rak'ah: the request for guidance.",
   "after": {"en": "Amin: O Allah, answer our prayer.", "review_note": "Not part of the Quran text; said after Al-Fatiha.",
             "words": [["آمِين", "Amin (O Allah, answer)", ""]]}},

  {"id": "ruku", "title": "Bowing", "ar_title": "الرُّكُوعُ",
   "what": "Said while bowing, usually three times.",
   "lines": [{"en": "Glory be to my Lord, the Magnificent.",
              "words": [["سُبْحانَ", "Glory be to", "سبح"], ["رَبِّيَ", "my Lord", "ربب"], ["الْعَظِيمِ", "the Magnificent", "عظم"]]}]},

  {"id": "rising", "title": "Rising from bowing", "ar_title": "الرَّفْعُ مِنَ الرُّكُوعِ",
   "what": "The first line is said while rising; the second once standing.",
   "review_note": "Also said as رَبَّنا لَكَ الْحَمْدُ (without وَ); both are authentic.",
   "lines": [{"en": "Allah hears the one who praises Him.",
              "words": [["سَمِعَ", "hears", "سمع"], ["اللَّهُ", "Allah", "أله"], ["لِمَنْ", "the one who", ""], ["حَمِدَهُ", "praises Him", "حمد"]]},
             {"en": "Our Lord, and to You belongs all praise.",
              "words": [["رَبَّنا", "Our Lord", "ربب"], ["وَلَكَ", "and to You (belongs)", ""], ["الْحَمْدُ", "all praise", "حمد"]]}]},

  {"id": "sujud", "title": "Prostration", "ar_title": "السُّجُودُ",
   "what": "Said in prostration, usually three times; the second line between the two prostrations.",
   "lines": [{"en": "Glory be to my Lord, the Most High.",
              "words": [["سُبْحانَ", "Glory be to", "سبح"], ["رَبِّيَ", "my Lord", "ربب"], ["الْأَعْلى", "the Most High", "علو"]]},
             {"en": "My Lord, forgive me.",
              "words": [["رَبِّ", "My Lord", "ربب"], ["اغْفِرْ", "forgive", "غفر"], ["لِي", "me", ""]]}]},

  {"id": "tashahhud", "title": "Tashahhud", "ar_title": "التَّشَهُّدُ",
   "what": "Said while sitting, after every second rak'ah and at the end of the prayer.",
   "review_note": "This is the wording narrated by Ibn Mas'ud. Other authentic wordings exist (e.g. Ibn Abbas: التَّحِيّاتُ الْمُبارَكاتُ...); the teacher chooses.",
   "lines": [{"en": "All greetings are for Allah, and the prayers and the good things.",
              "words": [["التَّحِيّاتُ", "All greetings", "حيي"], ["لِلَّهِ", "are for Allah", "أله"],
                        ["وَالصَّلَواتُ", "and the prayers", "صلو"], ["وَالطَّيِّباتُ", "and the good things", "طيب"]]},
             {"en": "Peace be upon you, O Prophet, and the mercy of Allah and His blessings.",
              "words": [["السَّلامُ", "Peace", "سلم"], ["عَلَيْكَ", "be upon you", ""], ["أَيُّها", "O", ""],
                        ["النَّبِيُّ", "Prophet", "نبأ"], ["وَرَحْمَةُ", "and the mercy", "رحم"], ["اللَّهِ", "of Allah", "أله"],
                        ["وَبَرَكاتُهُ", "and His blessings", "برك"]]},
             {"en": "Peace be upon us and upon the righteous servants of Allah.",
              "words": [["السَّلامُ", "Peace", "سلم"], ["عَلَيْنا", "be upon us", ""], ["وَعَلى", "and upon", ""],
                        ["عِبادِ", "the servants", "عبد"], ["اللَّهِ", "of Allah", "أله"], ["الصّالِحِينَ", "the righteous", "صلح"]]},
             {"en": "I bear witness that there is no god except Allah, and I bear witness that Muhammad is His servant and His Messenger.",
              "words": [["أَشْهَدُ", "I bear witness", "شهد"], ["أَنْ", "that", ""], ["لا", "there is no", ""],
                        ["إِلٰهَ", "god", "أله"], ["إِلَّا", "except", ""], ["اللَّهُ", "Allah", "أله"],
                        ["وَأَشْهَدُ", "and I bear witness", "شهد"], ["أَنَّ", "that", ""], ["مُحَمَّدًا", "Muhammad", "حمد"],
                        ["عَبْدُهُ", "is His servant", "عبد"], ["وَرَسُولُهُ", "and His Messenger", "رسل"]]}]},

  {"id": "salawat", "title": "Blessings on the Prophet", "ar_title": "الصَّلاةُ الإِبْراهِيمِيَّةُ",
   "what": "Said in the final sitting, after the tashahhud.",
   "review_note": "Wording varies slightly between narrations; the teacher chooses.",
   "lines": [{"en": "O Allah, send prayers upon Muhammad and upon the family of Muhammad,",
              "words": [["اللَّهُمَّ", "O Allah", "أله"], ["صَلِّ", "send prayers", "صلو"], ["عَلى", "upon", ""],
                        ["مُحَمَّدٍ", "Muhammad", "حمد"], ["وَعَلى", "and upon", ""], ["آلِ", "the family", "أول"], ["مُحَمَّدٍ", "of Muhammad", "حمد"]]},
             {"en": "as You sent prayers upon Ibrahim and upon the family of Ibrahim. Indeed, You are Praiseworthy, Glorious.",
              "words": [["كَما", "as", ""], ["صَلَّيْتَ", "You sent prayers", "صلو"], ["عَلى", "upon", ""], ["إِبْراهِيمَ", "Ibrahim", ""],
                        ["وَعَلى", "and upon", ""], ["آلِ", "the family", "أول"], ["إِبْراهِيمَ", "of Ibrahim", ""],
                        ["إِنَّكَ", "Indeed You are", ""], ["حَمِيدٌ", "Praiseworthy", "حمد"], ["مَجِيدٌ", "Glorious", "مجد"]]},
             {"en": "O Allah, bless Muhammad and the family of Muhammad,",
              "words": [["اللَّهُمَّ", "O Allah", "أله"], ["بارِكْ", "bless", "برك"], ["عَلى", "(upon)", ""],
                        ["مُحَمَّدٍ", "Muhammad", "حمد"], ["وَعَلى", "and (upon)", ""], ["آلِ", "the family", "أول"], ["مُحَمَّدٍ", "of Muhammad", "حمد"]]},
             {"en": "as You blessed Ibrahim and the family of Ibrahim. Indeed, You are Praiseworthy, Glorious.",
              "words": [["كَما", "as", ""], ["بارَكْتَ", "You blessed", "برك"], ["عَلى", "(upon)", ""], ["إِبْراهِيمَ", "Ibrahim", ""],
                        ["وَعَلى", "and (upon)", ""], ["آلِ", "the family", "أول"], ["إِبْراهِيمَ", "of Ibrahim", ""],
                        ["إِنَّكَ", "Indeed You are", ""], ["حَمِيدٌ", "Praiseworthy", "حمد"], ["مَجِيدٌ", "Glorious", "مجد"]]}]},

  {"id": "taslim", "title": "Closing salam", "ar_title": "التَّسْلِيمُ",
   "what": "Said turning the head to the right, then to the left, to end the prayer.",
   "lines": [{"en": "Peace be upon you and the mercy of Allah.",
              "words": [["السَّلامُ", "Peace", "سلم"], ["عَلَيْكُمْ", "be upon you", ""], ["وَرَحْمَةُ", "and the mercy", "رحم"], ["اللَّهِ", "of Allah", "أله"]]}]},
]

# Short surahs, in teaching order (most recited first).
SURAHS = [
  {"id": "ikhlas", "n": 112, "title": "Al-Ikhlas", "ar_title": "الإِخْلاصُ", "what": "Sincerity: who Allah is."},
  {"id": "falaq", "n": 113, "title": "Al-Falaq", "ar_title": "الفَلَقُ", "what": "Daybreak: seeking protection from harm."},
  {"id": "nas", "n": 114, "title": "An-Nas", "ar_title": "النّاسُ", "what": "Mankind: seeking protection from the whisperer."},
  {"id": "kawthar", "n": 108, "title": "Al-Kawthar", "ar_title": "الكَوْثَرُ", "what": "Abundance: the gift given to the Prophet ﷺ."},
  {"id": "nasr", "n": 110, "title": "An-Nasr", "ar_title": "النَّصْرُ", "what": "Help: victory, praise and seeking forgiveness."},
  {"id": "kafirun", "n": 109, "title": "Al-Kafirun", "ar_title": "الكافِرُونَ", "what": "The disbelievers: to you your religion, to me mine."},
  {"id": "masad", "n": 111, "title": "Al-Masad", "ar_title": "المَسَدُ", "what": "Palm fibre: the fate of Abu Lahab."},
  {"id": "maun", "n": 107, "title": "Al-Ma'un", "ar_title": "الماعُونَ", "what": "Small kindnesses: true prayer and helping others."},
  {"id": "quraysh", "n": 106, "title": "Quraysh", "ar_title": "قُرَيْشٌ", "what": "Quraysh: gratitude for safety and food."},
  {"id": "fil", "n": 105, "title": "Al-Fil", "ar_title": "الفِيلُ", "what": "The elephant: the army that marched on the Ka'bah."},
]

# Meaning of each ayah, and of each word in order (drafts, own wording).
QURAN = {
  "1:1": ("In the name of Allah, the Most Gracious, the Most Merciful.",
          ["In the name", "of Allah", "the Most Gracious", "the Most Merciful"]),
  "1:2": ("All praise is for Allah, Lord of the worlds.",
          ["All praise", "is for Allah", "Lord", "of the worlds"]),
  "1:3": ("The Most Gracious, the Most Merciful.", ["the Most Gracious", "the Most Merciful"]),
  "1:4": ("Master of the Day of Judgement.", ["Master", "of the Day", "of Judgement"]),
  "1:5": ("You alone we worship, and You alone we ask for help.",
          ["You alone", "we worship", "and You alone", "we ask for help"]),
  "1:6": ("Guide us to the straight path,", ["Guide us (to)", "the path", "the straight"]),
  "1:7": ("the path of those You have blessed, not of those who earned anger, nor of those who went astray.",
          ["the path", "of those (whom)", "You have blessed", "(upon them)", "not (of)", "those who earned anger", "(upon them)", "and nor", "those who went astray"]),

  "105:1": ("Have you not seen how your Lord dealt with the people of the elephant?",
            ["Have not", "you seen", "how", "dealt", "your Lord", "with the people", "of the elephant"]),
  "105:2": ("Did He not make their plan go astray?", ["Did not", "He make", "their plan", "into", "going astray"]),
  "105:3": ("And He sent against them birds in flocks,", ["And He sent", "against them", "birds", "in flocks"]),
  "105:4": ("striking them with stones of baked clay,", ["striking them", "with stones", "of", "baked clay"]),
  "105:5": ("and He made them like eaten-up straw.", ["and He made them", "like straw", "eaten up"]),

  "106:1": ("For the security of Quraysh,", ["For the security", "of Quraysh"]),
  "106:2": ("their security in the journeys of winter and summer,", ["their security", "(in) the journey", "of winter", "and summer"]),
  "106:3": ("let them worship the Lord of this House,", ["so let them worship", "the Lord", "of this", "House"]),
  "106:4": ("who fed them against hunger and made them safe from fear.",
            ["who", "fed them", "against", "hunger", "and made them safe", "from", "fear"]),

  "107:1": ("Have you seen the one who denies the Judgement?", ["Have you seen", "the one who", "denies", "the Judgement"]),
  "107:2": ("That is the one who pushes away the orphan", ["That", "is the one who", "pushes away", "the orphan"]),
  "107:3": ("and does not encourage feeding the poor.", ["and does not", "encourage", "(to)", "feeding", "the poor"]),
  "107:4": ("So woe to those who pray", ["So woe", "to those who pray"]),
  "107:5": ("who are heedless of their prayer,", ["who", "they", "of", "their prayer", "are heedless"]),
  "107:6": ("those who show off,", ["those who", "they", "show off"]),
  "107:7": ("and hold back small kindnesses.", ["and hold back", "small kindnesses"]),

  "108:1": ("Indeed, We have given you al-Kawthar (abundant good).", ["Indeed We", "have given you", "al-Kawthar (abundance)"]),
  "108:2": ("So pray to your Lord and sacrifice.", ["So pray", "to your Lord", "and sacrifice"]),
  "108:3": ("Indeed, your enemy is the one cut off.", ["Indeed", "your enemy", "he", "is the one cut off"]),

  "109:1": ("Say: O disbelievers,", ["Say", "O", "(you)", "disbelievers"]),
  "109:2": ("I do not worship what you worship,", ["I do not", "worship", "what", "you worship"]),
  "109:3": ("nor do you worship what I worship,", ["nor", "are you", "worshippers", "of what", "I worship"]),
  "109:4": ("nor will I worship what you worship,", ["nor", "am I", "a worshipper", "of what", "you worship"]),
  "109:5": ("nor will you worship what I worship.", ["nor", "are you", "worshippers", "of what", "I worship"]),
  "109:6": ("To you your religion, and to me mine.", ["To you", "your religion", "and to me", "my religion"]),

  "110:1": ("When the help of Allah comes, and the victory,", ["When", "comes", "the help", "of Allah", "and the victory"]),
  "110:2": ("and you see people entering the religion of Allah in crowds,",
            ["and you see", "the people", "entering", "into", "the religion", "of Allah", "in crowds"]),
  "110:3": ("then glorify your Lord with praise and ask His forgiveness. Indeed, He always accepts repentance.",
            ["then glorify", "with the praise", "of your Lord", "and ask His forgiveness", "Indeed He", "is ever", "accepting of repentance"]),

  "111:1": ("May the hands of Abu Lahab perish, and may he perish.", ["Perish", "the two hands", "of Abu", "Lahab", "and he perished"]),
  "111:2": ("His wealth and what he earned will not help him.", ["Will not", "help", "him", "his wealth", "and what", "he earned"]),
  "111:3": ("He will burn in a fire of blazing flame,", ["He will burn", "(in) a fire", "of", "blazing flame"]),
  "111:4": ("and his wife, the carrier of firewood,", ["and his wife", "the carrier", "of firewood"]),
  "111:5": ("around her neck a rope of palm fibre.", ["around", "her neck", "a rope", "of", "palm fibre"]),

  "112:1": ("Say: He is Allah, the One.", ["Say", "He", "is Allah", "the One"]),
  "112:2": ("Allah, the Eternal Refuge.", ["Allah", "the Eternal Refuge"]),
  "112:3": ("He does not give birth, nor was He born,", ["He does not", "give birth", "and not", "was He born"]),
  "112:4": ("and there is none equal to Him.", ["and not", "is", "to Him", "equal", "anyone"]),

  "113:1": ("Say: I seek refuge in the Lord of the daybreak", ["Say", "I seek refuge", "in the Lord", "of the daybreak"]),
  "113:2": ("from the evil of what He created,", ["from", "the evil", "of what", "He created"]),
  "113:3": ("and from the evil of the darkness when it settles,", ["and from", "the evil", "of darkness", "when", "it settles"]),
  "113:4": ("and from the evil of those who blow on knots,", ["and from", "the evil", "of those who blow", "on", "knots"]),
  "113:5": ("and from the evil of an envier when he envies.", ["and from", "the evil", "of an envier", "when", "he envies"]),

  "114:1": ("Say: I seek refuge in the Lord of mankind,", ["Say", "I seek refuge", "in the Lord", "of mankind"]),
  "114:2": ("the King of mankind,", ["the King", "of mankind"]),
  "114:3": ("the God of mankind,", ["the God", "of mankind"]),
  "114:4": ("from the evil of the whisperer who withdraws,", ["from", "the evil", "of the whisperer", "who withdraws"]),
  "114:5": ("who whispers into the hearts of mankind,", ["who", "whispers", "into", "the chests (hearts)", "of mankind"]),
  "114:6": ("from among the jinn and mankind.", ["from among", "the jinn", "and mankind"]),
}
