import speech_recognition as sr
import pyttsx3
import datetime
import requests
import wikipedia
import os

# Initialize the speech recognition object
r = sr.Recognizer()

# Initialize the text-to-speech engine
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def get_weather():
    response = requests.get("http://api.openweathermap.org/data/2.5/weather?q=London,UK&appid=YOUR_API_KEY")
    weather_data = response.json()
    return weather_data["weather"][0]["description"]

def set_reminder(time, reminder):
    print(f"Reminder set for {time}: {reminder}")

def get_answer(question):
    try:
        return wikipedia.summary(question, sentences=2)
    except wikipedia.exceptions.DisambiguationError as e:
        return str(e)
    except wikipedia.exceptions.PageError:
        return "I couldn't find any information on that topic."

def main():
    while True:
        with sr.Microphone() as source:
            print("Listening...")
            audio = r.listen(source)

            try:
                text = r.recognize_google(audio, language="en-US")
                print("You said: " + text)

                if "what's the weather like" in text:
                    speak("The weather is " + get_weather())
                elif "set a reminder" in text:
                    time = input("Enter the time for the reminder: ")
                    reminder = input("Enter the reminder: ")
                    set_reminder(time, reminder)
                elif "what's" in text or "who's" in text or "what is" in text:
                    question = text.replace("what's", "").replace("who's", "").replace("what is", "")
                    answer = get_answer(question)
                    speak(answer)
                elif "open" in text:
                    app = text.replace("open ", "")
                    os.system(f"start {app}.exe")
                elif "exit" in text:
                    break
                else:
                    speak("I didn't understand that. Please try again.")

            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand your audio")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))

if __name__ == "__main__":
    main()
