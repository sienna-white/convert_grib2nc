import os
import re
import shutil
import pandas as pd 
import glob 

year = 2018
# where all the original forecast files are
source_dir = "/global/scratch/users/siennaw/gsi_2024/grib2nc/%d/finished" % year

inventory = pd.read_csv("inventory_%d.csv" % year)

import numpy as np 
date_col = inventory.columns[0]
dates = inventory[date_col]
hours = inventory.columns[1:]
d, hr = np.where(inventory.values[:, 1:] == 0) 

FILES = [] 

for (d,hr) in zip(d, hr):
    date = pd.to_datetime("%s %s:00" % (dates[d], hours[hr]))

    print("Missing %s" % date.strftime("%b %d %H:00"))

    # Go back in time 

    first_time = 0 

    for i in range(1, 24):
        date_1 = date - pd.Timedelta(hours=i)
        # print("... going back [%d] hr. Looking for %s" % (i, date_1.strftime("%b %d %H:00"))) 
        file_name = source_dir + '/wrfinput_d01_%s_*' % date_1.strftime('%Y%m%d%H')
        matching_files = sorted(glob.glob(file_name))
        # print("\t Looking for %s" % file_name)
        # print("\t Found %s" % matching_files)
        if len(matching_files) > 0:
            if first_time == 0:
                print("SKIPPING FIRST MATCH!")
                first_time = 1
            else : 
                print("\t Found %s" % matching_files)
                forecast_hour = int(matching_files[0].split('_')[-1].split('.')[0])
                print("\t Found a file w/ FH=[%d]" % forecast_hour)
                valid_file = date_1 - pd.Timedelta(hours= forecast_hour) 
                print("\t This file is from %d hours ago" % (forecast_hour + i))
                if forecast_hour + i < 24:
                    # valid_file = valid_file - pd.Timedelta(hours=forecast_hour + i)
                    best_file = valid_file.strftime('%Y%0m%0d%H')
                    print("\t Your best chance is this folder %s" % best_file)
                    FILES.append(best_file) 
                    break 
                else:
                    print("\t No files that are more recent...")
                    break
            
best_file = list(set(FILES))
with open('dates_2_copy_2018_Round2.txt', 'w') as f:
    for date in best_file:
        f.write(date + '\n')


