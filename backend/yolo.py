import os
from inference_sdk import InferenceHTTPClient
from tempfile import NamedTemporaryFile
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

# Initialize the Roboflow client
client = InferenceHTTPClient(
    api_url=os.getenv('ROBOFLOW_MODEL_ENDPOINT'),
    api_key=os.getenv('ROBOFLOW_API_KEY')
)

def detect_dental_damage(image_bytes):
    temp_file_path = None

    # Simpan gambar ke file sementara
    try:
        with NamedTemporaryFile(delete=False, suffix=".jpg") as temp:
            temp.write(image_bytes)
            temp_file_path = temp.name

        # Jalankan workflow Roboflow
        result = client.run_workflow(
            workspace_name=os.getenv('ROBOFLOW_WORKSPACE_NAME'),
            workflow_id=os.getenv('ROBOFLOW_WORKFLOW_ID'),
            images={"image": temp_file_path},
            use_cache=True
        )

        # print("Raw result from Roboflow:", result)

        # Validasi dan ekstrak prediksi
        if isinstance(result, list) and len(result) > 0 and isinstance(result[0], dict):
            predictions = result[0].get("predictions", {}).get("predictions", [])
            if predictions:
                class_list = [
                    {"class": pred.get("class"), "confidence": pred.get("confidence")}
                    for pred in predictions if "class" in pred
                ]
                return {
                    "success": True,
                    "data": class_list
                }
            
     
        # Jika tidak ada prediksi
        return {
            "success": True,
            "data": []
        }
    except requests.exceptions.HTTPError as e:
        print("HTTPError:", e)
        return {
            "success": False,
            "error": "HTTPError",
            "details": e.response.text if hasattr(e, "response") else str(e)
        }

    except Exception as e:
        print("Exception:", str(e))
        return {
            "success": False,
            "error": "Exception",
            "details": str(e)
        }

    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            os.remove(temp_file_path)
