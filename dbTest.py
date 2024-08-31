import sqlite3
import csv
con = sqlite3.connect("currencyRates.db")
cur = con.cursor()

"""with open('C:\\Users\\ckral\\oaf-psd-bootcamp\\currency.csv',mode='r') as file:
            csvFile=csv.reader(file)
            for lines in csvFile:
                
                print(lines)
"""

#cur.execute("CREATE TABLE rates(currency, rate)")
res = cur.execute("SELECT name FROM sqlite_master")
print(res.fetchone())


#cur.execute("""
   #         INSERT INTO rates VALUES
  #          ('Test', .5)
 #           """)
#con.commit()
insert_query="""INSERT INTO rates (currency, rate)
                VALUES (?, ?)"""
                #print(values)

#values=[("USD", 1),("GBP", 1.3)]
#cur.executemany('INSERT INTO rates VALUES (?, ?)', values)
#con.commit()
update_q="""UPDATE rates SET rate = ? WHERE currency = ?"""
#cur.execute(update_q,(2,"USD"))
#con.commit()
res=cur.execute("SELECT * FROM rates")
print(res.fetchall())
res=cur.execute("SELECT rate FROM rates WHERE currency = 'USD'")
#print(res.fetchall())
# 
con.close()