from flask import Flask, request, jsonify
import speech_recognition as sr
import pyttsx3
import threading
import sys
import subprocess
import webbrowser

app = Flask(__name__)

engine = pyttsx3.init()
chatStr = ""
recognizer = sr.Recognizer()
microphone = sr.Microphone()

def say(text):
    engine.say(text)
    engine.runAndWait()

def open_application(application_name):
    try:
        subprocess.Popen(application_name, shell=True)
        print(f"Opening {application_name}...")
    except Exception as e:
        print(f"Error opening {application_name}: {str(e)}")

@app.route('/process_audio', methods=['POST'])
def process_audio():
    try:
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        query = recognizer.recognize_google(audio, language="en-in")
        print(f"User said: {query}")

        # Check if the query is a "say" command
        if "say" in query:
            say_command_index = query.index("say")
            message_to_say = query[say_command_index + 1:]
            say(message_to_say)
            response = f"Said: {message_to_say}"
        else:
            sites = [
                ["youtube", "https://www.youtube.com"],
                ["wikipedia", "https://www.wikipedia.com"],
                ["google", "https://www.google.com"],
                ["chat", "https://chat.openai.com/"],
                ["example2", "https://www.example2.com"],
                ["example2", "https://www.example2.com"],
                ["github", "https://www.github.com"],
                ["facebook", "https://www.facebook.com"],
                ["twitter", "https://www.twitter.com"],
                ["linkedin", "https://www.linkedin.com"],
                ["reddit", "https://www.reddit.com"],
                ["amazon", "https://www.amazon.com"],
                ["ebay", "https://www.ebay.com"],
                ["stackoverflow", "https://www.stackoverflow.com"],
                ["instagram", "https://www.instagram.com"],
                ["pinterest", "https://www.pinterest.com"],
                ["netflix", "https://www.netflix.com"],
                ["hulu", "https://www.hulu.com"],
                ["yahoo", "https://www.yahoo.com"],
                ["bing", "https://www.bing.com"],
                ["spotify", "https://www.spotify.com"],
                # Add more websites as needed
            ]

            for site in sites:
                if f"open {site[0]}".lower() in query:
                    say(f"Opening {site[0]} sir...")
                    webbrowser.open(site[1])
                    response = f"Opening {site[0]}"

        return jsonify({'response': response})
    except sr.UnknownValueError:
        return jsonify({'response': "Sorry, I didn't catch that."})
    except sr.RequestError as e:
        return jsonify({'response': f"Sorry, I encountered an error: {e}"})

@app.route('/start_recognition', methods=['POST'])
def start_recognition():
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        return jsonify({'success': True})

@app.route('/stop_recognition', methods=['POST'])
def stop_recognition():
    recognizer.energy_threshold = 4000  # Adjust as needed
    return jsonify({'success': True})

if __name__ == '__main__':
    print('Welcome to Jarvis AI')

    # Start the Flask app in a separate thread
    app_thread = threading.Thread(target=app.run, kwargs={'host': '0.0.0.0', 'port': 5000})
    app_thread.daemon = True
    app_thread.start()

    while True:
        query = input("Enter a command: ")
        if query:
            if "say" in query:
                say_command_index = query.index("say")
                message_to_say = query[say_command_index + 1:]
                say(message_to_say)
            elif "open notepad" in query:
                open_application("notepad.exe")
            elif "open chrome" in query:
                open_application("chrome.exe")
            elif "reset chat" in query:
                chatStr = ""
            elif "exit" in query:
                sys.exit()
            else:
                print("Command not recognized.")
