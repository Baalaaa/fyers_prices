import uvicorn
from starlette.datastructures import QueryParams

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
@app.get("/api/v1/stocks_ltp")
async def get_stocks_ltp(symbol: str = Query(...)):
    """Fetch the latest Nifty Stock LTP"""

    try:

        # --- Symbol Check ---
        if symbol is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Symbol is required"
            )



        # --- Fetching LTP From Redis ---
        live_feed = redis.get_stocks_feeds(symbol=symbol)

        # --- LTP Check ---
        if live_feed is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Symbol is invalid"
            )

        return {
            "status": "ok",
            "code": 200,
            "message": "Success",
            "live feed": live_feed
        }


    except Exception as e:
        HTTPException(status_code=500, detail=str(e))


# ----- Ltp API ------
@app.get("/api/v1/index_data")
async def get_index_ltp(symbol: str = Query(...)):
    """Fetch the latest Nifty Stock LTP"""

    try:

        # --- Symbol Check ---
        if symbol is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Symbol is required"
            )



        # --- Fetching Feed From Redis ---
        live_feed = redis.get_index_feeds(symbol=symbol)

        # --- Feed Check ---
        if live_feed is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Symbol is invalid"
            )

        return {
            "status": "ok",
            "code": 200,
            "message": "Success",
            "live feed": live_feed
        }

    except Exception as e:
        HTTPException(status_code=500, detail=str(e))



if __name__ == '__main__':

    # --- Redis Client ---
    redis = RedisClient()
    redis.connect_remote_redis()
    uvicorn.run(app, host="127.0.0.1", port=8007)
