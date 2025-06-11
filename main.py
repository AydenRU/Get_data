from fastapi import FastAPI
from fastapi import HTTPException

import asyncio
import json

from pydantic import BaseModel

from BD import lifelist, DataBase

app = FastAPI(lifespan=lifelist)


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
    """
    result_data = await DataBase.get_post_db()

    return {'posts': [result_data['posts']], 'total_result': result_data['total_result']}

@app.get('/posts/{id}')
async def get_post_id(id: int) -> dict:
    """Асинхронно ищу Комментарии и Пост"""
    result_post = await DataBase.get_post_id_db(id)
    return result_post






