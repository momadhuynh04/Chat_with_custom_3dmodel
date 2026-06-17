import modal
from fastapi import FastAPI, Request
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("modal-tts")

app = modal.App("sillytavern-voice-engine")
web_app = FastAPI()

web_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Xây dựng image: đặt add_local_file CUỐI CÙNG với copy=True
voice_env = (
    modal.Image.debian_slim(python_version="3.10")
    .apt_install("ffmpeg", "libsndfile1")
    .pip_install(
        "torch==2.3.0",
        "torchaudio==2.3.0",
        "transformers==4.38.2",
        "TTS",
        "fastapi[standard]",
        "soundfile"
    )
    .env({"COQUI_TOS_AGREED": "1"})
    .add_local_file("sample.wav", remote_path="/root/sample.wav", copy=True)
)

@app.cls(image=voice_env, gpu="T4", scaledown_window=15)
class VoiceAPI:
    @modal.enter()
    def load_model(self):
        from TTS.api import TTS
        logger.info("Loading XTTSv2 model...")
        self.tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to("cuda")
        logger.info("Model loaded successfully")

    @modal.method()
    def generate_voice(self, text: str, language: str = "en") -> bytes:
        out_path = "/root/output.wav"
        self.tts.tts_to_file(
            text=text,
            speaker_wav="/root/sample.wav",
            language=language,
            file_path=out_path
        )
        with open(out_path, "rb") as f:
            return f.read()

@web_app.get("/v1/models")
async def get_models():
    return {
        "object": "list",
        "data": [{"id": "xtts-chelsea", "object": "model", "created": 1686935002, "owned_by": "openai"}]
    }

@web_app.post("/v1/audio/speech")
async def text_to_speech(request: Request):
    data = await request.json()
    text = data.get("input", "")
    if not text:
        return Response(content="Empty text", status_code=400)
    logger.info(f"Generating TTS for: {text[:50]}...")
    # Dùng async call
    audio_bytes = await VoiceAPI().generate_voice.remote.aio(text, language="en")
    return Response(content=audio_bytes, media_type="audio/wav")

@app.function(image=voice_env, gpu="T4", scaledown_window=15)
@modal.asgi_app()
def fastapi_app():
    return web_app