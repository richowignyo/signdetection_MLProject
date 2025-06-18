import cv2
import numpy as np
import mediapipe as mp
from tensorflow.keras.models import load_model
import pickle
import torch
from ultralytics import YOLO

# Load models
model_1hand = load_model("model/model_1hand.h5")
model_2hand = load_model("model/model_2hand.h5")

# Load label encoders
with open("model/label_encoder_1hand.pkl", "rb") as f:
    le_1 = pickle.load(f)
with open("model/label_encoder_2hand.pkl", "rb") as f:
    le_2 = pickle.load(f)

# Setup MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=4, min_detection_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# Load YOLO model for person detection
yolo_model = YOLO('yolov8n.pt')

# Enhancement used in training
def enhance_image(img):
    img = cv2.resize(img, (480, 480))
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    l_eq = cv2.equalizeHist(l)
    enhanced = cv2.merge((l_eq, a, b))
    return cv2.cvtColor(enhanced, cv2.COLOR_LAB2BGR)

def detect_people_yolo(image, conf_threshold=0.8):
    results = yolo_model(image)[0]
    count = 0
    for box in results.boxes:
        cls_id = int(box.cls[0])
        conf = float(box.conf[0])
        if cls_id == 0 and conf > conf_threshold:
            count += 1
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(image, f'Person {conf:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
    return count

def predict_image(image_path):
    image_raw = cv2.imread(image_path)
    if image_raw is None:
        return "Gambar tidak dapat dibaca."

    image_for_yolo = image_raw.copy()
    image_for_mp = image_raw.copy()

    person_count = detect_people_yolo(image_for_yolo)
    if person_count > 1:
        cv2.imwrite("debug_output.jpg", image_for_yolo)
        return "Terdeteksi lebih dari 1 orang. Harap gunakan 1 orang saja."

    enhanced_image = enhance_image(image_for_mp)
    img_rgb = cv2.cvtColor(enhanced_image, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    if not results.multi_hand_landmarks:
        cv2.imwrite("debug_output.jpg", image_for_mp)
        return "Tidak ada tangan terdeteksi."

    landmarks = results.multi_hand_landmarks
    num_hands = len(landmarks)

    if num_hands > 2:
        return "Terdeteksi lebih dari 2 tangan. Harap gunakan maksimal 2 tangan."

    all_coords = []
    for i, hand_landmarks in enumerate(landmarks):
        if len(hand_landmarks.landmark) < 19:
            return f"Tangan ke-{i+1} memiliki landmark kurang dari 19 (hanya {len(hand_landmarks.landmark)})."
        for lm in hand_landmarks.landmark:
            all_coords.extend([lm.x, lm.y])
        mp_drawing.draw_landmarks(image_for_mp, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    vec = np.array(all_coords).reshape(1, -1).astype("float32")

    if num_hands == 1 and vec.shape[1] == 42:
        pred = model_1hand.predict(vec, verbose=0)[0]
        label = le_1.inverse_transform([np.argmax(pred)])[0]
        conf = float(np.max(pred))
        cv2.imwrite("debug_output.jpg", image_for_mp)
        if conf < 0.5:
            return "Prediksi tidak cukup yakin untuk 1 tangan."
        return label, conf

    elif num_hands == 2 and vec.shape[1] == 84:
        pred = model_2hand.predict(vec, verbose=0)[0]
        label = le_2.inverse_transform([np.argmax(pred)])[0]
        conf = float(np.max(pred))
        cv2.imwrite("debug_output.jpg", image_for_mp)
        if conf < 0.5:
            return "Prediksi tidak cukup yakin untuk 2 tangan."
        return label, conf

    return "Format input tidak sesuai untuk prediksi."

def fallback_predict_image(image_path):
    return predict_image(image_path)
