import requests
import json

API_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-base"
HEADERS = {"Authorization": "your-api-key"}

def query_image(image_path):
    with open(image_path, "rb") as img:
        response = requests.post(API_URL, headers=HEADERS, data=img)
    return response.json()

# Run the function
result = query_image("sample-image.jpg")

# Extract and print the caption
if isinstance(result, list) and "generated_text" in result[0]:
    print("Caption:", result[0]["generated_text"])
else:
    print("Error:", result)
