
import os 
import pandas as pd 
import shutil


'''
Below is a collection of functions called by set_up_wps. I use these
functions to set up a bunch of WPS runs in order to (hopefully) pre-process a
bunch of GRIB files and prep them for the GSI run. 
'''


def get_folders_in_directory(directory_path):
    ''' Get a list of folders in a directory ''' 
    # Check that our directory exists
    if not os.path.isdir(directory_path):
        raise Exception("Error: Directory not found.")
    # Get a list of folders in the directory
    folders = [entry for entry in os.listdir(directory_path) if os.path.isdir(os.path.join(directory_path, entry))]
    if len(folders) == 0:
        raise Exception("No folders found in the directory.")
    return folders


def create_folder(working_directory, folder_name):
    ''' Create a folder in a specified directory.
        * working_directory --> filepath of where you want to create your folder [str]
        * folder_name --> name of the folder you're making [str]''' 
    folder_path = os.path.join(working_directory, folder_name)
    try:
        os.makedirs(folder_path)
        print(f"... Folder '{folder_path}' created successfully.")
    except FileExistsError:
        print(f"... Folder '{folder_path}' already exists")
         


def folder_name_to_date(folder):
    ''' Take the sort of bizarre name of our GRIB folders, which are the dates the files are from.
    Parse this name into a reasonable date. ''' 

    try:
        date = pd.to_datetime(folder, format='%Y%m%d%H')
    except:
        print('Erroring parsing folder.') 

    print('... Parsing %s  --> Run date is: %s' % (folder, date.strftime('%B %d,%Y %H:00')))
    start_time  = date
    end_time    = date.replace(hour=23, minute=0, second=0) # time at 11pm that same day
    # print(start_time, end_time)
    return start_time, end_time

def date2str(date):
    return date.strftime('%Y-%m-%d_%H:00:00')

def write_namelist_wps(start_time, end_time, dest_dir):
    with open('namelist_template.txt') as f:
        namelist = f.read()
        namelist = namelist.replace('REPLACE_START_DATE', date2str(start_time))
        namelist = namelist.replace('REPLACE_END_DATE', date2str(end_time))
        fout = os.path.join(dest_dir, 'namelist.wps')
        with open(fout, 'w') as f:
            f.write(namelist)
    print('... Wrote namelist file  --> %s' % fout)

def write_namelist_real(start_time, end_time, dest_dir):
    with open('namelist_real_template.txt') as f:
        namelist = f.read()
        namelist = namelist.replace('REPLACE_START_DATE',   date2str(start_time))        
        namelist = namelist.replace('REPLACE_START_MONTH',  str(start_time.month))
        namelist = namelist.replace('REPLACE_START_DAY',    str(start_time.day))
        namelist = namelist.replace('REPLACE_START_HOUR',   str(start_time.hour))
        namelist = namelist.replace('REPLACE_START_YEAR',   str(start_time.year))

        # END YEAR, MONTH, DAY are the same as the start date & the end time is always 23:00

        fout = os.path.join(dest_dir, 'namelist.input')
        with open(fout, 'w') as f:
            f.write(namelist)
    print('... Wrote namelist file  --> %s' % fout)



def copy_folder_contents(source_folder, destination_folder):
# thank you chat gpt for this
   import os
    import shutil

def copy_folder_contents(source_folder, destination_folder):
    try:
        # Create the destination folder if it doesn't exist
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)

        # Get a list of all files and subdirectories in the source folder
        items = os.listdir(source_folder)

        for item in items:
            source_item_path = os.path.join(source_folder, item)
            destination_item_path = os.path.join(destination_folder, item)

            # If the item is a file, copy it to the destination folder
            if os.path.isfile(source_item_path):
                shutil.copy(source_item_path, destination_item_path)

            # If the item is a subdirectory, recursively copy its contents
            elif os.path.isdir(source_item_path):
                copy_folder_contents(source_item_path, destination_item_path)

    except Exception as e:
        print(f"Error copying folder contents: {e}")


def write_job_script(working_directory, grib_file_path, start_time, folder):
    ''' Write a slurm batch script for the whole WPS process
    input:
        * working directory : folder you want to write script in
        * grib_file_path : folder where the grib files live 
        * folder : string with the name of the folder / file extension. should be the date in str form.
    ''' 
    with open('submit_wps_template.txt') as f:
        job_name = 'WPS_%s' % folder
        submit_wps_job = f.read()
        grib_file_path = '%s/*' % grib_file_path
        submit_wps_job = submit_wps_job.replace('REPLACE_WORKING_DIRECTORY', working_directory)
        submit_wps_job = submit_wps_job.replace('REPLACE_GRIB_FILE_PATH', grib_file_path)
        submit_wps_job = submit_wps_job.replace('REPLACE_JOB_NAME', job_name)
        submit_wps_job = submit_wps_job.replace('REPLACE_START_HOUR', str(start_time.hour)) 
        submit_wps_job = submit_wps_job.replace('REPLACE_DATE', start_time.strftime('%Y-%m-%d'))

        
        fout = os.path.join(working_directory, 'submit_wps_job.sh')
        with open(fout, 'w') as f:
            f.write(submit_wps_job)
    print('... Wrote shell script --> %s' % fout)
    # A bit confusing, but we want to now return the command-line expression needed 
    # to execute this script. This will be two lines of code -- opening the directory,
    # and then batching the script
    command_line = []
    # Open the working directory
    command_line.append('cd %s' % working_directory)
    # Submit the job 
    command_line.append('sbatch %s ' % fout)

    return (command_line)


def check_for_finished_netcdf(directory_path):
    # List all files in the directory
    files_in_directory = os.listdir(directory_path)

    # Check if any file has the specified file extension
    finished_files = [i for i in files_in_directory if 'met_em' in i]
    if len(finished_files)>0:
        print('... %d processed files found.' % len(finished_files))
        return True
    else:
        return False 
