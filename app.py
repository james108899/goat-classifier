from flask import Flask, request, jsonify
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from io import BytesIO
from PIL import Image
import os

app = Flask(__name__)
model = load_model('goat_sex_model_tf_saved')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        file = request.files['image']
        # Open the image using PIL (Pillow)
        img = Image.open(BytesIO(file.read()))
        
        # Convert RGBA to RGB if necessary
        if img.mode == 'RGBA':
            img = img.convert('RGB')
        
        # Resize image to match model input size
        img = img.resize((150, 150))
        
        # Convert image to array
        img_array = image.img_to_array(img)
        
        # Expand dimensions to match model input
        img_array = np.expand_dims(img_array, axis=0)
        
        # Normalize the image
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

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
