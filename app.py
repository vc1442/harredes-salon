from flask import Flask, render_template, request, redirect
from supabase import create_client

app = Flask(__name__)

# Supabase config
url = "https://sabggeijqmhusqifpumz.supabase.co"
key = "sb_publishable_Ded7baC1M711I_vJnPmuZA_j1EXAzxc"
supabase = create_client(url, key)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/booking', methods=['GET', 'POST'])
def booking():
    if request.method == 'POST':
        data = {
            "name": request.form['name'],
            "phone": request.form['phone'],
            "service": request.form['service'],
            "date": request.form['date'],
            "time": request.form['time']
        }
        supabase.table("bookings").insert(data).execute()
        return f'''
        <div style="text-align:center; padding:50px; font-family:Arial; background:#fff9fb;">
            <h2 style="color:#d46a8c;">✅ Booking Confirmed!</h2>
            <p>Thank you, <strong>{data["name"]}</strong>!<br>We'll call you at <strong>{data["phone"]}</strong>.</p>
            <a href="/" style="display:inline-block; margin-top:20px; padding:10px 20px; 
               background:#d46a8c; color:white; text-decoration:none; border-radius:5px;">
                ← Back to Home
            </a>
        </div>
        '''
    return render_template('booking.html')

@app.route('/admin')
def admin():
    response = supabase.table("bookings").select("*").order("date", desc=False).execute()
    bookings = [(r['name'], r['phone'], r['service'], r['date'], r['time']) for r in response.data]
    return render_template('admin.html', bookings=bookings)

if __name__ == '__main__':
    app.run(debug=False)