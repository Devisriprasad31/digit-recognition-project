from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
import numpy as np
from PIL import Image
import io
import os

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Allow frontend to connect to backend

# Define model path (Ensure correct extension)
MODEL_PATH = os.path.join(os.path.dirname(__file__), "model", "handwritten_digit_model.keras")

# Load the trained CNN model
try:
    model = tf.keras.models.load_model(MODEL_PATH)
    print("Model loaded successfully!")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

# Function to preprocess image
def preprocess_image(image):
    image = image.convert("L")  # Convert to grayscale
    image = image.resize((28, 28))  # Resize to 28x28
    image = np.array(image) / 255.0  # Normalize
    image = image.reshape(1, 28, 28, 1)  # Reshape for model input
    return image

# API route for image upload and prediction
@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    image = Image.open(io.BytesIO(file.read()))  # Read image
    processed_image = preprocess_image(image)  # Preprocess

    if model is None:
        return jsonify({"error": "Model not loaded"}), 500

    # Predict using the model
    prediction = model.predict(processed_image)
    predicted_digit = np.argmax(prediction)  # Get digit with highest probability

    return jsonify({"digit": int(predicted_digit)})  # Send result to frontend

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
