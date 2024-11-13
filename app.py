from flask import Flask, request, jsonify
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from io import BytesIO
import os
from PIL import Image

app = Flask(__name__)
model = load_model('goat_sex_model_tf_saved')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        file = request.files['image']
        
        # Read the image file and load it as a PIL image
        img = Image.open(BytesIO(file.read()))
        img = img.resize((150, 150))  # Resize the image to the target size
        
        # Convert the image to array and preprocess
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array /= 255.0

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
