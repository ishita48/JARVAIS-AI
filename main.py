import openai
import speech_recognition as sr
import pyttsx3
import random
import os
import requests
from textblob import TextBlob
import tkinter as tk
from tkinter import messagebox

# Initialize speech recognition
recognizer = sr.Recognizer()

# Initialize text-to-speech
engine = pyttsx3.init()

# Set OpenAI API key
openai.api_key = 'your-api-key'

# Function to recognize speech
def listen():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            print("You:", text)
            return text
        except sr.UnknownValueError:
            print("Sorry, could not understand audio.")
            return ""
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            return ""

# Function to speak
def speak(text):
    engine.say(text)
    engine.runAndWait()

# API functions
def fetch_joke():
    try:
        response = requests.get("https://official-joke-api.appspot.com/jokes/random")
        if response.status_code == 200:
            joke = response.json()
            return f"{joke['setup']} ... {joke['punchline']}"
        else:
            return "Couldn't fetch a joke at the moment."
    except Exception as e:
        return f"Error: {e}"

# Modify the generate_response function to use GPT-3
def generate_response(user_input):
    # Call GPT-3 to generate a response
    response = openai.Completion.create(
        engine="davinci",
        prompt=user_input,
        max_tokens=50
    )
    return response.choices[0].text.strip()

def fetch_definition(word):
    try:
        response = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}")
        if response.status_code == 200:
            definition = response.json()[0]['meanings'][0]['definitions'][0]['definition']
            return f"The definition of {word} is: {definition}"
        else:
            return "Couldn't fetch the definition at the moment."
    except Exception as e:
        return f"Error: {e}"

def fetch_trivia():
    try:
        response = requests.get("https://opentdb.com/api.php?amount=1&type=multiple")
        if response.status_code == 200:
            trivia = response.json()['results'][0]
            question = trivia['question']
            correct_answer = trivia['correct_answer']
            return f"Trivia: {question} The correct answer is: {correct_answer}"
        else:
            return "Couldn't fetch trivia at the moment."
    except Exception as e:
        return f"Error: {e}"


# API functions
def fetch_news():
    try:
        response = requests.get("https://newsapi.org/v2/top-headlines?country=us&apiKey=0ce0ea100487490b8221e0734c93fe4a") # REPLACE WITH YOUR OWN API KEY from newsapi
        if response.status_code == 200:
            news = response.json()
            articles = news['articles']
            if articles:
                return f"Latest news: {articles[0]['title']}"
            else:
                return "No news available at the moment."
        else:
            return "Couldn't fetch news at the moment."
    except Exception as e:
        return f"Error: {e}"


def fetch_fact():
    try:
        response = requests.get("https://uselessfacts.jsph.pl/random.json?language=en")
        if response.status_code == 200:
            fact = response.json()['text']
            return fact
        else:
            return "Couldn't fetch a fact at the moment."
    except Exception as e:
        return f"Error: {e}"

def fetch_covid_stats(country="USA"):
    try:
        response = requests.get(f"https://disease.sh/v3/covid-19/countries/{country}")
        if response.status_code == 200:
            data = response.json()
            stats = f"COVID-19 Stats for {country}:\nCases: {data['cases']}\nDeaths: {data['deaths']}\nRecovered: {data['recovered']}"
            return stats
        else:
            return "Couldn't fetch COVID-19 statistics at the moment."
    except Exception as e:
        return f"Error: {e}"

def fetch_currency_conversion(base="USD", target="EUR"):
    try:
        response = requests.get(f"https://api.exchangerate-api.com/v4/latest/{base}")
        if response.status_code == 200:
            rate = response.json()['rates'][target]
            return f"1 {base} is equal to {rate} {target}."
        else:
            return "Couldn't fetch currency conversion rates at the moment."
    except Exception as e:
        return f"Error: {e}"

def fetch_chuck_norris_joke():
    try:
        response = requests.get("https://api.chucknorris.io/jokes/random")
        if response.status_code == 200:
            joke = response.json()['value']
            return joke
        else:
            return "Couldn't fetch a Chuck Norris joke at the moment."
    except Exception as e:
        return f"Error: {e}"

