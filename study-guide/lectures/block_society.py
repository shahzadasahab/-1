"""Lectures 22–25 — Society, literacy, revision."""

from lectures.kit import box, fig, lecture, table
from web import svgs


def lectures() -> str:
    return "".join([
        lecture(22, "IoT collects, analytics explains, AI decides", "Unit 5 · Applications", "45 min", [
            "Keep IoT, analytics, and AI as a loop, not as synonyms.",
            "Name sensor, connectivity, processing, actuator, cloud, UI.",
            "Walk a Sindh irrigation chain in six labelled sentences.",
        ], "\n".join([
            box("recap", "BLOCK E OPENS", "Computing has left the lab. Today three cooperating technologies — and the exam trap of treating the three words as the same thing."),
            fig(svgs.iot_loop(), "Figure L22.1 — Smart irrigation: moisture sensor → radio → cloud analysis → valve → farmer’s phone."),
            fig(svgs.analytics_pipe(), "Figure L22.2 — Raw records become a decision only after cleaning."),
            table(["", "IoT", "Analytics", "AI"], [
                ["Job", "Sense and actuate", "Find patterns", "Decide or predict"],
                ["Pieces", "Sensors, actuators, links, cloud, UI", "Collect–store–clean–analyse–visualise", "Models, learning"],
                ["Example", "Soil probe, smartwatch", "Pass/fail pie chart", "Face unlock, recommendation"],
            ]),
            "<p><strong>Sensor ≠ actuator.</strong> A moisture probe does not open the tap; the valve does. Connectivity (Wi-Fi, Bluetooth, 4G/5G, LoRa) carries the message. Cloud stores the history. The UI is how a human looks and commands.</p>",
            "<p>Memorise the smart-home skeleton: sensor → Wi-Fi → hub/cloud → analytics vs set-point → rule/AI → actuator → phone UI. If Wi-Fi dies the chain breaks — that one failure sentence shows you understand dependency.</p>",
            box("exam", "LONG-ANSWER SKELETON (6 marks)", "A farmer in Sindh wants automatic irrigation. One mark each: sensor, link, decide/process, valve, farmer UI, and where analytics/AI sit on the decision side."),
            box("exit", "EXIT TICKET", "1. Watch → phone heart-rate is mainly which tech? 2. Device that judges dry soil vs opens the valve? 3. Duplicate rows are which analytics step?"),
            box("hw", "HOMEWORK", "Write the irrigation paragraph in six labelled sentences without looking. Then add the failure sentence (Wi-Fi dies)."),
        ])),

        lecture(23, "Sources, impacts, and assistive technology", "Unit 5 · Applications", "45 min", [
            "Classify primary, secondary, and tertiary sources.",
            "Write a 4-mark impact paragraph: help + harm + responsible action.",
            "Name four assistive-tech families.",
        ], "\n".join([
            box("recap", "LAST LECTURE", "IoT collects, analytics speaks, AI acts. Today: can you trust the story, and who does computing include?"),
            table(["Kind", "Meaning", "Example"], [
                ["Primary", "First-hand original", "Interview, NADRA CNIC capture"],
                ["Secondary", "Already explained", "Textbook, PBS census summary"],
                ["Tertiary", "Quick digest", "Encyclopedia, many Wikipedia leads"],
            ]),
            table(["Exhibit", "Verdict"], [
                ["Your interview with the librarian", "Primary source / primary data"],
                ["PBS graph of literacy rates", "Secondary"],
                ["Wikipedia lead paragraph", "Tertiary; start only"],
                ["Anonymous “forward this” image", "Unreliable — no author or date"],
                ["Government .gov.pk PDF, 2024", "Usually reliable secondary"],
            ]),
            "<p>Impact formula: <strong>field + one concrete help + one concrete harm + one responsible action</strong>. “In education, recorded lessons let a student replay a proof (help), but six-hour screen days blunt attention (harm). A responsible student uses the recording for the hard ten minutes, then walks.”</p>",
            "<p><strong>Assistive tech</strong> — mobility (wheelchair), sensory (NVDA screen reader), communication (picture boards), cognitive (audiobooks). They are how computing keeps its promise to everyone. Importance: education access, communication, independence, work, social life.</p>",
            box("exit", "EXIT TICKET", "1. Interview is which source? 2. Two reasons a website is unreliable? 3. What does a screen reader do?"),
            box("hw", "HOMEWORK", "Classify five sources actually on your phone. Then write one impact paragraph for healthcare using the four-sentence formula."),
        ])),

        lecture(24, "Digital literacy — find, judge, collect, show", "Unit 6 · Digital Literacy", "45 min", [
            "Use quotes, filetype:, and site: in a search.",
            "Tell qualitative from quantitative, primary data from secondary data.",
            "Design an ethical 90-minute mini inquiry.",
        ], "\n".join([
            box("recap", "LAST LECTURE", "Sources can lie. Literacy is the filter: find, judge, collect, and show — without stealing words or leaking private data."),
            fig(svgs.inquiry_flow(), "Figure L24.1 — From a sharp question to a final artefact."),
            table(["", "Qualitative", "Quantitative"], [
                ["Nature", "Words, reasons, feelings", "Numbers you can count"],
                ["Ask", "Why / how", "How many / how much"],
                ["Example", "“Notifications break my focus”", "4 hours/day, 72% distracted"],
            ]),
            "<p><strong>Primary data</strong> is what you gather for this question. <strong>Secondary data</strong> already exists (a PBS table). A NADRA record is a primary <em>source</em>; a published NADRA statistic you download is secondary <em>data for you</em>.</p>",
            "<p>Advanced search: quotes for a phrase, <code>filetype:pdf</code> for reports, <code>site:.edu</code> or <code>site:.gov.pk</code> for a domain family. Best PDF query for internet use in Pakistan: <code>\"internet usage in Pakistan\" filetype:pdf</code>.</p>",
            "<p>Ninety-minute inquiry: one sharp question · two advanced searches · eight mixed items (no CNIC, no phone) · 15 classmates with permission · one chart · one recommendation aimed at a real audience (principal, parents, or students).</p>",
            box("mistake", "NOT AN ARTEFACT", "A decorated Canva file is not an artefact if it never answers the question. Evidence → claim → recommendation. Copying without credit is plagiarism. Asking permission is ethics, not politeness."),
            box("exit", "EXIT TICKET", "1. Digital literacy in one sentence. 2. What does site: do? 3. Your own survey replies — primary or secondary data?"),
            box("hw", "HOMEWORK", "Write eight survey items on weekend internet hours. Mark which are qualitative. Remove any personal-id field. State your sample and your permission sentence."),
        ])),

        lecture(25, "Revision sitting — cards, burglar alarm, 40-mark paper", "All units · Closed book", "60–70 min", [
            "Recite the seven cards without notes.",
            "Build Y = A · (D + W) and poke eight rows.",
            "Sit the 40-mark rehearsal and mark it the same evening.",
        ], "\n".join([
            box("recap", "COURSE CLOSES", "Twenty-four sittings. Today you produce traces, not highlights."),
            "<h2>Burglar-alarm studio</h2>",
            "<p>Armed switch \\(A\\), door \\(D\\), window \\(W\\). Siren</p>",
            r"\[ Y = A \cdot (D + W). \]",
            fig(svgs.burglar_alarm(), "Figure L25.1 — OR of the contacts, then AND with the armed switch."),
            "<p>If \\(A=0\\) the house stays quiet. Build it in LogiSim and poke all eight rows.</p>",
            "<h2>Recitation cards</h2>",
            "<p><strong>A Gates.</strong> AND all 1s · OR any 1 · NOT flip · NAND not-all-1s · NOR only all 0s · XOR different · XNOR same · rows \\(2^n\\).</p>",
            "<p><strong>B SDLC.</strong> Analyse → Design → Code → Test → Deploy → Maintain (CAPP).</p>",
            "<p><strong>C OSI.</strong> Please Do Not Throw Sausage Pizza Away. ping = ICMP = layer 3.</p>",
            "<p><strong>D Algorithms.</strong> Bubble neighbours · Selection parks min · Linear any list · Binary sorted only · \\(\\mathrm{mid}=\\lfloor(lo+hi)/2\\rfloor\\).</p>",
            "<p><strong>E Python.</strong> input → str · indent 4 · = vs == · syntax / runtime / logic.</p>",
            "<p><strong>F Data.</strong> PK unique · FK points home · M:N + junction · AND same row · OR different rows.</p>",
            "<p><strong>G Society.</strong> Collect / explain / decide · sensor ≠ actuator · consent · no plagiarism.</p>",
            "<h2>40-mark rehearsal (60 minutes, closed book)</h2>",
            "<p><strong>A (10×1).</strong> Digital levels? XOR 1 when? First SDLC phase? TCP/IP layer count? Search that needs sorted data? <code>input()</code> type? ER rectangle? Soil dryness device? Your own survey replies? <code>site:</code> does what?</p>",
            "<p><strong>B (6×2).</strong> Analog vs digital · when Waterfall · why binary search fails on {9, 1, 4, 7} · <code>=</code> vs <code>==</code> · referential integrity · NADRA interview vs textbook paragraph.</p>",
            "<p><strong>C (3×6).</strong> Truth table of \\(Y=A'\\cdot B+C\\) plus SOP · Bubble-sort trace of {6, 2, 5, 1} · Sindh irrigation chain naming sensor, link, analytics, AI, actuator, UI.</p>",
            "<p><strong>Scheme A:</strong> two values; different; analysis; 4; binary; str; entity; sensor; primary; restrict domain.</p>",
            "<p><strong>Scheme B–C (short).</strong> Analog continuous / digital two levels. Waterfall when requirements are frozen. Binary search needs order. = stores, == tests. FK must match a living PK. Interview = primary; textbook = secondary. C1 eight rows + SOP. C2 passes → {2,5,1,6}, {2,1,5,6}, {1,2,5,6}; Selection swaps less. C3 six labelled sentences.</p>",
            "<h2>Three days without a teacher</h2>",
            "<p><strong>Day 1.</strong> Seven 2-input tables from a blank page. K-map \\(Y=\\sum m(1,3,5,7)\\). OSI both ways. HTTPS encapsulation in five sentences.</p>",
            "<p><strong>Day 2.</strong> Both sorts on {8, 3, 6, 2}. Binary-search 6 in {1..9}. Calculator + guess game; break them; read the traceback.</p>",
            "<p><strong>Day 3.</strong> Library or clinic ER. AND vs OR query rows. Irrigation long answer. Classify five phone sources. Sit this paper again. Target 32 / 40.</p>",
            box("exam", "READY MEANS", "A ready Intermediate student scores 28+ and can explain every miss. The board paper rewards people who can do a truth table, trace a sort, write a small program, draw an ER fragment, and judge a source."),
        ])),
    ])
