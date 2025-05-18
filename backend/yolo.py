import os
from inference_sdk import InferenceHTTPClient
from tempfile import NamedTemporaryFile
from dotenv import load_dotenv
import requests
from PIL import Image
import io
import base64

# Load environment variables
load_dotenv()

# Initialize the Roboflow client
client = InferenceHTTPClient(
    api_url=os.getenv('ROBOFLOW_MODEL_ENDPOINT'),
    api_key=os.getenv('ROBOFLOW_API_KEY')
)

def detect_dental_damage(image_bytes):
    temp_file_path = None

    # Save the image to a temporary file
    try:
        with NamedTemporaryFile(delete=False, suffix=".jpg") as temp:
            temp.write(image_bytes)
            temp_file_path = temp.name

        # Run the Roboflow workflow
        result = client.run_workflow(
            workspace_name=os.getenv('ROBOFLOW_WORKSPACE_NAME'),
            workflow_id=os.getenv('ROBOFLOW_WORKFLOW_ID'),
            images={"image": temp_file_path},
            use_cache=True
        )

        # Validate and extract predictions
        if isinstance(result, list) and len(result) > 0 and isinstance(result[0], dict):
            predictions = result[0].get("predictions", {}).get("predictions", [])
            label_visualization = result[0].get("label_visualization", None)
        
            if predictions:
                # Extract 'class' and 'confidence' from predictions
                class_list = [
                    {"class": pred.get("class"), "confidence": pred.get("confidence")}
                    for pred in predictions if "class" in pred
                ]
                
                # You can now return both the class data and the label visualization
                return {
                    "success": True,
                    "data": class_list,
                    "label_visualization": label_visualization
                }

        # If no predictions were found
        return {
            "success": True,
            "data": [],
            "label_visualization": None
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


