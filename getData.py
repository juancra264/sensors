import sqlite3
conn=sqlite3.connect('/home/jcramirez/sensors/sensorsData.db')
curs=conn.cursor()

maxTemp = 27.6

print ("\nEntire database contents:\n")
for row in curs.execute("SELECT * FROM DHT_data"):
    print (row)
