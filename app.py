from flask import Flask, render_template, redirect, url_for, request, jsonify
import os
from werkzeug.utils import secure_filename
from predict import predict_image, fallback_predict_image

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

    if isinstance(result, tuple):
        label, confidence = result
        os.remove(path)
        return jsonify({'label': label, 'confidence': round(confidence, 2)})

    elif isinstance(result, str):
        os.remove(path)
        return jsonify({'error': result}), 200

    result = fallback_predict_image(path)
    os.remove(path)

    if isinstance(result, tuple):
        label, confidence = result
        return jsonify({'label': label, 'confidence': round(confidence, 2)})
    else:
        return jsonify({'error': 'No hand detected or confidence too low'}), 200

if __name__ == '__main__':
    app.run(debug=True)
