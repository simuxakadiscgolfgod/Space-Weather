import urllib.request
import os

# Removes the previous forecast
try:
    os.remove('Forecast/forecast.txt')
except OSError:
    pass

# Checking if the directory already exists
dir_res = os.path.exists('Forecast')

# If it doesn't exist, then make a new directory
if not dir_res:
    os.makedirs('Forecast')

# Get forecast
with urllib.request.urlopen("https://services.swpc.noaa.gov/text/3-day-forecast.txt") as url:
    forecast_bytes = url.read()  # Read the binary content

# Decode the binary content to a string and add backticks for maintaining formatting in md
forecast_text = "```\n" + forecast_bytes.decode("utf-8") + "\n```"

# Write the modified forecast to a file
with open('Forecast/forecast.txt', 'w', encoding="utf-8") as f:  # Open the file in text mode
    f.write(forecast_text)
