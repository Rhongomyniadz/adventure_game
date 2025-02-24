import requests
import re
import base64
import whisper
import json
from langchain.prompts import ChatPromptTemplate
from langchain.llms.base import LLM
from typing import Any
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

OLLAMA_BASE_URL = "http://localhost:11434/api/generate"
MODELS = {
    "deepseek": "deepseek-r1:latest",
    "qwen-vl": "bsahane/Qwen2.5-VL-7B-Instruct:Q4_K_M_benxh"
}

class LocalOllamaLLM(LLM):
    model_name: str
    game_engine: Any

    @property
    def _llm_type(self) -> str:
        return "local_ollama"

    def _call(self, prompt: str, stop=None) -> str:
        return self.game_engine.call_model(self.model_name, prompt)

    @property
    def _identifying_params(self) -> dict:
        return {"model_name": self.model_name}
    
class GameEngine:
    def __init__(self):
        self.current_scene = 0
        self.player_state = {
            "health": 100,
            "inventory": [],
            "location": "starting_point"
        }
        self.last_action = ""
        self.whisper_model = whisper.load_model("base")
        
    def call_model(self, model_name, prompt):
        """Call a local Ollama model for text-based interactions."""
        try:
            response = requests.post(
                OLLAMA_BASE_URL,
                json={
                    "model": model_name,
                    "prompt": prompt,
                    "stream": False,
                    "options": {"temperature": 0.7}
                }
            )
            response_json = response.json()
            if "response" in response_json:
                return response_json["response"]
            else:
                print("Unexpected response format:", response_json)
                return ""
        except Exception as e:
            print(f"Error calling model: {e}")
            return ""

    def transcribe_voice(self, file_path):
        """Transcribe voice input using the Whisper Python package."""
        try:
            result = self.whisper_model.transcribe(file_path)
            return result["text"]
        except Exception as e:
            print(f"Error transcribing voice: {e}")
            return ""

    def process_image(self, file_path):
        """Process image input using Qwen-VL to introduce a new story element."""
        try:
            with open(file_path, "rb") as f:
                image_data = f.read()
            image_base64 = base64.b64encode(image_data).decode("utf-8")
            response = requests.post(
                OLLAMA_BASE_URL,
                json={
                    "model": MODELS["qwen-vl"],
                    "prompt": image_base64,
                    "stream": False,
                    "options": {"temperature": 0.7}
                }
            )
            response_json = response.json()
            if "response" in response_json:
                return response_json["response"]
            else:
                print("Unexpected response format from image processing:", response_json)
                return ""
        except Exception as e:
            print(f"Error processing image: {e}")
            return ""
        
    def generate_scene(self, model_choice):
        """Generate a game scene using the specified model."""
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", (
                "You are a game master. Create an interactive scene based on:\n"
                "Player State: {state}\n"
                "Current Scene: {scene}\n"
                "Previous Action: {action}\n"
                "Respond with 2-3 paragraph scene description ending with 3 choices.\n"
                "Do not include any internal chain-of-thought or meta commentary in your output."
            )),
            ("human", "{input}")
        ])
        
        prompt = prompt_template.format(
            state=self.player_state,
            scene=self.current_scene,
            action=self.last_action,
            input="Generate next scene"
        )
        
        local_llm = LocalOllamaLLM(model_name=model_choice, game_engine=self)
        scene_output = local_llm.invoke(prompt)
        scene_output = re.sub(r'<think>.*?</think>', '', scene_output, flags=re.DOTALL)
        return scene_output.strip()



    def handle_choice(self, choice):
        """Process the player's choice using DeepSeek."""
        prompt = f"""Player choice: {choice}
        Update game state considering:
        - Current location: {self.player_state['location']}
        - Inventory: {self.player_state['inventory']}
        - Health: {self.player_state['health']}
        
        Respond ONLY with a valid JSON object using this EXACT format:
        {{
            "state_update": {{
                "health": <number>,
                "inventory": <array>,
                "location": <string>
            }},
            "outcome_description": "<string>"
        }}
        No other text or formatting allowed.
        """
        response = self.call_model(MODELS["deepseek"], prompt)
        return self.parse_response(response)

    def update_game_state(self, result):
        self.player_state.update(result.get("state_update", {}))
        self.last_action = result.get("outcome_description", "")

    def parse_response(self, response):
        try:
            json_str = re.search(r'\{.*\}', response, re.DOTALL).group()
            return json.loads(json_str)
        except Exception as e:
            print(f"Invalid response format: {response}")
            return {
                "state_update": {},
                "outcome_description": "The game stumbles for a moment..."
            }
        
    def game_loop(self):
        print("Welcome to AI Dungeon!\n")
        while self.player_state["health"] > 0:
            scene = self.generate_scene(MODELS["deepseek"])
            print(f"\n{scene}\n")
            
            input_type = input("Enter input type (text/voice/image, or 'quit' to exit): ").strip().lower()
            if input_type == "quit":
                break
            
            if input_type == "voice":
                file_path = input("Enter path to audio file: ").strip()
                user_input = self.transcribe_voice(file_path)
                print(f"Transcribed voice input: {user_input}")
            elif input_type == "image":
                file_path = input("Enter path to image file: ").strip()
                user_input = self.process_image(file_path)
                print(f"Processed image input: {user_input}")
            else:
                user_input = input("Your action: ").strip()
            
            result = self.handle_choice(user_input)
            self.update_game_state(result)
            self.current_scene += 1

        print("\nGame Over! Thanks for playing!")

if __name__ == "__main__":
    game = GameEngine()
    game.game_loop()
