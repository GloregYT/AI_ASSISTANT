import requests
import json

URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

API_KEY = "AIzaSyBBsB7pZiAt6WmyBxaF3pVMohq5zjgekSo"

headers = {
    "Content-Type" : "application/json",
    "X-goog-api-key" : API_KEY,
}

payload = {
     "contents": [
       {
         "parts": [
           {
             "text": "Кхендекох"
           }
         ]
       }
     ]
   }
try:
    response = requests.post(URL, headers=headers, json=payload)
    print(response.json())
except Exception:
    print(Exception)
