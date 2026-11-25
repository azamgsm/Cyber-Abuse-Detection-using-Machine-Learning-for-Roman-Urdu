# text_utils.py
# Yeh file text saaf karne ka function rakhti hai.
# Notebook aur Flask app DONO isi ko use karte hain, taake dono jagah same cleaning ho.

import re

# Roman Urdu ke common stop words (aam lafz jin se abuse ka pata nahi chalta)
# NOTE: "nahi", "na", "mat" jaan bojh kar nahi rakhe, kyun ke negation ka matlab badal dete hain.
STOP_WORDS = {
    "hai", "hain", "ho", "hon", "tha", "thi", "the", "hoga", "hogi", "raha", "rahi", "rahe",
    "ka", "ki", "ke", "ko", "se", "me", "mein", "main", "par", "pe", "per", "tak",
    "aur", "ya", "ye", "yeh", "wo", "woh", "us", "is", "un", "in", "to", "toh", "bhi",
    "ne", "kya", "kyun", "kyu", "kia", "jo", "jis", "ek", "koi", "kuch", "hum", "ap", "aap",
    "tum", "mera", "meri", "mere", "tera", "teri", "tere", "apna", "apni", "apne",
    "kar", "karo", "kia", "kiya", "kr", "ha", "h", "hy", "hn", "ho", "the", "a", "an", "the", "and", "is", "of"
}

# Roman Urdu mein ek lafz ke kai spellings hote hain; sab ko ek spelling mein badlo
SPELLINGS = {
    "acha": ["achy", "achay", "achey", "ache", "achi", "achha", "achhe", "achhi", "acchi", "accha", "acche", "achaa"],
    "bohot": ["bohat", "buhat", "bahut", "bhot", "boht", "bahot", "bht"],
    "insan": ["insaan", "ensan", "insn"],
    "bewaqoof": ["bewakoof", "bewkoof", "bevkoof", "bewaqouf", "bewakuf"],
    "bekar": ["bekaar", "baikar", "bakar"],
    "aap": ["ap"],
    "tum": ["tm"],
    "nahi": ["nai", "nahin", "nhi", "nh"],
}
NORMALIZE = {variant: main for main, variants in SPELLINGS.items() for variant in variants}

def clean_text(text):
    """Ek comment ko saaf (clean) karke wapas deta hai."""
    text = str(text).lower()                          # 1) sab chhote (small) letters
    text = re.sub(r"http\S+|www\.\S+", " ", text)     # 2) links hatao
    text = re.sub(r"@\w+|#\w+", " ", text)            # 3) @mentions aur #hashtags hatao
    text = re.sub(r"[^a-z\s]", " ", text)             # 4) numbers, emoji, punctuation hatao (sirf a-z rakho)
    text = re.sub(r"(.)\1{2,}", r"\1\1", text)        # 5) "yaaaaar" -> "yaar" (3+ repeat ko 2 kar do)
    words = text.split()                               # 6) lafzon mein todo
    words = [NORMALIZE.get(w, w) for w in words]       # spelling ek jaisi karo
    words = [w for w in words if w not in STOP_WORDS]  # 7) stop words hatao
    return " ".join(words)                             # 8) wapas jod do
