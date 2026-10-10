"""Class XII — 30-day coaching crash course."""
from crash_lib import day

FRONT = r"""
<section class="cover">
  <div>
    <div class="cover-kicker"><span>Coaching crash course</span><span>Class XII · 30 days</span></div>
    <h1>Intermediate Computer Science<br>30-Day Crash</h1>
    <p class="subtitle">HCI · data structures · Python · analysis · neural nets · a venture</p>
    <div class="badge-row">
      <span class="badge">Days 1–7 HCI</span>
      <span class="badge">Days 8–15 Algorithms</span>
      <span class="badge">Days 16–20 Python</span>
      <span class="badge">Days 21–25 Analysis</span>
      <span class="badge">Days 26–30 Impact &amp; mock</span>
    </div>
    <div class="cover-box" style="margin-top:14px;">
      <p><strong>House rule.</strong> Two hours, one topic. Recall is closed-book. The worked example is copied by hand. The drill is silent. Green model lines are uncovered only when the pencil is down. A checkpoint under 7/10 owns the next evening.</p>
      <p style="margin-bottom:0;">This is the timed layer on top of the Teach Yourself notes. It does not replace a Figma file, a Python run, or a paper prototype you tested on a real classmate.</p>
    </div>
  </div>
  <div class="cover-meta">Class XII crash · 30 coached sessions · mock on Day 29 · mark scheme on Day 30</div>
</section>
"""

MAP = r"""
<div class="running"><span>XII · 30-Day Crash</span><span>Timetable</span></div>
<h2>The thirty days on one sheet</h2>
<table class="long">
<caption>Class XII crash timetable</caption>
<tr><th>Day</th><th>Focus</th><th>You must leave able to</th><th>Score</th></tr>
<tr><td>01</td><td>HCI loop</td><td>Name the channels and the feedback loop</td><td>/5</td></tr>
<tr><td>02</td><td>Interaction</td><td>Separate traditional from natural</td><td>/5</td></tr>
<tr><td>03</td><td>Accessibility</td><td>Contrast, type, colour plus symbol, keyboard</td><td>/5</td></tr>
<tr><td>04</td><td>Needs</td><td>Run a need analysis and name a failure</td><td>/5</td></tr>
<tr><td>05</td><td>UI / UX</td><td>Wireframe at two fidelities</td><td>/5</td></tr>
<tr><td>06</td><td>Figma &amp; test</td><td>Link frames; name SUS, NPS, task success</td><td>/5</td></tr>
<tr><td>07</td><td>Checkpoint</td><td>Unit 1 closed book</td><td>/10</td></tr>
<tr><td>08</td><td>Correctness</td><td>Trace a loop</td><td>/5</td></tr>
<tr><td>09</td><td>Clarity</td><td>Split a blob into functions</td><td>/5</td></tr>
<tr><td>10</td><td>Big-O</td><td>Classify 1, log n, n, n squared</td><td>/5</td></tr>
<tr><td>11</td><td>Array &amp; list</td><td>Say who has O(1) index access</td><td>/5</td></tr>
<tr><td>12</td><td>Stack &amp; queue</td><td>PUSH/POP versus enqueue/dequeue</td><td>/5</td></tr>
<tr><td>13</td><td>Tree &amp; graph</td><td>Hierarchy versus free links</td><td>/5</td></tr>
<tr><td>14</td><td>Retrieval</td><td>Walk an array, a list, and a queue</td><td>/5</td></tr>
<tr><td>15</td><td>Checkpoint</td><td>Unit 2 closed book</td><td>/10</td></tr>
<tr><td>16</td><td>List &amp; tuple</td><td>Mutability and slicing</td><td>/5</td></tr>
<tr><td>17</td><td>Set &amp; dict</td><td>Union and dict.get</td><td>/5</td></tr>
<tr><td>18</td><td>Functions</td><td>return and local scope</td><td>/5</td></tr>
<tr><td>19</td><td>Files</td><td>with, modes, try/except</td><td>/5</td></tr>
<tr><td>20</td><td>Checkpoint</td><td>Unit 3 on paper</td><td>/10</td></tr>
<tr><td>21</td><td>SQLite</td><td>connect, execute, commit, fetch</td><td>/5</td></tr>
<tr><td>22</td><td>pandas</td><td>fillna versus dropna</td><td>/5</td></tr>
<tr><td>23</td><td>Plots</td><td>Pick bar, hist, scatter, box</td><td>/5</td></tr>
<tr><td>24</td><td>Statistics</td><td>Mean, median, mode, spread</td><td>/5</td></tr>
<tr><td>25</td><td>Checkpoint</td><td>Unit 4 closed book</td><td>/10</td></tr>
<tr><td>26</td><td>Neural nets</td><td>Layers, weights, loss, depth</td><td>/5</td></tr>
<tr><td>27</td><td>Security</td><td>Name a threat and a shield</td><td>/5</td></tr>
<tr><td>28</td><td>Equity</td><td>Equal access versus equity</td><td>/5</td></tr>
<tr><td>29</td><td>Venture</td><td>Prototype, MVP, riskiest assumption, beachhead</td><td>/5</td></tr>
<tr><td>30</td><td>Mock</td><td>90-minute paper, then the mark scheme</td><td>/50</td></tr>
</table>
<div class="callout why"><div class="mark">Last two days</div><div>Day 29 is the venture only, so the idea has a night to settle. Day 30 is the mock and then the mark scheme. Do not read the scheme until the 90 minutes are over. A checkpoint under 7/10 owns the next evening.</div></div>
"""

# Day 30 holds both the paper and, after a forced break in the HTML, the scheme.
# The renderer prints `paper` instead of drills when set. Scheme-only days print scheme.
# For day 30 we put the paper in `paper` and append the scheme inside it after an instruction,
# NO — student would see the scheme. Split: day 29 venture only, day 30 paper in `paper`
# and scheme passed... renderer shows paper OR scheme, not both.
# So day 30 paper only, and I'll put the scheme as the `scheme` field... looking at renderer:
# if scheme: show scheme (no paper)
# elif paper: show paper
# I need both on day 30 with a page break between them so the student can print paper first.
# I'll put paper HTML that ends, then a section... but it's one day section.
# Practical coaching fix: Day 30 teach/board empty, paper first, and scheme in a
# following HTML chunk with break-before. I'll special-case by putting the scheme
# AFTER the paper inside the paper string, preceded by:
# <h2 class="part">Mark scheme — open only after the 90 minutes</h2>
# h2.part has break-before page. The student who prints the PDF still sees it later,
# which is normal for a booklet, with a clear stop line. Good.

DAYS = []  # filled below

def add(d):
    DAYS.append(d)

add(day(1, "The HCI loop", "Unit 1 · Human–Computer Interaction",
    ["Define HCI in one sentence", "Name five sensory channels", "Explain why missing feedback is a defect"],
    r"""<p><strong>HCI</strong> (also CHI or MMI) is the design of technology so a person can use it efficiently and without being shut out. UI is what you see. The loop is the subject: a human sends input, the computer answers with feedback, and the human decides what to do next.</p>
<p>Channels: <strong>sight</strong> (screen), <strong>touch</strong> (tap, keys, vibration), <strong>hearing</strong> (voice prompts), <strong>voice</strong> (spoken commands), <strong>spatial</strong> (body position in a motion game). A system that changes state and does not tell you has a broken loop, not a minimalist style.</p>""",
    r"""<p><strong>Board.</strong> Student taps “Submit” on an attendance app. Sight: the button darkens. Touch: a short vibration. Hearing: optional click. If none of these happen, the student taps again and you get duplicate rows. Write the repair: a visible “Saved” line plus a disabled button. That is feedback, and it is worth marks.</p>""",
    [
        (r"HCI in one sentence.", r"Designing the exchange between a person and a computer so the system is usable, efficient, and respectful of human limits."),
        (r"Name the five channels.", r"Sight, touch, hearing, voice, spatial."),
        (r"UI or the loop: a button with no confirmation.", r"The loop is broken. Feedback is missing, so the user cannot tell success from failure."),
        (r"Two other names for HCI.", r"CHI (computer–human interface) and MMI (man–machine interaction)."),
        (r"Why does a coach care about vibration on a phone?", r"Touch feedback reaches users who cannot rely on the screen alone, and it confirms a tap."),
    ],
    r"Sketch the two circles, human and computer, and label both arrows. No icons required.",
    r"Defining HCI as ‘making screens pretty’. Pretty is later. The loop comes first."))

