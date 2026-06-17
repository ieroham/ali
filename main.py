from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
import edge_tts, io

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST","GET","OPTIONS"],
    allow_headers=["*"],
)

@app.post("/tts")
async def tts(data: dict):
    text = data.get("text","سلام")
    voice = data.get("voice","fa-IR-FaridNeural")
    audio = io.BytesIO()
    communicate = edge_tts.Communicate(text, voice)
    async for chunk in communicate.stream():
        if chunk["type"]=="audio":
            audio.write(chunk["data"])
    return Response(audio.getvalue(), media_type="audio/mpeg")

@app.get("/")
def root(): return {"ok": True}
