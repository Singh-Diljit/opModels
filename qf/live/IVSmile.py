import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def days(date): #expand to trading days etc based on best principals
    date_format = "%Y-%m-%d"
    a = datetime.strptime('2022-05-08', date_format) #fix it to today date
    b = datetime.strptime(date, date_format)
    delta = b - a
    return delta.days

def options_chain(symbol):

    tk = yf.Ticker(symbol)
    # Expiration dates
    exps = tk.options
    # Get options for each expiration
    options = pd.DataFrame()
    for e in exps:
        opt = tk.option_chain(e)
        opt = pd.DataFrame().append(opt.calls).append(opt.puts)
        opt['expirationDate'] = e
        options = options.append(opt, ignore_index=True)
    # Bizarre error in yfinance that gives the wrong expiration date
    # Add 1 day to get the correct expiration date
    #options['expirationDate'] =
    #pd.to_datetime(options['expirationDate']) + datetime.timedelta(days = 1)
    #options['dte'] =
    #(options['expirationDate'] - datetime.datetime.today()).dt.days / 365
    
    # Boolean column if the option is a CALL
    options['CALL'] = options['contractSymbol'].str[4:].apply(
        lambda x: "C" in x)
    
    options[['bid', 'ask', 'strike']] = options[['bid', 'ask', 'strike']].apply(pd.to_numeric)
    options['mark'] = (options['bid'] + options['ask']) / 2 # Calculate the midpoint of the bid-ask
    
    # Drop unnecessary and meaningless columns
    options = options.drop(columns = ['contractSize', 'currency', 'change', 'percentChange', 'lastTradeDate', 'lastPrice'])

    return options

test = options_chain('AAPL')
test = test[(test['CALL']== True)]
req = pd.DataFrame()
req['strike'] = test['strike']
req['T'] = [days(x) for x in test['expirationDate']]
req['IV'] = test['impliedVolatility']

threedee = plt.figure().gca(projection='3d')
threedee.scatter(req['strike'], req['T'], req['IV'])
threedee.set_xlabel('strike')
threedee.set_ylabel('Time')
threedee.set_zlabel('IV')
plt.show()

plt.show()

def option_chain(symbol):

    stock = yf.Ticker(symbol)

    options = pd.DataFrame()
    for date in stock.options:
        opt = pd.DataFrame().append(stock.option_chain(date).calls)
        opt['Time'] = days(date)
        options = options.append(opt, ignore_index = True) #what does ignore do?

    return options
    
options = option_chain('AAPL')
data = pd.DataFrame()
data['strike'] = [x for x in options['strike'] if 50 < x < 250]
data['Time'] = options['Time']
data['iv'] = options['impliedVolatility']

from matplotlib import cm
from sys import argv

fig = plt.figure()
ax = fig.gca(projection='3d')
ax.set_xlabel('strike')
ax.set_ylabel('time')
ax.set_zlabel('vol')
#ax = Axes3D(fig)
surf = ax.plot_trisurf(data['strike'], data['Time'], data['iv'], cmap=cm.jet, linewidth=0.1)
fig.colorbar(surf, shrink=0.5, aspect=5)
plt.savefig('teste.pdf')
plt.show()


from matplotlib import pyplot as plt
from mpl_toolkits import mplot3d
import numpy as np
from statistics import NormalDist as normal

#From BSM File
def volSurface(optionPrice, spotPrice, intRate, dividend,
               strikeRange=.2, timeInterval=2, steps=10):
    """Graph the BSM implied volatility vs time vs strike."""
    time = [timeInterval/steps * i for i in range(1, steps+2)]
    strike = [spotPrice - strikeRange/2 + strikeRange/steps * i for i in range(1, steps+2)]
    impliedVol = [(T_, S_, vol(optionPrice, spotPrice, S_, intRate, T_, dividend))
                    for S_ in strike for T_ in time]

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot3D([x[0] for x in impliedVol], [x[1] for x in impliedVol], [x[2] for x in impliedVol])

    # Show the plot
    plt.show()
