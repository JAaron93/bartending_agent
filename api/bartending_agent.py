from typing import Dict, List, Optional
import google.generativeai as genai
from langgraph.graph import Graph, StateGraph
from langgraph.prebuilt import ToolNode
import os
from dotenv import load_dotenv

load_dotenv()

class BartendingAgent:
    def __init__(self):
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        self.cartesia_api_key = os.getenv("CARTESIA_API_KEY")
        
        genai.configure(api_key=self.gemini_api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        
        self.menu = {
            "1": {"name": "Old Fashioned", "price": 12.00},
            "2": {"name": "Margarita", "price": 10.00},
            "3": {"name": "Mojito", "price": 11.00},
            "4": {"name": "Martini", "price": 13.00},
            "5": {"name": "Whiskey Sour", "price": 11.00},
            "6": {"name": "Gin and Tonic", "price": 9.00},
            "7": {"name": "Manhattan", "price": 12.00},
            "8": {"name": "Daiquiri", "price": 10.00},
            "9": {"name": "Negroni", "price": 11.00},
            "10": {"name": "Cosmopolitan", "price": 12.00}
        }
        
        self.current_order = []
        self.conversation_history = []
        
    def get_menu_text(self) -> str:
        menu_text = "Here's our menu:\n"
        for item_id, item in self.menu.items():
            menu_text += f"{item_id}. {item['name']} - ${item['price']:.2f}\n"
        return menu_text
    
    def process_order(self, text: str) -> str:
        # Add the user's input to conversation history
        self.conversation_history.append({"role": "user", "content": text})
        
        # Check if the order is in the menu
        order_found = False
        for item_id, item in self.menu.items():
            if item["name"].lower() in text.lower() or item_id in text:
                self.current_order.append(item)
                order_found = True
                break
        
        if not order_found:
            response = f"I'm sorry, I don't recognize that drink. {self.get_menu_text()}"
        else:
            response = f"Great choice! I've added {self.current_order[-1]['name']} to your order. Would you like anything else?"
        
        # Add the agent's response to conversation history
        self.conversation_history.append({"role": "assistant", "content": response})
        
        return response
    
    def get_voice_response(self, text: str) -> str:
        # This would be where you'd call the Cartesia API
        # For now, we'll just return the text
        return text
    
    def reset_order(self):
        self.current_order = []
        self.conversation_history = [] 