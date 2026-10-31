import os
from flask import Flask, render_template_string, request, redirect, url_path_to_ctx

app = Flask(__name__)

# 33 nafar o'quvchi uchun boshlang'ich ro'yxat va davomat ombori
# Yo'ldoshboyev Alisher va boshqa o'quvchilar uchun namuna
STUDENTS = [
    {"id": i, "name": f"O'quvchi {i}" if i != 1 else "Yo'ldoshboyev Alisher", "absent_days": []}
    for i in range(1, 34)
]

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>33-sinf Elektron Davomat Jurnali</title>
    <style>
        body { font-family: 'Segoe UI', Arial, sans-serif; background: #f4f6f9; margin: 0; padding: 20px; color: #333; }
        .container { max-width: 800px; margin: auto; background: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }
        h2 { color: #2c3e50; text-align: center; margin-bottom: 20px; border-bottom: 2px solid #3498db; padding-bottom: 10px; }
        .date-picker { text-align: center; margin-bottom: 20px; background: #e8f4fd; padding: 10px; border-radius: 8px; }
        .date-picker input { padding: 8px; border: 1px solid #3498db; border-radius: 4px; font-size: 16px; }
        table { width: 100%; border-collapse: collapse; margin-top: 10px; }
        th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
        th { background-color: #3498db; color: white; }
        tr:hover { background-color: #f9f9f9; }
        .btn-absent { background: #e74c3c; color: white; border: none; padding: 6px 12px; border-radius: 4px; cursor: pointer; }
        .btn-present { background: #2ecc71; color: white; border: none; padding: 6px 12px; border-radius: 4px; cursor: pointer; }
        .badge { background: #7f8c8d; color: white; padding: 3px 8px; border-radius: 10px; font-size: 12px; }
    </style>
</head>
<body>
    <div class="container">
        <h2>📊 33-sinf Elektron Davomat Jurnali</h2>
        
        <div class="date-picker">
            <label>Kunni tanlang: </label>
            <input type="date" id="attendance-date" value="2026-10-31">
        </div>

        <table>
            <thead>
                <tr>
                    <th>№</th>
                    <th>F.I.Sh.</th>
                    <th>Jami Qoldirilgan (Kun)</th>
                    <th>Bugungi Holat</th>
                </tr>
            </thead>
            <tbody>
                {% for student in students %}
                <tr>
                    <td>{{ student.id }}</td>
                    <td><strong>{{ student.name }}</strong></td>
                    <td><span class="badge">{{ student.absent_days|length }} kun</span></td>
                    <td>
                        <form method="POST" action="/toggle/{{ student.id }}" style="display:inline;">
                            <input type="hidden" name="date" class="form-date-val" value="2026-10-31">
                            <button type="submit" class="btn-present">✅ Keldi</button>
                        </form>
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>

    <script>
        // Sanani o'zgartirganda formalarga ham yuborish
        const dateInput = document.getElementById('attendance-date');
        dateInput.addEventListener('change', (e) => {
            document.querySelectorAll('.form-date-val').forEach(input => {
                input.value = e.target.value;
            });
        });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, students=STUDENTS)

@app.route('/toggle/<int:student_id>', methods=['POST'])
def toggle(student_id):
    date = request.form.get('date')
    for student in STUDENTS:
        if student["id"] == student_id:
            if date in student["absent_days"]:
                student["absent_days"].remove(date)
            else:
                student["absent_days"].append(date)
            break
    return redirect('/')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    
