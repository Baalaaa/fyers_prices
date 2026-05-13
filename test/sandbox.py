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
                              access_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsiZDoxIiwiZDoyIiwieDowIiwieDoxIiwieDoyIl0sImF0X2hhc2giOiJnQUFBQUFCcUFfQ3lTdWdTRDJtWlFjLUk3amROcVNqbHVJLW1yTHRsaFBSTGdhUTdxRXJib19NX0x6cWdneHhld2o4Nk9KYWdHa2VFZ3FxTFhqZjBteXJELVhGV1BxRlBMRHAtQ3VwWlRJYWxfUVBFVkNrS1R1Zz0iLCJkaXNwbGF5X25hbWUiOiIiLCJvbXMiOiJLMSIsImhzbV9rZXkiOiJlMmUzNTU5ZGE5ZTdjMTI4NjcyM2VmNTJkNjA5MDcwNjZjODUyZTVhNTc5MTUyMzBlOGJmMmU0ZSIsImlzRGRwaUVuYWJsZWQiOiJOIiwiaXNNdGZFbmFibGVkIjoiTiIsImZ5X2lkIjoiWEIxNDU2MCIsImFwcFR5cGUiOjEwMCwiZXhwIjoxNzc4NzE4NjAwLCJpYXQiOjE3Nzg2NDMxMjIsImlzcyI6ImFwaS5meWVycy5pbiIsIm5iZiI6MTc3ODY0MzEyMiwic3ViIjoiYWNjZXNzX3Rva2VuIn0.GiUDuYDWe_zRm3NOrvabrvMr5Oy7nkERRDGghvYso8w")

    # --- Connecting.... ----
    fyers_obj.connect()