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

frame = get_data(symbol='BTCUSDT', interval='15m', past='1 week ago UTC')

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

# Functions to identify the Engulfing candle patterns

def Revsignal1(frame):
    length = len(frame)
    high = list(frame['High'])
    low = list(frame['Low'])
    close = list(frame['Close'])
    open = list(frame['Open'])
    signal = [0] * length
    bodyframe = [0] * length

    for row in range(1, length):
        bodyframe[row] = abs(open[row]-close[row])
        bodyframemin = 0.003
        if (bodyframe[row]>bodyframemin and bodyframe[row-1]>bodyframemin and
            open[row-1]<close[row-1] and
            open[row]>close[row] and
            (open[row]-close[row-1])>=+0e-5 and close[row]<open[row-1]):
            signal[row] = 1
        elif (bodyframe[row]>bodyframemin and bodyframe[row-1]>bodyframemin and
              open[row-1]>close[row-1] and
              open[row]<close[row] and
              (open[row]-close[row-1])<=-0e-5 and close[row]>open[row-1]):
            signal[row] = 2
        else:
            signal[row] = 0

    return signal

# Plotting the support resistence levels on the chart

sr = []
n1 = 3
n2 = 2

for row in range(3, 205):
    if support(frame, row, n1, n2):
        sr.append((row, frame['Low'][row], 1))
    if resistence(frame, row, n1, n2):
        sr.append((row, frame['High'][row], 2))

# merging the levels
plotlist1 = [x[1] for x in sr if x[2]==1]
plotlist2 = [x[1] for x in sr if x[2]==2]
plotlist1.sort()
plotlist2.sort()

for i in range(1, len(plotlist1)):
    if(i>=len(plotlist1)):
        break

    if abs(plotlist1[i]-plotlist1[i-1])<=1.005:
        plotlist1.pop(i)

for i in range(1, len(plotlist2)):
    if(i>=len(plotlist2)):
        break

    if abs(plotlist2[i]-plotlist2[i-1])<=1.005:
        plotlist2.pop(i)

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
    if(c>len(plotlist1)-1):
        break
    
    fig.add_shape(type='line',
                  x0=s,
                  y0=plotlist1[c],
                  x1=e,
                  y1=plotlist1[c],
                  line=dict(color='darkred', width=1))
    c+=1

c=0
while(1):
    if(c>len(plotlist2)-1):
        break
    
    fig.add_shape(type='line',
                  x0=s,
                  y0=plotlist2[c],
                  x1=e,
                  y1=plotlist2[c],
                  line=dict(color='darkgreen', width=1))
    c+=1

fig.show()