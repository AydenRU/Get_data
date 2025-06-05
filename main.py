from fastapi import FastAPI
from pydantic import BaseModel

import json



app = FastAPI()

def open_json(adres: str):
    with open(adres, encoding='utf-8') as comments:
        result_data = json.load(comments)
    return result_data

data_post = open_json('data\\posts.json')
data_comments = open_json('data\\comments.json')





print(data_post)

