from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import asyncio
import litellm
import os

app = FastAPI()

# Set your OpenAI API key
os.environ["OPENAI_API_KEY"] = ""  # ← keep your real key here

@app.get("/")
async def get():
    return HTMLResponse("Voice AI Assistant is running.")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    # Create persistent conversation history (outside loop!)
    conversation_history = [{
        "role": "system",
        "content": "You are a helpful Japanese language tutor. Ask what JLPT level the user is studying. Speak English at first, but nudge them toward using Japanese. Keep replies short and natural like a phone conversation."
    }]

    try:
        while True:
            data = await websocket.receive_text()
            print(f"📥 Received: {data}")  # ✅ log user message

            conversation_history.append({"role": "user", "content": data})

            print("🧠 Calling GPT-4-turbo with:", conversation_history)  # ✅ log full input to LLM

            response = litellm.completion(
                model="gpt-4o",
                messages=conversation_history,
                stream=False,
            )

            reply = response["choices"][0]["message"]["content"]
            print("💬 Reply:", reply)  # ✅ log model reply

            conversation_history.append({"role": "assistant", "content": reply})

            await websocket.send_text(reply)

    except Exception as e:
        error_msg = f"Error: {str(e)}"
        print(error_msg)
        try:
            await websocket.send_text(error_msg)
        except:
            pass
        await websocket.close()
