from openai import OpenAI
import os

SYS_MESSAGE = """You are modeling a process workflow. You are given a textual description of a process workflow. 
The aim is to return the workflow description as a directional graph.
Every described function from the text is mapped to a node. Keep the context of the function and include rather more information for one task.
The graph must be returned in a JSON representation. The key is the source node and the values are the target nodes stored in a list.
I give you an example.
I would like to know how warm it is in Berlin. Put the information in an email and send it to Nick Reiter.
{
    "weather in Berlin": ["write an email"]
    "write an email": ["send the email"]
}
Only provide the JSON
"""

class Agent():
    def __init__(
        self,
        model: str = 'gpt-4-0613',
    ):
        self.model = model
        self.chat_history = [{'role': 'system', 'content': SYS_MESSAGE}]
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    def ask(self, query:str) -> str:
        self.chat_history.append({'role': 'user', 'content': query})
        res = self.client.chat.completions.create(
                model=self.model,
                messages=self.chat_history
            )
        res_content = res.choices[0].message.content
        self.chat_history.append({'role': 'system', 'content': res_content})
        return res_content