add(day(2, "Traditional and natural interaction", "Unit 1 · Human–Computer Interaction",
    ["Give two examples of each family", "Name four interaction styles", "Name three UI families"],
    r"""<p><strong>Traditional interaction</strong> uses keyboard, mouse, and tap or swipe. A PC answers on a monitor and speakers. A phone answers with light, sound, and vibration.</p>
<p><strong>Natural interaction</strong> uses voice, gesture, face, and spatial tracking: a smart speaker, a wave to dismiss a call, face unlock.</p>
<p>Styles you should be able to list: direct manipulation, command line, menus, forms, conversation, gesture, voice, context-aware, biometric, haptic, multimodal. UI families: GUI, CLI, touch, voice UI, and NUI (natural UI such as VR).</p>
<p>Components of an HCI situation: user (and other stakeholders), computer, task, interface, environment, and feedback in both directions.</p>""",
    r"""<p><strong>Board: college attendance.</strong> Traditional version: teacher taps a row on a phone (touch GUI, form fill). Natural version: a camera recognises a face at the door (biometric, context-aware). Say the trade: natural can be faster and can also fail on lighting, privacy, and consent. The crash answer names the style and one risk, not a gadget catalogue.</p>""",
    [
        (r"Mouse and keyboard belong to which family?", r"Traditional interaction."),
        (r"Face unlock belongs to which family?", r"Natural interaction, biometric."),
        (r"One GUI and one CLI example.", r"A phone home screen is a GUI. A terminal command such as python file.py is a CLI."),
        (r"What is multimodal?", r"More than one channel at once, for example captions plus vibration plus a spoken prompt."),
        (r"User versus stakeholder.", r"The user operates the system. A stakeholder is affected or decides, such as a parent who never opens the attendance app but receives the SMS."),
    ],
    r"Write six interaction styles from memory. Stop at six.",
    r"Calling every touchscreen ‘natural’. Tap and swipe are traditional phone interaction. Gesture-in-the-air and voice are the natural family.",
    recall=[("Five channels?", "Sight, touch, hearing, voice, spatial"), ("What is missing if a tap does nothing visible?", "Feedback")]))

add(day(3, "Accessibility is a constraint", "Unit 1 · Human–Computer Interaction",
    ["Test contrast in words", "Refuse colour-only meaning", "Include keyboard and screen-reader paths"],
    r"""<p>Accessibility is not a theme you add if there is time. Four constraints the paper expects:</p>
<table>
<tr><th>Constraint</th><th>Fail</th><th>Pass</th></tr>
<tr><td>Contrast</td><td>Pale grey on white</td><td>Dark text on a light ground, or the reverse</td></tr>
<tr><td>Readability</td><td>Decorative font, long lines</td><td>A plain face, a sane size, short lines</td></tr>
<tr><td>Colour-blind safety</td><td>Red means error, with no other cue</td><td>Icon plus the word “Failed”</td></tr>
<tr><td>Inclusive navigation</td><td>Mouse only</td><td>Tab order, visible focus, screen-reader names, captions</td></tr>
</table>
<p>A greyscale test is the one-minute audit: if the meaning disappears when colour disappears, the interface is not done.</p>""",
    r"""<p><strong>Board audit of a login.</strong> Placeholder text is light grey. The error is a red border only. The submit control is a 16-pixel icon. Repairs, in mark order: darker label text (contrast), the sentence “Password too short” (not colour alone), a larger target with the word Submit (readability and hit size), and a tab order that reaches the button (keyboard).</p>""",
    [
        (r"Why is red-only an accessibility defect?", r"Colour-blind users and anyone in greyscale lose the signal. Add a word and an icon."),
        (r"One contrast failure.", r"Pale grey text on a white card, especially outdoors."),
        (r"What should a keyboard user see?", r"A visible focus ring and a sensible Tab order, including the primary button."),
        (r"Name one screen reader.", r"NVDA or VoiceOver."),
        (r"Captions support which channel when hearing is unavailable?", r"Sight. They move speech into text."),
    ],
    r"Pick any school app you use. Write four lines: contrast, type, colour-plus-word, keyboard. One honest fail is enough.",
    r"Saying ‘we used blue so it is accessible’. Colour choice without contrast and without a non-colour cue does not pass.",
    recall=[("Traditional input devices?", "Keyboard, mouse, tap and swipe"), ("Natural examples?", "Voice, gesture, face, spatial tracking")]))

add(day(4, "Need analysis and the usual failures", "Unit 1 · Human–Computer Interaction",
    ["State a need as a gap", "Order the five analysis steps", "Match a symptom to a repair"],
    r"""<p>A <strong>need</strong> is the gap between the current state and the desired state. Steps: identify users, collect information, analyse, prioritise, propose solutions. Design for a named person, not for “users”.</p>
<table>
<tr><th>Symptom</th><th>Likely cause</th><th>Repair</th></tr>
<tr><td>Cannot find the next action</td><td>Weak hierarchy</td><td>One obvious primary button</td></tr>
<tr><td>Error with no explanation</td><td>System-centred text</td><td>Plain language plus how to fix it</td></tr>
<tr><td>Tiny targets</td><td>Desktop layout on a phone</td><td>Thumb-sized controls and spacing</td></tr>
<tr><td>Colour-only status</td><td>Accessibility skipped</td><td>Icon plus text</td></tr>
<tr><td>Ten-step signup</td><td>No need analysis</td><td>Cut fields; ask later</td></tr>
</table>""",
    r"""<p><strong>Board: mobile banking for a grandparent.</strong> Current state: a six-field transfer and a 12-point font. Desired state: send money to a saved name without fear. Needs, in priority: large type, a biometric login, a confirmation sentence, a second language. A 19-year-old who only tests on their own phone will miss all four. That sentence is the need-analysis mark.</p>""",
    [
        (r"Define a need.", r"The gap between how things are and how they need to be for a named user."),
        (r"Five steps, in order.", r"Identify users, collect information, analyse, prioritise, propose solutions."),
        (r"Tiny targets. Repair.", r"Enlarge the controls and separate them so a thumb hits one thing."),
        (r"‘Invalid input’ as the only error. What is wrong?", r"It does not say which field failed or how to repair it."),
        (r"Why interview someone who is not you?", r"Your habits hide the gaps. A different age, language, or eyesight reveals them."),
    ],
    r"Write a four-line need analysis for a college attendance app: user, current, desired, top priority.",
    r"Listing features (‘add dark mode’) before naming the person and the gap.",
    recall=[("Colour-only status fails whom?", "Colour-blind users and greyscale viewing"), ("Contrast fail example?", "Pale grey on white")]))

add(day(5, "UI, UX, wireframe, fidelity", "Unit 1 · Human–Computer Interaction",
    ["Separate UI from UX", "Sketch a low-fidelity wireframe", "Say when high fidelity is worth the time"],
    r"""<p><strong>UI</strong> is the visual and interactive layout: type, colour, controls, spacing. <strong>UX</strong> is the whole journey: time, trust, errors, and how you feel when you leave. “The transfer took four taps and I was never unsure” is a UX sentence. The button style that made the fourth tap obvious is UI.</p>
<p>A <strong>wireframe</strong> is a layout blueprint. A <strong>prototype</strong> is an early model you can tap before production code.</p>
<table>
<tr><th></th><th>Low fidelity</th><th>High fidelity</th></tr>
<tr><td>Looks like</td><td>Boxes and labels</td><td>Colour, type, images, motion</td></tr>
<tr><td>For</td><td>Structure and flow, cheap changes</td><td>Look-and-feel, a stakeholder demo</td></tr>
<tr><td>Speed</td><td>Minutes, including paper</td><td>Hours or days</td></tr>
</table>""",
    r"""<p><strong>Board, four frames, low fidelity.</strong> Welcome, Sign in, Class list, Saved. Each frame is a rectangle. One primary button. No colour. Arrows between frames are the flow. You are not allowed to discuss the logo until a classmate can tap the paper story without asking where to press.</p>""",
    [
        (r"UI or UX: ‘I trusted the confirmation sentence’.", r"UX. Trust is the journey, even though UI carried the sentence."),
        (r"When do you stay at low fidelity?", r"While the flow is still wrong. Changes are cheap. Polish on a bad flow wastes the hour."),
        (r"What is a prototype?", r"An early, tappable model used to test layout and flow before the final build."),
        (r"Four frames for attendance, names only.", r"Welcome, Sign in, Mark class, Confirmed. Other names are fine if the story is complete."),
        (r"Why one primary button?", r"So the next action is unambiguous. Extra buttons hide the path."),
    ],
    r"Draw the four frames on paper in six minutes. Give them to someone who has not seen the lesson. Note every pause.",
    r"Starting in high fidelity because the tool makes it easy. You will defend colours instead of fixing the flow.",
    recall=[("Five need-analysis steps?", "Users, collect, analyse, prioritise, propose"), ("A need is a what?", "A gap between current and desired")]))

