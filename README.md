Sienna White
siennaw@berkeley.edu 
July 27 2023

# Read Me 

A huge part of GSI involves taking binary files (GRIB) and converting them to wrfinput files, which are netcdf files. This repository is designed to facilitate that process.

There are four main steps that are involved in creating wrfinput files listed below. Three of them are housed under the "WPS" software, while the last exectuable "real.exe" is part of the WRF suite. 

For more info on WPS, I recommend :  [https://ral.ucar.edu/sites/default/files/public/Lesson-wps.html] 

 
 [WPS Suite] (input file : namelist.wps)
 
     (1) ungrib  --> takes grib files and "unpacks" them to an interim file format. Ungrib will call a Variance Table. 
     
     (2) geogrid --> creates geogrid netcdf object with the specified spatial dimensions you'd like for your domain
     
     (3) metgrid --> interpolates ungribbed-object onto the geogrid to create a met_em netcdf file 
     
 [WRF Suite] (input file : namelist.input) 
 
     (4) real    --> creates wrfinput file from the met_em netcdf file. 
     
Thus, for each grib file, we need to run 4 (!) executables and create 2 input files (namelist.wps, and namelist.input.) 

# Step 1 : Downloading grib files + directory structure 
In order to start the conversion, you need a folder somewhere on scratch that contains all your grib files. All the grib files should be in their own subdirectory. Ideally it will look something like this:

   grib_folder/
      2018110800/
         gribfile.grib2
         anothergrib.grib2
      2018110800/ 
      ... etc 
  
From what I can tell, when you download grib files from the internet, they come tarballed as these directories. So hopefully getting this directory structure isn't too much of a hassle. Each folder name contains very important info about the date of the grib files. The format is [YEAR][MONTH][DAY][HOUR]. Inside, the grib files represent forecasts starting \textit{from that start time.}. So if the name of the folder ends in 18 (6pm) than the first file is the forecast at 6pm, second file is 7pm, etc. 



I am going to try and document how best to run WPS to convert GRIB files from HRRR-Smoke model runs into input files for GSI. I created
this directory as a base directory with all the needed files (thank you
Adam!) 

In order to run this, you need to create your own folder where you
want your output to live (and your analysis.) 

# Make your analysis folder somewhere where file size / memory 
will not be an issue 

cd /my_scratch_directory/ 
mdkir my_folder/ 
cd my_folder/

Next, you're going to copy over all the files in this folder to your
folder. 

cp -r /global/home/users/siennaw/scratch/WPS/wps_files/* .


This will make sure you have all the pieces you need. You will need 
to edit your namelist.wps file!  I struggled a lot with getting the date right. 
Seems like keeping the grib file linked to the date it belongs to is a tricky task indeed. Might require some good folder organization.  


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



Running WPS to pre-process GRIB HRRR-Smoke output + preparing it for GSI
Sienna White // July 27 2023

I am going to try and document how best to run WPS to convert GRIB
files from HRRR-Smoke model runs into input files for GSI. I created
this directory as a base directory with all the needed files (thank you
Adam!) 

This code is about as automated as I could make it. 

    * namelist.input template : 



This will make sure you have all the pieces you need. You will need 
to edit your namelist.wps file!  I struggled a lot with getting the date right. 
Seems like keeping the grib file linked to the date it belongs to is a tricky task indeed. Might require some good folder organization.  


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
