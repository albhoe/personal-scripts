import json
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime as dt
import matplotlib.pyplot as plt
import os
import plotly.graph_objs as go

class Asset:
    
    def __init__(self,dict):
        self.name = dict['name']
        self.count = dict['count']
        self.avg_init_price = dict['avg_init_price']

    def get_current_price(self):
        price = yf.Ticker(self.name).history(period='1d',interval='1m').tail(1)['Close'].values[0]
        return price
    
    def compute_price(self,count):  
        return self.get_current_price()*count
    
    def buy(self,count):
        if count <= 0:
            raise ValueError("Must buy at least one share")
        
        current_unit_price = self.get_current_price()
        if self.count+count >= 0:
            # recompute average initial price for the long position.
            if self.count <= 0:
                #From short or neutral to long position. Reset initial price to current price.
                self.avg_init_price = current_unit_price
            else:
                #In Long position. Update initial price with average.
                self.avg_init_price = ((current_unit_price*count) + (self.avg_init_price * (self.count)))/(count+self.count)
        self.count += count
        return current_unit_price*count
            
    def sell(self,count):
        if count <= 0:
            raise ValueError("Must buy at least one share")
        
        current_unit_price = self.get_current_price()
        if self.count+count <= 0:
            # recompute average initial price for the short position.
            if self.count >= 0:
                #From Long or neutral to short position. Reset initial price to current price.
                self.avg_init_price = current_unit_price
            else:
                #In short position. Update initial price with average.
                self.avg_init_price = (current_unit_price*count + (self.avg_init_price * abs(self.count)))/(count+abs(self.count))
        self.count -= count
        return current_unit_price*count

    def view(self):
        current_unit_price = self.get_current_price()
        value = current_unit_price*self.count
        profit = (current_unit_price - self.avg_init_price) * self.count
        profit_percent =  ((current_unit_price/self.avg_init_price)-1) * 100
        return pd.Series({"Ticker Symbol":self.name,"Shares Owned":self.count,\
                          "Initial Price":self.avg_init_price,"Current Price":current_unit_price,\
                            "Total Value":value,"Profit":profit,"Profit %":profit_percent})

class Player:
    def __init__(self,dict):
        self.name = dict['name']
        self.cash = dict['cash']
        self.portfolio = {d['name']:Asset(d) for d in dict['portfolio'].values()} 

    def assets_to_dict(self):
        for asset in self.portfolio.keys():
            self.portfolio[asset] = self.portfolio[asset].__dict__
        return self.portfolio

    def buy(self,asset,count):
        if asset not in self.portfolio:
            self.portfolio[asset] = Asset({"name":asset,"count":0,"avg_init_price":0})

        if self.portfolio[asset].compute_price(count) <= self.cash:
            price = self.portfolio[asset].buy(count)
            self.cash -= price
            if self.portfolio[asset].count == 0:
                self.portfolio.pop(asset)
            print(f"Successully bought {count} shares for {price}")
    
    def sell(self,asset,count):
        if asset not in self.portfolio:
            self.portfolio[asset] = Asset({"name":asset,"count":0,"avg_init_price":0})
        
        price = self.portfolio[asset].sell(count)
        self.cash += price
        if self.portfolio[asset].count == 0:
            self.portfolio.pop(asset)
        print(f"Successully sold {count} shares for {price}")
    
    def list_portfolio(self):
        asset_list = [value.view() for value in dict(self.portfolio).values()]
        df = pd.DataFrame.from_records(asset_list)
        df.sort_values(by='Profit %',inplace=True)
        print(df.to_string(index=False))

        if len(df) > 0:
            total_asset_value = sum(df['Total Value'])
        else:
            total_asset_value = 0
        print(f"Total Portfolio Value: {self.cash + total_asset_value}")

#First time setup
if not os.path.exists("./savedata"):
    os.mkdir("./savedata/")
if not os.path.exists("./savedata/marketgame_save"):
    with open("./savedata/marketgame_save",'w') as f:
        player_name = input("New Player. Enter a player name:")
        starting_cash = 100000
        data = {"update_time":dt.now().timestamp(),"players":{player_name:{"name":player_name,"cash":100000,"portfolio":{}}}}
        json.dump(data,f)
else:
    player_name = "Albert Hoe"


with open("./savedata/marketgame_save",'r') as f:
    data = json.load(f)
    player = Player(data['players'][player_name])
    try:
        while(True):
            action=input("What would you like to do? (buy/sell/view/quit):")
            if action.upper() == 'BUY': 
                if dt.now().hour >= 20 or (dt.now().hour < 9 and dt.now().minute < 30) or dt.now().weekday()>=5:
                    print("Market is closed. Cannot buy/sell at this time.")
                    continue 
                ticker = input("Enter ticker symbol:").upper()
                count = int(input("Enter number of shares to buy:"))
                player.buy(ticker,count)
            if action.upper() == 'SELL':  
                if dt.now().hour >= 20 or (dt.now().hour < 9 and dt.now().minute < 30) or dt.now().weekday()>=5:
                    print("Market is closed. Cannot buy/sell at this time.")
                    continue 
                ticker = input("Enter ticker symbol:").upper()
                count = int(input("Enter number of shares to sell:"))
                player.sell(ticker,count)

            if action.upper() == 'VIEW':  
                ticker = input("Enter ticker symbol (or press enter to view all):").upper()
                if ticker == "":
                    print(f"Liquid Assets:{player.cash}")

                    player.list_portfolio()

                elif ticker == 'cash':
                    print(f"Liquid Assets:{player.cash}\n")

                elif ticker in player.portfolio:
                    print(player.portfolio[ticker].view())
                    history = yf.Ticker(ticker).history(period='1d',interval='1m')
                    history.reset_index(inplace=True)
                    history.plot(x='Datetime',y='Close',title=f"{ticker} Price History")
                    plt.show()
                else: 
                    print("Asset not found in portfolio")
                    history = yf.Ticker(ticker).history(period='1d',interval='1m')
                    history.reset_index(inplace=True)
                    print(history.columns)
                    history.plot(x='Datetime',y='Close',title=f"{ticker} Price History")
                    plt.show()

            if action.upper() == 'QUIT':
                raise KeyboardInterrupt
                
    except Exception as e:
        print(f"Exiting game. Error: {e}")
    except KeyboardInterrupt:
        print("Exiting game.")
    finally:
        with open("./savedata/marketgame_save",'w') as f:
            data['players'][player_name]['portfolio'] = player.assets_to_dict()
            data['players'][player_name] = player.__dict__
            json.dump(data,f)


