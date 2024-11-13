import tensorflow as tf
print("TensorFlow Version:", tf.__version__)
print("Keras Version:", tf.keras.__version__)

try:
    model = tf.keras.models.load_model('C:/Users/mrrda/Documents/goat_project/goat_sex_model.h5')
    print("Model loaded successfully")
except Exception as e:
    print("Error loading model:", str(e))
