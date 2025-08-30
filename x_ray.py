import urllib.request, json
import pandas as pd
import numpy as np
from dateutil.parser import parse
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import os

#get GOES X-RAY FLUX data (3 days; 1-minute interval)
with urllib.request.urlopen("https://services.swpc.noaa.gov/json/goes/primary/xrays-3-day.json") as url_16, urllib.request.urlopen("https://services.swpc.noaa.gov/json/goes/secondary/xrays-3-day.json") as url_18:
    data_16 = json.load(url_16)
    data_18 = json.load(url_18)

    x_ray_16_df = pd.DataFrame(data_16)
    x_ray_18_df = pd.DataFrame(data_18)

#removes previous image from logging dir
try:
    os.remove('X-Ray_Data/x-ray-data.png')
except OSError:
    pass

#remove outliers
x_ray_16_df.loc[x_ray_16_df['flux']<= 1e-9, 'flux'] = np.nan
x_ray_18_df.loc[x_ray_18_df['flux']<= 1e-9, 'flux'] = np.nan

#convert timetag to datetime
x_ray_16_df['time_tag'] = x_ray_16_df['time_tag'].apply(lambda x: parse(x))
x_ray_18_df['time_tag'] = x_ray_18_df['time_tag'].apply(lambda x: parse(x))

#split data by short or long x-ray flux for 16 satellite
split_data_16 = dict(tuple(x_ray_16_df.groupby('energy')))

goes_16_short_df = split_data_16['0.05-0.4nm']
goes_16_long_df = split_data_16['0.1-0.8nm']

#split data by short or long x-ray flux for 18 satellite
split_data_18 = dict(tuple(x_ray_18_df.groupby('energy')))

goes_18_short_df = split_data_18['0.05-0.4nm']
goes_18_long_df = split_data_18['0.1-0.8nm']

#stretch figure
fig, ax = plt.subplots(figsize=(15, 5))

#plot lines
ax.plot(goes_16_short_df['time_tag'], goes_16_short_df['flux'], label='GOES-16 Short')
ax.plot(goes_18_short_df['time_tag'], goes_18_short_df['flux'], label='GOES-18 Short')
ax.plot(goes_16_long_df['time_tag'], goes_16_long_df['flux'], label='GOES-16 Long')
ax.plot(goes_18_long_df['time_tag'], goes_18_long_df['flux'], label='GOES-18 Long')

#change y-axis to log
ax.set_yscale('log')

#set the y-axis limits and ticks
ax.set_ylim(1e-9, 1e-2)
ax.set_yticks([1e-9, 1e-8, 1e-7, 1e-6, 1e-5, 5e-5, 1e-4, 1e-3, 2e-3, 1e-2])

#set secondary y-axis
ax2 = ax.twinx()
ax2.set_yscale('log')
ax2.set_ylim(1e-9, 1e-2)
ax2.set_yticks([1e-9, 1e-5, 5e-5, 1e-4, 1e-3, 2e-3], ['R0', 'R1', 'R2', 'R3', 'R4', 'R5'])
ax2.tick_params(axis=u'both', which=u'both', length=0)

#get the last timestamp and calculate the time range
time_end = datetime.strptime(str(goes_16_short_df['time_tag'].iloc[-1]), "%Y-%m-%d %H:%M:%S%z")
time_start = time_end - timedelta(days=3)

#set the x-axis limits
ax.set_xlim(time_start, time_end)

#show x-axis labels every 8 hours
hour_interval = 8
x_ticks = [time_start + timedelta(hours=i) for i in range(0, int((time_end - time_start).total_seconds() / 3600) + 10, hour_interval)]
x_tick_labels = [tick.strftime("%Y-%m-%d \n %H:%M") for tick in x_ticks]
ax.set_xticks(x_ticks, x_tick_labels, rotation=45)
ax.tick_params(axis=u'both', which=u'both', length=0)

#set titles, legend
ax.set_title("GOES X-Ray Flux (1 minute data)")
ax.set_xlabel("Universal Time")
ax.set_ylabel("Watts * m^-2")
ax2.set_ylabel("R-Scale for Radio Blackouts")
legend = ax.legend(loc='upper left')

#gridlines for dates
ax.grid()
ax.set_axisbelow(True)  # grid lines are behind the rest

#Logging data to csv and outputing graph
#Checking if the directory already exists?
dir_res = os.path.exists('X-Ray_Data')

#If it doesn't exist then make a new directory
if (dir_res == False):
  os.makedirs('X-Ray_Data')
else:
  pass

#Graph save
plt.savefig('X-Ray_Data/x-ray-data.png', bbox_inches='tight')

#Created a function for logging 4 dataframes
def csv_logger(dataframe, filename):
  #Checking if the previous log file exists?
  file_res = os.path.exists(filename)

  if (file_res == False):
    dataframe.to_csv(filename, mode='a', index=False, header=True)
  else:
    #Get file size, Github gives a warning if its more than 50mb
    file_size = os.path.getsize(filename)

    if file_size > 50*1024*1024:
        # Trim file - keep only recent half
        df = pd.read_csv(filename)
        keep_rows = len(df) // 2
        df = df.iloc[keep_rows:]
        df.to_csv(filename, index=False)

    last_df = pd.read_csv(filename)
    last_date = last_df.iloc[last_df.tail(1).index[0], 0]

    #drop all rows that are in file
    dataframe = dataframe[dataframe['time_tag'] > last_date]
    dataframe.to_csv(filename, mode='a', index=False, header=False)

#Logging 4 dataframes to csv
csv_logger(goes_16_short_df, 'X-Ray_Data/goes_16_short_log.csv')
csv_logger(goes_18_short_df, 'X-Ray_Data/goes_18_short_log.csv')
csv_logger(goes_16_long_df, 'X-Ray_Data/goes_16_long_log.csv')
csv_logger(goes_18_long_df, 'X-Ray_Data/goes_18_long_log.csv')
