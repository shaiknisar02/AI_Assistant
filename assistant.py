import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import webbrowser
import pyjokes
import os
import random

# Initialize Text-to-Speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Speed of speech
engine.setProperty('volume', 1.0)

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Female voice

# --- Helper Functions ---

def speak(text):
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()

def listen():
    """Captures voice input from the microphone"""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio).lower()
        print(f"You said: {command}")
        return command
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that.")
        return ""
    except sr.RequestError:
        speak("Network error.")
        return ""

def wish_user():
    hour = int(datetime.datetime.now().hour)
    if hour < 12:
        greet = "Good morning"
    elif 12 <= hour < 18:
        greet = "Good afternoon"
    else:
        greet = "Good evening"
    speak(f"{greet}! Hello Shaik Nisar, your virtual assistant is online.")
    speak("How can I help you today?")

def tell_joke():
    joke = pyjokes.get_joke()
    speak("Here's a funny one for you.")
    speak(joke)

def open_website(site_name):
    urls = {
        "youtube": "https://www.youtube.com",
        "google": "https://www.google.com",
        "gmail": "https://mail.google.com",
        "github": "https://www.github.com",
        "stackoverflow": "https://stackoverflow.com",
    }
    url = urls.get(site_name.lower())
    if url:
        speak(f"Opening {site_name}")
        webbrowser.open(url)
    else:
        speak(f"Sorry, I don't have {site_name} saved. Searching it instead.")
        pywhatkit.search(site_name)

def respond_to_fun_phrases(command):
    responses = {
        "how are you": ["I'm just a bunch of code, but feeling fantastic!", "Doing great! What about you?"],
        "who are you": ["I'm your smart assistant!", "I’m your helpful voice buddy."],
        "what's your name": ["I’m Nisar's personal assistant.", "You can call me your digital friend."],
        "tell me something funny": ["Why don’t scientists trust atoms? Because they make up everything!"]
    }
    for phrase, replies in responses.items():
        if phrase in command:
            speak(random.choice(replies))
            return True
    return False

# --- Core Command Execution ---

def execute_command(command):
    """Respond to voice commands"""
    if respond_to_fun_phrases(command):
        return

    if "time" in command:
        time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The time is {time}")

    elif "date" in command:
        today = datetime.date.today().strftime("%B %d, %Y")
        speak(f"Today's date is {today}")

    elif "wikipedia" in command:
        topic = command.replace("wikipedia", "").strip()
        speak(f"Searching Wikipedia for {topic}")
        try:
            summary = wikipedia.summary(topic, sentences=2)
            speak(summary)
        except wikipedia.exceptions.DisambiguationError:
            speak("There are multiple results. Please be more specific.")
        except wikipedia.exceptions.PageError:
            speak("I couldn't find any information on that.")

    elif "play" in command:
        song = command.replace("play", "").strip()
        speak(f"Playing {song} on YouTube")
        pywhatkit.playonyt(song)

    elif "search for" in command:
        query = command.replace("search for", "").strip()
        speak(f"Searching Google for {query}")
        pywhatkit.search(query)

    elif "joke" in command:
        tell_joke()

    elif "open notepad" in command:
        speak("Opening Notepad")
        os.system("notepad")

    elif "open calculator" in command:
        speak("Opening Calculator")
        os.system("calc")

    elif "open chrome" in command:
        chrome_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
        if os.path.exists(chrome_path):
            speak("Opening Chrome")
            os.startfile(chrome_path)
        else:
            speak("Chrome is not installed in the default path.")

    elif "open" in command:
        # Open specific websites
        site_name = command.replace("open", "").strip()
        open_website(site_name)

    elif "exit" in command or "quit" in command or "stop" in command:
        speak("Goodbye! Have a great day.")
        exit()

    else:
        speak("I didn't understand that. Can you please repeat?")

# --- Main Execution Loop ---

if __name__ == "__main__":
    wish_user()
    while True:
        command = listen()
        if command:
            execute_command(command)
