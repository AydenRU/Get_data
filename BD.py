from asyncio import gather

import asyncpg
import asyncio
from asyncpg import Connection, Pool

from contextlib import asynccontextmanager

from processing_data import data_post, data_comments
from processing_data import jsontime_in_time

# curses = asyncpg.connect(host='localhost', user='postgres', password='postgres', database='postgres')

pool: Pool = None


@asynccontextmanager
async def lifelist(app: "FastAPI"):
    global pool

    pool = await asyncpg.create_pool(host='localhost', user='postgres', password='postgres', database='postgres', min_size=1, max_size=4)
    await create_db()
    await json_load_in_bd(data_post, data_comments)
    yield
    await pool.close()

async def create_db():
    # curses: Connection = await asyncpg.connect(host='localhost', user='postgres', password='postgres', database='postgres')
    try:
        async with pool.acquire() as curses:
            async with curses.transaction():
                await curses.execute("""
                                    DROP TABLE IF EXISTS post CASCADE
                                    """
                )
                await curses.execute("""
                                    DROP TABLE IF EXISTS comments CASCADE
                                    """
                )
                await curses.execute("""CREATE TABLE post (
                                id SERIAL PRIMARY KEY,
                                title VARCHAR(128) NOT NULL,
                                body TEXT NOT NULL,
                                author VARCHAR(64) NOT NULL,
                                created_at TIMESTAMP NOT NULL DEFAULT now()
                                )"""
                )

                await curses.execute("""CREATE TABLE comments (
                                id SERIAL PRIMARY KEY,
                                post_id INT NOT NULL,
                                comment TEXT NOT NULL,
                                created_at TIMESTAMP NOT NULL DEFAULT now(),
                                comment_user VARCHAR(64) NOT NULL,
                                CONSTRAINT post_id_fk FOREIGN KEY (post_id) REFERENCES post(id)
                                )"""
                )

    except Exception as error:
        print(error)


async def json_load_in_bd(data_post, data_comments):
    try:
        async with pool.acquire() as cursor:
            async with cursor.transaction():
                await cursor.executemany("""INSERT INTO post (title, body, author, created_at)
                                        VALUES ($1, $2, $3, $4)
                                        """, ((post['title'], post['body'], post['author'], jsontime_in_time(post['created_at'])) for post in data_post))
#
                await cursor.executemany("""INSERT INTO comments (post_id, comment, created_at, comment_user)
                                        VALUES ($1, $2, $3, $4)
                                        """, ((comment['post_id'], comment['comment'], jsontime_in_time(comment['created_at']), comment['user']) for comment in data_comments))
    except Exception as error:
        print(error)

async def get_post_db() -> dict:
    try:
        async with pool.acquire() as cursor:
            async with cursor.transaction():
                data = await cursor.fetch("""SELECT * FROM post""")

                row = await cursor.fetchval("""SELECT COUNT(*) FROM post""")

        return {'posts': [dict(row) for row in data], 'total_result': row}


    except Exception as error:
        print(error)

async def get_post_id_db(id: int) -> dict:
    """
    Ты получаешь:
    {'post': post, 'comments': comments}
    """
    try:
        async with pool.acquire() as cursor:
            async with cursor.transaction():
                post = await cursor.fetchrow("""SELECT * FROM post WHERE id = $1""", id)
                comments = await cursor.fetch("""SELECT * FROM comments WHERE post_id = $1""", id)

        if not comments:
            comments = "У данного поста еще нету комментариев"
        else:

            comments = [dict(comment) for comment in comments]
        post = dict(post)

        return {'post': post, 'comments': comments}

    except Exception as error:
        print(error)
        return {'error': 'Ошибка сервера'}

