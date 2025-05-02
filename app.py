from flask import Flask, request, render_template, send_file
import matplotlib.pyplot as plt
import pandas as pd
import io
import os
from scipy.integrate import odeint
import numpy as np

app = Flask(__name__)

data_points = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload_data', methods=['POST'])
def upload_data():
    content = request.get_json()
    brightness = content.get('brightness')
    timestamp = content.get('timestamp')
    if brightness is not None and timestamp is not None:
        data_points.append((timestamp, brightness))
    return {'status': 'ok'}

@app.route('/graph')
def show_graph():
    if not data_points:
        return "No data available yet"

    df = pd.DataFrame(data_points, columns=['timestamp', 'brightness'])
    df['time'] = (df['timestamp'] - df['timestamp'].iloc[0]) / 1000  # convert to seconds

    # Solve a simple differential equation: dy/dt = -k*y
    def model(y, t, k):
        return -k * y

    y0 = df['brightness'].iloc[0]
    t_vals = df['time'].values
    k = 0.1  # decay constant (example)
    y_vals = odeint(model, y0, t_vals, args=(k,))

    # Plot
    plt.figure()
    plt.plot(df['time'], df['brightness'], label='Measured Intensity')
    plt.plot(t_vals, y_vals, label='Model: dy/dt = -k*y')
    plt.xlabel('Time (s)')
    plt.ylabel('Brightness')
    plt.legend()
    plt.title('Light Intensity vs Time')
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    return send_file(buf, mimetype='image/png')
