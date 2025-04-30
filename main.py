import speech_recognition as sr
import os
import win32com.client
import webbrowser
import datetime

def say(text):
    # os. system(f"say{text}")
    speaker = win32com.client.Dispatch("SAPI.SpVoice")
    speaker.Speak(text)

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except Exception as e:
            return "Some Error Occurred.. Sorry for that... "

if __name__ == "__main__":
    print("Shanto")
    say("Hello I am you Assistant PUUKI")

    while True:
        print("listening.........")
        query= takeCommand()

        sites = [
            ["Youtube", "https://youtube.com"], 
            ["Wikipedia", "https://wikipedia.com"],
            ["Facebook", "https://facebook.com"],
            ["Google", "https://google.com"],
            ["Keep", "https://keep.google.com"],
            ["Email", "https://mail.google.com"],
        ]

        for site in sites:
            if f"Open {site[0]}".lower() in query.lower():
                say(f"Opening {site[0]} Shanto ... ")
                webbrowser.open(site[1])

        if "open music" or "play music" in query:
            say("Music is starting...")
            musicPath = "D:\GitHub\AI-Desktop-Assistant\music1.mp3"
            # os.system(f"open {musicPath}")
            os.startfile(musicPath)
        
        elif "the time" in query:
            time = datetime.datetime.now().strftime("%H:%M:%S")
            say(f"The time is {time}")

        elif "exit" or "close" or "stop" in query:
            say("Clossing the Project. Thank you..")
            exit()
        
        else:
            print("Close...")
        
            
        # say(query)
    