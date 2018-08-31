import urllib.request
import os
import time

path = "C:/Users/bav9158/git/course-predictor/data/intraQuarter"

def Check_Yahoo():
    statspath = path+'/_KeyStats'
    stock_list = [x[0] for x in os.walk(statspath)]

    ## Added a counter to call out how many files we've already added
    counter = 0
    for e in stock_list[1:]:

        try:
            e = e.replace(statspath+"\\","")
            ## Changed the URL & added the modules
            link = "https://query2.finance.yahoo.com/v10/finance/quoteSummary/"+e.upper()+"?modules=assetProfile,financialData,defaultKeyStatistics,calendarEvents,incomeStatementHistory,cashflowStatementHistory,balanceSheetHistory"
            #https://query2.finance.yahoo.com/v10/finance/quoteSummary/abc?modules=assetProfile,financialData,defaultKeyStatistics,calendarEvents,incomeStatementHistory,cashflowStatementHistory,balanceSheetHistory
            #https://query2.finance.yahoo.com/v10/finance/quoteSummary/abc?function=TIME_SERIES_WEEKLY_ADJUSTED&modules=assetProfile,financialData,defaultKeyStatistics,calendarEvents,incomeStatementHistory,cashflowStatementHistory,balanceSheetHistory
            resp = urllib.request.urlopen(link).read()
            ## We go by Bond. JSON Bond
            save = "C:/Users/bav9158/git/course-predictor/data/yahoo/"+str(e)+".json"
            store = open(save,"w")
            store.write(str(resp))
            store.close()
            ## Print some stuff while working. Communication is key
            counter +=1
            print("Stored "+ e +".json")
            print("We now have "+str(counter)+" JSON files in the directory.")
    
    
        except Exception as e:
            print(str(e))
            time.sleep(2)
            
Check_Yahoo()