import urllib.request
import os

#removes previous forecast
try:
    os.remove('Forecast/forecast.txt')
except OSError:
    pass

#Checking if the directory already exists?
dir_res = os.path.exists('Forecast')

#If it doesn't exist then make a new directory
if (dir_res == False):
  os.makedirs('Forecast')
else:
  pass

#get forecast
with urllib.request.urlopen("https://services.swpc.noaa.gov/text/3-day-forecast.txt") as url:
  forecast = url.read()

#write forecast to file
with open('Forecast/forecast.txt', 'wb') as f:
    f.write(forecast)
