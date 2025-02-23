import speech_recognition as sr
import pyttsx3
import subprocess
import time
import sys

# Initialize the recognizer and text-to-speech engine
recognizer = sr.Recognizer()
tts_engine = pyttsx3.init()

# Function to convert text to speech
def speak(text):
    tts_engine.say(text)
    tts_engine.runAndWait()

# Function to listen for audio input and convert it to text
def listen():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio).lower()
            print(f"User said: {command}")
            return command
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
            return ""
        except sr.RequestError:
            print("Could not request results; check your network connection.")
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
    active = False
    while True:
        if not active:
            print("Waiting for activation phrase 'Jarvis'...")
            command = listen()
            if "jarvis" in command:
                active = True
                speak("How can I assist you?")
            elif "stop the app" in command:
                speak("Shutting down the application.")
                sys.exit()
            
        else:
            command = listen()
            if "stop talking" in command:
                speak("Deactivating voice assistant.")
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
