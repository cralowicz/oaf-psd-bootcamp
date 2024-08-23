""" testing api 
thanks to https://www.exchangerate-api.com/docs/free """

import requests
import json

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

        #write to csv https://www.geeksforgeeks.org/convert-json-to-csv-in-python/
        #this includes last update (utc) and next update time (utc)
        #save those in the csv and before calling the request again, read the csv, compare time, then proceed to use same file or send request to then overwrite the file
    else:
        print(response)
    
get_currency_data()