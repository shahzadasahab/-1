#!/usr/bin/env python3
"""Generate the Class XI Computer Science teach-yourself study guide PDF."""

from __future__ import annotations

import os

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    NextPageTemplate,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

import extra_drills
import unit1
import unit2
import unit3
import unit4
import unit5
import unit6
from pdf_kit import (
    BOTTOM,
    CREAM,
    GOLD,
    LEFT,
    LINE,
    NAVY,
    PAGE_H,
    PAGE_W,
    PALE,
    RIGHT,
    TEAL,
    TOP,
    WHITE,
    Callout,
    ColoredRule,
    bullets,
    h1,
    h2,
    h3,
    numbered,
    p,
    register_fonts,
    simple_table,
    stylesheet,
)

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "Class_XI_Computer_Science_Teach_Yourself_Study_Guide.pdf")


class GuideDoc(BaseDocTemplate):
    def __init__(self, path, styles):
        super().__init__(
            path,
            pagesize=A4,
            leftMargin=LEFT,
            rightMargin=RIGHT,
            topMargin=TOP,
            bottomMargin=BOTTOM,
            title="Class XI Computer Science — Teach Yourself Study Guide",
            author="Self-study companion to the Sindh Textbook Board Class XI Computer Science syllabus",
            subject="Digital logic, algorithms, Python, databases, IoT, digital literacy",
        )
        self.styles = styles
        cover = PageTemplate("cover", frames=[Frame(0, 0, PAGE_W, PAGE_H, id="c")], onPage=self._cover_bg)
        body = PageTemplate(
            "body",
            frames=[Frame(LEFT, BOTTOM, PAGE_W - LEFT - RIGHT, PAGE_H - TOP - BOTTOM, id="b")],
            onPage=self._body_chrome,
        )
        self.addPageTemplates([cover, body])

    def _cover_bg(self, canv, doc):
        canv.saveState()
        canv.setFillColor(NAVY)
        canv.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
        canv.setFillColor(TEAL)
        canv.rect(0, 0, 14 * mm, PAGE_H, fill=1, stroke=0)
        canv.setFillColor(GOLD)
        canv.rect(14 * mm, 0, 2.2 * mm, PAGE_H, fill=1, stroke=0)
        canv.setFillColor(TEAL)
        canv.rect(0, 28 * mm, PAGE_W, 18 * mm, fill=1, stroke=0)
        canv.setFillColor(WHITE)
        canv.setFont("Sans", 9)
        canv.drawString(24 * mm, 35 * mm, "Self-paced  •  Worked examples  •  Closed-book drills  •  Full answer keys")
        canv.restoreState()

    def _body_chrome(self, canv, doc):
        canv.saveState()
        canv.setFillColor(NAVY)
        canv.rect(0, PAGE_H - 12 * mm, PAGE_W, 12 * mm, fill=1, stroke=0)
        canv.setFillColor(GOLD)
        canv.rect(0, PAGE_H - 12.8 * mm, PAGE_W, 1.1 * mm, fill=1, stroke=0)
        canv.setFillColor(WHITE)
        canv.setFont("Sans", 8)
        canv.drawString(LEFT, PAGE_H - 8 * mm, "Class XI Computer Science  ·  Teach Yourself Study Guide")
        canv.drawRightString(PAGE_W - RIGHT, PAGE_H - 8 * mm, "Sindh Textbook Board syllabus")
        canv.setStrokeColor(LINE)
        canv.setLineWidth(0.4)
        canv.line(LEFT, 12 * mm, PAGE_W - RIGHT, 12 * mm)
        canv.setFillColor(NAVY)
        canv.setFont("Sans", 8)
        canv.drawString(LEFT, 7 * mm, "Original teaching companion  ·  Not a reprint of the textbook")
        canv.drawRightString(PAGE_W - RIGHT, 7 * mm, f"{doc.page}")
        canv.restoreState()


