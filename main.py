from typing import Any
from ai_agent import AIAgent
from ai_agent.mqtt_client import MQTTClient
from ai_agent.llm_model import LLMModel
from config import (
    MQTT_BROKER, MQTT_PORT, MQTT_TOPIC, AGENT_NAME,
    LLM_API_BASE, LLM_API_KEY, LLM_MODEL, LLM_SYSTEM_PROMPT, LLM_TEMPERATURE,
    MEMORY_LENGTH
)

def main():
    mqtt_client = MQTTClient(MQTT_BROKER, MQTT_PORT, MQTT_TOPIC)
    llm_model = LLMModel(LLM_API_BASE, LLM_API_KEY, LLM_MODEL, LLM_SYSTEM_PROMPT, LLM_TEMPERATURE)
    agent = AIAgent(mqtt_client, llm_model, AGENT_NAME, MEMORY_LENGTH)

    # Define the custom on_message handler
    def on_message(client: Any, userdata: Any, msg: Any) -> None:
        message = msg.payload.decode()
        
        # Check if the message is from the agent itself
        if not message.startswith(f"{AGENT_NAME}:"):
            print(f"Received message: {message}")
            response = agent.process_message(message)
            agent.send_message(response)

    # Set the custom on_message handler
    mqtt_client.set_on_message_callback(on_message)

    agent.run()

if __name__ == "__main__":
    main()