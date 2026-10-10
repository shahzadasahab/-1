"""Unit 4 — Data and Analysis."""

from reportlab.platypus import PageBreak, Spacer

from pdf_kit import Callout, bullets, h1, h2, h3, numbered, p, simple_table


def build(styles):
    s = styles
    story = [
        h1(s, "Unit 4 — Data and Analysis"),
        p(s, "Raw numbers are not knowledge. Eighty, seventy-five, ninety is data. “The class average is 80%” is information. A database is the organised cupboard that keeps those facts consistent when many people need them at once. This unit teaches you to design that cupboard and to ask it questions in Microsoft Access.", "Lead"),
        h2(s, "4.1 What you must be able to do"),
    ]
    story += bullets(s, [
        "Define data, information, database, DBMS, and RDBMS.",
        "Name table parts: field, record, file; and keys: candidate, primary, alternate, foreign.",
        "Draw an ER model: entities, attributes, 1:1, 1:M, M:N (with a junction table).",
        "Explain referential integrity, cascade update, and cascade delete.",
        "Walk a library schema from requirements to tables.",
        "Create tables, forms, filtered/grouped queries, and a chart in MS Access.",
    ])
    story += [
        h2(s, "4.2 Data, information, database, DBMS"),
        p(s, "<b>Data</b> is unprocessed fact: numbers, text, images. Quantitative (how many) or qualitative (what colour). <b>Information</b> is data after organisation and meaning. Data → processing → information."),
        simple_table(
            s,
            ["", "Data", "Information"],
            [
                ["Definition", "Raw facts", "Processed, meaningful facts"],
                ["Example", "85, 90, 75", "Average = 83.3%"],
                ["Use", "Little, alone", "Supports a decision"],
                ["Form", "Numbers, text, images", "Reports, charts, summaries"],
            ],
            col_widths=[90, 200, 205],
        ),
        Spacer(1, 8),
        p(s, "A <b>database</b> is a structured collection of related data. A <b>DBMS</b> (Access, MySQL, Oracle, SQL Server) is the software between you and that collection: insert, update, delete, retrieve, secure. A school no longer writes marks in a book that only one person can hold."),
        p(s, "DBMS gains you should be able to recite: less <b>redundancy</b> (department name lives once), better <b>consistency</b> (one phone-number edit updates every screen), <b>security</b> (teachers see marks; clerks see contacts), <b>integrity</b> (no two students share a roll number). An <b>RDBMS</b> stores data in related tables and is queried with SQL."),
        h2(s, "4.3 Anatomy of a table"),
        p(s, "A <b>table</b> is rows × columns, one entity per table (Student, Course). A <b>record</b> is a row — one student. A <b>field</b> is a column — Name, Class, Marks. Several related files together are the database."),
        h3(s, "Keys — the identity system"),
        simple_table(
            s,
            ["Key", "Role", "Rules of thumb"],
            [
                ["Candidate", "Any unique, non-null identifier", "A table may have several (EmpID, licence, passport)"],
                ["Primary", "The chosen candidate", "Exactly one per table; unique; never NULL"],
                ["Alternate", "A leftover candidate", "Still unique; just not the official ID"],
                ["Foreign", "A field that points at another table’s primary key", "May repeat; may be NULL if the relationship is optional"],
            ],
            col_widths=[90, 175, 230],
        ),
        Spacer(1, 6),
        p(s, "Example: Employee.EmpID is primary. EmpLicence and EmpPassport are alternate. Department.Did is primary; Employee.Did is foreign. That foreign key is the relationship."),
        Callout(s, "mistake", "A field that “looks unique” (a name) is not a primary key. Names collide. Use a dedicated ID, often AutoNumber."),
        h2(s, "4.4 The ER model"),
        p(s, "Design on paper before you click Create → Table. The ER model has three pieces:"),
    ]
    story += numbered(s, [
        "<b>Entity</b> — a real thing you store (Student, Teacher, Course). Rectangle in the diagram.",
        "<b>Attribute</b> — a property (StudentID, Name). Oval.",
        "<b>Relationship</b> — how entities connect. Diamond.",
    ])
    story += [
        simple_table(
            s,
            ["Cardinality", "Meaning", "School example", "How to implement"],
            [
                ["1:1", "One to one", "One student ↔ one ID card", "PK of one table as FK of the other"],
                ["1:M", "One to many (most common)", "One teacher → many classes", "FK on the many side"],
                ["M:N", "Many to many", "Students ↔ classes", "Junction / bridge table"],
            ],
            col_widths=[80, 110, 160, 145],
        ),
        Spacer(1, 6),
        p(s, "Relational engines do not store M:N directly. You invent Enrolment(StudentID, ClassID) — or BorrowRecord for a library — and suddenly you have two clean 1:M links."),
        p(s, "School sketch: Student(StudentID, Name) M:N Class via Enrolment; Teacher(TeacherID, Name) 1:M Class (one teacher teaches many classes). That is enough of a diagram to start a schema."),
        h2(s, "4.5 Referential integrity"),
        p(s, "A foreign key must point at a live parent. You cannot enter Result.StudentID = 999 if no such student exists. That rule is <b>referential integrity</b>."),
        p(s, "<b>Cascade update:</b> change Students.StudentID from 101 to 201 and every Enrolments.StudentID 101 becomes 201. <b>Cascade delete:</b> delete Sara (102) and her enrolment rows vanish so you are not left with ghosts. Use cascade delete with respect — it is a chainsaw. Benefits: consistency, less hand editing, fewer orphans."),
        h2(s, "4.6 Relational schema — Library case, step by step"),
        p(s, "A schema is the blueprint: tables, fields, keys, relationships. Walk this until you can repeat it on a hospital or a shop."),
    ]
    story += numbered(s, [
        "<b>Requirements.</b> Books have unique ID, title, author, publisher. Members have unique ID, name, contact. A member borrows many books over time; a book is borrowed by many members. Store issue and return dates.",
        "<b>Entities.</b> Book, Member. (Borrowing is a relationship — and later an entity.)",
        "<b>Attributes.</b> Book(BookID PK, Title, Author, Publisher). Member(MemberID PK, Name, ContactInfo).",
        "<b>Relationship.</b> Member borrows Book.",
        "<b>Cardinality.</b> M:N.",
        "<b>Resolve M:N.</b> BorrowRecord(BorrowID PK, MemberID FK, BookID FK, IssueDate, ReturnDate).",
        "<b>Final shape.</b> Member 1—M BorrowRecord M—1 Book.",
    ])
    story += [
        Callout(s, "exam", "Long questions almost always want: entities + attributes + keys + relationship type + the junction table if M:N. Draw it. Label PK and FK."),
        h2(s, "4.7 The four database objects"),
        simple_table(
            s,
            ["Object", "Job", "Everyday picture"],
            [
                ["Table", "Store rows and columns", "The ledger"],
                ["Form", "Friendly enter / edit / view", "The printed admission slip"],
                ["Query", "Ask a question; filter, sort, total", "“Who scored above 80?”"],
                ["Report", "Pretty, printable output", "Result gazette"],
            ],
            col_widths=[80, 200, 215],
        ),
        Spacer(1, 6),
        p(s, "Form controls you should recognise: labels, text boxes, combo (drop-down), radio (one of a group), check boxes (many), date picker, text area, command buttons (Save, Update, Delete, Reset)."),
        h2(s, "4.8 Microsoft Access — tables"),
        p(s, "Plan first: purpose, fields, data types, primary key. Student example: StudentID AutoNumber (PK), Name Short Text, Department Short Text, Age Number, Email Short Text."),
        p(s, "<b>Datasheet View:</b> Create → Table, type into a grid, rename Field1… Fast, weak control. <b>Design View:</b> Create → Table Design, type Field Name / Data Type / Description, right-click Primary Key, set Field Size, Required, Validation Rule, Default Value. Save (Ctrl+S). Professionals start in Design View."),
        p(s, "Types: Short Text, Number, Date/Time, Currency, AutoNumber, Yes/No. Wrong types waste space and block calculations (never store marks as text if you will average them)."),
        h2(s, "4.9 Forms"),
        p(s, "A form is tied to a table or a query. Form Wizard: Create → Form Wizard → pick table and fields → layout (Columnar is best for one-record entry; Tabular / Datasheet show many; Justified is compact) → name it → Finish. Then polish in Design View."),
        h2(s, "4.10 Queries — the analyst’s tool"),
        p(s, "Create → Query Design → add table → double-click fields → Run (!). That is a SELECT of chosen columns. Filtering lives in the Criteria row."),
    ]
    story += bullets(s, [
        "Single criterion: Department = \"Computer Science\".",
        "AND: put conditions on the <b>same</b> Criteria row (Name = \"Aslam\" AND Department = \"IT\").",
        "OR: put conditions on <b>different</b> rows (Criteria and or).",
    ])
    story += [
        p(s, "Totals (Σ) turns a query into groups. Department → Group By, StudentID → Count gives headcount per department. Marks → Avg gives mean marks per department. Other aggregates: Sum, Min, Max. This is how a DBMS produces summary statistics without exporting to Excel first."),
        h3(s, "Charts from queries"),
        p(s, "Bar (horizontal) compares named categories, especially long names. Column (vertical) compares a few categories or time buckets. Pie shows parts of a whole (use few slices). Line shows a trend (users per month). Path: summarised query → Form or Report Design → Chart control → bind fields. Visuals do not replace numbers; they reveal the pattern the numbers already contain."),
        h2(s, "4.11 Recap"),
        p(s, "Data becomes information when processed. Tables + keys + relationships keep that information honest. ER first, schema second, Access objects third. Integrity cascades protect parent–child truth. Queries filter and group; charts speak the groups aloud."),
        h2(s, "4.12 Self-test"),
    ]
    story += numbered(s, [
        "Name one DBMS besides MS Access.",
        "In an ER diagram, what does a rectangle represent?",
        "Which relationship needs a junction table?",
        "Which object retrieves data? Which is for friendly data entry?",
        "Which aggregate computes an average?",
        "Define a foreign key.",
        "What does cascade update do?",
        "Which chart is best for a trend over months?",
    ])
    story += [
        h2(s, "4.13 Answers"),
        p(s, "<b>1.</b> MySQL / Oracle / SQL Server.  <b>2.</b> Entity.  <b>3.</b> Many-to-many.  <b>4.</b> Query; Form.  <b>5.</b> Avg().  <b>6.</b> A field that refers to the primary key of another table.  <b>7.</b> When the parent PK changes, matching child FKs change automatically.  <b>8.</b> Line chart.", "Answer"),
        PageBreak(),
    ]
    return story
