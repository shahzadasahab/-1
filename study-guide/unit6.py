"""Unit 6 — Digital Literacy."""

from reportlab.platypus import PageBreak, Spacer

from pdf_kit import Callout, bullets, h1, h2, h3, numbered, p, simple_table


def build(styles):
    s = styles
    story = [
        h1(s, "Unit 6 — Digital Literacy"),
        p(s, "Digital literacy is not “I can open Chrome.” It is the ability to find information, judge it, gather new evidence, and show the result without harming anyone’s privacy or stealing anyone’s words. In the Information Age the flood is instant; the skill is the filter.", "Lead"),
        h2(s, "6.1 What you must be able to do"),
    ]
    story += bullets(s, [
        "Use advanced search (quotes, filetype:, site:) and evaluate a source.",
        "Tell qualitative from quantitative, primary from secondary data.",
        "Choose and design interviews, surveys, prototypes, observation, or simulation.",
        "Plan an ethical data-collection approach for a research question.",
        "Present findings in a spreadsheet, slides, infographic, report, or dashboard.",
        "Ship a digital artefact that actually answers the question.",
    ])
    story += [
        h2(s, "6.2 Two ways data can look"),
        simple_table(
            s,
            ["", "Qualitative", "Quantitative"],
            [
                ["Nature", "Words, reasons, feelings", "Numbers you can count or measure"],
                ["Ask", "Why / how", "How many / how much"],
                ["Examples", "“Notifications break my focus”", "4 hours/day, 72% feel distracted"],
                ["Typical tools", "Interview notes, open questions", "Tallies, averages, charts"],
            ],
            col_widths=[90, 200, 205],
        ),
        Spacer(1, 6),
        p(s, "Good projects often collect both. Hours of phone use (quantitative) plus the sentence “I open Instagram when a chapter is hard” (qualitative) explain each other."),
        h2(s, "6.3 Primary versus secondary data"),
        p(s, "<b>Primary data</b> is what you gather for this question: your survey, your interview, your observation, your experiment. You control the wording. <b>Secondary data</b> already exists: a PBS table, a research PDF, a government site. You do not control how it was collected, so you must say so."),
        p(s, "Related but not identical: Unit 5’s primary/secondary/tertiary <i>sources</i> are about documents. Unit 6’s primary/secondary <i>data</i> is about whether <b>you</b> collected the numbers. A NADRA record is a primary source; if you download a published NADRA statistic for your project, that statistic is secondary data for you."),
        h2(s, "6.4 Five ways to collect original data"),
        simple_table(
            s,
            ["Method", "Best when", "Watch out"],
            [
                ["Interview", "You need depth from a few people", "Time; interviewer bias; hard to tally"],
                ["Survey / form", "The same questions for many people", "Poor wording; tiny or biased sample"],
                ["Prototype", "You are testing an idea of a product", "Feedback is about the mock-up, not the final"],
                ["Observation", "Behaviour matters more than opinions", "People change when watched; privacy"],
                ["Simulation", "The real trial is costly, risky, or slow", "The model may not match the world"],
            ],
            col_widths=[95, 200, 200],
        ),
        Spacer(1, 6),
        p(s, "Google Forms and Microsoft Forms will host a survey, timestamp replies, and draw baby charts. Use closed items for counts and one or two open items for voice."),
        h2(s, "6.5 Designing the approach — eight steps"),
    ]
    story += numbered(s, [
        "Write one sharp research question. “How does daily mobile use affect Class XI study habits?” is a question. “Mobiles and youth” is a fog.",
        "Decide qualitative, quantitative, or mixed.",
        "Pick methods that can actually answer it.",
        "Choose a sample that resembles the group (30–50 classmates from more than one section is a start, not a national poll).",
        "Build the tools: form, interview script, observation sheet.",
        "Collect carefully. Do not “help” people toward the answer you like.",
        "Store in a spreadsheet and keep a backup.",
        "Ethics: permission first, no extra personal fields, no names unless needed, private storage, educational use only.",
    ])
    story += [
        Callout(s, "mistake", "A decorated Canva file is not an artefact if it never answers the research question. Evidence → claim → recommendation. Decoration last."),
        h2(s, "6.6 Searching like a researcher"),
        p(s, "Quotes keep a phrase intact: \"mobile phone use\" \"study habits\". <b>filetype:pdf</b> prefers reports. <b>site:.edu</b> or site:.gov.pk stays in a family of hosts. Combine them: \"internet usage in Pakistan\" filetype:pdf."),
        p(s, "Then interrogate each hit: Is an author or organisation named? Is it recent? Is it educational, governmental, or research-based? Are there facts and references? Is it balanced? Fail two of these and keep walking."),
        h2(s, "6.7 Showing the data"),
        simple_table(
            s,
            ["Tool", "Use it to", "Examples"],
            [
                ["Spreadsheet", "Grid, formulas, sort, filter, charts", "Excel, Google Sheets, Numbers"],
                ["Slides", "Talk an audience through findings", "PowerPoint, Slides, Canva, Gamma"],
                ["Infographic", "One-page visual argument", "Canva, Express, Power BI"],
                ["Report", "Full method + evidence + conclusion", "Word, Docs, Notion"],
                ["Dashboard", "Interactive filters", "Power BI, Tableau, Looker Studio"],
            ],
            col_widths=[95, 200, 200],
        ),
        Spacer(1, 6),
        p(s, "Match visual to message: table for exact values, bar for categories, line for time, pie for a few shares of a whole. AI helpers (Copilot, Gemini, Magic Write) may tidy sentences; they must not invent percentages. You remain the author."),
        h2(s, "6.8 Case study you can copy as a template"),
        p(s, "<b>Question:</b> How does daily mobile phone use affect the study habits of students?"),
        p(s, "<b>Why it matters:</b> the same device is a library and a casino. The class will not accept a sermon; they will accept evidence."),
        p(s, "<b>Data mix:</b> hours online, yes/no “I use it to study,” main activity, distraction (quant). Two open questions on help and harm (qual). One or two secondary PDFs for comparison."),
        p(s, "<b>Sample survey items:</b> (1) Hours per day? (2) Used for study? (3) Main activity? (4) Does it distract you? (5) Study hours without the phone? (6) How does it help? (7) What problems appear? (8) One rule for wiser use?"),
        p(s, "<b>Ethics in action:</b> ask first; do not store phone numbers; aggregate before you present (“Student 1, 2, 3” not real names)."),
        p(s, "<b>Spreadsheet columns:</b> id | daily hours | study use | main app | distracted | study hours | comment. Then compute average phone time, average study time, percent distracted, mode activity."),
        p(s, "<b>Minimum visuals:</b> bar of hour-bands; pie of main purpose; column of yes / no / sometimes distracted."),
        p(s, "<b>A plausible reading</b> (your numbers will differ): many students live on the phone 3–5 hours; about half use it for lectures and notes; social notifications still steal focus; students who treat the phone as a tool manage time better than those who treat it as entertainment. Conclusion: do not ban the device; teach limits — mute notifications, educational apps in study blocks, planned offline minutes."),
        h3(s, "Artefact skeleton (every one of these headings)"),
    ]
    story += numbered(s, [
        "Title",
        "Research question",
        "Introduction",
        "Method (who, how, ethics)",
        "Primary findings",
        "Secondary-source comparison",
        "Charts",
        "Conclusion",
        "Recommendations",
        "References (no silent copying — that is plagiarism)",
    ])
    story += [
        h2(s, "6.9 Recap"),
        p(s, "Literacy = search + judge + collect + respect people + show the answer. Primary data is yours; secondary data is borrowed with a citation. The artefact is a structured argument, not a collage."),
        h2(s, "6.10 Self-test"),
    ]
    story += numbered(s, [
        "Define digital literacy in one sentence of your own.",
        "A classmate describes how the phone wrecks her concentration. Qualitative or quantitative?",
        "Best search for a reliable PDF on internet use in Pakistan?",
        "Survey replies you collected this week are what kind of data?",
        "What does the site: operator do?",
        "Copying a paragraph without credit is called?",
        "Why ask permission before a survey?",
        "Name three presentation tools listed in this unit.",
    ])
    story += [
        h2(s, "6.11 Answers"),
        p(s, "<b>1.</b> Any sentence that includes find, evaluate, create/communicate, and responsible use.  <b>2.</b> Qualitative.  <b>3.</b> \"internet usage in Pakistan\" filetype:pdf.  <b>4.</b> Primary.  <b>5.</b> Restricts results to a site or domain.  <b>6.</b> Plagiarism.  <b>7.</b> Research ethics / consent / privacy.  <b>8.</b> PowerPoint, Google Slides, Canva (or Word/Sheets/Tableau — any three from the tables).", "Answer"),
        PageBreak(),
    ]
    return story
