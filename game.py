import requests
from langchain.prompts import ChatPromptTemplate
from langchain.llms.base import LLM
from typing import Any

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
        
    def call_model(self, model_name, prompt):
        """Call local Ollama model"""
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


    def generate_scene(self, model_choice):
        """Generate game scene using specified model via direct prompt composition."""
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", (
                "You are a game master. Create an interactive scene based on:\n"
                "Player State: {state}\n"
                "Current Scene: {scene}\n"
                "Previous Action: {action}\n"
                "Respond with 2-3 paragraph scene description ending with 3 choices."
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
        return local_llm(prompt)

    def handle_choice(self, choice):
        """Process player choice using Qwen-VL model"""
        prompt = f"""Player choice: {choice}
        Update game state considering:
        - Current location: {self.player_state['location']}
        - Inventory: {self.player_state['inventory']}
        - Health: {self.player_state['health']}
        Respond with JSON containing:
        - state_update: dict
        - outcome_description: str
        """
        
        response = self.call_model(MODELS["qwen-vl"], prompt)
        return self.parse_response(response)

    def update_game_state(self, result):
        self.player_state.update(result.get("state_update", {}))
        self.last_action = result.get("outcome_description", "")

    def parse_response(self, response):
        try:
            import json
            return json.loads(response)
        except Exception as e:
            print(f"Error parsing response: {e}")
            return {}
        
    def game_loop(self):
        print("Welcome to AI Dungeon!\n")
        while self.player_state["health"] > 0:
            current_model = MODELS["deepseek"] if self.current_scene % 2 == 0 else MODELS["qwen-vl"]
            
            scene = self.generate_scene(current_model)
            print(f"\n{scene}\n")
            
            choice = input("Your choice (1-3, or 'quit'): ")
            if choice.lower() == 'quit':
                break
                
            result = self.handle_choice(choice)
            self.update_game_state(result)
            
            self.current_scene += 1

        print("\nGame Over! Thanks for playing!")

if __name__ == "__main__":
    game = GameEngine()
    game.game_loop()
