from flask import Flask, request, jsonify
import os
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from io import BytesIO
from PIL import Image
import datetime

app = Flask(__name__)
model = load_model('goat_sex_model_tf_saved')

# Welcome route
@app.route('/')
def welcome():
    return "Welcome to the Goat Classifier API!"

# Prediction route
@app.route('/predict', methods=['POST'])
def predict():
    try:
        file = request.files['image']
        img = Image.open(BytesIO(file.read()))

        # Convert RGBA to RGB if necessary
        if img.mode == 'RGBA':
            img = img.convert('RGB')

        # Resize image to model's input size
        img = img.resize((150, 150))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array /= 255.0  # Normalize image

        # Make prediction
        prediction = model.predict(img_array)
        result = 'Billy' if prediction > 0.5 else 'Nanny'
        accuracy_percentage = float(prediction[0][0]) * 100

        return jsonify({
            'prediction': result,
            'accuracy_percentage': accuracy_percentage
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route to save images with prediction and confidence
@app.route('/save_image', methods=['POST'])
def save_image():
    try:
        file = request.files['image']
        prediction = request.form['prediction']
        confidence = request.form['confidence']

        # Generate filename based on prediction, confidence, and timestamp
        timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        filename = f"{prediction}_{confidence}_{timestamp}.jpg"
        save_path = os.path.join("saved_images", filename)

        # Create directory if it doesn't exist
        if not os.path.exists("saved_images"):
            os.makedirs("saved_images")

        # Save the image
        img = Image.open(file.stream)
        img.save(save_path)

        return jsonify({"message": "Image saved successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
