# test_predict_model.py
from predict import predict_image
import sys

import cv2
import mediapipe as mp
import matplotlib.pyplot as plt


# Path gambar bisa di-hardcode atau lewat argumen
image_path = "static/uploads/body dot (4).jpg"  # Ganti dengan gambar uji Anda

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

image = cv2.imread(image_path)
rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

with mp_hands.Hands(static_image_mode=True, max_num_hands=2) as hands:
    results = hands.process(rgb)
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.title(f"Terdeteksi {len(results.multi_hand_landmarks)} tangan")
plt.axis('off')
plt.show()

result = predict_image(image_path)

if result:
    label, conf = result
    print(f"\n✅ Prediksi: {label} (Confidence: {conf:.2f})")
else:
    print("❌ Tidak dapat memprediksi. Cek deteksi tangan atau confidence rendah.")
