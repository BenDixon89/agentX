from .mqtt_client import MQTTClient
from .llm_model import LLMModel
from collections import deque
from typing import Dict, List

class AIAgent:
    def __init__(self, mqtt_client: MQTTClient, llm_model: LLMModel, agent_name: str, memory_length: int = 10):
        self.mqtt_client = mqtt_client
        self.llm_model = llm_model
        self.agent_name = agent_name
        self.memory_length = memory_length
        self.overall_memory: deque = deque(maxlen=memory_length)
        self.user_memories: Dict[str, deque] = {}

    def process_message(self, message: str) -> str:
        # Extract user name and message content
        user_name, user_message = message.split(": ", 1)
        print(f"User message: {user_message}")

        # Update memories
        self.overall_memory.append({"role": "user", "content": f"{user_name}: {user_message}"})
        if user_name not in self.user_memories:
            self.user_memories[user_name] = deque(maxlen=self.memory_length)
        self.user_memories[user_name].append({"role": "user", "content": user_message})

        # Prepare context for LLM
        context = self._prepare_context(user_name)

        # Generate response
        response = self.llm_model.generate_response(context, user_message)

        # Update memories with the agent's response
        self.overall_memory.append({"role": "assistant", "content": response})
        self.user_memories[user_name].append({"role": "assistant", "content": response})

        return f"{self.agent_name}: {response}"

    def _prepare_context(self, user_name: str) -> List[Dict[str, str]]:
        context = [{"role": "system", "content": self.llm_model.system_prompt}]
        context.extend(list(self.overall_memory))
        context.append({"role": "system", "content": f"Now focusing on conversation with user: {user_name}"})
        context.extend(list(self.user_memories[user_name]))
        return context

    def send_message(self, message: str):
        self.mqtt_client.publish(message)

    def run(self):
        self.mqtt_client.connect()
        self.mqtt_client.loop_forever()