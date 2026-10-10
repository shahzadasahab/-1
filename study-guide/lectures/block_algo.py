"""Lectures 9–12 — Computational thinking and algorithms."""

from lectures.kit import box, fig, lecture, table
from web import svgs


def lectures() -> str:
    return "".join([
        lecture(9, "Think so a machine can follow you", "Unit 2 · Computational Thinking", "45 min", [
            "Define an algorithm and contrast it with pseudocode.",
            "Name decomposition, pattern recognition, and abstraction on a school task.",
            "Judge an algorithm on correctness, efficiency, and clarity.",
        ], "\n".join([
            box("recap", "BLOCK B OPENS", "Unit 1 taught machines truth and conversation. Unit 2 teaches you to write steps so clear that a classmate — or Python — can follow them."),
            "<p>An <strong>algorithm</strong> is a finite, language-independent sequence of logical steps. It is the recipe, not the cooked dish. <strong>Pseudocode</strong> writes those steps with IF / FOR / WHILE but no compiler punctuation.</p>",
            table(["", "Algorithm", "Pseudocode"], [
                ["Audience", "Anyone who can follow logic", "Someone about to code"],
                ["Form", "Numbered everyday steps", "Structured keywords"],
                ["Syntax", "None required", "Conventions, still not executable"],
                ["Purpose", "Get the logic right", "Bridge logic to a language"],
            ]),
            "<ul>",
            "<li><strong>Decomposition</strong> — split “learn Spanish” into alphabet, vocabulary, grammar, practice. A school app becomes login, timetable, results.</li>",
            "<li><strong>Pattern recognition</strong> — a triangle of stars that grows by one star per row is a loop \\(i=1\\ldots n\\).</li>",
            "<li><strong>Abstraction</strong> — making tea is boil, add, steep, pour. Ignore mug colour and kettle brand.</li>",
            "</ul>",
            table(["Move", "Strategy"], [
                ["Split “build the app” into login, marks, notices", "Decomposition"],
                ["Every notice has a title, date, body — same shape", "Pattern recognition"],
                ["Ignore button colour when specifying “post a notice”", "Abstraction"],
                ["Write numbered steps before opening VS Code", "Algorithm"],
            ]),
            box("exam", "BOARD TRAP", "Ignoring the kettle brand is <strong>abstraction</strong>, not decomposition. Decomposition lists the subtasks. Pattern recognition notices that every hot drink shares “heat → infuse → pour.”"),
            "<p>Judge every algorithm on <strong>correctness</strong> (right for every valid input, and it finishes), <strong>efficiency</strong> (time and memory as \\(n\\) grows), and <strong>clarity</strong> (a classmate can maintain it).</p>",
            box("exit", "EXIT TICKET", "1. Define an algorithm in one sentence. 2. Which CT strategy ignores mug colour? 3. Name correctness, efficiency, clarity."),
            box("hw", "HOMEWORK", "Write an algorithm (not Python) for borrowing a library book. Mark one step as abstraction and one as decomposition."),
        ])),

        lecture(10, "Bubble Sort — neighbours swap", "Unit 2 · Algorithms", "45 min", [
            "Trace Bubble Sort on a 5-item list, pass by pass.",
            "Write the nested-loop pseudocode.",
            "State one strength and one weakness.",
        ], "\n".join([
            box("recap", "LAST LECTURE", "An algorithm is finite steps. Today the steps compare neighbours until the list is ordered."),
            "<p>Walk along the list. Whenever two neighbours are in the wrong order, swap them. After pass \\(k\\), the \\(k\\) largest items sit at the right. Nested loops give time that grows like \\(n^2\\).</p>",
            fig(svgs.bubble_sort_passes(), "Figure L10.1 — Trace of {8, 4, 1, 9, 3}. Teal cells are already parked."),
            "<pre>FOR pass ← 0 TO n−2\n    FOR i ← 0 TO n−2−pass\n        IF DATA[i] &gt; DATA[i+1] THEN swap</pre>",
            "<p>Diary of {8, 4, 1, 9, 3}: pass 1 ends {4, 1, 8, 3, <strong>9</strong>}; pass 2 ends {1, 4, 3, <strong>8, 9</strong>}; pass 3 ends {1, 3, <strong>4, 8, 9</strong>}; pass 4 confirms.</p>",
            "<p><strong>Strengths:</strong> easy to see; in-place; stable (equal keys keep their order). <strong>Weaknesses:</strong> many swaps; hopeless for large \\(n\\).</p>",
            "<p>Studio list \\(\\{6,2,5,1\\}\\): pass 1 → \\(\\{2,5,1,6\\}\\) (three swaps); pass 2 → \\(\\{2,1,5,6\\}\\); pass 3 → \\(\\{1,2,5,6\\}\\).</p>",
            box("exit", "EXIT TICKET", "1. After pass 1, where does the largest item sit? 2. Why is the inner loop shorter each pass? 3. Is Bubble Sort stable?"),
            box("hw", "HOMEWORK", "Trace {8, 3, 6, 2} on paper. Show the list at the end of each pass. Count swaps."),
        ])),

        lecture(11, "Selection Sort — park the minimum", "Unit 2 · Algorithms", "45 min", [
            "Trace Selection Sort on the same list as Lecture 10.",
            "Explain why it usually swaps less than Bubble Sort.",
            "State that it is not stable.",
        ], "\n".join([
            box("recap", "LAST LECTURE", "Bubble Sort swaps neighbours and parks the largest at the right. Selection Sort parks the next minimum at the left — at most one write per pass."),
            "<p>On pass \\(k\\), find the minimum of the unsorted tail and swap it into index \\(k\\). Still \\(\\Theta(n^2)\\) comparisons, fewer writes, <strong>not stable</strong>.</p>",
            fig(svgs.selection_sort_passes(), "Figure L11.1 — Same list {8, 4, 1, 9, 3}. Gold is the newly parked minimum."),
            "<ul>",
            "<li>Pass 0: smallest of the whole list is 1; swap with 8 → {1, 4, 8, 9, 3}.</li>",
            "<li>Pass 1: smallest of the tail is 3; swap with 4 → {1, 3, 8, 9, 4}.</li>",
            "<li>Pass 2: smallest of the tail is 4; swap with 8 → {1, 3, 4, 9, 8}.</li>",
            "<li>Pass 3: smallest of the tail is 8; swap with 9 → {1, 3, 4, 8, 9}.</li>",
            "</ul>",
            "<p>On \\(\\{6,2,5,1\\}\\) Selection finds min \\(1\\) and swaps once with \\(6\\) → \\(\\{1,2,5,6\\}\\). Watch equal keys: sort {9, 4, 7, 4, 1}. Bubble Sort should keep the first 4 ahead of the second. Selection Sort may swap their order — that single observation is a 3-mark “disadvantage” answer.</p>",
            box("exam", "TEXTBOOK COUSIN", "Some traces swap as soon as a smaller value is seen. Standard selection finds the <em>index</em> of the minimum, then swaps once. In the paper, follow the version your teacher traced."),
            box("exit", "EXIT TICKET", "1. How many swaps per pass in standard Selection Sort? 2. Why is it not stable? 3. Same time class as Bubble Sort?"),
            box("hw", "HOMEWORK", "Sort {9, 4, 7, 4, 1} with both algorithms. Circle the two 4s and see who keeps their order."),
        ])),

        lecture(12, "Linear search and binary search", "Unit 2 · Algorithms", "45 min", [
            "Trace linear search on unsorted data.",
            "Compute mid and discard a half on a sorted list.",
            "Say when binary search is simply wrong.",
        ], "\n".join([
            box("recap", "LAST LECTURE", "Two sorts, both \\(n^2\\). Searching asks a different question: is this value here, and where?"),
            "<p><strong>Linear search</strong> checks items \\(1,2,\\ldots,n\\). Works on unsorted data. Worst case \\(n\\) probes.</p>",
            "<p><strong>Binary search</strong> requires a sorted array. Each step uses</p>",
            r"\[ \mathrm{mid} = \left\lfloor \frac{\mathrm{low}+\mathrm{high}}{2} \right\rfloor. \]",
            "<p>If the target is smaller, set \\(\\mathrm{high}=\\mathrm{mid}-1\\); if larger, \\(\\mathrm{low}=\\mathrm{mid}+1\\). About \\(\\log_2 n\\) probes — twenty looks for a million items.</p>",
            fig(svgs.binary_search(), "Figure L12.1 — Find 3. Gold is mid; grey cells have been discarded."),
            "<p>Find 11 in \\(\\{2,5,7,11,13,17,19\\}\\): \\(\\mathrm{mid}=\\lfloor(0+6)/2\\rfloor=3\\), hit on the first probe. Find 2 (left edge): three looks. Find 12 (absent): finish with \\(\\mathrm{low}&gt;\\mathrm{high}\\) and report not found — write that failure case so you do not invent a crash.</p>",
            table(["", "Linear", "Binary"], [
                ["Needs sorted data?", "No", "Yes"],
                ["Idea", "One-by-one", "Halve the interval"],
                ["Best for", "Small or unsorted; one-off search", "Large static sorted lists"],
                ["Growth", "\\(O(n)\\)", "\\(O(\\log n)\\)"],
            ]),
            box("mistake", "COMMON MISTAKE", "Binary search on an unsorted list is not “a bit worse.” It is wrong: the discarded half may hold the target. {9, 1, 4, 7} is a 2-mark trap."),
            box("exit", "EXIT TICKET", "1. One limitation of binary search. 2. Write the mid formula. 3. Why does linear search still matter?"),
            box("hw", "HOMEWORK", "Binary-search 6 in {1,2,3,4,5,6,7,8,9}. Write every low, high, mid. Then state what happens if the list is shuffled."),
        ])),
    ])
