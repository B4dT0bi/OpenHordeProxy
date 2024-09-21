from flask import Blueprint, jsonify
import asyncio
from services.models_service import get_models

models_blueprint = Blueprint('models_routes', __name__)


@models_blueprint.route('/v1/models', methods=['GET'])
def get_available_models():
    model_type = "text"  # Default to text models
    models = asyncio.run(get_models(model_type))
    
    # Wrap models in the correct format
    response = {
        "object": "list",
        "data": models
    }
    
    return jsonify(response)
