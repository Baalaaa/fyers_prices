import json
import os
import threading
import time

import redis
from dotenv import load_dotenv

from redis_client import RedisClient

# --- .env files  ---
load_dotenv()


# --- Candle Generator ---
class CandleGenerator:

    def __init__(self, r):
        self.r = r
        self.candles = {}
        self.TICK_CHANNEL = "ticks"
        self.CANDLE_CHANNEL = "candles:1m"
        self.TIMEFRAME_SECONDS = 60


    def get_bucket(self, ts):
        """Convert timestamp to minutes bucket"""
        return int(ts // self.TIMEFRAME_SECONDS) * self.TIMEFRAME_SECONDS


    def process_tick(self, tick: dict):
        """Process one tick"""

        symbol = tick["symbol"]
        price = float(tick["price"])
        qty = float(tick.get("qty", 0))
        ts = float(tick.get("ts", time.time()))

        bucket = self.get_bucket(ts)
        current = self.candles.get(symbol)

        if current and current['start'] != bucket:
            self.save_candle(symbol, current)
            current = None

        if current is None:
            self.candles[symbol] = {
                "start": bucket,
                "open": price,
                "high": price,
                "low": price,
                "close": price,
                "volume": qty }
        else:
            current["high"] = max(current['high'], price)
            current["low"] = min(current["low"], price)
            current["close"] = price
            current["volume"] = qty


    def save_candle(self, symbol, candle):
        """Save candle to Redis"""

        key = f"candles:{symbol}:{candle['start']}"
        self.r.hset(key, mapping=candle)

        self.r.publish("candles", json.dumps({
            "symbol": symbol,
            **candle,
        }))

        print(f"[CANDLE] {symbol} | "
              f"O={candle['open']} H={candle['high']} "
              f"L={candle['low']} C={candle['close']} V={candle['volume']}")

# -------- MAIN --------
def run():


    r = redis.Redis(
        host=os.getenv("REDIS_HOST", "localhost"),
        port=int(os.getenv("REDIS_PORT", 6379)),
        password=os.getenv("REDIS_PASSWORD"),
        decode_responses=True
    )
    print(r.ping())
    generator = CandleGenerator(r)

    pubsub = r.pubsub()
    pubsub.subscribe(generator.TICK_CHANNEL)

    print("Listening for ticks...")

    for msg in pubsub.listen():
        if msg["type"] != "message":
            continue

        try:
            tick = json.loads(msg["data"])
            generator.process_tick(tick)
        except Exception as e:
            print("Bad tick:", e)


if __name__ == '__main__':
    run()