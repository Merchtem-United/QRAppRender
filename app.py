from flask import Flask, render_template, request, jsonify
import qrcode
import io
import base64
import os

app = Flask(__name__)

# Route voor de homepagina
@app.route('/')
def home():
    return render_template('index.html')

# Route om QR-code te genereren
@app.route('/generate_qr', methods=['POST'])
def generate_qr():
    data = request.json.get("amount", "")
    if not data:
        return jsonify({"error": "Invalid data"}), 400
    
    # Genereer de QR-code afbeelding
    img = qrcode.make(f"Betaling voor: {data} euro")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    img_str = base64.b64encode(buf.getvalue()).decode("utf-8")
    
    return jsonify({"qr_code": img_str})

# Start de server en maak deze beschikbaar op de door Heroku toegewezen poort
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)