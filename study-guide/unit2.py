"""Unit 2 — Computational Thinking and Algorithms."""

from reportlab.platypus import PageBreak, Spacer

from pdf_kit import Callout, bullets, code_block, h1, h2, h3, numbered, p, simple_table


def build(styles):
    s = styles
    story = [
        h1(s, "Unit 2 — Computational Thinking and Algorithms"),
        p(s, "Computational thinking is not “thinking like a computer.” It is thinking so clearly that a computer — or another human — can follow you. Four habits do the work: decompose the mess, spot the pattern, hide the noise, write the steps.", "Lead"),
        h2(s, "2.1 What you must be able to do"),
    ]
    story += bullets(s, [
        "Define an algorithm and contrast it with pseudocode.",
        "Apply decomposition, pattern recognition, and abstraction to a real task.",
        "Trace Bubble Sort and Selection Sort on a short list, counting comparisons and swaps.",
        "Trace Linear Search and Binary Search, and say when each is the right tool.",
        "Judge an algorithm on correctness, efficiency, and clarity.",
    ])
    story += [
        h2(s, "2.2 Algorithm versus pseudocode"),
        p(s, "An <b>algorithm</b> is a finite, language-independent sequence of logical steps that solves a problem. It is the recipe, not the cooked dish. <b>Pseudocode</b> is that recipe written with programming-shaped words (IF, FOR, WHILE) but without a compiler’s punctuation. You write the algorithm to know <i>what</i> must happen; you write pseudocode to show <i>how</i> it will look just before real code."),
        simple_table(
            s,
            ["", "Algorithm", "Pseudocode"],
            [
                ["Audience", "Anyone who can follow logic", "Someone about to code"],
                ["Form", "Numbered steps, everyday language", "Structured keywords, indentation"],
                ["Syntax", "None required", "Conventions, still not executable"],
                ["Purpose", "Get the logic right", "Bridge logic to a language"],
            ],
            col_widths=[90, 200, 205],
        ),
        Spacer(1, 8),
        Callout(s, "why", "Every program you will write in Unit 3 is an algorithm wearing Python clothes. If the algorithm is wrong, prettier syntax will not save it."),
        h2(s, "2.3 Three algorithmic strategies"),
        h3(s, "Decomposition"),
        p(s, "Split a large problem into parts you can finish and test alone. Learning a language is not “learn Spanish.” It is alphabet, vocabulary, grammar, tenses, sentence practice, listening, feedback. In software, a school app becomes login, timetable, results, attendance — each a module. When something breaks, you know which piece to open."),
        h3(s, "Pattern recognition"),
        p(s, "Ask: what repeats, and what changes on a rule? A triangle of stars that grows by one star per row is a loop from 1 to n, printing i stars. Patterns become loops, conditions, and reusable functions. Without this habit you rewrite the same logic ten times."),
        h3(s, "Abstraction"),
        p(s, "Keep what changes the answer; drop what only decorates. Making tea, abstracted: boil water, add tea, steep, pour, serve. Brand of kettle, cup colour, and kitchen location do not belong in the algorithm. They are noise. Abstraction is how a “sort any list of comparable items” routine can sort marks, names, or dates."),
        Callout(s, "exam", "Ignoring kettle brand while describing tea-making is <b>abstraction</b>, not decomposition. Decomposition would be listing the separate subtasks. Pattern recognition would be noticing that every hot drink shares “heat liquid → infuse → pour.”"),
        h2(s, "2.4 Sorting — putting a list in order"),
        p(s, "Sorting arranges items ascending, descending, or by time. Searching, filtering, and ranking all get cheaper on ordered data. This syllabus asks you to own two simple sorts. Neither is used on a million records in industry; both are used to teach nested loops and swaps."),
        h3(s, "Bubble Sort (ripple sort)"),
        p(s, "Walk along the list. Whenever two neighbours are in the wrong order, swap them. After pass 1 the largest item has “bubbled” to the end. After pass 2 the next-largest is parked. After n−1 passes the list is sorted. An inner pointer stops one place earlier each pass because the tail is already finished."),
        p(s, "Trace {8, 4, 1, 9, 3} ascending:"),
    ]
    story += bullets(s, [
        "Pass 1: 8↔4 → 4,8,1,9,3; 8↔1 → 4,1,8,9,3; 8&lt;9 no swap; 9↔3 → 4,1,8,3,9. Nine sits.",
        "Pass 2: 4↔1 → 1,4,8,3,9; 4&lt;8; 8↔3 → 1,4,3,8,9. Eight sits.",
        "Pass 3: 1&lt;4; 4↔3 → 1,3,4,8,9. Four sits.",
        "Pass 4: 1&lt;3. Done. Sorted: 1, 3, 4, 8, 9.",
    ])
    story += [
        code_block(
            s,
            """FOR pass = 0 TO n-2
    FOR i = 0 TO n-2-pass
        IF DATA[i] > DATA[i+1] THEN
            swap DATA[i] and DATA[i+1]
        END IF
    END FOR
END FOR""",
        ),
        p(s, "<b>Strengths:</b> easy to see; in-place (no extra array); stable (equal keys keep their order). <b>Weaknesses:</b> nested loops, so time grows about with n²; many swaps (three assignments each); hopeless for large data."),
        h3(s, "Selection Sort"),
        p(s, "On pass k, find the smallest item in the unsorted tail and swap it into position k. At most one swap per pass. Trace {8, 4, 1, 9, 3}:"),
    ]
    story += bullets(s, [
        "Pass 0: smallest of the whole list is 1; swap with 8 → {1, 4, 8, 9, 3}.",
        "Pass 1: smallest of the tail is 3; swap with 4 → {1, 3, 8, 9, 4}.",
        "Pass 2: smallest of the tail is 4; swap with 8 → {1, 3, 4, 9, 8}.",
        "Pass 3: smallest of the tail is 8; swap with 9 → {1, 3, 4, 8, 9}.",
    ])
    story += [
        p(s, "Textbook traces sometimes swap as soon as a smaller value is seen (a selection-sort cousin). The standard form finds the <i>index</i> of the minimum, then swaps once. In an exam, follow the version your teacher traced, but understand both."),
        p(s, "<b>Strengths:</b> simple; few writes (good when writing is expensive); in-place. <b>Weaknesses:</b> still n² comparisons; does not notice an already-sorted list; not stable; still only for small n. Merge Sort would sort a million items while Bubble Sort was still warming up — know that fact even though Merge Sort is not in this unit."),
        Callout(s, "try", "Hand-trace both sorts on {5, 1, 4, 2}. Count swaps. Selection Sort should use fewer swaps. Then sort the names Ahmed, Zara, Bilal, Amina descending by hand — that is the same algorithm on letters."),
        h2(s, "2.5 Searching"),
        h3(s, "Linear (sequential) search"),
        p(s, "Look at item 1, then 2, then 3, … until you find the target or run out. Works on sorted or unsorted data. One loop. No extra memory. For 10 classroom numbers it is faster than a clever method that needs setup. For a million records with the target at the end, you do a million checks."),
        p(s, "Example: find 7 in {8, 3, 6, 1, 7, 2, 4, 5}. Compare 8, 3, 6, 1, 7 — found at the fifth look."),
        h3(s, "Binary search — only on sorted data"),
        p(s, "Look at the middle. If it is the target, stop. If the target is smaller, throw away the right half. If larger, throw away the left half. Repeat. Each step halves the remaining work. A million items take about 20 looks. A billion take about 30."),
        p(s, "Find 3 in the sorted list {1, 2, 3, 4, 5, 6, 7, 8}. Mid ≈ 4. 3 &lt; 4, keep left {1, 2, 3}. Mid ≈ 2. 3 &gt; 2, keep right {3}. Found. Use integer mid = INT((low+high)/2). Off-by-one errors (looping forever, or skipping the last cell) are the usual bug — draw the shrinking interval every time."),
        simple_table(
            s,
            ["", "Linear", "Binary"],
            [
                ["Needs sorted data?", "No", "Yes — or you must sort first"],
                ["Idea", "Check one by one", "Halve the interval"],
                ["Best for", "Small or unsorted lists; one-off search", "Large static sorted lists, many searches"],
                ["Risk", "Slow on huge n", "Logic / off-by-one; fails if unsorted"],
                ["Extra memory", "None", "None (iterative form)"],
            ],
            col_widths=[120, 190, 185],
        ),
        Spacer(1, 8),
        Callout(s, "mistake", "Binary search on an unsorted list is not “a bit worse.” It is wrong. The discarded half may contain the target."),
        h2(s, "2.6 Judging an algorithm"),
    ]
    story += numbered(s, [
        "<b>Correctness.</b> Right output for every valid input, including empties, zeros, negatives. It must finish — no infinite loop. A MOD-2 even/odd test is correct because remainder 0 ↔ even for every integer you try.",
        "<b>Efficiency.</b> Time as n grows, and memory used. Linear search time grows with n; binary search grows with log n on sorted data. Ask: does it still finish if the file is 100 times larger?",
        "<b>Clarity.</b> Named variables, indentation, comments, obvious IF/LOOP structure. The next reader (often future-you) must be able to change it.",
    ])
    story += [
        h3(s, "A short decision guide"),
    ]
    story += bullets(s, [
        "Unsorted search → Linear Search.",
        "Sorted search, large n, many queries → Binary Search.",
        "Need order → a sorting algorithm (Bubble/Selection here; faster sorts later in life).",
        "Same sub-problem repeats → think dynamic programming (awareness only at this level).",
        "Tiny n, teaching, or writing is expensive → simplicity or few swaps can beat a “faster” famous algorithm.",
    ])
    story += [
        Callout(s, "exam", "“Which search for a large sorted dataset?” Binary Search. Always add the reason: logarithmic steps, but only after the list is ordered."),
        h2(s, "2.7 Recap"),
        p(s, "CT = decompose + recognise + abstract + algorithm. Bubble Sort swaps neighbours; Selection Sort parks the next minimum. Linear Search walks; Binary Search halves a sorted list. Prefer the algorithm that is correct first, clear second, and only then as fast as the data size demands."),
        h2(s, "2.8 Self-test"),
    ]
    story += numbered(s, [
        "Define an algorithm in one sentence.",
        "Which CT strategy is “ignore the mug colour when describing tea”?",
        "Bubble Sort is also called what?",
        "Why does Selection Sort often perform fewer swaps than Bubble Sort?",
        "Give one advantage and one limitation of Binary Search.",
        "What do BEG, END, and MID stand for in the binary-search write-up?",
        "When is Linear Search the better choice?",
        "Name the three evaluation criteria in this unit.",
    ])
    story += [
        h2(s, "2.9 Answers"),
        p(s, "<b>1.</b> A finite, language-independent sequence of logical steps that solves a problem.", "Answer"),
        p(s, "<b>2.</b> Abstraction.", "Answer"),
        p(s, "<b>3.</b> Ripple sort.", "Answer"),
        p(s, "<b>4.</b> Each pass does at most one swap after the minimum is found; Bubble Sort may swap on almost every comparison.", "Answer"),
        p(s, "<b>5.</b> Advantage: ~20 probes for a million items. Limitation: data must already be sorted; jumping to mid needs random access (arrays).", "Answer"),
        p(s, "<b>6.</b> Beginning, end, and middle index of the current interval.", "Answer"),
        p(s, "<b>7.</b> Unsorted data, very small n, or a single search where sorting first would cost more than walking the list.", "Answer"),
        p(s, "<b>8.</b> Correctness, efficiency, clarity.", "Answer"),
        PageBreak(),
    ]
    return story
