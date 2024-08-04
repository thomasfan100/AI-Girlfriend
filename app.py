from langchain_community.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate 
from langchain.memory import ConversationBufferWindowMemory
from dotenv import find_dotenv, load_dotenv
import requests
from playsound import playsound

import os
from flask import Flask, render_template, request
app = Flask(__name__)
load_dotenv(find_dotenv())
ELEVEN_LABS_API_KEY = os.getenv("ELEVEN_LABS_API_KEY")

def get_response_from_ai(human_input):
    '''
    template = """
    you are as a role of my girlfriend, be kind sweet and sexy
    {history}
    Boyfriend: {human_input}
    Shirley:
    """

    prompt = PromptTemplate(
        input_variables=("history","human_input"),
        template = template
    )
    
    chatgpt_chain = LLMChain(
        llm=OpenAI(temperature=0.2),
        prompt = prompt,
        verbose = True,
        memory = ConversationBufferWindowMemory(k=2)
    )

    output = chatgpt_chain.predict(human_input=human_input)
    '''
    x = len(human_input)
    if x > 30:
        output = "hey thomas i really like the way you look you sexy mongrel rawr uwu"
    elif x > 20:
        output = "are you going to get in my steel plate reinforced pants yet or what?"
    elif x > 10:
        output = "you know you are just such a loner and just a bad bad BAD boy. quick do five wall kisses"
    else:
        output = "god your dong is just so gianormous i need to see that thing helicopter. make it go brrrrrr"
    return output

def get_voice_message(message):
    payload = {
        "text":message,
        "model_id" :"eleven_monolingual_v1",
        "voice_settings":{
            "stability": 0,
            "similarity_boost":0
        }
    }
    headers = {
        'Accept' : 'audio/mpeg',
        'xi-api-key' : ELEVEN_LABS_API_KEY,
        'Content-Type' :'application/json'
    }
    response = requests.post("https://api.elevenlabs.io/v1/text-to-speech/kPzsL2i3teMYv0FxEYQ6",json=payload, headers = headers)
    if response.status_code == 200 and response.content:
        with open('./static/audio.mp3','wb') as f:
            f.write(response.content)
        playsound('./static/audio.mp3')
        return response.content

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/send_message', methods=(['POST']))
def send_message():
    human_input = request.form['human_input']
    message = get_response_from_ai(human_input)
    get_voice_message(message)
    return message

if __name__ == "__main__":
    #app.run(debug=True)
    app.run(host="0.0.0.0",port=5000)