
Sienna White 
July 27 2023

I am going to try and document how best to run WPS to convert GRIB
files from HRRR-Smoke model runs into input files for GSI. I created
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