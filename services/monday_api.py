from dotenv import load_dotenv
import os, requests, json 

load_dotenv(".env.production")

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
BOARD_ID = os.getenv("BOARD_ID") #id del board config

def load_board_config():
    url = "https://api.monday.com/v2?="
    payload = json.dumps({
        "query":f'query {{ boards(ids: {BOARD_ID}) {{ name id description items_page (limit:500) {{cursor items{{name url column_values{{  id text type ... on DateValue {{time date}}}}}}}}}}}}'
    })
    headers = {
    'Authorization': ACCESS_TOKEN,
    'Content-Type': 'application/json',
    'API-version': '2023-10'
    }
    data = requests.request("POST", url, headers=headers, data=payload)
    dataJson = data.json()
    
    config = {}
    
    for item in dataJson["data"]["boards"][0]["items_page"]["items"]:
       vals = { cv["id"]: cv["text"] for cv in item["column_values"] }
       print(f'vals: {vals} ')
       config[vals["long_text_mks9arq7"]] ={
           "col_comment": vals["long_text_mks9a1zs"],
           "col_rating":  vals["long_text_mks93dwf"],
           "area": vals["text_mks93aaq"],
           "correo": vals["long_text_mks9tvzs"],
           "usuario": vals["long_text_mks9bp9d"],
           "itTicket":vals["long_text_mksbsedy"]
       }
    
    # print("config: ",config)  
    return config
    

def get_data_item(item_id):
    url = "https://api.monday.com/v2?="
    payload = json.dumps({
        "query": f'query {{items (ids: {item_id}) {{name column_values {{id value text}}}}}}'
    })
    
    headers = {
    'Authorization': ACCESS_TOKEN,
    'Content-Type': 'application/json',
    'API-version': '2023-10'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.text


