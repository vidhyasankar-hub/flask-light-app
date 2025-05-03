from flask import Flask, request, jsonify, render_template
import matplotlib.pyplot as plt
import io
import base64
import numpy as np
from datetime import datetime
from sympy import symbols, Eq, dsolve, Function
import os

app = Flask(__name__)
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
        brightness_data.append((timestamp, brightness))

    return jsonify(status='success')

@app.route('/result')
def result():
    if not brightness_data:
        return "No data available yet."

    times = [datetime.fromisoformat(t[0]) for t in brightness_data]
    brightness_values = [float(b[1]) for b in brightness_data]
    
    # Normalize time
    t_seconds = [(t - times[0]).total_seconds() for t in times]

    # Plot intensity vs time
    plt.figure()
    plt.plot(t_seconds, brightness_values, marker='o')
    plt.title('Intensity vs Time')
    plt.xlabel('Time (s)')
    plt.ylabel('Brightness')
    plt.grid(True)

    # Save plot to buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image_base64 = base64.b64encode(buf.getvalue()).decode()
    buf.close()

    # Solve differential equation symbolically
    t = symbols('t')
    I = Function('I')
    eq = Eq(I(t).diff(t), -0.1 * I(t))  # Example DE: dI/dt = -0.1*I
    sol = dsolve(eq, I(t)).simplify()

    return f'''
        <h2>Intensity vs Time Graph</h2>
        <img src="data:image/png;base64,{image_base64}">
        <h2>Differential Equation and Solution</h2>
        <p>Equation: dI/dt = -0.1 * I</p>
        <p>Solution: {sol}</p>
        <br><a href="/">Back to live stream</a>
    '''

# Deployment settings
port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)
