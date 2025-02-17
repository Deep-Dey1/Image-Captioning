import requests

API_URL = "https://huggingface.co/api/whoami"
HEADERS = {"Authorization": "Bearer your-api-key"}  # Added 'Bearer '

response = requests.get(API_URL, headers=HEADERS)
print(response.json())  # Should return your Hugging Face username if the key is correct
