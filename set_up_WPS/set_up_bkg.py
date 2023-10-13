######### USER INPUT #############

GENERATE_LIST_OF_FOLDERS = False 

####################################

import os 
import sys
if os.getcwd() not in sys.path: # Add the current directory to the Python path
    sys.path.append(current_directory)
import pandas as pd 
import set_up_bkg_lib as bkg 


# Where the grib files live 
grib_directory = '/global/home/users/siennaw/scratch/data/grib/'

# Where we will process our files
working_directory = '/global/scratch/users/siennaw/smoke/data/bkg/grib2wrf/'

# WPS files 
wps_fn = '../wps_files/'

# List of folders to process 
fout='folders2process.txt'

# Shell script to launch written jobs 
fshell = 'jobs2run.sh'

# Delete shell script if it already exists 
if os.path.exists(fshell):
    os.remove(fshell)


# (1) : Look at GRIB Folders, make a list of folders to process
if GENERATE_LIST_OF_FOLDERS: 

    # Get list of folders with grib files. Each folder is named after the date. 
    grib_folders = util.get_folders_in_directory(grib_directory)

    print('Found the following folders to convert ...')
    with open(fout, 'w') as f:
        for folder in grib_folders:
            f.write(folder + '\n')
            print(folder)

    user = input("List of folders has been written. Continue running [y] or stop the script [n]?")
    if user == 'n':
        exit()
    elif user == 'y':
        pass
    else:
        Exception("No valid input given.")


with open(fout, 'r') as f:
    grib_folders = f.read()
    grib_folders = list(grib_folders.split('\n'))

# Loop through each grib folder and prep a WPS run namelist
for folder in grib_folders[0:1]:

    print('\n Processing %s' % folder)
    
    run = bkg.WPSRun(folder)

    # Path where the unprocessed GRIB files live
    grib_file_path = os.path.join(grib_directory, folder, 'postprd')

    # Create working folder / Where we'll process the GRIB files 
    run.create_working_folder(working_directory)

    # Write a namelist for WPS executables 
    run.write_namelist_wps()

    # Write a namelist for real.exe 
    run.write_namelist_real()

    # Write sbatch submission script for slurm 
    run.write_slurm_script(grib_file_path) 

    # Copy over supporting files 
    print('... Copying over WPS files to working folder ...')
    bkg.copy_folder_contents(wps_fn, run.working_folder)

    # Write down shell command to launch that run 
    run.write_shell_command(fshell)

    print('%s is ready to run! \n\n' % folder)
