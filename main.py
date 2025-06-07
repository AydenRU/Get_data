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
    """    Формат ответа:
    posts: [
        {
            id: <int>,
            title: <str>,
            body: <str>,
            author:	<str>,
            created_at: <str>,
            comments_count: <int>
        }
    ],
    total_results: <int>

    Порядок ключей словаря в ответе не важен
    """
    result_data = data_post.copy()
    counter_comments = {}
    for comment in data_comments:
        counter_comments[comment['post_id']] = counter_comments.get(comment['post_id'], 0) + 1

    for post in result_data:
        if post['id'] in counter_comments:
            post['comments_count'] = counter_comments[post['id']]

    return {'post': result_data, 'total_results': len(result_data)}


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
    result_post["result_comments"] = result_comments

    return {"post": result_post}






