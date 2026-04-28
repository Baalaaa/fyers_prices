import pandas as pd

today = pd.Timestamp.now().normalize()

cols = [
    "token","description","segment","instrument_type","tick_size",
    "unknown_1","trading_session","last_update","expiry","symbol",
    "lot_size","unknown_2","strike","underlying","unknown_3",
    "unknown_4","unknown_5","unknown_6","unknown_7","unknown_8","unknown_9"
]

# --- Load CSV ---
df = pd.read_csv(r"D:\Bala\Learning\fyers_prices\NSE_FO.csv", names=cols, header=None)

# --- Convert expiry ---
df["expiry"] = pd.to_datetime(df["expiry"], unit="s", errors="coerce")

# --- Drop invalid expiry ---
df = df[df["expiry"].notna()]

# --- Detect instrument type correctly ---
df['instrument_type'] = df['symbol'].apply(
    lambda x: "OPT" if str(x).endswith(("CE", "PE"))
    else ("FUT" if "FUT" in str(x) else "UNKNOWN")
)

# --- Filter NIFTY Options only ---
underlying = ["NIFTY", "BANKNIFTY", "FINNIFTY"]
df = df[
    (df["underlying"].isin(underlying)) &
    (df["instrument_type"] == "OPT")
]

# --- Convert numeric ---
df["strike"] = pd.to_numeric(df["strike"], errors="coerce")
df["lot_size"] = pd.to_numeric(df["lot_size"], errors="coerce")

# --- Filter valid expiries ---
df = df[df["expiry"] >= today]

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

print("E1 Expiry:", e1_expiry)
print("Total Symbols:", len(options_symbols))










