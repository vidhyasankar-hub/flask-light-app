from flask import Flask, render_template, request, jsonify
import numpy as np
import matplotlib.pyplot as plt
from sympy import symbols, Function, Eq, dsolve, exp, simplify
from datetime import datetime
import os
import io
import base64

app = Flask(__name__)

# Store brightness and time data
brightness_data = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload_frame', methods=['POST'])
def upload_frame():
    data = request.get_json()
    brightness = data.get('brightness')
    timestamp = data.get('timestamp')

    if brightness is not None and timestamp is not None:
        print(f"Brightness: {brightness}, Timestamp: {timestamp}")
        try:
            t = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
            brightness_data.append((t, brightness))
        except Exception as e:
            print("Timestamp parse error:", e)

    return jsonify(status='success')

@app.route('/results')
def results():
