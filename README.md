Sienna White
siennaw@berkeley.edu 
July 27 2023

# Read Me 

A huge part of GSI involves taking binary files (GRIB) and converting them to wrfinput files, which are netcdf files. This repository is designed to facilitate that process.

There are four main steps that are involved in creating wrfinput files listed below. Three of them are housed under the "WPS" software, while the last exectuable "real.exe" is part of the WRF suite. 

For more info on WPS, I recommend :  [https://ral.ucar.edu/sites/default/files/public/Lesson-wps.html] 

Note: As of November 2024, we have removed the real.exe step from this process. 
 
 [WPS Suite] (input file : namelist.wps)
 
     (1) ungrib  --> takes grib files and "unpacks" them to an interim file format. Ungrib will call a Variance Table. 
     
     (2) geogrid --> creates geogrid netcdf object with the specified spatial dimensions you'd like for your domain
     
     (3) metgrid --> interpolates ungribbed-object onto the geogrid to create a met_em netcdf file 
          
Thus we need to run 3 (!) executables and create a unique input file (namelist.wps) for each file. Since this is so time-consuming, this process was created to try and automate as much as possible. I'll list the steps below.

# Step 1 : Downloading grib files + directory structure 

In order to start the conversion, you need a folder somewhere on scratch that contains all your grib files. This will probably be in Becca's directory. All the grib files should be in their own subdirectory. Ideally it will look something like this:

 grib_folder/
   2018110800/
      gribfile.grib2
      anothergrib.grib2
   2018110800/ 
   ... etc 

From what I can tell, when you download grib files from the internet, they come tarballed as these directories. So hopefully getting this directory structure isn't too much of a hassle. Each folder name contains very important info about the date of the grib files. The format is [YEAR][MONTH][DAY][HOUR]. Inside, the grib files represent forecasts starting \textit{from that start time.}. So if the name of the folder ends in 18 (6pm) than the first file is the forecast at 6pm, second file is 7pm, etc. 

# Step 2: Make a "working folder" to process files in. 
This can be as simple as just some directory within your scratch directory. Just make a folder and copy its path. I will refer to this as your "working directory." 

    cd /my_scratch_directory/ 

    mkdir working/ 


# Step 3: Getting your executables
If you want to compile the executables yourself, awesome. It will be a bit of a challenge. For now, the step is set up to copy the exectuables out of my scratch directory. 

# Step 4: Running 1_set_up_bkg.py
This is the main script that will do 99% of the work for you! So please don't edit anything without asking me. You need to edit the first couple lines of the script. It will look like this:

 ```
  ######### USER INPUT #############
  GENERATE_LIST_OF_FOLDERS = True # True or False
  
  # Where we will process our files (Change to a folder on your scratch)
  working_directory = '/global/scratch/users/siennaw/gsi_2024/grib2nc/working/'
  
  # Where the finished files should be saved
  output_directory = '/global/scratch/users/siennaw/gsi_2024/grib2nc/finished/'
  
  # Where the grib files live 
  grib_directory = '/global/scratch/users/rasugrue/convert/smallgrib_NOAA_Nov2024/'
  ####################################
```
 Note that the working directory should be the path to the folder you just created. The finished files directory doesn't matter-- right now that's not used at all. And the grib_directory will be a path we'll provide-- it's whatever folder Becca/Tina or myself have downloaded HRRR files into. 

This script has two options (GENERATE_LIST_OF_FOLDERS=True or GENERATE_LIST_OF_FOLDERS=False). You will want to run this script twice. The first time, change GENERATE_LIST_OF_FOLDERS=True. This changes the purpose of the script: instead of doing a billion things to set up the conversion, it just goes into the grib_directory and writes you a nice textfile with a list of every folder in that directory. After it does this, it will ask if you want to continue. Enter "n" to say no. It's good practice to glance over the list you just generated, and make sure everything looks reasonable. 

Once you've done that, change GENERATE_LIST_OF_FOLDERS=False and run the script again. This will take a lot longer. Now, the script is generating subdirectories in your working folder and setting up all the "ingredients" for a conversion run in each folder. 

Once this is done, the script will print out that you can run a shell script to submit all the jobs it just created. You can do that in the command line,

  $ ./jobs2run 

 and now all your conversion jobs will be submitted to sbatch! 
 



** Ignore ** 
Original geogrid file (for CONUS):
    &geogrid
    parent_id         = 1,
    parent_grid_ratio = 1,
    i_parent_start    = 1,
    j_parent_start    = 1,
    e_we          = 1800,
    e_sn          = 1060,
    geog_data_res = 'modis_15s+modis_fpar+modis_lai+30s',
    dx = 3000,
    dy = 3000,
    map_proj =  'lambert',
    ref_lat   = 38.5,
    ref_lon   = -97.5,
    truelat1  = 38.5,
    truelat2  = 38.5,
    stand_lon = -97.5,
    geog_data_path = '/global/home/groups/co_aiolos/chow/geog_v3.6',
    ref_x = 900.0,
    ref_y = 530.0,
    /


OLD:
    Original geogrid file (for CONUS):
    &geogrid
    parent_id         = 1,
    parent_grid_ratio = 1,
    i_parent_start    = 1,
    j_parent_start    = 1,
    e_we          = 1800,
    e_sn          = 1060,
    geog_data_res = 'modis_15s+modis_fpar+modis_lai+30s',
    dx = 3000,
    dy = 3000,
    map_proj =  'lambert',
    ref_lat   = 38.5,
    ref_lon   = -97.5,
    truelat1  = 38.5,
    truelat2  = 38.5,
    stand_lon = -97.5,
    geog_data_path = '/global/home/groups/co_aiolos/chow/geog_v3.6',
    ref_x = 900.0,
    ref_y = 530.0,
    /


     data = xr.open_dataset("blank_wrfinput")
 
 blank_netcdf =  data.get(['PM2_5_DRY'])#, 'RH', 'Q', 'QVAPOR']) 
 
 print(blank_netcdf)
 
 blank_netcdf.to_netcdf("blank_wrfinput.nc")
 
 source activate smoke_env


