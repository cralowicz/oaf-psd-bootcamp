"""
a gofundme donation caluclator to figure out what you should donate
in order for the recipient to receive the full amount intended. Also to convert 
between currency as needed
 """
from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
import csv
import sqlite3
import requests
import json
from datetime import datetime,timezone
#class of api calling
#class for mock data service
#class for data handler (contain csv, check if needs updating to call api, update db, then query db) 




class AbstractCurrencyService(ABC):
    """barebones of the api calling class and the backup data class"""
    @abstractmethod
    def updateDatetimes():
       """create and/or update the csv"""
    pass
    @abstractmethod
    def compareDateTime():
        """to see if it is time to call api again
        #compare current datetime (utc) with api's "time of next update" (utc)"""
        pass
    @abstractmethod
    def updateDB():
        """to see if it is time to call api again
        #compare current datetime (utc) with api's "time of next update" (utc)"""
        pass
   #should i just open the api in the main method and call methods in response to it opening or nah?
    @abstractmethod
    def openAPI():
        """to see if it is time to call api again
        #compare current datetime (utc) with api's "time of next update" (utc)"""
        pass
    

class APIService(AbstractCurrencyService):
    url='https://open.er-api.com/v6/latest/USD'
  
    def get_currency_data()->requests:
        url='https://open.er-api.com/v6/latest/USD'
        response=requests.get(url)
        #print(type(response))
        if response.status_code==200:
       # print(response)
            data=response.json()
            rates=data['rates']
            try:
                for country in rates.keys():
                    update_query="""UPDATE rates SET rate = ? WHERE currency = ?"""
                    #print(values)
                    cur.execute(update_query, (rates[country],country ))
                    con.commit()
                    
            except sqlite3.Error as error:
                print("Failed to update MySQL table {}".format(error))
            res=cur.execute("SELECT * FROM rates")
            print(res.fetchall())

            #update datetime csv here too
            return response
        else:
            # print(response)
            return response
        
    def updateDatetimes():
        #update csv
        pass
    def compareDateTime()->bool:
        print("\nReading csv\n")
        with open('C:\\Users\\ckral\\oaf-psd-bootcamp\\currency.csv',mode='r') as file:
            csvFile=csv.reader(file)
            for lines in csvFile:
                l=lines[0]
                if (l=="time_next_update_utc"):
                    nextUpdate=lines[1]
                #if(l=="time_last_update_utc"):
                 #   lastUpdate=lines[1]
            
        currentDT = datetime.now(timezone.utc)
        update=datetime.strptime(nextUpdate, '%d %b %Y %X %z')
       # prevUpdate=datetime.strptime(lastUpdate,'%d %b %Y %X %z')
        # update=update.strftime('%d %b %Y %X %z')   
        #if(currentDT>prevUpdate):
         #   print("\ncurrent time later than last update")
        #else:
         #   print("\ncurrent time is before last update...somehow...?")
        if(currentDT<update):
            #not time to update
            print("not yet")
            return False
        elif(update<currentDT):
            #time to update
            print("time for an update")
            return True
        
    def updateDB(con, cur):
      #make this the name of get_currency_data? idek if this is going to work 
        pass

"""
Mock Data Handler Class in case API not working
"""
class MockDataService(AbstractCurrencyService):
    #will need to overwrite csv every time
    def updateDB():
        print("API not connected-out of date exchange rates in use")
       


##I took this from the eg but I think this is if you are having someone log in
#ok change this to build the environment based on the code
#returned from the API
"""???????"""
class ENVIRONMENT(Enum):
    PRODUCTION=1
    DEV=2

class ServiceFactory():
    def buildService(name:ENVIRONMENT)->AbstractCurrencyService:
        if(name==ENVIRONMENT.DEV):
            return MockDataService()
        elif (name==ENVIRONMENT.PRODUCTION):
            return APIService()
        else:
            return "unspecified name"
    
"""
Main
"""
#1)check if update datetime align
# A)if yes, call api and get response
#   1)if api response is 200, update the db and csv and use API service
#   2)if api response is NOT 200 use mock data service (which will just provide un-updated db with warning)
# B)if no, do not call api and proceed with program
tf=APIService.compareDateTime()
print(tf)
if(tf==True):
    #call aip
    apiValidation=APIService.get_currency_data()
    print(apiValidation)
    if(apiValidation.status_code==200):
        print("use api ")
        con = sqlite3.connect("currencyRates.db")
        cur = con.cursor()
        APIService.updateDB(con, cur)
    else:
        print("use mock")
        MockDataService.updateDB()
elif(tf==False):
    #go ahead with program
    pass

#gofundme fees, 2.9% + $.30usd
feePercentage=.029
flatFeeAddOn=.3 #will need to convert this when converting currency
print("Converting between any currencies? Y or N")
converting=input()
#if yes
if(converting == "Y" or converting =="y"):
    #so far im only doing USD as the donator currency
   
    print("Please type in the abbreviation of the currency in which the donation will be received")
    donationCurrency=input()
    amountIntended=input("How much do you want the fundee to receive in their currency: ")
    floatIntended=float(amountIntended)
    lowerCaseCurrency=donationCurrency.lower()

    """
    Change this: 
    calculate fees first, then convert
    """
    if(lowerCaseCurrency=="gbp"):
        #1 gbp = 1.30 usd
        floatIntended=float(amountIntended)
        amountToDonate=(floatIntended*feePercentage) +(.3*1.30)+floatIntended 
        amountToDonateUSD=amountToDonate*1.30 #this turns it into usd
        print("You need to donate at least", amountToDonate, "GBP, which is ", amountToDonateUSD, "USD")
    if(lowerCaseCurrency=="eur"):
        #1 eur = 1.09 usd
        floatIntended=float(amountIntended)
        amountToDonate=(floatIntended*feePercentage) +(.3*1.09)+floatIntended
        amountToDonateUSD=amountToDonate*1.09 #this turns it into usd
        print("You need to donate at least",amountToDonate, "EUR, which is ", amountToDonateUSD, "USD")
    if(lowerCaseCurrency=="cad"):
        #1 gbp = 0.73 usd
        floatIntended=float(amountIntended)
        amountToDonate=(floatIntended*feePercentage) +(.3*.73)+floatIntended
        amountToDonateUSD=amountToDonate*.73 #this turns it into usd
        print("You need to donate at least", amountToDonate , "CAD, which is ", amountToDonateUSD, "USD")
    else:
        print("Unknown currency")
        exit
else:
    amountIntended=input("How much do you want the fundee to receive: ")
    floatIntended=float(amountIntended)
    amountToDonate=(floatIntended*feePercentage) +.3+floatIntended
    print("You need to donate at least", amountToDonate, "USD")


print("End of program")
exit