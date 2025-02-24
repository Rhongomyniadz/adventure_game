# Offline Command-Line AI Adventure Game

This repository contains a text-based adventure game that runs **entirely offline** using:

1. **[Ollama](https://github.com/jmorganca/ollama)** to host local AI models (DeepSeek and Qwen-VL)
2. **[LangChain](https://github.com/hwchase17/langchain)** for conversation management and prompt orchestration
3. **OpenAI's Whisper** (local installation) for speech-to-text input
4. **Qwen-VL** for image-based story influences
5. **JSON State Management** for consistent game progression

---

## Features

- **Local AI Models**: No external API calls; your data stays on your machine
- **Multi-modal Input**:
  - Text commands
  - Voice input via Whisper
  - Image inputs that influence the story
- **Dynamic State Tracking**:
  - Health system
  - Inventory management
  - Location-based progression
- **Adaptive Storytelling**: AI-generated scenes with 3 choices per interaction

---

## Prerequisites

1. **Python 3.9+**
2. **[Ollama](https://github.com/jmorganca/ollama) installed and running**
3. **Required Models**:
   - DeepSeek: `ollama pull deepseek-r1:latest`
   - Qwen-VL: `ollama pull bsahane/Qwen2.5-VL-7B-Instruct:Q4_K_M_benxh`
4. **System Resources**:
   - 8GB+ RAM recommended
   - 4GB+ VRAM for image processing

---

## Installation

1. **Clone the repository**:
   ```bash
   git clone <THE-REPO-URL>
   cd adventure_game

2. **Install Python dependencies**:
    ```bash
    pip install -r requirements.txt

3. **Install and configure Ollama**:
    Follow Ollama’s instructions to install locally.
    Download the required models (for example, DeepSeek, Qwen-VL, and Whisper) using:
    ```bash
    ollama pull deepseek-r1:latest
    ollama pull bsahane/Qwen2.5-VL-7B-Instruct:Q4_K_M_benxh

## Usage

1. **Run the Game**:
   ```bash
   python3 game.py

2. **Gameplay options**:
- Regular text input: Type commands directly
- Voice input: Provide path to .wav file when prompted
- Image input: Provide path to .jpg/.png to influence story

3. **Game flow**:
- Each scene presents 3 choices
- Input format validation built-in
- Health system affects story outcomes
- Inventory items unlock special interactions
