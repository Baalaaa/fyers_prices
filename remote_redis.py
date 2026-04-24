import os
import time

import redis

from loggers import logger
from dotenv import load_dotenv



load_dotenv()


class RedisClient:

    def __init__(self):
        self.HOST = os.getenv("REDIS_HOST")
        self.PORT = int(os.getenv("REDIS_PORT"))
        self.PASSWORD = os.getenv("REDIS_PASSWORD")



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
            logger.error("Redis Error:", e)


    def append_stocks_feeds(self, symbol: str, ltp_price: float):
        """Appends stocks feeds to the Redis server"""

        try:
            self.r.set(symbol, ltp_price)

        except Exception as e:
            logger.error("Redis Error:", e)


    def get_stocks_feeds(self, symbol: str):
        """Gets stocks feeds from the Redis server"""

        try:

            response = self.r.get(symbol)
            # if response is not None:
            #     print(response)
            # print(response)
            return response

        except Exception as e:
            logger.error("Redis Error:", e)


    def append_index_feeds(self, symbol: str, live_data: dict):
        """Appends stocks feeds to the Redis server"""

        try:

            self.r.hset(symbol, mapping=live_data)

        except Exception as e:
            logger.error("Redis Error:", e)

    def get_index_feeds(self, symbol: str):
        """Gets stocks feeds from the Redis server"""

        try:

            response = self.r.hgetall(symbol)
            return response

        except Exception as e:
            logger.error("Redis Error:", e)


if __name__ == '__main__':
    redis_client = RedisClient()
    redis_client.connect_remote_redis()
    data = {
        "symbol": "NSE:NIFTY50-INDEX",
        "ltp": 22345,
        "timestamp": 1713945000
    }
    redis_client.append_index_feeds(symbol="NSE:NIFTY50", live_data=data)
    time.sleep(20)
    redis_client.get_stocks_feeds(symbol='NSE:NIFTY50')