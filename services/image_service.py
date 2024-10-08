from config import Config
from horde_sdk.ai_horde_api.apimodels import ImageGenerateAsyncRequest, ImageGenerationInputPayload, LorasPayloadEntry
from horde_sdk.ai_horde_api.ai_horde_clients import AIHordeAPISimpleClient
from horde_sdk import ANON_API_KEY
from pathlib import Path
import base64

# Initialize AI Horde Simple Client
simple_client = AIHordeAPISimpleClient()


# Function to parse LoRAs from configuration
def parse_loras(loras_env):
    if not loras_env:
        return []

    loras = []
    for lora_str in loras_env.split(','):
        parts = lora_str.split(':')
        name = parts[0]
        model = int(parts[1]) if len(parts) > 1 else 1
        clip = int(parts[2]) if len(parts) > 2 else 1
        inject_trigger = parts[3] if len(parts) > 3 else 'any'
        loras.append(LorasPayloadEntry(name=name, model=model, clip=clip, inject_trigger=inject_trigger))
    return loras


# Validate image dimensions
def validate_image_size(width, height):
    if not (64 <= width <= 3072) or not (64 <= height <= 3072):
        raise ValueError("Width and height must be between 64 and 3072.")
    if width % 64 != 0 or height % 64 != 0:
        raise ValueError("Width and height must be divisible by 64.")


# Image generation service function
def generate_image_service(prompt, n, size, model, api_key, response_format="url"):
    try:
        width, height = map(int, size.split('x'))
    except ValueError:
        raise ValueError("Invalid size format. Use 'WIDTHxHEIGHT' format.")

    # Validate image size
    validate_image_size(width, height)

    # Parse LoRAs from configuration
    loras = parse_loras(Config.LORAS)

    # Get additional parameters from config
    sampler_name = Config.SAMPLER_NAME
    cfg_scale = Config.CFG_SCALE
    clip_skip = Config.CLIP_SKIP
    steps = Config.STEPS
    hires_fix = Config.HIRES_FIX

    # Map OpenAI model to AI Horde model
    horde_model = Config.get_horde_model(model)

    # If api_key is None, use ANON_API_KEY
    effective_api_key = api_key if api_key else ANON_API_KEY

    # Send image generation request to AI Horde with the appropriate API key
    status_response, job_id = simple_client.image_generate_request(
        ImageGenerateAsyncRequest(
            apikey=effective_api_key,  # Use the API key provided in the OpenAI request, or ANON_API_KEY if None
            params=ImageGenerationInputPayload(
                sampler_name=sampler_name,
                cfg_scale=cfg_scale,
                width=width,
                height=height,
                hires_fix=hires_fix,
                clip_skip=clip_skip,
                steps=steps,
                loras=loras,
            ),
            prompt=prompt,
            models=[horde_model]  # Use mapped AI Horde model
        )
    )

    if len(status_response.generations) == 0:
        raise Exception("No generations returned from the AI Horde API.")

    # Create directory to save images
    example_path = Path(Config.IMAGE_SAVE_PATH)
    example_path.mkdir(exist_ok=True, parents=True)

    images_data = []

    for idx, generation in enumerate(status_response.generations):
        image_name = f"{job_id}_generation_{idx + 1}.webp"
        image_path = example_path / image_name

        # Download and save the generated image before responding
        image_pil = simple_client.download_image_from_generation(generation)
        image_pil.save(image_path)

        # Return image as base64 encoded string if response_format is 'b64_json'
        if response_format == 'b64_json':
            with open(image_path, "rb") as image_file:
                b64_image = base64.b64encode(image_file.read()).decode('utf-8')
                images_data.append({"b64_json": b64_image})
        else:
            # Determine if SERVER_BASE_URL is provided to override the local server
            if Config.SERVER_BASE_URL:
                image_url = f"{Config.SERVER_BASE_URL}/{image_name}"
            else:
                image_url = f"http://{Config.HOST}:{Config.PORT}/images/{image_name}"
            images_data.append({"url": image_url})

    return {"data": images_data}
