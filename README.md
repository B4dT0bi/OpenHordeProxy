# OpenHordeProxy

OpenHordeProxy is a Python-based proxy tool that converts OpenAI image and text generation requests into requests for AI
Horde, using a Flask API. This tool allows developers to seamlessly switch between OpenAI's image generation models,
chat completions, and AI Horde.

## Features

- Proxy OpenAI requests to AI Horde via Flask API.
- Text generation through the AI Horde text models.
- Easy configuration using environment variables.
- Integrated with AI Horde SDK.
- Supports LoRA models for fine-tuning image generation.
- Automatic image saving and URL generation with configurable server paths.
- Flexible model mapping from OpenAI to AI Horde models.
- Configurable generation parameters like sampler, scale, steps, and more.

## Requirements

- Python 3.8 or higher
- Flask
- Gunicorn (for production)
- horde-sdk
- Pillow
- python-dotenv
- loguru

## Installation

### Using Python's `venv`

1. Create a virtual environment using Python's built-in `venv`:

```bash
python3 -m venv venv
```

2. Activate the virtual environment:

On macOS/Linux:

```bash
source venv/bin/activate
```

On Windows:

```bash
venv\Scripts\activate
```

3. Install the dependencies:

```bash
pip install -r requirements.txt
```

### Using `conda`

1. Create a new conda environment:

```bash
conda create -n openhordeproxy python=3.8
```

2. Activate the environment:

```bash
conda activate openhordeproxy
```

3. Install the dependencies:

```bash
pip install -r requirements.txt
```

## Set up the `.env` file:

Create a `.env` file in the project root with the following content:

```env
AI_HORDE_API_KEY=your_ai_horde_api_key
HOST=0.0.0.0
PORT=5000
DEFAULT_HORDE_MODEL=stable_diffusion
IMAGE_SAVE_PATH=requested_images
SERVER_BASE_URL=http://localhost:5000/images/
LORAS=GlowingRunesAI,AnotherLora:2

# Model mapping from OpenAI models to AI Horde models
OPENAI_MODEL_MAP_dall_e_2=stable_diffusion
OPENAI_MODEL_MAP_dall_e_3='SDXL 1.0'

# Enable or disable anonymous access (set to True to allow anonymous requests without an API key)
ALLOW_ANONYMOUS_ACCESS=False

# Additional generation parameters (optional)
SAMPLER_NAME=k_euler
CFG_SCALE=7
CLIP_SKIP=1
STEPS=30
HIRES_FIX=False
```

## Starting the Application in Production

In a production environment, you should use a WSGI server like **Gunicorn** instead of the built-in Flask server.

To install **Gunicorn**, run:

```bash
pip install gunicorn
```

### Running with Gunicorn

You can start the application with the included `start.sh` script, which uses **Gunicorn**:

```bash
./start.sh
```

This will start the Flask application using Gunicorn with 4 workers, running on `http://0.0.0.0:5000`.

Alternatively, you can manually run Gunicorn with:

```bash
gunicorn --workers 4 --bind 0.0.0.0:5000 app:app
```

### Nginx as a Reverse Proxy (Optional)

For improved performance and security in production, it's recommended to use **Nginx** as a reverse proxy to forward
requests to Gunicorn. Here's an example Nginx configuration:

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /images/ {
        alias /path/to/your/image/folder/;
    }
}
```

Make sure to replace `/path/to/your/image/folder/` with the correct path where the images are stored.

## API Endpoints

### Image Generation

- **Endpoint:** `/v1/images/generations`
- **Method:** `POST`

**Request Format:**

```json
{
  "prompt": "A futuristic cityscape with flying cars",
  "n": 2,
  "size": "512x512",
  "model": "dall-e-2"
}
```

**Response Format:**

```json
{
  "data": [
    {
      "url": "http://localhost:5000/images/jobid_generation_1.webp"
    },
    {
      "url": "http://localhost:5000/images/jobid_generation_2.webp"
    }
  ]
}
```

### Text Generation (Chat Completion)

- **Endpoint:** `/v1/chat/completions`
- **Method:** `POST`

**Request Format:**

```json
{
  "model": "koboldcpp/LLaMA2-13B-Psyfighter2",
  "messages": [
    {
      "role": "user",
      "content": "What is the meaning of life?"
    }
  ],
  "max_completion_tokens": 100,
  "temperature": 0.7,
  "top_p": 0.95
}
```

**Response Format:**

```json
{
  "choices": [
    {
      "text": "The meaning of life is subjective and depends on the individual."
    }
  ]
}
```

### Testing with Curl

#### Image Generation

```bash
curl -X POST http://localhost:5000/v1/images/generations -H "Content-Type: application/json" -H "Authorization: Bearer YOUR_OPENAI_API_KEY" -d '{
    "prompt": "A magical forest with glowing trees",
    "n": 1,
    "size": "512x512",
    "model": "dall-e-2"
}'
```

#### Text Generation (Chat Completion)

```bash
curl -X POST http://localhost:5000/v1/chat/completions -H "Content-Type: application/json" -H "Authorization: Bearer YOUR_OPENAI_API_KEY" -d '{
    "model": "koboldcpp/LLaMA2-13B-Psyfighter2",
    "messages": [{"role": "user", "content": "What is the meaning of life?"}],
    "max_completion_tokens": 100,
    "temperature": 0.7,
    "top_p": 0.95
}'
```

## License

This project is licensed under the MIT License.
