# Smart-Assistant
Smart assistant that uses LLM as a brain and with ability to interact with other APIs [open weather etc..], and with the ability to control the system for opening apps, setting reminders etc..

Download Ollama

* Windows && Mac download from
    * URL: https://ollama.com/download
* For Linux
  ```
  curl -fsSL https://ollama.com/install.sh | sh
  ```

Insall dependencies

* download requirement.txt to install all needed packages
    ```
    pip install -r requirement.txt
    ```
* Or 
    ```
    pip install pyaudio pyttsx3 vosk SpeechRecognition
    ```

Vosk model

* URL: https://alphacephei.com/vosk/models
   ```
   Model	Size	Word error rate/Speed	Notes	License
   vosk-model-en-us-0.22-lgraph	128M	7.82 (librispeech) 8.20 (tedlium)	Big US English model with dynamic graph	Apache 2.0
   ```
