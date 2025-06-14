from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from fastapi import FastAPI
from contextlib import asynccontextmanager
import logging
from config.settings import Settings
from typing import Optional
from config.auth.auth_settings import AuthSettings


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

            await self.create_expired_index(
                collection_name="refreshTokens", field_name="expiredAt"
            )

            return self.database
        except Exception as e:
            logging.info(f"Failed to connect to MongoDB: {e}")
            if self.client:
                self.client.close()
            raise

    async def create_expired_index(self, collection_name: str, field_name: str):
        try:
            if self.database is None:
                raise Exception("Database not initialized. Call initialize() first.")

            collection = self.database[collection_name]
            index_name = f"{field_name}_expire_index"

            # the index creation is an idempotent operation in MongoDB, so it can be called multiple times without error
            await collection.create_index(
                keys=[(field_name, 1)],
                name=index_name,
                expireAfterSeconds=60,  # 60 seconds
                background=True,  # Create index in the background
            )
            logging.info(
                f"Created index {index_name} on {collection_name} for field {field_name} with expiration of 60 seconds."
            )
        except Exception as e:
            logging.info(
                f"Failed to create TTL index on {collection_name}.{field_name} in MongoDB: {e}"
            )

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
