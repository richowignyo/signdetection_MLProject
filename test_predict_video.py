from predict import predict_image
from predict_video import predict_video
import os

def detect_auto(image_path=None, video_path=None):
    if video_path and os.path.exists(video_path):
        print(f"Mencoba prediksi sebagai video (kata): {video_path}")
        result = predict_video(video_path)
        if result:
            print(f"[KATA - Video] Deteksi: {result}")
            return
        else:
            print("[KATA - Video] Tidak terdeteksi, fallback ke huruf.")

    if image_path and os.path.exists(image_path):
        print(f"Mencoba prediksi sebagai gambar (huruf): {image_path}")
        result = predict_image(image_path)
        if result:
            print(f"[HURUF - Image] Deteksi: {result[0]} dengan confidence {result[1]:.2f}")
        else:
            print("[HURUF - Image] Tidak terdeteksi.")

# Contoh penggunaan
detect_auto(image_path='C:/6 - machine Learning/signdetection_MLProject/static/uploads/body dot (4).jpg')
detect_auto(video_path='C:/6 - machine Learning/signdetection_MLProject/static/uploads/BISINDO_Apa Kabar_001.mp4')
