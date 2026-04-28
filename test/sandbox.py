import os


from contract_files import ContractFileDownloader
from fyers_websocket import FyersServices
from redis_client import RedisClient


if __name__ == '__main__':

    downloader = ContractFileDownloader()
    # downloader.fetch_sensex_contract_file()
    # downloader.fetch_sensex_current_week_expiry_contract()
    # downloader.fetch_cash_market_contract_file()
    downloader.fetch_cash_market_symbols()

    # os.makedirs("fyers_logs", exist_ok=True)
    # # ---- Redis Client ----
    # redis_client_obj = RedisClient()
    # redis_client_obj.connect_remote_redis()
    #
    # # ---- Contract Download ----
    # contract_dwn = ContractFileDownloader()
    #
    # # --- Fyers instance ---
    # fyers_obj = FyersServices(redis_client=redis_client_obj, contract_file_dwn=contract_dwn, access_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsiZDoxIiwiZDoyIiwieDowIiwieDoxIiwieDoyIl0sImF0X2hhc2giOiJnQUFBQUFCcDhDY2Q5WG5hbVpDSDFDREtaM29lRW1nanB4ay12R3dDajkyV0UtdEhNbWV5X2NlSXc4OHd4eDhpX0RuLVVEY0g0aGZJZjY4UWd1bkl0VWFGYnFrRkJHUW1sSWV0Mll3NEx5OWVqbC1KRkVfWXVOND0iLCJkaXNwbGF5X25hbWUiOiIiLCJvbXMiOiJLMSIsImhzbV9rZXkiOiI5YTJhY2EzZDIyNjhmYzAyMzAwNzVlMGFmY2E1MTBjMWI5OTc0MjI2MTllZDg5ODg3OWI1ZWJhOSIsImlzRGRwaUVuYWJsZWQiOiJOIiwiaXNNdGZFbmFibGVkIjoiTiIsImZ5X2lkIjoiWEIxNDU2MCIsImFwcFR5cGUiOjEwMCwiZXhwIjoxNzc3NDIyNjAwLCJpYXQiOjE3NzczNDYzMzMsImlzcyI6ImFwaS5meWVycy5pbiIsIm5iZiI6MTc3NzM0NjMzMywic3ViIjoiYWNjZXNzX3Rva2VuIn0.JdcZGf06yuqo5-i7e3FjdxC-0QvBcsJgRiaH9VIpNAs")
    #
    # # --- Connecting.... ----
    # fyers_obj.connect()