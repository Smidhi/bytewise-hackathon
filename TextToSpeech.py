import pygame
import asyncio
import edge_tts
import os
from dotenv import dotenv_values

# Load environment variables
env_vars = dotenv_values(".env")
AssistantVoice = env_vars.get("AssistantVoice", "en-CA-LiamNeural")  # default voice

if not AssistantVoice:
    raise ValueError("AssistantVoice is not set in .env or is empty.")

async def TextToAudioFile(text: str) -> None:
    file_path = r"Data\speech.mp3"

    # Ensure Data folder exists
    if not os.path.exists("Data"):
        os.makedirs("Data")

    if os.path.exists(file_path):
        os.remove(file_path)

    # Create TTS audio
    communicate = edge_tts.Communicate(text, AssistantVoice, pitch='+5Hz', rate='+13%')
    await communicate.save(file_path)

def TTS(Text, func=lambda r=None: True):
    try:
        # Run async TTS
        asyncio.run(TextToAudioFile(Text))

        # Initialize pygame mixer
        pygame.mixer.init()
        pygame.mixer.music.load(r"Data\speech.mp3")
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            if func() == False:
                break
            pygame.time.Clock().tick(10)

        return True

    except Exception as e:
        print(f"Error in TTS: {e}")
        return False

    finally:
        try:
            pygame.mixer.music.stop()
            pygame.mixer.quit()
        except Exception as e:
            # Only print if mixer was initialized
            pass

def TextToSpeech(Text, func=lambda r=None: True):
    TTS(Text, func)

if __name__ == "__main__":
    while True:
        text_input = input("Enter the text: ").strip()
        if text_input:
            TextToSpeech(text_input)
