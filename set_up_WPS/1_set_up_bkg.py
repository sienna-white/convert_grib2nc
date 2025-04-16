'''
How To Process GRIB files Using this Script!!! 

** INPUTS ** 
There are three user inputs required to run this script. I will explain each of them
below.
    (1) working_directory --> this is the directory that you want the actual "processing"
                              to occur in. The script will create a bunch of folders in this
                              directory. Think of it as sort of a workspace that you don't 
                              mind getting pretty messy.

    (2) output_directory --> this is the directory where the script will OUTPUT all finished 
                             netcdfs. So every "completely processed" file will be saved here.
                             All the interim stuff will stay in the working directory.

    (3) GENERATE_LIST_OF_FOLDERS --> This is a boolean value (True or False). I will explain its 
                                     significance below.


** HOW TO USE **                                     
In order to convert your grib files to netcdf, you will probably want to run 
this script twice. The first time you run this, you should set 

    GENERATE_LIST_OF_FOLDERS = True

This instructs the script to look in the in the folder where I've put all the grib files 
and TELLS YOU WHAT'S THERE. It will write a list of all available folders w/ grib files 
to "folders2process.txt". It will then ask you if you want to continue. Unless you want to 
process every single folder (unlikely) you should type 'n' for NO. 

Once you've generated "folders2process.txt" you can look at the file manually and delete
any folders you're not interested in processing. My hopes is that this workflow will enable
better batch-scale processing. 

Now that  "folders2process.txt" is ready to go, set 

    GENERATE_LIST_OF_FOLDERS = True

and run again! This should actually write all the input files / etc and set up the folders 
in your working directory. The script will then print out a shell command to submit all your 
jobs to slurm. You can copy and paste that into terminal to launch the jobs! 
'''

######### USER INPUT #############
GENERATE_LIST_OF_FOLDERS = True # True or False

# Where we will process our files (Change to a folder on your scratch)
working_directory = '/global/scratch/users/siennaw/gsi_2024/grib2nc/2021/test/'

# Where the finished files should be saved
output_directory = '/global/scratch/users/siennaw/gsi_2024/grib2nc/107/finished'

# Where the grib files live 
grib_directory = "/global/scratch/users/rasugrue/HRRR_download/MASSDEN_copy/"
# grib_directory ='/global/scratch/users/rasugrue/convert/smallgrib_NOAA_Nov2024/from_MSU'
####################################

import os 
import sys
if os.getcwd() not in sys.path: # Add the current directory to the Python path
    sys.path.append(current_directory)
import pandas as pd 
import set_up_bkg_lib as bkg 
import stat

#################### Do not change these. ############################## 
# WPS files 
wps_fn = '../wps_files/'

# List of folders to process 
fout=  sys.argv[1]  #"folders2process.txt" #sys.argv[1]  #sys.argv[1] #'folders2process.txt' #sys.argv[1] #
# fout = 'folders2020.txt'
 
# Shell script to launch written jobs 
fshell =  sys.argv[2] #'jobs2run.sh' #sys.argv[2] #
print("Shell script to launch jobs: ", fshell)

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

    # Get argument passed to script 
    # fout = sys.argv[1]
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
for f,folder in enumerate(grib_folders):

    print('\n Processing %s [%d/%d]' % (folder, f, len(grib_folders)))
    
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
    run.write_slurm_script(grib_file_path, output_directory) 

    # Copy over supporting files 
    print('... Copying over WPS files to working folder ...')
    run.copy_wps_files() 
    run.copy_executables()

    # Write down shell command to launch that run 
    run.write_shell_command(fshell)

    print('%s is ready to run! \n\n' % folder)

# Make the shell script exectuable 
st = os.stat(fshell)
os.chmod(fshell, st.st_mode | stat.S_IEXEC)
print('To submit jobs, run: \n \t $ ./%s' % fshell)