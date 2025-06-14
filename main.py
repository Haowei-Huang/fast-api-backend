from fastapi import FastAPI
from contextlib import asynccontextmanager
from config.database_manager import DatabaseManager
from config.settings import Settings
from routers import users, hotels, bookings
import logging
from fastapi.middleware.cors import CORSMiddleware
from exceptions.exception_handler import add_exception_handlers

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3000",  # Corrected
    "http://127.0.0.1:3001",  # Added for consistency if you use this port
    "http://127.0.0.1:8000",
]


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

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD"],
    allow_headers=[
        "Content-Type",
        "Authorization",
        "Access-Control-Allow-Origin",
        "Accept",
    ],
)

add_exception_handlers(app)

app.include_router(users.router)
app.include_router(hotels.router)
app.include_router(bookings.router)
