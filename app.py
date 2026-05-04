import json
import os
from typing import List

import uvicorn
from fastapi.middleware.cors import CORSMiddleware

from contract_files import ContractFileDownloader
from fyers_websocket import FyersServices
from redis_client import RedisClient
from fastapi import FastAPI, HTTPException, status, Query

# --- Flask App ---
app = FastAPI(title="Nifty Stock API")

# --- Redis Client ---
redis_c = RedisClient()
redis_c.connect_remote_redis()

# ---- CORS -----
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    max_age=600
)


# ---- Root API ----
@app.get("/")
async def root():
    return {
        "status": "ok",
        "code": 200,
        "message": "Server Running"
    }


# ----- Ltp API ------
@app.get("/api/v1/live_feed/")
async def get_live_feed(symbols: List[str] = Query(...)):
    """Fetch the Latest Live Feed"""

    try:
        # --- Symbol Check ---
        if symbols is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Symbol is required")

        result = {}
        for symbol in symbols:
            # --- Fetching Live Feed From Redis ---
            live_feed = redis_c.get_live_feeds(symbol=symbol)
            if live_feed:
                result[symbol] = json.loads(live_feed)
            else:
                result[symbol] = None

        return {
            "status": "ok",
            "code": 200,
            "message": "Success",
            "live_feed": result
        }

    except Exception as e:
        HTTPException(status_code=500,detail="internal server error")





if __name__ == '__main__':

    # os.makedirs("fyers_logs", exist_ok=True)



    # # ---- Contract Download ----
    # contract_dwn = ContractFileDownloader()
    #
    # # --- Fyers instance ---
    # fyers_obj = FyersServices(redis_client=redis, contract_file_dwn=contract_dwn,
    #                           access_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsiZDoxIiwiZDoyIiwieDowIiwieDoxIiwieDoyIl0sImF0X2hhc2giOiJnQUFBQUFCcDhDY2Q5WG5hbVpDSDFDREtaM29lRW1nanB4ay12R3dDajkyV0UtdEhNbWV5X2NlSXc4OHd4eDhpX0RuLVVEY0g0aGZJZjY4UWd1bkl0VWFGYnFrRkJHUW1sSWV0Mll3NEx5OWVqbC1KRkVfWXVOND0iLCJkaXNwbGF5X25hbWUiOiIiLCJvbXMiOiJLMSIsImhzbV9rZXkiOiI5YTJhY2EzZDIyNjhmYzAyMzAwNzVlMGFmY2E1MTBjMWI5OTc0MjI2MTllZDg5ODg3OWI1ZWJhOSIsImlzRGRwaUVuYWJsZWQiOiJOIiwiaXNNdGZFbmFibGVkIjoiTiIsImZ5X2lkIjoiWEIxNDU2MCIsImFwcFR5cGUiOjEwMCwiZXhwIjoxNzc3NDIyNjAwLCJpYXQiOjE3NzczNDYzMzMsImlzcyI6ImFwaS5meWVycy5pbiIsIm5iZiI6MTc3NzM0NjMzMywic3ViIjoiYWNjZXNzX3Rva2VuIn0.JdcZGf06yuqo5-i7e3FjdxC-0QvBcsJgRiaH9VIpNAs")
    #
    # # --- Connecting.... ----
    # fyers_obj.connect()


    # ---- Fast API ---
    uvicorn.run("app:app", host="127.0.0.1", port=8007, reload=True)
