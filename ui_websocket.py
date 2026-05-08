import json
import os
import asyncio
import time

import redis
import uvicorn

from dotenv import load_dotenv
from config.loggers import logger
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware

# --- Instances ---
load_dotenv()
app =FastAPI()


# ---- CORS ----
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Redis Connection ---
redis_conn = redis.Redis(
    host=os.getenv("REDIS_HOST"),
    port=int(os.getenv("REDIS_PORT")),
    password=os.getenv("REDIS_PASSWORD"),
    decode_responses=True )


@app.websocket("/ws/{symbol}")
async def websocket_endpoint(ws: WebSocket, symbol: str):
    """Create websocket endpoint."""

    # --- Accepting Connection ---
    await ws.accept()
    try:
    # ---- Today Whole Data -----
        pattern = f"candle:{symbol}:1m:*"
        keys = list(redis_conn.scan_iter(pattern))
        candles = []
        if keys:
            sorted_key = sorted(keys, key=lambda x: int(x.split(":")[-1]))

            for key in sorted_key:

                candle = redis_conn.hgetall(key)
                # print("RAW CANDLE:", candle)
                candles.append({
                    "time":int(candle["start"]),
                    "open":float(candle["open"]),
                    "high":float(candle["high"]),
                    "low":float(candle["low"]),
                    "close":float(candle["close"]),
                    "volume":float(candle["volume"])
                })

            # Send Data
            await ws.send_text(json.dumps({
                "type": "history",
                "data": candles
            }))

        # ---- Subscribe Live data -----
        pubsub = redis_conn.pubsub()
        pubsub.subscribe("candles:1m")
        pubsub.get_message()

        while True:
            message = pubsub.get_message()
            if message and message["type"] == "message":
                data = json.loads(message["data"])
                await ws.send_text(json.dumps({
                    "type": "live",
                    "data": data
                }))
            await asyncio.sleep(0.1)

    except Exception as e:
        logger.error(f"Websocket Error: {e} !")




if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8009)