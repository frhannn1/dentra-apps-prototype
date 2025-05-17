def summarize_detections(predictions):
    """
    Menerima list prediksi dari YOLO (Roboflow)
    dan mengembalikan ringkasan dalam bentuk teks
    untuk diberikan ke LLM.

    Contoh input:
    [
        {"class": "Caries", "confidence": 0.92},
        {"class": "Tartar", "confidence": 0.85}
    ]

    Output:
    "Terdeteksi 1 kerusakan gigi bertipe 'Caries' dengan confidence 92%, dan 1 'Tartar' dengan confidence 85%."
    """
    if not predictions:
        return "Tidak ada kerusakan gigi yang terdeteksi."

    summary_lines = []
    for pred in predictions:
        label = pred.get("class", "Unknown")
        confidence = round(pred.get("confidence", 0) * 100, 2)
        summary_lines.append(f"Kerusakan '{label}' dengan keyakinan {confidence}%")

    return "Terdeteksi kerusakan gigi sebagai berikut:\n- " + "\n- ".join(summary_lines)
