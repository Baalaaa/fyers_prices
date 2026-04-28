import os

from config.loggers import logger
from fyers_apiv3.FyersWebsocket import data_ws
from constants.nifty_stock_symbol import nifty_symbol_list



# --- Class FyersServices  ---
class FyersServices:

    # --- Default Constructor Func ---
    def __init__(self, access_token, redis_client, contract_file_dwn):

        self.redis = redis_client
        self.access_token = access_token
        self.contract_obj = contract_file_dwn
        self.contract_obj.fetch_nifty_contract_file()
        self.contract_obj.fetch_sensex_contract_file()
        self.fyers = data_ws.FyersDataSocket(
            access_token=self.access_token,
            log_path="fyers_logs",
            litemode=False,
            write_to_file=False,
            reconnect=True,
            on_connect=self.onopen,
            on_close=self.onclose,
            on_error=self.onerror,
            on_message=self.onmessage
        )

    def connect(self):
        self.fyers.connect()

    def clean_symbol(self, sym):
        return sym.removeprefix('NSE:').removesuffix('-EQ')


    # --- onMessage Func ---
    def onmessage(self, message):
        if message.get('type') == 'sf' and 'symbol' in message:
            symbol = self.clean_symbol(message['symbol'])
            logger.info(f"Symbol: {symbol} -> {message['ltp']}")
            self.redis.append_live_feeds(symbol=symbol, live_quote=message)

        elif message.get('type') in ['cn', 'ful', 'sub']:
            logger.info(message)

    # --- onError Func ---
    def onerror(self, message):
        logger.error(f"Error: {message}")


    # --- onClose Func ---
    def onclose(message):
        logger.warning(f"Connection closed: {message}")


    # --- onOpen Func ---
    def onopen(self):
        data_type = "SymbolUpdate"

        sensex_symb = self.contract_obj.fetch_sensex_current_week_expiry_contract()
        nifty_symb = self.contract_obj.fetch_nifty_current_week_expiry_contract()

        self.fyers.subscribe(symbols=nifty_symbol_list, data_type=data_type)
        self.fyers.subscribe(symbols=sensex_symb, data_type=data_type)
        self.fyers.subscribe(symbols=nifty_symb, data_type=data_type)
        self.fyers.keep_running()



