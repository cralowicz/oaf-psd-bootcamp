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
    @abstractmethod
    def get_rate(currency)->float:
        """get rate"""
        pass
    @abstractmethod
    def check_for_currency(currency)->bool:
        """return false if input is not in db"""

class APIService(AbstractCurrencyService):
    url='https://open.er-api.com/v6/latest/USD'
  
    def get_currency_data(cur, con)->requests:
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
            nextUpdate=data['time_next_update_utc']
            last_update=data['time_last_update_utc']
            lastUpdate=datetime.strptime(last_update, '%a, %d %b %Y %X %z')
            #lastUpdate.strftime('%d %b %Y %X %z')
            update=datetime.strptime(nextUpdate, '%a, %d %b %Y %X %z')
            #update.strftime('%d %b %Y %X %z') 
            print(update)
            print(update.strftime('%d %b %Y %X %z') )
            update_data={'time_last_update_utc':lastUpdate.strftime('%d %b %Y %X %z'),'time_next_update_utc': update.strftime('%d %b %Y %X %z') }
            APIService.updateDatetimes(update_data)
            return response
        else:
            # print(response)
            return response
        
    def updateDatetimes(update_data):
        with open('C:\\Users\\ckral\\oaf-psd-bootcamp\\currency.csv', 'w') as currency_csv:
            for date in update_data.keys():
                 print(date)
                 currency_csv.write("%s,%s\n" %(date, update_data[date]))  
               
        currency_csv.close()
        #update csv
        pass
    def compareDateTime()->bool:
        #NEED TO SAVE DATETIME OF LAST TIME THE DB WAS UPDATED maybe still not sure
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
        print(currentDT)
        print(update)
        if(currentDT<update):
            #not time to update
            print("not yet")
            return False
        elif(update<currentDT):
            #time to update
            print("time for an update")
            return True
        
    #function to get currency input
    def getCurrency():
        print("Please type in the abbreviation of the currency in which the donation will be received")
        donorCurrency= input()
        donCurrCaps = donorCurrency.upper()
        print(donCurrCaps)
        return donCurrCaps
    
    #function to return rate
    def currencyRate(dc, cur):
    #sql query to get rate inserting currency into where clause
        res=cur.execute("SELECT rate FROM rates WHERE currency = ?", (dc,))
        x = res.fetchall()

        #x is a list of tuples, need to separate out rate as float
        conversionRate = x[0][0]
        return conversionRate
    
    def check_for_currency(dc, cur)->bool:
        #sql query to return a boolean
        res=cur.execute("SELECT rate FROM rates WHERE currency = ?", (dc,))
        queryBool = res.fetchone() is not None

        #this if statement handles returning the rate as float
        if queryBool is True:
            print (f'Currency is {dc}')
            return float(APIService.currencyRate(dc,cur))

        #if the currency doesn't exist it gives the user an error
        else:
            print ('Currency does not exist.')
"""
Mock Data Handler Class in case API not working
"""
class MockDataService(AbstractCurrencyService):
    #will need to overwrite csv every time
    def updateDB():
        print("API not connected-out of date exchange rates in use")
       
    def get_rate(currency)->float:
        """get rate"""
        pass
    def check_for_currency(currency)->bool:
        """return false if input is not in db"""


    
"""
Main
"""
#1)check if update datetime align
# A)if yes, call api and get response
#   1)if api response is 200, update the db and csv and use API service
#   2)if api response is NOT 200 use mock data service (which will just provide un-updated db with warning)
# B)if no, do not call api and proceed with program


#gofundme fees, 2.9% + $.30usd
feePercentage=.029
flatFeeAddOn=.3 #will need to convert this when converting currency

print("Converting between any currencies? Y or N")
converting=input()
#if yes
if(converting == "Y" or converting =="y"):
    con = sqlite3.connect("currencyRates.db")
    cur = con.cursor()
    tf=APIService.compareDateTime()
    if(tf==True):
        #call aip
        apiValidation=APIService.get_currency_data(cur, con) #db is now up to date
        print(apiValidation)
        if(apiValidation.status_code==200):
            print("use api ")
            user_input=APIService.getCurrency()
            xchange_rate=APIService.check_for_currency(user_input, cur)
            
        else:
            print("use mock")
            MockDataService.updateDB()
    elif(tf==False):
        user_input=APIService.getCurrency()
        xchange_rate=APIService.check_for_currency(user_input,cur)
 
        
    #if the currency is invalid it won't return a float
    #while loop forces user to input valid abbreviation
    while type(xchange_rate) != float:
        #allow user to exit program
        print("Would you like to try again?")
        exitQuestion = input("Y/N: ")

        if exitQuestion.upper() == "N":
            print("End of program")
            exit()
        elif exitQuestion.upper() == "Y":
            user_input = APIService.getCurrency()
            xchange_rate = APIService.check_for_currency(user_input,cur)


    amountIntended=input("How much do you want the fundee to receive in their currency: ")
    floatIntended=float(amountIntended)

    amountToDonate=(floatIntended*feePercentage) +(.3*xchange_rate)+floatIntended 
    amountToDonateUSD=amountToDonate*(xchange_rate) #this turns it into usd
    print(user_input)
    print("You need to donate at least", amountToDonate, user_input,", which is ", amountToDonateUSD, "USD")

else:
#no currency   
    amountIntended=input("How much do you want the fundee to receive: ")
    floatIntended=float(amountIntended)
    amountToDonate=(floatIntended*feePercentage) +.3+floatIntended
    print("You need to donate at least", amountToDonate, "USD")


print("End of program")
exit