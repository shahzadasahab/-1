#!/usr/bin/env python3
"""Urdu explanations and dual captions for the cheat-sheet voice.

Computer Science terms stay in English. The spoken line is Roman Urdish so an
English voice can read it. The caption line is the same sentence in Urdu
script, with those English terms left in Latin letters.
"""

from __future__ import annotations

import re

# Longest English wording first. Replacements explain the line in Roman Urdu
# and leave the syllabus terms in English.
PHRASES: tuple[tuple[str, str], ...] = (
    (
        "a digital system is an electronic system that uses only two values: 0 and 1",
        "Digital system ek electronic system hai jo sirf do values use karta hai: 0 aur 1",
    ),
    (
        "a signal is a changing voltage that carries information",
        "Signal ek badalta hua voltage hai jo information le kar chalti hai",
    ),
    (
        "a truth table shows all possible input combinations and the output for each one",
        "Truth table saari possible input combinations aur har ek ka output dikhati hai",
    ),
    (
        "logic gates are electronic circuits that perform boolean operations",
        "Logic gates electronic circuits hain jo Boolean operations perform karti hain",
    ),
    (
        "they take one or more input bits and produce one output bit",
        "Yeh ek ya zyada input bits leti hain aur ek output bit deti hain",
    ),
    (
        "a logic diagram shows how logic gates are connected to create a circuit",
        "Logic diagram dikhata hai ke logic gates kaise jur kar circuit banati hain",
    ),
    (
        'it is a "picture" of a boolean expression',
        "Yeh Boolean expression ki ek picture hai",
    ),
    (
        "a k-map is a graphical tool used to simplify boolean expressions",
        "K-map ek graphical tool hai jo Boolean expressions ko simplify karne ke liye use hota hai",
    ),
    (
        "adjacent cells differ by only one bit (gray code)",
        "Padosi cells sirf ONE bit se alag hoti hain (Gray code)",
    ),
    (
        "the waterfall model is a linear, sequential approach to the sdlc",
        "Waterfall model SDLC ka seedha, ek ke baad ek approach hai",
    ),
    (
        "each phase must be completed before the next begins",
        "Har phase poora ho, tab agla shuru ho",
    ),
    (
        "sdlc is a structured process that guides software development from beginning to end",
        "SDLC ek structured process hai jo software development ko shuru se akhir tak le jati hai",
    ),
    (
        "the agile model is an iterative approach: software is built in small, repeated cycles called sprints (usually 2-4 weeks)",
        "Agile model ek iterative approach hai: software chhote, dohraye hue cycles mein banta hai jinhen sprints kehte hain (aam tor pe 2-4 weeks)",
    ),
    (
        "computational thinking is a systematic approach to solving problems",
        "Computational Thinking maslon ko hal karne ka systematic approach hai",
    ),
    (
        "an algorithm is a step-by-step logical procedure used to solve a problem",
        "Algorithm ek qadam ba qadam logical procedure hai jo masla hal karne ke liye use hota hai",
    ),
    (
        "decomposition is a problem-solving technique in which a complex task is broken down into smaller, manageable parts (sub-tasks)",
        "Decomposition ek technique hai jis mein complex task ko chhote, manageable parts (sub-tasks) mein toda jata hai",
    ),
    (
        "decomposition is a problem- solving technique in which a complex task is broken down into smaller, manageable parts (sub-tasks)",
        "Decomposition ek technique hai jis mein complex task ko chhote, manageable parts (sub-tasks) mein toda jata hai",
    ),
    (
        "abstraction means hiding unnecessary features and focusing only on the essential ones needed to solve a problem",
        "Abstraction ka matlab non-zaroori features chhupana aur sirf un zaroori cheezon pe dhyaan dena hai jo masla hal karne ke liye chahiye",
    ),
    (
        "bubble sort repeatedly compares adjacent elements and swaps them if they are in the wrong order",
        "Bubble Sort baar baar padosi elements ko compare karti hai aur agar order galat ho to unhein swap karti hai",
    ),
    (
        "selection sort repeatedly selects the smallest element from the unsorted portion and moves it to its correct position at the front",
        "Selection Sort unsorted hisse mein se baar baar sab se chhota element chunti hai aur usay aage sahi jagah le aati hai",
    ),
    (
        "linear search examines each element in the list one by one, from the start, until the target is found or the list ends",
        "Linear Search list ke har element ko shuru se ek ek kar ke dekhti hai, jab tak target mile ya list khatam ho",
    ),
    (
        "binary search is an efficient search algorithm that works by repeatedly dividing the search interval in half",
        "Binary Search ek efficient search algorithm hai jo search interval ko baar baar aadha karke kaam karti hai",
    ),
    (
        "list must be sorted",
        "List sorted hona zaroori hai",
    ),
    (
        "an ide is a software tool that helps programmers write, run and manage code in one place",
        "IDE ek software tool hai jo programmers ko ek hi jagah code likhne, chalane aur manage karne mein madad deti hai",
    ),
    (
        "a variable is a named space in computer memory used to store data",
        "Variable computer memory mein ek naam wali jagah hai jahan data store hota hai",
    ),
    (
        "a data type specifies the kind of data a variable holds",
        "Data type batati hai ke variable kis tarah ka data rakhta hai",
    ),
    (
        "control structures decide the order in which statements are executed (flow of control)",
        "Control structures yeh decide karti hain ke statements kis order mein chalain (flow of control)",
    ),
    (
        "decide the order in which statements are executed",
        "statements kis order mein chalain yeh decide hota hai",
    ),
    (
        "a library (module) is a collection of pre-written code that offers ready-made functions",
        "Library (module) pehle se likhe hue code ka collection hai jo ready-made functions deti hai",
    ),
    (
        "debugging is the process of identifying, tracing and fixing bugs so a program works correctly",
        "Debugging bugs ko pehchanne, trace karne aur theek karne ka process hai taake program theek chale",
    ),
    (
        "data is raw; information is processed data used for decision-making",
        "Data raw hota hai. Information processed data hoti hai jo decision-making ke liye use hoti hai",
    ),
    (
        "a dbms is software that lets you create, manage and interact with databases",
        "DBMS woh software hai jo databases create karne, manage karne aur unke saath kaam karne deti hai",
    ),
    (
        "a key is a field (or set of fields) that uniquely identifies records and links tables",
        "Key ek field (ya fields ka set) hai jo records ko uniquely identify karti hai aur tables ko jodti hai",
    ),
    (
        "integrity constraints are rules that keep keys honest",
        "Integrity constraints woh rules hain jo keys ko theek rakhti hain",
    ),
    (
        "an rdbms stores data in several related tables and uses primary and foreign keys to keep relationships",
        "RDBMS kai related tables mein data rakhti hai aur relationships ke liye primary aur foreign keys use karti hai",
    ),
    (
        "the er model is a blueprint that shows what data will be stored (entities, attributes) and how it connects (relationships) before tables are created",
        "ER model ek blueprint hai jo tables banne se pehle dikhata hai ke kaunsa data store hoga (entities, attributes) aur woh kaise jurta hai (relationships)",
    ),
    (
        "referential integrity means every foreign-key value in a child table must match an existing primary-key value in the parent table (or be null if allowed)",
        "Referential integrity ka matlab yeh hai ke child table ki har foreign-key value parent table ki maujooda primary-key value se match kare (ya agar ijazat ho to NULL ho)",
    ),
    (
        "artificial intelligence is the ability of a computer system to perform tasks that normally need human thinking, such as recognising faces, understanding language and making decisions",
        "Artificial Intelligence computer system ki woh ability hai ke aise tasks kare jin ke liye aam tor pe insani soch chahiye, jaise chehra pehchanna, language samajhna aur decisions lena",
    ),
    (
        "data analytics is the process of collecting, organising, cleaning, studying and presenting data to find useful information",
        "Data Analytics data ko jama, murattab, saaf, study aur present karne ka process hai taake useful information mile",
    ),
    (
        "the internet of things is a system in which physical devices are connected to the internet and can collect and share data to perform tasks automatically",
        "Internet of Things ek system hai jis mein physical devices Internet se jude hon aur khud data jama karke share kar saken taake tasks automatic hon",
    ),
    (
        "iot is a system in which physical devices are connected to the internet and can collect and share data to perform tasks automatically",
        "IoT ek system hai jis mein physical devices Internet se jude hon aur khud data jama karke share kar saken taake tasks automatic hon",
    ),
    (
        "information sources are ways to find knowledge and data",
        "Information sources knowledge aur data dhoondhne ke tareeqe hain",
    ),
    (
        "they are primary (firsthand), secondary (explained by others) and tertiary (summarised)",
        "Yeh primary (firsthand), secondary (doosron ki explanation) aur tertiary (khulasa) hote hain",
    ),
    (
        "assistive technologies are devices, software and systems that help people with disabilities or functional limitations (difficulty in seeing, hearing, moving, speaking, remembering)",
        "Assistive technologies woh devices, software aur systems hain jo disabilities ya functional limitations wale logon ki madad karte hain (dekhne, sunne, chalne, bolne ya yaad rakhne mein mushkil)",
    ),
    (
        "digital literacy is the ability to understand and use digital devices, the internet and online tools in a safe, effective and responsible manner",
        "Digital literacy digital devices, internet aur online tools ko mehfooz, effective aur zimmedari se samajhne aur use karne ki ability hai",
    ),
    (
        "qualitative data is descriptive and non-numerical",
        "Qualitative data descriptive aur non-numerical hoti hai",
    ),
    (
        "quantitative data is numerical, countable or measurable",
        "Quantitative data numerical, countable ya measurable hoti hai",
    ),
    (
        "a data-collection strategy is a planned method for gathering original (new) information",
        "Data-collection strategy original (nayi) information ikatthi karne ka planned method hai",
    ),
    (
        "a data-collection strategy is a planned method for gathering original information",
        "Data-collection strategy original information ikatthi karne ka planned method hai",
    ),
    (
        "an inquiry is an investigation to find the answer to a question using digital tools",
        "Inquiry ek tahqeeq hai jo digital tools se sawal ka jawab dhoondhti hai",
    ),
    (
        "an inquiry is an investigation to find the answer to a question",
        "Inquiry ek tahqeeq hai jo sawal ka jawab dhoondhti hai",
    ),
    (
        "the data shows most students use phones 3-5 hours daily",
        "Data dikhata hai ke zyada tar students roz 3-5 hours phone use karte hain",
    ),
    (
        "however, half use them for lectures and notes",
        "Lekin aadhe unhein lectures aur notes ke liye use karte hain",
    ),
    (
        "therefore, phones help study when used for learning, but entertainment use increases distraction",
        "Is liye phone padhai mein madad karta hai jab learning ke liye use ho, lekin entertainment wali use distraction barhati hai",
    ),
    (
        "a digital artefact is a final product created using digital technologies that answers the research question with evidence and conclusions",
        "Digital artefact digital technologies se bana hua final product hai jo research question ka jawab evidence aur conclusions ke saath deta hai",
    ),
    (
        "hci is the study and design of technology so that it serves people",
        "HCI technology ki study aur design hai taake woh logon ke kaam aaye",
    ),
    (
        "hci is used to design and develop interactive systems (desktop apps, websites, mobile apps) as human-centred solutions across many domains of life",
        "HCI interactive systems (desktop apps, websites, mobile apps) ko design aur develop karne ke liye use hoti hai, taake kai domains mein human-centred solutions banen",
    ),
    (
        "hci ensures that machines are approachable and usable, turning complex technology into everyday tools",
        "HCI yeh yaqeen dilati hai ke machines qareeb aur usable hon, aur complex technology ko rozmarra ke tools bana deti hai",
    ),
    (
        "accessibility principles are hci guidelines that ensure digital systems are usable by all individuals, including people with diverse physical, sensory and cognitive abilities",
        "Accessibility principles woh HCI guidelines hain jo yaqeen dilati hain ke digital systems sab logon ke liye usable hon, jin mein alag alag physical, sensory aur cognitive abilities wale log bhi shamil hain",
    ),
    (
        "need analysis is the process of identifying the gap between the existing situation and the desired outcome",
        "Need analysis maujooda halat aur matlooba nateeje ke beech farq pehchanne ka process hai",
    ),
    (
        "hci problems are common difficulties that stop users from using technology smoothly",
        "HCI problems woh aam mushkilat hain jo users ko technology aasani se use karne se rokti hain",
    ),
    (
        "they happen when systems fail to meet human needs or cognitive limits",
        "Yeh tab hoti hain jab systems human needs ya cognitive limits poori na kar saken",
    ),
    (
        "ui design is the process of creating and organizing the visual elements of a software application so users can interact with it easily and efficiently",
        "UI design software application ke visual elements banane aur unhein arrange karne ka process hai taake users aasani aur efficiency se interact kar saken",
    ),
    (
        "ui is what you see",
        "UI woh hai jo nazar aaye",
    ),
    (
        "ux is how it feels",
        "UX yeh hai ke mehsoos kaise ho",
    ),
    (
        "wireframing is creating a basic visual outline or blueprint of a user interface before the final design",
        "Wireframing final design se pehle user interface ka sada visual outline ya blueprint banana hai",
    ),
    (
        "an algorithm is correct if its output matches the expected results for all valid inputs",
        "Algorithm tab correct hai jab uska output saare valid inputs ke expected results se match kare",
    ),
    (
        "a trace table is a technique used to monitor how the values of variables change during the execution of an algorithm",
        "Trace table ek technique hai jo algorithm ke execution ke dauran variables ki values ke badalne ko monitor karti hai",
    ),
    (
        "clarity means an algorithm is easy to read, understand and modify",
        "Clarity ka matlab yeh hai ke algorithm parhna, samajhna aur badalna aasan ho",
    ),
    (
        "modularity means breaking an algorithm into smaller, independent parts such as functions, classes or modules",
        "Modularity ka matlab algorithm ko chhote, independent parts mein todna hai, jaise functions, classes ya modules",
    ),
    (
        "readability is how easily another person can understand the purpose and logic of an algorithm without running it",
        "Readability yeh hai ke doosra insaan algorithm ko chalaye baghair uska purpose aur logic kitni aasani se samajh sake",
    ),
    (
        "algorithm efficiency is measured in terms of time (speed) and space (memory)",
        "Algorithm efficiency time (speed) aur space (memory) ke hisaab se naapi jati hai",
    ),
    (
        "big o notation is a mathematical method used to describe how the running time (or memory) grows as the input size n grows",
        "Big O notation ek mathematical method hai jo batati hai ke input size n barhne pe running time (ya memory) kaise barhti hai",
    ),
    (
        "a data structure is a systematic way of organising, storing and managing data so that an algorithm can access, modify and process it efficiently",
        "Data structure data ko organise, store aur manage karne ka systematic tareeqa hai taake algorithm usay efficiently access, modify aur process kar sake",
    ),
    (
        "a stack is a linear data structure that works on the lifo principle: last-in, first-out",
        "Stack ek linear data structure hai jo LIFO principle pe chalti hai: Last-In, First-Out",
    ),
    (
        "a queue is a linear data structure that works on the fifo principle: first-in, first-out",
        "Queue ek linear data structure hai jo FIFO principle pe chalti hai: First-In, First-Out",
    ),
    (
        "a list stores an ordered collection of items in a single variable",
        "List ek single variable mein items ka ordered collection rakhti hai",
    ),
    (
        "it is mutable and written with square brackets",
        "Yeh mutable hai aur square brackets mein likhi jati hai",
    ),
    (
        "a tuple is an ordered collection that is immutable",
        "Tuple ek ordered collection hai jo immutable hai",
    ),
    (
        "once created, items cannot be added, removed or replaced",
        "Banne ke baad items add, remove ya replace nahi ho sakte",
    ),
    (
        "a dictionary stores data as key-value pairs",
        "Dictionary data ko key-value pairs mein rakhti hai",
    ),
    (
        "a dictionary stores data as key- value pairs",
        "Dictionary data ko key-value pairs mein rakhti hai",
    ),
    (
        "it is ordered (python 3.7+), mutable, and its keys are unique",
        "Yeh ordered (Python 3.7+), mutable hai, aur us ki keys unique hoti hain",
    ),
    (
        "a function is a named block of code that is written once and runs whenever it is called, avoiding duplicate code",
        "Function code ka naam wala block hai jo ek dafa likha jata hai aur jab call ho tab chalta hai, taake duplicate code na ho",
    ),
    (
        "file handling is a program's ability to create, read, write, update and delete files on disk",
        "File handling program ki woh ability hai ke disk pe files create, read, write, update aur delete kar sake",
    ),
    (
        "the with statement is a context manager: it opens the file, runs the indented block, and always closes the file when the block ends-even if an error occurs",
        "with statement ek context manager hai: file kholta hai, indented block chalata hai, aur block khatam hote hi file hamesha band karta hai, chahe error ho",
    ),
    (
        "data analysis is examining, organising and interpreting data to extract useful information",
        "Data analysis data ko dekhna, murattab karna aur samajhna hai taake useful information nikle",
    ),
    (
        "a dataframe is a 2-d table of rows and columns, like excel or an sql table",
        "DataFrame rows aur columns ki 2-D table hai, jaise Excel ya SQL table",
    ),
    (
        "median is the middle value of the ordered list",
        "Median ordered list ki beech wali value hai",
    ),
    (
        "mode is the value that appears most often",
        "Mode woh value hai jo sab se zyada baar aaye",
    ),
    (
        "for an even count, the median is the mean of the two middle values",
        "Even count pe median do beech wali values ka mean hota hai",
    ),
    (
        "a machine learning model is the system that learns from data and gives an output",
        "Machine learning model woh system hai jo data se seekhta hai aur output deta hai",
    ),
    (
        "deep learning is a machine-learning method in which computers use multi-layer neural networks to learn complex patterns from data",
        "Deep learning ek machine-learning method hai jis mein computers multi-layer neural networks se data ke complex patterns seekhte hain",
    ),
    (
        "deep learning is a machine- learning method in which computers use multi-layer neural networks to learn complex patterns from data",
        "Deep learning ek machine-learning method hai jis mein computers multi-layer neural networks se data ke complex patterns seekhte hain",
    ),
    (
        "a neural network is a computer model that learns patterns from data",
        "Neural network ek computer model hai jo data se patterns seekhta hai",
    ),
    (
        "secure collaboration means using digital tools to work together in a safe, controlled and responsible way",
        "Secure collaboration ka matlab digital tools se mil kar kaam karna hai, mehfooz, controlled aur zimmedari se",
    ),
    (
        "data protection means keeping digital information safe from unauthorised access, misuse, loss, damage or accidental deletion",
        "Data protection ka matlab digital information ko unauthorised access, misuse, loss, damage ya accidental deletion se mehfooz rakhna hai",
    ),
    (
        "a security threat is any action, event or weakness that can harm a computer system or its data",
        "Security threat koi bhi action, event ya weakness hai jo computer system ya us ke data ko nuqsan pahuncha sake",
    ),
    (
        "mitigation techniques are protective measures that prevent threats or reduce their impact",
        "Mitigation techniques woh protective measures hain jo threats ko rokein ya un ka asar kam karein",
    ),
    (
        "an entrepreneur is a person who identifies a problem, thinks of a solution, and tries to change that solution into a product or service",
        "Entrepreneur woh shakhs hai jo problem pehchane, solution soche, aur us solution ko product ya service banane ki koshish kare",
    ),
    (
        "entrepreneurship in the digital age means using digital tools to start, test, improve, and grow a business idea",
        "Entrepreneurship in the digital age ka matlab digital tools se business idea ko shuru karna, test karna, behtar banana aur barhana hai",
    ),
    (
        "a prototype is an early model of a product, service, website, or app that shows how the idea may look or work",
        "Prototype product, service, website ya app ka early model hai jo dikhata hai ke idea kaisa dikhe ya kaise chale",
    ),
    (
        "it is not the final product and is made to test the idea and collect feedback",
        "Yeh final product nahi hota, aur idea test karne aur feedback lene ke liye banta hai",
    ),
    (
        "a minimum viable product (mvp) is the simplest working version of a product",
        "Minimum Viable Product (MVP) product ka sab se sada working version hai",
    ),
    (
        "a beachhead market is a small and focused group of first users who have a clear need and are likely to try the product early",
        "Beachhead market pehle users ka chhota aur focused group hai jin ki need clear ho aur jo product ko jaldi try karne wale hon",
    ),
    (
        "a small, focused group of first users with a clear need who are likely to try the product early",
        "pehle users ka chhota focused group jin ki need clear ho aur jo product jaldi try karein",
    ),
    (
        "xor is 1 when the inputs differ",
        "XOR tab 1 hota hai jab inputs alag hon",
    ),
    (
        "xnor is the equality gate",
        "XNOR equality gate hai",
    ),
    (
        "where n is the number of inputs",
        "jahan n inputs ki tadaad hai",
    ),
    (
        "analog is continuous",
        "analog continuous hai",
    ),
    (
        "digital has only two levels",
        "digital ke paas sirf do levels hain",
    ),
    (
        "easy to design",
        "design karna aasan hai",
    ),
    (
        "screen reader is an example of",
        "Screen reader is ki example hai",
    ),
)

