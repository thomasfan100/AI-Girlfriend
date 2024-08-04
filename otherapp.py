from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferWindowMemory
from dotenv import find_dotenv, load_dotenv
import requests
import os
from flask import Flask, render_template, request, jsonify

load_dotenv(find_dotenv())

GOOGLE_GEMINI_API_KEY = os.getenv("GOOGLE_GEMINI_API_KEY")
GOOGLE_GEMINI_API_URL = "https://gemini.googleapis.com/v1/models/text"

def get_response_from_gemini(human_input, history):
    template = """
    You are acting as my girlfriend, be kind, sweet, and sexy.
    {history}
    Boyfriend: {human_input}
    Shirley:
    """

    prompt = template.format(history=history, human_input=human_input)

    headers = {
        "Authorization": f"Bearer {GOOGLE_GEMINI_API_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "input": prompt,
        "temperature": 0.2,
    }

    response = requests.post(GOOGLE_GEMINI_API_URL, headers=headers, json=data)
    response_data = response.json()

    output = response_data.get("output", "No response received")
    return output

app = Flask(__name__)
memory = ConversationBufferWindowMemory(k=2)

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/send_message', methods=['POST'])
def send_message():
    human_input = request.form['human_input']
    
    # Retrieve conversation history
    history = "\n".join([f"{message['role']}: {message['content']}" for message in memory.chat_memory.messages])
    
    # Get response from the Gemini API
    message = get_response_from_gemini(human_input, history)
    
    # Update memory with new conversation turns
    memory.chat_memory.add_message({"role": "user", "content": human_input})
    memory.chat_memory.add_message({"role": "assistant", "content": message})
    
    return jsonify({"message": message})

if __name__ == "__main__":
    app.run(debug=True)
