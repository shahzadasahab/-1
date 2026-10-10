/* Class XII - Chapter 4 (Data and Analysis) - Part 2: Visualisation and Descriptive Statistics */
Lectures.add({
  id: 'xii-4-05',
  cls: 'XII',
  ch: 4,
  n: 5,
  title: 'Organising Data & Graphs with Matplotlib',
  titleUr: 'ڈیٹا کی ترتیب اور Matplotlib کے گراف',
  mins: 10,
  source: 'Unit 4 · §4.4 – 4.4.3, Line / Bar / Pie',
  keywords: ['data organization', 'table', 'frequency distribution', 'matplotlib', 'line graph', 'bar graph', 'pie chart', 'plt'],
  objectives: [
    '**Data organization** کے تین طریقے بیان کر سکیں: table، frequency distribution اور graph۔',
    '**Frequency distribution table** بنانا اور پڑھنا جان لیں۔',
    '**Matplotlib** سے **line graph**، **bar graph** اور **pie chart** کا code لکھ سکیں۔',
  ],
  blocks: [
    { t: 'say', ur: 'بچو، پچھلے lectures میں ہم نے data جمع کرنا، DataFrame بنانا اور missing values ٹھیک کرنا سیکھا۔ اب data صاف ہے۔ لیکن سینکڑوں numbers دیکھ کر کوئی بات سمجھ نہیں آتی۔ آج ہم سیکھیں گے کہ data کو ترتیب کیسے دیں اور پھر اسے تصویر کی شکل میں کیسے دکھائیں۔' },
    { t: 'h', ur: 'Data Organization and Representation' },
    { t: 'note', kind: 'def', ur: 'Definition: Data organization and representation اکٹھے کیے گئے data کو ایک منظم شکل میں ترتیب دینے کا عمل ہے، تاکہ اسے سمجھنا، analyze کرنا اور دوسروں تک پہنچانا آسان ہو جائے۔' },
    { t: 'say', ur: 'سوچیں کہ آپ کی کلاس کے ایک سو بیس بچوں کے نمبر ایک بے ترتیب کاغذ پر لکھے ہیں۔ ان سے کیا نتیجہ نکلے گا؟ کچھ نہیں۔ لیکن یہی نمبر table میں ہوں، یا گنتی کے خانوں میں، یا ایک graph میں، تو بات فوراً سمجھ آ جاتی ہے۔ کتاب کے مطابق representation کے تین عام طریقے ہیں۔' },
    { t: 'diagram', id: 'xii4.organise-ways', cap: 'Figure 4.2: Different ways to organize and represent data', say: 'اس تصویر میں تینوں طریقے ایک ساتھ ہیں۔ بائیں طرف Tabular representation ہے، یعنی rows اور columns۔ درمیان میں Frequency distribution table ہے، جس میں نمبروں کی ranges اور ہر range کی گنتی ہے۔ دائیں طرف Graphical representation ہے، جس میں data کو bars یا lines کی شکل میں دکھایا جاتا ہے۔' },
    { t: 'h', ur: 'Tabular Representation' },
    { t: 'say', ur: '**Table** data کو rows اور columns میں رکھتا ہے۔ اس سے values کا موازنہ اور خلاصہ بنانا آسان ہو جاتا ہے۔ کتاب کی مثال میں چار طلبہ کے تین مضامین کے نمبر اور ان کا average دیا گیا ہے۔' },
    {
      t: 'table',
      title: 'Students scores with average',
      head: ['Student', 'English', 'Math', 'Science', 'Average'],
      rows: [['Ahsan', '78', '82', '80', '80'], ['Inaya', '88', '76', '92', '85'], ['Bilal', '70', '60', '75', '68'], ['Saba', '90', '84', '85', '86']],
      say: 'اس table میں ہر row ایک طالب علم کی ہے اور ہر column ایک مضمون کا۔ احسن کے نمبر اٹھہتر، بیاسی اور اسی ہیں، اور average اسی ہے۔ عنایہ کا average پچاسی، بلال کا اڑسٹھ اور صبا کا چھیاسی ہے۔ ایک نظر میں آپ بتا سکتے ہیں کہ سب سے آگے کون ہے۔',
    },
    { t: 'h', ur: 'Frequency Distribution Table' },
    { t: 'say', ur: 'جب data بہت زیادہ ہو تو ہر نمبر الگ لکھنا مشکل ہو جاتا ہے۔ تب ہم نمبروں کو **ranges** یعنی intervals میں گروپ کر دیتے ہیں۔ پھر گنتے ہیں کہ ہر range میں کتنے بچے آئے۔ اس گنتی کو **frequency** کہتے ہیں اور پورے table کو **frequency distribution table**۔' },
    {
      t: 'table',
      title: 'Frequency distribution of marks',
      head: ['Range of Marks', 'Frequency'],
      rows: [['0 – 49', '3'], ['50 – 59', '5'], ['60 – 69', '7'], ['70 – 79', '9'], ['80 – 89', '4'], ['90 – 100', '2']],
      say: 'یہ table دیکھیں۔ صفر سے انچاس نمبر لینے والے تین بچے ہیں۔ پچاس سے انسٹھ میں پانچ، ساٹھ سے انہتر میں سات، اور ستر سے اناسی میں نو بچے ہیں۔ اسی سے نواسی میں چار، اور نوے سے سو میں صرف دو بچے ہیں۔ سب سے زیادہ بچے ستر سے اناسی والی range میں ہیں۔',
    },
    { t: 'note', kind: 'tip', ur: 'کتاب کے مطابق یہ table بتاتا ہے کہ طلبہ کے نمبر مختلف ranges میں کیسے پھیلے ہیں اور زیادہ تر طلبہ کے نمبر کہاں ہیں۔ یہاں کل تیس طلبہ ہیں، تین جمع پانچ جمع سات جمع نو جمع چار جمع دو۔' },
    { t: 'h', ur: 'Graphical Representation' },
    { t: 'note', kind: 'def', ur: 'Definition: Graphs اور charts کے ذریعے data کو بصری شکل میں پیش کرنا، تاکہ trends، patterns اور موازنے آسانی سے سمجھ آئیں، Graphical representation کہلاتا ہے۔' },
    { t: 'say', ur: 'Python میں data کو تصویر بنانے کے لیے کئی libraries ہیں۔ سب سے مشہور **Matplotlib** ہے۔ اس سے line graph، bar chart اور scatter plot جیسے charts بنتے ہیں۔ یہ سادہ بھی ہے اور لچکدار بھی، اس لیے تعلیم اور تحقیق میں عام استعمال ہوتی ہے۔ ہم ہمیشہ `import matplotlib.pyplot as plt` لکھتے ہیں۔ آگے ہر graph میں `plt` سے مراد یہی library ہے۔' },
    { t: 'h', ur: 'Line Graph' },
    { t: 'say', ur: '**Line graph** بتاتا ہے کہ وقت کے ساتھ data کیسے بدلتا ہے۔ نقطوں کو سیدھی لکیروں سے جوڑا جاتا ہے۔ اس سے trends اور اتار چڑھاؤ صاف نظر آتے ہیں، جیسے دنوں، مہینوں یا سالوں میں۔ اس کا syntax ہے plt.plot کے اندر x کی values اور y کی values۔' },
    {
      t: 'code',
      lang: 'python',
      code: `import matplotlib.pyplot as plt

years = ["2021", "2022", "2023", "2024"]
marks = [65, 70, 75, 80]

plt.figure()
plt.plot(years, marks, marker='o', color='blue', linewidth=2)
plt.xlabel("Year")
plt.ylabel("Percentage Marks")
plt.title("Students Performance Over Years")
plt.show()`,
      say: 'یہ کتاب کا پہلا graph ہے۔ پہلے library import ہوتی ہے۔ پھر years اور marks کی دو lists بنتی ہیں۔ plt.figure نیا canvas بناتا ہے۔ plt.plot لکیر کھینچتا ہے، marker o ہر نقطے پر گول نشان لگاتا ہے، color blue رنگ بتاتا ہے اور linewidth لکیر کی موٹائی۔ xlabel، ylabel اور title محور اور heading لکھتے ہیں۔ آخر میں plt.show graph دکھا دیتا ہے۔',
    },
    { t: 'diagram', id: 'xii4.line-chart', cap: 'Figure 4.3: Line graph of year-wise percentage', say: 'نتیجہ دیکھیں۔ دو ہزار اکیس میں پینسٹھ فیصد، پھر ستر، پچھتر اور دو ہزار چوبیس میں اسی فیصد۔ لکیر اوپر جا رہی ہے، یعنی کارکردگی ہر سال بہتر ہو رہی ہے۔' },
    {
      t: 'code',
      lang: 'python',
      code: `import matplotlib.pyplot as plt

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
temps = [12, 15, 22, 25, 30, 35, 38, 37, 33, 28, 23, 18]

plt.plot(months, temps, marker='o', color='blue')
plt.title("Average Monthly Temperature", fontsize=14)
plt.xlabel("Months", fontsize=12)
plt.ylabel("Temperature (C)", fontsize=12)
plt.grid(True)
plt.show()`,
      say: 'دوسری مثال مہینوں کے درجہ حرارت کی ہے۔ months اور temps دو lists ہیں۔ fontsize سے لکھائی کا سائز بدلتا ہے۔ plt.grid True ڈالنے سے پس منظر میں خانے بن جاتے ہیں جن سے values پڑھنا آسان ہو جاتا ہے۔',
    },
    { t: 'diagram', id: 'xii4.line-temps', cap: 'Figure 4.5: Average temperature month wise', say: 'جنوری سے جولائی تک درجہ حرارت بڑھتا ہے اور جولائی میں اڑتیس ڈگری کو پہنچ جاتا ہے۔ پھر دسمبر تک آہستہ آہستہ کم ہو کر اٹھارہ رہ جاتا ہے۔ ہمارے ہاں گرمی کا یہی چکر ہوتا ہے۔' },
    { t: 'h', ur: 'Bar Graph' },
    { t: 'say', ur: '**Bar graph** مختلف categories کی values کا موازنہ کرتا ہے۔ ہر category کے لیے ایک مستطیل bar بنتا ہے۔ bar کی اونچائی اس category کی value ہوتی ہے۔ مثلاً مضمون وار نمبر۔ اس کا syntax ہے plt.bar، جس میں پہلے category والی values اور پھر ان کی numeric values دیتے ہیں۔' },
    {
      t: 'code',
      lang: 'python',
      code: `import pandas as pd
import matplotlib.pyplot as plt

data = {
    "Name": ["Arabic", "English", "Math", "Science", "Social Science"],
    "Marks": [45, 57, 80, 65, 50]
}
df = pd.DataFrame(data)

plt.figure(figsize=(8, 5))
plt.bar(df["Name"], df["Marks"], edgecolor='black', color='skyblue')
plt.title("Marks vs Students")
plt.xlabel("Students")
plt.ylabel("Marks")
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()`,
      say: 'پہلے ایک dictionary سے DataFrame بنایا گیا ہے۔ پھر plt.bar میں df کے Name اور Marks columns دیے گئے ہیں۔ edgecolor black سے bars کے گرد کالی لکیر آتی ہے اور color skyblue سے رنگ ہلکا نیلا ہوتا ہے۔ grid کے ساتھ axis y کا مطلب ہے کہ صرف افقی خانے بنیں۔ alpha سے لکیر ہلکی ہو جاتی ہے۔ tight layout لکھائی کو کٹنے سے بچاتا ہے۔',
    },
    { t: 'diagram', id: 'xii4.bar-chart', cap: 'Figure 4.4: Bar chart showing student performance subject wise', say: 'یہاں پانچ مضامین کے پانچ bars ہیں۔ سب سے اونچا bar Math کا ہے اور سب سے چھوٹا Arabic کا۔ آپ ایک نظر میں موازنہ کر سکتے ہیں۔' },
    { t: 'h', ur: 'Pie Chart' },
    { t: 'say', ur: '**Pie chart** پورے کے حصے دکھاتا ہے۔ دائرے کا ہر slice ایک category کا تناسب یا فیصد ہوتا ہے۔ جیسے ایک پیزا کے ٹکڑے۔ تمام فیصد کا مجموعہ ہمیشہ سو ہوتا ہے۔ syntax ہے plt.pie، جس میں numeric values اور labels دیے جاتے ہیں۔' },
    {
      t: 'code',
      lang: 'python',
      code: `import matplotlib.pyplot as plt

subjects = ['Math', 'Physics', 'Computer Science', 'Biology', 'Chemistry']
students = [25, 15, 30, 10, 20]

plt.figure()
plt.pie(students, labels=subjects, autopct='%1.1f%%', startangle=90)
plt.title("Percentage of Students Choosing Different Subjects",
          fontsize=14, fontweight='bold')
plt.show()`,
      say: 'subjects میں مضامین کے نام ہیں اور students میں ہر مضمون چننے والوں کی تعداد۔ autopct فیصد slice کے اندر لکھتا ہے، اور اس کا format ایک اعشاریہ والا ہے۔ startangle نوے کا مطلب ہے کہ پہلا slice اوپر سے شروع ہو۔ fontweight bold سے heading موٹی لکھی جاتی ہے۔',
    },
    { t: 'diagram', id: 'xii4.pie', cap: 'Figure 4.6: Example of Pie Chart', say: 'سب سے بڑا slice Computer Science کا ہے، تیس فیصد۔ پھر Math پچیس، Chemistry بیس، Physics پندرہ اور Biology دس فیصد۔ ان سب کا مجموعہ سو فیصد بنتا ہے۔' },
    {
      t: 'table',
      title: 'Which graph for which job?',
      head: ['Graph', 'Syntax', 'Best use'],
      rows: [['Line graph', 'plt.plot(x, y)', 'وقت کے ساتھ تبدیلی'], ['Bar graph', 'plt.bar(x, y)', 'categories کا موازنہ'], ['Pie chart', 'plt.pie(values, labels=...)', 'پورے کے حصے']],
      say: 'خلاصہ یاد کر لیں۔ وقت کے ساتھ تبدیلی کے لیے line graph۔ categories کے موازنے کے لیے bar graph۔ اور پورے کے حصے دکھانے کے لیے pie chart۔',
    },
    { t: 'note', kind: 'exam', ur: 'امتحان میں اکثر پوچھا جاتا ہے: دو data visualization techniques کی وضاحت کریں۔ ہر graph کی تعریف، syntax، ایک مثال اور اس کا استعمال لکھیں۔ سوال میں کتاب کے مطابق line graph کو trends کے لیے اور bar graph کو موازنے کے لیے بتائیں۔' },
    { t: 'terms', items: [{ en: 'Frequency', ur: 'کسی range میں آنے والی values کی گنتی' }, { en: 'Matplotlib', ur: 'Python کی graph بنانے والی library' }, { en: 'Line graph', ur: 'وقت کے ساتھ تبدیلی دکھانے والا graph' }, { en: 'Bar graph', ur: 'categories کا موازنہ کرنے والا graph' }, { en: 'Pie chart', ur: 'پورے کے حصے دکھانے والا دائرہ' }] },
    { t: 'recap', items: ['Data کو table، frequency distribution اور graph میں ترتیب دیا جاتا ہے۔', 'Frequency distribution table میں ranges اور ہر range کی گنتی ہوتی ہے۔', 'Line graph = وقت کے ساتھ تبدیلی، Bar graph = categories کا موازنہ، Pie chart = پورے کے حصے۔', 'Matplotlib میں plt.plot، plt.bar اور plt.pie کے بعد plt.show سے graph دکھتا ہے۔'] },
  ],
  quiz: [
    { q: 'Frequency distribution table میں frequency کا کیا مطلب ہے؟', opts: ['کسی range میں آنے والی values کی گنتی', 'سب نمبروں کا average', 'سب سے بڑا نمبر', 'graph کا رنگ'], a: 0, why: 'ہر range میں جتنے data points آئیں، وہی اس کی frequency ہوتی ہے۔' },
    { q: 'وقت کے ساتھ data میں تبدیلی دکھانے کے لیے کون سا graph بہترین ہے؟', opts: ['Pie chart', 'Bar graph', 'Line graph', 'Table'], a: 2, why: 'Line graph نقطوں کو جوڑ کر trends اور اتار چڑھاؤ دکھاتا ہے۔' },
    { q: 'Pie chart کے تمام slices کے فیصد کا مجموعہ کتنا ہوتا ہے؟', opts: ['پچاس', 'ایک سو', 'دو سو', 'کوئی بھی'], a: 1, why: 'Pie chart پورے کے حصے دکھاتا ہے، اس لیے مجموعہ سو فیصد ہوتا ہے۔' },
    { q: 'Matplotlib میں graph اسکرین پر دکھانے کا function کون سا ہے؟', opts: ['plt.figure()', 'plt.title()', 'plt.grid()', 'plt.show()'], a: 3, why: 'آخر میں plt.show() final graph کو display کرتا ہے۔' },
  ],
  homework: ['اپنی کلاس کے دس بچوں کے نمبر لے کر ایک frequency distribution table بنائیں، چھ ranges کے ساتھ۔', 'اپنے ایک ہفتے کے study hours کا line graph بنانے کا Python code لکھیں۔', 'اپنے دن کی سرگرمیوں، یعنی پڑھائی، نیند اور تفریح، کے لیے pie chart کا code لکھیں۔'],
});