PHRASES = tuple(sorted(PHRASES, key=lambda item: len(item[0]), reverse=True))

URDU_HINTS = {
    "aaj", "aasan", "aasani", "aata", "aati", "aaye", "abhi", "achanak", "aadha", "aadhe",
    "aage", "agla", "alag", "andar", "aur", "awaaz", "baad", "baar", "badal", "badalta",
    "badalne", "band", "bana", "banana", "banane", "banati", "banaya", "banne", "banta",
    "bara", "bari", "barhta", "barhti", "barhne", "beech", "behtar", "bhi", "bilkul",
    "bolte", "bolo", "chale", "chalen", "chalne", "chalta", "chalti", "cheez", "cheezon",
    "chhota", "chhote", "chhoti", "chhupana", "dafa", "dauran", "dekhna", "dekhne",
    "dekhti", "deta", "dete", "deti", "dhyaan", "dikhata", "dikhati", "din", "do", "dono",
    "doosra", "doosron", "ek", "farq", "gin", "ginte", "hai", "hain", "hal", "halat",
    "hamesha", "har", "hissa", "hisse", "hona", "hon", "hota", "hote", "hoti", "ho",
    "hua", "hue", "ikatthi", "insaan", "insani", "jagah", "jaldi",
    "jama", "jawab", "jin", "jinhen", "jis", "jo", "jur", "jurta", "ka", "kaam", "kaise",
    "kaisa", "kam", "kare", "karein", "karna", "karne", "karta", "karte", "karti", "ke",
    "kehte", "khatam", "khud", "ki", "kis", "kitab", "kitni", "ko", "koi", "koshish",
    "kyunke", "le", "lena", "leti", "liye", "logon", "madad", "masla", "maslon",
    "matlab", "maujooda", "mehfooz", "mehsoos", "mein", "mile", "mushkil", "mushkilat",
    "na", "naam", "naapi", "nahi", "nahin", "naya", "nayi", "ne", "nikle", "nuqsan",
    "pa", "padhai", "pahuncha", "par", "parhna", "pe", "pehchane", "pehchanne", "pehle",
    "phir", "poora", "poori", "qadam", "qareeb", "rakhta", "rakhti", "roz",
    "rozmarra", "saare", "saari", "sab", "saath", "sada", "sake", "saken", "sakta",
    "sakte", "samajh", "samajhna", "samajhne", "sawaal", "sawal", "se", "seedha",
    "seedhi", "seekhta", "seekhte", "shakhs", "shamil",     "shuru", "sirf", "soche", "sunne", "suno", "taake", "tab", "tadaad", "tak", "tarah", "tareeqa",
    "tareeqe", "theek", "toda", "todna", "un", "unhein", "us", "usay", "wali", "wala",
    "wale", "woh", "ya", "yaad", "yaqeen", "yeh", "yehi", "zaroori", "zyada",
}

