from typing import Dict, List, Optional
import google.generativeai as genai
from langgraph.graph import Graph, StateGraph
from langgraph.prebuilt import ToolNode
import os
import logging
from dotenv import load_dotenv
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
    before_sleep_log
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
if not load_dotenv():
    raise EnvironmentError("Could not load .env file. Please ensure it exists in the project root.")

class BartendingAgent:
    def __init__(self):
        # Check for required environment variables
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        if not self.gemini_api_key:
            raise EnvironmentError(
                "GEMINI_API_KEY not found in environment variables. "
                "Please add it to your .env file."
            )

        self.cartesia_api_key = os.getenv("CARTESIA_API_KEY")
        if not self.cartesia_api_key:
            raise EnvironmentError(
                "CARTESIA_API_KEY not found in environment variables. "
                "Please add it to your .env file."
            )
        
        try:
            genai.configure(api_key=self.gemini_api_key)
            self.model = genai.GenerativeModel('gemini-pro')
            logger.info("Successfully initialized Gemini model")
        except Exception as e:
            logger.error(f"Failed to initialize Gemini model: {str(e)}")
            raise RuntimeError(
                f"Failed to initialize Gemini model: {str(e)}. "
                "Please check if your GEMINI_API_KEY is valid."
            )
        
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
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((ConnectionError, TimeoutError, genai.types.GenerativeAIError)),
        before_sleep=before_sleep_log(logger, logging.WARNING),
        reraise=True
    )
    def process_order(self, text: str) -> str:
        try:
            # Add the user's input to conversation history
            self.conversation_history.append({"role": "user", "content": text})
            logger.info(f"Processing order: {text}")
            
            # Check if the order is in the menu
            order_found = False
            for item_id, item in self.menu.items():
                if item["name"].lower() in text.lower() or item_id in text:
                    self.current_order.append(item)
                    order_found = True
                    logger.info(f"Order found: {item['name']}")
                    break
            
            if not order_found:
                response = f"I'm sorry, I don't recognize that drink. {self.get_menu_text()}"
                logger.warning(f"Order not found in menu: {text}")
            else:
                response = f"Great choice! I've added {self.current_order[-1]['name']} to your order. Would you like anything else?"
            
            # Add the agent's response to conversation history
            self.conversation_history.append({"role": "assistant", "content": response})
            
            return response
        except Exception as e:
            logger.error(f"Error processing order: {str(e)}")
            return "I'm sorry, there was an error processing your order. Please try again."
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((ConnectionError, TimeoutError)),
        before_sleep=before_sleep_log(logger, logging.WARNING),
        reraise=True
    )
    def get_voice_response(self, text: str) -> str:
        try:
            if not self.cartesia_api_key:
                raise RuntimeError(
                    "Cannot generate voice response: CARTESIA_API_KEY is not set"
                )
            
            logger.info(f"Generating voice response for text: {text}")
            
            # This would be where you'd call the Cartesia API
            # For now, we'll just return the text
            return text
        except Exception as e:
            logger.error(f"Error generating voice response: {str(e)}")
            raise RuntimeError(
                f"Failed to generate voice response: {str(e)}. "
                "Please check your CARTESIA_API_KEY and network connection."
            )
    
    def reset_order(self):
        try:
            self.current_order = []
            self.conversation_history = []
            logger.info("Order and conversation history reset successfully")
        except Exception as e:
            logger.error(f"Error resetting order: {str(e)}")
            raise RuntimeError(f"Failed to reset order: {str(e)}") 