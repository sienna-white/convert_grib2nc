
import os 
import sys
if os.getcwd() not in sys.path: # Add the current directory to the Python path
    sys.path.append(current_directory)
import pandas as pd 
import set_up_wps_util as util 


# Where we will process our files
working_directory = '/global/scratch/users/siennaw/smoke/data/bkg/grib2wrf'

# Where the grib files live 
grib_directory = '/global/home/users/siennaw/scratch/data/grib/'

# Get list of folders with grib files. Each folder is named after the date. 
grib_folders = util.get_folders_in_directory(grib_directory)
print(grib_folders)


commands = []

grib_folders = ['2018111418']

# Loop through each grib folder and prep a WPS run namelist
for folder in grib_folders:

    print('\n Processing %s' % folder)

    # Create a folder for processing the GRIB data
    try: 
        working_folder = util.create_folder(working_directory, folder)  
    except:
        print('skipping ...')
        # continue  

    # Strip the date of the data from the folder name, figure out start + end times
    start_time, end_time = util.folder_name_to_date(folder)

    # Write a namelist with those coordinating start / end times for WPS
    util.write_namelist_wps(start_time, end_time, working_folder)

    # Write a namelist for real.exe
    util.write_namelist_real(start_time, end_time, working_folder)

    # Copy over WPS supporting contents 
    print('... Copying over WPS files to working folder ...')
    util.copy_folder_contents('/global/home/users/siennaw/scratch/WPS/wps_files', working_folder)

    # Path where the unprocessed GRIB files live
    grib_file_path = os.path.join(grib_directory, folder, 'postprd')

    # Write a script for batch submission
    command = util.write_job_script(working_folder, grib_file_path, start_time, folder)

    commands.append(command)

    print('%s is ready to run! \n\n' % folder)

for command in commands:
    print(command)
