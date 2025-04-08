# Bartending Agent Prototype

A prototype of a conversational bartending agent that uses Gemini 2.5, LangGraph, and Cartesia's voice API, integrated with Godot for a real-time interactive experience.

## Features

- Multi-turn conversational ordering system
- Voice generation using Cartesia's API
- Real-time WebSocket communication with Godot
- Menu management with 10 alcoholic beverages
- Speech-to-text integration
- Image display support in Godot

## Setup

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file in the root directory with your API keys:
```
GEMINI_API_KEY=your_gemini_api_key
CARTESIA_API_KEY=your_cartesia_api_key
```

3. Start the FastAPI server:
```bash
uvicorn api.server:app --reload
```

4. Open the Godot project and run the game.

## Project Structure

- `api/`: Contains the FastAPI server and bartending agent logic
  - `server.py`: FastAPI server with WebSocket endpoint
  - `bartending_agent.py`: Main agent logic with menu management
- `godot_scripts/`: Contains GDScript files for the Godot game
  - `bartender.gd`: Main game logic and API communication
  - `menu_display.gd`: Menu display and management

## Usage

1. Start the FastAPI server
2. Launch the Godot game
3. Use your microphone to place orders
4. The agent will respond with voice and text
5. Your order will be displayed in the game

## Menu Items

1. Old Fashioned - $12.00
2. Margarita - $10.00
3. Mojito - $11.00
4. Martini - $13.00
5. Whiskey Sour - $11.00
6. Gin and Tonic - $9.00
7. Manhattan - $12.00
8. Daiquiri - $10.00
9. Negroni - $11.00
10. Cosmopolitan - $12.00

## Notes

- The agent will reject orders for items not on the menu
- All responses are generated using Gemini 2.5
- Voice responses are generated using Cartesia's API
- Images can be added to the menu using the `display_image` function in `menu_display.gd` 