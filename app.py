from aiohttp import web
from aiohttp_swagger import *
import asyncio
import logging
import aiomongo
import os
from dataclasses import dataclass

@dataclass(frozen=True)
class Config:
    MONGO_HOST: str = 'mongo'
    MONGO_PORT: int = 27017
    SERVER_HOST: str = '0.0.0.0'
    SERVER_PORT: int = 8080

config = Config(MONGO_HOST = os.getenv('MONGO_HOST', 'mongo'), MONGO_PORT = int(os.getenv('MONGO_PORT', 27017)),
    SERVER_HOST = os.getenv('SERVER_HOST', '0.0.0.0'), SERVER_PORT = int(os.getenv('SERVER_PORT', 8080)))

mongo_client = None

async def handler(request):
    # see http://localhost:8080/api/doc for swagger

    """
    ---
    description: This end-point allows to asynchronousely ping python.org
    tags:
    - Asynchronous subtask
    produces:
    - text/plain
    responses:
        "200":
            description: successful operation. Return "Hello" text
        "405":
            description: invalid HTTP Method
    """
    name = request.match_info.get('name', "Anonymous")
    db = mongo_client.get_default_database()
    print(db)
    resp = await db.items.insert_one({'x': 1})
    
    return web.Response(text=f"Hello, {name}")

def setup_routes(app):
    app.add_routes([web.get('/', handler), web.get('/{name}', handler)])

async def init(loop):
    global mongo_client
    app = web.Application(loop=loop)
    setup_routes(app)
    setup_swagger(app)
    mongo_client = await aiomongo.create_client(f'mongodb://{config.MONGO_HOST}:{config.MONGO_PORT}/test?w=2&maxpoolsize=10', loop=loop)
    return app, mongo_client, config.SERVER_HOST, config.SERVER_PORT

def main():
    global mongo_client
    logging.basicConfig(level=logging.DEBUG)

    logging.debug(config)

    loop = asyncio.get_event_loop()
    app, mongo_client, host, port = loop.run_until_complete(init(loop))
    web.run_app(app, host=host, port=port)

if __name__ == '__main__':
    main()
