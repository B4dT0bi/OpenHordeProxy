import time
import uuid

from flask import Blueprint, jsonify, request
from loguru import logger

from config import Config
from services.text_service import generate_text_service

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

    # Convert messages to a single prompt string
    prompt = "".join([msg['content'] for msg in messages])

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

    # Generate the completion using the text service
    generated_text = generate_text_service(prompt, model, api_key, max_completion_tokens, frequency_penalty,
                                           presence_penalty, temperature, top_p, logit_bias, n, stop)

    # Create a response following the required structure
    response = {
        "id": f"chatcmpl-{str(uuid.uuid4())[:4]}",
        "object": "chat.completion",
        "created": int(time.time()),
        "model": model,
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": generated_text
                },
                "finish_reason": "stop"
            }
        ]
    }

    logger.info(f"Sending response : {response}")
    return jsonify(response)


# Endpoint for prompt completion (POST request)
@text_blueprint.route('/v1/completions', methods=['POST'])
def completions():
    data = request.json

    # Check if prompt and model are provided, otherwise return an error
    prompt = data.get("prompt")
    model = data.get("model")
    if not prompt or not model:
        return jsonify({"error": "Prompt and model are required"}), 400

    # Extract the API key from the Authorization header using Bearer token
    auth_header = request.headers.get("Authorization")
    api_key = None

    if auth_header and auth_header.startswith("Bearer "):
        api_key = auth_header.split(" ")[1]  # Extract the key after 'Bearer'
    elif not auth_header and not Config.ALLOW_ANONYMOUS_ACCESS:
        return jsonify({"error": "Authorization header must be provided and start with 'Bearer'"}), 401

    # Extract other optional parameters
    best_of = data.get("best_of", 1)
    frequency_penalty = data.get("frequency_penalty", 0)
    logit_bias = data.get("logit_bias")
    max_tokens = data.get("max_tokens", 16)
    n = data.get("n", 1)
    presence_penalty = data.get("presence_penalty", 0)
    seed = data.get("seed", None)
    stop = data.get("stop")
    suffix = data.get("suffix", None)
    temperature = data.get("temperature", 1)
    top_p = data.get("top_p", 1)

    logger.info(f"Completion request for model: {model}, temperature: {temperature}, top_p: {top_p}")

    # Generate the completion using the text service
    generated_text = generate_text_service(prompt, model, api_key, max_completion_tokens=max_tokens,
                                           frequency_penalty=frequency_penalty, presence_penalty=presence_penalty,
                                           temperature=temperature, top_p=top_p, logit_bias=logit_bias, n=n, stop=stop)

    # Create response based on the completions format
    response = {
        "id": f"cmpl-{str(uuid.uuid4())[:4]}",
        "object": "text_completion",
        "created": int(time.time()),
        "model": model,
        "choices": [
            {
                "text": generated_text,
                "index": 0,
                "finish_reason": "stop"
            }
        ]
    }

    return jsonify(response)
