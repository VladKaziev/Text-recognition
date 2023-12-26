import requests
import json
import base64
from PIL import Image
from io import BytesIO

IAM_TOKEN = "t1.9euelZqNi4mWlcqbjpuKxs6QjImJm-3rnpWays_Ll5aYmsyKzZOWzciWmcnl8_chZVRT-e9QGx00_d3z92ETUlP571AbHTT9zef1656Vmpuej4yNk5OdiciNx47My46Z7_zF656Vmpuej4yNk5OdiciNx47My46Z.-G8IJ4RZ4070NOebkqXrhDxdt873H8fMeu76Z6dQ9x1b8RaRK3tnvLiu2H7BDuoZVCMsdjOUppZKGRnNjwCyCw"
FOLDER_ID = "b1grc30v0gvo3smdu8q9"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {IAM_TOKEN}",
    "x-folder-id": FOLDER_ID,
    "x-data-logging-enabled": "true"
}

with Image.open("1234.jpg") as img:
    img = img.resize((512, 512))

    img_byte_arr = BytesIO()
    img.save(img_byte_arr, format='JPEG')
    img_byte_arr = img_byte_arr.getvalue()

    encoded_string = base64.b64encode(img_byte_arr).decode()

body = {
  "mimeType": "JPEG",
  "languageCodes": ["ru"],
  "model": "page",
  "content": encoded_string
}

response = requests.post("https://ocr.api.cloud.yandex.net/ocr/v1/recognizeText", headers=headers, json=body)

with open('output_response.json', 'w') as file:
    json.dump(response.json(), file)
