import requests
import os
import time
import requests

HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACEHUB_API_TOKEN")
api_url = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2"
headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}

prompt = "A fantasy character in an artistic style."

while True:
    response = requests.post(api_url, headers=headers, json={"inputs": prompt})
    if response.status_code == 200:
        print("✅ Image generated successfully!")
        break
    elif response.status_code == 503:
        print("⏳ Model is still loading. Retrying in 30 seconds...")
        time.sleep(30)  # Wait and retry
    else:
        print(f"❌ Error: {response.status_code}, {response.text}")
        break

