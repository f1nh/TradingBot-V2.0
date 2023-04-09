import config, pandas as pd, plotly.graph_objects as go
from binance.client import Client

# Connect to the client via api key and secret
client = Client(config.API_KEY, config.API_SECRET)

# Function to get historical data from a symbol
def get_data(symbol, interval, past, client=client):
    frame = pd.DataFrame(client.get_historical_klines(symbol,
                                                      interval,
                                                      past))
    frame = frame.iloc[:, :6]
    frame.columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume']
    frame = frame.astype(float)
    frame['Time'] = pd.to_datetime(frame['Time'], unit='ms')

    return frame

# Function to define the support levels
def support(frame, l, n1, n2):
    for i in range(l-n1+1, l+1):
        if(frame.low[i]>frame.low[i-1]):
            return 0 
        
    for i in range(l+1, l+n2+1):
        if(frame.low[i]<frame.low[i-1]):
            return 0 
        
    return 1

# Function to define the resistence levels
def resistence(frame, l, n1, n2):
    for i in range(l-n1+1, l+1):
        if(frame.high[i]<frame.high[i-1]):
            return 0
        
    for i in range(l+1, l+n2+1):
        if(frame.high[i]>frame.high[i-1]):
            return 0
        
    return 1
