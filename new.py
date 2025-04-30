import win32com.client

def say(text):
    speaker = win32com.client.Dispatch("SAPI.SpVoice")
    speaker.Speak(text)

# say("হ্যালো শান্তো, আমি উইন্ডোজ স্পিকিং অ্যাসিস্ট্যান্ট।")

# while 1:
#     s= input("Enter you words: ")
#     speaker.Speak(s)

if __name__ == "__main__":
    print("Shanto")  # just printing something
    say("Hello Shanto, I am your AI desktop assistant.")
    