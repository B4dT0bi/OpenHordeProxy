from flask import Blueprint, jsonify, request
from config import Config
from services.text_service import generate_text_service
from loguru import logger

# Initialize the blueprint for text routes
text_blueprint = Blueprint('text_routes', __name__)


# Endpoint for chat completion (POST request)
@text_blueprint.route('/v1/chat/completions', methods=['POST'])
def chat_completions():
    data = request.json

    # Check if messages and model are provided, otherwise return an error
    messages = data.get("messages")
    model = data.get("model")
    if not messages or not model:
        return jsonify({"error": "Messages and model are required"}), 400

    # Extract the API key from the Authorization header using Bearer token
    auth_header = request.headers.get("Authorization")
    api_key = None

    if auth_header and auth_header.startswith("Bearer "):
        api_key = auth_header.split(" ")[1]  # Extract the key after 'Bearer'
    elif not auth_header and not Config.ALLOW_ANONYMOUS_ACCESS:
        return jsonify({"error": "Authorization header must be provided and start with 'Bearer'"}), 401

    # Extract other optional parameters
    frequency_penalty = data.get("frequency_penalty", 0)
    presence_penalty = data.get("presence_penalty", 0)
    temperature = data.get("temperature", 1)
    top_p = data.get("top_p", 1)
    max_completion_tokens = data.get("max_completion_tokens")
    logit_bias = data.get("logit_bias")
    n = data.get("n", 1)
    stop = data.get("stop")

    logger.info(f"Chat request for model: {model}, temperature: {temperature}, top_p: {top_p}")

    # Call service function to generate chat completions
    return jsonify(generate_text_service(messages, model, api_key, max_completion_tokens, frequency_penalty,
                                         presence_penalty, temperature, top_p, logit_bias, n, stop))
