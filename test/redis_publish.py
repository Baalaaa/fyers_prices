import json
import os
import time

import redis
from fyers_apiv3.FyersWebsocket import data_ws

from redis_client import RedisClient


class RedisPublish:

    def __init__(self, redis_client, access_token):
        self.symbols = ["NSE:NIFTY50-INDEX"]
        self.redis_conn = redis_client
        self.access_token = access_token

        self.fyers = data_ws.FyersDataSocket(
            access_token=self.access_token,
            log_path="fyers_logs",
            litemode=False,
            write_to_file=False,
            reconnect=True,
            on_connect=self.onopen,
            on_message=self.onmessage,
        )

    def connect(self):
        self.fyers.connect()

    def onmessage(self, message):
        try:
            symbol = message.get("symbol", "").split(":")[-1]

            ts = message.get("last_traded_time") or time.time()

            tick = {
                "symbol": symbol,
                "price": message.get("ltp"),
                "qty": 1,
                "ts": ts,
            }

            self.redis_conn.publish("ticks", json.dumps(tick))

            print("LIVE TICK:", tick)

        except Exception as e:
            print("Error:", e)

    def onopen(self):
        print("Connected to Fyers")

        self.fyers.subscribe(
            symbols=self.symbols,
            data_type="symbolData"
        )


# -------- MAIN --------
if __name__ == '__main__':
    r = redis.Redis(host="redis-16193.c246.us-east-1-4.ec2.cloud.redislabs.com", port=16193,
                    password="zzWFR4UyaYgK9AmPgwM3f7FU0RuWxM6Z", decode_responses=True)
    print(r.ping())
    fyers_obj = RedisPublish(redis_client=r, access_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsiZDoxIiwiZDoyIiwieDowIiwieDoxIiwieDoyIl0sImF0X2hhc2giOiJnQUFBQUFCcC1DR0RiZlZMWWFXX2Rfd01pYllXZ0t1YUV5Rjhad3lzUVJGcDA0MWo3VEFjNTBMTXpVWUhfRk9sUTZ3c0lOdDBGU2VJMWM0YVp5Tk1WcWlWQnRDbGxZcDFqai0zb0NWQXoyUXlCM2tHMGRfQ0kxdz0iLCJkaXNwbGF5X25hbWUiOiIiLCJvbXMiOiJLMSIsImhzbV9rZXkiOiI3ODgyZGY5NDAyYmEyYjRkNjBmM2E3NzExYmMxNDM0NzM1MmExMDBlN2QyOWUyMzFiMjE5YWExNCIsImlzRGRwaUVuYWJsZWQiOiJOIiwiaXNNdGZFbmFibGVkIjoiTiIsImZ5X2lkIjoiWEIxNDU2MCIsImFwcFR5cGUiOjEwMCwiZXhwIjoxNzc3OTQxMDAwLCJpYXQiOjE3Nzc4NjkxODcsImlzcyI6ImFwaS5meWVycy5pbiIsIm5iZiI6MTc3Nzg2OTE4Nywic3ViIjoiYWNjZXNzX3Rva2VuIn0.GNTs8GZpxOBtjz7uP5XGRCSUnERNxoQdftaHgcHpSN0")
    fyers_obj.connect()