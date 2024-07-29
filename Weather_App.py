#Weather_App.py
#pulls data from a webstire to provide temp and humidity for a user-provided city

class Weather:
    def fetchData(url, location):
        """fetch data using the url to the weather website"""
    def fetchCity(cityName, stateName, countryName):
        """gets the user provided city, state, and country names and puts
        it into a usable format"""
    def returnData():
        """using the two class functions fetchCity() and fetchData()
        this function gets the temp and humidity data for the location"""
        location=fetchCity()
        data=fetchData(url, location)
        return data
    def dataFormatted(data):
        """this function gets the temp and humidity data from returnData()
        and puts it into a format that can be returned to and read by the user"""
        weatherString=returnData()
        print(weatherString)