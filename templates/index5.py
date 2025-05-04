<!DOCTYPE html>
<html>
<head>
  <title>Intensity Logger</title>
</head>
<body>
  <h2>Camera Brightness Logger</h2>
  <video id="video" width="320" height="240" autoplay playsinline></video>
  <canvas id="canvas" width="320" height="240" style="display: none;"></canvas>
  <button onclick="startLogging()">Start Logging</button>
  <button onclick="stopLogging()">Stop Logging</button>

  <script>
    let video = document.getElementById('video');
    let canvas = document.getElementById('canvas');
    let context = canvas.getContext('2d');
    let logging = false;
    let stream;
    let logInterval;

    async function startCamera() {
      try {
        if (stream) {
          stream.getTracks().forEach(t => t.stop());
        }
        stream = await navigator.mediaDevices.getUserMedia({
          video: { facingMode: 'environment' }
        });
        video.srcObject = stream;
      } catch (err) {
        alert("Camera access failed: " + err.message);
        console.error("Camera error:", err);
      }
    }

    function calculateBrightness(imageData) {
      let data = imageData.data;
      let r, g, b, avg;
      let colorSum = 0;

      for (let x = 0, len = data.length; x < len; x += 4) {
        r = data[x];
        g = data[x + 1];
        b = data[x + 2];
        avg = Math.floor((r + g + b) / 3);
        colorSum += avg;
      }

      return Math.floor(colorSum / (data.length / 4));
    }

    function logBrightness() {
      if (!logging) return;

      context.drawImage(video, 0, 0, canvas.width, canvas.height);
      let imageData = context.getImageData(0, 0, canvas.width, canvas.height);
      let brightness = calculateBrightness(imageData);
      let timestamp = new Date().toISOString();

      // Send to Python in Colab
      google.colab.kernel.invokeFunction(
        'logFrameColab', [timestamp, brightness], {}
      ).then(() => console.log("Logged:", timestamp, brightness));
    }

    function startLogging() {
      if (!logging) {
        logging = true;
        logInterval = setInterval(logBrightness, 1000);  // log every second
        console.log("Started logging...");
      }
    }

    function stopLogging() {
      logging = false;
      clearInterval(logInterval);
      console.log("Stopped logging.");
    }

    startCamera();
  </script>
</body>
</html>
