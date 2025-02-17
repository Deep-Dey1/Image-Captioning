from PIL import Image
import requests
from transformers import BlipProcessor, BlipForConditionalGeneration

# Load BLIP model
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

# Load an image (URL or local file)
image_url = "sample-image.jpg"
image = Image.open(requests.get(image_url, stream=True).raw)

# Generate caption
inputs = processor(image, return_tensors="pt")
out = model.generate(**inputs)

# Print result
print(processor.decode(out[0], skip_special_tokens=True))
