from flask import Blueprint

# Initialize the blueprint for image routes (if needed in future)
image_blueprint = Blueprint('image_routes', __name__)


def register_routes(app):
    app.register_blueprint(image_blueprint)
