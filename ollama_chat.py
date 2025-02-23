import subprocess
conversation_history = []
def ollama_chat(model, user_input):
    global conversation_history
    conversation_history.append(f"User: {user_input}")
    prompt = "\n".join(conversation_history)
    try:
        result = subprocess.run(
            ["ollama", "run", model, prompt],
            capture_output=True,
            text=True,
            check=True
        )pip install polyglot

        bot_response = result.stdout.strip()
        conversation_history.append(f"Assistant: {bot_response}")
        print(f"J.A.R.V.I.S.: {bot_response}")
        return bot_response
    except subprocess.CalledProcessError as e:
        return "I'm having trouble connecting to the AI."