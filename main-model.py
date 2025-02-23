import cv2  
import urllib.request  
import numpy as np  
import requests  
import pyttsx3  
import time  

# Step 1: Capture Image from DroidCam
URL = "http://ip of droid cam:port/mjpegfeed"  # Change to your DroidCam stream URL
image_path = "captured_image.jpg"

stream = urllib.request.urlopen(URL)
bytes_data = bytes()

while True:
    bytes_data += stream.read(1024)
    a = bytes_data.find(b'\xff\xd8')
    b = bytes_data.find(b'\xff\xd9')
    
    if a != -1 and b != -1:
        jpg = bytes_data[a:b+2]
        bytes_data = bytes_data[b+2:]

        img = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
        cv2.imshow('DroidCam Feed (Press "C" to Capture)', img)

        # Press 'c' to capture and save the image
        if cv2.waitKey(1) & 0xFF == ord('c'):
            cv2.imwrite(image_path, img)
            cv2.waitKey(100)  # Small delay to ensure image is saved
            print(f"✅ Image saved as '{image_path}'")
            break  

cv2.destroyAllWindows()

# Step 2: Upload Image to Hugging Face API for Captioning
API_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-base"
HEADERS = {"Authorization": "Bearer your hugging face api key"}  # Replace with your actual API key

def get_caption(image_path):
    """Uploads the image to Hugging Face API and retrieves a caption."""
    try:
        # Open the image in binary mode
        with open(image_path, "rb") as image_file:
            image_bytes = image_file.read()  # Read file as bytes
            response = requests.post(API_URL, headers=HEADERS, data=image_bytes)

        response_json = response.json()
        print("🔍 API Response:", response_json)  # Debugging output

        # Handle API errors
        if "error" in response_json:
            print("❌ API Error:", response_json["error"])
            if "loading" in response_json["error"]:  
                print("⏳ Model is still loading. Retrying in 10 seconds...")
                time.sleep(10)
                return get_caption(image_path)  # Retry the request
            return None

        # Extract caption safely
        if isinstance(response_json, list) and "generated_text" in response_json[0]:
            return response_json[0]["generated_text"]
        
        return response_json.get("generated_text", "No caption generated")
    
    except Exception as e:
        print(f"❌ Error while processing image: {str(e)}")
        return None


# Get the caption
caption = get_caption(image_path)

if caption:
    print(f"📝 Caption: {caption}")

    # Step 3: Convert Caption to Speech
    engine = pyttsx3.init()
    engine.say(caption)
    engine.runAndWait()
else:
    print("⚠️ Could not generate a caption. Please check the API response.")
