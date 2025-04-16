import pandas as pd 
import os 
import glob 

# Create an hourly timeseries for a year

year = 2017
times_daily = pd.date_range(start='%d-11-26' % year, end='%d-12-31' % year, freq='D')

# Convert to just the date
times_daily = pd.to_datetime(times_daily)
times_daily = [time_daily.date() for time_daily in times_daily]

# Initilize the output dataframe
output = pd.DataFrame(index=times_daily)

for hour in range(0, 24):
    output['%02d' % hour] = 0 

directory = "/global/scratch/users/siennaw/gsi_2024/grib2nc/%d/finished/" % year

full_days = 0
files = 0

missing = [] 
for day in times_daily:

    count = 0 

    for hour in range(0, 24):
        datestring = "%s%02d" % (day.strftime('%Y%m%d'), hour)

    # # Check if the file exists
        file_name = directory + 'wrfinput_d01_%s_*' % datestring
        matching_files = glob.glob(file_name)
        #print(file_name)
        #print(matching_files)

        if len(matching_files)>0 : #os.path.exists(file_name):
            # print("\tFile exists: %s" % file_name)
            count += 1 
            files += 1
            output.loc[day, '%02d' % hour] = 1
        else:
            missing.append(datestring) #  output.loc[day, 'exists'] = False
    
    print("Checked for files on day %s [%d/24]" % (day, count))
    if count == 24:
        full_days += 1

print("Number of full days: %d" % full_days)
print("Number of files: %d" % files)
output.to_csv('inventory_%d.csv' % year)
print("Number of missing hours: %d" % len(missing))

print("Percentage of missing hours: %f" % (len(missing) / (24 * len(times_daily))))

fout = "inventory_%d_missing.txt" % year

with open(fout, 'w') as f:
    for item in missing:
        f.write("%s\n" % item)


# print(missing)
# if not os.path.exists(metgrid_file_name):
#   print('Metgrid file does not exist.')
#   sys.exit(1)
