import pandas as pd 
import os 
import glob
# Create an hourly timeseries for a year
folder = '/global/scratch/users/siennaw/gsi_2024/grib2nc/finished/'

import os
import re 
# Use regex to extract the 10 digit date
# from the filename

date_pattern = re.compile(r'\d{10}')

processed = [] 
for file_name in os.listdir(folder):
    if file_name.endswith(".nc"):
        filedate =re.search(date_pattern, file_name).group()
        processed.append(filedate)


print("There are %d files that have been processed." % len(processed))

# Read in folders2process.txt

with open('folders2process_FULL.txt', 'r') as f:
    folders2process_FULL = f.read().splitlines() 

print("There are %d files available grib files..." % len(folders2process_FULL))

# Set operation to extract the difference

to_process = list(set(folders2process_FULL) - set(processed))
Nprocess = len(to_process)
print("This leaves %d files left to process." % len(to_process))

# Let's split the list of files to process into chunks of 800
# to make it easier to run the script in parallel

chunk = 200 
nchunks = len(to_process) // chunk
print(nchunks)

fileN = 0 
for i in range(0, Nprocess, chunk): 

    folder_subset = to_process[i:i+chunk]
    print(i, i+chunk)
    # Print the list of files to process to a file
    with open('remaining_folders2process_%d.txt' % fileN, 'w') as f:
        for folder in folder_subset:
            f.write(folder + '\n')
    fileN += 1

# # Get list of *.nc files in a directory
# files = 



# def get_list_of_files_in_directory(directory_path):
#     ''' Get a list of files in a directory ''' 
#     # Check that our directory exists
#     if not os.path.isdir(directory_path):
#         raise Exception("Error: Directory not found.")
#     # Get a list of folders in the directory
#     files = [entry for entry in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, entry))]
#     if len(files) == 0:
#         raise Exception("No files found in the directory


# # Initilize the output dataframe
# output = pd.DataFrame(index=times_daily)

# for hour in range(0, 24):
#     output['%02d' % hour] = 0 

# directory = "/global/scratch/users/siennaw/gsi_2024/grib2nc/finished/"

# full_days = 0

# missing = [] 
# for day in times_daily:

#     count = 0 

#     for hour in range(0, 24):
#         datestring = "%s%02d" % (day.strftime('%Y%m%d'), hour)

#     # # Check if the file exists
#         file_name = directory + 'wrfinput_d01_%s.nc' % datestring

#         if os.path.exists(file_name):
#             # print("\tFile exists: %s" % file_name)
#             count += 1 
#             output.loc[day, '%02d' % hour] = 1
#         else:
#             missing.append(datestring) #  output.loc[day, 'exists'] = False
    
#     print("Checked for files on day %s [%d/24]" % (day, count))
#     if count == 24:
#         full_days += 1

# print("Number of full days: %d" % full_days)
# output.to_csv('inventory_%d.csv' % year)


# print(missing)
# # if not os.path.exists(metgrid_file_name):
# #   print('Metgrid file does not exist.')
# #   sys.exit(1)