# Function to generate a response based on user input
def gigenerate_response(user_input):
    sentiment = TextBlob(user_input).sentiment.polarity
    if sentiment > 0.5:
        return "That's great to hear!"
    elif sentiment < -0.5:
        return "I'm sorry to hear that."
    elif "how are you" in user_input.lower():
        return random.choice(["I'm doing great, thank you for asking!", "I'm feeling fantastic today!", "I'm functioning optimally, ready to assist!"])
    elif "joke" in user_input.lower():
        return fetch_joke()
    elif "definition" in user_input.lower():
        word = user_input.split("definition of")[-1].strip()
        return fetch_definition(word)
    elif "news" in user_input.lower():
        return fetch_news()
    elif "trivia" in user_input.lower():
        return fetch_trivia()
    elif "fact" in user_input.lower():
        return fetch_fact()
    elif "covid" in user_input.lower():
        country = user_input.split("covid stats for")[-1].strip()
        return fetch_covid_stats(country)
    elif "currency" in user_input.lower():
        parts = user_input.split()
        base = parts[-3].upper()
        target = parts[-1].upper()
        return fetch_currency_conversion(base, target)
    elif "chuck norris" in user_input.lower():
        return fetch_chuck_norris_joke()
    elif "thank you" in user_input.lower():
        return random.choice(["You're welcome!", "Happy to help!", "No problem!"])
    elif "instagram" in user_input.lower():
        os.system("start https://www.instagram.com/isha.is.sleepy/")
        return "Opening Instagram..."
    elif "youtube" in user_input.lower():
        os.system("start https://www.youtube.com/")
        return "Opening YouTube..."
    elif "github" in user_input.lower():
        os.system("start https://github.com/ishita48")
        return "Opening GitHub..."
    elif "linkedin" in user_input.lower():
        os.system("start https://www.linkedin.com/in/ishita-gupta-tech/")
        return "Opening LinkedIn..."
    else:
        return "I'm sorry, I didn't quite catch that. Can you please repeat?"

# Function to handle speech mode
def speech_mode():
    while True:
        user_input = listen()
        if user_input.lower() in ["exit", "goodbye", "jarvis stop", "stop", "bye"]:
            print("Jarvis: Goodbye!")
            speak("Goodbye!")
            break
        response = generate_response(user_input)
        print("Jarvis:", response)
        speak(response)

# Function to handle text mode
def text_mode():
    def on_submit():
        user_input = entry.get()
        response = generate_response(user_input)
        chat_log.config(state=tk.NORMAL)
        chat_log.insert(tk.END, f"You: {user_input}\n")
        chat_log.insert(tk.END, f"Jarvis: {response}\n\n")
        chat_log.config(state=tk.DISABLED)
        entry.delete(0, tk.END)

    root = tk.Tk()
    root.title("Jarvis A.I.")
    root.configure(bg='#f8f8ff')

    chat_log = tk.Text(root, bg='#f8f8ff', font=('Helvetica', 12), wrap='word', state=tk.DISABLED)
    chat_log.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    entry_frame = tk.Frame(root, bg='#f8f8ff')
    entry_frame.pack(fill=tk.X, padx=10, pady=10)

    entry = tk.Entry(entry_frame, bg='#ffe4e1', font=('Helvetica', 12))
    entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

    submit_button = tk.Button(entry_frame, text="Submit", bg='#b0e0e6', font=('Helvetica', 12), command=on_submit)
    submit_button.pack(side=tk.RIGHT)

    root.mainloop()

# Main function to handle conversation
def main():
    greeting = ("Hello, I'm Jarvis A.I. A pop up will appear soon,\n"
                "please select whether you want to use the speech recognition mode\n"
                "or text mode every time you want to interact.\n"
                "Thank you.")
    print("Jarvis: " + greeting)
    speak(greeting)

    try:
        mode = messagebox.askyesno("Mode Selection", "Do you want to use Speech Recognition mode? Click 'No' for Text mode.")
    except tk.TclError:
        print("Error: Tkinter is not properly installed or configured.")
        sys.exit(1)

    if mode:
        speech_mode()
    else:
        text_mode()

# GUI functions...
def text_mode():
    def on_submit():
        user_input = entry.get()
        response = generate_response(user_input)
        chat_log.config(state=tk.NORMAL)
        chat_log.insert(tk.END, f"You: {user_input}\n", "user")
        chat_log.insert(tk.END, f"Jarvis: {response}\n\n", "jarvis")
        chat_log.config(state=tk.DISABLED)
        entry.delete(0, tk.END)

    root = tk.Tk()
    root.title("Jarvis A.I.")
    root.configure(bg='#2c3e50')

    chat_frame = tk.Frame(root, bg='#2c3e50')
    chat_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    chat_log = tk.Text(chat_frame, bg='#34495e', fg='#ecf0f1', font=('Helvetica', 12), wrap='word', state=tk.DISABLED)
    chat_log.pack(fill=tk.BOTH, expand=True)

    entry_frame = tk.Frame(root, bg='#2c3e50')
    entry_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

    entry = tk.Entry(entry_frame, bg='#34495e', fg='#ecf0f1', font=('Helvetica', 12))
    entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

    submit_button = tk.Button(entry_frame, text="Submit", bg='#2980b9', fg='#ecf0f1', font=('Helvetica', 12), command=on_submit)
    submit_button.pack(side=tk.RIGHT)

    style = tk.Style()
    style.configure("user", foreground="#3498db")
    style.configure("jarvis", foreground="#e74c3c")

    root.mainloop()

if __name__ == "__main__":
    main()

