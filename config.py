MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_TOPIC = "ai_agent_x/messages"

# Agent settings
AGENT_NAME = "AI_Assistant"
MEMORY_LENGTH = 10  # Number of messages to remember

# LLM API settings
LLM_API_BASE = "http://localhost:1234/v1"
LLM_API_KEY = "lm-studio"
LLM_MODEL = "bartowski/gemma-2-9b-it-GGUF"
LLM_SYSTEM_PROMPT = "You are a helpful AI assistant."
LLM_TEMPERATURE = 0.7