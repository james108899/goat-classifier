import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import GlobalAveragePooling2D, Dense

# Recreate the model architecture
base_model = MobileNetV2(input_shape=(150, 150, 3), include_top=False, weights='imagenet')
base_model.trainable = False

model = tf.keras.Sequential([
    base_model,
    GlobalAveragePooling2D(),
    Dense(1, activation='sigmoid')
])

# Load weights from the original .h5 file
model.load_weights('goat_sex_model.h5')

# Save the model in the SavedModel format
model.save('goat_sex_model_tf_saved', save_format='tf')
