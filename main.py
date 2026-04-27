import json
from typing import List

import uvicorn

from loggers import logger
from remote_redis import RedisClient
from fastapi import FastAPI, HTTPException, status, Query

# --- Flask App ---
app = FastAPI(title="Nifty Stock API")


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
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Symbol is required"
            )

        result = {}

        for symbol in symbols:

            # --- Fetching Live Feed From Redis ---
            live_feed = redis.get_live_feeds(symbol=symbol)

            if live_feed:
                result[symbol] = json.loads(live_feed)
            else:
                result[symbol] = None


        return {
            "status": "ok",
            "code": 200,
            "message": "Success",
            "live feed": result
        }

    except Exception as e:
        HTTPException(
            status_code=500,
            detail="internal server error"
        )





if __name__ == '__main__':

    # --- Redis Client ---
    redis = RedisClient()
    redis.connect_remote_redis()

    # ---- Fast API ---
    uvicorn.run(app, host="127.0.0.1", port=8007)
