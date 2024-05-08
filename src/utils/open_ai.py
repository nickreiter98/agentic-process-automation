import os
from openai import OpenAI
from dotenv import load_dotenv

from typing import List, Dict

load_dotenv('.env')

class OpenAIConnection():
    def __init__(self):
        self.model = os.environ['OPENAI_MODEL']
        self.client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

    def request(self, messages: List[Dict[str, str]]) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages
        )
        return response.choices[0].message.content