EN_FUNC = {
    "the", "a", "an", "of", "and", "to", "that", "in", "with", "for", "from", "on",
    "by", "is", "are", "was", "were", "this", "it", "as", "or", "if", "when", "where",
    "which", "who", "into", "over", "after", "before", "than", "then", "so", "but",
    "not", "only", "they", "their", "its", "be", "can", "will", "each", "every",
}

CODE_MARK = re.compile(r"(print\s*\(|\bdef\s+\w+\(|\bimport\s+|==|#|f\"|input\s*\()")
MCQ_MARK = re.compile(r"\b[a-d]\.\s", re.I)

PATTERNS: tuple[tuple[re.Pattern[str], object], ...] = (
    (
        re.compile(r"^(?:A|An|The)\s+(.+?)\s+is\s+(?:an?|the)\s+(.+?)\s+that\s+(.+)$", re.I),
        lambda m: f"{cap(m.group(1))} ek {m.group(2)} hai jo {m.group(3)}",
    ),
    (
        re.compile(r"^(.+?)\s+is\s+(?:an?|the)\s+(.+?)\s+that\s+(.+)$", re.I),
        lambda m: f"{cap(m.group(1))} ek {m.group(2)} hai jo {m.group(3)}",
    ),
    (
        re.compile(r"^(.+?)\s+is\s+(?:an?|the)\s+(.+?)\s+used\s+to\s+(.+)$", re.I),
        lambda m: f"{cap(m.group(1))} ek {m.group(2)} hai jo {m.group(3)} ke liye use hota hai",
    ),
    (
        re.compile(r"^(.+?)\s+means\s+(.+)$", re.I),
        lambda m: f"{cap(m.group(1))} ka matlab {m.group(2)} hai",
    ),
    (
        re.compile(r"^(.+?)\s+is\s+used\s+to\s+(.+)$", re.I),
        lambda m: f"{cap(m.group(1))} ko {m.group(2)} ke liye use karte hain",
    ),
    (
        re.compile(r"^(?:A|An|The)\s+(.+?)\s+is\s+(?:an?|the)\s+([^:.]+)$", re.I),
        lambda m: f"{cap(m.group(1))} ek {m.group(2).strip()} hai",
    ),
    (
        re.compile(r"^(.+?)\s+shows\s+(.+)$", re.I),
        lambda m: f"{cap(m.group(1))} {m.group(2)} dikhata hai",
    ),
    (
        re.compile(r"^(.+?)\s+are\s+(.+?)\s+that\s+(.+)$", re.I),
        lambda m: f"{cap(m.group(1))} {m.group(2)} hain jo {m.group(3)}",
    ),
    (
        re.compile(r"^(.+?)\s+is\s+(.+?)\s+when\s+(.+)$", re.I),
        lambda m: f"{cap(m.group(1))} {m.group(2)} hota hai jab {m.group(3)}",
    ),
    (
        re.compile(r"^(.+?)\s+are\s+([^:.]+)$", re.I),
        lambda m: f"{cap(m.group(1))} {m.group(2).strip()} hain",
    ),
    (
        re.compile(r"^(.+?)\s+is\s+([^:.]+)$", re.I),
        lambda m: f"{cap(m.group(1))} {m.group(2).strip()} hai",
    ),
)


