from flask import Flask, request, render_template_string
import pandas as pd
import os

app = Flask(__name__)

# 📁 Excel file
EXCEL_FILE = "students.xlsx"
df = pd.read_excel(EXCEL_FILE)

# 🧠 تجهيز بيانات رقمية
df["MARK"] = pd.to_numeric(df["MARK"], errors="coerce")

# 📊 إحصائيات
total_students = len(df)
avg_mark = round(df["MARK"].mean(), 2)

top_student = df.loc[df["MARK"].idxmax()] if not df.empty else None

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Manarat Al Madina Secondary Schools</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <style>
        body {
            font-family: Arial;
            background: #f4f7fc;
            margin: 0;
        }

        .container {
            max-width: 1100px;
            margin: auto;
            padding: 20px;
        }

        h1 {
            text-align: center;
            color: #2c3e50;
        }

        .cards {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 15px;
            margin-top: 20px;
        }

        .card {
            background: white;
            padding: 15px;
            border-radius: 12px;
            box-shadow: 0 3px 10px rgba(0,0,0,0.1);
            text-align: center;
        }

        .card h2 {
            margin: 0;
            color: #3498db;
        }

        .search-box {
            margin: 20px 0;
        }

        input {
            width: 100%;
            padding: 12px;
            border-radius: 10px;
            border: 1px solid #ccc;
        }

        button {
            width: 100%;
            padding: 12px;
            margin-top: 10px;
            background: #3498db;
            color: white;
            border: none;
            border-radius: 10px;
        }

        table {
            width: 100%;
            margin-top: 20px;
            border-collapse: collapse;
            background: white;
            border-radius: 10px;
            overflow: hidden;
        }

        th, td {
            padding: 10px;
            border-bottom: 1px solid #ddd;
            text-align: center;
        }

        th {
            background: #3498db;
            color: white;
        }

    </style>
</head>

<body>

<div class="container">

    <h1>🏫Manarat Al Madina Secondary Schoolsd</h1>

    <!-- 📊 Stats -->
    <div class="cards">
        <div class="card">
            <h2>{{total}}</h2>
            <p>👨‍🎓 Students</p>
        </div>

        <div class="card">
            <h2>{{avg}}</h2>
            <p>📊 Average Mark</p>
        </div>

        <div class="card">
            <h2>{{top}}</h2>
            <p>🏆 Top Student</p>
        </div>
    </div>

    <!-- 🔍 Search -->
    <div class="search-box">
        <form method="post">
            <input name="student_id" placeholder="Search by ID">
            <button type="submit">Search</button>
        </form>
    </div>

    {% if result %}
        <div class="card">
            {% if result.error %}
                <p style="color:red">{{ result.error }}</p>
            {% else %}
                {% for k, v in result.items() %}
                    <p><b>{{k}}</b>: {{v}}</p>
                {% endfor %}
            {% endif %}
        </div>
    {% endif %}

   

</div>

</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def dashboard():
    result = None

    if request.method == "POST":
        student_id = request.form.get("student_id")
        match = df[df["ID"].astype(str) == str(student_id)]

        if not match.empty:
            result = match.iloc[0].to_dict()
        else:
            result = {"error": "Student not found"}

    return render_template_string(
        HTML,
        total=total_students,
        avg=avg_mark,
        top=top_student["NAME"] if top_student is not None else "N/A",
        result=result,
        columns=df.columns,
        table_data=df.to_dict(orient="records")
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
