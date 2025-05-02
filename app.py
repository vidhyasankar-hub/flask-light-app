from flask import Flask, render_template, request, jsonify, send_file
import numpy as np
import matplotlib.pyplot as plt
import io
import base64
from scipy.integrate import odeint

app = Flask(__name__)

brightness_data = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload_data', methods=['POST'])
def upload_data():
    data = request.get_json()
    brightness = data.get('brightness')
    timestamp = data.get('timestamp')
    
    if brightness is not None and timestamp is not None:
        print(f"Brightness: {brightness}, Timestamp: {timestamp}")
        brightness_data.append((timestamp, brightness))
    
    return jsonify(status='success')

@app.route('/graph')
def show_graph():
    if not brightness_data:
        return 'No brightness data to plot.', 400

    # Sort data by timestamp
    sorted_data = sorted(brightness_data, key=lambda x: x[0])
    timestamps, intensities = zip(*sorted_data)
    
    # Normalize timestamps
    t0 = timestamps[0]
    times = [(t - t0) for t in timestamps]

    # Solve differential equation (example: exponential decay model)
    def model(I, t, k):
        return -k * I

    k = 0.1  # decay constant (you can tune this)
    I0 = intensities[0]
    solution = odeint(model, I0, times, args=(k,))
    solution = [s[0] for s in solution]

    # Plotting
    fig, ax = plt.subplots()
    ax.plot(times, intensities, 'bo-', label='Measured Intensity')
    ax.plot(times, solution, 'r--', label='ODE Fit: dI/dt = -kI')
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Intensity')
    ax.set_title('Intensity vs Time')
    ax.legend()
    plt.tight_layout()

    # Save to BytesIO and encode to base64 for display
    img_io = io.BytesIO()
    plt.savefig(img_io, format='png')
    img_io.seek(0)
    encoded_img = base64.b64encode(img_io.read()).decode('utf-8')
    plt.close(fig)

    html = f"""
    <h2>Intensity vs Time</h2>
    <img src="data:image/png;base64,{encoded_img}" alt="Graph">
    <p>Differential Equation: dI/dt = -kI, with k = {k}</p>
    """

    return html

if __name__ == '__main__':
    app.run(debug=True)
