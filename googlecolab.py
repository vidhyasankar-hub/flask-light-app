
# @title Upload index5.html and Serve It with Camera Access {display-mode: "form"}

# Step 1: Upload the file
from google.colab import files
uploaded = files.upload()

# Step 2: Start a simple HTTP server to serve index5.html
import os
import threading
import socketserver
from http.server import SimpleHTTPRequestHandler

# Serve from current working directory
os.chdir('/content')

# Function to start HTTP server in a thread
def start_server(port=8000):
    handler = SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", port), handler)
    thread = threading.Thread(target=httpd.serve_forever)
    thread.daemon = True
    thread.start()
    print(f"Server started at http://localhost:{port}")

start_server(8000)

# Step 3: Show public link (for camera access, open in a new browser tab)
from IPython.display import display, HTML
public_link = "http://localhost:8000/index5.html"
display(HTML(f'<a href="{public_link}" target="_blank" style="font-size:18px;color:blue;">Click here to open index5.html (camera access)</a>'))
