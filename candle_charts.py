from datetime import datetime

import pandas as pd
import mplfinance as mpf
from matplotlib.pyplot import title

from config.loggers import logger




# ---- Charts Func -----
def create_charts(candles: list) -> None:
    """Creates charts based on candles data"""

    try:
        rows = []

        for candle in candles:
            rows.append({
                "Date": datetime.fromtimestamp(int(candle['start'])),
                "Open": float(candle['open']),
                "High": float(candle['high']),
                "Low": float(candle['low']),
                "Close": float(candle['close']),
                "Volume": float(candle.get('volume', 0)),
            })

            # --- Dataframe ---
            df = pd.DataFrame(rows)

            # --- Set Index ---
            df.set_index("Date", inplace=True)

            # --- Sort Index ---
            df.sort_index(inplace=True)

            # ---- Plot ----
            mpf.plot(
                df,
                type="candle",
                title="NIFTY50 1-Min Candles",
                figsize=[12, 8]
            )

    except Exception as e:
        logger.error(f"exception occurred while creating charts failed: {e} !")