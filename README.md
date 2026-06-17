# Chat with 3d model 

roleplay chat platform run local that allow run 3D AI VTuber characters directly on your computer. The system combines AI brain (LLM), natural speech (TTS), speech recognition (STT), and real-time lip-sync on the Unity 3D platform.

i use tavern and is a little bit too much so i vibe this this waay simple configuration and 3d chat

havnt got alot of resources so i bring up wwhat i have test llm: openrouter, ollma, tts:openrouter,azure, and slot for my modal app (app_voice.py), kokoro(build in) ,img: automatic1111,openrouter, polination(free clound service)

## Download

---

## 🚀 User Guide 

The project is highly automated. You only need to follow these two steps:

### First Time (System Setup)

1. Double-click the **`setup.bat`** file.

2. Wait for the script to automatically check and install all necessary environments (Node.js, Deno, FFmpeg) and compile the console interface (WebUI).

*(Note: If your computer requests permission to install the software, press "Y" to agree.)*

### Every Time After (Running the Software)
1. Double-click the **`start.bat` file.

2. This file will automatically start the AI ​​server and open your web browser (address `http://localhost:8001`).

3. Open the **Unity** app (LiveTemplatev2) and press Play. That's it!

---

## 🛠️ Available Features

* **Full Automation:** Double-click the `.bat` file to set up and run. Deno automatically handles both the server and the web control panel.

* **Diverse Chat Models (LLM):** Supports plugging in APIs from OpenRouter, OpenAI, Gemini, or custom servers.

* **Voice Modeling (TTS):** Kokoro, OpenRouter (Grok), Azure... The system automatically converts audio formats accurately for Unity using FFmpeg.

* **Voice Chat (STT):** Ultra-fast voice recognition via Whisper or Groq.

* **Lorebooks (AI Memory):** Automatically injects contextual information into the AI ​​brain whenever the user mentions a keyword.

* **3D Synchronization:** Directly plug `.vrm` character files into Unity; the character will lip-sync and move based on the voice.

**PreView**

[3d ui preview](https://youtu.be/_TRZaD-d7ow)

<img width="1864" height="706" alt="image" src="https://github.com/user-attachments/assets/acffd9e5-4014-4889-a893-86ef6d176cd9" />

---


## 🔮 Future Updates

The project is still under development and refinement. Below are the features expected in the future:

* Improved auto-emotes for 3D avatars based on the emotions of the spoken words.

* Supports integrated live chat reading directly from YouTube/Twitch(not sure cus my agent plan this not me).

* Added Vision feature (showing images to AI for analysis).

* Expanded spatial sound and environmental effects in Unity.

* Packaged everything into a single `.exe` installation file (Standalone App).

* and other bullshit if someone request
