from datetime import datetime
import backtrader as bt
#import matplotlib.pyplot as plt 

# Create a subclass of Strategy to define the indicators and logic

class SmaCross(bt.Strategy):
# Create a subclass of SignalStrategy to define the indicators and signals
#class SmaCross(bt.SignalStrategy):

    # list of parameters which are configurable for the strategy
    params = dict(
        pfast=10, # period for the fast moving average
        pslow=30  # period for the slow moving average
    )

    def __init__(self):
        sma1 = bt.ind.SMA(period=self.p.pfast) # fast moving average
        sma2 = bt.ind.SMA(period=self.p.pslow) # slow moving average
        self.crossover = bt.ind.CrossOver(sma1, sma2) # crossover signal
        #crossover = bt.ind.CrossOver(sma1, sma2) # crossover signal
        #self.signal_add(bt.SIGNAL_LONG, crossover) # use it as LONG signal

    def next(self):
        if not self.position: # not in the market
            if self.crossover > 0: # if fast crosses slow to the upside
                self.buy() # enter long
                #self.order_target_size(target=1) # enter long

        elif self.crossover < 0: # in the market & cross to the downside
            self.close() # close long position
            #self.order_target_size(target=0) # close long position

def main():
    # create a "Cerebro" engine instance
    cerebro = bt.Cerebro() 
    # Create a data feed
    data = bt.feeds.YahooFinanceData(dataname='TSLA',
                                     fromdate=datetime(2020, 1, 1),
                                     todate=datetime(2020, 12, 31))
    # Add the data feed
    cerebro.adddata(data) 
    # Add the trading strategy
    cerebro.addstrategy(SmaCross) 
    # run it all
    cerebro.run() 
    # and plot it with a single command
    cerebro.plot() 

if __name__ == '__main__':
    main()
