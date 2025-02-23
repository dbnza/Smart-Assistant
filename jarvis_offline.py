import os
import sys
import pyaudio
import json
import pyttsx3
import subprocess
from vosk import Model, KaldiRecognizer

# Initialize the text-to-speech engine
tts_engine = pyttsx3.init()

# Function to convert text to speech
def speak(text):
    tts_engine.say(text)
    tts_engine.runAndWait()

# Function to listen for audio input and convert it to text using Vosk
def listen(model_path, sample_rate=16000, device_index=None):
    """
    Recognize speech from the microphone using the Vosk model.

    Parameters:
    - model_path (str): Path to the Vosk model directory.
    - sample_rate (int): Sampling rate for audio capture. Default is 16000 Hz.
    - device_index (int or None): Device index for the microphone. Default is None (uses default device).

    Returns:
    - str: The recognized text from the speech input.
    """
    # Check if the model path exists
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model path '{model_path}' does not exist. Please check the path and try again.")

    # Load the Vosk model
    model = Model(model_path)
    recognizer = KaldiRecognizer(model, sample_rate)

    # Initialize PyAudio
    p = pyaudio.PyAudio()

    # Open the microphone stream
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=sample_rate,
                    input=True,
                    frames_per_buffer=8000,
                    input_device_index=device_index)
    stream.start_stream()

    print("Listening...")

    try:
        while True:
            data = stream.read(4000, exception_on_overflow=False)
            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()
                result_dict = json.loads(result)
                command = result_dict.get('text', '').lower()
                if command:
                    print(f"User said: {command}")
                    if "stop talking" in command:
                        print("Deactivating voice assistant.")
                        speak("Deactivating voice assistant.")
                        break
                    return command
    except KeyboardInterrupt:
        print("\nTerminated by user")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()
    return ""

# Function to interact with Ollama's tinydolphin model
def query_ollama(prompt):
    try:
        # Run the Ollama model with the user's prompt
        result = subprocess.run(
            ["ollama", "run", "tinydolphin", prompt],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            print(f"Error: {result.stderr}")
            return "I'm sorry, I couldn't process that."
    except Exception as e:
        print(f"An error occurred: {e}")
        return "I'm sorry, an error occurred."

# Main function to run the assistant
def run_assistant():
    model_path = "end paste hine" 
    active = False
    while True:
        if not active:
            print("Waiting for activation phrase 'Jarvis'...")
            command = listen(model_path)
            if "jarvis" in command:
                active = True
                speak("How can I assist you?")
            elif "stop the app" in command:
                speak("Shutting down the application.")
                sys.exit()
        else:
            command = listen(model_path)
            if "stop talking" in command:
                active = False
            elif command:
                response = query_ollama(command)
                speak(response)
            elif "stop the app" in command:
                speak("Shutting down the application.")
                sys.exit()

# Start the assistant
if __name__ == "__main__":
    run_assistant()
