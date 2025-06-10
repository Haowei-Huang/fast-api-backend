from fastapi import FastAPI
from contextlib import asynccontextmanager
from config.database_manager import DatabaseManager
from config.settings import Settings
from routers import users
import logging


# Use lifespan to connect to the database
@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("Starting up application...")

    settings = Settings()
    db_manager = DatabaseManager(settings)
    app.state.db_manager = db_manager

    try:
        # initialize database
        await app.state.db_manager.initialize(settings)
        logging.info("Database manager initialized.")
        yield
    finally:
        app.state.db_manager.close()


app = FastAPI(
    title="fast-api-backend",
    summary="fast api backend for simplibook project",
    lifespan=lifespan,
)

app.include_router(users.router)
