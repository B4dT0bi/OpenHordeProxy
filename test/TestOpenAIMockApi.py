import os
import unittest

from horde_sdk import ANON_API_KEY
from loguru import logger
from openai import OpenAI


class TestOpenAIMockAPI(unittest.TestCase):

    def setUp(self):
        # Set the API key and base URL for OpenAI mock API (which proxies to AI Horde)
        self.llm_client = OpenAI(api_key=os.getenv("AI_HORDE_API_KEY", ANON_API_KEY),
                                 base_url="http://localhost:5000/v1")

    def test_chat_completions(self):
        # Define the prompt and parameters for the OpenAI API call
        response = self.llm_client.chat.completions.create(
            model="gpt-3.5-turbo",  # Assuming this maps to a model in AI Horde
            messages=[{"role": "user", "content": "What is the meaning of life?"}],
            max_tokens=50,
            temperature=0.7,
            top_p=0.9
        )

        logger.info(f"Response : {response}")

        # Assert that the response contains required fields
        self.assertTrue(response.id.startswith("cmpl"))

        # Check that the choices are returned and contain a valid message
        choices = response.choices
        self.assertTrue(len(choices) > 0)

        # Print the result for visual inspection
        print("Generated completion:", choices[0].message.content)


if __name__ == '__main__':
    unittest.main()
