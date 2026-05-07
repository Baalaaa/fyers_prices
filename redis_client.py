import json
import os
import redis

from config.loggers import logger
from dotenv import load_dotenv


# --- Loading .env Files ---
load_dotenv()


# ---- Class Redis Client ----
class RedisClient:

    # ---- Default Constructor ----
    def __init__(self):
        self.HOST = os.getenv("REDIS_HOST")
        self.PORT = int(os.getenv("REDIS_PORT"))
        self.PASSWORD = os.getenv("REDIS_PASSWORD")


    # ---- Connect Redis Func ----
    def connect_remote_redis(self):
        """Connects to a Redis server"""

        try:
            self.r = redis.Redis(
                host=self.HOST,
                port=self.PORT,
                password=self.PASSWORD,
                username="default",
                decode_responses=True
            )
            self.r.ping()
            print("Connected to Redis")

        except Exception as e:
            logger.error(f"Redis Error: {e}")


    # ---- Append Live Feed Func -----
    def append_live_feeds(self, symbol: str, live_quote: dict):
        """Appends stocks feeds to the Redis server"""

        try:
            self.r.set(symbol, json.dumps(live_quote))

        except Exception as e:
            logger.error(f"Redis Error: {e}")


    # ---- Get Live Feed ----
    def get_live_feeds(self, symbol: str):
        """Gets stocks feeds from the Redis server"""

        try:
            response = self.r.get(symbol)

            # ---- Check Response ---
            if response is None:
                logger.error(response)

            return response

        except Exception as e:
            logger.error(f"Redis Error: {e}")




if __name__ == '__main__':
    redis_client = RedisClient()
    redis_client.connect_remote_redis()
