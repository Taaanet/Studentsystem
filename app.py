from flask import Flask, request, render_template_string, send_from_directory
import pandas as pd
import os

app = Flask(**name**)

# -----------------------------

# تحميل ملف الطلاب

# -----------------------------

EXCEL_FILE = "students.xlsx"
df = pd.read_excel(EXCEL_FILE)

# تحويل الدرجات لأرقام

if "MARK" in df.columns:
df["MARK"] = pd.to_numeric(df["MARK"], errors="coerce")

# إحصائيات

total_students = len(df)

avg_mark = 0
if "MARK" in df.columns:
avg_mark = round(df["MARK"].mean(), 2)

top_student = None
if not df.empty and "MARK" in df.columns:
top_student = df.loc[df["MARK"].idxmax()]

# -----------------------------

# خدمة الشعار

# -----------------------------

@app.route("/logo.png")
def logo():
return send_from_directory(".", "logo.png")

HTML = """

<!DOCTYPE html>

<html lang="ar" dir="rtl">

<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>نتائج الطلاب</title>

<style>

*{
    box-sizing:border-box;
}

body{
    margin:0;
    background:#f4f7fc;
    font-family:Tahoma, Arial, sans-serif;
}

.container{
    max-width:1000px;
    margin:auto;
    padding:20px;
}

.header{
    text-align:center;
    margin-bottom:25px;
}

.header img{
    width:220px;
    max-width:100%;
}

.header h1{
    margin-top:15px;
    color:#182c61;
}

.cards{
    display:grid;
    grid-template-columns:repeat(auto-fit,minmax(220px,1fr));
    gap:15px;
    margin-bottom:25px;
}

.card{
    background:white;
    padding:20px;
    border-radius:15px;
    text-align:center;
    box-shadow:0 4px 12px rgba(0,0,0,.08);
}

.card h2{
    margin:0;
    color:#3498db;
}

.search-box{
    background:white;
    padding:20px;
    border-radius:15px;
    box-shadow:0 4px 12px rgba(0,0,0,.08);
}

input{
    width:100%;
    padding:14px;
    border:1px solid #ccc;
    border-radius:10px;
    font-size:16px;
}

button{
    width:100%;
    padding:14px;
    margin-top:10px;
    border:none;
    border-radius:10px;
    background:#3498db;
    color:white;
    font-size:16px;
    cursor:pointer;
}

button:hover{
    background:#2980b9;
}

.result-card{
    margin-top:25px;
    background:white;
    border-radius:15px;
    padding:25px;
    box-shadow:0 4px 12px rgba(0,0,0,.08);
}

.result-card img{
    width:150px;
    display:block;
    margin:auto;
    margin-bottom:15px;
}

.result-card h2{
    text-align:center;
    color:#182c61;
    margin-bottom:20px;
}

.result-row{
    padding:10px 0;
    border-bottom:1px solid #eee;
    font-size:18px;
}

.result-row:last-child{
    border-bottom:none;
}

.error{
    text-align:center;
    color:red;
    font-size:20px;
    font-weight:bold;
}

.footer{
    text-align:center;
    margin-top:30px;
    color:#777;
}

</style>

</head>

<body>

<div class="container">

```
<div class="header">
    <img src="/logo.png" alt="School Logo">
    <h1>مدارس المنارات الثانوية - المدينة المنورة</h1>
</div>

<div class="cards">

    <div class="card">
        <h2>{{ total }}</h2>
        <p>عدد الطلاب</p>
    </div>

    <div class="card">
        <h2>{{ avg }}</h2>
        <p>متوسط الدرجات</p>
    </div>

    <div class="card">
        <h2>{{ top }}</h2>
        <p>الطالب المتفوق</p>
    </div>

</div>

<div class="search-box">

    <form method="POST">

        <input
            type="text"
            name="student_id"
            placeholder="أدخل رقم الطالب أو رقم الهوية"
            required>

        <button type="submit">
            بحث
        </button>

    </form>

</div>

{% if result %}

    {% if result.error %}

        <div class="result-card">
            <div class="error">
                {{ result.error }}
            </div>
        </div>

    {% else %}

        <div class="result-card">

            <img src="/logo.png">

            <h2>نتيجة الطالب</h2>

            {% for k,v in result.items() %}

                <div class="result-row">
                    <strong>{{ k }}</strong> :
                    {{ v }}
                </div>

            {% endfor %}

        </div>

    {% endif %}

{% endif %}

<div class="footer">
    نظام نتائج الطلاب
</div>
```

</div>

</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def dashboard():

```
result = None

if request.method == "POST":

    student_id = request.form.get("student_id", "").strip()

    match = df[df["ID"].astype(str) == student_id]

    if not match.empty:
        result = match.iloc[0].to_dict()
    else:
        result = {
            "error": "لا توجد بيانات لهذا الرقم"
        }

return render_template_string(
    HTML,
    total=total_students,
    avg=avg_mark,
    top=top_student["NAME"] if top_student is not None and "NAME" in top_student else "-",
    result=result
)
```

if **name** == "**main**":
port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)
