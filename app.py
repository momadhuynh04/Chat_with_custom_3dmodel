import modal
from fastapi import FastAPI, Request
import base64
import io

LORA_URL = "https://civitai.com/api/download/models/491767"
LORA_FILE = "character.safetensors"

app = modal.App("sillytavern-pony-engine")
web_app = FastAPI()

image_env = (
    modal.Image.debian_slim()
    .apt_install("wget")
    .pip_install(
        "torch", "torchvision", "torchaudio", 
        "transformers", "accelerate", "diffusers", 
        "safetensors", "fastapi[standard]", "peft"
    )
    .run_commands(f"wget -qO /root/{LORA_FILE} '{LORA_URL}'") 
)

@app.cls(image=image_env, gpu="A10G", scaledown_window=10)
class VisionAPI:
    @modal.enter()
    def load_model(self):
        import torch
        from diffusers import AutoPipelineForText2Image
        self.pipe = AutoPipelineForText2Image.from_pretrained(
            "Bakanayatsu/Pony-Diffusion-V6-XL-for-Anime",
            torch_dtype=torch.float16,
            use_safetensors=True
        ).to("cuda")
        self.pipe.load_lora_weights("/root", weight_name=LORA_FILE)

    @modal.method()
    def generate(self, prompt: str, negative_prompt: str):
        out = self.pipe(
            prompt=prompt,
            negative_prompt=negative_prompt,
            num_inference_steps=25,
            guidance_scale=7.0,
            width=832,
            height=1216
        )
        img = out.images[0]
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        return base64.b64encode(buf.getvalue()).decode("utf-8")

@web_app.get("/sdapi/v1/options")
async def get_options(): return {"sd_model_checkpoint": "pony-diffusion-v6-xl"}

@web_app.get("/sdapi/v1/sd-models")
async def get_models(): return [{"title": "pony-diffusion-v6-xl"}]

@web_app.get("/sdapi/v1/sd-vae")
async def get_vae(): return [{"model_name": "None"}]

@web_app.get("/sdapi/v1/samplers")
async def get_samplers(): return [{"name": "Euler a"}]

@web_app.post("/sdapi/v1/txt2img")
async def txt2img(request: Request):
    data = await request.json()
    prompt = data.get("prompt", "")
    negative_prompt = data.get("negative_prompt", "")
    img_b64 = VisionAPI().generate.remote(prompt, negative_prompt)
    return {"images": [img_b64]}

@app.function(image=image_env, gpu="A10G", scaledown_window=15)
@modal.asgi_app()
def fastapi_app():
    return web_app