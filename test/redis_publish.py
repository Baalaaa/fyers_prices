import json
import os
import time
from datetime import datetime

import redis

from fyers_apiv3.FyersWebsocket import data_ws
from constants.nifty_stock_symbol import nifty_symbol_list, index_symbol


class RedisPublish:

    def __init__(self, redis_client, access_token):
        self.symbols = nifty_symbol_list
        self.index_symbols = index_symbol
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
            on_error=self.onerror,
            on_close=self.onclose,
        )

    def connect(self):
            self.fyers.connect()


    def onmessage(self, message):
        try:

            # --
            if not isinstance(message, dict):
                return

            # --
            if "symbol" not in message:
                return

            # --
            if "ltp" not in message:
                return

            symbol = message.get("symbol", "").split(":")[-1]
            ts = int(message.get("last_traded_time") or time.time())
            tick = {
                "symbol": symbol,
                "price": message.get("ltp"),
                "qty": 1,
                "ts": ts,
            }
            self.redis_conn.publish("ticks", json.dumps(tick))
            # print("LIVE TICK:", tick, datetime.fromtimestamp(tick['ts']))

        except Exception as e:
            print("Error:", e)


    def onopen(self):
        print("Connected to Fyers")

        self.fyers.subscribe(
            symbols=self.symbols,
            data_type="SymbolUpdate")

        self.fyers.subscribe(
            symbols=self.index_symbols,
            data_type="IndexData")

        self.fyers.keep_running()


    def onclose(self, message):
        print("Socket Closed:", message)


    def onerror(self, message):
        print("Socket Error:", message)




# -------- MAIN --------
if __name__ == '__main__':
    r = redis.Redis(host="redis-15952.c267.us-east-1-4.ec2.cloud.redislabs.com", port=15952,
                    password="CbHCxaZqeqPRsW0Q37GYgIDDGF7Hs8cs", decode_responses=True)
    print(r.ping())
    os.makedirs("fyers_logs", exist_ok=True)
    fyers_obj = RedisPublish(redis_client=r, access_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsiZDoxIiwiZDoyIiwieDowIiwieDoxIiwieDoyIl0sImF0X2hhc2giOiJnQUFBQUFCcUFfQ3lTdWdTRDJtWlFjLUk3amROcVNqbHVJLW1yTHRsaFBSTGdhUTdxRXJib19NX0x6cWdneHhld2o4Nk9KYWdHa2VFZ3FxTFhqZjBteXJELVhGV1BxRlBMRHAtQ3VwWlRJYWxfUVBFVkNrS1R1Zz0iLCJkaXNwbGF5X25hbWUiOiIiLCJvbXMiOiJLMSIsImhzbV9rZXkiOiJlMmUzNTU5ZGE5ZTdjMTI4NjcyM2VmNTJkNjA5MDcwNjZjODUyZTVhNTc5MTUyMzBlOGJmMmU0ZSIsImlzRGRwaUVuYWJsZWQiOiJOIiwiaXNNdGZFbmFibGVkIjoiTiIsImZ5X2lkIjoiWEIxNDU2MCIsImFwcFR5cGUiOjEwMCwiZXhwIjoxNzc4NzE4NjAwLCJpYXQiOjE3Nzg2NDMxMjIsImlzcyI6ImFwaS5meWVycy5pbiIsIm5iZiI6MTc3ODY0MzEyMiwic3ViIjoiYWNjZXNzX3Rva2VuIn0.GiUDuYDWe_zRm3NOrvabrvMr5Oy7nkERRDGghvYso8w")
    fyers_obj.connect()