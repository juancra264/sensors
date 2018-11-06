import Adafruit_DHT
import time
import requests

# constants
URL = 'https://corlysis.com:8086/write'


# get data from DHT sensor
def getDHTdata():
    DHTSensor = Adafruit_DHT.DHT11
    DHTpin = 4
    hum, temp = Adafruit_DHT.read_retry(DHTSensor, DHTpin)
    if hum is not None and temp is not None:
        hum = round(hum)
        temp = round(temp, 1)
    return temp, hum


def main():
    corlysis_params = {"db": "RPI", "u": "token", "p": "665834623388d19d1779dbd61399f1f3", "precision": "ms"}
    payload = ""
    unix_time_ms = int(time.time()*1000)
    temp, hum = getDHTdata()    
    # read sensor data and convert it to line protocol
    line = "sensors_data temperature={},humidity={} {}\n".format(temp,
                                                                 hum,
                                                                 unix_time_ms)
    payload += line
    #print(payload)
    try:
        # try to send data to cloud
        r = requests.post(URL, params=corlysis_params, data=payload)
        if r.status_code != 204:
            raise Exception("data not written")
        payload = ""
    except:
        print('cannot write to InfluxDB')
        payload = ""
    

if __name__ == "__main__":
    main()

