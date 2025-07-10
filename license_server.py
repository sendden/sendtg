from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

licenses = {
    "AB12-CD34-EF56": "2025-07-15",
    "GH78-IJ90-KL12": "2025-07-21",
    "MN34-OP56-QR78": "2025-08-14",
}


@app.route('/')
def index():
    return "License API is running"

@app.route('/check_key', methods=['POST'])
def check_key():
    data = request.json
    if not data or 'key' not in data:
        return jsonify({"status": "error", "message": "Ключ не предоставлен"}), 400
    key = data['key']
    expiry_str = licenses.get(key)
    if not expiry_str:
        return jsonify({"status": "invalid", "message": "Ключ не найден"}), 404
    expiry_date = datetime.strptime(expiry_str, "%Y-%m-%d")
    if datetime.now() > expiry_date:
        return jsonify({"status": "expired", "message": "Срок действия ключа истёк"}), 403
    return jsonify({"status": "valid", "message": "Ключ валиден"}), 200
