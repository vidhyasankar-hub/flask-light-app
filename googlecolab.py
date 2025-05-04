# @title Refactored app4.py for Google Colab (with Drive support) { display-mode: "form" }
# Mount Google Drive
from google.colab import drive
drive.mount('/content/drive')

# Setup paths
import csv
import os
import matplotlib.pyplot as plt
import sympy as sp
from datetime import datetime

drive_path = '/content/drive/MyDrive/LightIntensityProject'
os.makedirs(drive_path, exist_ok=True)

data_file = os.path.join(drive_path, 'data.csv')

# Initialize CSV file
if not os.path.exists(data_file):
    with open(data_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['timestamp', 'brightness'])

print(f"Data will be stored in: {data_file}")

# Function to log a brightness frame
def log_frame(timestamp, brightness):
    with open(data_file, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, brightness])
    print(f"Logged: {timestamp}, {brightness}")

# Function to generate output graph and symbolic solution
def generate_output():
    times, brightnesses = [], []

    with open(data_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            times.append(datetime.fromisoformat(row['timestamp']))
            brightnesses.append(float(row['brightness']))

    if times and brightnesses:
        # Plot graph
        plt.figure(figsize=(10, 5))
        plt.plot(times, brightnesses, label='Brightness', color='teal')
        plt.xlabel('Time')
        plt.ylabel('Brightness')
        plt.title('Intensity vs Time')
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()

        graph_path = os.path.join(drive_path, 'intensity_plot.png')
        plt.savefig(graph_path)
        plt.close()
        print(f"Graph saved to: {graph_path}")

    # Symbolic differential equation
    t, y, k = sp.symbols('t y k')
    eq = sp.Eq(sp.Derivative(y, t), -k * y)
    sol = sp.dsolve(eq, y)

    with open(os.path.join(drive_path, 'equation.txt'), 'w') as f:
        f.write(f"Differential Equation:\n{str(eq)}\n")

    with open(os.path.join(drive_path, 'solution.txt'), 'w') as f:
        f.write(f"Symbolic Solution:\n{str(sol)}\n")

    print("Equation and solution saved in Google Drive.")

# Example usage: log one data point (you can modify or call this from HTML/js via Colab forms or APIs)
# log_frame(datetime.now().isoformat(), 130.7)

# To manually run after data collection:
# generate_output()
