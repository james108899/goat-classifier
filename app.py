from flask import Flask, request, jsonify
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from io import BytesIO
import os

app = Flask(__name__)
model = load_model('goat_sex_model.h5')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        file = request.files['image']
        img = image.load_img(BytesIO(file.read()), target_size=(150, 150))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array /= 255.0

        prediction = model.predict(img_array)
        result = 'Billy' if prediction > 0.5 else 'Nanny'
        accuracy_percentage = float(prediction[0][0]) * 100

        # If saving the image is required, use a cloud storage solution or database
        # For demonstration, this line is commented out
        # file.save(os.path.join('data/collected', file.filename))

        return jsonify({
            'prediction': result,
            'accuracy_percentage': accuracy_percentage
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

