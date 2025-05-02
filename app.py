from flask import Flask, request, render_template
import base64
import cv2
import numpy as np
import re
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload_frame', methods=['POST'])
def upload_frame():
    data = request.get_json()
    if 'image' not in data:
        return 'No image data', 400

    image_data = data['image']
    # Strip the header: data:image/jpeg;base64,...
    image_data = re.sub('^data:image/.+;base64,', '', image_data)
    frame_bytes = base64.b64decode(image_data)
    np_arr = np.frombuffer(frame_bytes, np.uint8)
    frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    if frame is not None:
        intensity = np.mean(frame)
        print(f"Received frame. Avg intensity: {intensity:.2f}")
    else:
        print("Failed to decode frame.")

    return 'Frame received', 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
