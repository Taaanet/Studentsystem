from flask import Flask, request, render_template_string
import pandas as pd
import os

app = Flask(__name__)

# ==========================
# Load Excel
# ==========================
EXCEL_FILE = "students.xlsx"

df = pd.read_excel(EXCEL_FILE)

if "MARK" in df.columns:
    df["MARK"] = pd.to_numeric(df["MARK"], errors="coerce")

total_students = len(df)

avg_mark = (
    round(df["MARK"].mean(), 2)
    if "MARK" in df.columns
    else 0
)



# ==========================
# HTML
# ==========================

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>

<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">

<title>Manarat Al Madina Schools</title>

<style>

*{
margin:0;
padding:0;
box-sizing:border-box;
font-family:'Segoe UI',Tahoma,sans-serif;
}

body{
background:#eef3f9;
}

.container{
max-width:1200px;
margin:auto;
padding:25px;
}

.header{
background:linear-gradient(135deg,#0f4c81,#1b74d1);
color:white;
padding:25px;
border-radius:18px;
text-align:center;
box-shadow:0 5px 20px rgba(0,0,0,.15);
}

.header h1{
font-size:32px;
}

.cards{
display:grid;
grid-template-columns:repeat(auto-fit,minmax(250px,1fr));
gap:20px;
margin-top:25px;
}

.card{
background:white;
padding:20px;
border-radius:15px;
box-shadow:0 5px 15px rgba(0,0,0,.08);
text-align:center;
}

.card h2{
color:#0f4c81;
font-size:30px;
}

.search-box{
background:white;
padding:20px;
border-radius:15px;
margin-top:25px;
box-shadow:0 5px 15px rgba(0,0,0,.08);
}

.search-box input{
width:100%;
padding:14px;
border-radius:10px;
border:1px solid #ccc;
font-size:16px;
}

.search-box button{
margin-top:10px;
width:100%;
padding:14px;
background:#0f4c81;
color:white;
border:none;
border-radius:10px;
font-size:16px;
cursor:pointer;
}

.search-box button:hover{
background:#0d3d68;
}

.student-card{
margin-top:30px;
background:white;
border-radius:20px;
overflow:hidden;
box-shadow:0 8px 25px rgba(0,0,0,.12);
display:flex;
flex-wrap:wrap;
}

.student-info{
flex:2;
padding:30px;
}

.student-avatar{
flex:1;
min-width:250px;
background:linear-gradient(135deg,#0f4c81,#1b74d1);
display:flex;
justify-content:center;
align-items:center;
padding:20px;
}

.student-avatar svg{
width:220px;
height:220px;
}

.student-info h2{
color:#0f4c81;
margin-bottom:20px;
}

.info-grid{
display:grid;
grid-template-columns:repeat(auto-fit,minmax(250px,1fr));
gap:12px;
}

.info-item{
background:#f8fafc;
padding:12px;
border-radius:10px;
border-left:5px solid #1b74d1;
}

.info-item b{
color:#0f4c81;
}

.progress-container{
margin-top:25px;
}

.progress-bar{
height:25px;
background:#ddd;
border-radius:30px;
overflow:hidden;
}

.progress-fill{
height:100%;
background:linear-gradient(90deg,#00b894,#00d084);
text-align:center;
color:white;
font-weight:bold;
line-height:25px;
}

.error{
background:#ffe6e6;
color:red;
padding:15px;
border-radius:10px;
margin-top:20px;
}

.footer{
text-align:center;
padding:20px;
color:#777;
}

</style>

</head>

<body>

<div class="container">

<div class="header">
<h1>🏫 Manarat Al Madina Schools</h1>
<p>Student Results Portal</p>
</div>

<div class="cards">

<div class="card">
<h2>{{total}}</h2>
<p>Total Students</p>
</div>

<div class="card">
<h2>{{avg}}</h2>
<p>Average Mark</p>
</div>

</div>

<div class="search-box">

<form method="POST">

<input
name="student_id"
placeholder="Enter Student ID"
required>

<button type="submit">
🔍 Search Student
</button>

</form>

</div>

{% if result %}

{% if result.error %}

<div class="error">
{{ result.error }}
</div>

{% else %}

<div class="student-card">

<div class="student-info">

<h2>🎓 Student Information</h2>

<div class="info-grid">

{% for k,v in result.items() %}

<div class="info-item">
<b>{{k}}</b><br>
{{v}}
</div>

{% endfor %}

</div>

{% if mark_percentage is not none %}

<div class="progress-container">

<h3 style="margin-bottom:10px;">
Academic Performance
</h3>

<div class="progress-bar">
<div class="progress-fill"
style="width:{{mark_percentage}}%">
{{mark_percentage}}%
</div>
</div>

</div>

{% endif %}

</div>

<div class="student-avatar">

<svg viewBox="0 0 512 512" fill="white">

<path d="M256 32L32 144l224 112 183-91v123h41V144L256 32z"/>

<path d="M136 238v84c0 59 54 106 120 106s120-47 120-106v-84l-120 60-120-60z"/>

<circle cx="256" cy="210" r="35"/>

</svg>

</div>

</div>

{% endif %}
{% endif %}

<div class="footer">
taaanet@gmail.com © 2026 © by Taha_Mohamadd 0554289816
</div>

</div>

</body>
</html>
"""

# ==========================
# Route
# ==========================

@app.route("/", methods=["GET", "POST"])
def dashboard():

    result = None
    mark_percentage = None

    if request.method == "POST":

        student_id = request.form.get("student_id")

        match = df[df["ID"].astype(str) == str(student_id)]

        if not match.empty:

            result = match.iloc[0].to_dict()

            if "MARK" in result:

                try:
                    student_mark = float(result["MARK"])

                    TOTAL_MARK = 20
                    mark_percentage = round(
                        (student_mark / TOTAL_MARK) * 100,
                        1
                 )

                  if mark_percentage > 100:
                      mark_percentage = 100

                except:
                    mark_percentage = 0

        else:

            result = {
                 "error": "Student not found"
            }

    return render_template_string(
    HTML,
    total=total_students,
    avg=avg_mark,
    result=result,
    mark_percentage=mark_percentage
    )

# ==========================
# Run
# ==========================

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port
    )
