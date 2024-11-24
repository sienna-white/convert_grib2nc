Sienna White

 siennaw@berkeley.edu  
 
 Note: As of November 2024, we have removed the real.exe step from this process. 

# Read Me 
Past HRRR-Smoke runs are archived as a GRIB2 files. GRIB2 is essentially a fancy compressed binary file format for weather model outputs. Unfortunately, GSI cannot read these GRIB2 files (in fact, almost nothing can read GRIB2 files), so in order to run GSI, we will have to convert the GRIB2 files into NETCDF. NETCDF is a common and friendly data type for multi-dimensional environmental data.

This process (converting GRIB2 → NETCDF) is one of the most tedious parts of setting up a GSI run. I created this repository to hopefully explain what's happening in a fairly accessible manner. 

Here is what is happening at each stage of the process:
 
 [WPS Suite] (input file : namelist.wps)
   1. Ungrib: This step unpacks the binary GRIB2 files and places them in an interim file format (unreadable to us humans). It unpacks the variables we define the in the ungrib Vtable. It will automatically assign the units we denote in the Vtable as well. (This will be important when we start worrying about what units things are in – NOAA changed its standard units for smoke in 2021.) Ungrib is fairly slow! It runs in serial and tends to take about 10 minutes per hour time step, as far as I can tell.
      
   2. Geogrid: This step creates a grid for our data, using geographic parameters defined in the namelist.wps file. This is where we are cropping data to just California reigon. This step is very fast.
  
   3. Metgrid: This step takes the ungribbed files, and interpolates them onto the grid we created w/ geogrid. The output of metgrid are a bunch of netcdf files that start with “met_em” (one for each hour). This step is relatively fast.

[Last step: NOT WPS]   

  4.  Python post-processing: this step is pretty silly. Historically, we would run a fourth executable (real.exe) that took the metgrid file and created a "wrfinput" file. However, now that NOAA is providing very sparse datasets (Eg, just smoke-- no temperature, wind, etc), real.exe won't run (that program is designed to create an initial condition for WRF the weather model!). So, we do a bit of a silly hack, where we take a template wrfinput file and just drag-and-drop in our data from metgrid and update the date. We do this with a python script. 

For more info on WPS, I recommend :  [https://ral.ucar.edu/sites/default/files/public/Lesson-wps.html] 

## Using this repository
From your (user) end, you’ll need to do the following in order to convert HRRR-Smoke output from GRIB2 → netcdf:

 1. Download or locate your GRIB files 
 2. Create a folder where you want the files to be processed
 3. Use the “1_set_up_bkg.py” script to pre-process the GRIB files and set up WPS for your GRIB files.
 4. Submit all the WPS/REAL jobs to slurm using provided script (will output at the end of step 3).
 
## Step 1 : Downloading grib files + directory structure 

In order to start the conversion, you need a folder somewhere on scratch that contains all your grib files. This will probably be in Becca's directory. All the grib files should be in their own subdirectory. Ideally it will look something like this:

```
 grib_folder/
   2018110800/
      gribfile.grib2
      anothergrib.grib2
   2018110800/ 
   ... etc 
```

From what I can tell, when you download grib files from the internet, they come tarballed as these directories. So hopefully getting this directory structure isn't too much of a hassle. Each folder name contains very important info about the date of the grib files. The format is [YEAR][MONTH][DAY][HOUR]. Inside, the grib files represent forecasts starting \textit{from that start time.}. So if the name of the folder ends in 18 (6pm) than the first file is the forecast at 6pm, second file is 7pm, etc. 

## Step 2: Make a "working folder" to process files in. 
This can be as simple as just some directory within your scratch directory. Just make a folder and copy its path. I will refer to this as your "working directory." 

    cd /my_scratch_directory/ 

    mkdir working/ 


## Step 3: Getting your executables
If you want to compile the executables yourself, awesome. It will be a bit of a challenge. For now, the step is set up to copy the exectuables out of my scratch directory. 

## Step 4: Running 1_set_up_bkg.py
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

    $ python 1_set_up_bkg.py

This script has two options (GENERATE_LIST_OF_FOLDERS=True or GENERATE_LIST_OF_FOLDERS=False). You will want to run this script twice. The first time, change GENERATE_LIST_OF_FOLDERS=True. This changes the purpose of the script: instead of doing a billion things to set up the conversion, it just goes into the grib_directory and writes you a nice textfile with a list of every folder in that directory. After it does this, it will ask if you want to continue. Enter "n" to say no. It's good practice to glance over the list you just generated, and make sure everything looks reasonable. 

Once you've done that, change GENERATE_LIST_OF_FOLDERS=False and run the script again. This will take a lot longer. Now, the script is generating subdirectories in your working folder and setting up all the "ingredients" for a conversion run in each folder. 

Once this is done, the script will print out that you can run a shell script to submit all the jobs it just created. You can do that in the command line,
```
  $ ./jobs2run 
```
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


