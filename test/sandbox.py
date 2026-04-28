from contract_files import ContractFileDownloader



















if __name__ == '__main__':
    downloader = ContractFileDownloader()
    downloader.fetch_sensex_contract_file()
    downloader.fetch_sensex_current_week_expiry_contract()
    downloader.fetch_cash_market_contract_file()
    downloader.fetch_cash_market_symbols()