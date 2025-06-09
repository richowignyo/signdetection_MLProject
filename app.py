from flask import Flask, render_template, redirect, url_for, request, jsonify
import os
from werkzeug.utils import secure_filename
from predict import predict_image
from predict_video import predict_video  # pastikan file ini ada

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/chat')
def chat():
    return render_template('chat.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/bisindo')
def bisindo():
    return render_template('bisindo.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'Empty filename'}), 400

    filename = secure_filename(file.filename)
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(path)

    result = predict_image(path)
    if result is None:
        return jsonify({'error': 'No hand detected'}), 200

    label, confidence = result
    return jsonify({'label': label, 'confidence': round(confidence, 2)})

@app.route('/predict-video', methods=['POST'])
def predict_video_route():
    if 'video' not in request.files:
        return jsonify({'error': 'No video uploaded'}), 400
    file = request.files['video']
    if file.filename == '':
        return jsonify({'error': 'Empty filename'}), 400

    filename = secure_filename(file.filename)
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(path)

    label = predict_video(path)
    if label:
        return jsonify({'label': label})
    else:
        return jsonify({'label': None})  # fallback to image handled in JS

if __name__ == '__main__':
    app.run(debug=True)