add(day(6, "Figma, then SUS, NPS, and task success", "Unit 1 · Human–Computer Interaction",
    ["Create linked phone frames", "Watch one user in silence", "Define three evaluation measures"],
    r"""<p>Figma is the browser tool for this unit. Crash path: new file, press F for the frame tool, drag a phone frame, duplicate it for each screen, put a title and one button on each, open the Prototype tab, drag a link from the button to the next frame, present, and tap through.</p>
<p>Evaluation: <strong>SUS</strong> (System Usability Scale, a short score out of 100), <strong>NPS</strong> (would you recommend this?), and <strong>task success</strong> (did they finish, in how many seconds, with how many errors). Formative evaluation happens during design. Summative evaluation happens after a version exists. Also know: expert review, accessibility audit, A/B test, keyboard walkthrough.</p>""",
    r"""<p><strong>Board test of the attendance prototype.</strong> Task: “Mark Ali present and reach a confirmation.” You say nothing. You write the seconds and the pauses. A pause on the class list is a defect in hierarchy, not a clumsy user. Formative, because you will change the frame tonight. A SUS form after the finished flow would be summative.</p>""",
    [
        (r"Which key creates a frame in Figma?", r"F, then drag."),
        (r"Where do you connect a button to the next screen?", r"The Prototype tab."),
        (r"What does SUS measure, roughly?", r"Perceived usability, reported as a score out of 100."),
        (r"NPS asks what?", r"Whether the person would recommend the product."),
        (r"Formative or summative: a paper test in week one.", r"Formative. You are still changing the design."),
    ],
    r"If Figma is available, link three frames and watch one person. If not, do the same with paper and a finger.",
    r"Explaining the interface while the user is stuck. Their pause is the data. Your explanation hides it.",
    recall=[("Low fidelity is for what?", "Structure and flow, changed cheaply"), ("UI versus UX in one line?", "UI is the layout. UX is the whole journey.")]))

add(day(7, "HCI checkpoint", "Unit 1 · Human–Computer Interaction",
    ["Score 7/10", "Use the words contrast, feedback, and formative", "Repair one lost answer before algorithms"],
    r"""<p>Closed book, 30 minutes. Full sentences. A drawing of four boxes is an acceptable answer for the wireframe item.</p>""",
    r"""<p>Mark in class. The lowest item becomes tomorrow’s warm-up even though the unit changes.</p>""",
    [
        (r"Define HCI.", r"The design of interaction between people and computers so systems are usable and inclusive."),
        (r"Two traditional and one natural example.", r"Keyboard and tap are traditional. Voice command or face unlock is natural."),
        (r"Why a red border alone fails.", r"Colour is the only signal. Add text and an icon for colour-blind and greyscale users."),
        (r"Need-analysis steps — list them.", r"Identify users, collect, analyse, prioritise, propose."),
        (r"UI versus UX with the attendance confirmation.", r"The sentence ‘Saved’ is UI. The relief of not double-submitting is UX."),
        (r"Low versus high fidelity, one line each.", r"Low is boxes and flow. High is near-final look and feel."),
        (r"What is a wireframe?", r"A blueprint of layout and flow without final polish."),
        (r"SUS, NPS, task success — one each.", r"SUS: usability score. NPS: recommend or not. Task success: finished or not, with time or errors."),
        (r"Formative versus summative.", r"Formative during design. Summative after a version is ready to judge."),
        (r"One feedback repair for a silent Submit button.", r"Show a confirmation and disable the button so the loop closes."),
    ],
    r"Redraw your worst answer. One repair, then stop.",
    r"Starting stacks and queues with an HCI checkpoint still blank.",
    recall=[("Figma frame key?", "F"), ("Summative means?", "Evaluation after a version exists")]))

add(day(8, "Correctness by hand", "Unit 2 · Algorithms and Data Structures",
    ["Fill a trace table", "State a loop invariant in words", "Catch the empty-input case"],
    r"""<p>An algorithm is <strong>correct</strong> when every valid input produces the specified output and the process stops. Two tools: a <strong>trace table</strong> (line, variables, condition, output) and <strong>stepwise reasoning</strong> (an invariant such as “after k steps, S is the sum of the first k integers”).</p>
<p>Trace tables catch arithmetic slips. Invariants catch structural lies, including the empty case $N=0$, which a trace of $N=3$ can miss.</p>
<div class="formula">\[ S = \frac{N(N+1)}{2} \]</div>""",
    r"""<p><strong>Board: sum 1..N for N=3.</strong></p>
<table>
<tr><th>Line</th><th>i</th><th>S</th><th>i &le; 3</th></tr>
<tr><td>start</td><td>—</td><td>0</td><td>—</td></tr>
<tr><td>loop</td><td>1</td><td>1</td><td>true</td></tr>
<tr><td>loop</td><td>2</td><td>3</td><td>true</td></tr>
<tr><td>loop</td><td>3</td><td>6</td><td>true</td></tr>
<tr><td>exit</td><td>4</td><td>6</td><td>false</td></tr>
</table>
<p>Closed form checks the trace: $3 \times 4 / 2 = 6$. For $N=0$ the loop never runs and $S$ stays 0, which is correct. Say that edge aloud.</p>""",
    [
        (r"What must a correct algorithm do besides ‘usually work’?", r"Match the specification for every valid input, and stop."),
        (r"A trace table is best at catching what?", r"Arithmetic slips, bad updates, and loops that do not end, on a small n."),
        (r"An invariant is best at catching what?", r"A structural mistake, including forgotten edge cases."),
        (r"Sum 1..3 by the closed form.", r"6."),
        (r"Sum 1..0. What should happen?", r"The loop does not run. The sum stays 0."),
    ],
    r"Trace sum 1..4. The last S must be 10, and you must show the failing condition.",
    r"A final number with no rows. The rows are the answer.",
    recall=[("HCI checkpoint pass mark?", "7/10"), ("Formative evaluation happens when?", "During design")]))

add(day(9, "Clarity: modules and names", "Unit 2 · Algorithms and Data Structures",
    ["Give one function one job", "Rename a mystery variable", "Say which refinement is clarity and which is speed"],
    r"""<p><strong>Modularity</strong> means one function, one job, loosely coupled. <code>calculate_sum</code> and <code>find_average</code> beat a forty-line blob. <strong>Readability</strong> means names that carry units, shallow nesting, and comments only where the why is not obvious. <code>velocity = distance / time</code> documents itself.</p>
<p>Refine for clarity by renaming and extracting. Refine for efficiency by doing less work: stop early, avoid recomputing, or pick a better structure. Do not confuse the two. A faster mess is still a mess. A clear $O(n^2)$ on twenty rows is often the right classroom choice.</p>""",
    r"""<p><strong>Board, before and after.</strong> Before: one block reads numbers, sums them, divides, and prints a sentence. After: <code>total(nums)</code> returns the sum, <code>average(nums)</code> returns total divided by length and refuses an empty list, <code>main</code> only prints. The behaviour is the same. The clarity mark is the split, not a new formula.</p>""",
    [
        (r"Single responsibility in one line.", r"A function does one job that you can name with one verb."),
        (r"Replace x = a / b with a readable line.", r"velocity = distance / time, or any names that carry meaning."),
        (r"Clarity refinement or efficiency refinement: extracting a function.", r"Clarity."),
        (r"Efficiency refinement: one example.", r"Stop a search when the item is found, or replace a nested scan with a better structure."),
        (r"Why refuse an empty list inside average?", r"Division by zero. The function should not pretend the mean of nothing is zero."),
    ],
    r"Take any 15-line program you wrote in Class XI and split it into two named functions. Do not add features.",
    r"Commenting every line instead of renaming. A comment that repeats the code is not clarity.",
    recall=[("Closed form for sum 1..N?", "N(N+1)/2"), ("Trace tables show what?", "Each variable after each step")]))

