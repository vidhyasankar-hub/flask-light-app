from flask import Flask, render_template, request
import cv2
import numpy as np
import base64

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload_frame', methods=['POST'])
def upload_frame():
    try:
        data = request.get_json()
        image_data = data['image'].split(',')[1]
        image_bytes = base64.b64decode(image_data)
        np_arr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        # Example OpenCV processing (grayscale conversion)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        print("Received and processed a frame.")
        return '', 204  # No content response
    except Exception as e:
        print("Error processing frame:", str(e))
        return 'Error', 500

if __name__ == '__main__':
    app.run(debug=True)
