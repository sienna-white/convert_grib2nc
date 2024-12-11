import pandas as pd 
import os 
# Create an hourly timeseries for a year

year = 2020
times_hourly = pd.date_range(start='%d-01-01' % year, end='%d-12-31' % year, freq='H')
times_daily = pd.date_range(start='%d-01-01' % year, end='%d-12-31' % year, freq='D')

# Convert to just the date
times_daily = pd.to_datetime(times_daily)
times_daily = [time_daily.date() for time_daily in times_daily]

# Initilize the output dataframe
output = pd.DataFrame(index=times_daily)

for hour in range(0, 24):
    output['%02d' % hour] = 0 

directory = "/global/scratch/users/siennaw/gsi_2024/grib2nc/finished/"

for day in times_daily:

    print("Checking for files on day %s" % day)

    for hour in range(0, 24):
        datestring = "%s%02d" % (day.strftime('%Y%m%d'), hour)

    # # Check if the file exists
        file_name = directory + 'wrfinput_d01_%s.nc' % datestring

        if os.path.exists(file_name):
            print("\tFile exists: %s" % file_name)
            output.loc[day, '%02d' % hour] = 1
        # else:
        #     output.loc[day, 'exists'] = False

output.to_csv('inventory_%d.csv' % year)
# if not os.path.exists(metgrid_file_name):
#   print('Metgrid file does not exist.')
#   sys.exit(1)