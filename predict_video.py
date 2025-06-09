# predict_video.py (revisi)

import numpy as np
import cv2
from tensorflow.keras.models import load_model
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.models import Model

# Config
SEQUENCE_LENGTH = 50
IMG_SIZE = (112, 112)

# Load model
lstm_model = load_model('model/lstm_model.h5')

# CNN extractor
base_cnn = MobileNetV2(weights='imagenet', include_top=False, pooling='avg', input_shape=(*IMG_SIZE, 3))
cnn_model = Model(inputs=base_cnn.input, outputs=base_cnn.output)

# Labels (pastikan urutan sesuai training)
LABELS = ['Apa Kabar', 'Baik', 'Halo', 'Kami', 'Kamu', 'Saya', 'Selamat Pagi', 'Selamat Siang', 'Selamat Sore', 'Terima Kasih']

def extract_features_from_video(video_path, max_frames=SEQUENCE_LENGTH):
    cap = cv2.VideoCapture(video_path)
    frames = []

    while len(frames) < max_frames:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.resize(frame, IMG_SIZE)
        frame = preprocess_input(frame.astype(np.float32))
        frames.append(frame)

    cap.release()

    while len(frames) < max_frames:
        frames.append(np.zeros_like(frames[0]))

    frames_array = np.array(frames)  # (SEQUENCE_LENGTH, H, W, C)
    features = cnn_model.predict(frames_array, verbose=0)  # (SEQUENCE_LENGTH, 1280)
    return np.expand_dims(features, axis=0)  # (1, SEQUENCE_LENGTH, 1280)

def predict_video(video_path):
    features = extract_features_from_video(video_path)
    prediction = lstm_model.predict(features, verbose=0)[0]
    label_idx = np.argmax(prediction)
    confidence = prediction[label_idx]

    if confidence < 0.8:
        return None
    return LABELS[label_idx]
