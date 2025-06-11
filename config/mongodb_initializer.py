from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from fastapi import FastAPI
from contextlib import asynccontextmanager
import logging
from config.settings import Settings
from typing import Optional


class MongoDBInitializer:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.database = None
        self.client = None

    # method for start the MongoDb Connection
    async def initialize(self):
        try:
            # Set MongoDB client
            self.client = AsyncIOMotorClient(
                self.settings.db_url, serverSelectionTimeoutMS=10000
            )
            self.database = self.client.get_database(self.settings.db_name)
            ping_response = await self.database.command("ping")

            # check database connection
            if int(ping_response["ok"]) != 1:
                raise Exception("Problem connecting to database cluster.")
            else:
                logging.info("Connected to database cluster.")

            return self.database
        except Exception as e:
            logging.info(f"Failed to connect to MongoDB: {e}")
            if self.client:
                self.client.close()
            raise

    async def get_connection(self) -> Optional[AsyncIOMotorDatabase]:
        if self.database is None:
            await self.initialize()

        # Validate connection is still alive
        try:
            await self.database.command("ping")
            return self.database
        except Exception as e:
            logging.error(f"Database connection lost: {e}")
            raise

    # method to close the database connection
    def close(self):
        if self.client:
            self.client.close()
            self.database = None
            self.client = None
            logging.info("Mongo connection closed.")
