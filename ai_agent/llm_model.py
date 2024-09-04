from openai import OpenAI
from typing import List, Dict

class LLMModel:
    def __init__(self, api_base: str, api_key: str, model: str, system_prompt: str, temperature: float):
        self.client = OpenAI(base_url=api_base, api_key=api_key)
        self.model = model
        self.system_prompt = system_prompt
        self.temperature = temperature

    def generate_response(self, context: List[Dict[str, str]], user_message: str) -> str:
        messages = context + [{"role": "user", "content": user_message}]
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
        )
        return completion.choices[0].message.content