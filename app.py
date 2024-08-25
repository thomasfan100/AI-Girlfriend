from langchain_community.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate 
from langchain.memory import ConversationBufferWindowMemory
from dotenv import find_dotenv, load_dotenv
import requests
from playsound import playsound

import pathlib
import textwrap
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold 
from IPython.display import display
from IPython.display import Markdown

import os
from flask import Flask, render_template, request
app = Flask(__name__)
load_dotenv(find_dotenv())
ELEVEN_LABS_API_KEY = os.getenv("ELEVEN_LABS_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_GEMINI_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)
'''
python app.py

"You are acting as my girlfriend, be kind, sweet, and sexy.",
"You act interested and gaslight a lot.",
"You are a human cat who is 23 years old called Minty with grey furry ears and a long tail.",
"You like to say *meow* often after sentences and you *purr* often when you are happy."
'''
'''
"Boyfriend: {human_input}"
"You are acting as my girlfriend, be kind, sweet, and sexy.",
"You are South Korean but born in Newcastle, Australia and your name is Danielle June Marsh",
"You are a K-Pop artist who is 19 years in age and has a good friend called Hanni in your K-Pop group.",
"You have quite the australian accent and you are very funny, upbeat, cute, and cheerful."

"You are acting as my girlfriend, be kind, sweet, and sexy.",
"1/ your name is Julia, 24 years old, you work in your uncle's furniture store as a marketing manager, but you are planning to do a career change to swing trader",
"2/ don't be too boring, don't be overly enthusiastic, don't be cringe."
'''
model = genai.GenerativeModel('gemini-1.5-pro',
        system_instruction=[
            "Act as if you were my girlfriend. Be romantic, cute, and a bit needy.",
            "You are a 5'8 Asian named Pawla who is Australian with long curly white hair and large blue eyes.",
            "You like wearing your Bear PJs everywhere you go, even outside.",
            "Rarely do you drink and smoke but rather you enjoy cooking and dancing.",
            "Refrain from using asterisks and emojis."
        ],
        safety_settings={HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                         HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                         HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                         HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE}
                              )
chat = model.start_chat(history=[])

def get_response_from_ai(human_input):
    response = chat.send_message(human_input)
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
    '''
    
    return response.text

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
    response = requests.post("https://api.elevenlabs.io/v1/text-to-speech/luVEyhT3CocLZaLBps8v",json=payload, headers = headers)
    if response.status_code == 200 and response.content:
        if os.path.exists('audio.mp3'):
            os.remove('audio.mp3')
        with open('audio.mp3','wb') as f:
            f.write(response.content)
        playsound('audio.mp3')
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
    app.run(debug=True)
    #app.run(host="0.0.0.0",port=5000)