add(day(10, "Big-O without the folklore", "Unit 2 · Algorithms and Data Structures",
    ["Classify constant, log, linear, and quadratic", "Spot a nested loop", "Say what short-circuiting saves"],
    r"""<p>Efficiency has two axes: time (steps as $n$ grows) and space (extra memory). The course expects these classes:</p>
<table>
<tr><th>Class</th><th>Growth</th><th>Classroom example</th></tr>
<tr><td>$O(1)$</td><td>Does not grow with n</td><td>Array index, hash lookup</td></tr>
<tr><td>$O(\log n)$</td><td>Halves the work</td><td>Binary search</td></tr>
<tr><td>$O(n)$</td><td>One pass</td><td>Linear search, one loop</td></tr>
<tr><td>$O(n \log n)$</td><td>Good general sort</td><td>Divide-and-conquer sort (named, not derived)</td></tr>
<tr><td>$O(n^2)$</td><td>Nested loops</td><td>Bubble sort, all-pairs compare</td></tr>
</table>
<p>Logarithmic is excellent, linear is good, quadratic becomes poor as $n$ leaves the classroom. Short-circuit a compound test when the first clause already decides it.</p>""",
    r"""<p><strong>Board.</strong> One loop over a class list is $O(n)$. A loop inside a loop over the same list is $O(n^2)$. Reading <code>marks[i]</code> is $O(1)$. Binary search on sorted roll numbers is $O(\log n)$. Say the three questions from the book: Does it scale? Where is the bottleneck? Is the cost worth it?</p>""",
    [
        (r"Nested loops usually mean which class?", r"$O(n^2)$."),
        (r"Array index access?", r"$O(1)$."),
        (r"Binary search?", r"$O(\log n)$, on sorted data."),
        (r"A single pass that prints every name?", r"$O(n)$."),
        (r"Why short-circuit <code>a and b</code>?", r"If a is false, b cannot save the expression, so you skip the work."),
    ],
    r"Label four snippets you invent: index, one loop, nested loops, binary search. Four labels, no essays.",
    r"Saying $O(1)$ means ‘fast in real seconds’. It means the step count does not grow with n.",
    recall=[("One function, one what?", "Job / responsibility"), ("A clarity refinement example?", "A meaningful name or an extracted function")]))

add(day(11, "Arrays and linked lists", "Unit 2 · Algorithms and Data Structures",
    ["State the cost of an index", "Explain a node", "Choose a list when inserts are frequent"],
    r"""<p>An <strong>array</strong> is a fixed sequence with indexes, often from 0. Reading <code>A[i]</code> is $O(1)$. Inserting in the middle pushes neighbours and is painful. Classroom chairs with painted numbers.</p>
<p>A <strong>linked list</strong> is nodes of (data + pointer). You walk from the head. There is no jump to the tenth node. Inserting once you are standing on the node is natural. Browser back/forward history is the picture.</p>""",
    r"""<p><strong>Board choice.</strong> Term grades, random lookup by week number: array. A playlist where you constantly insert the next song after the current one: linked list. Say the cost you are buying: the array sells you $O(1)$ access and charges you for middle inserts. The list sells you inserts and charges you a walk.</p>""",
    [
        (r"Cost of A[i]?", r"$O(1)$."),
        (r"What is stored in a list node besides the value?", r"A pointer (reference) to the next node."),
        (r"Why is the tenth list node not O(1)?", r"You must follow nine pointers from the head. There is no index jump."),
        (r"Frequent middle inserts. Array or list?", r"List, once you are at the position."),
        (r"Random access by position. Array or list?", r"Array."),
    ],
    r"Draw five array cells and five linked nodes holding the same values. Circle the access you would use to reach the third.",
    r"Drawing a list and then writing A[3]. That notation belongs to the array.",
    recall=[("O(n^2) pattern?", "Nested loops"), ("O(log n) example?", "Binary search")]))

add(day(12, "Stack and queue", "Unit 2 · Algorithms and Data Structures",
    ["PUSH and POP", "Enqueue and dequeue", "Match undo to a stack and a printer to a queue"],
    r"""<p>A <strong>stack</strong> is LIFO: last in, first out. <strong>PUSH</strong> adds on top. <strong>POP</strong> removes from the top. Undo, a pile of plates, function-call return.</p>
<p>A <strong>queue</strong> is FIFO: first in, first out. <strong>Enqueue</strong> at the rear. <strong>Dequeue</strong> from the front. With two pointers both operations are $O(1)$. A printer line, a ticket window.</p>
<p>Do not mix the verbs. A stack has one end that matters. A queue has two.</p>""",
    r"""<p><strong>Board.</strong> PUSH 10, PUSH 20, POP, PUSH 30. The stack from bottom to top is 10, then 30. A second POP returns 30. The 10 is still there.</p>
<p><strong>Queue.</strong> Enqueue 76, 90, 77. Dequeue returns 76. The new front is 90. The rear is still 77 until another enqueue.</p>""",
    [
        (r"LIFO structure and its two verbs.", r"Stack. PUSH and POP."),
        (r"FIFO structure and its two verbs.", r"Queue. Enqueue at the rear, dequeue from the front."),
        (r"Undo is which structure?", r"A stack."),
        (r"A fair printer is which structure?", r"A queue. First document printed is the first submitted."),
        (r"After PUSH 1, PUSH 2, POP, what remains?", r"1, alone."),
    ],
    r"Act it with books (stack) and a line of three classmates (queue). Say the verb as you move.",
    r"Dequeuing from the rear because it is ‘the end’. The front leaves. The rear arrives.",
    recall=[("Array access cost?", "O(1) by index"), ("List access?", "Walk from the head")]))

add(day(13, "Trees and graphs", "Unit 2 · Algorithms and Data Structures",
    ["Define root, parent, and child", "Define vertex and edge", "Refuse a tree when roads loop"],
    r"""<p>A <strong>tree</strong> is a hierarchy from one <strong>root</strong>. Each child has one parent. Family trees, organisation charts, folders. No cycles.</p>
<p>A <strong>graph</strong> is vertices plus edges, with no forced hierarchy. A social network: people are vertices, friendships are edges. A road map: cities are vertices, roads are edges, and several routes may exist. Any vertex may connect to any other.</p>""",
    r"""<p><strong>Board.</strong> College departments: the principal is the root, heads of department are children, teachers are grandchildren. One parent each. That is a tree. The same teachers in a WhatsApp group where anyone messages anyone is a graph. If you force that group into a tree you will invent a boss who does not exist.</p>""",
    [
        (r"A tree starts at what?", r"A single root."),
        (r"Graph pieces.", r"Vertices (nodes) and edges (links)."),
        (r"Org chart: tree or graph?", r"Tree, if each person has one manager."),
        (r"Road network with two routes between towns.", r"Graph. Cycles and multiple paths are allowed."),
        (r"One reason a tree is not a general social network.", r"A tree forbids arbitrary cycles and gives each node one parent. Friendships do not work that way."),
    ],
    r"Draw a three-level tree of your own family or college, then a four-vertex graph of roads. Label root versus vertices.",
    r"Calling every diagram with lines a tree. If there are two paths, it is a graph.",
    recall=[("Stack removal verb?", "POP"), ("Queue removal end?", "Front")]))

add(day(14, "Retrieval and the verb that picks the structure", "Unit 2 · Algorithms and Data Structures",
    ["Trace an array scan", "Trace a list walk", "Always dequeue from the front"],
    r"""<p>Shared operations: insert, delete, traverse, search, sort. Costs differ. Retrieval traces the course wants:</p>
<ul>
<li><strong>Array:</strong> jump to an index, or scan forward.</li>
<li><strong>Linked list:</strong> start at the head and follow pointers by position or by key.</li>
<li><strong>Queue:</strong> the only honest removal is from the front.</li>
<li><strong>Stack:</strong> the only honest removal is from the top.</li>
</ul>
<table>
<tr><th>Verb in the problem</th><th>Structure</th></tr>
<tr><td>Next / previous by index</td><td>Array or list</td></tr>
<tr><td>Undo, backtrack</td><td>Stack</td></tr>
<tr><td>First come, first served</td><td>Queue</td></tr>
<tr><td>Parent / child</td><td>Tree</td></tr>
<tr><td>Many-to-many links</td><td>Graph</td></tr>
</table>""",
    r"""<p><strong>Board trace, list.</strong> Nodes Ali → Sara → Omar. Find Omar: start at Ali, follow to Sara, follow to Omar. Three hops, no index. <strong>Array trace:</strong> if Omar is at index 2, you read that cell once. <strong>Queue trace:</strong> jobs 76, 90, 77. The next retrieval is 76, then 90. You do not ‘search the middle’ of a pure queue.</p>""",
    [
        (r"Grades by week number.", r"Array."),
        (r"Printer spooler.", r"Queue."),
        (r"Undo stack of edits. Which edit returns first?", r"The most recent. LIFO."),
        (r"GPS with alternative roads.", r"Graph."),
        (r"How do you reach the third node of a linked list?", r"From the head, follow two pointers. You cannot jump."),
    ],
    r"Fill the five-row verb table from a blank page.",
    r"Using a stack for a printer ‘because both are linear’. Fairness is FIFO. A stack prints the latest job first.",
    recall=[("Tree has how many roots?", "One"), ("Graph components?", "Vertices and edges")]))

