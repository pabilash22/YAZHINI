import yaml
import sounddevice as sd
import numpy as np
import whisper
import pyttsx3

# Load config
with open("config.yaml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

with open(config["system_prompt_file"], "r", encoding="utf-8") as f:
    system_prompt = f.read()

assistant_name = config["name"]
wake_word = config["wake_word"]

# Setup TTS
engine = pyttsx3.init()
engine.setProperty('rate', 170)

# Load Whisper model
model = whisper.load_model("base")

def speak(text):
    print(f"{assistant_name}: {text}")
    engine.say(text)
    engine.runAndWait()

def listen():
    print("Kekuren...")
    duration = 5  # 5 seconds listen
    fs = 16000
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()
    audio = np.squeeze(recording)
    result = model.transcribe(audio, language="ta")
    return result["text"].lower()

speak(f"Aaneittu irukken PTG. Naan {assistant_name}.")

while True:
    text = listen()
    print(f"Neenga: {text}")
    
    if wake_word in text:
        command = text.replace(wake_word, "").strip()
        
        if "enna neram" in command:
            from datetime import datetime
            time_now = datetime.now().strftime("%I:%M PM")
            speak(f"Ippo neram {time_now} sir.")
        
        elif "exit" in command or "stop" in command:
            speak("Sari sir, poren.")
            break
        
        else:
            speak("Sorry PTG, adha ippo seiya mudiyala.")