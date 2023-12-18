@asynccontextmanager
async def lifespan(app: FastAPI):
    redis_db = await sess_db()
    databases["redis_db"] = redis_db
    yield
    databases.clear()
    redis_db.quit()