def cap(text: str) -> str:
    text = re.sub(r"^(?:a|an|the)\s+", "", text.strip(), flags=re.I)
    text = re.sub(r"\s+", " ", text).strip(" ,;")
    if text[:1].islower():
        text = text[0].upper() + text[1:]
    return text


def normalize(text: str) -> str:
    text = text.replace("—", ", ").replace("–", "-")
    text = text.replace("“", '"').replace("”", '"').replace("’", "'")
    text = re.sub(r"([A-Za-z0-9])-\s+([A-Za-z0-9])", r"\1-\2", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def english_scores(text: str) -> tuple[int, int]:
    words = re.findall(r"[A-Za-z']+", text)
    english = sum(1 for word in words if word.lower() in EN_FUNC)
    urdu = sum(1 for word in words if word.lower() in URDU_HINTS)
    return english, urdu


def should_explain(text: str) -> bool:
    if not text or CODE_MARK.search(text) or MCQ_MARK.search(text):
        return False
    english, urdu = english_scores(text)
    if urdu >= 2 and urdu >= english:
        return False
    return english >= 2 or bool(re.search(r"\b(is|are|means|shows|uses|used)\b", text, re.I))


def apply_phrases(text: str) -> str:
    folded = text
    for source, target in PHRASES:
        pattern = re.compile(re.escape(source), re.I)
        folded = pattern.sub(target, folded)
    return folded


def apply_patterns(text: str) -> str:
    for pattern, builder in PATTERNS:
        match = pattern.match(text.strip())
        if match:
            return builder(match)
    return text


def tidy(text: str) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"\s+([,.;:!?])", r"\1", text)
    text = text.replace("..", ".").replace(":.", ".")
    return text


