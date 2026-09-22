"""Choose a picture (emoji) for each word in the learning path.

    TYPESAFE_API_KEY=... python3 tools/typesafe-exp/pick_pictures.py

Select, don't generate: TypeSafe picks from a fixed list of emoji, or none.
A picture is kept only when the word is a concrete, picturable thing and the
choice is confident; abstract words, verbs and grammar words get none.
Writes PIC into path-data.js (tools/build-path.js keeps it on rebuild).
"""
import json, os, re
from concurrent.futures import ThreadPoolExecutor
from run import ask

ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
EMOJI = {
 "👨": "man, father", "👩": "woman, mother", "👦": "boy, son", "👧": "girl, daughter", "👴": "old man, grandfather",
 "👵": "old woman, grandmother", "👶": "baby", "👪": "family", "🧑‍🎓": "student", "🧑‍🏫": "teacher",
 "🧑‍⚕️": "doctor, nurse", "🧑‍🔧": "mechanic, engineer, workman", "🧑‍🍳": "cook", "🧑‍💼": "office worker, employee, accountant",
 "👮": "police officer", "🧑‍🌾": "farmer", "🤝": "friend, meeting, handshake", "👋": "hello, goodbye, wave",
 "🏠": "house, home", "🏢": "building, company, office", "🏫": "school", "🏥": "hospital", "🕌": "mosque",
 "🕋": "Kaaba, Mecca", "🏪": "shop, store", "🏦": "bank", "🏨": "hotel", "🏛️": "museum", "🏭": "factory",
 "🛏️": "bed, bedroom", "🛋️": "sofa, sitting room", "🪑": "chair", "🚪": "door", "🪟": "window", "🪞": "mirror",
 "🚿": "shower, bathroom", "🛁": "bath", "🚽": "toilet", "🍳": "kitchen, cooking, frying pan", "🧺": "laundry, basket",
 "🧹": "broom, sweeping", "📺": "television", "💻": "computer, laptop", "📱": "mobile phone", "☎️": "telephone",
 "🕰️": "clock", "⌚": "watch", "⏰": "alarm clock", "📅": "calendar, date, day", "🗓️": "week, month, timetable",
 "📚": "books, library", "📖": "book, reading", "✏️": "pencil, pen", "🖊️": "pen", "📓": "notebook", "🎒": "school bag",
 "📰": "newspaper", "✉️": "letter, envelope", "🗺️": "map", "🧮": "counting, mathematics", "🔬": "science, laboratory",
 "🎨": "drawing, painting, art", "🖌️": "brush, calligraphy", "⚽": "football", "🏊": "swimming", "🏃": "running",
 "🚴": "cycling", "🎮": "games", "🎵": "music", "📷": "camera, photo", "🖼️": "picture, photo, painting",
 "🧵": "sewing", "🌱": "gardening, plant", "🎣": "fishing", "📮": "stamps, post",
 "🚗": "car", "🚌": "bus", "🚆": "train", "✈️": "plane, airport", "🚲": "bicycle", "🚕": "taxi", "🚢": "ship",
 "🛣️": "road", "🌉": "bridge", "🚦": "traffic lights", "⛽": "petrol station", "🧳": "suitcase, travel",
 "🍞": "bread", "🍚": "rice", "🍗": "chicken (food)", "🥩": "meat", "🐟": "fish", "🥚": "egg", "🧀": "cheese",
 "🥛": "milk", "☕": "coffee", "🍵": "tea", "💧": "water", "🧃": "juice", "🍎": "apple", "🍊": "orange (fruit)",
 "🍌": "banana", "🍇": "grapes", "🍉": "watermelon", "🍓": "strawberry", "🍋": "lemon", "🌴": "palm tree",
 "🫘": "beans", "🥕": "carrot", "🍅": "tomato", "🧅": "onion", "🥒": "cucumber", "🥔": "potato", "🥗": "salad",
 "🍰": "cake", "🍬": "sweets", "🍯": "honey", "🧂": "salt", "🍽️": "meal, plate, dishes", "🥄": "spoon", "🍴": "fork, knife",
 "🥤": "drink", "🍲": "soup, stew, food", "🥐": "breakfast pastry", "🌅": "morning, dawn, sunrise", "🌇": "evening, sunset",
 "🌙": "night, moon", "⭐": "star", "☀️": "sun, sunny", "☁️": "cloud, cloudy", "🌧️": "rain", "❄️": "snow, cold",
 "🌬️": "wind", "🌡️": "temperature, heat", "🔥": "fire, hot", "🌈": "rainbow", "⛈️": "storm",
 "🌸": "spring, flower", "🍂": "autumn", "🏖️": "beach, summer", "⛰️": "mountain", "🏜️": "desert", "🌊": "sea",
 "🏞️": "river, nature, park", "🌳": "tree, garden", "🏙️": "city", "🏘️": "village, neighbourhood", "🌍": "world, earth, country",
 "🐪": "camel", "🐎": "horse", "🐄": "cow", "🐑": "sheep", "🐐": "goat", "🐓": "chicken, rooster (animal)",
 "🐈": "cat", "🐕": "dog", "🐦": "bird", "🐝": "bee", "🦁": "lion", "🐘": "elephant", "🐜": "ant", "🐍": "snake",
 "🐠": "tropical fish",
 "👕": "shirt, t-shirt", "👗": "dress", "👖": "trousers", "👟": "shoes", "🧥": "coat, jacket", "🧣": "scarf",
 "🧕": "headscarf, hijab", "👓": "glasses", "👜": "handbag", "💍": "ring", "🧦": "socks", "👔": "suit, tie",
 "💰": "money", "💵": "cash, price", "🛒": "shopping, market cart", "🏷️": "price tag", "🎁": "gift",
 "❤️": "heart, love", "🦷": "tooth", "👁️": "eye", "👂": "ear", "👃": "nose", "👄": "mouth", "✋": "hand",
 "🦶": "foot", "💪": "arm, strong", "🧠": "head, brain", "🤒": "ill, fever", "💊": "medicine", "🩺": "check-up",
 "🕋 ": "Hajj", "📿": "prayer beads, dhikr", "🤲": "dua, supplication", "🧎": "prostration, prayer", "📜": "Qur'an, scroll",
 "🌙 ": "Ramadan, crescent", "🕯️": "candle", "🔑": "key", "🎓": "graduation, university", "🏆": "prize, winning",
 "1️⃣": "one", "2️⃣": "two", "3️⃣": "three", "4️⃣": "four", "5️⃣": "five", "6️⃣": "six", "7️⃣": "seven",
 "8️⃣": "eight", "9️⃣": "nine", "🔟": "ten",
 "none": "None of these pictures clearly shows the word",
}

