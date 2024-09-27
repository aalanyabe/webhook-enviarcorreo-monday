import requests
import json

# webhook_url = "https://webhook.site/594e6dba-54c6-4005-a0f7-f58fb622cf32"
webhook_url = "http://127.0.0.1:5000/webhook"

data = {
    'name' : 'DevOps Journey',
    'Channel URL': 'https://www.youtube.com/watch?v=CKeJYQs92hs'
}

r = requests.post(webhook_url, data = json.dumps(data),headers= {'Content-type': 'application/json'})