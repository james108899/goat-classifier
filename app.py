from flask import Flask, request, jsonify, send_from_directory
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from io import BytesIO
from PIL import Image
import os

app = Flask(__name__)
model = load_model('goat_sex_model_tf_saved')

# Create uploads directory if it doesn't exist
os.makedirs('uploads', exist_ok=True)

# Welcome message route
@app.route('/')
def welcome():
    return "Welcome to the Goat Classifier API!"

# Serve the frontend files
@app.route('/<path:filename>')
def frontend_files(filename):
    return send_from_directory('frontend', filename)

# Prediction route
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get the uploaded image file
        file = request.files['image']
        # Open and process the image
        img = Image.open(BytesIO(file.read()))

        # Convert RGBA to RGB if necessary
        if img.mode == 'RGBA':
            img = img.convert('RGB')

        # Resize the image to match model input size
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

        # Save the image with prediction label and accuracy in filename
        output_path = f"uploads/{result}_{accuracy_percentage:.2f}_{file.filename}"
        img.save(output_path)

        # Send the result to the frontend
        return jsonify({
            'prediction': result,
            'accuracy_percentage': accuracy_percentage,
            'image_url': f"/uploads/{result}_{accuracy_percentage:.2f}_{file.filename}"
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Serve saved images from the uploads folder
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory('uploads', filename)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
