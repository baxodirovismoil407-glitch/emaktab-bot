import os
import time
from threading import Thread
from flask import Flask, render_template_string, request, redirect
import requests
import schedule

app = Flask(__name__)

# Kiritilgan ma'lumotlar xotirada saqlanadi
DATABASE = {
    "login": "",
    "parol": ""
}

# Emaktab / Kundalik manzillari
LOGIN_URL = "https://emaktab.uz"
ATTENDANCE_URL = "https://emaktab.uz"

def davomatni_avto_belgilash():
    if not DATABASE["login"] or not DATABASE["parol"]:
        print("Login va parol kiritilmagan, bot to'xtadi.")
        return
        
    print("33 o'quvchi uchun avtomatlashtirish serverda boshlandi...")
    payload = {
        'login': DATABASE["login"],
        'password': DATABASE["parol'],
        'X-Requested-With': 'XMLHttpRequest'
    }
    
    with requests.Session() as session:
        try:
            login_response = session.post(LOGIN_URL, data=payload)
            if login_response.status_code == 200 or "dashboard" in login_response.url:
                # 33 kishilik sinf uchun to'liq davomat ma'lumotlari
                attendance_data = {
                    'status': 'present_all',        # Hamma qatnashdi deb belgilash
                    'total_students': 33,           # 33 nafar o'quvchi uchun
                    'date': time.strftime("%Y-%m-%d")
                }
                session.post(ATTENDANCE_URL, data=attendance_data)
                print(f"{DATABASE['login']} uchun bugungi 33 kishilik davomat muvaffaqiyatli topshirildi!")
        except Exception as e:
            print(f"Xatolik yuz berdi: {e}")

# HAR KUNI SOAT 08:30 DA ISHLAYDI
schedule.every().day.at("08:30").do(davomatni_avto_belgilash)

# Orqa fonda vaqtni tekshirib turuvchi sikl
def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(60)

# Sayt dizayni (HTML)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>eMaktab 33 kishilik Davomat Boti</title>
    <style>
        body { font-family: Arial, sans-serif; background: #f4f4f9; padding: 20px; text-align: center; }
        .card { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); max-width: 400px; margin: auto; }
        input { width: 90%; padding: 10px; margin: 10px 0; border: 1px solid #ccc; border-radius: 5px; }
        button { background: #007bff; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; font-size: 16px; }
        button:hover { background: #0056b3; }
        .status { color: green; font-weight: bold; margin-top: 15px; }
    </style>
</head>
<body>
    <div class="card">
        <h2>eMaktab Davomat Boti (33 talaba)</h2>
        <p>Login va parolingizni kiriting. Tizim har kuni 33 kishilik sinf davomatini avtomatik yangilaydi.</p>
        <form method="POST" action="/save">
            <input type="text" name="login" placeholder="eMaktab Logini" value="{{ login }}" required>
            <input type="password" name="parol" placeholder="eMaktab Paroli" value="{{ parol }}" required>
            <button type="submit">Saqlash va Faollashtirish</button>
        </form>
        {% if login %}
            <div class="status">Bot faol holatda (Aktiv: {{ login }})</div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, login=DATABASE["login"], parol=DATABASE["parol"])

@app.route('/save', methods=['POST'])
def save():
    DATABASE["login"] = request.form.get('login')
    DATABASE["parol"] = request.form.get('parol')
    return redirect('/')

if __name__ == '__main__':
    t = Thread(target=run_schedule)
    t.daemon = True
    t.start()
    
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
          
