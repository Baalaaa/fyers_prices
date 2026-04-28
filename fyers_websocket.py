import os

from config.loggers import logger
from redis_client import RedisClient
from fyers_apiv3.FyersWebsocket import data_ws
from contract_files import ContractFileDownloader
from constants.nifty_stock_symbol import nifty_symbol_list



# --- Class FyersServices  ---
class FyersServices:

    # --- Default Constructor Func ---
    def __init__(self, redis_client, contract_file_dwn):

        self.redis = redis_client
        self.contract_obj = contract_dwn

        # --- Reading Text File ---
        with open(os.path.abspath("access_token.txt"), "r") as f:
            self.access_token = f.read().strip()


    # --- onMessage Func ---
    def onmessage(self, message):

        if message['type'] == 'sf':
            if 'symbol' in message:
                sym = message['symbol']
                symbol = sym.removeprefix('NSE:').removesuffix('-EQ')
                print(f"Symbol: {symbol}, LTP: {message['ltp']},Open: {message['open_price']}, High: {message['high_price']},Low: {message['low_price']}, Volume: {message['vol_traded_today']}")
                self.redis.append_live_feeds(symbol, live_quote=message)

        elif message['type'] in ['cn', 'ful', 'sub']:
            print(message)

        else:
            sym = message['symbol']
            symbol = sym.removeprefix('NSE:').removesuffix('-EQ')
            print(f"Symbol: {symbol}, LTP: {message['ltp']}")
            self.redis.append_live_feeds(symbol, live_quote=message)


    # --- onError Func ---
    def onerror(self, message):
        logger.error("Error:", message)


    # --- onClose Func ---
    def onclose(message):
        logger.warning("Connection closed:", message)


    # --- onOpen Func ---
    def onopen(self):
        data_type = "SymbolUpdate"

        # ---- symbols ----
        sensex_symb = self.contract_obj.fetch_sensex_current_week_expiry_contract()
        nifty_symb = self.contract_obj.fetch_nifty_current_week_expiry_contract()

        fyers.subscribe(symbols=nifty_symbol_list, data_type=data_type)
        fyers.subscribe(symbols=sensex_symb, data_type=data_type)
        fyers.subscribe(symbols=nifty_symb, data_type=data_type)
        fyers.keep_running()



if __name__ == '__main__':

    # ---- Redis Client ----
    redis_client_obj = RedisClient()
    redis_client_obj.connect_remote_redis()

    # ---- Contract Download ----
    contract_dwn = ContractFileDownloader()

    # --- Fyers instance ---
    fyers_obj = FyersServices(redis_client=redis_client_obj, contract_file_dwn=contract_dwn)

    # --- Fyers DataSocket ---
    fyers = data_ws.FyersDataSocket(
        access_token=fyers_obj.access_token,
        log_path="fyers_logs/",
        litemode=False,
        write_to_file=False,
        reconnect=True,
        on_connect=fyers_obj.onopen,
        on_close=fyers_obj.onclose,
        on_error=fyers_obj.onerror,
        on_message=fyers_obj.onmessage
    )

    # --- Connecting.... ----
    fyers.connect()