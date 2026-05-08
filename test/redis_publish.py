import json
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
    r = redis.Redis(host="redis-15952.c267.us-east-1-4.ec2.cloud.redislabs.com", port=15952,
                    password="CbHCxaZqeqPRsW0Q37GYgIDDGF7Hs8cs", decode_responses=True)
    print(r.ping())
    fyers_obj = RedisPublish(redis_client=r, access_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsiZDoxIiwiZDoyIiwieDowIiwieDoxIiwieDoyIl0sImF0X2hhc2giOiJnQUFBQUFCcF9WbkpqX3Y0T3dwQk5MUjFVbDlxaTFmc3lhQ1ltNXRucVRiOWJ4VG1BTUpYckdNNFJmcXU5TGJucU9mWTVlcjdFa1p2VWJYQnRrQ0NuQmRrSC1wR2ptaWIzcGxJX2o3cTFHa3lZaDd1VVRvZy1TST0iLCJkaXNwbGF5X25hbWUiOiIiLCJvbXMiOiJLMSIsImhzbV9rZXkiOiJlZWEwOGRkMmE0ZGI1MjYwNTgyM2IyMTJkMTVhN2QyOTAxYWY2NDg1MDg5YWMyY2JmZGJmZmVlYyIsImlzRGRwaUVuYWJsZWQiOiJOIiwiaXNNdGZFbmFibGVkIjoiTiIsImZ5X2lkIjoiWEIxNDU2MCIsImFwcFR5cGUiOjEwMCwiZXhwIjoxNzc4Mjg2NjAwLCJpYXQiOjE3NzgyMTEyNzMsImlzcyI6ImFwaS5meWVycy5pbiIsIm5iZiI6MTc3ODIxMTI3Mywic3ViIjoiYWNjZXNzX3Rva2VuIn0.atWUSwp34517M7fy1ROLcAQ6D6sRfAuIwMXh8Mxt6C0")
    fyers_obj.connect()