def cover(styles):
    s = styles
    story = [NextPageTemplate("cover"), Spacer(1, 58 * mm)]
    story.append(Paragraph("SINDH  ·  CLASS XI  ·  COMPUTER SCIENCE", s["CoverKicker"]))
    story.append(Spacer(1, 10))
    story.append(ColoredRule(GOLD, 1.4, 4, 14, width=120 * mm))
    story.append(Paragraph("Teach Yourself", s["CoverTitle"]))
    story.append(Spacer(1, 4))
    story.append(Paragraph("Study Guide", s["CoverTitle"]))
    story.append(Spacer(1, 14))
    story.append(Paragraph(
        "An in-depth, self-paced companion covering Digital Logic, SDLC,<br/>"
        "Networks, Algorithms, Python, Databases, IoT &amp; AI,<br/>"
        "and Digital Literacy — with traces, labs, and answers.",
        s["CoverSub"],
    ))
    story.append(Spacer(1, 28))
    story.append(Paragraph("Read  ·  Try  ·  Check  ·  Recite  ·  Review", s["CoverKicker"]))
    story += [NextPageTemplate("body"), PageBreak()]
    return story


def front_matter(styles):
    s = styles
    story = [
        h1(s, "How to teach yourself with this book"),
        p(s, "This guide was written for a student who may not have a coach in the room. It follows the Class XI Computer Science syllabus used by the Sindh Textbook Board (units on computer systems, computational thinking, Python, data and analysis, applications of computing, and digital literacy). It is a companion, not a photocopy: explanations, traces, and drills are original, so you still need your textbook for official figures, LogiSim screenshots, and board-prescribed wording.", "Lead"),
        h2(s, "The five-pass method"),
    ]
    story += numbered(s, [
        "<b>Read for the map.</b> Skim headings and the “what you must be able to do” list. Spend ten minutes, not an hour.",
        "<b>Read for the mechanism.</b> When you hit a worked example, cover the answer with a card and attempt it first. If you only watch, you will recognise the idea and still fail the paper.",
        "<b>Try this now.</b> Every amber box is a mini exam. Write on paper. Then uncover the unit answers.",
        "<b>Recite.</b> Close the guide. Say the seven gates, the six SDLC phases, the OSI mnemonic, the three error types, the four keys. If a list will not come, that list is your next revision card.",
        "<b>Review on a schedule.</b> Tomorrow, next week, next month. Memory is a muscle; unused circuits fade.",
    ])
    story += [
        Callout(s, "key", "Understanding is not the same as recall. You can follow a binary-search trace today and still blank on BEG/END/MID in the exam. Recitation is not childish. It is how professionals keep protocols in their heads."),
        h2(s, "What “done” looks like for a unit"),
    ]
    story += bullets(s, [
        "You can teach the core idea to a classmate in three minutes without notes.",
        "You have hand-traced at least one full example (truth table, sort, search, query, or IoT chain).",
        "You scored the unit self-test closed-book and corrected every miss in writing.",
        "You can name the favourite exam traps listed in the green and rose boxes.",
    ])
    story += [
        h2(s, "Suggested eight-week plan"),
        p(s, "Treat a “week” as five honest sessions of 50–70 minutes. Stretch if Python or Access labs need more lab time; do not skip the recitation days."),
        simple_table(
            s,
            ["Week", "Focus", "Must-finish artefact"],
            [
                ["1", "Unit 1 logic: signals, gates, tables, K-maps", "One LogiSim circuit + its table"],
                ["2", "Unit 1 SDLC + OSI/TCP-IP", "Waterfall vs Agile table from memory; ping reflection"],
                ["3", "Unit 2 CT + both sorts", "Two full traces on a new 6-item list"],
                ["4", "Unit 2 search + evaluation; start Unit 3", "Binary search on a sorted register"],
                ["5", "Unit 3 Python: types, operators, if/loops", "Calculator + even/odd programs run in VS Code"],
                ["6", "Unit 3 libraries/debug; Unit 4 ER + keys", "ATM or report-card program; one ER diagram"],
                ["7", "Unit 4 Access objects; Unit 5 IoT/AI/sources", "One grouped query; irrigation long answer"],
                ["8", "Unit 6 inquiry + mixed revision paper", "Mini artefact (slides or one-page infographic) + practice exam"],
            ],
            col_widths=[50, 210, 235],
        ),
        Spacer(1, 8),
        h2(s, "Materials"),
    ]
    story += bullets(s, [
        "This PDF, your textbook, a notebook used only for traces.",
        "Python 3 and VS Code (Python extension) — or an online interpreter when a lab is closed.",
        "LogiSim Evolution (Java 21+) for Unit 1.",
        "Microsoft Access if your centre assesses practical database work.",
        "A browser for Forms, Sheets, and advanced search practice.",
    ])
    story += [
        h2(s, "Contents"),
        p(s, "<b>Unit 1</b>  Computer Systems — digital logic, SDLC, OSI &amp; TCP/IP + studio", "TOCItem"),
        p(s, "<b>Unit 2</b>  Computational Thinking &amp; Algorithms — CT, sort, search + traces", "TOCItem"),
        p(s, "<b>Unit 3</b>  Programming Fundamentals — Python, control, libraries, ATM lab", "TOCItem"),
        p(s, "<b>Unit 4</b>  Data and Analysis — ER, keys, Access, queries, clinic schema", "TOCItem"),
        p(s, "<b>Unit 5</b>  Applications &amp; Impacts — AI, IoT, sources, ethics, assistive tech", "TOCItem"),
        p(s, "<b>Unit 6</b>  Digital Literacy — search, collect, present, 90-minute inquiry", "TOCItem"),
        p(s, "<b>Final week</b>  Three-day mixed drills without a teacher", "TOCItem"),
        p(s, "<b>Mixed paper</b>  40-mark closed-book rehearsal with full mark scheme", "TOCItem"),
        p(s, "<b>Quick cards &amp; glossary</b>  Last-night recitation sheets", "TOCItem"),
        PageBreak(),
    ]
    return story


