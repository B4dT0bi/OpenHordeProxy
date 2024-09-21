import asyncio
import sys

import aiohttp
from horde_sdk.ai_horde_api.ai_horde_clients import AIHordeAPIAsyncClientSession
from horde_sdk.ai_horde_api.apimodels import HordeStatusModelsAllRequest, HordeStatusModelsAllResponse

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


async def get_models(model_type="text"):
    async with aiohttp.ClientSession() as aiohttp_session:
        async with AIHordeAPIAsyncClientSession(aiohttp_session=aiohttp_session) as client:
            request = HordeStatusModelsAllRequest(type=model_type)
            response = await client.submit_request(
                request,
                expected_response_type=HordeStatusModelsAllResponse,
            )

            if isinstance(response, HordeStatusModelsAllResponse):
                # Map the response to OpenAI model format
                return [
                    {
                        "id": model.name,
                        "created": 1686935002,  # fixed value as AI Horde doesnt have any created timestamp
                        "object": "model",
                        "owned_by": "AI Horde"  # Static value since it's owned by AI Horde
                    }
                    for model in response.root
                ]
            else:
                raise ValueError("Failed to fetch models from AI Horde.")
