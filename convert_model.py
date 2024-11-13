from tensorflow.keras.models import load_model

# Load the existing .h5 model
model = load_model('goat_sex_model.h5')

# Save it in the SavedModel format
model.save('goat_sex_model', save_format='tf')
