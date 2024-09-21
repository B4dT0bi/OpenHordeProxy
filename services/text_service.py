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

    # Send text generation request to AI Horde
    status_response, job_id = simple_client.text_generate_request(
        TextGenerateAsyncRequest(
            apikey=effective_api_key,  # Use the API key provided in the request, or ANON_API_KEY if None
            prompt=prompt,
            params=ModelGenerationInputKobold(
                max_tokens=max_completion_tokens,
                temperature=temperature,
                top_p=top_p,
                n=n,
                logit_bias=logit_bias,
                stop=stop,
                frequency_penalty=frequency_penalty,
                presence_penalty=presence_penalty
            ),
            models=[model]  # Use the specified model
        )
    )

    if len(status_response.generations) == 0:
        raise Exception("No generations returned from the AI Horde API.")

    # Prepare the response with generated text
    generated_texts = [{"text": generation.text} for generation in status_response.generations]

    return {"choices": generated_texts}
