const canvas = document.createElement('canvas');
const ctx = canvas.getContext('2d');
let captureInterval;
let videoElem;
let lastValidText = "";

window.addEventListener('DOMContentLoaded', () => {
  videoElem = document.getElementById("webcam");
  const spinner = document.getElementById("loading-spinner");
  const startBtn = document.getElementById("start-transcribe");
  const stopBtn = document.getElementById("stop-transcribe");
  const resetBtn = document.getElementById("reset-transcribe");

  let streamStarted = false;
  let countdownOverlay;

  startBtn.addEventListener("click", () => {
    if (!streamStarted) {
      startWebcam().then(() => {
        streamStarted = true;
        showCountdown(() => {
          captureInterval = setInterval(captureImageSnapshot, 3000);
        });
      });
    } else {
      showCountdown(() => {
        captureInterval = setInterval(captureImageSnapshot, 3000);
      });
    }
  });

  stopBtn.addEventListener("click", () => {
    clearInterval(captureInterval);
  });

  resetBtn.addEventListener("click", () => {
    clearInterval(captureInterval);
    document.getElementById("transcription-output").innerText = "";
    lastValidText = "";
  });

  function startWebcam() {
    return navigator.mediaDevices.getUserMedia({ video: true, audio: false })
      .then(stream => {
        videoElem.srcObject = stream;
        return videoElem.play();
      })
      .catch(err => console.error("Webcam error:", err));
  }

  function showCountdown(callback) {
    const webcamContainer = document.getElementById("webcam-container");
    if (!countdownOverlay) {
      countdownOverlay = document.createElement('div');
      countdownOverlay.id = 'countdown-overlay';
      Object.assign(countdownOverlay.style, {
        position: 'absolute',
        top: '50%',
        left: '50%',
        transform: 'translate(-50%, -50%)',
        fontSize: '5rem',
        fontWeight: 'bold',
        color: '#fff',
        background: 'rgba(0,0,0,0.7)',
        padding: '30px',
        borderRadius: '12px',
        zIndex: '1000',
        textAlign: 'center',
        width: '120px',
      });
      webcamContainer.style.position = 'relative';
      webcamContainer.appendChild(countdownOverlay);
    }

    let count = 5;
    countdownOverlay.style.display = 'block';
    countdownOverlay.textContent = count;

    const countdown = setInterval(() => {
      count--;
      if (count > 0) {
        countdownOverlay.textContent = count;
      } else {
        clearInterval(countdown);
        countdownOverlay.style.display = 'none';
        callback();
      }
    }, 1000);
  }

  function captureImageSnapshot() {
    canvas.width = videoElem.videoWidth;
    canvas.height = videoElem.videoHeight;
    ctx.drawImage(videoElem, 0, 0, canvas.width, canvas.height);

    canvas.toBlob(blob => {
      const formData = new FormData();
      formData.append('image', blob, 'frame.jpg');

      spinner.classList.remove("hidden");

      fetch('/predict', {
        method: 'POST',
        body: formData
      })
        .then(res => res.json())
        .then(data => {
          console.log("[📦 Response]", data);
          if (data.label) {
            restorePreviousText();
            appendTranscription(data.label);
          } else if (data.error) {
            appendErrorHint(data.error);
          }
        })
        .catch(err => {
          console.error('Snapshot prediction error:', err);
        })
        .finally(() => {
          spinner.classList.add("hidden");
        });
    }, 'image/jpeg');
  }

  function appendTranscription(text) {
    const output = document.getElementById('transcription-output');

    if (
      output.innerText.includes("Teks hasil deteksi akan tampil di sini") ||
      output.innerText.startsWith("⛔")
    ) {
      output.innerText = '';
      lastValidText = '';
    }

    let i = 0;
    const typeInterval = setInterval(() => {
      if (i < text.length) {
        output.textContent += text[i];
        i++;
        output.scrollTop = output.scrollHeight;
      } else {
        clearInterval(typeInterval);
        lastValidText = output.textContent.trim();
      }
    }, 50);
  }

  function appendErrorHint(msg) {
    const output = document.getElementById('transcription-output');
    if (!output.innerText.startsWith("⛔")) {
      lastValidText = output.innerText.trim();
    }
    output.innerText = "⛔ " + msg;

    setTimeout(() => {
      if (output.innerText.startsWith("⛔")) {
        output.innerText = lastValidText;
      }
    }, 2500);
  }

  function restorePreviousText() {
    const output = document.getElementById('transcription-output');
    if (output.innerText.startsWith("⛔")) {
      output.innerText = lastValidText;
    }
  }
});
