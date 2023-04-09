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
def support(frame, l, n1, n2): # n1 n2 means how many candles before and after candle l
    for i in range(l-n1+1, l+1):
        if(frame['Low'][i]>frame['Low'][i-1]):
            return 0 
        
    for i in range(l+1, l+n2+1):
        if(frame['Low'][i]<frame['Low'][i-1]):
            return 0 
        
    return 1

# Function to define the resistence levels
def resistence(frame, l, n1, n2): # n1 n2 means how many candles before and after candle l
    for i in range(l-n1+1, l+1):
        if(frame['High'][i]<frame['High'][i-1]):
            return 0
        
    for i in range(l+1, l+n2+1):
        if(frame['High'][i]>frame['High'][i-1]):
            return 0
        
    return 1

# Plotting the support resistence levels on the chart
frame = get_data(symbol='BTCUSDT', interval='15m', past='1 week ago UTC')

sr = []
n1 = 3
n2 = 2

for row in range(3, 205):
    if support(frame, row, n1, n2):
        sr.append((row, frame['Low'][row], 1))
    if resistence(frame, row, n1, n2):
        sr.append((row, frame['High'][row], 2))

print(sr)

s = 0
e = 200
dfpl = frame[s:e]

fig = go.Figure(data=[go.Candlestick(x=dfpl.index,
                                     open=dfpl['Open'],
                                     high=dfpl['High'],
                                     low=dfpl['Low'],
                                     close=dfpl['Close'])])
c = 0
while(1):
    if(c>len(sr)-1):
        break
    
    fig.add_shape(type='line',
                  x0=s,
                  y0=sr[c][1],
                  x1=e,
                  y1=sr[c][1])
    c+=1
    
fig.show()