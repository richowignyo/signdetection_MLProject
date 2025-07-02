# 👌👆✌️ Sign Detection MLProject

A machine learning project to detect traffic signs using MediaPipe, FCNN, YoloV8, and Flask.  
This project provides a web interface for uploading images and detecting signs in real-time.

![GitHub](https://img.shields.io/badge/Python-3.10-blue)
![GitHub](https://img.shields.io/badge/Framework-Flask-red)
![GitHub](https://img.shields.io/badge/ObjectDetection-YOLOv8-green)
![GitHub](https://img.shields.io/badge/HandLandmarking-Mediapipe-purple)
![GitHub](https://img.shields.io/badge/Modelling-FCNN-black)

---

## 📂 Project Structure

---
#### signdetection_MLProject/
#### ├── app.py # Main Flask application
#### ├── predict.py # Prediction logic using YOLO
#### ├── yolov8n.pt # YOLOv8 model weights
#### ├── requirements.txt # List of dependencies
#### ├── static/ # Static files (CSS, images)
#### │── sample_output.png # Sample detection result
#### ├── templates/ # HTML templates for frontend
#### ├── model/ # (optional) Saved model files
#### └── README.md # This file


---

## 🚀 How to Run the App Locally

### 1. Clone the Repository
```bash
git clone https://github.com/richowignyogyo/signdetection_MLProject.git
cd signdetection_MLProject
```

### 2. Install Requirements
```bash
pip install -r requirements.txt
```

### 3. Run the App
```bash
python app.py
```

## 🧠 Model Used
YOLOv8n from Ultralytics for object detection

OpenCV for image processing

Mediapipe for hand landmark

FCNN for modelling

Flask for web app routing

---

## ✅ Cara Menggunakannya:
1. Buka repo kamu di GitHub
2. Klik file `README.md`
3. Klik tombol ✏️ Edit
4. Hapus isinya dan **paste seluruh markdown di atas**
5. Commit perubahan
