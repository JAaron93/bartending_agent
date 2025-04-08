from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from bartending_agent import BartendingAgent
import json

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

agent = BartendingAgent()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Receive audio data from Godot
            data = await websocket.receive_text()
            data = json.loads(data)
            
            # Process the order
            response = agent.process_order(data["text"])
            
            # Get voice response
            voice_response = agent.get_voice_response(response)
            
            # Send response back to Godot
            await websocket.send_json({
                "text": response,
                "voice": voice_response,
                "current_order": agent.current_order
            })
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await websocket.close()

@app.get("/menu")
async def get_menu():
    return agent.menu

@app.post("/reset")
async def reset_order():
    agent.reset_order()
    return {"status": "success"} 