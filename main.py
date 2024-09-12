import os
import webbrowser
import speech_recognition as sr
import datetime
import pyttsx3
from pytube import Search
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import threading

# Load models and tokenizers only once
token = "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"
tokenizer = AutoTokenizer.from_pretrained("gpt2", token=token)
model = AutoModelForCausalLM.from_pretrained("gpt2", token=token)
chat_pipeline = pipeline("text-generation", model=model, tokenizer=tokenizer)

# Initialize chat history
chatStr = ""

# Initialize speech recognition
r = sr.Recognizer()

def say(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def takeCommand():
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.5)
        r.pause_threshold = 0.5
        print("Listening...")
        try:
            audio = r.listen(source)
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except Exception as e:
            print(f"Error: {e}")
            return "Some Error Occurred. Sorry from Siri"

def play_youtube_video(query):
    search = Search(query)
    video = search.results[0]
    webbrowser.open(video.watch_url)

def ai(prompt):
    try:
        response = chat_pipeline(prompt, max_length=50, num_return_sequences=1, truncation=True)
        ai_response = response[0]['generated_text']
        print(f"AI Response: {ai_response}")
        say(ai_response)
        return ai_response
    except Exception as e:
        print(f"Error: {e}")
        say("I'm sorry, I couldn't process that request.")
        return ""

def chat(query):
    global chatStr
    print(f"Current chat history: {chatStr}")
    chatStr += f"User: {query}\nSiri: "
    try:
        response = chat_pipeline(chatStr, max_length=50, num_return_sequences=1, truncation=True)
        reply = response[0]['generated_text'].split('Siri: ')[-1]
        print(f"AI Response: {reply}")
        say(reply)
        chatStr += f"{reply}\n"
        return reply
    except Exception as e:
        print(f"Error: {e}")
        say("I'm sorry, I couldn't process that request.")
        return ""

def main():
    print("Hi Siri")
    say("Hi, I am Siri, the A.I.")
    while True:
        query = takeCommand().lower()
        if "quit" in query or "exit" in query:
            say("Goodbye!")
            break
        sites = [["youtube", "https://www.youtube.com"], ["wikipedia", "https://www.wikipedia.com"], ["google", "https://www.google.com"]]
        for site in sites:
            if f"open {site[0]}".lower() in query:
                threading.Thread(target=lambda: webbrowser.open(site[1])).start()
        if "the time" in query:
            hour = datetime.datetime.now().strftime("%H")
            minute = datetime.datetime.now().strftime("%M")
            say(f"The time is {hour} and {minute} minutes")
        elif "open facetime" in query:
            os.system("open /System/Applications/FaceTime.app")
        elif "open pass" in query:
            os.system("open /Applications/Passky.app")
        elif "using ai" in query:
            ai(prompt=query)
        elif "reset chat" in query:
            chatStr = ""
        elif "play" in query:
            threading.Thread(target=play_youtube_video, args=(query,)).start()
        else:
            print("Chatting...")
            chat(query)

if __name__ == '__main__':
    main()