add(day(15, "Algorithms checkpoint", "Unit 2 · Algorithms and Data Structures",
    ["Score 7/10", "Show a trace, not a definition only", "Name a structure from a verb"],
    r"""<p>Closed book. Traces are compulsory on the items that ask for them.</p>""",
    r"""<p>Half marks are not available for a correct structure with the wrong removal end.</p>""",
    [
        (r"Correctness in one sentence.", r"Every valid input gives the specified output, and the algorithm stops."),
        (r"Sum 1..2. Show S after each step.", r"S becomes 1, then 3. Then the loop stops."),
        (r"$O(1)$, $O(n)$, $O(n^2)$: give one example each.", r"Index access; one loop; nested loops or bubble sort."),
        (r"Binary search class, and the condition.", r"$O(\log n)$, sorted random-access data."),
        (r"Array versus list for A[i].", r"Array is O(1). A list walks."),
        (r"PUSH 4, PUSH 7, POP. What is popped? What remains?", r"7 is popped. 4 remains."),
        (r"Enqueue A, enqueue B, dequeue. Who leaves?", r"A. The front leaves."),
        (r"Org chart structure.", r"Tree."),
        (r"Social network structure.", r"Graph."),
        (r"Name one clarity refinement.", r"Extract a function or rename a variable so the job is obvious."),
    ],
    r"Redo only the trace you lost. Then leave the unit.",
    r"Defining LIFO and then popping the bottom item in the trace.",
    recall=[("Queue fairness word?", "FIFO"), ("Stack fairness word?", "LIFO")]))

add(day(16, "Lists and tuples", "Unit 3 · Programming Fundamentals",
    ["Mutate a list", "Slice without the stop index", "Choose a tuple for a fixed record"],
    r"""<p>A <strong>list</strong> is ordered and mutable. Indexes run from 0, and negative indexes count from the end. A slice <code>lst[start:stop:step]</code> stops <strong>before</strong> stop, like <code>range</code>. Methods: <code>append</code>, <code>insert</code>, <code>remove</code>, <code>sort</code>, <code>reverse</code>, <code>count</code>, <code>index</code>.</p>
<p>A <strong>tuple</strong> is ordered and immutable. Use it for a fixed record such as a city and its coordinates. Methods are mostly <code>count</code> and <code>index</code>. A tuple may contain a list, and that inner list can still change — do not hide behind that trick in an exam unless the question raises it.</p>""",
    r"""<pre><code>fruits = ["mango", "apple", "banana"]
fruits.append("guava")
print(fruits[0:2])   # mango, apple — stop excluded
point = (24.86, 67.01)  # tuple, not to be sorted in place</code></pre>
<p><strong>Board.</strong> <code>fruits.sort()</code> changes the list. <code>sorted(fruits)</code> would return a new list and leave the original, but <code>sorted</code> is a built-in, not a list method. Say which one you used.</p>""",
    [
        (r"List or tuple for a shopping list you will edit?", r"List. It is mutable."),
        (r"What does a[1:4] include if a has indexes 0..5?", r"Indexes 1, 2, and 3. Not 4."),
        (r"append versus insert.", r"append adds at the end. insert(i, x) places x at index i."),
        (r"Why store (name, roll) as a tuple?", r"The pair should not gain or lose fields by accident. It is a fixed record."),
        (r"Negative index -1.", r"The last item."),
    ],
    r"Predict fruits after append, insert(0, 'date'), and remove('apple'). Then run it if you can.",
    r"Sorting a tuple with .sort(). Tuples have no sort method. Use sorted(), which returns a list.",
    recall=[("POP removes from where?", "The top of a stack"), ("Dequeue removes from where?", "The front of a queue")]))

add(day(17, "Sets and dictionaries", "Unit 3 · Programming Fundamentals",
    ["Use a set to kill duplicates", "Write union and intersection", "Prefer dict.get over a bare key"],
    r"""<p>A <strong>set</strong> is unordered and unique. No index. <code>add</code>, <code>update</code>, <code>remove</code> (errors if missing), <code>discard</code> (quiet). Operators: <code>|</code> union, <code>&amp;</code> intersection, <code>-</code> difference, <code>^</code> symmetric difference.</p>
<p>A <strong>dictionary</strong> maps a unique key to a value. <code>d[k]</code> raises KeyError if the key is absent. <code>d.get(k, default)</code> does not. <code>d[k] = v</code> inserts or overwrites. Views: <code>keys</code>, <code>values</code>, <code>items</code>.</p>
<div class="formula">\[ |A \cup B| \text{ is not required; write the operator } A|B \]</div>""",
    r"""<pre><code>submitted = set()
submitted.add("Ali")
submitted.add("Ali")      # still one Ali
freq = {}
for w in text.split():
    freq[w] = freq.get(w, 0) + 1</code></pre>
<p><strong>Board.</strong> Two submissions from Ali must not double-count. A set does that for free. The frequency loop is the crash pattern for “how many times does each word appear?”.</p>""",
    [
        (r"Why a set for ‘students who submitted’?", r"Uniqueness is automatic. A second add does not duplicate."),
        (r"A|B and A&amp;B.", r"Union and intersection."),
        (r"d['x'] when x is missing.", r"KeyError."),
        (r"Safe lookup with a default of 0.", r"<code>d.get('x', 0)</code>."),
        (r"Loop over keys and values.", r"<code>for k, v in d.items():</code>"),
    ],
    r"Word-count the sentence ‘the cat saw the dog’. The value for the must be 2.",
    r"Indexing a set. Sets have no order you are allowed to use as an index.",
    recall=[("Slice stop inclusive?", "No"), ("Tuple mutable?", "No")]))

add(day(18, "Functions, return, and scope", "Unit 3 · Programming Fundamentals",
    ["Write a function that returns", "Guard division by zero", "Separate local from global"],
    r"""<p>A function packages a sub-problem. <code>def name(parameters):</code> then a body and usually <code>return</code>. Built-ins (<code>len</code>, <code>sum</code>, <code>range</code>) come with Python. User-defined functions are yours.</p>
<p><strong>Local</strong> names exist inside the function. <strong>Global</strong> names exist at module level. Prefer returning a value over writing a global. Parameters are local.</p>
<pre><code>def divide(a, b):
    if b == 0:
        return "Cannot divide by zero"
    return a / b</code></pre>""",
    r"""<p><strong>Board calculator.</strong> Four functions: add, subtract, multiply, divide. <code>main</code> only reads two numbers and a choice, then calls one function and prints the return value. Decomposition is the picture: one problem, four sub-problems. A divide by zero must return a message or raise a handled error, not crash the demo.</p>""",
    [
        (r"What does return do?", r"Sends a value back to the caller and ends the function."),
        (r"Is a parameter local or global?", r"Local to the function."),
        (r"Why avoid global inside a function?", r"The function becomes harder to test and can change state the caller did not expect."),
        (r"Built-in or user-defined: len, and your divide.", r"len is built-in. divide is user-defined."),
        (r"Empty list passed to a mean function. What must you guard?", r"Division by len(nums) when the length is 0."),
    ],
    r"Write average(nums) so it returns the mean or a clear message. Trace [10, 20] and [].",
    r"Printing inside every function and also returning. Pick one. The crash course prefers return so the caller can test it.",
    recall=[("dict.get default avoids what?", "KeyError"), ("Set union operator?", "|")]))

add(day(19, "Files, with, and exceptions", "Unit 3 · Programming Fundamentals",
    ["Choose r, w, and a", "Use with so the file closes", "Catch FileNotFoundError"],
    r"""<p>Text versus binary. <code>open(path, mode)</code> returns a file object. Modes: <code>'r'</code> read (error if missing), <code>'w'</code> write and <strong>overwrite</strong>, <code>'a'</code> append and create if needed. <code>'rb'</code> and <code>'wb'</code> are the binary cousins. Methods: <code>read</code>, <code>readline</code>, <code>readlines</code>, <code>write</code>, <code>close</code>.</p>
<p>The <code>with</code> statement closes the file even when an error happens. Wrap a missing file:</p>
<pre><code>try:
    with open("marks.txt") as f:
        rows = f.readlines()
except FileNotFoundError:
    print("Create the file first.")</code></pre>
<p>Grade tracker: <code>'w'</code> to create, <code>'a'</code> to add a student, <code>'r'</code> to average the lines.</p>""",
    r"""<p><strong>Board disaster.</strong> <code>open("marks.txt", "w")</code> on a file that already holds a term of marks. The file becomes empty, then you write today’s one line. The repair for “add a row” is mode <code>"a"</code>. Say overwrite aloud whenever you write <code>"w"</code>.</p>""",
    [
        (r"Mode that destroys existing text.", r"<code>'w'</code>."),
        (r"Mode that adds to the end.", r"<code>'a'</code>."),
        (r"Why with?", r"It closes the file for you, including when an exception fires."),
        (r"readlines() returns what?", r"A list of lines."),
        (r"Which exception if the path is wrong on read?", r"FileNotFoundError."),
    ],
    r"On paper, write the three open modes and one sentence each. Then write the try/except skeleton from memory.",
    r"Using 'w' to ‘save an update’. That is a new file, not an update.",
    recall=[("return sends a value where?", "Back to the caller"), ("Local variable visible outside?", "No")]))

