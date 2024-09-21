
from flask import Flask
from routes.image_routes import image_blueprint
from routes.models_routes import models_blueprint
from routes.text_routes import text_blueprint
from config import Config

# Create Flask app instance
app = Flask(__name__)

# Register blueprints
app.register_blueprint(image_blueprint)
app.register_blueprint(text_blueprint)
app.register_blueprint(models_blueprint)

if __name__ == '__main__':
    # Run Flask app
    app.run(host=Config.HOST, port=Config.PORT)
