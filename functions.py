import config, pandas as pd, plotly.graph_objects as go
from binance.client import Client

client = Client(config.API_KEY, config.API_SECRET)

def get_data(symbol, interval, past, client=client):
    frame = pd.DataFrame(client.get_historical_klines(symbol,
                                                      interval,
                                                      past))
    frame = frame.iloc[:, :6]
    frame.columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume']
    frame = frame.astype(float)
    frame['Time'] = pd.to_datetime(frame['Time'], unit='ms')

    return frame

