
# OpenHordeProxy

OpenHordeProxy is a Python-based proxy tool that converts OpenAI image and text generation requests into requests for AI Horde, using a Flask API. This tool allows developers to seamlessly switch between OpenAI's image generation models, chat completions, and AI Horde.

## Features
- Proxy OpenAI requests to AI Horde via Flask API.
- Support for various image formats including PNG, JPEG, and more.
- Text generation through the AI Horde text models.
- Easy configuration using environment variables.
- Integrated with AI Horde SDK.
- Supports LoRA models for fine-tuning image generation.
- Automatic image saving and URL generation with configurable server paths.
- Flexible model mapping from OpenAI to AI Horde models.
- Configurable generation parameters like sampler, scale, steps, and more.
- Fetch available models from AI Horde via the `/v1/models` endpoint.

## Model Mapping

You can map OpenAI models to specific AI Horde models by configuring the `.env` file with environment variables. For example:

```env
OPENAI_MODEL_MAP_gpt_35_turbo=koboldcpp/LLaMA2-13B-Psyfighter2
OPENAI_MODEL_MAP_gpt_4=StableDiffusion
```

The application will automatically use the mapped AI Horde model when the corresponding OpenAI model is requested.

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
DEFAULT_HORDE_MODEL=Deliberate
IMAGE_SAVE_PATH=requested_images
SERVER_BASE_URL=http://localhost:5000/images/
LORAS=GlowingRunesAI,AnotherLora:2

# Model mapping from OpenAI models to AI Horde models
OPENAI_MODEL_MAP_gpt_35_turbo=koboldcpp/LLaMA2-13B-Psyfighter2
OPENAI_MODEL_MAP_gpt_4=StableDiffusion

# Enable or disable anonymous access (set to True to allow anonymous requests without an API key)
ALLOW_ANONYMOUS_ACCESS=False

# Additional generation parameters (optional)
SAMPLER_NAME=k_euler
CFG_SCALE=7
CLIP_SKIP=1
STEPS=30
HIRES_FIX=False
```

### Testing with Curl

You can test the text generation with model mapping using this curl command:

```bash
curl -X POST http://localhost:5000/v1/chat/completions -H "Content-Type: application/json" -H "Authorization: Bearer YOUR_OPENAI_API_KEY" -d '{
    "model": "gpt-3.5-turbo",
    "messages": [{"role": "user", "content": "What is the meaning of life?"}],
    "max_completion_tokens": 100,
    "temperature": 0.7,
    "top_p": 0.95
}'
```

## License

This project is licensed under the MIT License.