def mixed_exam(styles):
    s = styles
    story = [
        h1(s, "Mixed rehearsal paper (40 marks)"),
        p(s, "Time yourself for 60 minutes. No notes. Then mark with the scheme that follows. A ready student scores 28+ and can explain every miss.", "Lead"),
        h2(s, "Section A — Multiple choice (10 × 1 = 10)"),
    ]
    story += numbered(s, [
        "A digital signal has (a) infinite values (b) only two values (c) three values (d) ten values.",
        "XOR is 1 when inputs are (a) the same (b) different (c) both 0 (d) both 1.",
        "First SDLC phase: (a) Testing (b) Requirement analysis (c) Coding (d) Design.",
        "TCP/IP has (a) 3 (b) 4 (c) 5 (d) 7 layers.",
        "Which search needs sorted data? (a) Linear (b) Sequential (c) Binary (d) Bubble.",
        "input() returns (a) int (b) float (c) str (d) bool.",
        "A rectangle in an ER diagram is (a) attribute (b) relationship (c) entity (d) key.",
        "Soil moisture is read by a (a) actuator (b) sensor (c) monitor (d) hearing aid.",
        "Survey replies you collected yourself are (a) secondary (b) processed (c) primary (d) tertiary data.",
        "site: restricts a search to (a) file type (b) language (c) a domain (d) date.",
    ])
    story += [
        h2(s, "Section B — Short answers (6 × 2 = 12)"),
    ]
    story += numbered(s, [
        "Differentiate analog and digital signals in two crisp points.",
        "When would you choose Waterfall rather than Agile? One project feature is enough if it is precise.",
        "Why is Binary Search wrong on {9, 1, 4, 7} even if you “halve carefully”?",
        "State the difference between = and == in Python.",
        "What is referential integrity? Give a one-line school example.",
        "Classify a NADRA CNIC interview versus a textbook paragraph about NADRA.",
    ])
    story += [
        h2(s, "Section C — Structured (18 marks)"),
    ]
    story += numbered(s, [
        "<b>(6 marks)</b> Draw / list the truth table for Y = A′ · B + C and write the SOP minterms of the 1-rows.",
        "<b>(6 marks)</b> Trace Bubble Sort on {6, 2, 5, 1}. Show the list after each pass. Then say whether Selection Sort would use fewer swaps, and why.",
        "<b>(6 marks)</b> A farmer in Sindh wants automatic irrigation. Explain sensors, connectivity, processing, actuator, and UI. State where analytics and AI sit in the loop.",
    ])
    story += [
        h2(s, "Mark scheme"),
        p(s, "<b>A:</b> 1b, 2b, 3b, 4b, 5c, 6c, 7c, 8b, 9c, 10c.", "Answer"),
        p(s, "<b>B1.</b> Analog: continuous / many values / sine-like / noise-sensitive. Digital: two levels / square / noise-tolerant. (1+1)", "Answer"),
        p(s, "<b>B2.</b> Requirements fixed and known; hard deadline; familiar technology; small well-specified system. (2 for a precise feature + implication)", "Answer"),
        p(s, "<b>B3.</b> Binary search assumes order so it can discard a half. That list is unsorted; the target may sit in the discarded half. (2)", "Answer"),
        p(s, "<b>B4.</b> = stores a value; == tests equality and yields True/False. (1+1)", "Answer"),
        p(s, "<b>B5.</b> A child FK must match a living parent PK. You cannot store marks for StudentID 999 if that student does not exist. (1+1)", "Answer"),
        p(s, "<b>B6.</b> Interview / official capture = primary source. Textbook discussion = secondary source. (1+1)", "Answer"),
        p(s, "<b>C1.</b> 8 correctly ordered rows (3), helper or correct Y column (2), minterms for every 1-row ORed (1). Typical 1-rows: 001, 010, 011, 101, 111 → C + A′B.", "Answer"),
        p(s, "<b>C2.</b> Pass1 → 2,5,1,6; Pass2 → 2,1,5,6; Pass3 → 1,2,5,6 (3). Selection Sort does at most one swap per pass after finding the min, so usually fewer swaps (2) plus a correct reason (1).", "Answer"),
        p(s, "<b>C3.</b> One mark each for sensor, link, decide/process, valve/actuator, farmer UI, and placing analytics/AI on the decision side — max 6.", "Answer"),
        PageBreak(),
    ]
    return story


