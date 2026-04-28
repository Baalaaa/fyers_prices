import io
import os
import requests
import pandas as pd

from config.loggers import logger




# ------ Class Contract File -------
class ContractFileDownloader:

    # ---- Default Constructor Func  -----
    def __init__(self):

        self.today = pd.Timestamp.now().normalize()
        self.sensex_contract_file_url = "https://public.fyers.in/sym_details/BSE_FO.csv"
        self.cash_market_file_url = "https://public.fyers.in/sym_details/NSE_FO.csv"
        self.cash_market_file_url = "https://public.fyers.in/sym_details/NSE_CM.csv"

        self.csv_columns = [  "token","description","segment","instrument_type","tick_size",
                              "unknown_1","trading_session","last_update","expiry","symbol",
                              "lot_size","unknown_2","strike","underlying","unknown_3",
                              "unknown_4","unknown_5","unknown_6","unknown_7","unknown_8","unknown_9" ]

        self.cash_market_columns =  [ "token", "description", "segment", "instrument_type",  "tick_size",
                                      "unknown_1", "trading_session", "last_update", "symbol", "unknown_2", "unknown_3",
                                      "unknown_4", "isin", "unknown_5" ]


    # ----- Nifty Contract file Downloader Func ----
    def fetch_nifty_contract_file(self) -> None:
        """Download the nifty contract file"""

        try:
            filename = os.path.join("contract_data", "nifty_contract.csv")
            response = requests.get(self.sensex_contract_file_url)
            if response.status_code == 200:
                df = pd.read_csv(io.StringIO(response.text))
                df.to_csv(filename, index=False)
                logger.info(f"nifty_contract_file.csv downloaded. ")
            else:
                logger.warning(f"Failed to download nifty contract file with status code: {response.status_code} .")

        except Exception as e:
            logger.error(e)


    # ----- Nifty current week Contract Func ----
    def fetch_nifty_current_week_expiry_contract(self) -> list:
        """Download the nifty contract file"""

        try:
            filename = os.path.join("contract_data", "nifty_contract.csv")
            nifty_df = pd.read_csv(filename, names=self.csv_columns, header=None)

            # ---- Expiry Format ----
            nifty_df["expiry"] = pd.to_datetime(nifty_df["expiry"],unit='s', errors="coerce")

            # ---- Drop Invalid Expiry ----
            sensex_df = nifty_df[nifty_df['expiry'].notna()]

            # ---- Extracting Option Type ----
            nifty_df['instrument_type'] = nifty_df['symbol'].apply(
                lambda x: "OPT" if str(x).endswith(("CE", "PE"))
                else ("FUT" if "FUT" in str(x) else "UNKNOWN")
            )

            # ---- Filtering only OPT -----
            nifty_df = nifty_df[
                (nifty_df['underlying'] == "SENSEX") &
                (nifty_df['instrument_type'] == "OPT")
            ]

            # --- Convert numeric ---
            nifty_df["strike"] = pd.to_numeric(nifty_df["strike"], errors="coerce")
            nifty_df["lot_size"] = pd.to_numeric(nifty_df["lot_size"], errors="coerce")

            # --- Filter valid expiries ---
            df = nifty_df[nifty_df["expiry"] >= self.today]

            # --- Get E1 expiry ---
            e1_expiry = sorted(df["expiry"].unique())[0]

            # --- Filter E1 only ---
            e1_df = df[df["expiry"] == e1_expiry]

            # --- Extract option type ---
            e1_df["option_type"] = e1_df["symbol"].str[-2:]

            # --- Final clean data ---
            final_df = e1_df[[
                "symbol", "underlying", "strike", "option_type", "expiry", "lot_size"
            ]]

            options_symbols = final_df["symbol"].tolist()
            logger.info(f"E1 Expiry: {e1_expiry} & Total Symbols: {len(options_symbols)}")

            return options_symbols

        except Exception as e:
            logger.error(e)
            return None


    # ----- Sensex Contract file Downloader Func ----
    def fetch_sensex_contract_file(self) -> None:
        """Download the sensex contract file"""

        try:
            filename = os.path.join("contract_data", "sensex_contract.csv")
            response = requests.get(self.sensex_contract_file_url)
            if response.status_code == 200:
                df = pd.read_csv(io.StringIO(response.text))
                df.to_csv(filename, index=False)
                logger.info(f"sensex_contract_file.csv downloaded. ")
            else:
                logger.warning(f"Failed to download sensex contract file with status code: {response.status_code} .")

        except Exception as e:
            logger.error(e)


    # ----- Sensex current week Contract Func ----
    def fetch_sensex_current_week_expiry_contract(self) -> list:
        """Download the sensex contract file"""

        try:
            filename = os.path.join("contract_data", "sensex_contract.csv")
            sensex_df = pd.read_csv(filename, names=self.csv_columns, header=None)

            # ---- Expiry Format ----
            sensex_df["expiry"] = pd.to_datetime(sensex_df["expiry"],unit='s', errors="coerce")

            # ---- Drop Invalid Expiry ----
            sensex_df = sensex_df[sensex_df['expiry'].notna()]

            # ---- Extracting Option Type ----
            sensex_df['instrument_type'] = sensex_df['symbol'].apply(
                lambda x: "OPT" if str(x).endswith(("CE", "PE"))
                else ("FUT" if "FUT" in str(x) else "UNKNOWN")
            )

            # ---- Filtering only OPT -----
            sensex_df = sensex_df[
                (sensex_df['underlying'] == "SENSEX") &
                (sensex_df['instrument_type'] == "OPT")
            ]

            # --- Convert numeric ---
            sensex_df["strike"] = pd.to_numeric(sensex_df["strike"], errors="coerce")
            sensex_df["lot_size"] = pd.to_numeric(sensex_df["lot_size"], errors="coerce")

            # --- Filter valid expiries ---
            df = sensex_df[sensex_df["expiry"] >= self.today]

            # --- Get E1 expiry ---
            e1_expiry = sorted(df["expiry"].unique())[0]

            # --- Filter E1 only ---
            e1_df = df[df["expiry"] == e1_expiry]

            # --- Extract option type ---
            e1_df["option_type"] = e1_df["symbol"].str[-2:]

            # --- Final clean data ---
            final_df = e1_df[[
                "symbol", "underlying", "strike", "option_type", "expiry", "lot_size"
            ]]

            options_symbols = final_df["symbol"].tolist()
            logger.info(f"E1 Expiry: {e1_expiry} & Total Symbols: {len(options_symbols)}")

            return options_symbols

        except Exception as e:
            logger.error(e)
            return None


    # ----- Cash Market Contract file Downloader Func ------
    def fetch_cash_market_contract_file(self) -> None:
        """Download the cash market contract file"""

        try:
            filename = os.path.join("contract_data", "cash_market_contract.csv")
            response = requests.get(self.sensex_contract_file_url)
            if response.status_code == 200:
                df = pd.read_csv(io.StringIO(response.text))
                df.to_csv(filename, index=False)
                logger.info(f"cash_market_contract.csv downloaded. ")
            else:
                logger.warning(f"Failed to download sensex contract file with status code: {response.status_code} .")

        except Exception as e:
            logger.error(e)


    # -------- Cash Market Symbol Func -------
    def fetch_cash_market_symbols(self) -> list | None:
        """Download the sensex contract file"""

        try:
            filename = os.path.join("contract_data", "cash_market_contract.csv")
            cm_df = pd.read_csv(filename, names=self.cash_market_columns, header=None)



            print(cm_df)

            # return stocks_symbols

        except Exception as e:
            logger.error(e)
            return None





