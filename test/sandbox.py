import os


from contract_files import ContractFileDownloader
from fyers_websocket import FyersServices
from redis_client import RedisClient


if __name__ == '__main__':

    # downloader = ContractFileDownloader()
    # # downloader.fetch_sensex_contract_file()
    # # downloader.fetch_sensex_current_week_expiry_contract()
    # # downloader.fetch_cash_market_contract_file()
    # downloader.fetch_cash_market_symbols()

    os.makedirs("fyers_logs", exist_ok=True)

    # --- Redis Client ---
    redis = RedisClient()
    redis.connect_remote_redis()

    # ---- Contract Download ----
    contract_dwn = ContractFileDownloader()

    # --- Fyers instance ---
    fyers_obj = FyersServices(redis_client=redis, contract_file_dwn=contract_dwn,
                              access_token="'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsiZDoxIiwiZDoyIiwieDowIiwieDoxIiwieDoyIl0sImF0X2hhc2giOiJnQUFBQUFCcC1DR0RiZlZMWWFXX2Rfd01pYllXZ0t1YUV5Rjhad3lzUVJGcDA0MWo3VEFjNTBMTXpVWUhfRk9sUTZ3c0lOdDBGU2VJMWM0YVp5Tk1WcWlWQnRDbGxZcDFqai0zb0NWQXoyUXlCM2tHMGRfQ0kxdz0iLCJkaXNwbGF5X25hbWUiOiIiLCJvbXMiOiJLMSIsImhzbV9rZXkiOiI3ODgyZGY5NDAyYmEyYjRkNjBmM2E3NzExYmMxNDM0NzM1MmExMDBlN2QyOWUyMzFiMjE5YWExNCIsImlzRGRwaUVuYWJsZWQiOiJOIiwiaXNNdGZFbmFibGVkIjoiTiIsImZ5X2lkIjoiWEIxNDU2MCIsImFwcFR5cGUiOjEwMCwiZXhwIjoxNzc3OTQxMDAwLCJpYXQiOjE3Nzc4NjkxODcsImlzcyI6ImFwaS5meWVycy5pbiIsIm5iZiI6MTc3Nzg2OTE4Nywic3ViIjoiYWNjZXNzX3Rva2VuIn0.GNTs8GZpxOBtjz7uP5XGRCSUnERNxoQdftaHgcHpSN0")

    # --- Connecting.... ----
    fyers_obj.connect()