# test_backend.py
from predict import predict_image
import cv2

# Path ke gambar uji coba (ganti dengan nama file kamu)
image_path = "static/uploads/body dot (4).jpg"

# Jalankan prediksi
hasil = predict_image(image_path)

print("\n=== HASIL PREDIKSI BACKEND ===")
if isinstance(hasil, tuple):
    label, confidence = hasil
    print(f"✅ Huruf Terdeteksi: {label}")
    print(f"🔢 Confidence: {confidence:.2f}")
else:
    print(f"❌ Error: {hasil}")

print("📸 Debug disimpan: debug_output.jpg")
