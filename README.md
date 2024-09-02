# oaf-psd-bootcamp
Summary of content:

  This application is essentially a calculator but with one very specific use. It is to be used in tandem with gofundme to help a user decide how much they want to donate; it takes the user input of how much the user wants the fundee to receive in their currency, calculates and adds how much in transaction fees gofundme takes, converts the currency from USD to the currency of the fund if necessary, and outputs how much the user should donate in the fund currency if they want the fundee to receive the full original amount intended as well as, if there is currency conversion necessary, how much that would come to in USD.

Eg: User wants to donate $20 CAD to a fund, in order for the recipient to receive the full $20CAD the donor would need to donate at least $20.80CAD, which is $15.43 USD. The user can decide for themselves if $0.80CAD ($0.59 USD) is worth it to round up or not.

Data Source:

  Exchange Rate Open API https://www.exchangerate-api.com/docs/free (it updates the currency exchange rates once every 24hrs)

  Gofundme’s “pricing and fees” page for how much they charge in transaction fees (not calling api, just looked it up)

Data Storage:

  I am using a database to store the api’s currency exchange rate information and a csv to keep the api's "last_update_time" and "next_update_time" and will update those once once it is confirmed whether the db and csv needs to be updated or not by comparing current datetime with the saved "next_update_time"
  
Data Utilization:

  Call the database to be able to find the currency abbreviation needed and get the exchange rate in order to convert currency as necessary.
