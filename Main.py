"""
a gofundme donation caluclator to figure out what you should donate
in order for the recipient to receive the full amount intended. Also to convert 
between currency as needed
 """
from abc import ABC
from datetime import datetime
from enum import Enum
#class of api calling
#class for mock data service
#class for data handler (contain csv, check if needs updating to call api, update db, then query db) 

"""???????"""
class ENVIRONMENT(Enum):
    PRODUCTION=1
    DEV=2


class AbstractCurrencyService(ABC):
    """barebones of the api calling class and the backup data class"""
    @abstractmethod
    def populateCSV():
        #smth smth smth
        pass
    def compareDateTime():
        #to see if it is time to call api again
        #compare current datetime (utc) with api's "time of next update" (utc)
        pass

class APIService(AbstractCurrencyService):
    url='https://open.er-api.com/v6/latest/USD'
    #will need to overwrite csv every time 
    def populateCSV():
         #smth smth smth
        pass
    def compareDateTime():
        #to see if it is time to call api again
        #compare current datetime (utc) with api's "time of next update" (utc)
        pass

"""
Mock Data Handler Class in case API not working
"""
class MockDataService(AbstractCurrencyService):
    #will need to overwrite csv every time
    def populateCSV():
        #overwrite csv to input TEST:0.5
          #smth smth smth
        print("API not connected")
        pass


##OK I think this is if you are having someone log in
#ok change this to build the environment based on the code
#returned from the API
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

#gofundme fees, 2.9% + $.30usd
feePercentage=.029
flatFeeAddOn=.3 #will need to convert this when converting currency
#amountIntended
#floatIntended
print("Converting between any currencies? Y or N")
converting=input()
#if yes
if(converting == "Y" or converting =="y"):
    #so far im only doing USD as the donator currency
        #print("Please type in the abbreviation of the currency in which you use")
        #print("eg. USD, GBP, IQD, etc")
        #userCurrency=input()
    print("Please type in the abbreviation of the currency in which the donation will be received")
    donationCurrency=input()
    amountIntended=input("How much do you want the fundee to receive in their currency: ")
    ##this might be better to do in oop so it is easier to mix and match conversions instead of making
    #infinite if statements
    #or an api?? idk if possible
    floatIntended=float(amountIntended)
    #convert here
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