add(day(20, "Python checkpoint", "Unit 3 · Programming Fundamentals",
    ["Score 7/10 on paper", "Show a slice and a get()", "Refuse mode w for an append"],
    r"""<p>No computer. Predict output exactly, including crashes.</p>""",
    r"""<p>A crash described as a number scores 0 on that item.</p>""",
    [
        (r"a = [10, 20, 30, 40]; a[1:3]?", r"[20, 30]."),
        (r"After a.append(50), what is a[-1]?", r"50."),
        (r"Can you assign into a tuple’s first slot?", r"No. Tuples are immutable."),
        (r"{1, 1, 2} as a set, printed idea.", r"Two members: 1 and 2. Duplicates die."),
        (r"d.get('missing', 5)?", r"5, and no exception."),
        (r"d['missing']?", r"KeyError."),
        (r"Where does a function parameter live?", r"In local scope."),
        (r"open(path, 'w') on an existing file does what first?", r"Truncates it to empty."),
        (r"Which mode appends?", r"'a'."),
        (r"Write the header of a with-statement that reads notes.txt.", r"<code>with open('notes.txt') as f:</code>"),
    ],
    r"Retype the two items you lost and run them tomorrow if a PC is free. Tonight, paper only.",
    r"Giving [20, 30, 40] for a slice that excludes the stop.",
    recall=[("Append mode letter?", "a"), ("with closes the file when?", "On leaving the block, even after an error")]))

add(day(21, "SQLite from Python", "Unit 4 · Data and Analysis",
    ["Name the connection stack", "Insert with placeholders", "Commit before you trust the file"],
    r"""<p>A program cannot see a database until a connection exists. Stack: engine, driver, connection, cursor, SQL, then <code>commit</code> or <code>fetchall</code>, then <code>close</code>. SQLite is one file, which is why labs use it.</p>
<pre><code>import sqlite3
con = sqlite3.connect("school.db")
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS marks (id INTEGER PRIMARY KEY, name TEXT, math INTEGER)")
cur.execute("INSERT INTO marks (name, math) VALUES (?, ?)", ("Ayesha", 88))
con.commit()
cur.execute("SELECT name, math FROM marks WHERE math &gt;= 80")
print(cur.fetchall())
con.close()</code></pre>
<p>Verbs: CREATE, INSERT, SELECT, UPDATE, DELETE. The question marks are placeholders so values are data, not glued into the sentence.</p>""",
    r"""<p><strong>Board mistake.</strong> Insert, then <code>close</code>, and never <code>commit</code>. The next run does not see Ayesha. The repair is <code>con.commit()</code> before close. Say it as “the cursor staged the row; commit writes the file.”</p>""",
    [
        (r"What does connect() return?", r"A connection to the database file."),
        (r"What is a cursor for?", r"Executing SQL and fetching rows."),
        (r"Why commit?", r"To persist inserts and updates. Without it the change can vanish."),
        (r"Why (?, ?) instead of pasting the name into the SQL text?", r"The value stays data. You avoid broken quotes and injection-style surprises."),
        (r"fetchall() after SELECT returns what?", r"The matching rows, typically a list of tuples."),
    ],
    r"Write the five verbs and the order: connect, cursor, execute, commit, close.",
    r"Selecting and then wondering why yesterday’s insert is gone. You never committed.",
    recall=[("File mode that overwrites?", "w"), ("FileNotFoundError belongs to which operation?", "Reading a path that is not there")]))

add(day(22, "DataFrames and missing values", "Unit 4 · Data and Analysis",
    ["Load a CSV into a DataFrame", "Add a column", "Choose fillna or dropna and say why"],
    r"""<p>pandas gives you a table that can compute. <code>pd.read_csv</code>, <code>pd.read_excel</code>, and <code>pd.DataFrame</code>. <code>head()</code> shows the top. A new column is an assignment: <code>df["Total"] = df["Math"] + df["Science"]</code>.</p>
<p>Missing cells arrive as <code>NaN</code>. <code>isnull().sum()</code> counts them. <code>fillna</code> replaces them (often with the column mean). <code>dropna</code> deletes broken rows. Filling keeps $n$. Dropping is honest when the row is junk. Never fill and then forget you invented data.</p>""",
    r"""<pre><code>import pandas as pd
df = pd.read_csv("marks.csv")
print(df.isnull().sum())
df["Math"] = df["Math"].fillna(df["Math"].mean())</code></pre>
<p><strong>Board.</strong> One blank Math score in a class of 30. Filling with the mean keeps the student in the Total column. Dropping removes the whole student, including a valid Science score. Say which you chose and why. The why is the mark.</p>""",
    [
        (r"Function that reads a CSV.", r"<code>pd.read_csv</code>."),
        (r"What is NaN?", r"A missing numeric value."),
        (r"Count missing values per column.", r"<code>df.isnull().sum()</code>."),
        (r"Replace missing Science with the column mean.", r"<code>df['Science'] = df['Science'].fillna(df['Science'].mean())</code>."),
        (r"When is dropna the honest choice?", r"When the row is junk, not when a single cell can be explained."),
    ],
    r"Invent a four-row table with one blank. Write both a fill sentence and a drop sentence. Circle the one you would defend.",
    r"Filling missing exam marks with 0. That is a decision, and it pulls the mean down. Say so if you do it.",
    recall=[("SQLite persist call?", "commit()"), ("Placeholders look like?", "Question marks")]))

add(day(23, "Six plots, six questions", "Unit 4 · Data and Analysis",
    ["Match a question to a plot", "State why histogram bars touch", "Write the core matplotlib call"],
    r"""<p>Choose the plot from the question, not from the function you remember.</p>
<table>
<tr><th>Question</th><th>Plot</th></tr>
<tr><td>How did yearly averages move?</td><td>Line — <code>plot</code></td></tr>
<tr><td>Which subject scored higher?</td><td>Bar — <code>bar</code></td></tr>
<tr><td>What share chose Biology?</td><td>Pie — <code>pie</code></td></tr>
<tr><td>How are scores distributed?</td><td>Histogram — <code>hist</code></td></tr>
<tr><td>Does yield rise with rain?</td><td>Scatter — <code>scatter</code></td></tr>
<tr><td>Which class is more spread out?</td><td>Box — <code>boxplot</code></td></tr>
</table>
<p>Histogram bars touch because neighbouring bins share a boundary on a continuous axis. Bar-chart bars are separate categories and usually have gaps. Always label axes and write a title.</p>""",
    r"""<pre><code>import matplotlib.pyplot as plt
plt.scatter(rain, yield_)
plt.xlabel("Rain")
plt.ylabel("Yield")
plt.title("Yield against rain")
plt.show()</code></pre>
<p><strong>Board sentence.</strong> “The points rise together, so higher rain is associated with higher yield in this sample.” You do not claim the rain caused the yield unless the study was designed for cause. Association is the safe word.</p>""",
    [
        (r"Plot for parts of a whole.", r"Pie."),
        (r"Plot for two numeric variables.", r"Scatter."),
        (r"Plot for a continuous distribution.", r"Histogram."),
        (r"Why do histogram bars touch?", r"Bins share edges on a continuous number line."),
        (r"Plot that shows median and spread side by side.", r"Box plot."),
    ],
    r"Write six questions of your own, one per plot, about college life. No code required if the match is correct.",
    r"Using a pie chart for a trend over years. Time wants a line.",
    recall=[("fillna keeps or deletes the row?", "Keeps the row and replaces the hole"), ("dropna does what?", "Deletes rows with missing values")]))

