from fastapi import FastAPI
from app.api import router as api_router
from app.exceptions import init_exception_handler
from app.log import init_log
from app.middlewares import init_middlewares
from contextlib import asynccontextmanager
from app.database import craete_database_if_not_exist

@asynccontextmanager
async def lifespan(app: FastAPI):
    await craete_database_if_not_exist()
    yield

app = FastAPI(title="MyWallets API", lifespan=lifespan)
init_log()
init_exception_handler(app)
init_middlewares(app)
app.include_router(api_router, prefix="/api")