def load_js(file, *names):
    src = open(os.path.join(ROOT, file), encoding="utf8").read()
    out = {}
    for n in names:
        m = re.search(r"const\s+" + n + r"\s*=\s*(\[.*?\]|\{.*?\});\s*\n", src, re.S)
        out[n] = m.group(1) if m else None
    return out

def main():
    import subprocess
    words = json.loads(subprocess.check_output(["node", "-e", """
      const fs=require('fs');
      let v=fs.readFileSync('vocab-data.js','utf8').replace(/const\\s+VOCAB\\s*=/,'globalThis.VOCAB=');eval(v);
      let p=fs.readFileSync('path-data.js','utf8').replace(/const\\s+(PATH|PIC)\\s*=/g,'globalThis.$1=');eval(p);
      const ids=new Set(PATH.flatMap(u=>u.words));
      console.log(JSON.stringify(VOCAB.filter(w=>ids.has(w.id)).map(w=>({id:w.id,ar:w.ar,en:w.en}))));"""], cwd=ROOT))
    Q = {
        "concrete": {"type": "noul", "instructions": "Is `english` a concrete, physical thing, place, person, animal, food or weather "
                     "that a single small picture could show clearly? (Verbs, feelings, grammar words, question words and "
                     "abstract ideas are not.)"},
        "pic": {"type": "choice", "instructions": "Which picture best shows the meaning of the Arabic word `arabic` (`english`)?",
                "criteria": EMOJI},
    }
    with ThreadPoolExecutor(8) as ex:
        res = list(ex.map(lambda w: ask({"arabic": w["ar"], "english": w["en"]}, Q), words))
    pic = {}
    for w, r in zip(words, res):
        a = r["answers"]; ch = a["pic"]["choice"].strip()
        if a["concrete"]["noul"] >= 0.7 and ch != "none" and a["pic"]["probabilities"].get(a["pic"]["choice"], 0) >= 0.6:
            pic[w["id"]] = ch
    print(f"pictures for {len(pic)} of {len(words)} path words")
    for w in words[:400]:
        if w["id"] in pic: print(f"  {pic[w['id']]}  {w['en']}")
    p = os.path.join(ROOT, "path-data.js")
    s = open(p, encoding="utf8").read()
    s = re.sub(r"const PIC = \{.*?\};", "const PIC = " + json.dumps({str(k): v for k, v in pic.items()}, ensure_ascii=False) + ";", s, flags=re.S)
    open(p, "w", encoding="utf8").write(s)

if __name__ == "__main__":
    main()
