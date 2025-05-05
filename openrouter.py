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
