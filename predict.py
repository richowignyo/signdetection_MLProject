# predict.py (FIXED: sinkronisasi preprocessing)
import cv2
import numpy as np
import mediapipe as mp
from tensorflow.keras.models import load_model
import pickle

# Load models
model_1hand = load_model("model/model_1hand.h5")
model_2hand = load_model("model/model_2hand.h5")

# Load label encoders
with open("model/label_encoder_1hand.pkl", "rb") as f:
    le_1 = pickle.load(f)
with open("model/label_encoder_2hand.pkl", "rb") as f:
    le_2 = pickle.load(f)

# Setup MediaPipe (real-time friendly)
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# Enhancement used in training
def enhance_image(img):
    img = cv2.resize(img, (480, 480))
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    l_eq = cv2.equalizeHist(l)
    enhanced = cv2.merge((l_eq, a, b))
    return cv2.cvtColor(enhanced, cv2.COLOR_LAB2BGR)

def predict_image(image_path):
    image = cv2.imread(image_path)
    if image is None:
        return None

    image = enhance_image(image)
    img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    if not results.multi_hand_landmarks:
        return None

    landmarks = results.multi_hand_landmarks
    num_hands = len(landmarks)
    print(f"[DEBUG] Jumlah tangan terdeteksi: {num_hands}")

    all_coords = []
    for hand_landmarks in landmarks:
        for lm in hand_landmarks.landmark:
            all_coords.extend([lm.x, lm.y])

    vec = np.array(all_coords).reshape(1, -1).astype("float32")
    print(f"[DEBUG] Input shape: {vec.shape}")

    if num_hands == 1 and vec.shape[1] == 42:
        pred = model_1hand.predict(vec, verbose=0)[0]
        label = le_1.inverse_transform([np.argmax(pred)])[0]
        conf = float(np.max(pred))
        if conf < 0.5:
            return None
        return label, conf

    elif num_hands == 2 and vec.shape[1] == 84:
        pred = model_2hand.predict(vec, verbose=0)[0]
        label = le_2.inverse_transform([np.argmax(pred)])[0]
        conf = float(np.max(pred))
        if conf < 0.5:
            return None
        return label, conf

    return None

def fallback_predict_image(image_path):
    return predict_image(image_path)
