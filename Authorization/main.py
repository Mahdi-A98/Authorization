# In the name of GOD

from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager


from api.v1 import users_api
from db.db import collections, databases, sess_db
from config.middlewares import InternalSecurityMiddleware
from config.config import LOGGING_CONFIG


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis_db = await sess_db()
    databases["redis_db"] = redis_db
    yield
    databases.clear()
    redis_db.quit()

app = FastAPI(lifespan=lifespan)
app.include_router(users_api.router)
app.add_middleware(InternalSecurityMiddleware)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host="localhost", port=8004, log_level="debug", reload=True, log_config=LOGGING_CONFIG)
#     # uvicorn.run(app, host="localhost", port=8004, log_level="debug")