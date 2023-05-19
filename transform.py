import os
import openai
import requests
from classes import Entry
    
def create_summary(entries: list[Entry]):
    query = ""
    
    index = 1
    for entry in entries:
        query += f"{index}" + entry.description + "\n"
        index += 1
        
    query = f'''{query} \nWrite me a summary paragraph based on the descriptions within the above text.
    This summary should start with 'Hi Francois, this is my weekly summary'. It should be no longer than 4 sentences. 
    Below that summary, create a section for each description. Rewrite each description as it's own paragraph and correct for grammar and clarity.
    Assign each section a logical title based on the description. Below each description, list the links included in the paragraph.
    Each pargraph should be no longer than 6 sentences.'''
    
    return gpt(query)
    
    

def gpt(query: str):
    endpoint = "https://api.openai.com/v1/chat/completions" #POST
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {openai.api_key}"}
    body = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": f"{query}"}],
        "temperature": 0.9,
    }
    
    response = requests.post(url=endpoint, json=body, headers=headers).json()
        
    return response["choices"][0]["message"]["content"]