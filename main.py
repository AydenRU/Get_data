from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel
import asyncio
import json

app = FastAPI()

def open_json(adres: str):
     with  open(adres, encoding='utf-8') as comments:
        result_data = json.load(comments)
     if len(result_data) == 1:
         key = next(iter(result_data.keys()))
         return result_data[key]

     return result_data

async def find_comments(id: int):
    return [comment for comment in data_comments if comment["post_id"] == id]

data_post = open_json('data\\posts.json')
data_comments = open_json('data\\comments.json')


@app.get('/')
async def get_post() -> dict:
    counter_comments = {}
    for i in data_comments:
        counter_comments[i['post_id']] = counter_comments.get(i['post_id'], 0) + 1

    return {'post': data_post, 'length': len(data_post), "counter_comments": counter_comments}


@app.get('/posts/{id}')
async def get_post_id(id: int) -> dict:
    """Асинхронно ищу Комментарии и Пост"""
    result_comments = asyncio.create_task(find_comments(id))

    for i in data_post:
        if i["id"] == id:
            result_post = i
            break
    else:
        raise HTTPException(status_code=404, detail="Пост не найден")

    result_comments = await result_comments

    return {"post": result_post, "comments": result_comments}






