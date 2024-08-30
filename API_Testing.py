""" testing api 
thanks to https://www.exchangerate-api.com/docs/free """

import requests
import json
from datetime import datetime,timezone
import os
import csv
import sqlite3
con = sqlite3.connect("currencyRates.db")
cur = con.cursor()

def get_currency_data():
    url='https://open.er-api.com/v6/latest/USD'
    url2='https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m'
    response=requests.get(url)
    print(response)
    if response.status_code==200:
        print(response)
        data=response.json()
        #print(json.dumps(data, indent=4, sort_keys=True))
      

        currentDT = datetime.now(timezone.utc)
        #currentDT.strftime('%a, %d %b %Y %X %z')
        nextUpdate=data['time_next_update_utc']
        print("\nCurrent date time "+str(currentDT) )
        print("\nNext api update "+nextUpdate)
        last_update=data['time_last_update_utc']
        update_data={'time_last_update_utc':data['time_last_update_utc'],'time_next_update_utc':data['time_next_update_utc']}
        
        lastUpdate=datetime.strptime(last_update, '%a, %d %b %Y %X %z')
        update=datetime.strptime(nextUpdate, '%a, %d %b %Y %X %z')
        rates=data['rates']
        """if(currentDT<update):
            print("not yet")
        elif(update<currentDT):
            print("time for an update")
        if(currentDT>lastUpdate):
            print("\ncurrent time later than last update")
        else:
            print("\nno")"""
#writing csv
        try:
            for country in rates.keys():
                insert_query="""INSERT INTO rates (currency, rate)
                VALUES (?, ?)"""
                #print(values)
                cur.execute(insert_query, (country, rates[country]))
                con.commit()
        except sqlite3.connector.Error as error:
            print("Failed to insert into MySQL table {}".format(error))
        res=cur.execute("SELECT * FROM rates")
        print(res.fetchall())


        """ print("\nWriting csv\n")
       
        with open('C:\\Users\\ckral\\oaf-psd-bootcamp\\currency.csv', 'w') as currency_csv:
            for country in rates.keys():
                print(country)
                print(rates[country])
                currency_csv.write("%s, %s\n" %(country, rates[country]))
            for date in update_data.keys():
                 print(update_data[date])
                 currency_csv.write("%s, %s\n" %(date, update_data[date]))  
               
        currency_csv.close()
       
        
       # data_file=open('data_file.csv', 'w')
        csv_writer=csv.writer(currency_csv)
        count=0
        print(rates)
       

#reading csv
        print("\nReading csv\n")
        with open('C:\\Users\\ckral\\oaf-psd-bootcamp\\currency.csv',mode='r') as file:
            csvFile=csv.reader(file)
            for lines in csvFile:
                print(lines)

"""


        #write to csv https://www.geeksforgeeks.org/convert-json-to-csv-in-python/
        #this includes last update (utc) and next update time (utc)
        #save those in the csv and before calling the request again, read the csv, compare time, then proceed to use same file or send request to then overwrite the file
    else:
        print(response)
    
get_currency_data()


currentDT = datetime.now(timezone.utc)

print("\nCurrent date time "+str(currentDT.strftime('%a, %d %b %Y %X %z')) ) 
"""print("time_next_update_utc': Wed, 28 Aug 2024 00:35:41 +0000")
print("time_next_update_unix': 1724805341,")
"""
"""
utc offset (+0000, -0400, etc) %z
%a Sun, Mon,
%X 21:30:00 (en_US);

%c is close but not quite; Tue Aug 16 21:30:00 1988 (en_US);
"""