def explain_piece(text: str) -> str:
    core = text.strip()
    punct = ""
    match = re.match(r"^(.*?)([.!?])$", core)
    if match:
        core, punct = match.group(1).strip(), match.group(2)
    if ":" in core:
        head, tail = core.split(":", 1)
        if should_explain(head):
            head = apply_patterns(head.strip())
            return tidy(head) + ": " + tail.strip() + punct
    if not should_explain(core):
        return tidy(core) + punct
    return tidy(apply_patterns(core)) + punct


def explain_text(text: str) -> str:
    text = apply_phrases(normalize(text))
    parts = [part.strip() for part in re.split(r"(?<=[.!?])\s+", text) if part.strip()]
    explained = [explain_piece(part) for part in parts]
    out = " ".join(part for part in explained if part)
    out = re.sub(r"\s+", " ", out).strip()
    sentences = re.split(r"(?<=[.!?])\s+", out)
    return " ".join(
        sentence[:1].upper() + sentence[1:] if sentence else sentence for sentence in sentences
    )


SPELL_TEXT = """
aab اب
aadha آدھا
aadhe آدھے
aage آگے
aaj آج
aakhir آخر
aam عام
aasan آسان
aasani آسانی
aata آتا
aati آتی
aaye آئے
abhi ابھی
achanak اچانک
agla اگلا
alag الگ
andar اندر
asar اثر
aur اور
awaaz آواز
baad بعد
baar بار
babot بہت
badal بدل
badalta بدلتا
badalne بدلنے
baghair بغیر
band بند
bana بنا
banana بنانا
banane بنانے
banati بناتی
banaya بنایا
banne بننے
banta بنتا
banti بنتی
bara بڑا
bari بڑی
barabar برابر
barhta بڑھتا
barhti بڑھتی
barhne بڑھنے
beech بیچ
behtar بہتر
bhi بھی
bilkul بالکل
bolte بولتے
bolo بولو
chahe چاہے
chakkar چکر
chale چلے
chalen چلیں
chalaye چلائے
chalne چلنے
chalta چلتا
chalti چلتی
cheez چیز
cheezon چیزوں
chhota چھوٹا
chhote چھوٹے
chhoti چھوٹی
chhupana چھپانا
dafa دفعہ
dauran دوران
dekh دیکھ
dekhna دیکھنا
dekhne دیکھنے
dekhti دیکھتی
deta دیتا
dete دیتے
deti دیتی
dhyaan دھیان
dikhata دکھاتا
dikhati دکھاتی
dilati دلاتی
din دن
do دو
dono دونوں
doosra دوسرا
doosron دوسروں
dohraya دہرایا
dohraye دہرائے
ek ایک
farq فرق
gin گن
ginte گنتے
hai ہے
hain ہیں
hal حل
halat حالت
hamesha ہمیشہ
har ہر
hissa حصہ
hisse حصے
hona ہونا
hon ہوں
hota ہوتا
hote ہوتے
hoti ہوتی
ho ہو
hua ہوا
hue ہوئے
ikatthi اکٹھی
insaan انسان
insani انسانی
is اس
jagah جگہ
jaldi جلدی
jama جمع
jawab جواب
jin جن
jinhen جنہیں
jis جس
jo جو
jode جوڑے
jodti جوڑتی
jur جڑ
jurta جڑتا
ka کا
kaam کام
kaise کیسے
kaisa کیسا
kam کم
kare کرے
karein کریں
karna کرنا
karne کرنے
karta کرتا
karte کرتے
karti کرتی
ke کے
kehte کہتے
khatam ختم
khud خود
ki کی
kis کس
kitab کتاب
kitni کتنی
ko کو
koi کوئی
koshish کوشش
kyunke کیونکہ
le لے
lena لینا
leti لیتی
liye لیے
logon لوگوں
madad مدد
masla مسئلہ
maslon مسئلوں
matlab مطلب
matlooba مطلوبہ
maujooda موجودہ
mehfooz محفوظ
mehsoos محسوس
mein میں
mile ملے
mushkil مشکل
mushkilat مشکلات
na نہ
naam نام
naapi ناپی
nahi نہیں
nahin نہیں
nateeje نتیجے
naya نیا
nayi نئی
ne نے
nikle نکلے
nuqsan نقصان
padhai پڑھائی
pahuncha پہنچا
par پر
parhna پڑھنا
padosi پڑوسی
pe پہ
pehchane پہچانے
pehchanne پہچاننے
pehle پہلے
phir پھر
picture تصویر
poora پورا
poori پوری
qadam قدم
qareeb قریب
rakhta رکھتا
rakhti رکھتی
rakhein رکھیں
rokein روکیں
rokti روکتی
roz روز
rozmarra روزمرہ
saare سارے
saari ساری
sab سب
saath ساتھ
sada سادہ
sake سکے
saken سکیں
sakta سکتا
sakte سکتے
sakti سکتی
samajh سمجھ
samajhna سمجھنا
samajhne سمجھنے
sawaal سوال
sawal سوال
se سے
seedha سیدھا
seedhi سیدھی
seekhta سیکھتا
seekhte سیکھتے
shakhs شخص
shamil شامل
shuru شروع
sirf صرف
soche سوچے
sunne سننے
suno سنو
taake تاکہ
tab تب
tadaad تعداد
tak تک
tarah طرح
tareeqa طریقہ
tareeqe طریقے
theek ٹھیک
toda توڑا
todna توڑنا
tor پہ
un ان
unhein انہیں
us اس
usay اسے
uska اس کا
wali والی
wala والا
wale والے
woh وہ
ya یا
yaad یاد
yaqeen یقین
yeh یہ
yehi یہی
zaroori ضروری
zyada زیادہ
karo کرو
rakho رکھو
aksar اکثر
misaal مثال
kya کیا
likho لکھو
likhna لکھنا
likhni لکھنی
likhi لکھی
likha لکھا
aise ایسے
poochte پوچھتے
poochta پوچھتا
mat مت
bohat بہت
bahut بہت
sahih صحیح
waqt وقت
ghalat غلط
galat غلط
khana کھانا
kyun کیوں
dhoka دھوکا
kar کر
jab جب
naap ناپ
qisam قسم
gina گنا
naapa ناپا
jata جاتا
jaise جیسے
jaisa جیسا
jaisi جیسی
kuch کچھ
paas پاس
pani پانی
faida فائدہ
warna ورنہ
agar اگر
jahan جہاں
jaisi جیسی
dhal ڈھال
peechhe پیچھے
chakkar چکر
wapas واپس
upar اوپر
jaate جاتے
neeche نیچے
chaar چار
chhe چھ
saat سات
padosi پڑوسی
taraf طرف
dhoondh ڈھونڈ
dhoondo ڈھونڈو
kaat کاٹ
samajhta سمجھتا
dabba ڈبہ
rehta رہتا
haan ہاں
raasta راستہ
chalte چلتے
pata پتہ
rahe رہیں
raha رہا
rahi رہی
dobara دوبارہ
lao لاؤ
pehchanti پہچانتی
doosri دوسری
ishara اشارہ
chhanti چھانتی
faisla فیصلہ
hattati ہٹاتی
rang رنگ
rae رائے
milaap ملاپ
sunna سننا
chhuna چھونا
harkat حرکت
nazar نظر
bina بنا
ghalti غلطی
mukammal مکمل
batate بتاتے
kahan کہاں
hoga ہوگا
andaza اندازہ
hisaab حساب
dheere دھیرے
chadhhta چڑھتا
tez تیز
jati جاتی
khane خانے
pahunchte پہنچتے
agle اگلے
ungli انگلی
kai کئی
kisi کسی
daalo ڈالو
nikalo نکالو
nikalta نکلتا
taala تالا
laga لگا
padho پڑھو
purani پرانی
mita مٹا
jodo جوڑو
banao بناؤ
pakadta پکڑتا
sooraton صورتوں
khali خالی
seekhne سیکھنے
pehla پہلا
jeet جیت
bechne بیچنے
zaroor ضرور
zaroorat ضرورت
kabhi کبھی
yahan یہاں
wahan وہاں
lekin لیکن
magar مگر
toh تو
bahar باہر
thoda تھوڑا
thodi تھوڑی
kaun کون
kaunsi کونسی
kab کب
kitna کتنا
kitne کتنے
itna اتنا
itni اتنی
wahi وہی
apna اپنا
apni اپنی
apne اپنے
milao ملاؤ
milta ملتا
milti ملتی
mila ملا
dekho دیکھو
chalo چلو
jao جاؤ
jaaye جائے
aao آؤ
seedhiyon سیڑھیوں
kahin کہیں
khare کھڑے
qism قسم
ginti گنتی
samjho سمجھو
rakhna رکھنا
dena دینا
kholo کھولو
kholta کھولتا
bas بس
ab اب
kal کل
shuruat آغاز
idhar ادھر
udhar ادھر
bilkul بالکل
pooch پوچھ
sawal سوال
jawab جواب
matlab مطلب
tarah طرح
wala والا
wali والی
wale والے
cheezain چیزیں
cheezein چیزیں
shehar شہر
dost دوست
sarak سڑک
duniya دنیا
bhar بھر
jure جڑے
muashre معاشرے
school اسکول
kaam کام
barabar برابر
bhai بھائی
behan بہن
share شیئر
number نمبر
bura برا
badalte بدلتے
gehre گہرے
kam کم
asal اصل
karte کرتے
kartein کریں
ginn گن
shuru شروع
khatam ختم
kitne کتنے
sawal سوال
yaad یاد
rakho رکھو
hona ہونا
chahiye چاہیے
chahte چاہتے
chahiye چاہیے
payenge پائیں گے
waqai واقعی
dikhe دکھے
dikhta دکھتا
samajh سمجھ
aata آتا
faida فائدہ
paise پیسے
denge دیں گے
kaafi کافی
kis کس
kitni کتنی
baar بار
abhi ابھی
karein کریں
kare کرے
karega کرے گا
karegi کرے گی
karenge کریں گے
karunga کروں گا
matlb مطلب
matlab مطلب
ya یا
aur اور
phir پھر
bhi بھی
sirf صرف
nahi نہیں
nahin نہیں
mat مت
haan ہاں
na نہ
ek ایک
do دو
hai ہے
hain ہیں
ho ہو
tha تھا
thi تھی
log لوگ
to تو
arabon اربوں
"""


