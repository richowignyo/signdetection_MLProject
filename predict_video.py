import numpy as np
import cv2
from tensorflow.keras.models import load_model, Model
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

# Konfigurasi
SEQUENCE_LENGTH = 50
IMG_SIZE = (112, 112)

# Load model LSTM Bisindo
lstm_model = load_model('model/lstm_bisindo_kata_model.h5')

# CNN feature extractor
base_cnn = MobileNetV2(
    weights='imagenet',
    include_top=False,
    pooling='avg',
    input_shape=(*IMG_SIZE, 3)
)
cnn_model = Model(inputs=base_cnn.input, outputs=base_cnn.output)

# Urutan label sesuai training
LABELS = [
    'Apa', 'Apa Kabar', 'Bagaimana', 'Baik', 'Belajar', 'Berapa', 'Berdiri', 'Bingung', 'Dia',
    'Dimana', 'Duduk', 'Halo', 'Kalian', 'Kami', 'Kamu', 'Kapan', 'Kemana', 'Kita', 'Makan', 'Mandi',
    'Marah', 'Melihat', 'Membaca', 'Menulis', 'Mereka', 'Minum', 'Pendek', 'Ramah', 'Sabar', 
    'Saya', 'Sedih', 'Selamat Malam', 'Selamat Pagi', 'Selamat Siang', 'Selamat Sore', 'Senang', 'Siapa', 'Terima Kasih',
    'Tidur', 'Tinggi' 
]

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
    if len(frames) == 0:
        return None

    while len(frames) < max_frames:
        frames.append(np.zeros_like(frames[0]))

    frames_array = np.array(frames)
    features = cnn_model.predict(frames_array, verbose=0)
    return np.expand_dims(features, axis=0)

def predict_video(video_path):
    features = extract_features_from_video(video_path)
    if features is None:
        return None

    prediction = lstm_model.predict(features, verbose=0)[0]
    label_idx = np.argmax(prediction)
    confidence = prediction[label_idx]

    if confidence < 0.8:
        return None
    return LABELS[label_idx]
