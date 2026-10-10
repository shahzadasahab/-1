"""Lectures 18–21 — Data and analysis."""

from lectures.kit import box, fig, lecture, table
from web import svgs


def lectures() -> str:
    return "".join([
        lecture(18, "Data, DBMS, and the four keys", "Unit 4 · Data and Analysis", "45 min", [
            "Turn raw marks into one sentence of information.",
            "Define database, DBMS, and RDBMS.",
            "Place candidate, primary, alternate, and foreign keys.",
        ], "\n".join([
            box("recap", "BLOCK D OPENS", "Eighty, seventy-five, ninety is data. “The class average is 80%” is information. A database is the organised cupboard that keeps those facts consistent."),
            table(["", "Data", "Information"], [
                ["Definition", "Raw facts", "Processed, meaningful facts"],
                ["Example", "85, 90, 75", "Average = 83.3%"],
                ["Use", "Little, alone", "Supports a decision"],
            ]),
            "<p>A <strong>DBMS</strong> (Access, MySQL, Oracle, SQL Server) inserts, updates, deletes, and retrieves with less redundancy, better consistency, security, and integrity. An <strong>RDBMS</strong> stores related tables and is queried with SQL.</p>",
            "<p>A <strong>table</strong> is rows × columns. A <strong>record</strong> is a row. A <strong>field</strong> is a column.</p>",
            table(["Key", "Role"], [
                ["Candidate", "Any unique non-null identifier — a table may have several"],
                ["Primary", "The chosen candidate; exactly one; never NULL"],
                ["Alternate", "A leftover candidate (still unique)"],
                ["Foreign", "Points at another table’s primary key; may repeat"],
            ]),
            box("exam", "ONE-LINER", "Primary key: unique, not null, one per table. Foreign key: lives in the child, points home."),
            box("exit", "EXIT TICKET", "1. DBMS besides Access? 2. Define a foreign key. 3. Can a table have two primary keys?"),
            box("hw", "HOMEWORK", "For a Student table list two candidate keys and choose a primary key. Write one sentence why CNIC is a poor classroom PK (privacy)."),
        ])),

        lecture(19, "ER models and the three cardinalities", "Unit 4 · Data and Analysis", "45 min", [
            "Draw entity rectangles and name attributes.",
            "Recognise 1:1, 1:M, and M:N.",
            "Resolve M:N with a junction table.",
        ], "\n".join([
            box("recap", "LAST LECTURE", "Keys identify rows. Relationships say how rows of two tables belong together."),
            fig(svgs.cardinalities(), "Figure L19.1 — Only M:N needs a junction table."),
            fig(svgs.er_library(), "Figure L19.2 — Library ER: Member and Book are M:N, resolved as BorrowRecord."),
            "<p>A student has one ID card (1:1). A teacher teaches many classes (1:M). Students enrol on many courses and a course has many students (M:N) — that last pair needs a junction (Enrolment) holding both foreign keys plus extras such as date.</p>",
            "<p><strong>Clinic in 15 minutes.</strong> Patient and Doctor are M:N, resolved as Appointment(AppointmentID PK, PatientID FK, DoctorID FK, VisitDate, Fee). Customer 1—M Order needs <em>no</em> junction: one order belongs to one customer. Students over-use junction tables.</p>",
            box("exit", "EXIT TICKET", "1. ER rectangle is which concept? 2. Which relationship needs a junction? 3. Name the library junction entity."),
            box("hw", "HOMEWORK", "On paper, Bus / Route / Student. A bus serves one route; many students ride many buses across a week — that last link may need a Ride junction with a date."),
        ])),

        lecture(20, "Referential integrity and Access objects", "Unit 4 · Data and Analysis", "45 min", [
            "State referential integrity with a school example.",
            "Warn about cascade delete.",
            "Name table, form, query, report.",
        ], "\n".join([
            box("recap", "LAST LECTURE", "M:N is two 1:M links through a junction. Those links only work if every foreign key points at a living parent."),
            "<p><strong>Referential integrity:</strong> every foreign key must match a living parent. You cannot store marks for StudentID 999 if that student does not exist.</p>",
            "<p><em>Cascade update</em> rewrites child FKs when the parent PK changes. <em>Cascade delete</em> removes child rows when the parent is deleted — use it like a chainsaw. Cascade-delete of a doctor wipes appointment history; better to forbid the delete or mark the doctor inactive.</p>",
            "<p>Access objects: <strong>table</strong> stores, <strong>form</strong> enters, <strong>query</strong> asks, <strong>report</strong> prints. Create a table in Datasheet or Design view; pick datatypes (Short Text, Number, Date/Time, Currency, Yes/No, AutoNumber for a surrogate PK).</p>",
            box("exit", "EXIT TICKET", "1. Define referential integrity. 2. Cascade update in one sentence. 3. Which object is for friendly entry?"),
            box("hw", "HOMEWORK", "Write a 3-mark caution: why cascade-delete on Doctor is dangerous in the clinic schema."),
        ])),

        lecture(21, "Queries, totals, and charts", "Unit 4 · Data and Analysis", "45 min", [
            "Put AND on the same criteria row and OR on different rows.",
            "Use Group By with Count or Avg.",
            "Pick line, pie, or bar for the story.",
        ], "\n".join([
            box("recap", "LAST LECTURE", "Tables store; forms enter; queries ask. Today the Design grid — the usual practical-exam discriminator."),
            table(["Need", "Design grid"], [
                ["CS students only", "Department Criteria: \"Computer Science\""],
                ["IT or CS", "Criteria / or: two department values"],
                ["Aslam in IT", "Name and Department on the SAME row"],
                ["Headcount per dept", "Totals on; Department Group By; StudentID Count"],
                ["Average marks per dept", "Department Group By; Marks Avg"],
            ]),
            "<p>AND is horizontal (one row). OR is vertical (criteria / or). Totals \\(\\Sigma\\): Group By + Count / Avg / Sum / Min / Max.</p>",
            "<p>Line charts show trends (monthly attendance). Pies show parts of a whole (pass/fail). Bars compare named categories (marks by department).</p>",
            box("memory", "RECITE", "AND same row. OR different rows. Chart for a monthly trend = line."),
            box("exit", "EXIT TICKET", "1. Aggregate for a mean? 2. Chart for a monthly trend? 3. How do you write OR in Query Design?"),
            box("hw", "HOMEWORK", "On paper, design a grouped query: average fee per doctor from Appointment. Name the Group By field and the aggregate."),
        ])),
    ])