def _spell_table() -> dict[str, str]:
    table: dict[str, str] = {}
    for line in SPELL_TEXT.splitlines():
        line = line.strip()
        if not line:
            continue
        roman, urdu = line.split(maxsplit=1)
        table[roman.lower()] = urdu
    # Multi-word leftovers that should stay one Urdu phrase when seen as two tokens
    # are handled token by token. "aam tor pe" is three entries if present.
    table.setdefault("tor", "طور")
    table.setdefault("pe", "پہ")
    return table


SPELL = _spell_table()

WORD = re.compile(r"[A-Za-z][A-Za-z']*")
# These Roman tokens are Urdu in this script and also ordinary English words.
AMBIGUOUS = {"is", "do", "us", "to"}
MULTI_URDU = (
    ("is liye", "اس لیے"),
    ("is din", "اس دن"),
    ("is misaal", "اس مثال"),
    ("is row", "اس row"),
    ("is idea", "اس idea"),
    ("aam tor pe", "عام طور پہ"),
    ("qadam ba qadam", "قدم بہ قدم"),
)


def roman_to_urdu(text: str) -> str:
    converted = text.strip()
    for source, target in MULTI_URDU:
        converted = re.sub(re.escape(source), target, converted, flags=re.I)

    words = WORD.findall(converted)
    urdu_tokens = sum(
        1 for word in words if word.lower() in SPELL and word.lower() not in AMBIGUOUS
    )
    freeze_log = bool(re.search(r"\bO\s*\(|\bO of\b|\blog n\b|\bn log\b|\btime log\b", converted, re.I))

    def repl(match: re.Match[str]) -> str:
        token = match.group(0)
        if token.isupper() and len(token) > 1:
            return token
        key = token.lower()
        if key == "log" and freeze_log:
            return token
        if key == "do" and re.search(r"\b(?:what|to|can|could|should|would|please)\s+do\b|\bdo\s+(?:not|you|we|they|the|this)\b", converted, re.I):
            return token
        if key in {"is", "us"} and urdu_tokens < 1:
            return token
        if key == "to" and urdu_tokens < 2:
            return token
        spelled = SPELL.get(key)
        return spelled if spelled else token

    converted = WORD.sub(repl, converted)
    converted = re.sub(r"\.\s*$", "۔", converted)
    converted = re.sub(r"!\s*$", "۔", converted)
    if converted.endswith("?"):
        converted = converted[:-1] + "؟"
    return converted


def cues_from_vocal(text: str) -> list[dict[str, str]]:
    pieces = [part.strip() for part in re.split(r"(?<=[.!?])\s+", text.strip()) if part.strip()]
    cues: list[dict[str, str]] = []
    for piece in pieces:
        vocal = tidy(piece)
        if vocal and vocal[-1] not in ".!?":
            vocal += "."
        cues.append({"vocal": vocal, "ur": roman_to_urdu(vocal)})
    return cues
