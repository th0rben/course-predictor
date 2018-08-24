import quandl
from src.login_data import quandl_key
from src.course_predictor import path
import pandas as pd
import os 
quandl.ApiConfig.api_key = quandl_key


def StockPrices():
    df = pd.DataFrame()
    statspath = path+"/intraQuarter/_KeyStats"
    stock_list= [x[0] for x in os.walk(statspath)]
    print(stock_list)
    for each_dir in stock_list[1:]:
        try:
            ticker = each_dir.split("\\")[1]
            print(ticker)
            name = "WIKI/"+ticker.upper()
            data = quandl.get(name, 
                              trim_start = "2000-12-12", 
                              trim_end = "2014-12-30", 
                              authtoken=quandl_key)
            data[ticker.upper()] = data["Adj. Close"]
            df = pd.concat([df, data[ticker.upper()]], axis = 1)
             
        except Exception as e:
            print(e)
            try:
                ticker = each_dir.split("\\")[1]
                print(ticker)
                name = "WIKI/"+ticker.upper()
                data = quandl.get(name, 
                              trim_start = "2000-12-12", 
                              trim_end = "2014-12-30", 
                              authtoken=quandl_key)
                data[ticker.upper()] = data["Adj. Close"]
                df = pd.concat([df, data[ticker.upper()]], axis = 1)
            except Exception as e:
                print(e)
                
    df.to_csv("stock_prices.csv")
    
StockPrices()