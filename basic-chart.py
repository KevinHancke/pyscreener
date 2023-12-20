import pandas as pd
import pandas_ta as ta
import yfinance as yf
from lightweight_charts import Chart

if __name__ == '__main__':
    
    chart = Chart()
    
    df = pd.read_csv('Binance_BTCUSDT_1min.csv')
    df = df.iloc[:,:6]
    df.columns=['time','open', 'high', 'low', 'close', 'volume']
    df.reset_index(drop=True, inplace=True)
    df.time = pd.to_datetime(df.time)
    df = df.set_index("time")
    df = df.tail(50)

    chart.set(df)

    chart.watermark('BTC-1m')
    
    chart.show(block=True)