# AgentX: AI Agent with MQTT and LLM Integration

This project implements an AI agent that can communicate via MQTT and use either OpenAI's API or a local language model (LLM) to generate responses. The agent maintains conversation context for both overall and individual user interactions.

## Features

- MQTT communication for real-time messaging
- Integration with OpenAI API or local LLMs (e.g., using LM Studio)
- Short-term memory for maintaining conversation context
- Separate memory for overall conversation and individual users
- Configurable settings for easy customization

## Prerequisites

- Python 3.7+
- pip (Python package manager)

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/BenDixon89/agentX.git
   cd agentX
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Configuration

Edit the `config.py` file to set up your environment:

- MQTT settings (broker, port, topic)
- Agent settings (name, memory length)
- LLM API settings (API base URL, API key, model, system prompt, temperature)

### Using OpenAI API

To use the OpenAI API:

1. Sign up for an OpenAI account and obtain an API key
2. Set the following in `config.py`:
   ```python
   LLM_API_BASE = "https://api.openai.com/v1"
   LLM_API_KEY = "your-openai-api-key"
   LLM_MODEL = "gpt-3.5-turbo"  # or another available model
   ```

### Using a Local Model (e.g., LM Studio)

To use a local model with LM Studio:

1. Download and set up LM Studio (https://lmstudio.ai/)
2. Start the local server in LM Studio
3. Set the following in `config.py`:
   ```python
   LLM_API_BASE = "http://localhost:1234/v1"  # or the appropriate local URL
   LLM_API_KEY = "lm-studio"  # or any non-empty string
   LLM_MODEL = "your-local-model-name"
   ```

## Project Structure

- `main.py`: Entry point of the application
- `config.py`: Configuration settings
- `ai_agent/`:
  - `__init__.py`: Package initializer
  - `agent.py`: Main AI Agent class
  - `mqtt_client.py`: MQTT client implementation
  - `llm_model.py`: LLM integration (OpenAI or local)
- `.gitignore`: Specifies intentionally untracked files to ignore

## Usage

1. Ensure your MQTT broker is running and accessible
2. If using a local model, make sure it's running and available
3. Run the agent:
   ```
   python main.py
   ```

4. Send messages to the configured MQTT topic in the format:
   ```
   User_Name: Your message here
   ```

5. The agent will respond on the same MQTT topic with messages prefixed by its name:
   ```
   AI_Assistant: The agent's response
   ```

## How It Works

1. The agent subscribes to the configured MQTT topic
2. When a message is received, it extracts the user name and message content
3. The message is added to both the overall memory and the user-specific memory
4. A context is prepared, including:
   - The system prompt
   - Recent overall conversation history
   - A focus prompt for the specific user
   - Recent user-specific conversation history
5. This context is sent to the LLM (OpenAI or local) to generate a response
6. The response is added to the memories and sent back via MQTT

## Customization

- Adjust the `MEMORY_LENGTH` in `config.py` to change how many messages are remembered
- Modify the `LLM_SYSTEM_PROMPT` to change the AI's behavior or role
- Experiment with different `LLM_TEMPERATURE` values to adjust response randomness

## Troubleshooting

- Ensure all dependencies are installed
- Check that your MQTT broker is running and accessible
- Verify that your OpenAI API key is valid or your local LLM is running
- Check the console output for any error messages

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Docker Deployment

You can deploy AgentX using the pre-built Docker image from DockerHub or build your own image.

### Using the pre-built image from DockerHub

1. Pull the Docker image:
   ```
   docker pull bendixon89/agentx:latest
   ```

2. Run the Docker container:
   ```
   docker run -d --name agentx_container bendixon89/agentx:latest
   ```

   If you need to expose the MQTT port (1883) to your host machine, use:
   ```
   docker run -d -p 1883:1883 --name agentx_container bendixon89/agentx:latest
   ```

### Building your own Docker image

1. Ensure you have Docker installed on your system.

2. Build the Docker image:
   ```
   docker build -t agentx .
   ```

3. Run the Docker container:
   ```
   docker run -d --name agentx_container agentx
   ```

   If you need to expose the MQTT port (1883) to your host machine, use:
   ```
   docker run -d -p 1883:1883 --name agentx_container agentx
   ```

### Managing the Docker container

4. To view the logs of the running container:
   ```
   docker logs agentx_container
   ```

5. To stop the container:
   ```
   docker stop agentx_container
   ```

6. To remove the container:
   ```
   docker rm agentx_container
   ```

Note: Make sure your `config.py` file is properly configured before building or running the Docker image. If you're using a local LLM, you may need to adjust the `LLM_API_BASE` to point to your host machine's IP instead of `localhost`.