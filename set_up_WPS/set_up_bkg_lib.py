import os 
import pandas as pd 
import shutil
import pandas as pd 


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
        
class WPSRun:
    '''
    Class definition for Regex objects
    '''
    def __init__(self, folder):
        # assign input text to self.text
        self.folder = folder 

        try:
            date = pd.to_datetime(folder, format='%Y%m%d%H')
            self.date        = date
            self.start_time  = date
            self.end_time    = date + pd.Timedelta(hours=24)  # SW change on 2/14/2025 -- want to convert 24 hours 
            self.end_time_str = self.end_time.strftime('%Y-%m-%d_%H:00:00')
            self.start_time_str = self.start_time.strftime('%Y-%m-%d_%H:00:00')
            self.date_standard = folder
            print('Created class object for GRIB folder') 
            print('\t Dates : %s - %s' % (self.start_time_str , self.end_time_str))
            self.does_not_exist = False
        except:
            print('Erroring initializing file! Check folder name: \t%s' % folder) 
            self.does_not_exist = True

    def create_working_folder(self, working_directory): 
        ''' Create a folder in a specified directory.
        * working_directory --> filepath of where you want to create your folder [str]
        * folder_name --> name of the folder you're making [str]''' 
        folder_path = os.path.join(working_directory, self.folder)
        try:
            os.makedirs(folder_path)
            print(f"\t Folder '{folder_path}' created successfully.")
        except FileExistsError:
            print(f"\t Folder '{folder_path}' already exists")

        self.working_folder = folder_path
     
      

    def write_namelist_wps(self):
        '''' Write a namelist file to convert all the grib files in that folder. ''' 
        working_folder = self.working_folder 
        
        with open('namelist_template.txt') as f:
            namelist = f.read()
            namelist = namelist.replace('REPLACE_START_DATE', self.start_time_str)
            namelist = namelist.replace('REPLACE_END_DATE', self.end_time_str)

            fout = os.path.join(working_folder, 'namelist.wps')
            with open(fout, 'w') as f:
                f.write(namelist)

        print('\t Wrote namelist.wps file: \t%s' % fout)

    def write_namelist_real(self):
        working_folder = self.working_folder 

        with open('namelist_real_template.txt') as f:

            namelist = f.read()
            namelist = namelist.replace('REPLACE_START_DATE',   self.start_time_str)        
            namelist = namelist.replace('REPLACE_START_MONTH',  str(self.start_time.month))
            namelist = namelist.replace('REPLACE_START_DAY',    str(self.start_time.day))
            namelist = namelist.replace('REPLACE_START_HOUR',   str(self.start_time.hour))
            namelist = namelist.replace('REPLACE_START_YEAR',   str(self.start_time.year))

            # END YEAR, MONTH, DAY are the same as the start date & the end time is always 23:00
            fout = os.path.join(working_folder, 'namelist.input')
            with open(fout, 'w') as f:
                f.write(namelist)
        print('\t Wrote namelist.input file: \t%s' % fout)

    def copy_executables(self):
        destination_folder = self.working_folder
        source_folder = '/global/scratch/users/siennaw/gsi_2024/compiling/wrf_executables'

        # Get a list of all files and subdirectories in the source folder
        items = os.listdir(source_folder)
        try:
            for item in items:
                source_item_path = os.path.join(source_folder, item)
                destination_item_path = os.path.join(destination_folder, item)

                # If the item is a file, copy it to the destination folder
                if os.path.isfile(source_item_path):
                    shutil.copy(source_item_path, destination_item_path)
                    
        except Exception as e:
            print(f"Error copying folder contents: {e}")

    def copy_wps_files(self):
        destination_folder = self.working_folder
        source_folder = '../wps_files/'

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

    def write_slurm_script(self, grib_file_path, output_directory):
        ''' Write a slurm batch script for the whole WPS process
        input:
            * working directory : folder you want to write script in
            * grib_file_path : folder where the grib files live 
            * folder : string with the name of the folder / file extension. should be the date in str form.
        ''' 
        working_directory = self.working_folder 

        with open('submit_wps_template_2.txt') as f:
            job_name = 'WPS_%s' % self.folder
            self.job_name  = job_name 
            submit_wps_job = f.read()
            grib_file_path = '%s/*' % grib_file_path
            submit_wps_job = submit_wps_job.replace('REPLACE_WORKING_DIRECTORY', working_directory)
            submit_wps_job = submit_wps_job.replace('REPLACE_GRIB_FILE_PATH', grib_file_path)
            submit_wps_job = submit_wps_job.replace('REPLACE_JOB_NAME', job_name)
            submit_wps_job = submit_wps_job.replace('REPLACE_START_HOUR', str(self.start_time.hour)) 
            submit_wps_job = submit_wps_job.replace('REPLACE_DATE', self.start_time.strftime('%Y-%m-%d'))
            submit_wps_job = submit_wps_job.replace('REPLACE_FULL_DATE', self.date_standard)
            submit_wps_job = submit_wps_job.replace('REPLACE_OUTPUT_DIRECTORY', output_directory)
            
            fout = os.path.join(working_directory, 'submit_wps_job.sh')
            with open(fout, 'w') as f:
                f.write(submit_wps_job)
        print('\t Wrote submit_wps_job.sh: %s' % fout)

    def write_shell_command(self, fout):
        # A bit confusing, but we want to now return the command-line expression needed 
        # to execute this script. This will be two lines of code -- opening the directory,
        # and then batching the script
        with open(fout, 'a') as f:
            f.write('# Launch run for %s\n' % self.start_time_str)
            f.write('cd %s\n'     % self.working_folder)
            f.write('sbatch submit_wps_job.sh \n')
        return 

   
