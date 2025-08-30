import urllib.request, json
import pandas as pd
import numpy as np
from dateutil.parser import parse
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import os

# get planetary k index data (3 days; 3-hour interval)
with urllib.request.urlopen("https://services.swpc.noaa.gov/products/noaa-planetary-k-index.json") as geo_url:
    geo_data = json.load(geo_url)
    geo_df = pd.DataFrame(geo_data)

#removes previous image from logging dir
try:
    os.remove('Planetary_K_Data/planetary-k-data.png')
except OSError:
    pass

# set column names
geo_df = geo_df.rename(columns=geo_df.iloc[0]).drop(geo_df.index[0])

#change Kp to numeric
geo_df['Kp'] = pd.to_numeric(geo_df['Kp'], errors='coerce')

#remove outliers
geo_df.loc[geo_df['Kp'] < 0, 'Kp'] = np.nan

#convert timetag to datetime
geo_df['time_tag'] = geo_df['time_tag'].apply(lambda x: parse(x))

#stretch figure
fig, ax = plt.subplots(figsize=(15, 5))

#plot lines
ax.bar(geo_df['time_tag'], geo_df['Kp'], label='Kp', width=0.1)

#set the y-axis limits and ticks
ax.set_ylim(0, 9)
ax.set_yticks([*range(0, 10, 1)])

#set secondary y-axis
ax2 = ax.twinx()
ax2.set_ylim(0, 9)
ax2.set_yticks([0, 5, 6, 7, 8, 9], ['G0', 'G1', 'G2', 'G3', 'G4', 'G5'])
ax2.tick_params(axis=u'both', which=u'both', length=0)

#get the last timestamp and calculate the time range
time_end = datetime.strptime(str(geo_df['time_tag'].iloc[-1]), "%Y-%m-%d %H:%M:%S")
time_start = time_end - timedelta(days=3)

#set the x-axis limits
ax.set_xlim(time_start, time_end)

#show x-axis labels every 3 hours
hour_interval = 3
x_ticks = [time_start + timedelta(hours=i) for i in range(0, int((time_end - time_start).total_seconds() / 3600) + 10, hour_interval)]
x_tick_labels = [tick.strftime("%Y-%m-%d \n %H:%M") for tick in x_ticks]
ax.set_xticks(x_ticks, x_tick_labels, rotation=45, fontsize=8)
ax.tick_params(axis=u'both', which=u'both', length=0)

#set titles
ax.set_title("Estimated Planetary K index (3 hour data)")
ax.set_xlabel("Universal Time")
ax.set_ylabel("Kp index")
ax2.set_ylabel("G-Scale for Geomagnetic Storming")

#gridlines for dates
ax.grid()
ax.set_axisbelow(True)  # grid lines are behind the rest

#Logging data to csv and outputing graph
#Checking if the directory already exists?
dir_res = os.path.exists('Planetary_K_Data')

#If it doesn't exist then make a new directory
if (dir_res == False):
  os.makedirs('Planetary_K_Data')
else:
  pass

#Graph save
plt.savefig('Planetary_K_Data/planetary-k-data.png', bbox_inches='tight')

#Created a function for logging 4 dataframes
def csv_logger(dataframe, filename):
  #Checking if the previous log file exists?
  file_res = os.path.exists(filename)

  if (file_res == False):
    dataframe.to_csv(filename, mode='a', index=False, header=True)
  else:
    df = pd.read_csv(filename)
    #Get file size, Github gives a warning if its more than 50mb
    file_size = os.path.getsize(filename)

    if file_size > 50*1024*1024:
        # Trim file - keep only recent half
        keep_rows = len(df) // 2
        df = df.iloc[keep_rows:]
        df.to_csv(filename, index=False)
        
    #get the last date    
    last_date = df.iloc[-1, 0]
      
    #drop all rows that are in file
    dataframe = dataframe[dataframe['time_tag'] > last_date]
    dataframe.to_csv(filename, mode='a', index=False, header=False)

#Logging dataframe to csv
csv_logger(geo_df, 'Planetary_K_Data/planetary_k_log.csv')
