import os
from flask import Flask, request, jsonify, render_template_string
from sympy import symbols, Function, Eq, dsolve
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from datetime import datetime
import pandas as pd

app = Flask(__name__)
brightness_data = []

@app.route('/')
def index():
    return render_template_string(open("templates/index.html").read())

@app.route('/upload_frame', methods=['POST'])
def upload_frame():
    data = request.get_json()
    brightness = data.get('brightness')
    timestamp = data.get('timestamp')
    
    if brightness is not None and timestamp is not None:
        print(f"Brightness: {brightness}, Timestamp: {timestamp}")
        brightness_data.append((timestamp, brightness))
    
    return jsonify(status='success')

@app.route('/graph')
def graph():
    if not brightness_data:
        return "No brightness data available yet. Please wait..."

    # Prepare data
    df = pd.DataFrame(brightness_data, columns=['timestamp', 'brightness'])
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.sort_values('timestamp', inplace=True)

    # Plot
    plt.figure(figsize=(10, 4))
    plt.plot(df['timestamp'], df['brightness'], marker='o')
    plt.title('Light Intensity vs Time')
    plt.xlabel('Time')
    plt.ylabel('Brightness')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save to buffer
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    encoded = base64.b64encode(buf.read()).decode('utf-8')
    img_data = f"data:image/png;base64,{encoded}"

    # Solve differential equation
    t = symbols('t')
    y = Function('y')
    k = 0.1  # Example constant
    eqn = Eq(y(t).diff(t), -k * y(t))
    sol = dsolve(eqn, y(t))

    return f'''
    <h2>Light Intensity vs Time</h2>
    <img src="{img_data}" alt="Intensity Graph"/>
    <h2>Differential Equation</h2>
    <p>{str(eqn)}</p>
    <h2>Solution</h2>
    <p>{str(sol)}</p>
    '''

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
