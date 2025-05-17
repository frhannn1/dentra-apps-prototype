import os
import requests
from inference_sdk import InferenceHTTPClient
from tempfile import NamedTemporaryFile
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize the Roboflow client
client = InferenceHTTPClient(
    api_url=os.getenv('ROBOFLOW_MODEL_ENDPOINT'),
    api_key=os.getenv('ROBOFLOW_API_KEY')
)

def detect_dental_damage(image_bytes):
    # Save the image temporarily
    with NamedTemporaryFile(delete=False, suffix=".jpg") as temp:
        temp.write(image_bytes)
        temp_file_path = temp.name

    try:
        # Run the YOLO object detection workflow in Roboflow
        result = client.run_workflow(
            workspace_name=os.getenv('ROBOFLOW_WORKSPACE_NAME'),
            workflow_id=os.getenv('ROBOFLOW_WORKFLOW_ID'),
            images={"image": temp_file_path},
            use_cache=True  # Optional, you can remove this if needed
        )

        # Since the result is already a Python dictionary, no need for .json()
        # Return the 'predictions' from the result
        if 'predictions' in result:
            return result['predictions']
        else:
            return []

    except requests.exceptions.HTTPError as e:
        # Handle HTTP error if any
        print("HTTPError:", e)
        return {"error": "HTTPError", "details": str(e)}

    except Exception as e:
        # Catch other exceptions
        print("Error:", str(e))
        return {"error": "Exception", "details": str(e)}

    finally:
        # Make sure to delete the temporary file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
