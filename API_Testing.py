""" testing api 
thanks to https://www.exchangerate-api.com/docs/free """

import requests
import json
from datetime import datetime,timezone
import os

def get_currency_data():
    url='https://open.er-api.com/v6/latest/USD'
    url2='https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m'
    response=requests.get(url)
    print(response)
    if response.status_code==200:
        print(response)
        data=response.json()
        print(json.dumps(data, indent=4, sort_keys=True))
        """for key in data:{
            print(key, ":", data[key])
        }"""

        currentDT = datetime.now(datetime.UTC)
        #currentDT.strftime('%a, %d %b %Y %X %z')
        nextUpdate=data['time_next_update_utc']
        print("\nCurrent date time "+str(currentDT) )
        print("\nNext api update "+str(nextUpdate))

        #write to csv https://www.geeksforgeeks.org/convert-json-to-csv-in-python/
        #this includes last update (utc) and next update time (utc)
        #save those in the csv and before calling the request again, read the csv, compare time, then proceed to use same file or send request to then overwrite the file
    else:
        print(response)
    
#get_currency_data()
currentDT = datetime.now(timezone.utc)

print("\nCurrent date time "+str(currentDT.strftime('%a, %d %b %Y %X %z')) ) 
print("time_next_update_utc': Wed, 28 Aug 2024 00:35:41 +0000")
print("time_next_update_unix': 1724805341,")

"""
utc offset (+0000, -0400, etc) %z
%a Sun, Mon,
%X 21:30:00 (en_US);

%c is close but not quite; Tue Aug 16 21:30:00 1988 (en_US);
"""