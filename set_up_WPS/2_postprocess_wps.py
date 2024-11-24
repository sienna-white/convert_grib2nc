
import os 
import sys
if os.getcwd() not in sys.path: # Add the current directory to the Python path
    sys.path.append(current_directory)
import pandas as pd 
import set_up_wps_util as util 
import shutil
import set_up_bkg_lib as bkg 

# Where the finished netcdf files will live 
netcdf_directory = '/global/scratch/users/siennaw/gsi_2024/grib2nc/finished/'

# Where the processed grib / netcdf files live 
grib2wrf_directory = '/global/scratch/users/siennaw/gsi_2024/grib2nc/working/'

# Get list of folders in our "grib2wrf" directory. 
grib2wrf_folders = bkg.get_folders_in_directory(grib2wrf_directory)

print('Found %d files in /grib2wrf/ ...' % len(grib2wrf_folders))

# Loop through each folder see if there are completed runs ... 

with open('PROCESSED_GRIB_FILES.txt', 'w') as f:

    for folder in grib2wrf_folders:
        print('\n Looking for finished runs in %s' % folder)

        # Create a folder for the finished netcdf 
        try: 
            netcdf_folder = util.create_folder(netcdf_directory, folder)  
        except:
            print('... writing over existing files...')
            # print('skipping ...')
            # continue  

        # Strip the date of the data from the folder name, figure out start + end times
        start_time, end_time = util.folder_name_to_date(folder)

        grib2wrf_file_path = os.path.join(grib2wrf_directory, folder)

        if util.check_for_finished_netcdf(grib2wrf_file_path):
            # Copy over finished 

            for file in os.listdir(grib2wrf_file_path):

                if (file.endswith(".nc")) & ("blank" not in file):
                    copy_path = os.path.join(grib2wrf_file_path, file)
                    print(copy_path)
                    final_path = os.path.join(netcdf_folder, file)
                    shutil.copyfile(copy_path, final_path)

                    print('... Copying over %s ...' % copy_path)
                    # copy_path = '%s/*.nc' % grib2wrf_file_path

                    f.write('%s' % start_time.strftime('%B/%d/%Y'))
        else:
            print('No finished files found in %s!' % grib2wrf_file_path)
   

# grib_file_path = os.path.join(grib_directory, folder, 'postprd')
# command = util.write_job_script(working_folder,grib_file_path , folder)
# commands.append(command)