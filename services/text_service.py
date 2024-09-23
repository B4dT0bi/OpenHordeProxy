from horde_sdk import ANON_API_KEY
from horde_sdk.ai_horde_api.ai_horde_clients import AIHordeAPISimpleClient
from horde_sdk.ai_horde_api.apimodels import TextGenerateAsyncRequest, ModelGenerationInputKobold

from config import Config

# Initialize AI Horde Simple Client
simple_client = AIHordeAPISimpleClient()


# Text generation service function with timeout
def generate_text_service(prompt, model, api_key, max_completion_tokens=None, frequency_penalty=0, presence_penalty=0,
                          temperature=1, top_p=1, logit_bias=None, n=1, stop=None, timeout=60):
    # If api_key is None, use ANON_API_KEY
    effective_api_key = api_key if api_key else ANON_API_KEY

    # Map OpenAI model to AI Horde text model using the Config
    horde_model = Config.get_horde_text_model(model)

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

    # TODO : when AI Horde says Request is not possible we should stop trying and answer with error
    # Send text generation request to AI Horde with a timeout
    status_response, job_id = simple_client.text_generate_request(
        TextGenerateAsyncRequest(
            apikey=effective_api_key,  # Use the API key provided in the request, or ANON_API_KEY if None
            prompt=prompt,
            models=[horde_model],  # Use the mapped AI Horde model
            params=model_params
        ),
        timeout=timeout  # Set the timeout for the request
    )

    if len(status_response.generations) == 0:
        raise Exception("No generations returned from the AI Horde API.")

    # Get generated text
    return status_response.generations[0].text
