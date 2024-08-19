import sqlite3

con = sqlite3.connect("currencyRates.db")
cur = con.cursor()
#cur.execute("CREATE TABLE rates(currency, rate)")
res = cur.execute("SELECT name FROM sqlite_master")
print(res.fetchone())

cur.execute("""
            INSERT INTO rates VALUES
            ('Test', .5)
            """)
con.commit()
res=cur.execute("SELECT * FROM rates")
print(res.fetchone())
res=cur.execute("SELECT rate FROM rates WHERE currency = 'Test'")
print(res.fetchone())