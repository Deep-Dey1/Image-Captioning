import requests

API_URL = "https://huggingface.co/api/whoami"
HEADERS = {"Authorization": "Bearer your-hugging-face-api-key"}

response = requests.get(API_URL, headers=HEADERS)

print(response.status_code)  # Should be 200 if successful
print(response.json())  # Should return your Hugging Face username
