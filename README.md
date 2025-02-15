# Command-Line Video Game

This is an interactive offline command-line video game built using local AI models through Ollama and managed with LangChain. It uses:
- **deepseek r1-7b** for story generation and world-building.
- **qwen 2.5** for processing image inputs to influence the narrative.
- **Whisper** (via Ollama) for voice transcription.
- A built-in **sidekick** for gameplay advice.

## Setup

1. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
2. Ensure that Ollama is installed and that the following models are available and configured locally:
    - `deepseek r1-7b`
    - `qwen 2.5`
    - `whisper`
3. Run the game:
    ```bash
    python main.py
    ```
