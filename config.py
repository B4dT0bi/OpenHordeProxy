import os
from dotenv import load_dotenv
from loguru import logger

# Load environment variables from .env file
load_dotenv()


class Config:
    # Basic configuration
    AI_HORDE_API_KEY = os.getenv('AI_HORDE_API_KEY', 'ANON_API_KEY')
    HOST = os.getenv('HOST', '127.0.0.1')
    PORT = int(os.getenv('PORT', 5000))
    DEFAULT_HORDE_MODEL = os.getenv('DEFAULT_HORDE_MODEL', 'stable_diffusion')
    IMAGE_SAVE_PATH = os.getenv('IMAGE_SAVE_PATH', 'requested_images')

    # URL for serving images, either internally or externally
    SERVER_BASE_URL = os.getenv('SERVER_BASE_URL', f'http://{HOST}:{PORT}/images/')

    # Flag to enable or disable internal image server
    ENABLE_IMAGE_SERVER = os.getenv('ENABLE_IMAGE_SERVER', 'True').lower() == 'true'

    # LoRA configuration
    LORAS = os.getenv('LORAS', '')

    # Additional generation parameters
    SAMPLER_NAME = os.getenv('SAMPLER_NAME', 'k_euler')
    CFG_SCALE = int(os.getenv('CFG_SCALE', 7))
    CLIP_SKIP = int(os.getenv('CLIP_SKIP', 1))
    STEPS = int(os.getenv('STEPS', 30))
    HIRES_FIX = os.getenv('HIRES_FIX', 'False').lower() == 'true'

    # Anonymous access configuration
    ALLOW_ANONYMOUS_ACCESS = os.getenv('ALLOW_ANONYMOUS_ACCESS', 'False').lower() == 'true'

    # Method to map OpenAI text models to AI Horde models
    @staticmethod
    def get_horde_text_model(openai_model: str) -> str:
        # Mapping OpenAI models to AI Horde models based on environment variables.
        env_key = f'OPENAI_MODEL_MAP_{openai_model.replace("-", "_").replace(".", "_")}'
        return os.getenv(env_key, openai_model)

    # Method to map OpenAI image models to AI Horde models
    @staticmethod
    def get_horde_image_model(openai_model: str) -> str:
        # Mapping OpenAI models to AI Horde models based on environment variables.
        env_key = f'OPENAI_MODEL_MAP_{openai_model.replace("-", "_")}'
        return os.getenv(env_key, Config.DEFAULT_HORDE_MODEL)
