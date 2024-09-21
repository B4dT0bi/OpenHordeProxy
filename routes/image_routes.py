from flask import Blueprint, send_from_directory, jsonify, request
from config import Config
from services.image_service import generate_image_service
from loguru import logger

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
    api_key = None

    if auth_header and auth_header.startswith("Bearer "):
        api_key = auth_header.split(" ")[1]  # Extract the key after 'Bearer'
    elif not auth_header and not Config.ALLOW_ANONYMOUS_ACCESS:
        return jsonify({"error": "Authorization header must be provided and start with 'Bearer'"}), 401

    # Extract other parameters
    n = data.get("n", 1)
    size = data.get("size", "512x512")
    model = data.get("model", "dall-e-2")

    # Extract and log the additional parameters
    quality = data.get("quality", "standard")
    response_format = data.get("response_format", "url")
    style = data.get("style", "vivid")

    logger.info(f"Quality: {quality}, Response Format: {response_format}, Style: {style}")

    # If response_format is not "url" or "b64_json", return an error
    if response_format not in ["url", "b64_json"]:
        return jsonify({"error": "Only 'url' and 'b64_json' response formats are supported at this time."}), 400

    # Call service function to generate images, passing the API key and response format
    return jsonify(generate_image_service(prompt, n, size, model, api_key, response_format))
