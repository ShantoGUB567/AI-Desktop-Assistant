import speech_recognition as sr
import os
import win32com.client
import webbrowser
import datetime
import requests
from config import apikey

def say(text):
    speaker = win32com.client.Dispatch("SAPI.SpVoice")
    speaker.Speak(text)

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except Exception as e:
            return "Some Error Occurred.. Sorry for that... "

def ai(prompt):
    print("Analysing .....")
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {apikey}",
        "Content-Type": "application/json",
    }
    data = {
        "model": "deepseek/deepseek-r1:free",
        "messages": [{"role": "user", "content": f"{prompt}"}]
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code != 200:
        print("API error:", response.status_code)
        print(response.text)
        say("Sorry, API failed.")
        return

    res_json = response.json()
    if "choices" not in res_json:
        print("Invalid response:", res_json)
        say("Sorry, no valid AI response found.")
        return

    reply = res_json["choices"][0]["message"]["content"]
    print("ShanBot Response:", reply)
    print("done")


chatStr = ""
def chat(query):
    print("Analysing .....")
    global chatStr
    # print(chatStr)
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {apikey}",
        "Content-Type": "application/json",
    }
    data = {
        "model": "deepseek/deepseek-r1:free",
        "messages": [{"role": "user", "content": f"Shanto: {query}\nShanBot: (1/2 line)"}]
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code != 200:
        print("API error:", response.status_code, response.text)
        say("Sorry, API failed.")
        return

    res_json = response.json()
    if "choices" not in res_json:
        print("Unexpected response:", res_json)
        say("Sorry, invalid AI response.")
        return
    print("here is result")
    print(response.json()["choices"][0]["message"]["content"])
    say(response.json()["choices"][0]["message"]["content"])
    chatStr += response.json()["choices"][0]["message"]["content"]
    return response.json()["choices"][0]["message"]["content"]


if __name__ == "__main__":
    print("Welcome......")
    say("Hello I am your Assistant ShanBot")

    while True:
        print("listening.........")
        query= takeCommand()
        handled = False

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
                print(f"Opening {site[0]} ... ")
                say(f"Opening {site[0]} ... ")
                webbrowser.open(site[1])
                handled = True

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
                print(f"Opening {app} ... ")
                say(f"Opening {app}")
                handled = True


        if "open music" in query.lower() or "play music" in query.lower():
            say("Music is starting...")
            musicPath = "D:\GitHub\AI-Desktop-Assistant\music1.mp3"
            # os.system(f"open {musicPath}")
            os.startfile(musicPath)
            handled = True

        elif "vs code" in query.lower() or "open code" in query.lower():
            say("VS Code is starting...")
            vscode_path = r"C:\Users\alsha\AppData\Local\Programs\Microsoft VS Code\Code.exe"
            os.startfile(vscode_path) 
            handled = True
        
        elif "browser" in query.lower() or "open chrome" in query.lower():
            say("Your browser is starting...")
            chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
            os.startfile(chrome_path) 
            handled = True
        
        elif "the time" in query.lower():
            time = datetime.datetime.now().strftime("%H:%M:%S")
            say(f"The time is {time}")
            handled = True
        
        elif "nice" in query.lower() or "good" in query.lower() or "josh" in query.lower():
            say("Thank you sir .. ")
            handled = True

        elif "exit" in query.lower() or "close" in query.lower() or "stop" in query.lower():
            say("Clossing the Project. Thank you..")
            exit()
        
        elif "using AI".lower() in query.lower():
            say("Thinking...")
            ai(query)
            handled = True

        if not handled:
            chat(query)
        # chat(query)
        # else:
        #     chat(query)
        
        # else:
        #     print("Nothing matched. Waiting for next command.")
        
            
        # say(query)
    