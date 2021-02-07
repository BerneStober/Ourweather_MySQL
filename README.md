# Ourweather_MySQL
 This python script writes Ourweather data to a MySQL database. It runs on a Windows 10 PC which is on the same local network as the Ourweather device.
 The Windows 10 PC must have MySQL installed and MySQL must be set up with a database named datalogger that contains a table called ourweather. 
 The python script grabs the data every ten minutes and does this five times. It is called from the LoopDataGrab.bat file.  This bat file is executed 
 every hour by the Windows Task Scheduler application.  Doing it this way makes the data aquisition robust with respect to power failures or other PC outages. 
 
 This script was written with python 3.8 but runs on a machine with Python 3.7 installed. The import statements at the top of the script show the modules
 you must have installed in order for the script to run.  There is one issue with the script, it does not correct the time from the ourweather device for 
 standard time/daylight time issues. 
 
 Please read the comments in the script -- you will need to supply information such as your devices URL and your user name and password for your MySQL database.
 
 The script was adapted from a similar script available from Switchdoc.com (the purveyor of the Ourweather hardware) that was developed for a Raspberry Pi 
 running a Linux OS. 
 
 Enjoy!
