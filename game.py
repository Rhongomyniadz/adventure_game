import requests
import time
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import LLMChain

# Configuration
OLLAMA_BASE_URL = "http://localhost:11434/api/generate"
MODELS = {
    "deepseek": "deepseek-r1:7b",
    "qwen-vl": "bsahane/Qwen2.5-VL-7B-Instruct:Q4_K_M_benxh"
}

class GameEngine:
    def __init__(self):
        self.current_scene = 0
        self.player_state = {
            "health": 100,
            "inventory": [],
            "location": "starting_point"
        }
        
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
            return response.json()["response"]
        except Exception as e:
            print(f"Error calling model: {e}")
            return ""

    def generate_scene(self, model_choice):
        """Generate game scene using specified model"""
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", """You are a game master. Create an interactive scene based on:
            Player State: {state}
            Current Scene: {scene}
            Previous Action: {action}
            Respond with 2-3 paragraph scene description ending with 3 choices."""),
            ("human", "{input}")
        ])
        
        chain = LLMChain.from_string(
            llm=lambda text: self.call_model(model_choice, text),
            prompt=prompt_template
        )
        
        return chain.invoke({
            "state": self.player_state,
            "scene": self.current_scene,
            "action": self.last_action,
            "input": "Generate next scene"
        })

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

    def game_loop(self):
        print("Welcome to AI Dungeon!\n")
        while self.player_state["health"] > 0:
            # Alternate between DeepSeek and Qwen-VL
            current_model = MODELS["deepseek"] if self.current_scene % 2 == 0 else MODELS["qwen-vl"]
            
            # Generate scene
            scene = self.generate_scene(current_model)
            print(f"\n{scene}\n")
            
            # Get player input
            choice = input("Your choice (1-3, or 'quit'): ")
            if choice.lower() == 'quit':
                break
                
            # Process choice
            result = self.handle_choice(choice)
            self.update_game_state(result)
            
            self.current_scene += 1

        print("\nGame Over! Thanks for playing!")

if __name__ == "__main__":
    game = GameEngine()
    game.game_loop()
