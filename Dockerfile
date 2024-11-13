# Use the desired Python version
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . .

# Copy the SavedModel directory specifically
COPY goat_sex_model_tf_saved /app/goat_sex_model_tf_saved

# Expose the port that Flask will run on
EXPOSE 8000

# Start the Flask application using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--timeout", "120", "app:app"]

