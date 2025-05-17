import requests
import os
from dotenv import load_dotenv

load_dotenv()

def get_recommendation_from_llm(detection_results):
    try:
        if isinstance(detection_results, list) and detection_results:
            detected_items = [
                f"Class: {item.get('class')}, Confidence: {item.get('confidence')}"
                for item in detection_results
            ]
            result_text = "\n".join(detected_items)
        else:
            result_text = "No dental damage detected."

        response = requests.post(
            os.getenv("AZURE_OPENAI_ENDPOINT"),
            headers={
                "Authorization": f"Bearer {os.getenv('AZURE_OPENAI_API_KEY')}",
                "Content-Type": "application/json"
            },
            json={
                "model": os.getenv('AZURE_OPENAI_DEPLOYMENT'),
                "messages": [
                    {"role": "system", "content": "You are a dental assistant."},
                    {"role": "user", "content": f"Based on the following dental damage predictions, provide recommendations:\n{result_text}"}
                ],
                "max_tokens": 150
            }
        )

        llm_data = response.json()
        return llm_data.get("choices", [])[0].get("message", {}).get("content", "No recommendation provided.")

    except Exception as e:
        return f"Error while getting recommendation: {str(e)}"
