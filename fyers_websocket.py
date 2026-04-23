import os
from fyers_apiv3.FyersWebsocket import data_ws


# --- Class FyersServices  ---
class FyersServices:

    # --- Default Constructor ---
    def __init__(self):

        # --- Reading Text File ---
        with open(os.path.abspath("access_token.txt"), "r") as f:
            self.access_token = f.read().strip()


    # --- onMessage Func ---
    def onmessage(self, message):
        print("Response:", message)


    # --- onError Func ---
    def onerror(self, message):
        print("Error:", message)


    # --- onClose Func ---
    def onclose(message):
        print("Connection closed:", message)


    # --- onOpen Func ---
    def onopen(self):
        data_type = "SymbolUpdate"
        symbols = ['NSE:SBIN-EQ', 'NSE:ADANIENT-EQ']
        fyers.subscribe(symbols=symbols, data_type=data_type)
        fyers.keep_running()



if __name__ == '__main__':

    # --- Fyers instance ---
    fyers_obj = FyersServices()

    # --- Fyers DataSocket ---
    fyers = data_ws.FyersDataSocket(
        access_token=fyers_obj.access_token,
        log_path="",
        litemode=False,
        write_to_file=False,
        reconnect=True,
        on_connect=fyers_obj.onopen,
        on_close=fyers_obj.onclose,
        on_error=fyers_obj.onerror,
        on_message=fyers_obj.onmessage
    )

    fyers.connect()