add(day(24, "Centre and spread", "Unit 4 · Data and Analysis",
    ["Compute mean and median", "Choose mode for a category", "Define range and variance in words"],
    r"""<p>For values $x_1 \ldots x_n$:</p>
<div class="formula">\[ \bar{x} = \frac{1}{n}\sum x_i, \qquad \text{Range} = x_{\max}-x_{\min}, \qquad \sigma^2 = \frac{1}{n}\sum (x_i-\bar{x})^2 \]</div>
<p>Some mark schemes use $n-1$ in the variance. Follow the paper in front of you. The idea is “average squared distance from the mean”. Standard deviation is the square root.</p>
<table>
<tr><th>Situation</th><th>Centre</th><th>Why</th></tr>
<tr><td>Balanced test scores</td><td>Mean</td><td>Uses every value</td></tr>
<tr><td>Salaries with two extreme highs</td><td>Median</td><td>Resists extremes</td></tr>
<tr><td>Favourite fruit</td><td>Mode</td><td>A category, not a number line</td></tr>
</table>""",
    r"""<p><strong>Board:</strong> $10, 12, 13, 13, 80$. Sorted already. Mean $= 128/5 = 25.6$. Median $= 13$. The typical student is near 13. The mean is dragged by 80. Mode $= 13$. Range $= 70$. Say median in the sentence you would give a principal, and mention the outlier so you are not hiding it.</p>""",
    [
        (r"Mean of 10, 12, 13, 13, 80.", r"25.6."),
        (r"Median of that list.", r"13."),
        (r"Which centre for favourite fruit?", r"Mode."),
        (r"Range in words.", r"Maximum minus minimum."),
        (r"Variance in words.", r"The average of the squared distances from the mean."),
    ],
    r"Compute mean and median of 4, 4, 5, 7, 20. Write one sentence that chooses between them.",
    r"Reporting only the mean of a skewed list. The median is the honest ‘typical’ when one value is wild.",
    recall=[("Scatter is for what?", "The relationship of two numeric variables"), ("Histogram bars touch because?", "Bins are adjacent on a continuous axis")]))

add(day(25, "Analysis checkpoint", "Unit 4 · Data and Analysis",
    ["Score 7/10", "Commit, fill, and choose a plot", "Pick median when an outlier is obvious"],
    r"""<p>Closed book. Code may be pseudocode if the methods and the order are right.</p>""",
    r"""<p>A plot with no question attached scores at most half.</p>""",
    [
        (r"Order: cursor, connect, commit. Repair it.", r"connect, then cursor, then execute, then commit, then close."),
        (r"Why placeholders?", r"Values stay data and the SQL text stays intact."),
        (r"One line to fill missing Math with the mean.", r"<code>df['Math'] = df['Math'].fillna(df['Math'].mean())</code>."),
        (r"Line, bar, or scatter: rain versus yield.", r"Scatter."),
        (r"Parts of a whole.", r"Pie."),
        (r"Mean of 2, 4, 6.", r"4."),
        (r"Median of 2, 4, 100.", r"4. The mean would be pulled toward 100."),
        (r"Mode is for what kind of data?", r"The most common category or value."),
        (r"Range of 2, 4, 100.", r"98."),
        (r"Why say ‘associated’ instead of ‘caused’ on a scatter?", r"A plot shows a pattern, not by itself a cause."),
    ],
    r"One page: the five SQL verbs, one fillna line, the six plot names. That is the card.",
    r"Median of an even-length list invented as ‘the bigger middle’. Average the two middle values if the scheme says so; say you did.",
    recall=[("Mean is sensitive to what?", "Outliers / extreme values"), ("Box plot shows what?", "Median and spread, including quartiles")]))

add(day(26, "Machine learning, networks, depth", "Unit 5 · Applications and Impacts",
    ["Separate the three terms", "Label input, hidden, and output", "Name weight, bias, activation, and loss"],
    r"""<p>These are not synonyms. <strong>Machine learning</strong> is the field: a model studies data and then predicts. A <strong>neural network</strong> is one model, layers of nodes, inspired by a brain and implemented as arithmetic. <strong>Deep learning</strong> is the method of training a network with many hidden layers.</p>
<p>Input layer: pixels, samples, word ids, sensor numbers. Hidden layers build patterns (edges, then eyes, then a face). Output layer: the prediction. Each connection is a <strong>weight</strong>. A <strong>bias</strong> shifts the sum. An <strong>activation</strong> is a non-linear gate. <strong>Loss</strong> measures how wrong this guess was; training tries to shrink it.</p>
<div class="formula">\[ z = w_1 x_1 + \cdots + w_n x_n + b, \qquad \hat{y} = f(z) \]</div>
<p>“Deep” means several hidden layers, not a mysterious extra ingredient. It wants a lot of data and often a GPU. Face unlock, speech, translation, medical images, captions.</p>""",
    r"""<p><strong>Board: face unlock, no mythology.</strong> Input: the camera’s numbers. Hidden layers: features. Output: match or not, compared with the stored template. If the loss on training faces was high, the phone will annoy the owner or accept the wrong person. You do not need to train one. You need to label the layers and refuse to call the whole thing “just a database lookup” or “just IoT”.</p>""",
    [
        (r"Which term is the field, which is the model, which is the method?", r"Machine learning is the field. A neural network is a model. Deep learning is the method of training deep networks."),
        (r"Three layer names.", r"Input, hidden, output."),
        (r"What is a weight?", r"The number on a connection that scales an input."),
        (r"What does loss measure?", r"How wrong the current prediction is."),
        (r"Why the word deep?", r"Many hidden layers, so features are learned in stages."),
    ],
    r"Draw six circles in three columns and label the columns. One sentence: what z is.",
    r"Saying deep learning is a different subject from machine learning. It sits inside it.",
    recall=[("Median resists what?", "Extreme values"), ("Scatter claims association or automatic cause?", "Association")]))

add(day(27, "Threats and the boring shields", "Unit 5 · Applications and Impacts",
    ["Name six threats", "Match a shield to each", "Separate symmetric from asymmetric encryption"],
    r"""<p>Collaboration is only real if the wrong person cannot join and the right person’s file cannot vanish. Authentication (password, OTP, biometric), access control (view / edit / share), logs, and an official channel rather than a random public link.</p>
<p>Encryption turns plaintext into ciphertext and back. <strong>Symmetric:</strong> one shared secret, fast, hard to distribute. <strong>Asymmetric:</strong> a public key locks, a private key unlocks. That is how HTTPS starts.</p>
<table>
<tr><th>Threat</th><th>Shield</th></tr>
<tr><td>Malware</td><td>Antivirus, do not sideload junk</td></tr>
<tr><td>Phishing</td><td>Check the real domain; never send the password</td></tr>
<tr><td>Unauthorised access</td><td>Unique passwords and 2FA</td></tr>
<tr><td>Data theft</td><td>Encryption and least privilege</td></tr>
<tr><td>DoS</td><td>Provider limits; you still keep backups</td></tr>
<tr><td>Human error</td><td>Training, official tools, a tested restore</td></tr>
</table>""",
    r"""<p><strong>Board phishing.</strong> “Update your fee portal” with a link to a lookalike domain. Shields: do not click, open the portal from a bookmark, tell the lab in-charge. 2FA would not have made the fake page honest, but it limits a stolen password. Say both.</p>
<p>Backup story: a lab disk dies. Encryption did not help if there is no copy. Recovery is a separate control.</p>""",
    [
        (r"Public key encrypts a message to you. Which key decrypts?", r"Your private key."),
        (r"Symmetric encryption uses how many secrets?", r"One shared key for both directions."),
        (r"Phishing in one line.", r"A fake message that tries to make you reveal credentials or open a trap."),
        (r"2FA expands to what?", r"Two-factor authentication: password plus a second proof such as an OTP."),
        (r"A deleted file and no backup. Which control failed?", r"Backup and recovery, often after a human error."),
    ],
    r"Write three red flags on a fake fee email. Keep the note in your phone only as a reminder, not as a forwarded copy of the fake link.",
    r"Forwarding the phishing email ‘so others can see’. You just spread the link. Describe it; do not redistribute it.",
    recall=[("Deep learning sits inside what?", "Machine learning"), ("Hidden layers do what?", "Build features between input and output")]))

add(day(28, "Equal access is not equity", "Unit 5 · Applications and Impacts",
    ["Define both terms", "Add one support that equal access forgot", "Name a safe collaboration tool and a risky habit"],
    r"""<p><strong>Equal access</strong> hands everyone the same link. <strong>Equity</strong> adds what a particular learner needs so the link is actually usable: captions, a recording for a student on a weak connection, a mobile-friendly page, a screen reader, a large-type mode.</p>
<p>Tools the course names: Google Docs, Zoom, Teams, Classroom or an LMS, email, and WhatsApp used carefully. A 200-person group is a bad place for a marksheet. Official channels keep access control and logs. Equity is a design decision, not a slogan under the slide.</p>""",
    r"""<p><strong>Board.</strong> A teacher posts one PDF to every student. That is equal access. Equity for a low-vision student: a tagged file or large type, and an audio version. Equity for a student who shares a phone: a file small enough to download once, and a recording they can replay at night. Write both additions. One is not a substitute for the other.</p>""",
    [
        (r"Equal access in one line.", r"The same tool or file offered to everyone."),
        (r"Equity in one line.", r"Extra support so people with different constraints can actually use that offer."),
        (r"One equity addition for deaf students in a live class.", r"Captions or a written summary."),
        (r"Why not paste marks into a huge chat group?", r"No access control. People who should not see the marks will see them."),
        (r"Name two official collaboration tools.", r"Any two of Docs, Zoom, Teams, Classroom, school email."),
    ],
    r"Take one lesson you attended this month. Write the equal-access version and one equity addition.",
    r"Calling a single Zoom link ‘equity’ because everyone received it. That is access. Equity is the extra support.",
    recall=[("Private key decrypts what?", "Messages locked with your public key"), ("Phishing wants what from you?", "Credentials, or a click on a trap")]))

