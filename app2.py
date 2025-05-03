from flask import Flask, render_template, request, jsonify
import sympy as sp
from datetime import datetime
import os

app = Flask(__name__)

# Store data (in memory for now)
brightness_data = []

# Symbolic variables
t = sp.symbols('t')
y = sp.Function('y')
k = sp.Symbol('k')

# Differential equation and solution
diff_eq = sp.Eq(y(t).diff(t), -k * y(t))
solution = sp.dsolve(diff_eq, y(t))

@app.route('/')
def index():
    return render_template('index.html', differential_eq=str(diff_eq), solution=str(solution.rhs))

@app.route('/upload_frame', methods=['POST'])
def upload_frame():
    data = request.get_json()
    if data and 'brightness' in data:
        timestamp = data.get('timestamp', datetime.utcnow().isoformat())
        brightness = float(data['brightness'])
        brightness_data.append({'timestamp': timestamp, 'brightness': brightness})
        return jsonify(status="success")
    return jsonify(status="error", message="Invalid data")

if __name__ == '__main__':
    app.run(debug=True)
