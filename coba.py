from inference_sdk import InferenceHTTPClient

client = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key="dhGvUarq0W6I7AbmVkmA"
)

result = client.run_workflow(
    workspace_name="dental-ne7pt",
    workflow_id="custom-workflow-2",
    images={
        "image": "foto kasus gigi.jpg"
    },
    use_cache=True # cache workflow definition for 15 minutes
)
