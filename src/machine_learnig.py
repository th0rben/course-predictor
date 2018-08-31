import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm, preprocessing
import pandas as pd
from collections import Counter
#from matplotlib import style
#import statistics﻿
#style.use("ggplot")


how_much_better = 10

FEATURES = ['DE Ratio', 
            'Trailing P/E', 
            'Price/Sales', 
            'Price/Book', 
            'Profit Margin', 
            'Operating Margin', 
            'Return on Assets', 
            'Return on Equity', 
            'Revenue Per Share', 
            'Market Cap', 
            'Enterprise Value', 
            'Forward P/E', 
            'PEG Ratio', 
            'Enterprise Value/Revenue', 
            'Enterprise Value/EBITDA', 
            'Revenue', 
            'Gross Profit', 
            'EBITDA', 
            'Net Income Avl to Common ', 
            'Diluted EPS', 
            'Earnings Growth', 
            'Revenue Growth', 
            'Total Cash', 
            'Total Cash Per Share', 
            'Total Debt', 
            'Current Ratio', 
            'Book Value Per Share', 
            'Cash Flow', 
            'Beta', 
            'Held by Insiders', 
            'Held by Institutions', 
            'Shares Short (as of', 
            'Short Ratio', 
            'Short % of Float', 
            'Shares Short (prior ']

def Status_Calc(stock, sp500):
    difference = stock - sp500
    if difference > how_much_better:
        return 1
    else:
        return 0


def Build_Data_Set():
    data_df = pd.read_csv("key_stats_acc_perf_WITH_NA.csv")

    #data_df = data_df[:100]
    data_df = data_df.reindex(np.random.permutation(data_df.index))
    data_df = data_df.fillna(0).replace("N/A",0)

    data_df["Status2"] = list(map(Status_Calc, data_df["stock_p_change"], data_df["sp500_p_change"]))
    X = np.array(data_df[FEATURES].values)#.tolist())
    y = (data_df["Status2"]
         .replace("underperform",0)
         .replace("outperform",1)
         .values.tolist()) 
    X = preprocessing.scale(X)
    
    z = np.array(data_df[["stock_p_change","sp500_p_change"]])

    return X,y,z

def analysis_print(analysis):
    print("Accuracy:", (analysis["correct_count"]/analysis["test_size"]) * 100.00)
    print("Total Trades:", analysis["total_invests"])
    print("Ending with Strategy:",analysis["if_strat"])
    print("Ending with Market:",analysis["if_market"])
     
    compared = ((analysis["if_strat"] - analysis["if_market"]) /analysis["if_market"]) * 100.0
    do_nothing = analysis["total_invests"] * analysis["invest_amount"]
     
    avg_market = ((analysis["if_market"] - do_nothing) / do_nothing) * 100.0
    avg_strat = ((analysis["if_strat"] - do_nothing) / do_nothing) * 100.0
     
    print("Compared to market, we earn",str(compared)+"% more")
    print("Average investment return:",str(avg_strat)+"%")
    print("Average market return:",str(avg_market)+"%")

def Analysis():
    analysis = {}
    analysis["test_size"] = 1000
    analysis["invest_amount"] = 10000
    analysis["total_invests"] = 0
    # if invested in market (e. g. index fonds)
    analysis["if_market"] = 0
    # if invested with strategy
    analysis["if_strat"] = 0
    
    X, y, Z = Build_Data_Set()
    print(len(X))

    
    clf = svm.SVC(kernel="linear", C= 1.0)
    clf.fit(X[:-analysis["test_size"]],y[:-analysis["test_size"]])

    analysis["correct_count"] = 0 
    
    for x in range(1, analysis["test_size"]+1):
        # boxed in an array, for using clf.predict(data)later
        data = [X[-x]]
        prediction = clf.predict(data)[0]
        if (prediction==y[-x]):
            analysis["correct_count"] += 1
        if (prediction == 1):
            invest_return = analysis["invest_amount"] + (analysis["invest_amount"] * (Z[-x][0]/100))
            market_return = analysis["invest_amount"] + (analysis["invest_amount"] * (Z[-x][1]/100))
            analysis["total_invests"] += 1
            analysis["if_market"] += market_return
            analysis["if_strat"] += invest_return


    analysis_print(analysis)
    data_df = pd.read_csv("forward_sample_WITH_NA.csv")
    data_df = data_df.fillna(0).replace("N/A",0)
    
    X = np.array(data_df[FEATURES].values.tolist())
    X = preprocessing.scale(X)
    Z = data_df["Ticker"].values.tolist()
    
    invest_list = []
    not_invest_list = []
    for i in range(len(X)):
        data = [X[i]]
        prediction = clf.predict(data)[0]
        if prediction == 1:
            invest_list.append(Z[i])
        else:
            not_invest_list.append(Z[i])
    
    print(len(invest_list)/len(Z)*100,'% of the stocks are',how_much_better,'% better than the rest')
    return invest_list

print(Analysis())



#===============================================================================
# final_list = []
# 
# loops = 2
# 
# for x in range(loops):
#     stock_list = Analysis()
#     for e in stock_list:
#         final_list.append(e)
# 
# x = Counter(final_list)
# 
# print(15*"_")
# for each in x:
#     if x[each] > loops - (loops/3):
#         print(each)
#===============================================================================