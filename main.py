import speech_recognition as sr
import pyttsx3
import openai
from flask import Flask, request

openai.api_key = ""

app = Flask(__name__)
engine = pyttsx3.init()

def audio_to_text(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)
    except:
        return "Error"

def g_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=4000,
        n=1,
        stop=None,
        temperature=0.5
    )
    return response["choices"][0]["text"]

def speak_text(text):
    engine.say(text)
    engine.runAndWait()

@app.route('/process_prompt', methods=['POST'])
def process_prompt():
    prompt = request.form['prompt']
    if prompt:
        filename = "input.wav"
        speak_text("Say your question")
        with sr.Microphone() as source:
            recognizer = sr.Recognizer()
            source.pause_threshold = 1
            audio = recognizer.listen(source, phrase_time_limit=None, timeout=None)
            with open(filename, "wb") as f:
                f.write(audio.get_wav_data())
            text = audio_to_text(filename)
        if text:
            print(f"You said: {text}")
            response = g_response(text)
            print(f"GPT says: {response}")
            return response
    return "Error"

if __name__ == "__main__":
    main()
