# https://hk29.hatenablog.jp/entry/2020/04/25/170130

import sys
from yahoo_finance_api2 import share
from yahoo_finance_api2.exceptions import YahooFinanceError
from pandas_datareader import data
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from common.make_log import setup_logger

logger = setup_logger(__name__)

def company_stock(period_type, period, company_code):
    my_share = share.Share(company_code + '.T')
    symbol_data = None

    try:
        symbol_data = my_share.get_historical(share.PERIOD_TYPE_DAY,
                                            period_type,
                                            share.FREQUENCY_TYPE_MINUTE,
                                            period)
    except YahooFinanceError as e:
        logger.error(e.message)
        sys.exit(1)

    from datetime import datetime, timezone, timedelta

    date = symbol_data["timestamp"]

    old_datetime = datetime.fromtimestamp(date[0]/1000)
    now_datetime = datetime.fromtimestamp(date[len(date) - 1]/1000)

    old_date = old_datetime.strftime('%Y-%m-%d')
    now_date = now_datetime.strftime('%Y-%m-%d')

    old_time = old_datetime.strftime('%H:%M:%S')
    now_time = now_datetime.strftime('%H:%M:%S')

    

    price = symbol_data["close"]
    old_price = price[0]
    now_price = price[len(date) - 1]
    logger.info(str(old_time) + "の時の株価： " + str(old_price))
    logger.info(str(now_time) + "の時の株価： " + str(now_price))

    body = [
        [old_date, old_time, str(old_price)],
        [now_date, now_time, str(now_price)]
    ]

    df = pd.DataFrame(symbol_data.values(), index=symbol_data.keys()).T
    df.timestamp = pd.to_datetime(df.timestamp, unit='ms')
    df.index = pd.DatetimeIndex(df.timestamp, name='timestamp').tz_localize('UTC').tz_convert('Asia/Tokyo')

    plt.figure(figsize=(10 ,5))
    plt.title(company_code, color='black', size=15, loc='center') # title(タイトル, 線の色, 背景色, フォントサイズ,　タイトル位置)
    plt.plot(df.index, price, label='close', color='blue')
    # plt.show()
    return body

# plt.figure(figsize=(10 ,5))

# import time

# company_stock(2, 1, '9201.T')