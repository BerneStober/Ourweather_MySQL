######################################
#
# just readOURWEATHERData and put into MySQL
#
#
######################################

import sys
from datetime import timezone
import httplib2 as http
import json
import time

try:
    from urllib.parse import urlparse
except ImportError:
    from urllib.parse import urlparse

from datetime import datetime
import MySQLdb as mdb

import os

def Pausing (sec):
    time.sleep(sec)

# this writes output to a dedug file so you can troubleshoot errors
def WriteDebug (record):
    debugfile = open("debugmYsql.txt",'a+t')
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    debugfile.write(dt_string + ' ' + record + "\n")
    debugfile.close()

# fetch the JSON data from the OurWeather device
def fetchJSONData(uri, path):
    target = urlparse(uri+path)
    method = 'GET'
    body = ''

    h = http.Http()
    
    # If you need authentication some example:
    #if auth:
    #    h.add_credentials(auth.user, auth.password)

    response, content = h.request(
            target.geturl(),
            method,
            body,
            headers)

    # assume that content is a json reply
    # parse content with the json module
    data = json.loads(content)

    return data


def readOURWEATHERData(username, password):
        #print(('readOURWEATHERData - The time is: %s' % datetime.now()))
        WriteDebug (('readOURWEATHERData - The time is: %s' % datetime.now()))

        try:
            data = fetchJSONData(uri, path)
        except:
            print("-----Can't read from OurWeather")


        # pre split weather data
        preSplitData = data['FullDataString']
        WData = preSplitData.split(",")
        WriteDebug (str(WData).strip('[]'))
        print (WData)

        if (len(WData) < 18):   
            # we have a bad read
            # try again later
            print("bad read from OurWeather")
            return 0

        if (len(WData) == 18):
            # Version does not have air quality
            WData.append(0)
            WData.append(4)

        # open database
        # make sure you set up a MySQL database first
        # my database is called datalogger with a table called ourweather 
        con = mdb.connect('localhost', 'root', password, 'datalogger' )
        cur = con.cursor()

        #
        # Now put the data in MySQL
        # 
        # Put record in MySQL      

        WriteDebug ("writing SQLdata ");
        
        dt = datetime.now() 
        utc_time = dt.replace(tzinfo = timezone.utc) 
        utc_timestamp = utc_time.timestamp() 
        WriteDebug (str(utc_timestamp))
        print (utc_timestamp)

        # write record
        deviceid = 0
        query = 'INSERT INTO '+OURWEATHERtableName+('(timestamp, deviceid, Outdoor_Temperature , Outdoor_Humidity , Indoor_Temperature , Barometric_Pressure , Altitude , Current_Wind_Speed , Current_Wind_Gust , Current_Wind_Direction , Rain_Total , Wind_Speed_Minimum , Wind_Speed_Maximum , Wind_Gust_Minimum , Wind_Gust_Maximum , Wind_Direction_Minimum , Wind_Direction_Maximum , Display_English_Metrice , OurWeather_DateTime , OurWeather_Station_Name , Current_Air_Quality_Sensor , Current_Air_Quality_Qualitative, Battery_Voltage, Battery_Current, Solar_Voltage, Solar_Current, Load_Voltage, Load_Current ) VALUES(%.3f,  %i, %.3f, %.3f, %.3f, %.3f, %.3f, %.3f, %.3f, %.3f, %.3f, %.3f, %.3f, %.3f, %.3f, %.3f, %.3f, %i, "%s" , "%s", %i, %i,%.3f, %.3f, %.3f,%.3f,%.3f,%.3f)' % (utc_timestamp, int(data['id']), float(WData[0]), float(WData[1]), float(WData[2]), float(WData[3]), float(WData[4]), float(WData[5]), float(WData[6]), float(WData[7]), float(WData[8]), float(WData[9]), float(WData[10]), float(WData[11]), float(WData[12]), float(WData[13]), float(WData[14]), int(WData[15]), WData[16], WData[17], int(WData[18]), int(WData[19]), float(WData[20]), float(WData[21]), float(WData[22]), float(WData[23]), float(WData[24]), float(WData[25])) ) 
        
        print(("query=%s" % query))

        cur.execute(query)  
        con.commit()

retval = os.getcwd()
print ("Current working directory %s" % retval)
WriteDebug ("Current working directory %s" % retval)

os.chdir (r'C:\Users\Berne\source\repos\SDL_Pi_DataLogger')
retval = os.getcwd()

print ("Directory changed successfully %s" % retval)
WriteDebug ("Directory changed successfully %s" % retval)


#mysql user
username = "XXXXX"
#mysql Password
password = 'XXXXXXXXXX'
#mysql Table Name
OURWEATHERtableName = 'ourweather'

# set up your OurWeather IP Address here
uri = 'http://192.168.0.117/FullDataString'
path = '/'

headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json; charset=UTF-8'}

counter = 0
MaxCounter = 5
SecBetweenDataGrab = 600

while counter <= MaxCounter: 

    readOURWEATHERData(username, password)
    counter = counter + 1
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    WriteDebug (dt_string + ' at execution number' + str(counter) + ' now pausing for another ' + str(SecBetweenDataGrab) + ' seconds.')
    print (dt_string + ' at execution number' + str(counter) + ' now pausing for another ' + str(SecBetweenDataGrab) + ' seconds.')
    Pausing (SecBetweenDataGrab)

now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
print ('Execution completed at '+ dt_string)

