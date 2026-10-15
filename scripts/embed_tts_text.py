#!/usr/bin/env python3
"""Embed Urdu descriptive tutor text with English exam terms for TTS.

Writes app/src/main/assets/course/tts.json. Each page is one spoken script:
Urdu explains the booklet; exam terminology stays inside {braces} so the
narrator speaks those words in English, as printed.

Day scripts in course.json already follow the same brace convention.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import pymupdf

ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "app/src/main/assets/course/crash-course.pdf"
OUT = ROOT / "app/src/main/assets/course/tts.json"

ARABIC = re.compile(r"[\u0600-\u06FF\uFB50-\uFDFF\uFE70-\uFEFF]")
PRIVATE = re.compile(r"[\ue000-\uf8ff\u200b-\u200f\u202a-\u202e\ufffd]")
LATIN_WORD = re.compile(r"[A-Za-z][A-Za-z0-9'+.-]*")
TOKEN = re.compile(
    r"\{[^{}]+\}|⟪[^⟫]*⟫|[A-Za-z]+(?:'[A-Za-z]+)?|[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF]+|\d+(?:\.\d+)?|[^\s]"
)

# Exam terms spoken in English. Multi-word phrases are matched first.
ALWAYS = [
    "computer science", "class xi", "class xii", "teach yourself", "crash course",
    "new sindh curriculum", "boolean algebra", "boolean expression", "logic gate",
    "logic gates", "logic diagram", "logic diagrams", "truth table", "truth tables",
    "karnaugh map", "karnaugh maps", "gray code", "universal gate", "universal gates",
    "digital system", "digital systems", "analog signal", "analog signals",
    "digital signal", "digital signals", "sine wave", "square wave",
    "waterfall model", "agile model", "osi model", "osi layer", "osi layers",
    "primary key", "foreign key", "candidate key", "composite key", "entity relationship",
    "er model", "data type", "data types", "visual studio", "vs code", "big o notation",
    "big o", "binary search", "linear search", "bubble sort", "selection sort",
    "insertion sort", "neural network", "neural networks", "deep learning",
    "machine learning", "artificial intelligence", "standard deviation", "control structure",
    "trace table", "flow chart", "operating system", "ip address", "de morgan",
    "number system", "number systems", "conditional statement", "linked list",
    "closed-book drill", "closed book", "smart farming", "smart home", "smart grid",
    "descriptive analytics", "predictive analytics", "natural language",
    "black box", "white box", "use case", "data flow", "normal form",
    "mean absolute", "box plot", "bar chart", "pie chart", "line chart", "scatter plot",
    "primary memory", "secondary memory", "system software", "application software",
    "logic bomb", "social engineering", "two factor", "access control",
    "stack overflow", "syntax error", "runtime error", "logical error",
    "while loop", "for loop", "if else", "if-else", "else if",
    "algorithm", "algorithms", "pseudocode", "flowchart", "binary", "bit", "bits",
    "byte", "boolean", "nand", "nor", "xor", "xnor", "inverter", "logisim", "sdlc",
    "waterfall", "agile", "sprint", "sprints", "osi", "tcp", "udp", "icmp", "http",
    "https", "iot", "sensor", "sensors", "actuator", "actuators", "database", "dbms",
    "sql", "python", "variable", "variables", "tuple", "syntax", "debugging", "hci",
    "usability", "prototype", "prototypes", "wireframe", "figma", "median", "variance",
    "neuron", "mvp", "equity", "beachhead", "phishing", "authentication", "encryption",
    "malware", "firewall", "pandas", "numpy", "dataframe", "analytics", "encapsulation",
    "protocol", "protocols", "schema", "query", "queries", "operand", "operands",
    "minterm", "minterms", "maxterm", "maxterms", "karnaugh", "recursion", "iteration",
    "bandwidth", "latency", "router", "ethernet", "bluetooth", "zigbee", "cloud",
    "api", "json", "csv", "compiler", "interpreter", "pixel", "checksum", "subnet",
    "ransomware", "accessibility", "outlier", "outliers", "quartile", "histogram",
    "discrete", "continuous", "analog", "digital", "input", "inputs", "output",
    "outputs", "data", "network", "networks", "layer", "layers", "function",
    "functions", "model", "models", "protocol", "bit", "loop", "loops", "array",
    "stack", "queue", "schema", "field", "fields", "record", "records", "query",
    "table", "tables", "form", "forms", "key", "keys", "set", "list", "lists",
    "dictionary", "class", "object", "string", "integer", "float", "mode", "mean",
    "range", "node", "nodes", "edge", "edges", "graph", "tree", "hash", "index",
    "pointer", "token", "server", "client", "packet", "frame", "header", "payload",
    "session", "cookie", "cache", "backup", "virus", "worm", "trojan", "cipher",
    "plaintext", "ciphertext", "biometric", "password", "username", "login",
    "dataset", "datasets", "outlier", "correlation", "regression", "sampling",
    "population", "frequency", "percentage", "probability", "matrix", "vector",
    "pixel", "resolution", "interface", "layout", "widget", "button", "navigation",
    "affordance", "feedback", "heuristic", "persona", "sprint", "backlog", "scrum",
    "kanban", "deploy", "deployment", "maintenance", "requirement", "requirements",
    "testing", "debug", "compiler", "ide", "module", "library", "package", "import",
    "return", "parameter", "argument", "boolean", "operand", "operator", "operators",
    "expression", "statement", "indentation", "comment", "comments", "exception",
    "file", "files", "directory", "path", "string", "integer", "float", "boolean",
    "none", "true", "false", "null", "ascii", "unicode", "bit", "nibble",
    "overflow", "underflow", "rounding", "precision", "accuracy", "normalization",
    "denormalization", "cardinality", "modality", "attribute", "attributes",
    "entity", "entities", "relationship", "relationships", "tuple", "domain",
    "constraint", "constraints", "integrity", "redundancy", "anomaly", "join",
    "select", "project", "union", "intersection", "difference", "view", "index",
    "transaction", "commit", "rollback", "deadlock", "concurrency", "acid",
    "oltp", "olap", "etl", "api", "rest", "crud", "gui", "cli", "os", "ram", "rom",
    "cpu", "alu", "cu", "cache", "register", "bus", "port", "usb", "hdmi", "lan",
    "wan", "man", "pan", "isp", "dns", "dhcp", "nat", "vpn", "ssid", "ip", "mac",
    "osi", "pdu", "mtu", "qos", "voip", "smtp", "pop", "imap", "ftp", "ssh", "tls",
    "ssl", "html", "css", "url", "uri", "http", "browser", "cookie", "firewall",
    "malware", "phishing", "spam", "ddos", "dos", "vpn", "encryption", "decryption",
    "hashing", "checksum", "parity", "raid", "bios", "firmware", "kernel", "shell",
    "process", "thread", "scheduler", "deadlock", "paging", "segmentation",
    "virtual memory", "cloud computing", "edge computing", "iot", "sensor",
    "actuator", "microcontroller", "arduino", "raspberry", "protocol", "mqtt",
    "lora", "nb-iot", "zigbee", "bluetooth", "wifi", "rfid", "nfc", "gps",
    "algorithm", "heuristic", "complexity", "notation", "logarithm", "factorial",
    "recursion", "iteration", "sorting", "searching", "traversal", "bfs", "dfs",
    "stack", "queue", "deque", "priority queue", "linked list", "array", "tree",
    "binary tree", "heap", "graph", "vertex", "adjacency", "matrix", "list",
    "hash table", "collision", "bucket", "python", "interpreter", "indentation",
    "variable", "identifier", "keyword", "literal", "operator", "operand",
    "expression", "statement", "block", "suite", "slice", "mutable", "immutable",
    "tuple", "dictionary", "comprehension", "function", "parameter", "argument",
    "return", "scope", "namespace", "module", "package", "library", "exception",
    "traceback", "syntax", "semantics", "debugging", "breakpoint", "dry run",
    "trace table", "pseudocode", "flowchart", "hci", "usability", "accessibility",
    "prototype", "wireframe", "mockup", "persona", "affordance", "feedback",
    "cognitive", "ergonomics", "typography", "contrast", "navigation", "layout",
    "widget", "modal", "tooltip", "breadcrumb", "responsive", "figma", "sus",
    "nps", "analytics", "dataset", "outlier", "quartile", "percentile", "variance",
    "deviation", "histogram", "skewness", "correlation", "causation", "sampling",
    "population", "census", "bias", "validity", "reliability", "qualitative",
    "quantitative", "nominal", "ordinal", "interval", "ratio", "mean", "median",
    "mode", "range", "iqr", "pandas", "dataframe", "numpy", "matplotlib", "csv",
    "json", "sql", "query", "schema", "normalization", "neuron", "synapse",
    "weight", "bias", "activation", "epoch", "batch", "overfitting", "underfitting",
    "training", "inference", "label", "feature", "classification", "regression",
    "clustering", "supervised", "unsupervised", "reinforcement", "accuracy",
    "precision", "recall", "threshold", "token", "embedding", "prompt", "llm",
    "chatbot", "mvp", "equity", "beachhead", "pivot", "prototype", "stakeholder",
    "revenue", "customer", "segment", "value proposition", "business model",
    "phishing", "authentication", "authorization", "authorisation", "encryption",
    "malware", "firewall", "ransomware", "biometric", "password", "ciphertext",
    "plaintext", "cipher", "keylogger", "spyware", "adware", "trojan", "worm",
    "virus", "vpn", "ssl", "tls", "hash", "salt", "otp", "mfa", "2fa",
]
# De-duplicate while keeping longer phrases first.
ALWAYS = sorted(set(ALWAYS), key=lambda s: (-len(s), s))
ALWAYS_SET = {t.lower() for t in ALWAYS}
TERM_RE = re.compile(r"\b(" + "|".join(re.escape(t) for t in ALWAYS) + r")\b", re.I)

CAPS = {
    "AND", "OR", "NOT", "XOR", "XNOR", "NAND", "NOR", "TRUE", "FALSE", "HIGH", "LOW",
    "ON", "OFF", "BOTH", "EITHER", "ANY", "ALL", "SAME", "TCP", "UDP", "OSI", "SQL",
    "HTML", "CSS", "API", "URL", "RAM", "ROM", "CPU", "LAN", "WAN", "VPN", "HTTP",
    "HTTPS", "FTP", "SSH", "DNS", "DHCP", "IOT", "MVP", "HCI", "SDLC", "IDE", "GUI",
    "CLI", "CSV", "JSON", "ASCII", "USB", "HDMI", "MAC", "BIOS", "RAID", "QOS",
    "SMTP", "IMAP", "RFID", "NFC", "GPS", "BFS", "DFS", "IQR", "NPS", "SUS", "OTP",
    "MFA", "LLM", "ETL", "CRUD", "ACID", "OLTP", "OLAP", "MQTT", "SSID", "NAT",
    "ISP", "PAN", "MAN", "ALU", "PDU", "MTU", "VOIP", "POP", "TLS", "SSL", "URI",
    "DDOS", "DOS", "AI", "ML", "DL", "OS", "IP", "ID", "ER", "DB", "PK", "FK",
}

GLOSS = {
    "discrete": "منفرد، گنتی کے قابل",
    "continuous": "مسلسل، کسی حد میں کوئی بھی قدر",
    "analog": "ہموار لہر، شور سے متاثر",
    "digital": "صرف دو سطحیں، 0 اور 1",
    "bit": "ایک 0 یا 1",
    "bits": "0 اور 1 کے ہندسے",
    "signal": "سگنل، لہر",
    "boolean algebra": "صرف سچ اور جھوٹ کی الجبرا",
    "logic gate": "منطق کا سرکٹ",
    "logic gates": "منطق کے سرکٹ",
    "truth table": "ہر input کا output جدول",
    "inverter": "الٹ دینے والا گیٹ",
    "universal gate": "جس سے ہر گیٹ بنے",
    "algorithm": "قدم بہ قدم حل",
    "pseudocode": "عام زبان میں لکھے ہوئے قدم",
    "flowchart": "تیروں والا خاکہ",
    "variable": "نام والی قدر",
    "variables": "نام والی قدریں",
    "loop": "دہرایا جانے والا بلاک",
    "function": "نام والا کام",
    "database": "منظم ڈیٹا کا ذخیرہ",
    "dbms": "ڈیٹا بیس کا سافٹ ویئر",
    "primary key": "ہر قطار کی منفرد شناخت",
    "foreign key": "دوسری جدول کی کلید",
    "schema": "ڈیٹا کی ساخت",
    "query": "ڈیٹا کا سوال",
    "sdlc": "سافٹ ویئر بنانے کا چکر",
    "waterfall": "ایک طرف بہنے والا ماڈل",
    "agile": "چھوٹے چکر میں بنانا",
    "sprint": "دو سے چار ہفتے کا کام",
    "osi": "نیٹ ورک کی سات تہیں",
    "tcp": "بھروسہ مند ترسیل",
    "udp": "تیز مگر بغیر ضمانت",
    "iot": "جڑی ہوئی چیزیں",
    "sensor": "ماحول ناپنے والا آلہ",
    "actuator": "حکم پر کام کرنے والا آلہ",
    "hci": "انسان اور کمپیوٹر کا میل",
    "usability": "استعمال میں آسانی",
    "prototype": "جانچنے والا ابتدائی نمونہ",
    "wireframe": "سکرین کا خاکہ",
    "mvp": "کم سے کم قابل فروخت مصنوع",
    "equity": "حصص میں ملکیت",
    "beachhead": "پہلی چھوٹی منڈی",
    "neuron": "مصنوعی اعصابی خلیہ",
    "neural network": "نیورون کا جال",
    "encryption": "پیغام کو چھپانا",
    "authentication": "شناخت ثابت کرنا",
    "phishing": "جعلی پیغام سے چوری",
    "malware": "نقصان دہ سافٹ ویئر",
    "firewall": "نیٹ ورک کی دیوار",
    "mean": "اوسط",
    "median": "درمیانی قدر",
    "mode": "سب سے زیادہ آنے والی قدر",
    "range": "بڑی اور چھوٹی قدر کا فرق",
    "variance": "پھیلاؤ کا ناپ",
    "outlier": "باقی ڈیٹا سے الگ قدر",
    "data": "ڈیٹا، معلومات",
    "input": "اندر جانے والی قدر",
    "output": "باہر آنے والی قدر",
    "model": "کام کا نمونہ",
    "layer": "تہہ",
    "network": "جڑے ہوئے آلات",
    "protocol": "بات چیت کا قاعدہ",
    "stack": "آخر میں رکھا، پہلے نکلا",
    "queue": "پہلے رکھا، پہلے نکلا",
    "array": "لگے خانوں کی فہرست",
    "python": "پروگرامنگ کی زبان",
    "sql": "ڈیٹا بیس کی زبان",
    "pandas": "ڈیٹا کا پائتھن ٹول",
    "list": "ترتیب والی فہرست",
    "tuple": "ناقابل تبدیلی فہرست",
    "dictionary": "کلید اور قدر کے جوڑے",
    "set": "بغیر دہرائی کا مجموعہ",
    "string": "حروف کی قطار",
    "class": "اشیاء کا سانچہ",
    "object": "کلاس کی ایک مثال",
    "file": "محفوظ شدہ دستاویز",
    "testing": "درستگی کی جانچ",
    "debugging": "غلطی ڈھونڈنا",
    "syntax": "لکھنے کے قواعد",
    "operator": "عمل کی علامت",
    "expression": "قدر بنانے والا فقرہ",
    "iteration": "دہرانا",
    "recursion": "فنکشن کا خود کو بلانا",
    "bandwidth": "ڈیٹا کی گنجائش",
    "latency": "جواب میں تاخیر",
    "encryption": "خفیہ کاری",
    "password": "خفیہ لفظ",
    "cloud": "دور کا سرور",
    "interface": "استعمال کی سطح",
    "feedback": "جوابی ردِ عمل",
    "bias": "جھکاؤ",
    "accuracy": "درستگی",
    "training": "ماڈل کو سکھانا",
    "feature": "خصوصیت",
    "label": "نشان",
    "prompt": "ماڈل کو دیا گیا حکم",
    "regression": "عدد کی پیش گوئی",
    "classification": "قسم میں رکھنا",
    "normalization": "دہرائی ختم کرنا",
    "entity": "حقیقی چیز جس کا ریکارڈ ہو",
    "attribute": "خاصیت",
    "relationship": "دو چیزوں کا تعلق",
    "integrity": "ڈیٹا کا درست رہنا",
    "redundancy": "بے کار دہرائی",
    "transaction": "ایک مکمل کام",
    "index": "تیز تلاش کی فہرست",
    "view": "محفوظ شدہ سوال",
    "join": "دو جدول ملانا",
    "constraint": "پابندی",
    "domain": "جائز قدروں کا دائرہ",
    "cardinality": "تعلق کی گنتی",
    "anomaly": "تازہ کاری کی خرابی",
    "compiler": "پوری زبان کا ترجمہ",
    "interpreter": "سطر بہ سطر چلانا",
    "module": "الگ فائل کا کوڈ",
    "library": "تیار فنکشنز",
    "parameter": "فنکشن کا نام والا خانہ",
    "argument": "فنکشن کو دی گئی قدر",
    "exception": "چلتے وقت کی خرابی",
    "comment": "نوٹ جو چلتا نہیں",
    "indentation": "حاشیے کا فاصلہ",
    "mutable": "بدلنے کے قابل",
    "immutable": "بدل نہ سکنے والا",
    "scope": "نام کہاں تک نظر آئے",
    "keyword": "زبان کا محفوظ لفظ",
    "identifier": "نام",
    "literal": "لکھی ہوئی قدر",
    "slice": "فہرست کا ٹکڑا",
    "comprehension": "مختصر فہرست بنانا",
    "breakpoint": "رک جانے کی جگہ",
    "heuristic": "تجربے کا طریقہ",
    "complexity": "وقت یا جگہ کا ناپ",
    "sorting": "ترتیب دینا",
    "searching": "تلاش",
    "traversal": "ہر نوڈ پر جانا",
    "vertex": "گراف کا نقطہ",
    "heap": "ترتیب والا درخت",
    "collision": "ایک ہی خانے میں دو چیزیں",
    "persona": "فرضی صارف",
    "affordance": "دیکھ کر سمجھ آنے والا استعمال",
    "typography": "حروف کی ترتیب",
    "contrast": "رنگوں کا فرق",
    "mockup": "نظر آنے والا نمونہ",
    "responsive": "ہر سکرین پر درست",
    "ergonomics": "جسم کے مطابق ڈیزائن",
    "qualitative": "الفاظ والی معلومات",
    "quantitative": "اعداد والی معلومات",
    "nominal": "صرف نام والی قسم",
    "ordinal": "ترتیب والی قسم",
    "census": "سب کی گنتی",
    "sampling": "نمونہ لینا",
    "population": "پورا گروہ",
    "validity": "صحیح چیز ناپنا",
    "reliability": "بار بار وہی نتیجہ",
    "skewness": "ترچھا پھیلاؤ",
    "correlation": "ساتھ چلنے والا رشتہ",
    "causation": "سبب اور اثر",
    "percentile": "سو میں مقام",
    "histogram": "بندھے ہوئے خانوں کا چارٹ",
    "synapse": "نیورون کا جوڑ",
    "weight": "اثر کی مقدار",
    "epoch": "پورا ڈیٹا ایک بار",
    "overfitting": "یاد کر لینا، سمجھ نہ پانا",
    "underfitting": "سیکھ ہی نہ پانا",
    "inference": "سے جواب نکالنا",
    "clustering": "مشابہ گروہ بنانا",
    "supervised": "جواب کے ساتھ سیکھنا",
    "unsupervised": "بغیر جواب کے سیکھنا",
    "reinforcement": "انعام سے سیکھنا",
    "precision": "صحیح پکڑ کی شرح",
    "recall": "چھوٹے ہوئے صحیح کی شرح",
    "threshold": "فیصلے کی حد",
    "embedding": "معنی کا عددی نقشہ",
    "pivot": "راستہ بدلنا",
    "stakeholder": "جس کا مفاد ہو",
    "revenue": "آمدنی",
    "segment": "صارفوں کا ٹکڑا",
    "authorization": "اجازت",
    "authorisation": "اجازت",
    "decryption": "چھپا پیغام کھولنا",
    "ciphertext": "چھپا متن",
    "plaintext": "کھلا متن",
    "hashing": "ایک طرف کا نقش",
    "salt": "پاس ورڈ کے ساتھ اضافی راز",
    "spyware": "چھپ کر دیکھنے والا سافٹ ویئر",
    "adware": "اشتہاری سافٹ ویئر",
    "keylogger": "دبی ہوئی کلیدیں چرانے والا",
    "biometric": "جسم کی شناخت",
    "firmware": "آلہ کے اندر کا سافٹ ویئر",
    "kernel": "آپریٹنگ سسٹم کا مرکز",
    "process": "چلتا ہوا پروگرام",
    "thread": "کام کی پتلی دھاگہ",
    "paging": "میموری کے ٹکڑے",
    "cache": "تیز عارضی حافظہ",
    "register": "سی پی یو کا چھوٹا خانہ",
    "packet": "ڈیٹا کا لفافہ",
    "router": "راستہ چننے والا آلہ",
    "bandwidth": "گنجائش",
    "latency": "تاخیر",
    "checksum": "جمع کی جانچ",
    "parity": "جفت یا طاق جانچ",
    "cookie": "براؤزر کی یاد",
    "backup": "محفوظ نقل",
    "deployment": "صارف تک پہنچانا",
    "maintenance": "بننے کے بعد سنبھال",
    "requirement": "ضرورت",
    "sprint": "مختصر کام کا چکر",
    "backlog": "باقی کام کی فہرست",
    "normalization": "جدول سے دہرائی ہٹانا",
    "cardinality": "کتنے کا تعلق",
    "modality": "لازمی یا اختیاری",
    "anomaly": "اپ ڈیٹ کی خرابی",
    "redundancy": "دہرائی",
    "integrity": "درست رہنا",
    "transaction": "پورا یا کچھ نہیں",
    "deadlock": "آپس میں پھنس جانا",
    "concurrency": "ایک ساتھ چلنا",
    "index": "تیز تلاش",
    "join": "جدول ملانا",
    "constraint": "قاعدے کی پابندی",
    "domain": "جائز قدریں",
    "attribute": "کالم کی خاصیت",
    "entity": "ریکارڈ کی اصل چیز",
    "relationship": "تعلق",
    "tuple": "ایک قطار",
    "schema": "ساخت",
    "query": "سوال",
    "select": "چننا",
    "view": "دکھائی",
    "file": "فائل",
    "path": "راستہ",
    "directory": "فولڈر",
    "module": "ماڈیول",
    "package": "پیکج",
    "library": "لائبریری",
    "import": "لانا",
    "return": "واپس دینا",
    "parameter": "پیرامیٹر",
    "argument": "دلیل",
    "exception": "رن ٹائم خرابی",
    "comment": "تبصرہ",
    "indentation": "حاشیہ",
    "mutable": "قابلِ تبدیلی",
    "immutable": "مستقل",
    "scope": "دائرہ",
    "namespace": "ناموں کی جگہ",
    "keyword": "کی ورڈ",
    "identifier": "شناختی نام",
    "literal": "لتریل",
    "slice": "سلائس",
    "breakpoint": "بریک پوائنٹ",
    "traceback": "خرابی کا نشان",
    "syntax": "نحو",
    "semantics": "معنی",
    "operator": "آپریٹر",
    "operand": "آپرینڈ",
    "expression": "ایکسپریشن",
    "statement": "سٹیٹمنٹ",
    "block": "بلاک",
    "boolean": "بولین",
    "integer": "عدد",
    "float": "اعشاری",
    "string": "سٹرنگ",
    "none": "خالی قدر",
    "null": "غیر موجود",
    "true": "سچ",
    "false": "جھوٹ",
    "list": "لسٹ",
    "dictionary": "ڈکشنری",
    "set": "سیٹ",
    "class": "کلاس",
    "object": "آبجیکٹ",
    "array": "ایرے",
    "stack": "اسٹیک",
    "queue": "قطار",
    "tree": "درخت",
    "graph": "گراف",
    "node": "نوڈ",
    "edge": "کنارہ",
    "pointer": "پوائنٹر",
    "index": "انڈیکس",
    "hash": "ہیش",
    "heap": "ہیپ",
    "vertex": "ورٹیکس",
    "matrix": "میٹرکس",
    "vector": "ویکٹر",
    "pixel": "پکسل",
    "interface": "انٹرفیس",
    "layout": "لے آؤٹ",
    "widget": "وجٹ",
    "button": "بٹن",
    "navigation": "نیویگیشن",
    "feedback": "فیڈبیک",
    "persona": "پرسانا",
    "contrast": "کنٹراسٹ",
    "prototype": "پروٹوٹائپ",
    "wireframe": "وائر فریم",
    "figma": "فگما",
    "usability": "یوزیبلٹی",
    "accessibility": "رسائی",
    "analytics": "تجزیہ",
    "dataset": "ڈیٹا سیٹ",
    "outlier": "آؤٹ لائر",
    "quartile": "کوارٹائل",
    "variance": "ویرینس",
    "histogram": "ہسٹوگرام",
    "frequency": "فریکوئنسی",
    "percentage": "فیصد",
    "probability": "امکان",
    "sampling": "سیمپلنگ",
    "population": "آبادی",
    "bias": "بایس",
    "validity": "ویلیڈیٹی",
    "reliability": "رلائبلٹی",
    "qualitative": "کوالیٹیٹو",
    "quantitative": "کوانٹیٹیٹو",
    "neuron": "نیورون",
    "activation": "ایکٹیویشن",
    "epoch": "ایپوک",
    "overfitting": "اوور فٹنگ",
    "training": "ٹریننگ",
    "inference": "انفرنس",
    "classification": "درجہ بندی",
    "regression": "ریگریشن",
    "clustering": "کلسٹرنگ",
    "accuracy": "ایکیوریسی",
    "precision": "پریسیژن",
    "recall": "ریکال",
    "threshold": "تھریشولڈ",
    "prompt": "پرامپٹ",
    "chatbot": "چیٹ بوٹ",
    "mvp": "ایم وی پی",
    "equity": "ایکویٹی",
    "beachhead": "بیچ ہیڈ",
    "phishing": "فشنگ",
    "authentication": "تصدیق",
    "encryption": "انکرپشن",
    "malware": "مالویئر",
    "firewall": "فائر وال",
    "ransomware": "رینسم ویئر",
    "password": "پاس ورڈ",
    "biometric": "بایومیٹرک",
    "cloud": "کلاؤڈ",
    "server": "سرور",
    "client": "کلائنٹ",
    "packet": "پیکٹ",
    "router": "راؤٹر",
    "bandwidth": "بینڈوڈتھ",
    "latency": "لیٹنسی",
    "protocol": "پروٹوکول",
    "session": "سیشن",
    "cache": "کیشے",
    "backup": "بیک اپ",
    "cookie": "کوکی",
    "browser": "براؤزر",
    "url": "یو آر ایل",
    "ip": "آئی پی",
    "dns": "ڈی این ایس",
    "vpn": "وی پی این",
    "lan": "لان",
    "wan": "وان",
    "cpu": "سی پی یو",
    "ram": "ریم",
    "rom": "روم",
    "bus": "بس",
    "port": "پورٹ",
    "kernel": "کرنل",
    "process": "پراسیس",
    "thread": "تھریڈ",
    "firmware": "فرم ویئر",
    "compiler": "کمپائلر",
    "interpreter": "انٹرپریٹر",
    "ide": "آئی ڈی ای",
    "module": "ماڈیول",
    "library": "لائبریری",
    "package": "پیکج",
    "debug": "ڈیبگ",
    "testing": "ٹیسٹنگ",
    "deployment": "ڈپلائمنٹ",
    "maintenance": "مینٹیننس",
    "requirement": "ریکوائرمنٹ",
    "requirements": "ضروریات",
    "sprint": "سپرنٹ",
    "backlog": "بیک لاگ",
    "agile": "ایجائل",
    "waterfall": "واٹر فال",
    "sdlc": "ایس ڈی ایل سی",
    "osi": "او ایس آئی",
    "tcp": "ٹی سی پی",
    "udp": "یو ڈی پی",
    "icmp": "آئی سی ایم پی",
    "http": "ایچ ٹی ٹی پی",
    "iot": "آئی او ٹی",
    "sensor": "سینسر",
    "actuator": "ایکچوایٹر",
    "hci": "ایچ سی آئی",
    "python": "پائتھن",
    "sql": "ایس کیو ایل",
    "pandas": "پانڈاز",
    "numpy": "نمپائی",
    "dataframe": "ڈیٹا فریم",
    "json": "جے سن",
    "csv": "سی ایس وی",
    "api": "اے پی آئی",
    "html": "ایچ ٹی ایم ایل",
    "css": "سی ایس ایس",
    "recursion": "ریکرژن",
    "iteration": "دہرانا",
    "pseudocode": "سوڈو کوڈ",
    "flowchart": "فلو چارٹ",
    "algorithm": "الگورتھم",
    "algorithms": "الگورتھم",
    "boolean": "بولین",
    "inverter": "انورٹر",
    "karnaugh": "کارنو",
    "minterm": "من ٹرم",
    "maxterm": "میکس ٹرم",
    "logisim": "لاجی سم",
    "encapsulation": "انکیپسولیشن",
    "normalization": "نارملائزیشن",
    "cardinality": "کارڈینیلٹی",
    "integrity": "انٹیگریٹی",
    "redundancy": "ریڈنڈنسی",
    "anomaly": "اینوملی",
    "transaction": "ٹرانزیکشن",
    "deadlock": "ڈیڈ لاک",
    "concurrency": "ہم وقتی",
    "schema": "اسکیما",
    "entity": "اینٹیٹی",
    "attribute": "ایٹریبیوٹ",
    "constraint": "کنسٹرینٹ",
    "domain": "ڈومین",
    "tuple": "ٹیوپل",
    "variable": "ویری ایبل",
    "syntax": "سنٹیکس",
    "debugging": "ڈیبگنگ",
    "operand": "آپرینڈ",
    "operands": "آپرینڈ",
    "operator": "آپریٹر",
    "operators": "آپریٹر",
    "expression": "ایکسپریشن",
    "bitwise": "بٹ وار",
    "membership": "رکنیت",
    "relational": "تقابلی",
    "arithmetic": "حسابی",
    "assignment": "تفویض",
    "logical": "منطقی",
    "precedence": "ترجیح",
    "associativity": "جوڑ کی سمت",
    "short-circuit": "جلدی رک جانا",
    "dry run": "خشک چال",
    "trace table": "ٹریس جدول",
    "big o": "بگ او",
    "binary search": "بائنری تلاش",
    "linear search": "لکیری تلاش",
    "bubble sort": "ببل سارٹ",
    "selection sort": "سیلیکشن سارٹ",
    "insertion sort": "انسرشن سارٹ",
    "linked list": "لنکڈ لسٹ",
    "hash table": "ہیش جدول",
    "binary tree": "بائنری درخت",
    "priority queue": "ترجیحی قطار",
    "virtual memory": "ورچوئل میموری",
    "cloud computing": "کلاؤڈ کمپیوٹنگ",
    "machine learning": "مشین لرننگ",
    "deep learning": "ڈیپ لرننگ",
    "neural network": "نیورل نیٹ ورک",
    "artificial intelligence": "مصنوعی ذہانت",
    "standard deviation": "معیاری انحراف",
    "value proposition": "قدر کی پیشکش",
    "business model": "کاروباری نمونہ",
    "operating system": "آپریٹنگ سسٹم",
    "primary key": "پرائمری کلید",
    "foreign key": "فارن کلید",
    "truth table": "ٹروتھ ٹیبل",
    "logic gate": "لاجک گیٹ",
    "boolean algebra": "بولین الجبرا",
    "gray code": "گرے کوڈ",
    "square wave": "مربع لہر",
    "sine wave": "سائن لہر",
    "analog signal": "اینالاگ سگنل",
    "digital signal": "ڈیجیٹل سگنل",
    "digital system": "ڈیجیٹل نظام",
    "waterfall model": "واٹر فال ماڈل",
    "agile model": "ایجائل ماڈل",
    "data type": "ڈیٹا ٹائپ",
    "control structure": "کنٹرول سٹرکچر",
    "ip address": "آئی پی ایڈریس",
    "number system": "نمبر سسٹم",
    "pie chart": "پائی چارٹ",
    "bar chart": "بار چارٹ",
    "line chart": "لائن چارٹ",
    "scatter plot": "اسکیٹر پلاٹ",
    "box plot": "باکس پلاٹ",
}

# Descriptive English -> Urdu. Exam terms are NOT here; they stay in braces.
LEX = {
    "quantities": "مقداریں", "quantity": "مقدار", "separate": "الگ", "countable": "گنتی کے قابل",
    "items": "چیزیں", "item": "چیز", "students": "طلبہ", "student": "طالب علم", "cars": "گاڑیاں",
    "car": "گاڑی", "park": "پارک", "any": "کوئی بھی", "value": "قدر", "values": "قدریں",
    "water": "پانی", "temperature": "درجہ حرارت", "height": "قد", "heights": "بلندیاں",
    "time": "وقت", "only": "صرف", "two": "دو", "three": "تین", "four": "چار", "five": "پانچ",
    "six": "چھ", "seven": "سات", "eight": "آٹھ", "nine": "نو", "ten": "دس", "called": "کہلاتا ہے",
    "reliable": "قابل اعتماد", "accurate": "درست", "loss": "کمی", "quality": "معیار",
    "copying": "نقل", "easy": "آسان", "designing": "ڈیزائن بنانا", "programmable": "پروگرام کے قابل",
    "computers": "کمپیوٹر", "computer": "کمپیوٹر", "smartphones": "اسمارٹ فون", "smartphone": "اسمارٹ فون",
    "watches": "گھڑیاں", "watch": "گھڑی", "calculators": "کیلکولیٹر", "calculator": "کیلکولیٹر",
    "traffic": "ٹریفک", "lights": "بتیاں", "light": "روشنی", "cameras": "کیمرے", "camera": "کیمرہ",
    "all": "سب", "use": "استعمال", "uses": "استعمال کرتا ہے", "used": "استعمال ہوتا ہے",
    "using": "استعمال کرتے ہوئے", "it": "یہ", "so": "اس لیے", "because": "کیونکہ", "that": "کہ",
    "this": "یہ", "these": "یہ", "those": "وہ", "they": "وہ", "them": "انہیں", "their": "ان کا",
    "we": "ہم", "you": "آپ", "your": "آپ کا", "our": "ہمارا", "each": "ہر", "every": "ہر",
    "both": "دونوں", "one": "ایک", "first": "پہلا", "second": "دوسرا", "third": "تیسرا",
    "next": "اگلا", "last": "آخری", "new": "نیا", "old": "پرانا", "small": "چھوٹا", "large": "بڑا",
    "big": "بڑا", "long": "لمبا", "short": "مختصر", "good": "اچھا", "bad": "برا", "wrong": "غلط",
    "correct": "درست", "same": "وہی", "different": "مختلف", "important": "اہم", "example": "مثال",
    "examples": "مثالیں", "real": "حقیقی", "life": "زندگی", "people": "لوگ", "person": "شخص",
    "human": "انسانی", "voice": "آواز", "noise": "شور", "level": "سطح", "levels": "سطحیں",
    "clear": "واضح", "disturbance": "خلل", "disturbances": "خلل", "change": "تبدیلی",
    "changes": "تبدیلیاں", "changed": "بدل جاتا ہے", "stand": "کھڑے ہوں", "stairs": "سیڑھیاں",
    "ramp": "ڈھلوان", "fixed": "مقررہ", "analogy": "مثال", "remember": "یاد رکھیں", "must": "ضرور",
    "should": "چاہیے", "need": "ضرورت", "needs": "ضرورت ہے", "show": "دکھائیں", "shows": "دکھاتا ہے",
    "shown": "دکھایا گیا", "make": "بنائیں", "makes": "بناتا ہے", "made": "بنایا", "find": "تلاش کریں",
    "found": "ملا", "write": "لکھیں", "writes": "لکھتا ہے", "draw": "بنائیں", "read": "پڑھیں",
    "reads": "پڑھتا ہے", "see": "دیکھیں", "look": "دیکھیں", "keep": "رکھیں", "keeps": "رکھتا ہے",
    "open": "کھلا", "opens": "کھلتا ہے", "opened": "کھلا", "close": "بند", "closed": "بند",
    "start": "شروع", "starts": "شروع ہوتا ہے", "stop": "رکیں", "stops": "رک جاتا ہے",
    "help": "مدد", "helps": "مدد کرتا ہے", "work": "کام", "works": "کام کرتا ہے", "working": "کام",
    "try": "کوشش کریں", "check": "جانچیں", "compare": "موازنہ کریں", "explain": "وضاحت کریں",
    "define": "تعریف کریں", "state": "بیان کریں", "name": "نام", "names": "نام", "calculate": "حساب کریں",
    "convert": "بدلیں", "decimal": "اعشاری", "patterns": "نمونے", "pattern": "نمونہ",
    "multiply": "ضرب دیں", "power": "طاقت", "add": "جمع کریں", "adds": "جمع کرتا ہے",
    "number": "عدد", "numbers": "اعداد", "store": "ذخیرہ", "stores": "ذخیرہ کرتا ہے",
    "stored": "ذخیرہ ہوتا ہے", "everything": "ہر چیز", "foundation": "بنیاد", "developed": "بنایا",
    "mathematician": "ریاضی دان", "english": "انگریزی", "urdu": "اردو", "deals": "متعلق ہے",
    "combines": "ملاتا ہے", "combine": "ملانا", "constants": "مستقل", "constant": "مستقل",
    "operations": "اعمال", "operation": "عمل", "electronic": "الیکٹرانک", "circuits": "سرکٹ",
    "circuit": "سرکٹ", "perform": "انجام دیں", "performs": "انجام دیتا ہے", "exactly": "بالکل",
    "door": "دروازہ", "doors": "دروازے", "locks": "تالے", "lock": "تالا", "unlocked": "کھلا",
    "room": "کمرہ", "enter": "داخل ہوں", "switch": "سوئچ", "dark": "اندھیرا", "fridge": "فریج",
    "pressed": "دبایا گیا", "alarm": "الارم", "sounds": "بجتا ہے", "front": "سامنے", "back": "پیچھے",
    "flipped": "پلٹا", "whenever": "جب بھی", "built": "بنا", "rule": "اصول", "rules": "قواعد",
    "symbol": "علامت", "symbols": "علامتیں", "feature": "خصوصیت", "features": "خصوصیات",
    "nature": "نوعیت", "flows": "بہتی ہے", "flow": "بہاؤ", "smoothly": "ہموار", "smooth": "ہموار",
    "wave": "لہر", "basic": "بنیادی", "unit": "یونٹ", "units": "یونٹ", "physical": "طبعی",
    "digit": "ہندسہ", "digits": "ہندسے", "steps": "قدم", "step": "قدم", "infinite": "لامحدود",
    "resists": "مقابلہ کرتا ہے", "resist": "مقابلہ", "interference": "مداخلت", "easily": "آسانی سے",
    "disturbed": "متاثر", "thermometer": "تھرمامیٹر", "record": "ریکارڈ", "vinyl": "ونائل",
    "kind": "قسم", "kinds": "اقسام", "better": "بہتر", "best": "بہترین", "why": "کیوں",
    "many": "بہت", "give": "دیں", "gives": "دیتا ہے", "given": "دیا گیا", "which": "کون سا",
    "what": "کیا", "how": "کیسے", "when": "جب", "where": "کہاں", "who": "کون", "whose": "جس کا",
    "and": "اور", "or": "یا", "not": "نہیں", "but": "مگر", "if": "اگر", "then": "پھر",
    "else": "ورنہ", "also": "بھی", "very": "بہت", "more": "زیادہ", "most": "سب سے", "than": "سے",
    "after": "بعد", "before": "پہلے", "between": "درمیان", "again": "دوبارہ", "always": "ہمیشہ",
    "never": "کبھی نہیں", "often": "اکثر", "sometimes": "کبھی کبھار", "usually": "عموماً",
    "already": "پہلے ہی", "still": "اب بھی", "even": "حتیٰ", "now": "اب", "today": "آج",
    "page": "صفحہ", "pages": "صفحات", "book": "کتاب", "books": "کتابیں", "paper": "کاغذ",
    "answer": "جواب", "answers": "جوابات", "question": "سوال", "questions": "سوالات",
    "note": "نوٹ", "notes": "نوٹس", "approach": "طریقہ", "activity": "سرگرمی", "activities": "سرگرمیاں",
    "let": "دیں", "above": "اوپر", "below": "نیچے", "inside": "اندر", "outside": "باہر",
    "here": "یہاں", "there": "وہاں", "into": "میں", "onto": "پر", "about": "کے بارے",
    "other": "دوسرا", "another": "ایک اور", "such": "ایسا", "like": "جیسے", "just": "صرف",
    "well": "اچھی طرح", "way": "طریقہ", "ways": "طریقے", "part": "حصہ", "parts": "حصے",
    "whole": "پورا", "half": "آدھا", "full": "مکمل", "empty": "خالی", "simple": "سادہ",
    "complex": "پیچیدہ", "hard": "مشکل", "difficult": "مشکل", "possible": "ممکن",
    "impossible": "ناممکن", "common": "عام", "special": "خاص", "general": "عام",
    "specific": "مخصوص", "main": "مرکزی", "major": "بڑا", "minor": "چھوٹا", "single": "ایک",
    "double": "دوہرا", "several": "کئی", "few": "چند", "little": "تھوڑا", "enough": "کافی",
    "too": "زیادہ", "almost": "تقریباً", "about": "تقریباً", "around": "تقریباً",
    "approximately": "تقریباً", "exactly": "بالکل", "nearly": "قریب", "quite": "کافی",
    "rather": "کافی", "really": "واقعی", "actually": "دراصل", "probably": "غالباً",
    "perhaps": "شاید", "maybe": "شاید", "yes": "ہاں", "no": "نہیں", "please": "براہ کرم",
    "example": "مثال", "case": "صورت", "cases": "صورتیں", "problem": "مسئلہ", "problems": "مسائل",
    "solution": "حل", "solutions": "حل", "result": "نتیجہ", "results": "نتائج", "reason": "وجہ",
    "reasons": "وجہیں", "effect": "اثر", "effects": "اثرات", "cause": "سبب", "causes": "اسباب",
    "goal": "مقصد", "purpose": "مقصد", "aim": "ہدف", "idea": "خیال", "ideas": "خیال",
    "concept": "تصور", "concepts": "تصورات", "definition": "تعریف", "meaning": "مطلب",
    "means": "مطلب ہے", "meanings": "معانی", "word": "لفظ", "words": "الفاظ", "sentence": "جملہ",
    "line": "سطر", "lines": "سطریں", "point": "نکتہ", "points": "نکات", "group": "گروہ",
    "groups": "گروہ", "order": "ترتیب", "ordered": "ترتیب شدہ", "size": "سائز", "shape": "شکل",
    "color": "رنگ", "colour": "رنگ", "colors": "رنگ", "colours": "رنگ", "left": "بائیں",
    "right": "دائیں", "top": "اوپر", "bottom": "نیچے", "middle": "درمیان", "center": "مرکز",
    "centre": "مرکز", "side": "طرف", "sides": "اطراف", "end": "آخر", "ends": "ختم",
    "beginning": "شروع", "finish": "ختم", "finished": "ختم", "complete": "مکمل",
    "completed": "مکمل", "missing": "غائب", "extra": "اضافی", "total": "کل", "sum": "مجموع",
    "average": "اوسط", "count": "گنتی", "amount": "مقدار", "rate": "شرح", "speed": "رفتار",
    "fast": "تیز", "faster": "تیز تر", "slow": "آہستہ", "slower": "آہستہ تر", "quick": "جلد",
    "quickly": "جلدی", "slowly": "آہستہ", "early": "جلد", "late": "دیر", "high": "اونچا",
    "higher": "زیادہ", "low": "کم", "lower": "کم", "positive": "مثبت", "negative": "منفی",
    "zero": "صفر", "equal": "برابر", "equals": "برابر ہے", "greater": "بڑا", "less": "کم",
    "smaller": "چھوٹا", "larger": "بڑا", "biggest": "سب سے بڑا", "smallest": "سب سے چھوٹا",
    "increase": "بڑھنا", "increases": "بڑھتا ہے", "decrease": "گھٹنا", "decreases": "گھٹتا ہے",
    "grow": "بڑھنا", "grows": "بڑھتا ہے", "reduce": "کم کریں", "reduces": "کم کرتا ہے",
    "remove": "ہٹائیں", "removes": "ہٹاتا ہے", "delete": "مٹائیں", "insert": "ڈالیں",
    "replace": "بدل دیں", "copy": "نقل", "copies": "نقلیں", "move": "منتقل", "share": "بانٹیں",
    "send": "بھیجیں", "sends": "بھیجتا ہے", "receive": "وصول کریں", "receives": "وصول کرتا ہے",
    "save": "محفوظ کریں", "saved": "محفوظ", "load": "لوڈ کریں", "print": "چھاپیں",
    "choose": "چنیں", "chooses": "چنتا ہے", "chosen": "چنا گیا", "select": "منتخب کریں",
    "selected": "منتخب", "create": "بنائیں", "creates": "بناتا ہے", "created": "بنایا گیا",
    "build": "بنائیں", "building": "بنانا", "design": "ڈیزائن", "designed": "ڈیزائن کیا گیا",
    "plan": "منصوبہ", "plans": "منصوبے", "planning": "منصوبہ بندی", "test": "جانچ", "tests": "جانچ",
    "study": "مطالعہ", "learn": "سیکھیں", "learns": "سیکھتا ہے", "learning": "سیکھنا",
    "teach": "پڑھائیں", "teacher": "استاد", "teachers": "اساتذہ", "lesson": "سبق",
    "lessons": "اسباق", "chapter": "باب", "practice": "مشق", "exercise": "مشق",
    "homework": "گھر کا کام", "exam": "امتحان", "mark": "نمبر", "marks": "نمبر", "score": "نمبر",
    "grade": "درجہ", "pass": "کامیاب", "fail": "ناکام", "fails": "ناکام ہوتا ہے",
    "error": "غلطی", "errors": "غلطیاں", "mistake": "غلطی", "mistakes": "غلطیاں",
    "correctly": "درست طور پر", "wrongly": "غلط طور پر", "carefully": "احتیاط سے",
    "safely": "محفوظ طریقے سے", "clearly": "صاف", "directly": "براہ راست", "together": "اکٹھے",
    "alone": "اکیلے", "again": "دوبارہ", "once": "ایک بار", "twice": "دو بار", "times": "بار",
    "per": "فی", "during": "دوران", "within": "اندر", "without": "بغیر", "against": "خلاف",
    "across": "پار", "through": "سے", "along": "کے ساتھ", "among": "میں سے", "upon": "پر",
    "off": "بند", "up": "اوپر", "down": "نیچے", "out": "باہر", "in": "میں", "on": "پر",
    "at": "پر", "by": "سے", "for": "کے لیے", "with": "کے ساتھ", "from": "سے", "of": "کا",
    "to": "کو", "as": "جیسے", "than": "سے", "into": "میں", "over": "پر", "under": "نیچے",
    "between": "کے درمیان", "before": "سے پہلے", "after": "کے بعد", "about": "کے بارے میں",
    "because": "کیونکہ", "while": "جبکہ", "until": "جب تک", "unless": "جب تک نہ",
    "although": "اگرچہ", "though": "اگرچہ", "whether": "چاہے", "since": "چونکہ",
    "therefore": "اس لیے", "however": "تاہم", "otherwise": "ورنہ", "instead": "بجائے",
    "including": "بشمول", "except": "سوائے", "plus": "جمع", "minus": "منفی", "times": "ضرب",
    "divided": "تقسیم", "remainder": "باقی", "quotient": "حاصل تقسیم", "product": "حاصل ضرب",
    "factor": "جزو ضربی", "factors": "اجزائے ضربی", "multiple": "مضرب", "prime": "مفرد",
    "even": "جفت", "odd": "طاق", "positive": "مثبت", "negative": "منفی", "fraction": "کسر",
    "percentage": "فیصد", "percent": "فیصد", "ratio": "نسبت", "proportion": "تناسب",
    "angle": "زاویہ", "length": "لمبائی", "width": "چوڑائی", "area": "رقبہ", "volume": "حجم",
    "weight": "وزن", "mass": "کمیت", "distance": "فاصلہ", "direction": "سمت", "position": "مقام",
    "place": "جگہ", "places": "جگہیں", "home": "گھر", "school": "اسکول", "college": "کالج",
    "class": "جماعت", "student": "طالب علم", "teacher": "استاد", "book": "کتاب", "pen": "قلم",
    "board": "بورڈ", "lab": "لیب", "laboratory": "لیبارٹری", "internet": "انٹرنیٹ",
    "website": "ویب سائٹ", "web": "ویب", "online": "آن لائن", "offline": "آف لائن",
    "phone": "فون", "mobile": "موبائل", "message": "پیغام", "email": "ای میل", "call": "کال",
    "user": "صارف", "users": "صارفین", "customer": "گاہک", "customers": "گاہک",
    "people": "لوگ", "person": "شخص", "man": "آدمی", "woman": "خاتون", "child": "بچہ",
    "family": "خاندان", "friend": "دوست", "name": "نام", "age": "عمر", "date": "تاریخ",
    "year": "سال", "years": "سال", "month": "مہینہ", "week": "ہفتہ", "day": "دن", "days": "دن",
    "hour": "گھنٹہ", "hours": "گھنٹے", "minute": "منٹ", "minutes": "منٹ", "second": "سیکنڈ",
    "today": "آج", "tomorrow": "کل", "yesterday": "کل", "morning": "صبح", "evening": "شام",
    "night": "رات", "daily": "روزانہ", "weekly": "ہفتہ وار", "monthly": "ماہانہ",
    "information": "معلومات", "knowledge": "علم", "skill": "مہارت", "skills": "مہارتیں",
    "ability": "صلاحیت", "task": "کام", "tasks": "کام", "job": "کام", "jobs": "کام",
    "role": "کردار", "duty": "فرض", "right": "حق", "rights": "حقوق", "rule": "قاعدہ",
    "law": "قانون", "policy": "پالیسی", "process": "عمل", "method": "طریقہ", "methods": "طریقے",
    "technique": "تکنیک", "strategy": "حکمت عملی", "tool": "آلہ", "tools": "آلات",
    "device": "آلہ", "devices": "آلات", "machine": "مشین", "machines": "مشینیں",
    "program": "پروگرام", "programs": "پروگرام", "programme": "پروگرام", "code": "کوڈ",
    "coding": "کوڈ لکھنا", "software": "سافٹ ویئر", "hardware": "ہارڈ ویئر", "application": "اطلاق",
    "applications": "اطلاقات", "app": "ایپ", "apps": "ایپس", "screen": "سکرین", "window": "ونڈو",
    "menu": "مینو", "icon": "آئیکن", "text": "متن", "image": "تصویر", "images": "تصاویر",
    "picture": "تصویر", "video": "ویڈیو", "audio": "آواز", "sound": "آواز", "music": "موسیقی",
    "document": "دستاویز", "report": "رپورٹ", "reports": "رپورٹیں", "chart": "چارٹ",
    "charts": "چارٹ", "diagram": "خاکہ", "diagrams": "خاکے", "figure": "شکل", "figures": "شکلیں",
    "label": "لیبل", "labels": "لیبل", "title": "عنوان", "heading": "سرخی", "column": "کالم",
    "columns": "کالم", "row": "قطار", "rows": "قطاریں", "cell": "خانہ", "cells": "خانے",
    "box": "خانہ", "boxes": "خانے", "card": "کارڈ", "cards": "کارڈ", "sheet": "شیٹ",
    "spreadsheet": "اسپریڈ شیٹ", "formula": "فارمولا", "formulas": "فارمولے", "cell": "سیل",
    "click": "کلک", "type": "لکھیں", "typing": "لکھنا", "press": "دبائیں", "hold": "پکڑیں",
    "drag": "گھسیٹیں", "drop": "چھوڑیں", "scroll": "سکرول", "zoom": "بڑا کریں", "search": "تلاش",
    "sort": "ترتیب", "filter": "چھانٹ", "update": "تازہ کریں", "edit": "ترمیم", "undo": "واپس",
    "redo": "دوبارہ", "cut": "کاٹیں", "paste": "چسپاں", "format": "فارمیٹ", "style": "انداز",
    "font": "فونٹ", "size": "سائز", "bold": "موٹا", "align": "سیدھ", "margin": "حاشیہ",
    "header": "سرنامہ", "footer": "ذیلی نوشت", "link": "ربط", "links": "روابط", "source": "ماخذ",
    "sources": "ماخذ", "reference": "حوالہ", "references": "حوالے", "citation": "حوالہ",
    "author": "مصنف", "publisher": "ناشر", "edition": "ایڈیشن", "version": "ورژن",
    "chapter": "باب", "section": "حصہ", "paragraph": "پیرا", "topic": "موضوع", "topics": "موضوعات",
    "subject": "مضمون", "course": "کورس", "curriculum": "نصاب", "syllabus": "نصاب",
    "outcome": "حاصل", "outcomes": "حاصلات", "objective": "مقصد", "objectives": "مقاصد",
    "assessment": "جانچ", "rubric": "روبرک", "criterion": "معیار", "criteria": "معیار",
    "feedback": "رائے", "review": "جائزہ", "revision": "دہرائی", "recap": "دہرائی",
    "summary": "خلاصہ", "conclusion": "نتیجہ", "introduction": "تعارف", "overview": "جائزہ",
    "detail": "تفصیل", "details": "تفصیلات", "brief": "مختصر", "full": "مکمل", "partial": "جزوی",
    "optional": "اختیاری", "required": "لازمی", "necessary": "ضروری", "available": "دستیاب",
    "useful": "مفید", "helpful": "مددگار", "effective": "موثر", "efficient": "کارگر",
    "efficiency": "کارکردگی", "performance": "کارکردگی", "cost": "لاگت", "price": "قیمت",
    "free": "مفت", "paid": "ادا شدہ", "cheap": "سستا", "expensive": "مہنگا", "safe": "محفوظ",
    "secure": "محفوظ", "security": "سلامتی", "privacy": "رازداری", "private": "نجی",
    "public": "عوامی", "local": "مقامی", "global": "عالمی", "national": "قومی",
    "personal": "ذاتی", "social": "سماجی", "cultural": "ثقافتی", "ethical": "اخلاقی",
    "ethics": "اخلاق", "legal": "قانونی", "illegal": "غیر قانونی", "fair": "منصفانہ",
    "unfair": "ناانصافی", "bias": "جھکاؤ", "risk": "خطرہ", "risks": "خطرات", "threat": "خطرہ",
    "threats": "خطرات", "attack": "حملہ", "protect": "بچائیں", "protection": "تحفظ",
    "damage": "نقصان", "loss": "نقصان", "benefit": "فائدہ", "benefits": "فوائد",
    "advantage": "فائدہ", "disadvantage": "نقصان", "limitation": "حد", "limit": "حد",
    "limits": "حدود", "strength": "طاقت", "weakness": "کمزوری", "opportunity": "موقع",
    "challenge": "چیلنج", "problem-solving": "مسئلہ حل کرنا", "decision": "فیصلہ",
    "decide": "فیصلہ کریں", "decides": "فیصلہ کرتا ہے", "choice": "انتخاب", "choose": "چنیں",
    "option": "اختیار", "options": "اختیارات", "alternative": "متبادل", "prefer": "ترجیح",
    "compare": "موازنہ", "comparison": "موازنہ", "difference": "فرق", "differences": "فرق",
    "similarity": "مشابہت", "similar": "مشابہ", "match": "میل", "matches": "ملتا ہے",
    "fit": "فٹ", "suitable": "موزوں", "appropriate": "مناسب", "relevant": "متعلق",
    "related": "متعلق", "connection": "تعلق", "connected": "جڑا", "connect": "جوڑیں",
    "disconnect": "الگ کریں", "communication": "ابلاغ", "communicate": "بتائیں",
    "message": "پیغام", "signal": "اشارہ", "signals": "اشارے", "wave": "لہر", "waves": "لہریں",
    "smooth": "ہموار", "sharp": "تیز", "square": "مربع", "round": "گول", "circle": "دائرہ",
    "line": "لکیر", "arrow": "تیر", "box": "ڈبہ", "diamond": "ہیرا", "oval": "بیضوی",
    "rectangle": "مستطیل", "triangle": "مثلث", "bubble": "بلبلہ", "cloud": "بادل",
    "memory": "یاد", "remember": "یاد رکھیں", "forget": "بھولنا", "recall": "یاد کرنا",
    "understand": "سمجھیں", "understanding": "سمجھ", "explain": "سمجھائیں", "explanation": "وضاحت",
    "describe": "بیان کریں", "description": "بیان", "identify": "پہچانیں", "identification": "پہچان",
    "classify": "درجہ بند کریں", "category": "قسم", "categories": "اقسام", "type": "قسم",
    "types": "اقسام", "kind": "قسم", "form": "شکل", "forms": "شکلیں", "format": "ہیئت",
    "structure": "ساخت", "structures": "ساختیں", "pattern": "نمونہ", "sequence": "ترتیب",
    "series": "سلسلہ", "cycle": "چکر", "stage": "مرحلہ", "stages": "مراحل", "phase": "مرحلہ",
    "phases": "مراحل", "level": "درجہ", "degree": "درجہ", "scale": "پیمانہ", "measure": "ناپ",
    "measurement": "پیمائش", "unit": "اکائی", "standard": "معیار", "normal": "عام",
    "typical": "عام", "unusual": "غیر معمولی", "rare": "نایاب", "frequent": "بار بار",
    "frequency": "بار بار ہونا", "occur": "واقع ہونا", "occurs": "واقع ہوتا ہے",
    "happen": "ہونا", "happens": "ہوتا ہے", "become": "بن جانا", "becomes": "بن جاتا ہے",
    "remain": "رہنا", "remains": "رہتا ہے", "stay": "رہیں", "leave": "چھوڑیں", "reach": "پہنچیں",
    "return": "واپس", "returns": "واپس آتا ہے", "follow": "پیروی کریں", "follows": "پیروی کرتا ہے",
    "lead": "رہنمائی", "leads": "لے جاتا ہے", "allow": "اجازت", "allows": "اجازت دیتا ہے",
    "prevent": "روکیں", "prevents": "روکتا ہے", "avoid": "بچیں", "require": "ضرورت",
    "requires": "ضرورت ہے", "required": "لازمی", "include": "شامل", "includes": "شامل ہے",
    "contain": "رکھتا ہے", "contains": "رکھتا ہے", "consist": "پر مشتمل", "consists": "پر مشتمل ہے",
    "represent": "ظاہر کرے", "represents": "ظاہر کرتا ہے", "indicate": "بتائے", "indicates": "بتاتا ہے",
    "support": "سہارا", "supports": "سہارا دیتا ہے", "provide": "دیں", "provides": "دیتا ہے",
    "produce": "پیدا کرے", "produces": "پیدا کرتا ہے", "generate": "بنائیں", "generates": "بناتا ہے",
    "collect": "جمع کریں", "collects": "جمع کرتا ہے", "collected": "جمع شدہ", "gather": "اکٹھا کریں",
    "organise": "ترتیب دیں", "organize": "ترتیب دیں", "arranged": "ترتیب شدہ", "arrangement": "ترتیب",
    "prepare": "تیار کریں", "prepared": "تیار", "ready": "تیار", "done": "ہو گیا",
    "success": "کامیابی", "successful": "کامیاب", "failure": "ناکامی", "failed": "ناکام",
    "try": "کوشش", "attempt": "کوشش", "attempts": "کوششیں", "practice": "مشق", "repeat": "دہرائیں",
    "repeated": "دہرایا", "repetition": "دہراؤ", "continue": "جاری رکھیں", "continues": "جاری رہتا ہے",
    "pause": "رکیں", "wait": "انتظار", "watch": "دیکھیں", "observe": "مشاہدہ", "observation": "مشاہدہ",
    "notice": "نوٹس", "ignore": "نظر انداز", "focus": "توجہ", "attention": "توجہ", "careful": "محتاط",
    "caution": "احتیاط", "warning": "انتباہ", "important": "اہم", "critical": "نازک",
    "essential": "لازمی", "basic": "بنیادی", "advanced": "اعلیٰ", "simple": "سادہ",
    "detailed": "تفصیلی", "briefly": "مختصر اً", "finally": "آخر میں", "firstly": "پہلے",
    "secondly": "دوسرے", "lastly": "آخر میں", "meanwhile": "اس دوران", "later": "بعد میں",
    "earlier": "پہلے", "soon": "جلد", "immediately": "فوراً", "suddenly": "اچانک",
    "gradually": "آہستہ آہستہ", "automatically": "خود بخود", "manually": "ہاتھ سے",
    "correct": "درست", "incorrect": "غلط", "valid": "جائز", "invalid": "ناجائز",
    "possible": "ممکن", "available": "موجود", "present": "موجود", "absent": "غیر حاضر",
    "current": "موجودہ", "previous": "پچھلا", "following": "اگلا", "above": "اوپر والا",
    "below": "نیچے والا", "following": "مندرجہ ذیل", "given": "دیا گیا", "shown": "دکھایا گیا",
    "printed": "چھپا ہوا", "written": "لکھا ہوا", "spoken": "بولا ہوا", "drawn": "بنایا ہوا",
    "known": "معلوم", "unknown": "نامعلوم", "called": "کہلاتا ہے", "named": "نام رکھا",
    "defined": "تعریف کی گئی", "described": "بیان کیا گیا", "listed": "فہرست میں",
    "based": "بنیاد", "related": "متعلق", "associated": "جڑا", "linked": "جڑا",
    "shared": "مشترکہ", "common": "مشترک", "own": "اپنا", "each": "ہر ایک", "every": "ہر",
    "some": "کچھ", "any": "کوئی", "none": "کوئی نہیں", "nothing": "کچھ نہیں", "something": "کچھ",
    "everything": "سب کچھ", "someone": "کوئی", "everyone": "سب", "anyone": "کوئی بھی",
    "nobody": "کوئی نہیں", "many": "بہت سے", "much": "بہت", "few": "چند", "several": "کئی",
    "various": "مختلف", "certain": "کچھ خاص", "particular": "خاص", "whole": "سارا",
    "entire": "پورا", "rest": "باقی", "other": "دیگر", "others": "دوسرے", "another": "ایک اور",
    "same": "وہی", "own": "خود", "self": "خود", "together": "مل کر", "separately": "الگ الگ",
    "respectively": "بالترتیب", "approximately": "تقریباً", "exactly": "بالکل",
    "at least": "کم از کم", "at most": "زیادہ سے زیادہ",
    "student": "طالب علم", "students": "طلبہ", "class": "جماعت", "school": "اسکول",
    "teacher": "استاد", "answer": "جواب", "question": "سوال", "example": "مثال",
    "figure": "شکل", "table": "جدول", "page": "صفحہ", "booklet": "کتابچہ", "textbook": "نصابی کتاب",
    "lesson": "سبق", "unit": "یونٹ", "chapter": "باب", "exercise": "مشق", "activity": "سرگرمی",
    "note": "نوٹ", "misconception": "غلط فہمی", "approach": "طریقہ", "analogy": "تشبیہ",
    "stairs": "سیڑھیاں", "ramp": "ڈھلوان", "height": "بلندی", "temperature": "درجہ حرارت",
    "water": "پانی", "noise": "شور", "wave": "لہر", "smooth": "ہموار", "square": "مربع",
    "level": "سطح", "levels": "سطحیں", "copy": "نقل", "quality": "معیار", "reliable": "قابل اعتماد",
    "accurate": "درست", "easy": "آسان", "hard": "مشکل", "small": "معمولی", "large": "بڑا",
    "clear": "واضح", "disturbance": "خلل", "change": "بدلنا", "stand": "ظاہر کرنا",
    "stands": "ظاہر کرتا ہے", "represent": "ظاہر کرنا", "represents": "ظاہر کرتا ہے",
    "means": "مطلب", "meaning": "مطلب", "called": "کہلاتے ہیں", "name": "نام",
    "real": "روزمرہ", "life": "زندگی", "door": "دروازہ", "lock": "تالا", "locks": "تالے",
    "unlocked": "کھلا", "room": "کمرہ", "enter": "داخل ہونا", "light": "روشنی", "switch": "سوئچ",
    "dark": "اندھیرا", "alarm": "الارم", "front": "سامنے والا", "back": "پچھلا", "key": "چابی",
    "button": "بٹن", "pressed": "دبایا", "car": "گاڑی", "starts": "چلتی ہے", "fridge": "فریج",
    "open": "کھلا", "closed": "بند", "whenever": "جب بھی", "either": "کوئی ایک", "neither": "کوئی نہیں",
    "both": "دونوں", "all": "تمام", "any": "کوئی بھی", "every": "ہر", "only": "صرف",
    "two": "دو", "one": "ایک", "three": "تین", "four": "چار", "values": "قدریں", "value": "قدر",
    "numbers": "اعداد", "number": "عدد", "pattern": "نمونہ", "patterns": "نمونے",
    "power": "طاقت", "multiply": "ضرب", "add": "جمع", "read": "پڑھیں", "binary": "بائنری",
    "decimal": "اعشاری", "convert": "تبدیل کریں", "conversion": "تبدیلی", "count": "گنتی",
    "different": "مختلف", "same": "ایک جیسا", "opposite": "الٹ", "inverse": "الٹ",
    "invert": "الٹیں", "inverts": "الٹ دیتا ہے", "combine": "ملانا", "combination": "میل",
    "possible": "ممکن", "row": "قطار", "rows": "قطاریں", "column": "کالم", "cell": "خانہ",
    "group": "گروہ", "groups": "گروہ", "adjacent": "پڑوسی", "neighbour": "پڑوسی",
    "neighbor": "پڑوسی", "pair": "جوڑا", "pairs": "جوڑے", "single": "اکیلا", "wrap": "لپیٹ",
    "simplify": "سادہ کریں", "simplified": "سادہ", "expression": "اظہار", "variable": "متغیر",
    "constant": "مستقل", "operation": "عمل", "circuit": "سرکٹ", "wire": "تار", "wires": "تاریں",
    "connect": "جوڑیں", "connection": "جوڑ", "power": "بجلی", "voltage": "وولٹیج",
    "frequency": "تعدد", "current": "کرنٹ", "resistance": "مزاحمت", "switch": "سوئچ",
    "bulb": "بلب", "battery": "بیٹری", "ground": "ارتھ", "clock": "گھڑی", "pulse": "نبض",
    "edge": "کنارہ", "rising": "چڑھتا", "falling": "گرتا", "stable": "مستحکم", "unstable": "غیر مستحکم",
    "noise": "شور", "error": "خرابی", "correct": "درست", "detect": "پکڑیں", "corrects": "درست کرتا ہے",
    "send": "بھیجیں", "receive": "وصول", "sender": "بھیجنے والا", "receiver": "وصول کرنے والا",
    "channel": "چینل", "medium": "ذریعہ", "cable": "تار", "wireless": "بغیر تار", "wired": "تار والا",
    "address": "پتہ", "route": "راستہ", "path": "راستہ", "hop": "چھلانگ", "host": "میزبان",
    "device": "آلہ", "devices": "آلات", "computer": "کمپیوٹر", "phone": "فون", "printer": "پرنٹر",
    "server": "سرور", "client": "صارف آلہ", "request": "درخواست", "response": "جواب",
    "message": "پیغام", "packet": "لفافہ", "header": "سرنامہ", "body": "جسم", "payload": "اصل مواد",
    "port": "دروازہ نمبر", "socket": "جوڑ", "connection": "کنکشن", "session": "نشست",
    "reliable": "قابل اعتماد", "unreliable": "بے اعتبار", "ordered": "ترتیب والا",
    "unordered": "بے ترتیب", "fast": "تیز", "slow": "سست", "secure": "محفوظ", "open": "کھلا",
    "closed": "بند", "handshake": "مصافحہ", "acknowledge": "وصول نامہ", "timeout": "وقت ختم",
    "retry": "دوبارہ کوشش", "lost": "کھویا", "corrupt": "بگڑا", "delay": "تاخیر", "jitter": "لرزش",
    "throughput": "گزرنے والی مقدار", "congestion": "رش", "collision": "ٹکر", "broadcast": "سب کو",
    "multicast": "گروہ کو", "unicast": "ایک کو", "topology": "بناوٹ", "star": "ستارہ",
    "bus": "بس", "ring": "حلقہ", "mesh": "جال", "hybrid": "ملا جلا", "node": "نوڈ",
    "link": "ربط", "backbone": "ریڑھ", "gateway": "دروازہ", "bridge": "پل", "hub": "حب",
    "modem": "موڈیم", "antenna": "اینٹینا", "signal": "سگنل", "strength": "طاقت",
    "coverage": "کوریج", "range": "رسائی", "interference": "مداخلت", "security": "سلامتی",
    "privacy": "رازداری", "permission": "اجازت", "identity": "شناخت", "account": "اکاؤنٹ",
    "user": "صارف", "admin": "منتظم", "guest": "مہمان", "role": "کردار", "policy": "پالیسی",
    "rule": "قاعدہ", "allow": "اجازت", "deny": "انکار", "block": "روک", "filter": "چھانٹی",
    "log": "نوشتہ", "monitor": "نگرانی", "alert": "انتباہ", "incident": "واقعہ", "backup": "نقل",
    "restore": "بحال", "archive": "محفوظ خانہ", "compress": "دباؤ", "encrypt": "خفیہ کریں",
    "decrypt": "کھولیں", "sign": "دستخط", "verify": "تصدیق", "certificate": "سند",
    "trust": "اعتماد", "key": "کلید", "public": "عوامی", "private": "نجی", "secret": "راز",
    "password": "پاس ورڈ", "pin": "پن", "pattern": "نمونہ", "fingerprint": "انگلی کا نشان",
    "face": "چہرہ", "iris": "آنکھ", "token": "ٹوکن", "card": "کارڈ", "smart": "سمارٹ",
    "home": "گھر", "farm": "کھیت", "city": "شہر", "grid": "گرڈ", "wearable": "پہننے والا",
    "health": "صحت", "agriculture": "زراعت", "irrigation": "آبپاشی", "soil": "مٹی",
    "moisture": "نمی", "crop": "فصل", "weather": "موسم", "temperature": "درجہ حرارت",
    "humidity": "نمی", "light": "روشنی", "motion": "حرکت", "door": "دروازہ", "lamp": "لیمپ",
    "fan": "پنکھا", "valve": "والو", "pump": "پمپ", "motor": "موٹر", "robot": "روبوٹ",
    "camera": "کیمرہ", "speaker": "اسپیکر", "microphone": "مائیک", "display": "ڈسپلے",
    "battery": "بیٹری", "power": "بجلی", "energy": "توانائی", "solar": "شمسی", "save": "بچت",
    "waste": "ضیاع", "efficient": "بچت والا", "cost": "لاگت", "cheap": "سستا", "remote": "دور",
    "control": "کنٹرول", "automatic": "خودکار", "manual": "دستی", "schedule": "شیڈول",
    "threshold": "حد", "trigger": "چالان", "event": "واقعہ", "action": "عمل", "condition": "شرط",
    "if": "اگر", "else": "ورنہ", "while": "جب تک", "until": "جب تک", "repeat": "دہرائیں",
    "count": "گنتی", "counter": "گنتی کار", "flag": "جھنڈا", "status": "حالت", "state": "حالت",
    "initial": "ابتدائی", "final": "حتمی", "current": "موجودہ", "next": "اگلا", "previous": "پچھلا",
    "empty": "خالی", "full": "بھرا", "overflow": "حد سے بڑھنا", "underflow": "حد سے گھٹنا",
    "push": "ڈالیں", "pop": "نکالیں", "enqueue": "قطار میں ڈالیں", "dequeue": "قطار سے نکالیں",
    "peek": "اوپر دیکھیں", "top": "چوٹی", "front": "آگے", "rear": "پیچھے", "head": "سر",
    "tail": "دم", "parent": "والد", "child": "بچہ", "children": "بچے", "leaf": "پتا",
    "root": "جڑ", "depth": "گہرائی", "height": "اونچائی", "balance": "توازن", "visit": "ملاحظہ",
    "left": "بائیں", "right": "دائیں", "sorted": "ترتیب شدہ", "unsorted": "بے ترتیب",
    "ascending": "بڑھتا", "descending": "گھٹتا", "swap": "ادل بدل", "compare": "موازنہ",
    "pass": "چکر", "passes": "چکر", "comparison": "موازنہ", "best": "بہترین", "worst": "بدترین",
    "average": "اوسط", "case": "صورت", "time": "وقت", "space": "جگہ", "memory": "میموری",
    "temporary": "عارضی", "permanent": "مستقل", "local": "مقامی", "global": "عالمی",
    "parameter": "پیرامیٹر", "argument": "دلیل", "return": "واپسی", "call": "بلاوا",
    "define": "تعریف", "definition": "تعریف", "body": "جسم", "header": "سر", "name": "نام",
    "value": "قدر", "assign": "تفویض", "assignment": "تفویض", "update": "تازہ", "read": "پڑھنا",
    "write": "لکھنا", "append": "آخر میں جوڑیں", "insert": "داخل", "delete": "حذف",
    "search": "تلاش", "found": "مل گیا", "missing": "غائب", "duplicate": "دہرائی",
    "unique": "منفرد", "ordered": "ترتیب والا", "indexed": "نمبر والا", "mutable": "قابل تبدیلی",
    "immutable": "ناقابل تبدیلی", "empty": "خالی", "length": "لمبائی", "size": "سائز",
    "index": "انڈیکس", "slice": "ٹکڑا", "element": "رکن", "elements": "ارکان", "member": "رکن",
    "membership": "رکنیت", "key": "کلید", "pair": "جوڑا", "mapping": "نقشہ", "lookup": "ڈھونڈنا",
    "hash": "ہیش", "bucket": "ڈول", "collision": "ٹکر", "chain": "زنجیر", "probe": "کھوج",
    "load": "بوجھ", "factor": "جزو", "resize": "سائز بدلنا", "capacity": "گنجائش",
    "dynamic": "متحرک", "static": "ساکن", "fixed": "مقرر", "flexible": "لچکدار",
    "typed": "قسم والا", "untyped": "بغیر قسم", "convert": "بدلنا", "cast": "ڈالنا",
    "integer": "صحیح عدد", "whole": "پورا", "fraction": "کسر", "decimal": "اعشاری",
    "round": "گول", "floor": "نیچے", "ceil": "اوپر", "absolute": "مطلق", "sign": "نشان",
    "positive": "مثبت", "negative": "منفی", "zero": "صفر", "infinity": "لامحدود",
    "divide": "تقسیم", "remainder": "باقی", "modulo": "باقی", "power": "طاقت", "root": "جذر",
    "square": "مربع", "cube": "مکعب", "log": "لاگ", "random": "بے ترتیب", "seed": "بیج",
    "true": "سچ", "false": "جھوٹ", "and": "اور", "or": "یا", "not": "نہیں", "both": "دونوں",
    "either": "ایک", "neither": "کوئی نہیں", "condition": "شرط", "conditions": "شرائط",
    "branch": "شاخ", "branches": "شاخیں", "decision": "فیصلہ", "choice": "انتخاب",
    "otherwise": "ورنہ", "nested": "اندر اندر", "indent": "حاشیہ", "colon": "کولن",
    "block": "بلاک", "suite": "بلاک", "comment": "تبصرہ", "whitespace": "خالی جگہ",
    "error": "خرابی", "bug": "بگ", "fix": "درست کریں", "trace": "نشان", "step": "قدم",
    "debug": "خرابی نکالیں", "test": "جانچ", "case": "کیس", "expected": "متوقع",
    "actual": "اصل", "pass": "پورا", "fail": "ناکام", "assert": "تصدیق", "edge": "کنارا",
    "boundary": "سرحد", "normal": "عام", "invalid": "ناجائز", "valid": "جائز", "input": "ان پٹ",
    "output": "آؤٹ پٹ", "sample": "نمونہ", "dry": "خشک", "run": "چلائیں", "runs": "چلتا ہے",
    "running": "چل رہا", "execute": "چلائیں", "execution": "چلنا", "compile": "مرتب",
    "interpret": "ترجمہ کرتے چلیں", "source": "ماخذ", "program": "پروگرام", "script": "سکرپٹ",
    "editor": "ایڈیٹر", "terminal": "ٹرمینل", "console": "کنسول", "prompt": "اشارہ",
    "command": "حکم", "commands": "احکامات", "install": "نصب", "import": "درآمد",
    "library": "کتب خانہ", "module": "ماڈیول", "package": "پیکج", "function": "فنکشن",
    "method": "طریقہ", "object": "شے", "class": "جماعت", "instance": "مثال", "attribute": "صفت",
    "property": "خاصیت", "inherit": "وراثت", "inheritance": "وراثت", "parent": "والد",
    "child": "فرزند", "override": "بدل دیں", "polymorphism": "کئی شکلیں", "encapsulation": "لپیٹ",
    "abstraction": "خلاصہ", "interface": "رابطہ", "implement": "نافذ", "extends": "بڑھاتا ہے",
    "public": "کھلا", "private": "چھپا", "protected": "محفوظ", "constructor": "بنانے والا",
    "destructor": "مٹانے والا", "self": "خود", "this": "یہ", "super": "اوپر والا",
    "static": "ساکن", "instance": "مثال", "call": "بلاؤ", "return": "لوٹاؤ", "yield": "دو",
    "raise": "اٹھاؤ", "catch": "پکڑو", "handle": "سنبھالو", "exception": "استثنا",
    "finally": "آخر میں", "try": "کوشش", "except": "سوائے", "else": "ورنہ", "pass": "گزر",
    "break": "توڑو", "continue": "جاری", "return": "واپس", "global": "عالمی", "nonlocal": "بیرونی",
    "lambda": "مختصر فنکشن", "decorator": "لپیٹ", "generator": "بنانے والا", "iterator": "چلنے والا",
    "iterable": "جس پر چلیں", "comprehension": "مختصر تعمیر", "slice": "ٹکڑا", "stride": "قدم",
    "unpack": "کھولیں", "pack": "باندھیں", "zip": "جوڑیں", "map": "لگائیں", "filter": "چھانیں",
    "reduce": "سمیٹیں", "sort": "ترتیب", "sorted": "ترتیب شدہ", "reverse": "الٹ", "copy": "نقل",
    "deep": "گہرا", "shallow": "سطحی", "reference": "حوالہ", "identity": "شناخت", "equality": "برابری",
    "mutable": "بدلنے والا", "immutable": "نہ بدلنے والا", "side": "طرف", "effect": "اثر",
    "pure": "خالص", "recursive": "خود کو بلانے والا", "base": "بنیاد", "case": "صورت",
    "inductive": "اگلا قدم", "stack": "ڈھیر", "overflow": "بھر جانا", "depth": "گہرائی",
    "tail": "دم", "memo": "یاد", "cache": "کیش", "dynamic": "متحرک", "greedy": "لالچی",
    "divide": "بانٹو", "conquer": "جیتو", "brute": "کچا", "force": "زور", "optimal": "بہترین",
    "feasible": "ممکن", "constraint": "پابندی", "objective": "مقصد", "tradeoff": "لین دین",
    "trade-off": "لین دین", "scalable": "بڑھنے کے قابل", "readable": "پڑھنے کے قابل",
    "maintainable": "سنبھلنے کے قابل", "reusable": "دوبارہ استعمال", "modular": "ٹکڑوں والا",
    "coupled": "جڑا", "cohesion": "اندرونی جوڑ", "coupling": "بیرونی جوڑ", "refactor": "سدھارو",
    "version": "نسخہ", "commit": "محفوظ قدم", "branch": "شاخ", "merge": "ملانا", "conflict": "ٹکراؤ",
    "repository": "خزانہ", "remote": "دور", "clone": "نقل", "pull": "کھینچیں", "push": "دھکیلیں",
    "issue": "مسئلہ", "review": "جائزہ", "approve": "منظور", "release": "اجراء", "deploy": "لگائیں",
    "production": "اصل استعمال", "staging": "جانچ گاہ", "development": "تیاری", "environment": "ماحول",
    "configuration": "ترتیب", "setting": "سیٹنگ", "default": "طے شدہ", "custom": "اپنی مرضی",
    "user": "صارف", "experience": "تجربہ", "journey": "سفر", "goal": "مقصد", "pain": "تکلیف",
    "need": "ضرورت", "task": "کام", "scenario": "منظر", "story": "کہانی", "requirement": "ضرورت",
    "sketch": "خاکہ", "mock": "نقل", "click": "کلک", "tap": "چھونا", "swipe": "سرکانا",
    "gesture": "اشارہ", "keyboard": "کی بورڈ", "mouse": "ماؤس", "touch": "چھونا", "screen": "سکرین",
    "reader": "پڑھنے والا", "caption": "کیپشن", "alt": "متبادل متن", "focus": "توجہ",
    "tab": "ٹیب", "order": "ترتیب", "contrast": "فرق", "colour": "رنگ", "color": "رنگ",
    "font": "فونٹ", "size": "ناپ", "spacing": "فاصلہ", "alignment": "سیدھ", "hierarchy": "درجہ بندی",
    "consistency": "یکسانیت", "visibility": "نظر آنا", "error": "خرابی", "message": "پیغام",
    "recovery": "بحالی", "undo": "واپس", "confirm": "تصدیق", "cancel": "منسوخ", "save": "محفوظ",
    "submit": "جمع", "loading": "لوڈ", "empty": "خالی", "success": "کامیابی", "warning": "انتباہ",
    "disabled": "بند", "enabled": "چالو", "selected": "چنا", "hover": "اوپر ٹھہرنا",
    "responsive": "ہر ناپ پر درست", "mobile": "موبائل", "desktop": "ڈیسک ٹاپ", "tablet": "ٹیبلیٹ",
    "survey": "سروے", "interview": "انٹرویو", "observation": "مشاہدہ", "questionnaire": "سوالنامہ",
    "sample": "نمونہ", "random": "بے ترتیب", "stratified": "طبقاتی", "cluster": "گچھہ",
    "convenience": "آسان", "bias": "جھکاؤ", "representative": "نمائندہ", "confidence": "اعتماد",
    "interval": "وقفہ", "margin": "حاشیہ", "significance": "معنی", "hypothesis": "مفروضہ",
    "null": "صفر مفروضہ", "alternative": "متبادل", "variable": "متغیر", "independent": "آزاد",
    "dependent": "تابع", "control": "کنٹرول", "treatment": "عمل", "placebo": "نقلی",
    "trial": "آزمائش", "experiment": "تجربہ", "observational": "مشاہداتی", "causal": "سببی",
    "correlation": "باہمی رشتہ", "scatter": "بکھراؤ", "trend": "رجحان", "slope": "ڈھلوان",
    "intercept": "کاٹ", "residual": "باقی", "fit": "فٹ", "line": "لکیر", "curve": "خم",
    "distribution": "تقسیم", "normal": "عام", "skew": "ترچھا", "symmetric": "متشاکل",
    "spread": "پھیلاؤ", "center": "مرکز", "centre": "مرکز", "outlier": "باغی قدر",
    "whisker": "مونچھ", "quartile": "چوتھائی", "percentile": "صدی", "decile": "دسواں",
    "frequency": "تعدد", "relative": "نسبتی", "cumulative": "مجموعی", "bin": "خانہ",
    "width": "چوڑائی", "density": "کثافت", "proportion": "تناسب", "percentage": "فیصد",
    "fraction": "کسر", "ratio": "نسبت", "rate": "شرح", "per": "فی", "average": "اوسط",
    "typical": "عام", "extreme": "انتہا", "minimum": "کم سے کم", "maximum": "زیادہ سے زیادہ",
    "sum": "مجموع", "count": "گنتی", "missing": "غائب", "clean": "صاف", "cleaning": "صفائی",
    "raw": "خام", "processed": "عمل شدہ", "transform": "بدلنا", "scale": "پیمانہ",
    "normalize": "معیاری بنانا", "standardize": "معیاری", "encode": "کوڈ کرنا", "decode": "کھولنا",
    "category": "قسم", "numeric": "عددی", "numerical": "عددی", "categorical": "قسمی",
    "ordinal": "ترتیبی", "nominal": "نامی", "continuous": "مسلسل", "discrete": "منفرد",
    "time": "وقت", "series": "سلسلہ", "season": "موسم", "forecast": "پیش گوئی", "predict": "بتانا",
    "prediction": "پیش گوئی", "train": "سکھانا", "test": "جانچ", "validate": "تصدیق",
    "split": "بانٹ", "feature": "خصوصیت", "features": "خصوصیات", "target": "ہدف", "label": "لیبل",
    "row": "قطار", "column": "کالم", "table": "جدول", "cell": "خانہ", "header": "سرخی",
    "import": "لانا", "export": "نکالنا", "plot": "گراف", "axis": "محور", "legend": "کلید",
    "title": "عنوان", "grid": "جال", "marker": "نشان", "bar": "ستون", "pie": "دائرہ",
    "slice": "ٹکڑا", "histogram": "ہسٹوگرام", "boxplot": "بکس پلاٹ", "heatmap": "حرارتی نقشہ",
    "dashboard": "ڈیش بورڈ", "insight": "بصیرت", "story": "کہانی", "audience": "سامعین",
    "claim": "دعویٰ", "evidence": "ثبوت", "warrant": "جواز", "misleading": "گمراہ",
    "accurate": "درست", "honest": "ایماندار", "source": "ماخذ", "cite": "حوالہ", "ethics": "اخلاق",
    "consent": "رضامندی", "anonymous": "گمنام", "confidential": "خفیہ", "sensitive": "حساس",
    "personal": "ذاتی", "store": "رکھنا", "share": "بانٹنا", "delete": "مٹانا", "retain": "رکھنا",
    "purpose": "مقصد", "minimize": "کم کریں", "necessary": "ضروری", "lawful": "جائز",
    "farmer": "کسان", "field": "کھیت", "sensor": "سینسر", "reading": "پیمائش", "alert": "انتباہ",
    "irrigate": "پانی دیں", "yield": "پیداوار", "cost": "لاگت", "profit": "نفع", "loss": "نقصان",
    "customer": "گاہک", "market": "منڈی", "product": "مصنوع", "service": "خدمت", "price": "قیمت",
    "value": "قدر", "problem": "مسئلہ", "solution": "حل", "idea": "خیال", "team": "ٹیم",
    "founder": "بانی", "investor": "سرمایہ کار", "share": "حصہ", "ownership": "ملکیت",
    "revenue": "آمدن", "cost": "خرچ", "profit": "منافع", "loss": "خسارہ", "cash": "نقد",
    "budget": "بجٹ", "plan": "منصوبہ", "risk": "خطرہ", "assumption": "مفروضہ", "test": "آزمائش",
    "learn": "سیکھنا", "iterate": "دہرانا", "feedback": "رائے", "interview": "بات چیت",
    "prototype": "نمونہ", "minimum": "کم سے کم", "viable": "قابلِ کار", "launch": "آغاز",
    "beachhead": "پہلی چوکی", "segment": "حصہ", "niche": "تنگ منڈی", "competitor": "حریف",
    "advantage": "برتری", "channel": "راستہ", "partner": "ساتھی", "supplier": "سپلائر",
    "regulation": "ضابطہ", "license": "لائسنس", "tax": "ٹیکس", "contract": "معاہدہ",
    "pitch": "پیشکش", "slide": "سلائیڈ", "story": "کہانی", "ask": "مانگ", "offer": "پیشکش",
    "equity": "حصص", "debt": "قرض", "grant": "گرانٹ", "bootstrapping": "اپنے وسائل",
    "valuation": "قیمت لگانا", "dilution": "حصہ پتلا ہونا", "cap": "حد", "safe": "محفوظ",
    "term": "اصطلاح", "terms": "اصطلاحات", "sheet": "ورق", "due": "واجب", "diligence": "جانچ",
    "milestone": "سنگ میل", "roadmap": "راستہ نقشہ", "metric": "پیمائش", "kpi": "اشاریہ",
    "retention": "رہنا", "churn": "چھوڑ جانا", "acquisition": "حاصل کرنا", "activation": "چالو",
    "referral": "حوالہ", "viral": "پھیلتا", "growth": "بڑھوتری", "scale": "پیمانہ بڑھانا",
    "unit": "اکائی", "economics": "معیشت", "margin": "حاشیہ", "lifetime": "زندگی",
    "payback": "واپسی", "burn": "خرچ کی رفتار", "runway": "باقی وقت", "pivot": "موڑ",
    "persevere": "ڈٹے رہنا", "hypothesis": "مفروضہ", "experiment": "تجربہ", "evidence": "ثبوت",
    "lesson": "سبق", "journal": "روزنامچہ", "reflect": "سوچنا", "improve": "بہتر کرنا",
    "habit": "عادت", "practice": "مشق", "drill": "مشق", "recall": "یاد", "forget": "بھول",
    "spacing": "فاصلہ", "interleaving": "ملانا", "retrieval": "نکالنا", "elaboration": "وضاحت",
    "concrete": "ٹھوس", "abstract": "مجرد", "example": "مثال", "non-example": "جو مثال نہیں",
    "define": "تعریف", "explain": "وضاحت", "apply": "لگائیں", "analyse": "تجزیہ", "analyze": "تجزیہ",
    "evaluate": "جانچ", "create": "تخلیق", "remember": "یاد", "understand": "سمجھ",
    "diagram": "خاکہ", "redraw": "دوبارہ بنائیں", "label": "نشان", "annotate": "حاشیہ",
    "trace": "نشان لگائیں", "closed": "بند", "open": "کھلا", "book": "کتاب", "notes": "نوٹس",
    "aloud": "زبانی", "written": "تحریری", "oral": "زبانی", "marks": "نمبر", "rubric": "معیار",
    "checkpoint": "جانچ پڑتال", "repair": "مرمت", "mock": "نقلی امتحان", "blitz": "تیز دہرائی",
    "golden": "سنہری", "card": "کارڈ", "session": "نشست", "tutor": "استاد", "student": "طالب علم",
    "today": "آج", "yesterday": "کل", "tomorrow": "کل", "week": "ہفتہ", "hour": "گھنٹہ",
    "minute": "منٹ", "block": "بلاک", "homework": "گھر کا کام", "answer": "جواب", "key": "کلید",
    "list": "فہرست", "weak": "کمزور", "strong": "مضبوط", "revise": "دہرائیں", "tick": "نشان",
    "progress": "پیش رفت", "tracker": "ٹریکر", "complete": "مکمل", "incomplete": "ادھورا",
    "behind": "پیچھے", "ahead": "آگے", "schedule": "نظام الاوقات", "break": "وقفہ", "rest": "آرام",
    "sleep": "نیند", "phone": "فون", "room": "کمرہ", "desk": "میز", "copy": "کاپی", "pen": "قلم",
    "ruler": "پیمانہ", "pencil": "پنسل", "eraser": "ربڑ", "notebook": "کاپی", "folder": "فولڈر",
    "page": "صفحہ", "margin": "حاشیہ", "heading": "سرخی", "bullet": "نکتہ", "number": "نمبر",
    "underline": "لکیر", "highlight": "نمایاں", "box": "خانہ", "arrow": "تیر", "caption": "عنوان",
    "source": "ماخذ", "as": "جیسے", "printed": "چھپا", "exactly": "جوں کا توں", "do": "کریں",
    "does": "کرتا ہے", "did": "کیا", "done": "ہوا", "doing": "کرنا", "be": "ہونا", "been": "رہا",
    "being": "ہوتا", "am": "ہوں", "is": "ہے", "are": "ہیں", "was": "تھا", "were": "تھے",
    "will": "گا", "would": "گا", "shall": "گا", "can": "سکتا ہے", "could": "سکتا تھا",
    "may": "سکتا ہے", "might": "شاید", "must": "ضروری", "should": "چاہیے", "ought": "چاہیے",
    "have": "ہے", "has": "ہے", "had": "تھا", "having": "رکھتے ہوئے", "get": "حاصل", "gets": "حاصل کرتا ہے",
    "got": "ملا", "make": "بناؤ", "take": "لو", "takes": "لیتا ہے", "took": "لیا", "give": "دو",
    "put": "رکھو", "set": "رکھو", "let": "دو", "keep": "رکھو", "turn": "موڑو", "move": "ہلاؤ",
    "go": "جاؤ", "goes": "جاتا ہے", "come": "آؤ", "comes": "آتا ہے", "bring": "لاؤ", "brought": "لایا",
    "carry": "لے جانا", "hold": "تھامنا", "drop": "گرا دینا", "pick": "چننا", "place": "رکھنا",
    "fill": "بھرنا", "cover": "ڈھانپنا", "hide": "چھپانا", "reveal": "ظاہر", "display": "دکھانا",
    "present": "پیش", "introduce": "متعارف", "conclude": "نتیجہ", "summarise": "خلاصہ",
    "summarize": "خلاصہ", "outline": "خاکہ", "highlight": "نمایاں", "emphasise": "زور",
    "emphasize": "زور", "note": "نوٹ", "remember": "یاد", "forget": "بھول", "confuse": "خلط",
    "confusion": "خلط", "mistake": "غلطی", "trap": "پھندا", "trick": "چال", "common": "عام",
    "students": "طلبہ", "often": "اکثر", "think": "سوچتے ہیں", "thinks": "سوچتا ہے",
    "thought": "سوچا", "believe": "یقین", "assume": "مان لینا", "suppose": "فرض",
    "imagine": "تصور", "consider": "غور", "discuss": "بحث", "discussion": "بحث",
    "ask": "پوچھیں", "asks": "پوچھتا ہے", "asked": "پوچھا", "tell": "بتائیں", "told": "بتایا",
    "say": "کہیں", "says": "کہتا ہے", "said": "کہا", "speak": "بولیں", "speech": "تقریر",
    "talk": "بات", "listen": "سنیں", "hear": "سننا", "look": "دیکھو", "watch": "دیکھو",
    "see": "دیکھنا", "notice": "دھیان", "observe": "مشاہدہ", "measure": "ناپنا", "count": "گننا",
    "calculate": "حساب", "compute": "حساب", "estimate": "اندازہ", "approximate": "تقریباً",
    "round": "گول کرنا", "check": "جانچ", "verify": "تصدیق", "prove": "ثبوت", "proof": "ثبوت",
    "show": "دکھانا", "demonstrate": "دکھانا", "illustrate": "مثال سے", "sketch": "خاکہ",
    "draw": "کھینچنا", "redraw": "دوبارہ کھینچنا", "copy": "نقل", "trace": "ٹریس", "plot": "پلاٹ",
    "mark": "نشان", "label": "لیبل", "shade": "رنگ", "colour": "رنگ", "highlight": "نمایاں",
    "circle": "گول", "underline": "لکیر", "box": "خانہ", "tick": "ٹک", "cross": "کراس",
    "correct": "درست", "incorrect": "غلط", "right": "صحیح", "wrong": "غلط", "true": "سچ",
    "false": "جھوٹ", "yes": "ہاں", "no": "نہ", "maybe": "شاید", "unknown": "نامعلوم",
    "given": "دیا گیا", "find": "نکالو", "hence": "لہذا", "thus": "پس", "therefore": "اس لیے",
    "so": "تو", "because": "کیونکہ", "since": "چونکہ", "although": "حالانکہ", "however": "مگر",
    "but": "لیکن", "and": "اور", "or": "یا", "nor": "نہ", "yet": "پھر بھی", "also": "بھی",
    "too": "بھی", "as": "جیسا", "well": "اچھا", "just": "صرف", "only": "صرف", "even": "بھی",
    "still": "اب بھی", "already": "پہلے ہی", "yet": "ابھی", "again": "پھر", "once": "ایک بار",
    "twice": "دو بار", "always": "ہمیشہ", "never": "کبھی نہیں", "sometimes": "کبھی",
    "usually": "اکثر", "often": "اکثر", "rarely": "شاذ", "seldom": "کم", "frequently": "بار بار",
    "here": "یہاں", "there": "وہاں", "where": "جہاں", "when": "جب", "while": "جبکہ",
    "before": "پہلے", "after": "بعد", "during": "دوران", "until": "تک", "since": "سے",
    "now": "اب", "then": "پھر", "soon": "جلد", "later": "بعد", "early": "جلدی", "late": "دیر",
    "today": "آج", "tomorrow": "آنے والا کل", "yesterday": "گزرا کل", "daily": "روزانہ",
    "above": "اوپر", "below": "نیچے", "over": "پر", "under": "تلے", "inside": "اندر",
    "outside": "باہر", "between": "درمیان", "among": "درمیان", "across": "پار", "along": "ساتھ",
    "through": "کے پار", "around": "گرد", "near": "قریب", "far": "دور", "left": "بائیں",
    "right": "دائیں", "front": "آگے", "back": "پیچھے", "top": "اوپر", "bottom": "نیچے",
    "middle": "بیچ", "side": "طرف", "edge": "کنارہ", "corner": "کونا", "center": "درمیان",
    "centre": "درمیان", "north": "شمال", "south": "جنوب", "east": "مشرق", "west": "مغرب",
    "up": "اوپر", "down": "نیچے", "in": "اندر", "out": "باہر", "on": "پر", "off": "بند",
    "into": "اندر", "onto": "پر", "from": "سے", "to": "کو", "towards": "کی طرف", "toward": "کی طرف",
    "of": "کا", "for": "کے لیے", "with": "کے ساتھ", "without": "کے بغیر", "by": "کے ذریعے",
    "about": "کے بارے", "against": "کے خلاف", "between": "کے درمیان", "among": "کے درمیان",
    "within": "کے اندر", "upon": "پر", "per": "فی", "via": "کے راستے", "versus": "بمقابلہ",
    "vs": "بمقابلہ", "etc": "وغیرہ", "eg": "مثلاً", "ie": "یعنی", "approx": "تقریباً",
    "mr": "مسٹر", "mrs": "مسز", "dr": "ڈاکٹر", "prof": "پروفیسر", "fig": "شکل", "eq": "مساوات",
    "no": "نمبر", "vol": "جلد", "pp": "صفحات", "ed": "ایڈیشن", "ch": "باب", "sec": "حصہ",
    "ans": "جواب", "q": "سوال",     "a": "الف", "b": "ب", "c": "ج", "d": "د",
}

# Later duplicate keys in the dict above must not replace these tutor forms.
LEX.update({
    "is": "ہے", "are": "ہیں", "was": "تھا", "were": "تھے", "be": "ہونا",
    "has": "رکھتا ہے", "have": "رکھتے ہیں", "had": "رکھتا تھا",
    "do": "کرتا ہے", "does": "کرتا ہے", "did": "کیا",
    "can": "سکتا ہے", "could": "سکتا تھا", "should": "چاہیے", "must": "ضروری ہے",
    "use": "استعمال", "uses": "استعمال کرتا ہے", "used": "استعمال ہوتا ہے",
    "change": "بدلتا ہے", "changes": "بدلتے ہیں", "changed": "بدل گیا",
    "mean": "مطلب", "means": "مطلب ہے", "called": "کہلاتا ہے",
    "take": "لیتا ہے", "takes": "لیتا ہے", "make": "بناتا ہے", "makes": "بناتا ہے",
    "give": "دیتا ہے", "gives": "دیتا ہے", "show": "دکھاتا ہے", "shows": "دکھاتا ہے",
    "work": "کام", "works": "کام کرتا ہے", "need": "ضرورت", "needs": "ضرورت ہے",
    "not": "نہیں", "and": "اور", "or": "یا", "but": "مگر", "if": "اگر", "so": "اس لیے",
    "because": "کیونکہ", "when": "جب", "then": "پھر", "with": "کے ساتھ", "from": "سے",
    "for": "کے لیے", "this": "یہ", "that": "کہ", "it": "یہ", "they": "وہ", "them": "انہیں",
    "two": "دو", "one": "ایک", "three": "تین", "four": "چار", "all": "سب", "any": "کوئی بھی",
    "each": "ہر", "every": "ہر", "only": "صرف", "also": "بھی", "very": "بہت",
    "value": "قدر", "values": "قدریں", "number": "عدد", "numbers": "اعداد",
    "name": "نام", "time": "وقت", "height": "قد", "water": "پانی", "temperature": "درجہ حرارت",
    "student": "طالب علم", "students": "طلبہ", "example": "مثال", "examples": "مثالیں",
    "quantity": "مقدار", "quantities": "مقداریں", "separate": "الگ", "countable": "گنتی کے قابل",
    "items": "چیزیں", "item": "چیز", "level": "سطح", "levels": "سطحیں", "clear": "واضح",
    "small": "معمولی", "reliable": "قابل اعتماد", "accurate": "درست", "easy": "آسان",
    "computer": "کمپیوٹر", "computers": "کمپیوٹر", "programmable": "پروگرام کے قابل",
    "door": "دروازہ", "lock": "تالا", "locks": "تالے", "opens": "کھلتا ہے", "open": "کھلا",
    "unlocked": "کھلے", "room": "کمرہ", "enter": "داخل ہونا", "light": "روشنی", "dark": "اندھیرا",
    "switch": "سوئچ", "alarm": "الارم", "front": "آگے", "back": "پیچھے", "button": "بٹن",
    "symbol": "علامت", "operation": "عمل", "operations": "اعمال", "performs": "انجام دیتا ہے",
    "perform": "انجام دیتا ہے", "circuit": "سرکٹ", "circuits": "سرکٹ", "rule": "اصول",
    "signal": "سگنل", "signals": "سگنل", "wave": "لہر", "smooth": "ہموار", "noise": "شور",
    "disturbance": "خلل", "disturbances": "خلل", "kind": "قسم", "better": "بہتر", "why": "کیوں",
    "which": "کون سا", "what": "کیا", "how": "کیسے", "where": "کہاں", "who": "کون",
    "answer": "جواب", "question": "سوال", "page": "صفحہ", "book": "کتاب", "figure": "شکل",
    "diagram": "خاکہ", "chart": "چارٹ", "note": "نوٹ", "lesson": "سبق", "unit": "یونٹ",
    "teacher": "استاد", "teachers": "اساتذہ", "approach": "طریقہ", "activity": "سرگرمی",
    "misconception": "غلط فہمی", "analogy": "تشبیہ", "stairs": "سیڑھیاں", "ramp": "ڈھلوان",
    "fixed": "مقررہ", "heights": "بلندیاں", "copy": "نقل", "copying": "نقل", "quality": "معیار",
    "loss": "کمی", "foundation": "بنیاد", "developed": "بنایا", "mathematician": "ریاضی دان",
    "english": "انگریزی", "called": "کہلاتا ہے", "both": "دونوں", "either": "کوئی ایک",
    "same": "یکساں", "different": "مختلف", "real": "روزمرہ", "life": "زندگی",
    "store": "ذخیرہ کرتا ہے", "stores": "ذخیرہ کرتا ہے", "everything": "ہر چیز",
    "pattern": "نمونہ", "patterns": "نمونے", "multiply": "ضرب دیں", "add": "جمع کریں",
    "power": "طاقت", "decimal": "اعشاری", "convert": "بدلیں", "read": "پڑھیں",
    "group": "گروہ", "groups": "گروہ", "row": "قطار", "rows": "قطاریں", "column": "کالم",
    "possible": "ممکن", "exactly": "بالکل", "more": "زیادہ", "than": "سے", "into": "میں",
    "about": "کے بارے میں", "without": "کے بغیر", "between": "کے درمیان", "after": "کے بعد",
    "before": "سے پہلے", "during": "کے دوران", "through": "کے ذریعے", "over": "پر", "under": "تلے",
    "new": "نیا", "old": "پرانا", "first": "پہلا", "next": "اگلا", "last": "آخری",
    "important": "اہم", "common": "عام", "simple": "سادہ", "hard": "مشکل", "fast": "تیز",
    "slow": "آہستہ", "high": "اونچا", "low": "کم", "full": "مکمل", "empty": "خالی",
    "correct": "درست", "wrong": "غلط", "true": "سچ", "false": "جھوٹ",
    "people": "لوگ", "person": "شخص", "user": "صارف", "users": "صارفین", "device": "آلہ",
    "devices": "آلات", "program": "پروگرام", "code": "کوڈ", "screen": "سکرین", "text": "متن",
    "information": "معلومات", "result": "نتیجہ", "results": "نتائج", "problem": "مسئلہ",
    "solution": "حل", "method": "طریقہ", "process": "عمل", "step": "قدم", "steps": "قدم",
    "today": "آج", "day": "دن", "week": "ہفتہ", "hour": "گھنٹہ", "minute": "منٹ",
    "school": "اسکول", "college": "کالج", "phone": "فون", "home": "گھر", "paper": "کاغذ",
    "memory": "یاد", "understand": "سمجھیں", "explain": "وضاحت کریں", "define": "تعریف کریں",
    "describe": "بیان کریں", "compare": "موازنہ کریں", "calculate": "حساب کریں",
    "draw": "بنائیں", "write": "لکھیں", "keep": "رکھیں", "help": "مدد", "try": "کوشش کریں",
    "check": "جانچیں", "test": "جانچ", "error": "غلطی", "errors": "غلطیاں", "fix": "درست کریں",
    "build": "بنائیں", "create": "بنائیں", "design": "ڈیزائن", "plan": "منصوبہ",
    "learn": "سیکھیں", "learning": "سیکھنا", "teach": "پڑھائیں", "practice": "مشق",
    "example": "مثال", "feature": "خصوصیت", "features": "خصوصیات", "part": "حصہ", "parts": "حصے",
    "whole": "پورا", "side": "طرف", "end": "آخر", "start": "شروع", "stop": "رکیں",
    "always": "ہمیشہ", "never": "کبھی نہیں", "often": "اکثر", "usually": "عموماً",
    "here": "یہاں", "there": "وہاں", "now": "اب", "again": "دوبارہ", "still": "اب بھی",
    "just": "صرف", "well": "اچھی طرح", "way": "طریقہ", "case": "صورت", "point": "نکتہ",
    "line": "سطر", "word": "لفظ", "words": "الفاظ", "sentence": "جملہ", "meaning": "مطلب",
    "definition": "تعریف", "idea": "خیال", "reason": "وجہ", "effect": "اثر", "cause": "سبب",
    "goal": "مقصد", "purpose": "مقصد", "task": "کام", "tasks": "کام", "tool": "آلہ", "tools": "آلات",
    "machine": "مشین", "software": "سافٹ ویئر", "hardware": "ہارڈ ویئر", "internet": "انٹرنیٹ",
    "website": "ویب سائٹ", "online": "آن لائن", "message": "پیغام", "email": "ای میل",
    "security": "سلامتی", "privacy": "رازداری", "safe": "محفوظ", "risk": "خطرہ", "cost": "لاگت",
    "free": "مفت", "large": "بڑا", "long": "لمبا", "short": "مختصر", "good": "اچھا", "bad": "برا",
    "best": "بہترین", "same": "وہی", "other": "دوسرا", "another": "ایک اور", "such": "ایسا",
    "like": "جیسے", "into": "میں", "over": "پر", "under": "تلے", "between": "کے درمیان",
    "without": "بغیر", "within": "اندر", "across": "پار", "through": "سے", "against": "خلاف",
    "during": "دوران", "until": "جب تک", "while": "جبکہ", "since": "چونکہ", "therefore": "اس لیے",
    "however": "تاہم", "including": "بشمول", "except": "سوائے", "percent": "فیصد", "percentage": "فیصد",
    "total": "کل", "sum": "مجموع", "average": "اوسط", "count": "گنتی", "size": "سائز",
    "order": "ترتیب", "group": "گروہ", "share": "بانٹیں", "send": "بھیجیں", "save": "محفوظ کریں",
    "choose": "چنیں", "select": "منتخب کریں", "update": "تازہ کریں", "search": "تلاش", "sort": "ترتیب",
    "filter": "چھانٹ", "link": "ربط", "source": "ماخذ", "version": "ورژن", "title": "عنوان",
    "label": "لیبل", "labels": "لیبل", "row": "قطار", "cell": "خانہ", "box": "خانہ",
    "report": "رپورٹ", "image": "تصویر", "video": "ویڈیو", "document": "دستاویز",
    "user": "صارف", "customer": "گاہک", "people": "لوگ", "family": "خاندان", "age": "عمر",
    "date": "تاریخ", "year": "سال", "month": "مہینہ", "daily": "روزانہ", "weekly": "ہفتہ وار",
    "skill": "مہارت", "skills": "مہارتیں", "knowledge": "علم", "information": "معلومات",
    "rule": "قاعدہ", "rules": "قواعد", "law": "قانون", "right": "درست", "left": "بائیں",
    "public": "عوامی", "private": "نجی", "local": "مقامی", "global": "عالمی", "personal": "ذاتی",
    "social": "سماجی", "ethical": "اخلاقی", "legal": "قانونی", "fair": "منصفانہ",
    "benefit": "فائدہ", "advantage": "فائدہ", "disadvantage": "نقصان", "limit": "حد",
    "decision": "فیصلہ", "option": "اختیار", "options": "اختیارات", "difference": "فرق",
    "similar": "مشابہ", "match": "میل", "suitable": "موزوں", "required": "لازمی",
    "available": "دستیاب", "useful": "مفید", "effective": "موثر", "efficient": "کارگر",
    "performance": "کارکردگی", "strong": "مضبوط", "weak": "کمزور", "positive": "مثبت",
    "negative": "منفی", "zero": "صفر", "equal": "برابر", "greater": "بڑا", "less": "کم",
    "increase": "بڑھنا", "decrease": "گھٹنا", "remove": "ہٹائیں", "replace": "بدل دیں",
    "collect": "جمع کریں", "prepare": "تیار کریں", "complete": "مکمل", "missing": "غائب",
    "success": "کامیابی", "failure": "ناکامی", "repeat": "دہرائیں", "continue": "جاری رکھیں",
    "watch": "دیکھیں", "observe": "مشاہدہ", "focus": "توجہ", "attention": "توجہ",
    "warning": "انتباہ", "critical": "نازک", "essential": "لازمی", "basic": "بنیادی",
    "advanced": "اعلیٰ", "finally": "آخر میں", "later": "بعد میں", "soon": "جلد",
    "automatically": "خود بخود", "manually": "ہاتھ سے", "valid": "جائز", "invalid": "ناجائز",
    "current": "موجودہ", "previous": "پچھلا", "following": "اگلا", "known": "معلوم",
    "unknown": "نامعلوم", "given": "دیا گیا", "shown": "دکھایا گیا", "printed": "چھپا ہوا",
    "written": "لکھا ہوا", "based": "بنیاد", "related": "متعلق", "shared": "مشترکہ",
    "some": "کچھ", "none": "کوئی نہیں", "nothing": "کچھ نہیں", "something": "کچھ",
    "everything": "سب کچھ", "many": "بہت", "much": "بہت", "few": "چند", "several": "کئی",
    "whole": "سارا", "rest": "باقی", "others": "دوسرے", "together": "مل کر",
    "above": "اوپر", "below": "نیچے", "inside": "اندر", "outside": "باہر", "near": "قریب",
    "far": "دور", "middle": "بیچ", "top": "اوپر", "bottom": "نیچے", "center": "درمیان",
    "centre": "درمیان", "up": "اوپر", "down": "نیچے", "out": "باہر", "off": "بند",
    "yes": "ہاں", "no": "نہیں", "please": "براہ کرم", "etc": "وغیرہ",
})

PHRASES = [
    ("all use it", "سب اسے استعمال کرتے ہیں"),
    ("can take any value in a range", "کسی حد میں کوئی بھی قدر لے سکتی ہیں"),
    ("no loss of quality when copying", "نقل میں معیار کم نہیں ہوتا"),
    ("easy to design and programmable", "ڈیزائن میں آسان اور پروگرام کے قابل"),
    ("two clear levels", "دو واضح سطحیں"),
    ("do not change", "نہیں بدلتے"),
    ("does not change", "نہیں بدلتا"),
    ("separate, countable items", "الگ اور گنتی کے قابل چیزیں"),
    ("separate, countable values", "الگ اور گنتی کے قابل قدریں"),
    ("students in a class", "جماعت کے طلبہ"),
    ("cars in a car park", "پارکنگ کی گاڑیاں"),
    ("books on a shelf", "شیلف کی کتابیں"),
    ("water temperature", "پانی کا درجہ حرارت"),
    ("temperature of water", "پانی کا درجہ حرارت"),
    ("height of a person", "انسان کا قد"),
    ("any value in a range", "کسی حد میں کوئی بھی قدر"),
    ("only two values", "صرف دو قدریں"),
    ("no loss of quality", "نقل میں معیار کم نہیں ہوتا"),
    ("when copying", "نقل کرتے وقت"),
    ("easy to design", "ڈیزائن میں آسان"),
    ("traffic lights", "ٹریفک کی بتیاں"),
    ("digital watches", "ڈیجیٹل گھڑیاں"),
    ("digital cameras", "ڈیجیٹل کیمرے"),
    ("digital watch", "ڈیجیٹل گھڑی"),
    ("for example", "مثال کے طور پر"),
    ("for instance", "مثلاً"),
    ("such as", "جیسے"),
    ("as well as", "اور"),
    ("a lot of", "بہت"),
    ("lots of", "بہت"),
    ("in other words", "دوسرے لفظوں میں"),
    ("step by step", "قدم بہ قدم"),
    ("step-by-step", "قدم بہ قدم"),
    ("at least", "کم از کم"),
    ("at most", "زیادہ سے زیادہ"),
    ("according to", "کے مطابق"),
    ("based on", "کی بنیاد پر"),
    ("in order to", "تاکہ"),
    ("so that", "تاکہ"),
    ("as a result", "نتیجے میں"),
    ("on the other hand", "دوسری طرف"),
    ("each other", "ایک دوسرے"),
    ("one another", "ایک دوسرے"),
    ("as soon as", "جیسے ہی"),
    ("in front of", "کے سامنے"),
    ("a number of", "کئی"),
    ("the number of", "کی تعداد"),
    ("in terms of", "کے لحاظ سے"),
    ("in the form of", "کی شکل میں"),
    ("is used to", "کے لیے استعمال ہوتا ہے"),
    ("are used to", "کے لیے استعمال ہوتے ہیں"),
    ("used to", "استعمال ہوتا ہے"),
    ("able to", "کے قابل"),
    ("known as", "جسے کہتے ہیں"),
    ("referred to as", "جسے کہا جاتا ہے"),
    ("as follows", "درج ذیل ہے"),
    ("as shown", "جیسا کہ دکھایا گیا ہے"),
    ("make sure", "یقینی بنائیں"),
    ("keep in mind", "یاد رکھیں"),
    ("do not", "مت"),
    ("does not", "نہیں"),
    ("did not", "نہیں"),
    ("cannot", "نہیں کر سکتا"),
    ("can not", "نہیں کر سکتا"),
    ("there is", "موجود ہے"),
    ("there are", "موجود ہیں"),
    ("it is", "یہ"),
    ("this is", "یہ"),
    ("these are", "یہ"),
    ("that is", "یعنی"),
    ("which is", "جو ہے"),
    ("which are", "جو ہیں"),
    ("will be", "ہو گا"),
    ("can be", "ہو سکتا ہے"),
    ("should be", "ہونا چاہیے"),
    ("must be", "ہونا ضروری ہے"),
    ("may be", "ہو سکتا ہے"),
    ("is not", "نہیں"),
    ("are not", "نہیں"),
    ("was not", "نہیں تھا"),
    ("were not", "نہیں تھے"),
    ("more than", "سے زیادہ"),
    ("less than", "سے کم"),
    ("greater than", "سے بڑا"),
    ("equal to", "کے برابر"),
    ("same as", "جیسا"),
    ("different from", "سے مختلف"),
    ("because of", "کی وجہ سے"),
    ("instead of", "کی بجائے"),
    ("out of", "میں سے"),
    ("part of", "کا حصہ"),
    ("type of", "کی قسم"),
    ("kind of", "کی قسم"),
    ("number of", "کی تعداد"),
    ("set of", "کا مجموعہ"),
    ("list of", "کی فہرست"),
    ("a pair of", "ایک جوڑا"),
    ("one or more", "ایک یا زیادہ"),
    ("exactly one", "صرف ایک"),
    ("if and only if", "صرف اسی صورت میں جب"),
    ("as long as", "جب تک"),
    ("and so on", "وغیرہ"),
    ("so on", "وغیرہ"),
    ("of course", "یقیناً"),
    ("for this reason", "اس وجہ سے"),
    ("in addition", "اس کے علاوہ"),
    ("in fact", "دراصل"),
    ("in practice", "عمل میں"),
    ("in theory", "نظریے میں"),
    ("a few", "چند"),
    ("a little", "تھوڑا"),
    ("real life", "روزمرہ زندگی"),
    ("real-life", "روزمرہ"),
    ("from memory", "یاد سے"),
    ("on paper", "کاغذ پر"),
    ("closed book", "بند کتاب"),
    ("closed-book", "بند کتاب"),
    ("for students", "طلبہ کے لیے"),
    ("for teachers", "اساتذہ کے لیے"),
    ("in this lesson", "اس سبق میں"),
    ("in this unit", "اس یونٹ میں"),
    ("per cent", "فیصد"),
    ("common misconception", "عام غلط فہمی"),
    ("words to know", "اہم الفاظ"),
    ("check yourself", "خود جانچ"),
    ("maths corner", "ریاضی کا گوشہ"),
    ("try it", "خود کر کے دیکھیں"),
    ("did you know", "کیا آپ جانتے ہیں"),
    ("teacher's note", "استاد کا نوٹ"),
    ("answer key", "جواب کی کلید"),
    ("no fixed steps", "مقررہ قدم نہیں"),
    ("flows smoothly", "ہموار بہتی ہے"),
    ("resists noise", "شور کا مقابلہ کرتا ہے"),
    ("easily disturbed", "آسانی سے متاثر"),
    ("small disturbances", "معمولی خلل"),
    ("two clear levels", "دو واضح سطحیں"),
    ("fixed heights", "مقررہ بلندیاں"),
    ("any height", "کوئی بھی بلندی"),
    ("square wave", "مربع لہر"),
    ("smooth wave", "ہموار لہر"),
    ("human voice", "انسانی آواز"),
    ("power of 2", "2 کی طاقت"),
    ("power of two", "دو کی طاقت"),
    ("truth table", "{truth table}"),
    ("logic gate", "{logic gate}"),
    ("logic gates", "{logic gates}"),
]
PHRASES = sorted(PHRASES, key=lambda kv: len(kv[0]), reverse=True)
PHRASE_RE = re.compile("|".join(re.escape(k) for k, _ in PHRASES), re.I)
PHRASE_MAP = {k.lower(): v for k, v in PHRASES}

PREP = {
    "in": "میں", "on": "پر", "at": "پر", "for": "کے لیے", "with": "کے ساتھ", "from": "سے",
    "by": "سے", "of": "کا", "into": "میں", "about": "کے بارے میں", "without": "کے بغیر",
    "between": "کے درمیان", "over": "پر", "under": "کے نیچے", "before": "سے پہلے",
    "after": "کے بعد", "during": "کے دوران", "through": "کے ذریعے", "against": "کے خلاف",
    "across": "کے پار", "within": "کے اندر", "per": "فی", "than": "سے", "via": "کے راستے",
    "upon": "پر", "onto": "پر", "off": "سے", "into": "میں",
}
SKIP = {"the", "a", "an"}
COPULA = {"ہے", "ہیں", "تھا", "تھے", "تھی", "ہوں", "ہو"}
STOP_NP = SKIP | set(PREP) | {
    "and", "or", "but", "if", "when", "that", "which", "who", "to", "not", "so", "because",
    "is", "are", "was", "were", "be", "been", "has", "have", "had", "do", "does", "did",
    "can", "could", "should", "must", "may", "will", "would",
}
INF = {
    "learn": "سیکھنے", "read": "پڑھنے", "write": "لکھنے", "use": "استعمال کرنے",
    "take": "لے", "store": "ذخیرہ", "change": "بدل", "make": "بنا", "give": "دے",
    "show": "دکھا", "keep": "رکھ", "find": "ڈھونڈ", "help": "مدد", "work": "کام",
    "make": "بنانے", "find": "تلاش کرنے", "show": "دکھانے", "explain": "سمجھانے",
    "compare": "موازنہ کرنے", "draw": "بنانے", "calculate": "حساب کرنے", "store": "ذخیرہ کرنے",
    "send": "بھیجنے", "check": "جانچنے", "avoid": "بچنے", "understand": "سمجھنے",
    "remember": "یاد رکھنے", "convert": "بدلنے", "sort": "ترتیب دینے", "search": "تلاش کرنے",
    "build": "بنانے", "create": "بنانے", "design": "ڈیزائن کرنے", "solve": "حل کرنے",
    "describe": "بیان کرنے", "identify": "پہچاننے", "copy": "نقل کرنے", "redraw": "دوبارہ بنانے",
    "protect": "بچانے", "improve": "بہتر بنانے", "measure": "ناپنے", "predict": "بتانے",
    "collect": "جمع کرنے", "analyse": "تجزیہ کرنے", "analyze": "تجزیہ کرنے",
    "represent": "ظاہر کرنے", "perform": "انجام دینے", "connect": "جوڑنے",
}

VERB_END = {
    "uses": "استعمال کرتا ہے", "use": "استعمال کرتے ہیں", "has": "رکھتا ہے", "have": "رکھتے ہیں",
    "stores": "ذخیرہ کرتا ہے", "store": "ذخیرہ کرتے ہیں", "shows": "دکھاتا ہے", "show": "دکھاتے ہیں",
    "gives": "دیتا ہے", "give": "دیتے ہیں", "needs": "چاہتا ہے", "need": "چاہتے ہیں",
    "makes": "بناتا ہے", "make": "بناتے ہیں", "performs": "انجام دیتا ہے", "perform": "انجام دیتے ہیں",
    "contains": "رکھتا ہے", "contain": "رکھتے ہیں", "includes": "شامل کرتا ہے", "include": "شامل کرتے ہیں",
    "requires": "مانگتا ہے", "require": "مانگتے ہیں", "provides": "دیتا ہے", "provide": "دیتے ہیں",
    "produces": "بناتا ہے", "produce": "بناتے ہیں", "represents": "ظاہر کرتا ہے",
    "represent": "ظاہر کرتے ہیں", "allows": "اجازت دیتا ہے", "allow": "اجازت دیتے ہیں",
    "helps": "مدد کرتا ہے", "help": "مدد کرتے ہیں", "keeps": "رکھتا ہے", "keep": "رکھتے ہیں",
    "changes": "بدلتا ہے", "change": "بدلتے ہیں", "follows": "مانتا ہے", "follow": "مانتے ہیں",
    "returns": "واپس کرتا ہے", "return": "واپس کرتے ہیں", "reads": "پڑھتا ہے", "read": "پڑھتے ہیں",
    "writes": "لکھتا ہے", "write": "لکھتے ہیں", "sends": "بھیجتا ہے", "send": "بھیجتے ہیں",
    "receives": "وصول کرتا ہے", "receive": "وصول کرتے ہیں", "supports": "سہارا دیتا ہے",
    "describes": "بیان کرتا ہے", "describe": "بیان کرتے ہیں", "explains": "سمجھاتا ہے",
    "explain": "سمجھاتے ہیں", "compares": "موازنہ کرتا ہے", "compare": "موازنہ کرتے ہیں",
    "calculates": "حساب کرتا ہے", "calculate": "حساب کرتے ہیں", "converts": "بدلتا ہے",
    "convert": "بدلتے ہیں", "combines": "ملاتا ہے", "combine": "ملاتے ہیں",
    "creates": "بناتا ہے", "create": "بناتے ہیں", "builds": "بناتا ہے", "build": "بناتے ہیں",
    "runs": "چلتا ہے", "run": "چلتے ہیں", "works": "کام کرتا ہے", "work": "کام کرتے ہیں",
    "means": "مطلب رکھتا ہے", "mean": "مطلب رکھتے ہیں",
}


def norm(text: str) -> str:
    text = PRIVATE.sub("", text)
    text = ARABIC.sub(" ", text)
    text = text.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    text = text.replace("{", "(").replace("}", ")")
    text = re.sub(r"\be\.g\.", " مثلاً ", text, flags=re.I)
    text = re.sub(r"\bi\.e\.", " یعنی ", text, flags=re.I)
    text = re.sub(r"\betc\.", " وغیرہ ", text, flags=re.I)
    text = re.sub(r"\bvs\.", " بمقابلہ ", text, flags=re.I)
    text = re.sub(r"\bfig\.", " شکل ", text, flags=re.I)
    text = re.sub(r"\bpp\.", " صفحات ", text, flags=re.I)
    text = re.sub(r"(?<![A-Za-z])[A-Za-z]\.(?=\s|$)", " ", text)
    text = re.sub(r"\b(\d{3,4})s\b", r"\1", text)
    text = re.sub(r"\s+", " ", text).strip(" ·|-–—")
    return text.strip()


def apply_phrases(text: str) -> str:
    def repl(match: re.Match) -> str:
        return PHRASE_MAP[match.group(0).lower()]
    return PHRASE_RE.sub(repl, text)


def _protect_piece(text: str) -> str:
    def caps(match: re.Match) -> str:
        word = match.group(0)
        return "{" + word + "}" if word in CAPS else word

    def term(match: re.Match) -> str:
        return "{" + match.group(0).strip() + "}"

    text = TERM_RE.sub(term, text)
    parts = re.split(r"(\{[^{}]*\})", text)
    return "".join(
        part if part.startswith("{") else re.sub(r"\b[A-Z][A-Z0-9/+-]{1,}\b", caps, part)
        for part in parts
    )


def protect_terms(text: str) -> str:
    parts = re.split(r"(\{[^{}]*\})", text)
    return "".join(part if part.startswith("{") else _protect_piece(part) for part in parts)


def tokenize(text: str) -> list[str]:
    return TOKEN.findall(text)


def tr_word(token: str) -> str:
    if token.startswith("{") or token.startswith("⟪"):
        return token
    if re.fullmatch(r"\d+(?:\.\d+)?", token):
        return token
    if not re.search(r"[A-Za-z]", token):
        return token
    low = token.lower().strip(".,;:!?()[]\"'")
    if low in SKIP:
        return ""
    if low in LEX:
        return LEX[low]
    if low in ALWAYS_SET:
        return "{" + token.strip(".,;:!?") + "}"
    return token


def take_np(tokens: list[str], start: int) -> tuple[list[str], int]:
    np: list[str] = []
    j = start
    while j < len(tokens) and len(np) < 4:
        t = tokens[j]
        low = t.lower().strip(".,;:!?")
        if t.startswith("{") or t.startswith("⟪"):
            np.append(t)
            j += 1
            continue
        if low in STOP_NP or low in LEX and low in {
            "is", "are", "was", "were", "has", "have", "do", "does", "can", "not"
        }:
            break
        if not re.search(r"[A-Za-z]", t) and not t.startswith("{"):
            break
        if low in SKIP:
            j += 1
            continue
        np.append(t)
        j += 1
        if t.endswith(",") or t.endswith("."):
            break
    return np, j


def translate_stream(text: str) -> str:
    tokens = tokenize(text)
    out: list[str] = []
    i = 0
    while i < len(tokens):
        t = tokens[i]
        low = t.lower().strip(".,;:!?()[]\"'")
        if t.startswith("{") or t.startswith("⟪"):
            out.append(t)
            i += 1
            continue
        if low in SKIP or low in {"the"}:
            i += 1
            continue
        if low in {"do", "does", "did"} and i + 2 < len(tokens) and tokens[i + 1].lower() == "not":
            out.append(tr_word(tokens[i + 2]))
            out.append("نہیں")
            i += 3
            continue
        if low == "not" and i + 1 < len(tokens) and re.search(r"[A-Za-z]", tokens[i + 1]):
            out.append(tr_word(tokens[i + 1]))
            out.append("نہیں")
            i += 2
            continue
        if low in {"can", "could", "should", "must", "may", "will"} and i + 1 < len(tokens):
            nxt = tokens[i + 1].lower().strip(".,;:")
            if nxt in INF or nxt in LEX:
                out.append(tr_word(tokens[i + 1]))
                out.append({
                    "can": "سکتا ہے", "could": "سکتا تھا", "should": "چاہیے",
                    "must": "ضروری ہے", "may": "سکتا ہے", "will": "گا",
                }[low])
                i += 2
                continue
        if low == "to" and i + 1 < len(tokens):
            nxt = tokens[i + 1].lower().strip(".,;:")
            if nxt in INF:
                out.append(INF[nxt])
                i += 2
                continue
        if low in PREP:
            np, nxt_i = take_np(tokens, i + 1)
            if np:
                if low == "of" and out:
                    prev = out.pop()
                    out.extend(tr_word(x) for x in np)
                    out.append("کا")
                    out.append(prev)
                else:
                    out.extend(tr_word(x) for x in np)
                    out.append(PREP[low])
                i = nxt_i
                continue
        piece = tr_word(t)
        if piece:
            out.append(piece)
        i += 1
    return " ".join(x for x in out if x)


PARTICIPLE = {
    "کرتا", "کرتی", "کرتے", "ہوتا", "ہوتی", "ہوتے", "دیتا", "دیتی", "دیتے",
    "سکتا", "سکتی", "سکتے", "رہتا", "رہتی", "رہتے", "چاہتا", "چاہتی", "چاہتے",
    "جاتا", "جاتی", "جاتے", "آتا", "آتی", "آتے", "کہلاتا", "کہلاتی", "کہلاتے",
}


def move_copula(text: str) -> str:
    # Move a lone ہے/ہیں to the end, but never pull it out of a verb such as "کرتا ہے".
    clauses = re.split(r"([،,;:])", text)
    moved = []
    for clause in clauses:
        if re.fullmatch(r"[،,;:]", clause or ""):
            moved.append(clause)
            continue
        toks = clause.split()
        indexes = [i for i, t in enumerate(toks) if t in COPULA]
        if len(indexes) == 1:
            i = indexes[0]
            prev = toks[i - 1] if i else ""
            if prev not in PARTICIPLE and i != len(toks) - 1:
                cop = toks.pop(i)
                if toks and re.search(r"[.?!۔؟]$", toks[-1]):
                    punct = toks[-1][-1]
                    toks[-1] = toks[-1][:-1]
                    toks.append(cop + punct)
                else:
                    toks.append(cop)
        moved.append(" ".join(toks))
    return " ".join(moved)


def polish(text: str) -> str:
    parts = re.split(r"(\{[^{}]*\})", text)
    cleaned = []
    for part in parts:
        if part.startswith("{"):
            cleaned.append(part)
            continue
        part = part.replace("·", " ")
        part = part.replace(",", "،")
        part = re.sub(r"\.\s*(ہے|ہیں)", r" \1", part)
        part = re.sub(r"\)\s*\.", ")", part)
        part = re.sub(r"\(\s*\)", "", part)
        part = re.sub(r"\s+([،۔؟:;])", r"\1", part)
        part = re.sub(r"،{2,}", "،", part)
        cleaned.append(part)
    text = "".join(cleaned)
    text = re.sub(r"\}\s*\.", "}", text)
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"(ہے)(?:\s+ہے)+", r"\1", text)
    text = re.sub(r"(ہیں)(?:\s+ہیں)+", r"\1", text)
    return text.strip(" ،")


def brace_latin(text: str) -> str:
    parts = re.split(r"(\{[^{}]+\}|⟪[^⟫]*⟫)", text)
    out = []
    for part in parts:
        if part.startswith("{") or part.startswith("⟪"):
            out.append(part)
            continue
        def wrap(match: re.Match) -> str:
            word = match.group(0).strip(".")
            if not re.search(r"[A-Za-z]", word):
                return match.group(0)
            return "{" + word + "}"
        out.append(LATIN_WORD.sub(wrap, part))
    text = "".join(out)
    text = text.replace("⟪", "(").replace("⟫", ")")
    text = re.sub(r"(?<![A-Za-z{])[A-Za-z]\.(?![A-Za-z}])", "", text)
    text = re.sub(r"\}\s+\{", "} {", text)
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\s+([،,.:;؟!۔])", r"\1", text)
    text = re.sub(r"\(\s+", "(", text)
    text = re.sub(r"\s+\)", ")", text)
    text = re.sub(r"\{\s+", "{", text)
    text = re.sub(r"\s+\}", "}", text)
    text = re.sub(r"\{([^{}]*)\}", lambda m: "{" + re.sub(r"\s+", " ", m.group(1)).strip() + "}" if m.group(1).strip() else "", text)
    return text.strip()


def structure(text: str) -> str | None:
    """Subject–object–verb shapes that should not be translated left to right."""
    m = re.match(
        r"^(?:give\s+)?(?:two|one|an|a)?\s*examples of (.+?) and (?:two|one)\s+of (.+)$",
        text, re.I,
    )
    if m:
        return polish(f"{tr(m.group(1))} کی مثالیں اور {tr(m.group(2))} کی مثالیں")
    m = re.match(r"^(?:two|one|an|a)?\s*examples of (.+)$", text, re.I)
    if m:
        return polish(f"{tr(m.group(1))} کی مثالیں")
    m = re.match(r"^([^,;:]{1,80}) deals with (.+)$", text, re.I)
    if m and guarded_left(m.group(1)):
        return polish(f"{tr(m.group(1))} {tr(m.group(2))} سے متعلق ہے")
    m = re.match(
        r"^([^,;:]{1,80}) (uses|has|stores|shows|gives|needs|makes|performs|contains|includes|allows|helps|keeps|changes|describes|explains|combines|creates|runs|works|means) (.+)$",
        text, re.I,
    )
    if m and guarded_left(m.group(1)) and m.group(2).lower() in VERB_END:
        verb = VERB_END[m.group(2).lower()]
        so = re.split(r",?\s+so\s+", m.group(3), maxsplit=1, flags=re.I)
        if len(so) == 2:
            return polish(f"{tr(m.group(1))} {tr(so[0])} {verb}، اس لیے {tr(so[1])}")
        return polish(f"{tr(m.group(1))} {tr(m.group(3))} {verb}")
    m = re.match(r"^([^,;:]{1,80}) (is|are) (.+)$", text, re.I)
    if m and guarded_left(m.group(1)) and m.group(1).lower() not in {"it", "this", "that", "there", "which", "who"}:
        cop = "ہیں" if m.group(2).lower() == "are" else "ہے"
        return polish(f"{tr(m.group(1))} {tr(m.group(3).rstrip('.'))} {cop}")
    return None


def tr(text: str) -> str:
    text = norm(text)
    if not text:
        return ""
    shaped = structure(text)
    if shaped:
        return shaped
    # Translate parenthetical asides first so they stay grouped.
    def paren(match: re.Match) -> str:
        return "⟪" + tr(match.group(1)) + "⟫"
    text = re.sub(r"\(([^()]*)\)", paren, text)
    text = apply_phrases(text)
    text = protect_terms(text)
    text = translate_stream(text)
    text = move_copula(text)
    return polish(brace_latin(text))


def end_mark(original: str, statement: str) -> str:
    statement = polish(statement).strip(" ۔.؟?")
    if not statement:
        return ""
    if original.rstrip().endswith("?"):
        return statement + "؟"
    return statement + "۔"


def guarded_left(left: str) -> bool:
    if len(left.split()) > 10:
        return False
    return re.search(r"\b(if|when|because|although|which|that|so)\b", left, re.I) is None


def urdish(text: str) -> str:
    original = norm(text)
    if not original or len(re.findall(r"[A-Za-z]", original)) < 2:
        return ""
    key = original.lower().rstrip(".!? ")

    called = re.split(r",?\s+called\s+", original, maxsplit=1, flags=re.I)
    if len(called) == 2 and len(called[0].split()) >= 3:
        left, right = called
        return end_mark(original, f"{tr(left)}، جنہیں {tr(right)} کہتے ہیں")

    patterns: list[tuple[str, str]] = [
        (r"^what (?:is|are) (.+?)\??$", "کیا"),
        (r"^what do(?:es)? (.+?)\??$", "کیا"),
        (r"^which (.+?)\??$", "کون سا"),
        (r"^why (.+?)\??$", "کیوں"),
        (r"^how many (.+?)\??$", "کتنے"),
        (r"^how much (.+?)\??$", "کتنا"),
        (r"^how (.+?)\??$", "کیسے"),
        (r"^when (.+?)\??$", "کب"),
        (r"^where (.+?)\??$", "کہاں"),
        (r"^who (.+?)\??$", "کون"),
    ]
    for rx, gloss in patterns:
        m = re.match(rx, key, re.I)
        if m:
            body = tr(m.group(1))
            if gloss == "کیا" and rx.startswith("^what (?:is"):
                return f"{body} کیا ہے؟"
            if gloss == "کتنے":
                return f"{body} کتنے ہیں؟"
            if gloss == "کون سا":
                return f"کون سا {body}؟"
            return f"{gloss}: {body}؟"

    m = re.match(r"^give (.+)$", key, re.I)
    if m:
        return end_mark(original, f"{tr(m.group(1))} دیں")
    m = re.match(r"^(define|explain|state|name|list|describe|convert|calculate|find|write|draw|compare) (.+)$", key, re.I)
    if m:
        verb = {
            "define": "تعریف کریں", "explain": "وضاحت کریں", "state": "بیان کریں",
            "name": "نام بتائیں", "list": "فہرست دیں", "describe": "بیان کریں",
            "convert": "تبدیل کریں", "calculate": "حساب کریں", "find": "نکالیں",
            "write": "لکھیں", "draw": "بنائیں", "compare": "موازنہ کریں",
        }[m.group(1).lower()]
        return end_mark(original, f"{tr(m.group(2))} {verb}")

    m = re.match(r"^(.+?) (?:is|are) called (?:an? |the )?(.+)$", original, re.I)
    if m and guarded_left(m.group(1)):
        return end_mark(original, f"{tr(m.group(1))} کو {tr(m.group(2))} کہتے ہیں")

    m = re.match(r"^(.+?) deals with (.+)$", original, re.I)
    if m and guarded_left(m.group(1)):
        return end_mark(original, f"{tr(m.group(1))} {tr(m.group(2))} سے متعلق ہے")

    m = re.match(r"^(.+?) means (.+)$", original, re.I)
    if m and guarded_left(m.group(1)):
        return end_mark(original, f"{tr(m.group(1))} کا مطلب {tr(m.group(2))} ہے")

    m = re.match(r"^([^,;:]{1,90}?) (is|are) not (.+)$", original, re.I)
    if m and guarded_left(m.group(1)):
        cop = "ہیں" if m.group(2).lower() == "are" else "ہے"
        return end_mark(original, f"{tr(m.group(1))} {tr(m.group(3))} نہیں {cop}")

    m = re.match(r"^([^,;:]{1,90}?) (is|are) (.+)$", original, re.I)
    if m and guarded_left(m.group(1)) and m.group(1).lower() not in {"it", "this", "that", "there", "which", "who"}:
        cop = "ہیں" if m.group(2).lower() == "are" else "ہے"
        return end_mark(original, f"{tr(m.group(1))} {tr(m.group(3))} {cop}")

    m = re.match(r"^(it|this|that) is (.+)$", key, re.I)
    if m:
        return end_mark(original, f"یہ {tr(m.group(2))} ہے")

    for verb, ending in VERB_END.items():
        m = re.match(rf"^([^,;:]{{1,90}}?) {verb} (.+)$", original, re.I)
        if m and guarded_left(m.group(1)):
            return end_mark(original, f"{tr(m.group(1))} {tr(m.group(2))} {ending}")

    m = re.match(r"^([A-Za-z][A-Za-z0-9 /+-]{0,40}):\s*(.+)$", original)
    if m and len(m.group(1).split()) <= 5:
        return end_mark(original, f"{tr(m.group(1))}: {tr(m.group(2))}")

    return end_mark(original, tr(original))


def is_header(line: str) -> bool:
    low = line.lower()
    if low.startswith("teach-yourself"):
        return True
    if low.startswith("teacher's edition") or low.startswith("complete edition"):
        return True
    if "sindh textbook" in low or "not an official" in low or "independent study" in low:
        return True
    if re.fullmatch(r"\d+\s*/\s*\d+", line):
        return True
    if re.match(r"^unit \d+\s·", low) and len(line) < 90:
        return True
    if low.startswith("periods") or low.startswith("resources:"):
        return True
    if low.startswith("textbook"):
        return True
    if re.fullmatch(r"resources:.*", low) and len(line) < 40:
        return True
    return False


def is_code(line: str) -> bool:
    if re.search(r"\b(def|import|elif|return|print)\b", line) and re.search(r"[=()\[\]:#]", line):
        return True
    symbols = len(re.findall(r"[=+\-*/<>\[\]()]", line))
    words = re.findall(r"[A-Za-z]{3,}", line)
    return symbols >= 4 and symbols > len(words)


def useful(line: str) -> bool:
    if len(line) < 8:
        return False
    if re.fullmatch(r"[\d\s.+/=×·⇒<>\-]+", line):
        return False
    letters = re.findall(r"[A-Za-z]", line)
    return len(letters) >= 3


def extract(page) -> dict:
    headings: list[str] = []
    words: list[str] = []
    figures: list[str] = []
    paragraphs: list[str] = []
    questions: list[str] = []
    answers: list[str] = []
    notes: list[str] = []
    pending_code = ""
    buf = ""
    mode = ""
    skip_follow = False

    def flush() -> None:
        nonlocal buf
        text = norm(buf)
        buf = ""
        if not useful(text) or is_header(text):
            return
        if mode == "q":
            questions.append(text)
        elif mode == "a":
            answers.append(text)
        elif mode == "note":
            notes.append(text)
        else:
            paragraphs.append(text)

    for raw in (page.get_text("text") or "").splitlines():
        latin = re.findall(r"[A-Za-z]", raw)
        arabic = ARABIC.findall(raw)
        if len(arabic) > len(latin) and "words to know" not in raw.lower() and "figure" not in raw.lower():
            continue
        line = norm(raw)
        if not line or is_header(line):
            flush()
            mode = ""
            skip_follow = bool(line) and line.lower().startswith("resources")
            continue
        if skip_follow and not (line[:1].isupper() or line[:1].isdigit()):
            continue
        skip_follow = False
        low = line.lower()
        if re.fullmatch(r"\d+\.\d+[a-z]?", line):
            flush()
            pending_code = line
            mode = ""
            continue
        if pending_code and useful(line) and not low.startswith("words to know"):
            title = line.split("·")[0].strip()
            headings.append(f"{pending_code} {title}"[:120])
            pending_code = ""
            mode = ""
            continue
        if "words to know" in low:
            flush()
            tail = re.split(r"words to know", line, flags=re.I)[-1]
            found = re.findall(r"[A-Za-z][A-Za-z0-9+/-]*", tail)
            words.extend(found)
            mode = ""
            continue
        if low.startswith("figure") or low.startswith("fig."):
            flush()
            figures.append(line.split("·")[0].strip()[:160])
            mode = ""
            continue
        if low.startswith("misconception") or low.startswith("approach") or low.startswith("activity"):
            flush()
            notes.append(line)
            mode = "note"
            continue
        if re.match(r"^\d+\.\s+", line) and re.search(r"\b(give|which|what|how|why|state|define|explain|name|list|calculate|convert|find|write|draw|compare)\b", low):
            flush()
            questions.append(re.sub(r"^\d+\.\s+", "", line))
            mode = "q"
            continue
        if low == "answer":
            flush()
            mode = "a"
            continue
        if is_code(line):
            flush()
            paragraphs.append("CODE " + line[:180])
            mode = ""
            continue
        if buf and (buf[-1] not in ".?!:" and (line[:1].islower() or buf.endswith((",", ";")))):
            buf = f"{buf} {line}"
            continue
        flush()
        buf = line
    flush()
    # Join word list into known phrases.
    joined: list[str] = []
    i = 0
    tokens = words
    while i < len(tokens):
        hit = None
        for n in range(min(4, len(tokens) - i), 0, -1):
            chunk = " ".join(tokens[i:i + n]).lower()
            if chunk in ALWAYS_SET or chunk in GLOSS:
                hit = " ".join(tokens[i:i + n])
                i += n
                break
        if hit:
            joined.append(hit)
        else:
            joined.append(tokens[i])
            i += 1
    return {
        "headings": headings[:3],
        "words": joined[:12],
        "figures": figures[:3],
        "paragraphs": paragraphs[:8],
        "questions": questions[:4],
        "answers": answers[:4],
        "notes": notes[:3],
    }


def gloss_of(term: str) -> str:
    return GLOSS.get(term.lower(), "")


def speak_words(words: list[str]) -> str:
    if not words:
        return ""
    bits = []
    for word in words:
        g = gloss_of(word)
        shown = "{" + word + "}"
        bits.append(f"{shown} یعنی {g}" if g else shown)
    return "اہم الفاظ: " + "، ".join(bits) + "۔"


def speak_code(line: str) -> str:
    code = line[5:].strip() if line.startswith("CODE ") else line
    code = code.replace("{", "(").replace("}", ")")
    return f"صفحے پر کوڈ لکھا ہے: {{{code}}}۔ اسے دیکھ کر کاپی میں نقل کریں۔"


def page_script(number: int, info: dict) -> str:
    parts: list[str] = [
        f"اب کتابچے کا صفحہ نمبر {number}۔ میں اردو میں سمجھاؤں گا، اور امتحانی اصطلاح انگریزی میں ویسی ہی بولوں گا جیسے صفحے پر چھپی ہے۔"
    ]
    if info["headings"]:
        title = info["headings"][0]
        parts.append(f"عنوان: {{{title}}}۔")
    spoken = speak_words(info["words"])
    if spoken:
        parts.append(spoken)
    sentences = 0
    for para in info["paragraphs"]:
        if sentences >= 6:
            break
        if para.startswith("CODE "):
            parts.append(speak_code(para))
            sentences += 1
            continue
        for sentence in re.split(r"(?<=[.?!])\s+", para):
            if sentences >= 6:
                break
            said = urdish(sentence)
            if said and len(said) > 12:
                parts.append(said)
                sentences += 1
    for fig in info["figures"][:2]:
        caption = fig.replace("{", "(").replace("}", ")")
        parts.append(f"اس صفحے پر شکل چھپی ہے۔ عنوان {{{caption}}}۔ اسے غور سے دیکھیں اور کاپی میں نقل کریں۔")
    for q, a in zip(info["questions"], info["answers"] + [""] * len(info["questions"])):
        said_q = urdish(q)
        if said_q:
            parts.append("سوال۔ " + said_q)
        if a:
            said_a = urdish(a)
            if said_a:
                parts.append("جواب۔ " + said_a)
    for note in info["notes"][:2]:
        said = urdish(re.sub(r"^(Approach|Misconception|Activity):\s*", "", note, flags=re.I))
        if not said:
            continue
        if note.lower().startswith("misconception"):
            parts.append("عام غلطی۔ " + said)
        elif note.lower().startswith("approach"):
            parts.append("پڑھانے کا طریقہ۔ " + said)
        else:
            parts.append("سرگرمی۔ " + said)
    if len(parts) == 1:
        parts.append("یہ صفحہ خاکوں اور علامتوں کا ہے۔ چھپی ہوئی شکل دیکھیں، نام انگریزی میں لکھیں، اور کاپی میں نقل کریں۔")
    parts.append("اصطلاحات کو اردو میں نہ بدلیں۔ جب یہ بات زبانی آ جائے تو اگلے صفحے پر جائیں۔")
    script = " ".join(p.strip() for p in parts if p.strip())
    script = re.sub(r"\s+", " ", script).strip()
    if len(script) > 2400:
        script = script[:2400].rsplit("۔", 1)[0] + "۔ اصطلاحات کو اردو میں نہ بدلیں۔"
    return script


def validate(pages: dict[str, str]) -> None:
    latin_out = LATIN_WORD
    bad = []
    urdu_pages = 0
    for key, script in pages.items():
        if not script or "اب کتابچے کا صفحہ" not in script:
            bad.append(f"{key}: missing opener")
            continue
        if ARABIC.search(script):
            urdu_pages += 1
        if script.count("{") != script.count("}"):
            bad.append(f"{key}: unbalanced braces")
        visible = re.sub(r"\{[^{}]*\}", " ", script)
        leaked = [w for w in latin_out.findall(visible) if len(w) > 1 and not re.fullmatch(r"[A-Za-z]\.", w)]
        if leaked:
            bad.append(f"{key}: latin outside braces {leaked[:6]}")
    if urdu_pages < 280:
        bad.append(f"only {urdu_pages} pages contain Urdu")
    if bad:
        raise SystemExit("tts.json failed checks:\n" + "\n".join(bad[:30]))


def main() -> None:
    doc = pymupdf.open(PDF)
    pages: dict[str, str] = {}
    for i, page in enumerate(doc, start=1):
        pages[str(i)] = page_script(i, extract(page))
    validate(pages)
    OUT.write_text(json.dumps(pages, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    chars = sum(len(v) for v in pages.values())
    braces = sum(v.count("{") for v in pages.values())
    print(f"tts.json {len(pages)} pages, {chars} chars, {braces} english terms, {OUT.stat().st_size} bytes")
    if __import__("sys").argv[-1:] == ["--show"]:
        return
    # Spot-check the first teaching page.
    sample = pages.get("8", "")
    if "مقداریں الگ اور گنتی کے قابل چیزیں" not in sample:
        raise SystemExit("page 8 lost the Urdu description:\n" + sample[:700])
    if not re.search(r"\{[^}]*[Dd]igital system\}", sample):
        raise SystemExit("page 8 lost the English term Digital system:\n" + sample[:700])


if __name__ == "__main__":
    main()
