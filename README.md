# 👌✌️ Sign Language Detection - BISINDO Alphabet Recognition

A deep learning–based web application for real-time classification of BISINDO (Bahasa Isyarat Indonesia) alphabets using **MediaPipe Hands** and **Fully Connected Neural Network (FCNN)**.

> 📌 Built with Python, Flask, and TensorFlow/Keras.  
> 🖐️ Input: Hand landmarks (1 or 2 hands).  
> 🌐 Output: Predicted letter via web interface.

![Python](https://img.shields.io/badge/Python-3.10-red)
![Flask](https://img.shields.io/badge/Framework-Flask-yellow)
![Mediapipe](https://img.shields.io/badge/Mediapipe-Hands-green)
![Model](https://img.shields.io/badge/Model-FCNN-brown)
![Status](https://img.shields.io/badge/Deployment-Ready-pink)

---

## 📁 Project Structure

### signdetection_MLProject/
### ├── app.py # Flask web server
### ├── predict.py # Prediction logic
### ├── yolov8n.pt # YOLOv8 model weights (optional)
### ├── model/ # Saved FCNN models
### ├── static/ # Static files (images, CSS)
### │ └── sample_output.png # Example result
### ├── templates/ # Frontend templates
### ├── requirements.txt # Python dependencies
### └── README.md # Project documentation

---

## 🔄 Project Workflow

### 🔹 1. Data Preprocessing
- Resize to 480x480 px
- CLAHE to enhance hand detail
- Adaptive augmentation (rotation, shift, zoom, brightness) using `ImageDataGenerator`
- Output stored in `.csv` and zipped images

### 🔹 2. Feature Extraction with MediaPipe
- 21 landmarks per hand → numeric vectors
- 2 variants: 1 hand (42 features), 2 hands (84 features)
- Visualized for all alphabet classes

### 🔹 3. Dataset Split
- Stratified 80% train, 10% validation, 10% test
- Total samples:
  - 2,480 (1 hand) → 1,984 train, 248 val, 248 test
  - 5,980 (2 hands) → 4,784 train, 598 val, 598 test

---

## 🧠 FCNN Model Architecture

### 🖐️ 1-Hand Model
- Dense → BatchNorm → Dropout
- Total Parameters: 21,002
- Efficient for light deployment (82 KB)

### ✋✋ 2-Hand Model
- Deeper layers, more neurons
- Total Parameters: 80,912
- Suitable for complex handshape classification

---

## 📈 Evaluation Results

| Metric       | 1-Hand Model | 2-Hand Model |
|--------------|--------------|--------------|
| Accuracy     | 99%          | 98.96%       |
| Loss         | 0.0031       | 0.0486       |

- Precision, recall, and F1-score near 1.00 for most classes
- Minor drops only in class **V (1-hand)**, and **P & T (2-hand)**

---

## 📊 Visual Results

- 📉 Accuracy & Loss curves show fast convergence and minimal overfitting
- 🔀 Confusion matrix highlights model strength and few misclassifications

---

## 🖼️ Example Output

> Visual result from processed input image:

![Sample Output](static/sample_output.png)

---

## 🚀 How to Run the App Locally

```bash
# 1. Clone the repo
git clone https://github.com/richowignyogyo/signdetection_MLProject.git
cd signdetection_MLProject

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the Flask app
python app.py
```

## 🔧 Tech Stack
Python 3.10

Flask (Web)

TensorFlow/Keras (FCNN)

MediaPipe (Hand landmark extraction)

OpenCV

HTML/CSS (Frontend)
---

👤 Author
Richo Wignyogyo Aji S.



---

### ✅ Langkah berikutnya:
1. Buka GitHub → masuk ke repo `signdetection_MLProject`
2. Klik file `README.md`
3. Klik tombol ✏️ **Edit this file**
4. Paste seluruh teks di atas → klik "Commit changes"