def cards_and_glossary(styles):
    s = styles
    story = [
        h1(s, "Quick recitation cards"),
        h2(s, "Card A — Gates in one glance"),
        p(s, "AND all 1s. OR any 1. NOT flip. NAND not-all-1s. NOR only all 0s. XOR different. XNOR same. NAND &amp; NOR are universal. Precedence: ( )  NOT  AND  OR. Rows = 2<sup>n</sup>. SOP: 1-rows, complement the zeros."),
        h2(s, "Card B — SDLC and models"),
        p(s, "Analyse (SRS) → Design → Code → Test → Deploy → Maintain (CAPP). Waterfall: freeze, late test, heavy docs. Agile: sprint, story, backlog, standup, change next cycle. Black box = behaviour; white box = code."),
        h2(s, "Card C — OSI downstairs"),
        p(s, "Please Do Not Throw Sausage Pizza Away. 1 bits / 2 frames+MAC / 3 packets+IP+router / 4 segments+TCP|UDP+ports / 5 session / 6 encrypt-compress-translate / 7 HTTP FTP SMTP DNS. TCP/IP: App | Transport | Internet | Access. ping = ICMP = layer 3."),
        h2(s, "Card D — Algorithms"),
        p(s, "Decompose / pattern / abstract. Bubble: swap neighbours, biggest sinks right. Selection: park next minimum, few swaps. Linear: any list. Binary: sorted only, mid = INT((lo+hi)/2). Judge: correct, cheap, clear."),
        h2(s, "Card E — Python"),
        p(s, "input → str. Indent 4. = vs ==. // floor, % remainder, ** power. and/or/not. &amp; | ^ ~ &lt;&lt; &gt;&gt;. for known count; while until. break leaves; continue skips. Syntax / runtime / logic. pip for strangers; math random datetime are housemates."),
        h2(s, "Card F — Data"),
        p(s, "Data → information. PK unique not null. FK points home. 1:1 / 1:M / M:N+junction. Cascade update/delete. Table store, form enter, query ask, report print. AND same row; OR different rows. Avg Count Sum Min Max."),
        h2(s, "Card G — Society and literacy"),
        p(s, "IoT collect, analytics speak, AI decide. Sensor ≠ actuator. Primary / secondary / tertiary. Assistive: move, sense, speak, learn. Quotes + filetype: + site:. Primary data = you collected it. Consent. No plagiarism. Artefact answers the question."),
        h1(s, "Glossary (selected)"),
        p(s, "Use this to sharpen definitions. The official textbook glossary is longer; these are the ones that win short-answer marks if you can say them cold."),
        simple_table(
            s,
            ["Term", "Unit", "Working definition"],
            [
                ["Abstraction", "2", "Hide extra detail; keep what changes the answer"],
                ["Actuator", "5", "Turns a digital command into a physical action"],
                ["Agile / Sprint", "1", "Short iterative build cycle, typically 2–4 weeks"],
                ["Algorithm", "2", "Finite language-free steps that solve a problem"],
                ["Binary search", "2", "Halve a sorted list until the target appears"],
                ["Bit", "1", "One binary digit: 0 or 1"],
                ["Black-box test", "1", "Check inputs/outputs without reading code"],
                ["Candidate key", "4", "Any unique non-null identifier; one becomes PK"],
                ["Cascade delete", "4", "Deleting a parent removes dependent child rows"],
                ["Decomposition", "2", "Break a hard job into finishable parts"],
                ["Digital artefact", "6", "Final digital product that answers a research question"],
                ["Encapsulation", "1", "Adding headers as data walks down the stack"],
                ["Entity", "4", "A real-world thing stored as a table"],
                ["Foreign key", "4", "Field that refers to another table’s primary key"],
                ["IDE", "3", "Editor + run + debug in one workplace"],
                ["IoT", "5", "Networked things that sense, share, and act"],
                ["Logical error", "3", "Runs, but the answer is wrong"],
                ["MAC address", "1", "Hardware address of a network interface"],
                ["Minterm", "1", "AND-term for one truth-table row where Y=1"],
                ["Primary data", "6", "Collected first-hand for this study"],
                ["Primary key", "4", "The one chosen unique identifier of a row"],
                ["Protocol", "1", "Agreed rules for formatting and exchanging data"],
                ["Pseudocode", "2", "Structured English just short of real syntax"],
                ["Query", "4", "A stored question that filters or summarises tables"],
                ["Referential integrity", "4", "Every FK value must match a living PK"],
                ["SDLC", "1", "Named phases from idea to maintained software"],
                ["Sensor", "5", "Reads a physical condition into data"],
                ["SRS", "1", "Signed list of what the software must do"],
                ["TCP", "1", "Reliable, connection-oriented transport"],
                ["Traceback", "3", "Python’s map of where an error exploded"],
                ["UDP", "1", "Fast, connectionless transport"],
                ["Universal gate", "1", "NAND or NOR: enough to build any other gate"],
                ["User story", "1", "A feature written from a user’s point of view"],
                ["Waterfall", "1", "Finish one phase completely before the next"],
            ],
            col_widths=[110, 40, 345],
            center_cols=[1],
        ),
        Spacer(1, 10),
        h1(s, "A last word"),
        p(s, "The board paper rewards people who can <i>do</i> a truth table, <i>trace</i> a sort, <i>write</i> a small program, <i>draw</i> an ER fragment, and <i>judge</i> a source — not people who only highlighted the textbook. If you have worked every “Try this” box and marked the rehearsal paper twice, you are no longer a passenger in this course. You are the teacher you were waiting for."),
        Callout(s, "note", "Revisit Card C and Card E the night before the paper. Those two cards carry an outsized share of MCQs. Sleep. A tired brain drops bits."),
    ]
    return story


def main():
    register_fonts()
    styles = stylesheet()
    doc = GuideDoc(OUT, styles)
    story = []
    story += cover(styles)
    story += front_matter(styles)
    story += unit1.build(styles)
    story += extra_drills.unit1_studio(styles)
    story += unit2.build(styles)
    story += extra_drills.unit2_studio(styles)
    story += unit3.build(styles)
    story += extra_drills.unit3_studio(styles)
    story += unit4.build(styles)
    story += extra_drills.unit4_studio(styles)
    story += unit5.build(styles)
    story += extra_drills.unit5_studio(styles)
    story += unit6.build(styles)
    story += extra_drills.unit6_studio(styles)
    story += extra_drills.closing_week(styles)
    story += mixed_exam(styles)
    story += cards_and_glossary(styles)
    doc.build(story)
    print(f"Wrote {OUT} ({os.path.getsize(OUT)} bytes)")


if __name__ == "__main__":
    main()