Lectures.add({
  id: 'xii-4-06',
  cls: 'XII',
  ch: 4,
  n: 6,
  title: 'Histogram, Scatter Plot & Box Plot',
  titleUr: 'ہسٹوگرام، اسکیٹر پلاٹ اور باکس پلاٹ',
  mins: 10,
  source: 'Unit 4 · §4.5 (iv) – (vi)',
  keywords: ['histogram', 'bins', 'scatter plot', 'box plot', 'boxplot', 'quartile', 'median', 'matplotlib', 'distribution'],
  objectives: [
    '**Histogram** اور bar graph میں فرق بتا سکیں اور `plt.hist` استعمال کر سکیں۔',
    '**Scatter plot** سے دو variables کا تعلق پڑھ سکیں۔',
    '**Box plot** کی پانچ key values بیان کر سکیں اور دو datasets کا موازنہ کر سکیں۔',
  ],
  blocks: [
    { t: 'say', ur: 'بچو، پچھلے lecture میں ہم نے line graph، bar graph اور pie chart بنائے۔ آج تین اور graphs سیکھیں گے جو data کی distribution اور آپس کے تعلق کو دکھاتے ہیں۔ یہ ہیں Histogram، Scatter plot اور Box plot۔' },
    { t: 'h', ur: 'Histogram' },
    { t: 'say', ur: '**Histogram** numerical data کی distribution دکھاتا ہے۔ یہ values کو ranges میں گروپ کرتا ہے جنہیں **bins** کہتے ہیں۔ پھر ہر bin میں آنے والی values کی گنتی bar کی اونچائی بنتی ہے۔ یہ وہی کام ہے جو ہم نے frequency distribution table میں کیا تھا، فرق یہ ہے کہ یہاں تصویر بنتی ہے۔' },
    { t: 'note', kind: 'def', ur: 'Definition: Histogram numerical data کی distribution کو bins یعنی ranges میں گروپ کر کے دکھاتا ہے۔ Bar graph کے برعکس اس کے bars آپس میں جڑے ہوتے ہیں، کیونکہ data continuous ہوتا ہے۔' },
    { t: 'compare', left: { title: 'Bar graph', items: ['الگ الگ categories کا موازنہ', 'bars کے درمیان فاصلہ ہوتا ہے', 'مثال: مضمون وار نمبر'] }, right: { title: 'Histogram', items: ['numeric data کی distribution', 'bars آپس میں جڑے ہوتے ہیں', 'مثال: نمبروں کی ranges میں طلبہ کی گنتی'] }, say: 'Bar graph categories کا موازنہ کرتا ہے اور اس کے bars کے درمیان خالی جگہ ہوتی ہے۔ Histogram numeric data کی distribution دکھاتا ہے اور اس کے bars آپس میں ملے ہوتے ہیں۔ یہ فرق امتحان میں ضرور پوچھا جاتا ہے۔' },
    { t: 'math', tex: '\\text{plt.hist(scores, bins)}', cap: 'Histogram syntax', say: 'Syntax ہے plt dot hist، قوسین میں scores اور bins۔ scores numeric data ہے اور bins نمبروں کی ranges کی حدیں ہیں۔' },
    {
      t: 'code',
      lang: 'python',
      code: `import matplotlib.pyplot as plt

scores = [45, 50, 55, 60, 62, 65, 68, 70, 72, 75,
          78, 80, 82, 85, 88, 90, 92, 95, 98, 100]
bins = [40, 50, 60, 70, 80, 90, 100]

plt.hist(scores, bins=bins, edgecolor='black')
plt.title("Distribution of Student Scores")
plt.xlabel("Score Range")
plt.ylabel("Number of Students")
plt.grid(axis='y')
plt.show()`,
      say: 'یہاں بیس طلبہ کے نمبر scores میں ہیں اور bins میں چھ ranges کی حدیں ہیں، چالیس سے سو تک۔ plt.hist ان نمبروں کو bins میں گنتا ہے۔ edgecolor black سے bars کے کنارے نظر آتے ہیں۔ باقی lines title اور labels لگاتی ہیں۔ یاد رکھیں، آخری bin میں سو بھی شامل ہوتا ہے۔',
    },
    { t: 'diagram', id: 'xii4.histogram', cap: 'Figure 4.7: Histogram of student scores in different score ranges', say: 'نتیجہ دیکھیں۔ چالیس سے پچاس میں ایک طالب علم، پچاس سے ساٹھ میں دو، اور ساٹھ سے ستر میں چار۔ ستر سے اسی میں چار، اسی سے نوے میں چار، اور نوے سے سو میں پانچ۔ سب سے اونچا bar آخری ہے، یعنی زیادہ تر طلبہ کے نمبر نوے سے اوپر ہیں۔' },
    { t: 'points', title: 'Histogram کیسے پڑھیں؟', items: ['ہر bar ایک score range میں طلبہ کی تعداد دکھاتا ہے۔', 'X-axis پر score ranges یعنی bins ہوتی ہیں۔', 'Y-axis پر طلبہ کی تعداد ہوتی ہے۔', 'اس سے data کی distribution سمجھ آتی ہے۔'] },
    { t: 'h', ur: 'Scatter Plot' },
    { t: 'say', ur: '**Scatter plot** دو numerical variables کے درمیان تعلق دکھاتا ہے۔ ہر نقطہ ایک data point ہوتا ہے، جس کا ایک x اور ایک y ہوتا ہے۔ مثلاً بارش کتنی ہوئی اور فصل کتنی ہوئی۔ نقطے پھیلے ہوئے ہوں تو pattern خود نظر آ جاتا ہے۔' },
    { t: 'math', tex: '\\text{plt.scatter(x\\_values, y\\_values)}', cap: 'Scatter plot syntax', say: 'Syntax ہے plt dot scatter، قوسین میں x values اور y values۔ x values افقی محور پر اور y values عمودی محور پر جاتی ہیں۔' },
    {
      t: 'code',
      lang: 'python',
      code: `import matplotlib.pyplot as plt

x_values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
y_values = [2, 4, 5, 4, 7, 8, 9, 12, 11, 15]

plt.scatter(x_values, y_values, color='blue', alpha=0.7)
plt.title('Example Scatter Plot')
plt.xlabel('X-axis Values')
plt.ylabel('Y-axis Values')
plt.show()`,
      say: 'x values ایک سے دس تک ہیں اور y values ان کے جوڑ ہیں۔ plt.scatter دس نقطے بناتا ہے۔ color blue نقطوں کو نیلا کرتا ہے۔ alpha صفر اعشاریہ سات سے نقطے تھوڑے شفاف ہو جاتے ہیں تاکہ اوپر نیچے آنے والے نقطے بھی نظر آئیں۔',
    },
    { t: 'diagram', id: 'xii4.scatter', cap: 'Figure 4.8: Scatter graph, a rising pattern', say: 'نقطے بائیں نیچے سے دائیں اوپر کی طرف جا رہے ہیں۔ سرخ dashed line صرف سمجھانے کے لیے ہے کہ رجحان اوپر کو ہے۔ یعنی x بڑھتا ہے تو عام طور پر y بھی بڑھتا ہے۔ کتاب کی مثال میں یہ بارش اور فصل کی پیداوار ہے، جتنی زیادہ بارش، اتنی زیادہ پیداوار۔' },
    { t: 'note', kind: 'tip', ur: 'یاد رکھیں، scatter plot صرف تعلق دکھاتا ہے۔ نقطے نیچے سے اوپر جائیں تو دونوں variables ساتھ بڑھ رہے ہیں۔ اوپر سے نیچے جائیں تو ایک بڑھنے پر دوسرا کم ہو رہا ہے۔ بکھرے ہوئے نقطوں کا مطلب ہے کہ کوئی واضح تعلق نہیں۔' },
    { t: 'h', ur: 'Box Plot' },
    { t: 'say', ur: 'اب تیسرا graph، **Box plot**۔ یہ numerical data کو صرف پانچ key values سے خلاصہ بنا کر دکھاتا ہے۔ اس سے دو datasets کا موازنہ بھی آسان ہو جاتا ہے اور یہ بھی پتا چلتا ہے کہ data کتنا پھیلا ہوا ہے۔' },
    { t: 'note', kind: 'def', ur: 'Definition: Box plot ایسا graph ہے جو numerical data کی distribution کو پانچ key values سے خلاصہ کرتا ہے: minimum، first quartile Q1، median Q2، third quartile Q3 اور maximum۔' },
    { t: 'table', title: 'Box plot کی پانچ values', head: ['Value', 'مطلب'], rows: [['Minimum', 'سب سے چھوٹی value'], ['Q1', 'First quartile: نیچے کے پچیس فیصد data کی حد'], ['Median (Q2)', 'درمیانی value'], ['Q3', 'Third quartile: اوپر کے پچیس فیصد data کی حد'], ['Maximum', 'سب سے بڑی value']], say: 'پانچ values یاد کریں۔ Minimum سب سے چھوٹی۔ Q1 پہلا quartile۔ Median یعنی Q2 درمیان کی value۔ Q3 تیسرا quartile۔ اور Maximum سب سے بڑی۔ quartiles کا حساب ہم اگلے lecture میں کریں گے۔' },
    {
      t: 'code',
      lang: 'python',
      code: `import matplotlib.pyplot as plt

rainfall = [120, 135, 150, 160, 175, 180, 190, 200, 210, 220]
crop_yield = [100, 115, 130, 140, 150, 160, 170, 185, 200, 215]

plt.boxplot([rainfall, crop_yield], patch_artist=True)
plt.xticks([1, 2], ['Rainfall (mm)', 'Crop Yield Index'])
plt.title('Box Plot of Rainfall and Crop Yield')
plt.ylabel('Observed Values')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()`,
      say: 'یہاں دو datasets ہیں، بارش اور فصل کی پیداوار۔ plt.boxplot کو ان دونوں کی list دی گئی ہے، تو دو boxes بنیں گے۔ patch_artist True ہو تو boxes رنگ سے بھرے جا سکتے ہیں۔ xticks نیچے ہر box کا نام لکھتا ہے۔ باقی lines title اور grid لگاتی ہیں۔',
    },
    { t: 'diagram', id: 'xii4.boxplot-compare', cap: 'Figure 4.9: Box plot showing rainfall and crop yield distribution', say: 'ہر box کے اندر کی لکیر median ہے۔ box کا نچلا کنارہ Q1 اور اوپر کا کنارہ Q3 ہے۔ اوپر اور نیچے کی لکیریں whiskers ہیں، جو maximum اور minimum تک جاتی ہیں۔ بارش کا median ایک سو ستتر اعشاریہ پانچ ہے اور فصل کا ایک سو پچپن۔ یعنی بارش کی values عام طور پر زیادہ ہیں۔' },
    { t: 'points', title: 'Box plot کے Key Points', items: ['Box درمیانی پچاس فیصد data دکھاتا ہے، یعنی Q1 سے Q3 تک۔', 'Box کے اندر کی لکیر median ہے۔', 'Whiskers minimum اور maximum values دکھاتی ہیں۔', 'دو یا زیادہ datasets کے distribution کا موازنہ کرنے کے لیے مفید ہے۔'] },
    { t: 'note', kind: 'exam', ur: 'امتحان کا سوال: Histogram اور Bar graph میں فرق بتائیں۔ جواب: Histogram میں data continuous ہوتا ہے اور bars آپس میں جڑے ہوتے ہیں۔ Bar graph categories کا موازنہ کرتا ہے اور bars الگ ہوتے ہیں۔' },
    { t: 'terms', items: [{ en: 'Bins', ur: 'histogram کی ranges' }, { en: 'Distribution', ur: 'data کا پھیلاؤ، کہاں کتنی values' }, { en: 'Scatter plot', ur: 'دو variables کا تعلق دکھانے والے نقطے' }, { en: 'Quartile', ur: 'sorted data کے چار برابر حصوں کی حدیں' }, { en: 'Whisker', ur: 'box سے minimum اور maximum تک جانے والی لکیر' }] },
    { t: 'recap', items: ['Histogram = bins میں numeric data کی distribution، bars جڑے ہوتے ہیں۔', 'Scatter plot = دو variables کا تعلق، ہر نقطہ ایک data point۔', 'Box plot = minimum، Q1، median، Q3، maximum کا خلاصہ۔', 'Syntax: plt.hist، plt.scatter اور plt.boxplot۔'] },
  ],
  quiz: [
    { q: 'Histogram کے bars آپس میں جڑے کیوں ہوتے ہیں؟', opts: ['کیونکہ data continuous ہوتا ہے', 'کیونکہ data categories ہوتا ہے', 'کیونکہ رنگ ایک ہوتا ہے', 'کیونکہ grid لگی ہوتی ہے'], a: 0, why: 'Histogram continuous numerical data کو bins میں دکھاتا ہے، اس لیے bars کے درمیان وقفہ نہیں ہوتا۔' },
    { q: 'Scatter plot کا کیا مقصد ہے؟', opts: ['پورے کے حصے دکھانا', 'دو numerical variables کا تعلق دکھانا', 'وقت کے ساتھ تبدیلی دکھانا', 'categories کی گنتی'], a: 1, why: 'ہر نقطہ ایک x اور ایک y دکھاتا ہے، اس سے دو variables کا تعلق نظر آتا ہے۔' },
    { q: 'Box plot میں box کے اندر کی لکیر کیا ہوتی ہے؟', opts: ['Mean', 'Mode', 'Median', 'Maximum'], a: 2, why: 'Box کے اندر کی لکیر median یعنی Q2 دکھاتی ہے۔' },
    { q: 'Box plot کی پانچ key values میں کون سی شامل نہیں؟', opts: ['Minimum', 'Q1', 'Variance', 'Maximum'], a: 2, why: 'پانچ values یہ ہیں: minimum، Q1، median، Q3 اور maximum۔ Variance اس میں شامل نہیں۔' },
  ],
  homework: ['اپنی کلاس کے پندرہ طلبہ کے نمبر لے کر histogram کا Python code لکھیں اور بتائیں کہ زیادہ تر نمبر کس range میں ہیں۔', 'پچھلے ہفتے کی روزانہ study hours اور نیند کے گھنٹوں کا scatter plot بنانے کا code لکھیں۔', 'Histogram اور Bar graph میں دو فرق لکھیں۔'],
});
