from config.settings import Settings
from enum import Enum
import asyncio
import logging
from fastapi import Depends

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class DatabaseType(Enum):
    MONGODB = "mongodb"
    MYSQL = "mysql"
    POSTGRESQL = "postgresql"


class DatabaseManager:
    def __init__(self, settings: Settings):
        self.settings = settings
        try:
            self.db_type = DatabaseType(settings.db_type)
        except ValueError:
            raise ValueError(
                f"Unsupported database type: {settings.db_type}. Supported types: {[dt.value for dt in DatabaseType]}"
            )
        self.connection = None
        self.is_initialized = False
        self.initializer = None
        self._initialization_lock = asyncio.Lock()

    # initialize the database connection, if not initialized, initialize it
    async def initialize(self, settings: Settings):
        # Only one coroutine can execute this block at a time
        async with self._initialization_lock:
            # Double-check pattern: verify still not initialized
            if not self.is_initialized:
                try:
                    from config.mongodb_initializer import MongoDBInitializer

                    if self.db_type == DatabaseType.MONGODB:
                        self.initializer = MongoDBInitializer(self.settings)
                    else:
                        raise ValueError(
                            f"Database type {self.db_type} is not supported"
                        )

                    logging.info("Initializing database connection...")
                    self.connection = await self.initializer.initialize()
                    self.is_initialized = True
                    logging.info("Database initialization completed")

                    return self.connection
                except Exception as e:
                    logging.error(f"Failed to initialize database: {e}")
                    raise  # Re-raise for caller to handle()

            else:
                logging.info("Database already initialized, skipping")
                return self.connection

    # get database connection, if not initialized, raise exception
    async def get_connection(self):
        if not self.is_initialized:
            raise Exception("Database not initialized. Call initialize() first.")
        return self.connection

    # close database connection
    def close(self):
        if self.initializer:
            self.initializer.close()
            self.initializer = None
            self.connection = None
            self.is_initialized = False
