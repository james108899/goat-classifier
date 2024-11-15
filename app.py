from flask import Flask, request, jsonify, send_from_directory
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from io import BytesIO
from PIL import Image
import os
from google.cloud import storage
import uuid

# Initialize Flask app
app = Flask(__name__, static_folder="frontend", template_folder="frontend")
model = load_model('goat_sex_model_tf_saved')

# Google Cloud Storage bucket name
GCS_BUCKET_NAME = 'goat-classifier-uploads'

# Initialize GCS client and bucket
storage_client = storage.Client()
bucket = storage_client.bucket(GCS_BUCKET_NAME)

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
        filename = file.filename

        # Generate a unique filename to prevent overwriting
        unique_filename = str(uuid.uuid4()) + "_" + filename

        # Save the file temporarily to /tmp
        temp_image_path = os.path.join('/tmp', unique_filename)
        file.save(temp_image_path)

        # Upload the image to GCS
        blob = bucket.blob(f'uploads/{unique_filename}')
        blob.upload_from_filename(temp_image_path)

        # Process the image for prediction
        img = Image.open(temp_image_path)
        if img.mode == 'RGBA':
            img = img.convert('RGB')
        img = img.resize((150, 150))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array /= 255.0

        # Make prediction
        prediction = model.predict(img_array)
        result = 'Billy' if prediction > 0.5 else 'Nanny'
        accuracy_percentage = float(prediction[0][0]) * 100

        # Save prediction results to GCS
        log_data = f"{unique_filename},{result},{accuracy_percentage:.2f}\n"
        log_blob = bucket.blob('predictions_log.csv')

        # Check if the log file exists
        if log_blob.exists():
            # Download existing log data
            existing_log = log_blob.download_as_text()
            new_log = existing_log + log_data
        else:
            new_log = log_data

        # Upload the updated log
        log_blob.upload_from_string(new_log, content_type='text/csv')

        # Clean up temporary file
        os.remove(temp_image_path)

        return jsonify({
            'prediction': result,
            'accuracy_percentage': accuracy_percentage
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
