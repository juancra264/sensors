import time
import sqlite3
import Adafruit_DHT

dbname='sensorsData.db'
sampleFreq = 2 # time in seconds

# get data from DHT sensor
def getDHTdata():	
	DHTSensor = Adafruit_DHT.DHT11
	DHTpin = 4
	hum, temp = Adafruit_DHT.read_retry(DHTSensor, DHTpin)
	
	if hum is not None and temp is not None:
		hum = round(hum)
		temp = round(temp, 1)
	return temp, hum

# log sensor data on database
def logData (temp, hum):	
	conn=sqlite3.connect(dbname)
	curs=conn.cursor()
	curs.execute("INSERT INTO DHT_data values(datetime('now'), (?), (?))", (temp, hum))
	conn.commit()
	conn.close()

# display database data
def displayData():
	conn=sqlite3.connect(dbname)
	curs=conn.cursor()
	print ("\nEntire database contents:\n")
	for row in curs.execute("SELECT * FROM DHT_data"):
		print (row)
	conn.close()

# main function
def main():
	temp, hum = getDHTdata()
	logData (temp, hum)


# Execute program 
main()
