######### USER INPUT #############

'''
If this is false, the script will run and process ALL the files in the text file
"folders2process.txt". If it is true, it will check your grib directory and write 
a list of all folders w/ grib files to "folders2process.txt" and then check if you want
to continue. 


'''
GENERATE_LIST_OF_FOLDERS = False # True or False

####################################

import os 
import sys
if os.getcwd() not in sys.path: # Add the current directory to the Python path
    sys.path.append(current_directory)
import pandas as pd 
import set_up_bkg_lib as bkg 
import stat



# Where the grib files live (Do not change)
grib_directory = '/global/scratch/users/siennaw/scratch/data/grib/'

# Where we will process our files (Change to a folder on your scratch)
working_directory = '/global/scratch/users/siennaw/tmp/data/bkg/grib2wrf/'


# Do not change these. 
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
    grib_folders = bkg.get_folders_in_directory(grib_directory)

    print('Found the following folders to convert ...')
    with open(fout, 'w') as f:
        for folder in grib_folders:
            f.write(folder + '\n')
            print(folder)

    user = input("List of folders has been written. Continue running (enter: y) or stop the script (enter: n)?")
    if user == 'n':
        exit()
    elif user == 'y':
        pass
    else:
        Exception("No valid input given.")


with open(fout, 'r') as f:
    grib_folders = f.read()
    grib_folders = list(grib_folders.split('\n'))

# Remove empty strings 
grib_folders = list(filter(None, grib_folders))

# Loop through each grib folder and prep a WPS run namelist
for folder in grib_folders:

    print('\n Processing %s' % folder)
    
    run = bkg.WPSRun(folder)

 
    if run.does_not_exist:
        print('Skipping set-up for %s.' % folder)
        print('* This might be because the folder name is not a date, or because \
                it\'s formatted incorrectly. Double-check %s.' % fout)
        continue 

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

# Make the shell script exectuable 
st = os.stat(fshell)
os.chmod(fshell, st.st_mode | stat.S_IEXEC)
print('To submit jobs, run: \n \t $ ./%s' % fshell)