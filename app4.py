from flask import Flask, request, send_file, jsonify, render_template
import csv
import os
import matplotlib.pyplot as plt
import sympy as sp
from datetime import datetime

app = Flask(__name__)
data_file = 'data.csv'

# Ensure data.csv is initialized
if not os.path.exists(data_file):
    with open(data_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['timestamp', 'brightness'])

@app.route('/')
def index():
    return render_template('index4.html')  # Updated to use index4.html

@app.route('/upload_frame', methods=['POST'])
def upload_frame():
    data = request.get_json()
    timestamp = data['timestamp']
    brightness = data['brightness']
    with open(data_file, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, brightness])
    return jsonify(status="frame logged")

@app.route('/generate_output', methods=['POST', 'GET'])
def generate_output():
    times, brightnesses = [], []
    with open(data_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            times.append(datetime.fromisoformat(row['timestamp']))
            brightnesses.append(float(row['brightness']))

    # Plot and save graph
    if times and brightnesses:
        plt.figure(figsize=(10, 5))
        plt.plot(times, brightnesses, label='Brightness', color='teal')
        plt.xlabel('Time')
        plt.ylabel('Brightness')
        plt.title('Intensity vs Time')
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('intensity_plot.png')
        plt.close()

    # Save symbolic differential equation and solution
    t, y, k = sp.symbols('t y k')
    eq = sp.Eq(sp.Derivative(y, t), -k * y)
    sol = sp.dsolve(eq, y)

    with open('equation.txt', 'w') as f:
        f.write(f"Differential Equation:\n{str(eq)}\n")

    with open('solution.txt', 'w') as f:
        f.write(f"Symbolic Solution:\n{str(sol)}\n")

    return jsonify(status="Output generated", files=[
        'data.csv', 'intensity_plot.png', 'equation.txt', 'solution.txt'
    ])

@app.route('/cleanup', methods=['POST'])
def cleanup():
    for filename in ['data.csv', 'intensity_plot.png', 'equation.txt', 'solution.txt']:
        try:
            os.remove(filename)
        except FileNotFoundError:
            pass
    return jsonify(status="cleaned up")

@app.route('/download/<filename>')
def download_file(filename):
    path = os.path.join('.', filename)
    if os.path.exists(path):
        return send_file(path, as_attachment=True)
    else:
        return f"Error: File '{filename}' not found", 404

if __name__ == '__main__':
    app.run(debug=True)
