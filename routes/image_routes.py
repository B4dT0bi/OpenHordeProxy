from flask import Blueprint, send_from_directory, jsonify, request
from config import Config
from services.image_service import generate_image_service

# Initialize the blueprint for image routes
image_blueprint = Blueprint('image_routes', __name__)

# Route for serving images if internal server is enabled
if Config.ENABLE_IMAGE_SERVER:
    @image_blueprint.route('/images/<filename>')
    def serve_image(filename):
        image_directory = Config.IMAGE_SAVE_PATH
        try:
            return send_from_directory(image_directory, filename)
        except FileNotFoundError:
            return jsonify({"error": "Image not found"}), 404


# Endpoint for image generation (POST request)
@image_blueprint.route('/v1/images/generations', methods=['POST'])
def generate_image():
    data = request.json

    # Check if prompt is provided, otherwise return an error
    prompt = data.get("prompt")
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400

    # Extract the API key from the Authorization header using Bearer token
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "Authorization header must be provided and start with 'Bearer'"}), 401

    api_key = auth_header.split(" ")[1]  # Extract the key after 'Bearer'

    # Extract other parameters
    n = data.get("n", 1)
    size = data.get("size", "512x512")
    model = data.get("model", "dall-e-2")

    # Call service function to generate images, passing the API key
    return jsonify(generate_image_service(prompt, n, size, model, api_key))
