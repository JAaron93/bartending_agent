from fastapi import FastAPI, Response, status
import uvicorn
# Optional: You might import your agent later
# from api.bartending_agent import BartendingAgent

# Create the FastAPI application instance
app = FastAPI(title="Bartending Agent API")

# Optional: Instantiate your agent if needed globally
# agent = BartendingAgent()

# Define a simple root endpoint for testing
@app.get("/")
async def read_root():
    return {"message": "Welcome to the Bartending Agent API!"}

# Add other endpoints here later to interact with your agent
# For example:
# @app.post("/order")
# async def place_order(user_input: str):
#     response = agent.process_order(user_input)
#     return {"response": response}

@app.get('/favicon.ico', include_in_schema=False)
async def favicon_no_content():
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# This block allows running directly with `python main.py` for simple testing
# Uvicorn is preferred for development (--reload) and production
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000) 