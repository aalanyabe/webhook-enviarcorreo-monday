import requests

url = "http://127.0.0.1:5000/webhook"

r = requests.post(url)

print(r.content)