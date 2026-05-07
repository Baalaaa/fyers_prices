import json
import os
import threading
import time
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

from dotenv import load_dotenv
from config.loggers import logger
from redis_client import RedisClient


load_dotenv()


# ---- Utilities Func -----

def candle_hash_key(symbol, start_ts):
    """Create candle hash key"""
    return f"candle:{symbol}:1m:{start_ts}"


def candle_index_key(symbol):
    """Create candle index key"""
    return f"candle:{symbol}:1m"


def save_candle(r, symbol, candle):
    """Save candle to Redis"""

    try:
        # Creating Hash Key !
        hkey = candle_hash_key(symbol=symbol, start_ts=candle["start"])

        # Creating Index Key !
        ikey = candle_index_key(symbol=symbol)

        # Redis Pipeline inserts data all at a time !
        pipe = r.pipeline()

        pipe.hset(hkey, mapping={
            "open":   candle["open"],
            "high":   candle["high"],
            "low":    candle["low"],
            "close":  candle["close"],
            "volume": candle["volume"],
            "start":  candle["start"]
        })

        # Expiry if more than 7 days !
        if os.getenv('CANDLE_TTL_SECONDS'):
            pipe.expire(hkey, int(os.getenv('CANDLE_TTL_SECONDS')))

        # Sorted index !
        pipe.zadd(ikey, {str(candle["start"]): candle["start"]})

        # Execute !
        pipe.execute()

        # Broadcast Live into Redis Channel !
        r.publish(os.getenv('CANDLE_CHANNEL'), json.dumps({
            "symbol": symbol,
            "tf": "1m",
            **candle,
        }))

        print(f"[SAVED] {symbol} "
              f"@ {datetime.fromtimestamp(candle['start'], tz=ZoneInfo('Asia/Kolkata')):%H:%M} "
              f"O={candle['open']} H={candle['high']} "
              f"L={candle['low']} C={candle['close']} V={candle['volume']}")

    except Exception as e:
        logger.error(f"exception occurred while saving candle: {e} !")

def subscriber_loop(agg, r):
    """Subscriber loop"""

    try:
        pubsub = r.pubsub()
        pubsub.subscribe("ticks")
        print(f"[SUBSCRIBED] Listening on ticks ")

        for msg in pubsub.listen():
            if msg['type'] != 'message':
                continue
            try:
                tick = json.loads(msg['data'])
                symbol = tick['symbol']
                price = float(tick['price'])
                qty = float(tick.get('qty', 0))
                ts  = float(tick.get('ts', time.time()))
                agg.on_tick(symbol, price, qty, ts)

            except (json.JSONDecodeError, KeyError) as e:
                logger.error(f"[Warn] bad tick skipped: {e} -> {msg['data']!r}")



    except Exception as e:
        logger.error(f"exception occurred while subscribing candle: {e} !")

def flusher_loop(agg, stop_event):
    """Flusher loop"""

    while not stop_event.is_set():
        now = time.time()
        next_boundry = (int(now // 60) + 1) * 60
        sleep_time = (next_boundry - now) + 1
        if stop_event.wait(sleep_time):
            return
        agg.flush_expiry(time.time())

# ---- Class CandleAggregator ----
class CandleAggregator:

    def __init__(self, r):
        self.redis_client = r
        self.candle = {}
        self.state_lock = threading.Lock()
        self.TIMEFRAME_SECONDS = 60



    def bucket(self, ts):
        """convert ts into 1 min window eg. 10:01:45 into 10:01:0"""
        return int(ts // self.TIMEFRAME_SECONDS) * self.TIMEFRAME_SECONDS


    def on_tick(self, symbol, price, qty, ts):
        """Creates 1min candles if exists updates else new candle"""

        try:
            b = self.bucket(ts=ts)

            with self.state_lock:
                current_candle = self.candle.get(symbol)

                if current_candle and current_candle['start'] != b:
                    save_candle(self.redis_client, symbol=symbol, candle=current_candle)
                    current_candle = None

                if current_candle is None:
                    self.candle[symbol] = {
                        "start": b,
                        "open": price,
                        "high": price,
                        "low": price,
                        "close": price,
                        "volume": qty
                    }
                else:
                    current_candle["high"] = max(current_candle['high'], price)
                    current_candle["low"] = min(current_candle['low'], price)
                    current_candle["close"] = price
                    current_candle["volume"] += qty


        except Exception as e:
            logger.error(f"exception occurred while updating & creating candle: {e} !")


    def flush_expiry(self, now_ts):
        """Flush candle expiry & stores"""

        try:
            current_bucket = self.bucket(ts=now_ts)
            to_save = []

            # Check !
            with self.state_lock:
                for symbol, candle in list(self.candle.items()):
                    if candle['start'] < current_bucket:
                        to_save.append((symbol, candle))
                        del self.candle[symbol]

            # Saving Candles !
            for symbol, candle in to_save:
                save_candle(self.redis_client, symbol=symbol, candle=candle)

        except Exception as e:
            logger.error(f"exception occurred while flushing candle expiry: {e} !")



# ---- Execute Script Func ----
def execution_script():
    """main execution script"""

    try:
        # --- Connecting Redis ---
        redis_obj = RedisClient()
        redis_obj.connect_remote_redis()

        #
        redis_conn = redis_obj.r
        #
        agg = CandleAggregator(redis_conn)
        stop_event = threading.Event()

        threading.Thread(target=subscriber_loop, args=(agg, redis_conn), daemon=True).start()
        threading.Thread(target=flusher_loop, args=(agg, stop_event), daemon=True).start()


        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n[EXIST] flushing in flight candles....")
            stop_event.set()
            agg.flush_expiry(time.time() + 60)

    except Exception as e:
        logger.error(f"exception occurred while executing script: {e} !")













if __name__ == '__main__':
    execution_script()