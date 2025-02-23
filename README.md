# Offline Command-Line AI Adventure Game

This repository contains a text-based adventure game that runs **entirely offline** using:

1. **[Ollama](https://github.com/jmorganca/ollama)** to host local AI models (e.g., DeepSeek, Qwen-VL, and Whisper).
2. **[LangChain](https://github.com/hwchase17/langchain)** for conversation management, prompt orchestration, and memory.
3. **Whisper** for optional local speech-to-text input.
4. A **sidekick** (an AI-driven advisor) to offer hints and next-step guidance.
5. An **image-processing** hook with Qwen-VL to influence the story based on images you provide.

---

## Features

- **Local AI Models**: No external API calls; your data stays on your machine.
- **Speech Input** (Optional): Use Whisper locally to transcribe voice commands into text.
- **Sidekick**: Ask for hints or suggestions on what to do next.
- **Image Influence**: Supply images (e.g., `.jpg` or `.png`) to Qwen-VL, and watch the storyline adapt.
- **LangChain Memory**: Tracks the conversation and game state so your story remains consistent.

---

## Prerequisites

1. **Python 3.9+**
2. **[Ollama](https://github.com/jmorganca/ollama) installed**
3. **Local Models**:
   - DeepSeek (for world-building and story generation)
   - Qwen-VL (for image-based story influences)
   - Whisper (for speech transcription, if using voice input)
4. **Python Dependencies** (see [`requirements.txt`](./requirements.txt))

---

## Installation

1. **Clone the repository**:
   ```bash
   git clone <THE-REPO-URL>
   cd adventrue_game

2. **Install Python dependencies**:
    ```bash
    pip install -r requirements.txt

3. **Install and configure Ollama**:
    Follow Ollama’s instructions to install locally.
    Download the required models (for example, DeepSeek, Qwen-VL, and Whisper) using:
    ```bash
    ollama pull <MODEL-NAME>

## Usage

1. **Run the Game**:
   ```bash
   python3 game.py
