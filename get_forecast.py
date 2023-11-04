import urllib.request
import os
import re

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

# Decode the binary content to a string
forecast_text = forecast_bytes.decode("utf-8")

# Remove '# ' characters
forecast_text = forecast_text.replace("# ", ":")

# Apply ensp for foramtting issues
forecast_text = forecast_text.replace(" ", "&ensp;")

# Add "  " to lines end and split the text into lines
modified_forecast_lines = []
for line in forecast_text.splitlines():
    line += "  "
    modified_forecast_lines.append(line)

# Join the modified lines back into a single string
modified_forecast = '\n'.join(modified_forecast_lines)

# Write the modified forecast to a file
with open('Forecast/forecast.txt', 'w', encoding="utf-8") as f:  # Open the file in text mode
    f.write(modified_forecast)
