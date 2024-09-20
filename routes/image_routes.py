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

    n = data.get("n", 1)
    size = data.get("size", "512x512")
    model = data.get("model", "dall-e-2")

    # Call service function to generate images
    return jsonify(generate_image_service(prompt, n, size, model))
