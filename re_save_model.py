from tensorflow.keras.models import load_model

# Load the model in the new environment
model = load_model('goat_sex_model.h5')

# Re-save the model in the SavedModel format
model.save('goat_sex_model_tf_saved', save_format='tf')
