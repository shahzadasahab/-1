#!/usr/bin/env python3
"""Turn extracted cheat-sheet cards into spoken Urdish narration.

The PDF text is column debris: broken lines, gate labels, and bare formulas.
This pass rewrites each card as a short teacher script in Roman Urdu plus the
English terms the paper expects.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "csheet" / "src" / "main" / "assets" / "www" / "content"

NOISE = re.compile(
    r"^(?:[A-DXYVTabc]|[01]|HIGH(?:\s*1)?|LOW(?:\s*0)?|AND|OR|NOT|NAND|NOR|XOR|XNOR|Day|○|O)$",
    re.I,
)

DIAGRAM_LINE = {
    "stairs-ramp": "Diagram mein discrete seedhiyon ki tarah hai, sirf ginte hue steps. Continuous ek ramp hai, beech ki koi bhi height.",
    "analog-digital": "Diagram mein analog ek smooth sine wave hai, aur digital HIGH aur LOW ke beech square jump hai.",
    "gates-basic": "Diagram mein AND ki shape D jaisi hai, OR dhal ki tarah, aur NOT ek triangle hai jiske aage chhota bubble hai.",
    "gates-universal": "NAND, AND ke output pe bubble hai. NOR, OR ke output pe bubble hai. Bubble ka matlab NOT hai.",
    "gates-xor": "XOR, OR ki peechhe ek extra curve hai, aur tab ek hota hai jab inputs alag hon. XNOR pe bubble hai, jab inputs same hon.",
    "logic-circuit": "Logic diagram mein jo operation aakhir mein hoti hai, woh Y ke bilkul paas, right side pe gate hai.",
    "kmap": "K-map Gray code mein hai: zero zero, zero one, one one, one zero. Is misaal ka jawab A bar plus B C hai.",
    "sdlc": "SDLC ke chhe phase ek chakkar mein hain: requirements, design, implementation, testing, deployment, phir maintenance.",
    "waterfall": "Waterfall mein ek phase poora khatam ho, tab agla shuru ho. Wapas upar nahi jaate.",
    "agile": "Agile chhote sprints mein chalta hai. Har sprint ke baad kaam karta hua hissa milta hai.",
    "osi": "OSI ke saat layers hain, neeche se physical, data link, network, transport, session, presentation, application. TCP IP inko char groups mein rakhta hai.",
    "ct-pillars": "Computational thinking ke chaar pillars hain: decomposition, patterns, abstraction, aur algorithm.",
    "algorithm-steps": "Algorithm ka flow start se step, phir decision, phir stop tak hai.",
    "bubble-sort": "Bubble sort padosi numbers compare karta hai. Bara number end ki taraf bubble hota hai.",
    "selection-sort": "Selection sort unsorted hisson mein sab se chhota dhoondh kar aage le aata hai.",
    "search": "Linear search har item check karti hai. Binary search sorted list ko aadha aadha kaat ti hai.",
    "lang-levels": "Upar high-level language hai, jaise Python. Neeche machine code hai, jo computer seedha samajhta hai.",
    "variables": "Variable ek naam wala dabba hai. Naam rehta hai, andar ki value badal sakti hai.",
    "ifelse": "If ek sawal poochta hai. Haan pe ek raasta, na pe doosra. Dono ek saath nahi chalte.",
    "loops": "For tab jab dafa ka pata ho. While tab jab tak condition true rahe.",
    "debug": "Debug ka chakkar: bug dobara lao, line dhoondo, ek cheez theek karo, phir test karo.",
    "keys-table": "Primary key ek row ko pehchanti hai. Foreign key doosri table ki primary key ki taraf ishara karti hai.",
    "er": "ER diagram mein rectangle entity hai, diamond relationship hai, aur oval attribute hai.",
    "access": "Access mein table data rakhti hai, form ek record dikhati hai, query chhanti hai, chart dikhata hai.",
    "ai-iot": "AI faisla karti hai, IoT cheezon ko sense aur connect karti hai, analytics pattern nikalta hai.",
    "assistive": "Assistive technology rukawat hattati hai: screen reader, captions, alag input, aur contrast.",
    "data-types": "Qualitative categories hain, jaise rang ya rae. Quantitative numbers hain, jaise marks ya age.",
    "inquiry": "Inquiry ka raasta: sawal, search, sources, evidence, analysis, phir share.",
    "hci-senses": "HCI insaan aur system ka milaap hai: dekhna, sunna, chhuna, aur harkat.",
    "ui-ux": "UI woh hai jo screen pe nazar aaye. UX yeh hai ke kaam aasani se, bina ghalti, mukammal ho.",
    "wireframe": "Wireframe ek sada sketch hai. Boxes batate hain ke kya kahan hoga. Rang aur final lafz abhi nahi.",
    "trace": "Trace table mein har line ke baad variables ki value likhi hoti hai. Andaza nahi, likha hua hisaab.",
    "bigo": "Big O graph mein O of one seedhi line hai, log dheere chadhhta hai, n seedhi dhal hai, aur n square tez upar jati hai.",
    "array": "Array ek line mein items rakhti hai. Index zero se shuru hota hai, aur seedha usi khane pe pahunchte ho.",
    "structures": "Linked list agle node ki taraf ungli hai. Tree mein ek parent aur kai children. Graph mein koi bhi kisi se jur sakta hai.",
    "stack-queue": "Stack last in first out hai, upar se daalo aur upar se nikalo. Queue first in first out hai, aage se nikalta hai.",
    "py-collections": "List badal sakti hai. Tuple taala laga hota hai. Set mein duplicate nahi. Dictionary key se value nikalta hai.",
    "files": "File mode: r padho, w purani file mita kar likho, a end pe jodo, x nayi file banao.",
    "exceptions": "Try mein risk wala code. Except error pakadta hai. Finally dono sooraton mein chalta hai.",
    "pandas": "DataFrame ek table hai. Khali number NaN likhta hai, matlab value missing hai.",
    "stats": "Mean average hai. Median ordered list ka beech wala number. Mode woh hai jo sab se zyada baar aaye.",
    "neural": "Neural network mein input layer, hidden layers, aur output hota hai. Bahut hidden layers hon to deep learning kehte hain.",
    "security": "Threats malware, phishing, aur denial of service hain. Bachao update, MFA, aur backup se hota hai.",
    "mvp": "Prototype seekhne ke liye hai. MVP sab se chhota asal product hai jo sab se bari assumption ko test kare.",
    "beachhead": "Beachhead pehla chhota market hai jise poora jeet lo, us se pehle ke sab ko bechne ki koshish karo.",
}

MODE_LINE = {
    "teach": "Aaj naya topic hai. Pehle suno, phir band kitab se ek dafa bolo.",
    "checkpoint": "Aaj checkpoint hai. Pehle khud likho, phir notes se milao.",
    "blitz": "Aaj golden blitz hai. Sirf woh points jo paper mein baar baar aate hain.",
    "recap": "Aaj saari chapters ka halka recap hai. Jo atak jaye, usi card pe ruk jao.",
    "mock": "Aaj mock paper hai. Notes band karo, time lo, aur poora paper likho.",
    "mark": "Aaj mock ko mark karo. Jo galat ho, usay repair list mein likh lo.",
    "repair": "Aaj sirf woh topics jo mock mein chhoot gaye. Naya syllabus nahi.",
}


def tex_to_speech(tex: str) -> str:
    text = tex
    text = re.sub(r"\\d?frac\{([^{}]+)\}\{([^{}]+)\}", r"\1 over \2", text)
    text = text.replace(r"\cdot", " dot ")
    text = text.replace(r"\oplus", " xor ")
    text = text.replace(r"\log", " log ")
    text = text.replace(r"\sum", " sum of ")
    text = text.replace(r"\times", " times ")
    text = text.replace(r"\max", " maximum of ")
    text = text.replace(r"\min", " minimum of ")
    text = re.sub(r"\\overline\{([^{}]+)\}", r"\1 ka poora bar", text)
    text = re.sub(r"\\bar\{([^{}]+)\}", r"\1 bar", text)
    text = re.sub(r"(?<=\d)\s*/\s*(?=\d)", " divided by ", text)
    text = re.sub(r"\^\{([^{}]+)\}", r" ki power \1", text)
    text = re.sub(r"\^([A-Za-z0-9]+)", r" ki power \1", text)
    text = text.replace("'", " bar")
    text = text.replace("=", " barabar ")
    text = text.replace("+", " plus ")
    text = re.sub(r"[{}\\]", " ", text)
    text = re.sub(r"\s+", " ", text).strip(" .")
    return text


def strip_math(text: str) -> str:
    def repl(match: re.Match[str]) -> str:
        return " " + tex_to_speech(match.group(1) or match.group(2) or "") + " "

    return re.sub(r"\\\((.*?)\\\)|\\\[(.*?)\\\]", repl, text)


def fix_dots(text: str) -> str:
    parts = [part.strip() for part in re.split(r"\s*·\s*", text) if part.strip()]
    parts = [part for part in parts if re.search(r"[A-Za-z0-9]", part)]
    if len(parts) <= 1:
        return parts[0] if parts else ""
    merged: list[str] = [parts[0]]
    for part in parts[1:]:
        previous = merged[-1]
        previous_words = previous.split()
        part_words = part.split()
        previous_last = previous_words[-1] if previous_words else ""
        join_break = (
            previous_last
            and part_words
            and len(part_words) <= 3
            and part[:1].islower()
            and not previous.endswith((".", "!", "?", ":"))
        )
        if join_break:
            merged[-1] = previous.rstrip() + " " + part
        else:
            merged.append(part)
    if len(merged) == 1:
        return merged[0]
    if all(len(part.split()) <= 6 for part in merged):
        return ", ".join(merged)
    return ". ".join(merged)


def clean(text: str) -> str:
    text = strip_math(text)
    text = re.sub(r"(\d+\s+inputs?)\s*(?:→|->)\s*", r"\1 se ", text, flags=re.I)
    text = text.replace("→", " phir ").replace("⇒", " matlab ")
    text = text.replace("✔", " theek ").replace("✘", " galat ")
    text = text.replace("★", " ")
    text = re.sub(r"\(\s*'\s*\)", " bar ", text)
    text = re.sub(r"(?<=[A-Za-z])\s*/\s*(?=[A-Za-z])", " ya ", text)
    text = fix_dots(text)
    text = text.replace("arbons", "arabon")
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\s+([,.;:!?])", r"\1", text)
    text = re.sub(r"\(\s*\)", "", text)
    text = re.sub(r"\s+:", ":", text)
    text = text.replace("==", " barabar barabar ")
    text = re.sub(r"(?<![=\w])=(?!=)", " matlab ", text)
    if text.strip() in {"+", "−", "-"}:
        text = "plus" if text.strip() == "+" else "minus"
    if text.strip() == "*":
        text = "times"
    if text.strip() == "//":
        text = "double slash"
    if text.strip() == "%":
        text = "modulus"
    if text.strip() == "**":
        text = "power"
    text = text.replace("//", " double slash ")
    return text.strip(" ,;|")


def is_noise(text: str) -> bool:
    token = text.strip(" .,:;|()[]")
    if len(token) <= 1:
        return True
    if NOISE.match(token):
        return True
    words = [word.strip(".,:;()[]") for word in token.split() if word.strip(".,:;()[]")]
    if not words:
        return True
    if len(words) <= 5 and all(NOISE.match(word) or len(word) <= 1 for word in words):
        return True
    return False


def ensure_period(text: str) -> str:
    text = text.strip()
    if not text:
        return ""
    if text[-1] not in ".!?":
        text += "."
    return text


def without_lead(text: str, lead: str) -> str:
    pattern = re.compile(rf"^{re.escape(lead)}\s*:?\s*", re.I)
    return pattern.sub("", text).strip()


def speak_block(block: dict) -> list[str]:
    kind = block.get("type", "p")
    if kind == "table":
        headers = [clean(cell) for cell in block.get("headers") or []]
        headers = [cell for cell in headers if cell and not is_noise(cell)]
        lines: list[str] = []
        if headers:
            lines.append("Table yaad karo. Columns hain: " + ", ".join(headers) + ".")
        for row in block.get("rows") or []:
            cells = [clean(cell) for cell in row]
            cells = [cell for cell in cells if cell and not re.fullmatch(r"[01]", cell)]
            if not cells:
                continue
            if len(cells) == 1:
                lines.append(ensure_period(cells[0]))
            else:
                lines.append(ensure_period(cells[0] + ". " + ". ".join(cells[1:])))
        return lines
    if kind == "code":
        raw = block.get("text") or ""
        spoken = clean(raw.replace("\n", ". "))
        if not spoken or is_noise(spoken):
            return []
        return ["Code example. " + ensure_period(spoken)]
    text = clean(block.get("text") or "")
    if not text or is_noise(text):
        return []
    if kind == "def":
        text = "Paper ki definition, yehi lafz likhna. " + without_lead(text, "Def")
    elif kind == "tip":
        text = "Yaad rakho. " + without_lead(without_lead(text, "Yaad rakho"), "Yaad rakhne ka tarika")
    elif kind == "exam":
        text = "Paper mein aise poochte hain. " + without_lead(without_lead(text, "Paper mein"), "Paper mein")
    elif kind == "warn":
        text = "Dhoka mat khana. " + without_lead(without_lead(text, "Dhoka"), "Dhoka mat khana")
    elif kind == "answer":
        text = "Jawab. " + without_lead(text, "Jawab")
    return [ensure_period(text)]


LABEL_WORDS = {
    "define", "explain", "example", "diagram", "working", "matlab",
    "output", "input", "rule", "operation", "nature", "feature",
}

PHRASES = (
    ("where n is the number of inputs", "jahan n inputs ki tadaad hai"),
    ("1 only at 11", "output 1 sirf tab aata hai jab dono inputs 1 hon"),
    ("0 only at 11", "output 0 sirf tab aata hai jab dono inputs 1 hon"),
    ("1 only at 00", "output 1 sirf tab aata hai jab dono inputs 0 hon"),
    ("0 only at 00", "output 0 sirf tab aata hai jab dono inputs 0 hon"),
    ("flips the single input", "ek input ko ulta kar deta hai"),
    ("Only-1 or only-0 row", "khaas row"),
    ("true division", "asli division"),
    ("floor division", "neeche wali division, decimal gira do"),
    ("From fastest to slowest as n grows", "jaise jaise n barhta hai, tez se dheemi growth yeh hai"),
    ("As n doubles", "jab n double ho"),
)


CONTINUATION = re.compile(
    r"^(?:hai|hain|ho|tha|thi|the|raha|rahi|rahe|kar|karta|karti|karte|se|ka|ki|ke|mein|par|pe|aur|ya|nahi|nahin|bhi)\b",
    re.I,
)


def stitch(parts: list[str]) -> list[str]:
    stitched: list[str] = []
    for part in parts:
        part = part.strip()
        if not part:
            continue
        if not stitched:
            stitched.append(part)
            continue
        previous = stitched[-1].rstrip()
        label = previous.rstrip(".:").lower()
        previous_words = previous.rstrip(".!?").split()
        unfinished = not previous.endswith((".", "!", "?")) or len(previous_words) <= 4
        if label in LABEL_WORDS or (part[:1].islower() and (unfinished or CONTINUATION.match(part))):
            joiner = " " if part[:1].islower() else ": "
            body = part[0].lower() + part[1:] if label in LABEL_WORDS and part[:1].isupper() else part
            stitched[-1] = previous.rstrip(".") + joiner + body
        else:
            stitched.append(part)
    return stitched


def polish(text: str) -> str:
    for old, new in PHRASES:
        text = re.sub(old, new, text, flags=re.I)
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\s+([,.;:!?])", r"\1", text)
    text = text.replace(":.", ".")
    text = text.replace("..", ".")
    text = re.sub(r"\bRow\s+\d+\.?", "", text)
    text = re.sub(r"\bphir\s*\.", ".", text)
    text = re.sub(r"(?<![A-Za-z])\b\d{1,2},\s+(?=[A-Z])", "", text)
    text = re.sub(r"\b\d+\s+kahin bhi khare ho\.?", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    sentences = re.split(r"(?<=[.!?])\s+", text)
    text = " ".join(sentence[:1].upper() + sentence[1:] if sentence else sentence for sentence in sentences)
    return text


def narrate_card(card: dict) -> str:
    parts: list[str] = []
    title = (card.get("title") or "").strip()
    if title and title.lower() not in {"notes", "note"}:
        lead = title.rstrip(".")
        if card.get("golden"):
            lead += ". Yeh golden point hai, paper mein aksar aata hai"
        parts.append(ensure_period(lead))
    for block in card.get("blocks") or []:
        parts.extend(speak_block(block))
    diagram = card.get("diagram")
    if diagram and diagram in DIAGRAM_LINE:
        parts.append(ensure_period(DIAGRAM_LINE[diagram]))
    return polish(" ".join(stitch(parts)))


def narrate_page(page: dict) -> str:
    day = str(int(page.get("day") or "0"))
    title = clean(page.get("title") or "")
    chapter = clean(page.get("chapter") or "")
    mode = MODE_LINE.get(page.get("mode") or "", "Aaj ka hissa suno.")
    bits = [f"Day {day}.", ensure_period(title)]
    if chapter:
        bits.append(ensure_period(chapter))
    bits.append(ensure_period(mode))
    must = clean(page.get("mustLock") or "")
    if must and not is_noise(must):
        bits.append("Aaj ka must lock: " + ensure_period(must))
    subtitle = clean(page.get("subtitle") or "")
    if subtitle and len(subtitle) > 12:
        bits.append("Is din ke hisse: " + ensure_period(subtitle))
    return " ".join(bits)


def main() -> None:
    for name in ("xi.json", "xii.json"):
        path = CONTENT / name
        book = json.loads(path.read_text(encoding="utf-8"))
        spoken = 0
        for page in book["pages"]:
            page["narration"] = narrate_page(page)
            for card in page["cards"]:
                card["narration"] = narrate_card(card)
                spoken += 1
        path.write_text(json.dumps(book, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
        print(f"{name}: narrated {spoken} cards, {path.stat().st_size} bytes")


if __name__ == "__main__":
    main()