add(day(29, "Prototype, MVP, beachhead", "Unit 6 · Entrepreneurship in the Digital Age",
    ["Walk problem to first customers", "Separate prototype from MVP", "Name a riskiest assumption and a beachhead"],
    r"""<p>An entrepreneur notices a problem and builds a service, sometimes from a phone and a form. The crash journey is the syllabus: <strong>problem → idea → prototype → MVP → beachhead</strong>.</p>
<table>
<tr><th></th><th>Prototype</th><th>MVP</th></tr>
<tr><td>Question</td><td>Is the idea understandable?</td><td>Will they actually use it?</td></tr>
<tr><td>Must it work?</td><td>No</td><td>Yes, basically</td></tr>
<tr><td>Example</td><td>Paper canteen screens</td><td>A live form taking real orders for three days</td></tr>
</table>
<p>Fidelity: low (paper), mid (clickable slides), high (near-final). The <strong>riskiest assumption</strong> is the belief that kills the idea if it is false — test that first. A <strong>beachhead</strong> is the first tiny market you can name in one breath: “Grade XII in this college”, not “all students in Pakistan”.</p>
<p>Canteen case: pain is the queue. Paper menu. Then a form, orders close 20 minutes before break, a separate pickup line, a three-day test, then drop dishes nobody orders. Ethics: permission, no fake scarcity, no scraped personal data.</p>""",
    r"""<p><strong>Board, ten minutes, one idea.</strong> Problem: practical files go missing the night before submission. Beachhead: this class, this subject. Riskiest assumption: “students will check a shared folder the night before” — test that before you design a logo. Prototype: three paper screens. MVP: one shared folder and a Form that records “I uploaded”, run for one practical only. If nobody uploads, the assumption died cheaply. That is success of the test, not failure of your pride.</p>""",
    [
        (r"Prototype or MVP: a clickable Figma with no live data.", r"Prototype. It does not yet do the job for a real user."),
        (r"Riskiest assumption for a paid notes hub.", r"Students will pay rather than photocopy. Test that before the brand colours."),
        (r"Rewrite ‘an app for all Pakistani students’ as a beachhead.", r"For example: Class XII Computer Science in this college who missed last week’s practical."),
        (r"Canteen MVP in one sentence.", r"A live order form used for real food for a few days, with a cutoff and a pickup line."),
        (r"Low fidelity is allowed to be what?", r"Paper. It does not have to be software."),
    ],
    r"One page only: problem, beachhead, riskiest assumption, prototype sketch titles, MVP that could run this week. Sleep. The mock is tomorrow.",
    r"Building the high-fidelity app before anyone has used a paper screen.",
    recall=[("Equity adds what, beyond the same link?", "The specific support a learner needs"), ("Equal access is?", "The same offer to everyone")]))

add(day(30, "Mock paper, then the mark scheme", "Full mock · Class XII · 50 marks",
    ["Sit 90 minutes before you read a scheme", "Show traces and layer labels", "Leave with a 48-hour card"],
    r"""<p>The paper is the next pages. The scheme starts on a later page. Do not scroll there.</p>""",
    r"""<p>After marking, the card at the bottom is the only reread.</p>""",
    [],
    r"Copy the 48-hour card by hand. Repair only the section where you lost the most marks.",
    r"Marking from memory of what you meant. Mark the words on the script.",
    paper=r"""
<p class="marks">Section A · 10 × 1 = 10</p>
<ol>
<li>LIFO structure.</li>
<li>FIFO removal verb.</li>
<li>Cost of reading A[i] in an array.</li>
<li>Python structure that forbids duplicate members.</li>
<li>File mode that overwrites.</li>
<li>Plot for two numeric variables.</li>
<li>Centre that resists a single extreme salary.</li>
<li>Neural-network layer that receives raw pixels.</li>
<li>Key that decrypts a public-key message.</li>
<li>A tappable fake used to test an idea before it works: prototype or MVP?</li>
</ol>
<p class="marks">Section B · 8 × 3 = 24</p>
<ol start="11">
<li>Give one accessibility repair for a red-only error, and say who it protects.</li>
<li>Define UI and UX using a confirmation message.</li>
<li>Trace PUSH 5, PUSH 8, POP, PUSH 2. State the popped value and the final stack from bottom to top.</li>
<li>Binary search is $O(\log n)$. State the data condition and one situation where you must refuse it.</li>
<li>Predict <code>[10, 20, 30, 40][1:3]</code> and explain the stop.</li>
<li>Why does <code>d.get("k", 0)</code> differ from <code>d["k"]</code> when the key is missing?</li>
<li>Marks 10, 12, 13, 13, 80. State the median and why you might not quote the mean as “typical”.</li>
<li>Equal access or equity: one PDF for every student. Name the term, then add one equity support.</li>
</ol>
<p class="marks">Section C · 2 × 8 = 16</p>
<ol start="19">
<li>A college printer must be fair, and an editor must support undo. Choose a structure for each, name the operations, and show one short trace for each structure. (8)</li>
<li>Describe a canteen pre-order as prototype, then as MVP, name the riskiest assumption, and name a beachhead smaller than “the whole city”. (8)</li>
</ol>
<h2 class="part">Mark scheme — open after 90 minutes</h2>
<h3>Section A</h3>
<ol>
<li>Stack.</li>
<li>Dequeue (from the front).</li>
<li>$O(1)$.</li>
<li>Set.</li>
<li><code>w</code>.</li>
<li>Scatter.</li>
<li>Median.</li>
<li>Input layer.</li>
<li>Private key.</li>
<li>Prototype.</li>
</ol>
<h3>Section B — award the points in brackets</h3>
<ol start="11">
<li>Add a word and an icon (2). Protects colour-blind users or anyone who cannot rely on hue (1).</li>
<li>UI: the visible sentence or control (1). UX: the confidence or the journey (1). Both tied to confirmation (1).</li>
<li>POP returns 8 (1). Final stack bottom-to-top 5, 2 (2).</li>
<li>Sorted random-access data (2). Refuse on an unsorted pile (1).</li>
<li>[20, 30] (2). Stop index 3 is excluded (1).</li>
<li>get returns the default (1). Bare lookup raises KeyError (2).</li>
<li>Median 13 (1). Mean is dragged by 80 so it is not typical (2).</li>
<li>Equal access (1). One real support: captions, large type, audio, or a small download (2).</li>
</ol>
<h3>Section C</h3>
<ol start="19">
<li>Queue for the printer, enqueue and dequeue, FIFO trace (4). Stack for undo, push and pop, LIFO trace (4).</li>
<li>Prototype may be paper and need not work (2). MVP takes real orders and must basically work (2). A killer belief such as “students will order ahead” (2). A beachhead such as one college canteen at one break (2).</li>
</ol>
<div class="card-row">
<div class="card"><div class="label">48-hour card — HCI &amp; structures</div><p>Feedback closes the loop. Contrast, word plus icon, keyboard. Low fidelity before high. SUS, NPS, task success. $O(1)$ index, $O(n)$ walk, $O(n^2)$ nested, $O(\log n)$ binary. Stack LIFO. Queue FIFO. Tree one root. Graph free edges.</p></div>
<div class="card"><div class="label">48-hour card — Python &amp; data</div><p>Slice excludes stop. Set unique. dict.get. return and local scope. w overwrites, a appends, with closes. commit. fillna versus dropna. Six plots. Median resists outliers.</p></div>
<div class="card gold"><div class="label">48-hour card — impact &amp; venture</div><p>ML field, network model, deep method. Input, hidden, output, loss. Public locks, private unlocks. Phishing, 2FA, backups. Access is the same link. Equity is the extra support. Prototype asks “clear?”. MVP asks “used?”. Beachhead is embarrassingly small.</p></div>
</div>
<p>40–50: sit past papers. 30–39: repair the heavier card only. Under 30: repeat Days 7, 15, 20, and 25 before another full paper.</p>
"""))
