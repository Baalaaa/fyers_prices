from constants.nifty_stock_symbol import nifty_symbol_list
from remote_redis import RedisClient












if __name__ == '__main__':
    redis = RedisClient()
    redis.connect_remote_redis()

    for sym in nifty_symbol_list:
        redis.get_stocks_feeds(symbol=sym)
