// static/js/camera.js

const canvas = document.createElement('canvas');
const ctx = canvas.getContext('2d');
let captureInterval;
let countdownOverlay;
let videoElem;

window.addEventListener('DOMContentLoaded', () => {
  videoElem = document.getElementById("webcam");
  const spinner = document.getElementById("loading-spinner");
  const startBtn = document.getElementById("start-transcribe");
  const stopBtn = document.getElementById("stop-transcribe");
  const resetBtn = document.getElementById("reset-transcribe");

  let streamStarted = false;

  startBtn.addEventListener("click", () => {
    if (!streamStarted) {
      startWebcam().then(() => {
        streamStarted = true;
        startCapture();
      });
    } else {
      startCapture();
    }
  });

  stopBtn.addEventListener("click", () => {
    clearInterval(captureInterval);
  });

  resetBtn.addEventListener("click", () => {
    clearInterval(captureInterval);
    const output = document.getElementById("transcription-output");
    output.innerText = "";
    startCapture();
  });

  function startWebcam() {
    return navigator.mediaDevices.getUserMedia({ video: true })
      .then(stream => {
        videoElem.srcObject = stream;
        return videoElem.play();
      })
      .catch(err => console.error("Webcam error:", err));
  }

  function startCapture() {
    const webcamContainer = document.getElementById("webcam-container");

    if (!countdownOverlay) {
      countdownOverlay = document.createElement('div');
      countdownOverlay.id = 'countdown-overlay';
      countdownOverlay.style.position = 'absolute';
      countdownOverlay.style.top = '50%';
      countdownOverlay.style.left = '50%';
      countdownOverlay.style.transform = 'translate(-50%, -50%)';
      countdownOverlay.style.fontSize = '5rem';
      countdownOverlay.style.fontWeight = 'bold';
      countdownOverlay.style.color = '#fff';
      countdownOverlay.style.background = 'rgba(0,0,0,0.7)';
      countdownOverlay.style.padding = '30px';
      countdownOverlay.style.borderRadius = '12px';
      countdownOverlay.style.zIndex = '1000';
      countdownOverlay.style.textAlign = 'center';
      countdownOverlay.style.width = '120px';
      countdownOverlay.style.display = 'none';
      webcamContainer.style.position = 'relative';
      webcamContainer.appendChild(countdownOverlay);
    }

    countdownOverlay.style.display = 'block';
    let countdown = 5;
    countdownOverlay.textContent = countdown;

    const countdownTimer = setInterval(() => {
      countdown--;
      if (countdown > 0) {
        countdownOverlay.textContent = countdown;
      } else {
        clearInterval(countdownTimer);
        countdownOverlay.style.display = 'none';
        captureInterval = setInterval(captureAndSend, 1000);
        captureAndSend();
      }
    }, 1000);
  }

  function captureAndSend() {
    if (!videoElem || videoElem.readyState < 2) return;
    spinner.classList.remove("hidden");

    canvas.width = videoElem.videoWidth;
    canvas.height = videoElem.videoHeight;
    ctx.drawImage(videoElem, 0, 0, canvas.width, canvas.height);

    canvas.toBlob(blob => {
      const formData = new FormData();
      formData.append('image', blob, 'capture.jpg');

      fetch('/predict', {
        method: 'POST',
        body: formData
      })
        .then(res => res.json())
        .then(data => {
          if (data.label) {
            appendTranscription(data.label);
          }
        })
        .catch(err => console.error('Prediction error:', err))
        .finally(() => {
          spinner.classList.add("hidden");
        });
    }, 'image/jpeg');
  }

  function appendTranscription(text) {
    const output = document.getElementById('transcription-output');
    if (output.innerText.includes("Teks hasil deteksi")) {
      output.innerText = '';
    }
    output.textContent += ' ' + text;
    output.scrollTop = output.scrollHeight;
  }
  
});
