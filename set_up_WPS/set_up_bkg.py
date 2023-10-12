

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
            self.end_time    = date.replace(hour=23, minute=0, second=0)
            self.end_time_str = self.end_time.strftime('%Y-%m-%d_%H:00:00')
            self.start_time_str = self.start_time.strftime('%Y-%m-%d_%H:00:00')
            print('Created class object for GRIB folder \n \
                  \t Dates : %s - %s' % (self.start_time_str - self.end_time_str))
        except:
            print('Erroring initializing file! Check folder name: \t%s' % folder) 

    def sub(self, pattern1, pattern2):
        # regex sub
        self.text = re.sub(pattern1, pattern2, self.text)
        return self

    def write_namelist_wps(self, dest_dir):
        '''' Write a namelist file to convert all the grib files in that folder. ''' 

        with open('namelist_template.txt') as f:
            namelist = f.read()
            namelist = namelist.replace('REPLACE_START_DATE', self.start_time_str)
            namelist = namelist.replace('REPLACE_END_DATE', self.end_time_str)

            fout = os.path.join(dest_dir, 'namelist.wps')
            with open(fout, 'w') as f:
                f.write(namelist)

        print('\t Wrote namelist.wps file: \t%s' % fout)

    def write_namelist_real(self, dest_dir):

        with open('namelist_real_template.txt') as f:

            namelist = f.read()
            namelist = namelist.replace('REPLACE_START_DATE',   self.start_time_str)        
            namelist = namelist.replace('REPLACE_START_MONTH',  str(self.start_time.month))
            namelist = namelist.replace('REPLACE_START_DAY',    str(self.start_time.day))
            namelist = namelist.replace('REPLACE_START_HOUR',   str(self.start_time.hour))
            namelist = namelist.replace('REPLACE_START_YEAR',   str(self.start_time.year))

            # END YEAR, MONTH, DAY are the same as the start date & the end time is always 23:00
            fout = os.path.join(dest_dir, 'namelist.input')
            with open(fout, 'w') as f:
                f.write(namelist)
        print('\t Wrote namelist.input file: \t%s' % fout)

    
def write_job_script(self, working_directory, grib_file_path):
    ''' Write a slurm batch script for the whole WPS process
    input:
        * working directory : folder you want to write script in
        * grib_file_path : folder where the grib files live 
        * folder : string with the name of the folder / file extension. should be the date in str form.
    ''' 

    with open('submit_wps_template.txt') as f:
        job_name = 'WPS_%s' % self.folder
        submit_wps_job = f.read()
        grib_file_path = '%s/*' % grib_file_path
        submit_wps_job = submit_wps_job.replace('REPLACE_WORKING_DIRECTORY', working_directory)
        submit_wps_job = submit_wps_job.replace('REPLACE_GRIB_FILE_PATH', grib_file_path)
        submit_wps_job = submit_wps_job.replace('REPLACE_JOB_NAME', job_name)
        submit_wps_job = submit_wps_job.replace('REPLACE_START_HOUR', str(self.start_time.hour)) 
        submit_wps_job = submit_wps_job.replace('REPLACE_DATE', self.start_time.strftime('%Y-%m-%d'))

        
        fout = os.path.join(working_directory, 'submit_wps_job.sh')
        with open(fout, 'w') as f:
            f.write(submit_wps_job)
    print('Wrote submit_wps_job.sh --> %s' % fout)
    # A bit confusing, but we want to now return the command-line expression needed 
    # to execute this script. This will be two lines of code -- opening the directory,
    # and then batching the script
    command_line = []
    # Open the working directory
    command_line.append('cd %s' % working_directory)
    # Submit the job 
    command_line.append('sbatch %s ' % fout)

    return (command_line)
