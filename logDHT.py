import datetime
import time
import sqlite3
import Adafruit_DHT
import requests

dbname='/home/jcramirez/sensors/sensorsData.db'
URL = 'https://corlysis.com:8086/write'


# get time string
def gettime():
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")


# get data from DHT sensor
def getDHTdata():	
    DHTSensor = Adafruit_DHT.DHT11
    DHTpin = 4
    hum, temp = Adafruit_DHT.read_retry(DHTSensor, DHTpin)
    #if hum is not None and temp is not None:
    #    hum = round(hum)
    #    temp = round(temp, 1)
    return temp, hum


# log sensor data on database
def logData (temp, hum):
    conn=sqlite3.connect(dbname)
    curs=conn.cursor()
    #curs.execute("INSERT INTO DHT_data values(datetime('now'), (?), (?))", (temp, hum))
    curs.execute("INSERT INTO DHT_data values((?), (?), (?))", (gettime(), temp, hum))
    conn.commit()
    conn.close()

def logDataCorlysis(temp, hum):
    corlysis_params = {"db": "RPI", "u": "token", "p": "665834623388d19d1779dbd61399f1f3", "precision": "ms"}
    payload = ""
    unix_time_ms = int(time.time()*1000)
    line = "sensors_data temperature={},humidity={} {}\n".format(temp,
                                                                 hum,
                                                                 unix_time_ms)
    payload += line
    try:
        # try to send data to cloud
        r = requests.post(URL, params=corlysis_params, data=payload)
        if r.status_code != 204:
            raise Exception("data not written")
        payload = ""
    except:
        print('cannot write to InfluxDB')
        payload = ""



# main function
def main():
    temp, hum = getDHTdata()
    #print('Temp={}*  Humidity={}%'.format(temp, hum))
    logData (temp, hum)
    logDataCorlysis(temp, hum)


# Execute program 
if __name__ == "__main__":
    main()

