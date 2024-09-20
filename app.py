
from flask import Flask
from config import Config
from routes.image_routes import image_blueprint

# Create Flask app instance
app = Flask(__name__)

# Register the blueprint for image routes
app.register_blueprint(image_blueprint)

if __name__ == '__main__':
    # Run Flask app
    app.run(host=Config.HOST, port=Config.PORT)
