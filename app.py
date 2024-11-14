from flask import Flask, request, jsonify, send_from_directory, render_template
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from io import BytesIO
from PIL import Image
import os

app = Flask(__name__, static_folder="frontend", template_folder="frontend")
model = load_model('goat_sex_model_tf_saved')

# Root route to serve the HTML page
@app.route('/')
def index():
    return send_from_directory(app.template_folder, 'index.html')

# Endpoint to serve other static files (like CSS and JS)
@app.route('/<path:filename>')
def serve_file(filename):
    return send_from_directory(app.static_folder, filename)

# Prediction route
@app.route('/predict', methods=['POST'])
def predict():
    try:
        file = request.files['image']
        img = Image.open(BytesIO(file.read()))
        if img.mode == 'RGBA':
            img = img.convert('RGB')
        img = img.resize((150, 150))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array /= 255.0
        prediction = model.predict(img_array)
        result = 'Billy' if prediction > 0.5 else 'Nanny'
        accuracy_percentage = float(prediction[0][0]) * 100

        return jsonify({
            'prediction': result,
            'accuracy_percentage': accuracy_percentage
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
