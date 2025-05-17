import requests
import os
from dotenv import load_dotenv

load_dotenv()

def get_recommendation_from_llm(detection_results):
    # Ambil hanya kelas dari detection_results yang ada di dalam data
    if 'data' in detection_results:
        classes = [item.get('class') for item in detection_results['data']]
    else:
        classes = []
    
    # Cetak hasil kelas
    print(classes)  # Ini hanya berisi 'caries' atau daftar kelas lainnya
    
    try:
        if classes:
            detected_items = [f"Class: {item}" for item in classes]
            result_text = "\n".join(detected_items)
        else:
            result_text = "No dental damage detected."

        response = requests.post(
            os.getenv("AZURE_OPENAI_ENDPOINT"),
            headers={
                "api-key": os.getenv('AZURE_OPENAI_API_KEY'),
                "Content-Type": "application/json"
            },
            json={
                "messages": [
                    {"role": "system", "content": "You are a dental assistant."},
                    {"role": "user", "content": f"Based on the following dental damage predictions, provide recommendations:\n{result_text}"}
                ],
                "max_tokens": 150,
                "temperature": 0.7,
                "top_p": 1,
                "frequency_penalty": 0,
                "presence_penalty": 0
            }
        )

        # Coba parsing JSON dengan aman
        try:
            llm_data = response.json()
        except Exception as e:
            return f"Failed to parse response as JSON: {response.text}"

        # Cek apakah data dalam bentuk dictionary
        if not isinstance(llm_data, dict):
            return f"Unexpected response format (not dict): {llm_data}"

        choices = llm_data.get("choices", [])
        if choices and isinstance(choices[0], dict):
            return choices[0].get("message", {}).get("content", "No recommendation provided.")
        else:
            return f"Unexpected response structure: {choices}"

    except Exception as e:
        return f"Error while getting recommendation: {str(e)}"


