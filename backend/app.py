import os
from flask import Flask, request, jsonify
from yolo import detect_dental_damage
from llm import get_recommendation_from_llm
from dotenv import load_dotenv
from flask_cors import CORS

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

@app.route('/detect', methods=['POST'])
def detect():
    # Memastikan file gambar ada dalam request
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    image_file = request.files['image']
    image_bytes = image_file.read()

    # Proses deteksi kerusakan gigi menggunakan YOLO
    detection_result = detect_dental_damage(image_bytes)

    # Mengambil rekomendasi dari LLM berdasarkan hasil deteksi
    recommendation = get_recommendation_from_llm(detection_result)

    # Mengembalikan hasil deteksi dan rekomendasi
    return jsonify({"detection_result": detection_result, "recommendation": recommendation})

if __name__ == "__main__":
    app.run(debug=True)
