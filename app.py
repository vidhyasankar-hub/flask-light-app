from flask import Flask, render_template, request, jsonify
import base64
import cv2
import numpy as np
import re

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    image_data = data['image']

    # Remove the data URL prefix
    img_str = re.sub('^data:image/.+;base64,', '', image_data)
    img_bytes = base64.b64decode(img_str)

    # Convert bytes to numpy array
    np_arr = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    # Convert to grayscale to compute light intensity
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    intensity = int(np.mean(gray))  # Average brightness

    return jsonify({'intensity': intensity})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
