
#!/bin/bash

# Start the Flask application using Gunicorn with 4 workers
echo "Starting OpenHordeProxy with Gunicorn..."
gunicorn --workers 4 --bind 0.0.0.0:5000 app:app
