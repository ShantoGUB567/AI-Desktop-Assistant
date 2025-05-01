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
    say("Hello I am your Assistant PUUKI")

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

        apps = {
            "calculator": "start calc",
            "calendar": "start outlookcal:",
            "clock": "start ms-clock:",
            "notepad": "start notepad",
            "snipping tool": "start snippingtool",
            "settings": "start ms-settings:",
        }

        for app in apps:
            if app in query.lower():
                os.system(apps[app])
                say(f"Opening {app}")
                # return


        if "open music" in query.lower() or "play music" in query.lower():
            say("Music is starting...")
            musicPath = "D:\GitHub\AI-Desktop-Assistant\music1.mp3"
            # os.system(f"open {musicPath}")
            os.startfile(musicPath)

        elif "vs code" in query.lower() or "open code" in query.lower():
            say("VS Code is starting...")
            vscode_path = r"C:\Users\alsha\AppData\Local\Programs\Microsoft VS Code\Code.exe"
            os.startfile(vscode_path) 
        
        elif "browser" in query.lower() or "open chrome" in query.lower():
            say("Your browser is starting...")
            chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
            os.startfile(chrome_path) 
        
        elif "the time" in query.lower():
            time = datetime.datetime.now().strftime("%H:%M:%S")
            say(f"The time is {time}")
        
        elif "nice" in query.lower() or "good" in query.lower() or "josh" in query.lower():
            say("Thank you sir .. ")

        elif "exit" in query.lower() or "close" in query.lower() or "stop" in query.lower():
            say("Clossing the Project. Thank you..")
            exit()
        
        # else:
        #     print("Nothing matched. Waiting for next command.")
        
            
        # say(query)
    