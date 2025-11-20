from flask import Flask, render_template, request
from datetime import datetime
from groq import Groq

app = Flask(__name__)

client = Groq()

def ai_call(year):
    try:
        chat_completion = client.chat.completions.create(
            messages= [
                {
                    "role": "user",
                    "content": f"berikan satu kejadian menarik yang ada pada tahun {year}"
                }
            ],
            model="groq/compound-mini",
            stream=False
        )

        ai_output = chat_completion.choices[0].message.content
        return ai_output

    except Exception:
        return "Maaf, terjadi kesalahan saat memproses permintaan Anda."

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/usia', methods=['GET', 'POST'])
def cek_usia():
    if request.method == 'POST':
        # Ambil data dari form
        tahun_lahir = int(request.form['tahun_lahir'])
        tahun_sekarang = datetime.now().year
        usia = tahun_sekarang - tahun_lahir

        ai_output = ai_call(tahun_lahir)

        print(ai_output)

        return render_template('cek_usia.html', usia=usia, tahun_lahir=tahun_lahir, ai_output=ai_output)
    return render_template('cek_usia.html', usia= None)
    
if __name__ == "__main__":
    app.run(host='0.0.0.0')
