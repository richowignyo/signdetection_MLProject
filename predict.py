import cv2
import numpy as np
import mediapipe as mp
from tensorflow.keras.models import load_model

# Load trained model
model = load_model("model/fcnn_bisindo_final.h5")

# Setup MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=True, max_num_hands=1)

# Label mapping (0 -> A, ..., 25 -> Z)
label_map = [chr(i) for i in range(65, 91)]

def predict_image(image_path):
    image = cv2.imread(image_path)
    if image is None:
        return None
    img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    result = hands.process(img_rgb)

    if result.multi_hand_landmarks:
        lm = result.multi_hand_landmarks[0].landmark
        wrist = lm[0]
        coords = np.array([[pt.x - wrist.x, pt.y - wrist.y] for pt in lm])
        max_val = np.max(np.abs(coords))
        coords = coords / max_val if max_val != 0 else coords
        vec = coords.flatten().reshape(1, -1).astype("float32")

        pred = model.predict(vec)[0]
        pred_idx = np.argmax(pred)
        confidence = float(pred[pred_idx])
        if confidence < 0.8:
            return None  # skip prediksi tidak yakin
        return label_map[pred_idx], confidence
    return None

# Example usage:
# result = predict_image("static/uploads/test.jpg")
# print(result)  # ('C', 0.91)
