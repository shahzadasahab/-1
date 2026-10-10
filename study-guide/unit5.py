"""Unit 5 — Applications and Impacts of Computing."""

from reportlab.platypus import PageBreak, Spacer

from pdf_kit import Callout, bullets, h1, h2, h3, numbered, p, simple_table


def build(styles):
    s = styles
    story = [
        h1(s, "Unit 5 — Applications and Impacts of Computing"),
        p(s, "Computing has left the lab. It sits in Sindh’s classrooms, bank apps, hospital records, and irrigation channels. This unit is about three cooperating technologies — IoT, Data Analytics, and AI — plus the human questions: Is this source trustworthy? Who is helped? Who is harmed?", "Lead"),
        h2(s, "5.1 What you must be able to do"),
    ]
    story += bullets(s, [
        "Define AI, IoT, and Data Analytics and show how they form one loop: collect → analyse → decide.",
        "Name IoT components and map them onto smart cities, industry, health, school, home, and farm.",
        "Classify sources as primary, secondary, or tertiary and judge reliability.",
        "Give balanced positive and negative impacts, and rules for responsible use.",
        "Describe assistive-technology categories and why they matter.",
    ])
    story += [
        h2(s, "5.2 Three technologies, one loop"),
        p(s, "<b>Artificial Intelligence</b> is human-built “intelligence”: a system that uses data to decide. Face unlock, a YouTube recommendation, a website chatbot. In a smart home AI is the brain: the room is hot, so turn on the fan."),
        p(s, "<b>Internet of Things</b> is physical devices on a network that sense and act without a human in every loop: watches, meters, cameras, valves, vehicles."),
        p(s, "<b>Data Analytics</b> is the craft of collecting, storing, cleaning, studying, and presenting data so a decision is better than a guess. A college result meeting is analytics: gather marks, fix the missing roll number, find who failed Physics, draw the bar chart."),
        simple_table(
            s,
            ["", "IoT", "Data Analytics", "AI"],
            [
                ["Job", "Collect real-world signals; actuate", "Find patterns and meaning", "Decide or predict"],
                ["Pieces", "Sensors, actuators, links, cloud, UI", "Collect, store, clean, analyse, visualise", "Models, learning algorithms"],
                ["Works on", "Physical devices", "Records and numbers", "Software that chooses"],
                ["Example", "Soil moisture probe", "Pass/fail pie chart", "Siri / a recommendation"],
                ["Output", "Raw or streamed readings", "Reports and graphs", "An action or suggestion"],
            ],
            col_widths=[75, 145, 145, 130],
        ),
        Spacer(1, 6),
        Callout(s, "key", "IoT generates data. Analytics makes the data speak. AI acts on the speech. Exam answers that treat the three words as synonyms lose marks."),
        h2(s, "5.3 IoT components — learn the chain"),
    ]
    story += numbered(s, [
        "<b>Sensors</b> read the world: temperature, motion, fingerprint, camera, smoke, soil moisture.",
        "<b>Actuators</b> do the world: motor, switch, door, water valve, fan, alarm. Sensor ≠ actuator. A moisture probe does not open the tap; the valve does.",
        "<b>Connectivity</b> carries the message: Wi-Fi, Bluetooth, ZigBee, LoRaWAN, NB-IoT, 4G/5G. No link, no system.",
        "<b>Data processing</b> collect → organise → analyse → decide (on the device or in the cloud).",
        "<b>Cloud computing</b> is storage and programs on the internet (Drive, Classroom, an LMS) so a phone need not hold the whole farm’s history.",
        "<b>User interface</b> is how a human looks and commands: app, touch screen, dashboard, voice.",
    ])
    story += [
        h3(s, "Worked system: smart irrigation in rural Sindh"),
        p(s, "A soil-moisture sensor (IoT) reports “dry.” The reading travels over a mobile link to a small cloud service. Analytics compares it with the crop’s threshold and the weather forecast. AI / the control rule decides “irrigate for 12 minutes.” An actuator (valve) opens. The farmer’s phone UI shows the tank level and today’s water used. That one paragraph is a full long-answer if you name every component."),
        h2(s, "5.4 Where IoT is already living"),
        simple_table(
            s,
            ["Domain", "What it does", "Local flavour"],
            [
                ["Smart city", "Adaptive signals, e-challan, streetlights on motion, parking sensors, bins that text when full", "Karachi / Lahore / Islamabad congestion"],
                ["Industry", "Temperature and vibration on machines, automated repeats, in-line quality", "Textile mills in Sindh and Punjab"],
                ["Health", "Watch heart-rate, remote panels, emergency beacons, digital records", "Villages far from a hospital"],
                ["Education", "Boards, biometric attendance, room climate, remote lessons", "Government colleges in Sindh"],
                ["Home", "Lights, cameras, app-driven appliances, voice", "Turn lights off from the bus"],
                ["Farming", "Moisture and weather, automatic water, drones over fields", "Wheat, rice, cotton, sugarcane; water is scarce"],
            ],
            col_widths=[80, 230, 185],
        ),
        Spacer(1, 8),
        h2(s, "5.5 AI in Pakistani classrooms"),
        p(s, "Already visible: LMS platforms, post-COVID virtual classes, auto-marked quizzes, career hints from performance data, government digital-education pushes. Benefits: self-paced study, teacher time saved, early help for struggling students, access for some disabilities, better institutional decisions. Friction: weak rural internet, missing devices, untrained teachers, cost, privacy, and the risk of treating the tool as the teacher."),
        h2(s, "5.6 Information sources"),
        p(s, "The internet is a warehouse, not a librarian. You must sort what you pick up."),
        simple_table(
            s,
            ["Kind", "What it is", "Examples", "Goes bad when"],
            [
                ["Primary", "First-hand, original", "Interview, diary, photo, NADRA CNIC file", "Incomplete, wrongly recorded, or false"],
                ["Secondary", "Someone already explained the primary", "Textbook, news, PBS summary of a census", "Out of date, no references, no expert check"],
                ["Tertiary", "Quick digest of the first two", "Encyclopedia, dictionary, many Wikipedia pages", "Unknown site, too simple, no trail"],
            ],
            col_widths=[75, 130, 160, 130],
        ),
        Spacer(1, 6),
        p(s, "NADRA is primary because the citizen stood there and the state verified the fingerprints. A PBS report of that data is secondary. A one-paragraph wiki summary is tertiary. A nameless social-media post with no date and no source is simply unreliable — do not cite it."),
        h2(s, "5.7 Impacts — hold both handles"),
        simple_table(
            s,
            ["Field", "Help", "Harm"],
            [
                ["Education", "Online class, e-books, flexible hours", "Screen fatigue, weaker attention"],
                ["Communication", "Mail, chat, video across cities", "Less face-to-face skill"],
                ["Business", "Faster shops, digital banks, automation", "Some traditional jobs shrink"],
                ["Healthcare", "Records, telemedicine, smart devices", "Leaked patient data"],
                ["Agriculture", "Forecasts, smart irrigation", "Tools never reach offline villages"],
                ["Daily life", "Saved time, convenience", "Helplessness when the battery dies"],
            ],
            col_widths=[95, 200, 200],
        ),
        Spacer(1, 6),
        p(s, "Responsible use, as a student checklist: protect personal data, strong unique passwords, do not forward rumours, be civil online, use the machine to learn, and put the phone down and walk. Computing creates jobs and deletes jobs; it connects and isolates. Your job is to notice both and choose."),
        h2(s, "5.8 Assistive technologies"),
        p(s, "These are devices and programs that let people with disabilities join school, work, and street life. They are not “special gadgets for someone else.” A caption on a video helps a deaf classmate and also you in a noisy bus."),
        simple_table(
            s,
            ["Family", "Examples", "Picture"],
            [
                ["Mobility", "Wheelchair, walker, crutches, stair lift", "Getting to the next classroom"],
                ["Sensory", "Hearing aid, screen reader (NVDA, VoiceOver), Braille, white cane, magnifier", "Text becomes speech"],
                ["Communication", "Speech-generating device, text-to-speech, picture board", "A child points to “water”"],
                ["Cognitive / learning", "Spell-check, audiobook, reminders, mind maps, planners", "A reader who listens to the chapter"],
            ],
            col_widths=[110, 220, 165],
        ),
        Spacer(1, 6),
        p(s, "Why they matter: equal lessons, clearer talk, independence, better rehab data, a fairer workplace, a society that does not build stairs-only buildings. Careers: accessibility software, AI for recognition, biomedical devices, inclusive UX, rehabilitation technology. Skills: code, design, some health knowledge, patience, empathy."),
        h2(s, "5.9 Career sketch for this unit"),
        p(s, "IoT engineer, embedded engineer, network engineer, data analyst, system administrator; AI / ML engineer; assistive-software developer. Shared skills: Python or C++, electronics, Wi-Fi/Bluetooth thinking, cleaning data, explaining a system to a non-engineer, and ethics."),
        h2(s, "5.10 Recap"),
        p(s, "Sensors collect, analytics explain, AI decides, actuators move. Sources have a pedigree. Every convenience has a bill. Assistive tech is how computing keeps its promise to everyone, not only the already able."),
        h2(s, "5.11 Self-test"),
    ]
    story += numbered(s, [
        "A watch sends heart-rate to a phone. Which technology is that, mainly?",
        "In irrigation, which device judges dry versus wet soil? Which device opens the water?",
        "Removing duplicate student rows is which analytics step?",
        "Is an interview primary, secondary, or tertiary?",
        "Name two reasons a website might be unreliable.",
        "Give one positive and one negative impact of computing on healthcare.",
        "What does a screen reader do?",
        "List the six IoT components.",
    ])
    story += [
        h2(s, "5.12 Answers"),
        p(s, "<b>1.</b> IoT (sensing + connectivity). AI may sit in the phone app; do not lead with AI.  <b>2.</b> Sensor; actuator (valve).  <b>3.</b> Data cleaning.  <b>4.</b> Primary.  <b>5.</b> No author, no date, no references, sensational tone, unknown domain.  <b>6.</b> + telemedicine / digital records; − leaked files if security is weak.  <b>7.</b> Speaks on-screen text for a person who cannot see it well.  <b>8.</b> Sensors, actuators, connectivity, data processing, cloud, user interface.", "Answer"),
        PageBreak(),
    ]
    return story
