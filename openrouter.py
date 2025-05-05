import requests
from config import apikey

url = "https://openrouter.ai/api/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {apikey}",
    "Content-Type": "application/json",
    # "HTTP-Referer": "<your-site-url>",  # optional
    # "X-Title": "<your-site-name>",      # optional
}
data = {
    "model": "deepseek/deepseek-r1:free",
    "messages": [{"role": "user", "content": "talk about CSE? (in one line)"}]
}

response = requests.post(url, headers=headers, json=data)
print(response.json()["choices"][0]["message"]["content"])
# response = requests.post(url, headers=headers, json=data)

if response.status_code != 200:
    print("API error:", response.status_code, response.text)
    print("Sorry, API did not respond properly.")
    # return

    res_json = response.json()
    if "choices" not in res_json:
        print("Unexpected response:", res_json)
        print("Sorry, I did not get a valid response from AI.")
        # return

    reply = res_json["choices"][0]["message"]["content"]

# print("ALL reply :", reply)