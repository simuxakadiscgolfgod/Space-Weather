import urllib.request, json
import pandas as pd
import numpy as np
from dateutil.parser import parse
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import os

# get GOES Proton FLUX data (3 days; 5-minute interval)
with urllib.request.urlopen("https://services.swpc.noaa.gov/json/goes/primary/integral-protons-3-day.json") as url_16_proto:
    proto_data_16 = json.load(url_16_proto)
    proto_16_df = pd.DataFrame(proto_data_16)

#removes previous image from logging dir
try:
    os.remove('Proton_Data/proton-data.png')
except OSError:
    pass

#remove outliers
proto_16_df.loc[proto_16_df['flux']<= 1e-2, 'flux'] = np.nan

#convert timetag to datetime
proto_16_df['time_tag'] = proto_16_df['time_tag'].apply(lambda x: parse(x))

#split data by energy
split_proto_data_16 = dict(tuple(proto_16_df.groupby('energy')))

proto_10Mev = split_proto_data_16['>=10 MeV']
proto_50Mev = split_proto_data_16['>=50 MeV']
proto_100Mev = split_proto_data_16['>=100 MeV']

#stretch figure
fig, ax = plt.subplots(figsize=(15, 5))

#plot lines
ax.plot(proto_10Mev['time_tag'], proto_10Mev['flux'], label='GOES-16 >= 10 MeV')
ax.plot(proto_50Mev['time_tag'], proto_50Mev['flux'], label='GOES-16 >= 50 MeV')
ax.plot(proto_100Mev['time_tag'], proto_100Mev['flux'], label='GOES-16 >= 100 MeV')

#change y-axis to log
ax.set_yscale('log')

#set the y-axis limits and ticks
ax.set_ylim(1e-2, 1e5)
ax.set_yticks([1e-2, 1e-1, 1e0, 1e1, 1e2, 1e3, 1e4, 1e5])

#set secondary y-axis
ax2 = ax.twinx()
ax2.set_yscale('log')
ax.set_ylim(1e-2, 1e5)
ax2.set_yticks([1e-2, 1e1, 1e2, 1e3, 1e4, 1e5], ['S0', 'S1', 'S2', 'S3', 'S4', 'S5'])
ax2.tick_params(axis=u'both', which=u'both', length=0)

#get the last timestamp and calculate the time range
time_end = datetime.strptime(str(proto_10Mev['time_tag'].iloc[-1]), "%Y-%m-%d %H:%M:%S%z")
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
ax.set_title("GOES Proton Flux (5 minute data)")
ax.set_xlabel("Universal Time")
ax.set_ylabel("Particles * cm^-2 * s^-1 * sr^-1")
ax2.set_ylabel("S-Scale for Radiation Storms")
legend = ax.legend(loc='upper left')

#gridlines for dates
ax.grid()
ax.set_axisbelow(True)  # grid lines are behind the rest

#Logging data to csv and outputing graph
#Checking if the directory already exists?
dir_res = os.path.exists('Proton_Data')

#If it doesn't exist then make a new directory
if (dir_res == False):
  os.makedirs('Proton_Data')
else:
  pass

#Graph save
plt.savefig('Proton_Data/proton-data.png', bbox_inches='tight')

#Created a function for logging 3 dataframes
def csv_logger(dataframe, filename):
  #Checking if the previous log file exists?
  file_res = os.path.exists(filename)

  if (file_res == False):
    dataframe.to_csv(filename, mode='a', index=False, header=True)
  else:
    last_df = pd.read_csv(filename)
    last_date = last_df.iloc[last_df.tail(1).index[0], 0]

    #drop all rows that are in file
    dataframe = dataframe[dataframe['time_tag'] > last_date]
    dataframe.to_csv(filename, mode='a', index=False, header=False)

#Logging 3 dataframes to csv
csv_logger(proto_10Mev, 'Proton_Data/goes_16_10Mev_log.csv')
csv_logger(proto_50Mev, 'Proton_Data/goes_16_50Mev_log.csv')
csv_logger(proto_100Mev, 'Proton_Data/goes_16_100Mev_log.csv')
