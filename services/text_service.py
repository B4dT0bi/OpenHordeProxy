import time
import uuid

from config import Config
from horde_sdk.ai_horde_api.apimodels import TextGenerateAsyncRequest, ModelGenerationInputKobold
from horde_sdk.ai_horde_api.ai_horde_clients import AIHordeAPISimpleClient
from horde_sdk import ANON_API_KEY

# Initialize AI Horde Simple Client
simple_client = AIHordeAPISimpleClient()


# Text generation service function
def generate_text_service(messages, model, api_key, max_completion_tokens=None, frequency_penalty=0, presence_penalty=0,
                          temperature=1, top_p=1, logit_bias=None, n=1, stop=None):
    # If api_key is None, use ANON_API_KEY
    effective_api_key = api_key if api_key else ANON_API_KEY

    # Build prompt from conversation messages
    prompt = "".join([msg['content'] for msg in messages])

    # Prepare parameters for the generation request
    model_params = ModelGenerationInputKobold(
        max_context_length=1024,  # Default max context length
        max_length=max_completion_tokens if max_completion_tokens else 80,
        temperature=temperature,
        top_p=top_p,
        n=n,
        stop_sequence=stop if stop else [],
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty
    )

    # Send text generation request to AI Horde
    status_response, job_id = simple_client.text_generate_request(
        TextGenerateAsyncRequest(
            apikey=effective_api_key,  # Use the API key provided in the request, or ANON_API_KEY if None
            prompt=prompt,
            models=[model],  # Use the specified model
            params=model_params
        )
    )

    if len(status_response.generations) == 0:
        raise Exception("No generations returned from the AI Horde API.")

    # Get generated text
    generated_text = status_response.generations[0].text

    # Create a response following the required structure
    response = {
        "id": f"chatcmpl-{uuid.uuid4()}",
        "object": "chat.completion",
        "created": int(time.time()),
        "model": model,
        "system_fingerprint": f"fp_{uuid.uuid4().hex[:12]}",
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": generated_text
                },
                "logprobs": None,
                "finish_reason": "stop"
            }
        ],
        "usage": {
            "prompt_tokens": len(prompt.split()),
            "completion_tokens": len(generated_text.split()),
            "total_tokens": len(prompt.split()) + len(generated_text.split()),
            "completion_tokens_details": {
                "reasoning_tokens": 0
            }
        }
    }

    return response
