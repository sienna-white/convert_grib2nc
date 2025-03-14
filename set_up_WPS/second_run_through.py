

# Get list of folders in a directory

import os
import sys
import xarray as xr

# /global/scratch/users/siennaw/gsi_2024/grib2nc/working/2019042716

# Get the list of folders in the directory
path = '/global/scratch/users/siennaw/gsi_2024/grib2nc/working/'
folders = os.listdir(path)
print("Found %d folders in the directory." % len(folders))

subset = folders

template = xr.open_dataset("../wps_files/blank_wrfinput.nc")

# Look for folders that contain files that start with "met_em "

for fi, folder in enumerate(subset):
    print("\nLooking in folder: %s [%d/%d]" % (folder, fi, len(subset)))
    files = os.listdir(os.path.join(path, folder))
    for file in files:
        if file.startswith("met_em"):
            # print("\tFound met_em file: %s" % file)

            file_date = file[11:24]
            file_date = file_date.replace("_", "")
            file_date = file_date.replace("-", "")

            output_file_name = "wrfinput_d01_%s.nc" % file_date

            # Open the blank wrfinput file 
            metgrid_file_name = path + folder + '/' + file

            blank_wrf = template.copy()
            data = xr.open_dataset(metgrid_file_name)

            # Check if 'MASSDEN' is a variable in the metgrid file
            if 'MASSDEN' not in data.data_vars:
                print("\t ... no MASSDEN variable in %s" % metgrid_file_name)
                continue

            # Update the time stamps 
            blank_wrf = blank_wrf.assign_coords(Time=data.Time.values) 
            blank_wrf.attrs['SIMULATION_START_DATE'] = data.attrs['SIMULATION_START_DATE']
            blank_wrf.attrs['START_DATE'] = data.attrs['SIMULATION_START_DATE']

            # Substitute in the mass density data as PM2.5 data
            smoke_var_name = 'PM2_5_DRY'
            blank_wrf[smoke_var_name].attrs['units'] = 'ug/m3' # UNITS = ug/m3!  # Correct the units + description
            blank_wrf[smoke_var_name].attrs['description'] = data['MASSDEN'].attrs['description']

            blank_wrf[smoke_var_name][dict(bottom_top=0)] = data['MASSDEN'][dict(num_metgrid_levels=0)] 
            # We need to index array of data rather than use isel / sel. found this out the hard way.

            # Save the output 
            blank_wrf.to_netcdf(output_file_name)
            print("\t ... saved %s" % output_file_name)



    # print("Done looking in folder: %s" % folder)


# #!/bin/bash
# # Job name:
# #################################
# #SBATCH --job-name=WPS_2019042714
# #
# # Account:
# #SBATCH --account=co_aiolos ## << this is the condo that tina bought // could also use fc_anemos#
# #SBATCH --partition=savio3
# #
# #SBATCH --nodes=1
# # Wall clock limit (let's set to 10 mintes, 0 seconds)
# #SBATCH --time=00:04:00
# #SBATCH -o /global/scratch/users/siennaw/gsi_2024/grib2nc/working/2019042714/slurm-stdout # STDOUT

# ## Commands to run
# cd /global/scratch/users/siennaw/gsi_2024/grib2nc/working/2019042714       

# echo "Cleaning up directory..." 
# rm *.log
# rm GRIBFILE*

# echo "Starting on spack.."
# path2spack=/global/scratch/users/siennaw/gsi_2024/compiling/spack

# # This sources the environment variables spack needs from the local spack folder
# . ${path2spack}/share/spack/setup-env.sh

# # Load in modules 
# spack load bufr
# spack load ip
# spack load sp
# spack load bacio
# spack load w3emc
# spack load sigio
# spack load sfcio
# spack load nemsio
# spack load ncio
# spack load wrf-io
# spack load crtm
# spack load blas                 #not sure if these are needed too
# spack load netcdf-fortran       #not sure if these are needed too
# spack load netcdf-c             #not sure if these are needed too
# spack load jasper
# spack load hdf5

# ######### UNGRIB ############
# # Set up + run ungrib
# echo "Linking grib files to directory..."
# ./link_grib.csh /global/scratch/users/rasugrue/convert/smallgrib_NOAA_Nov2024/from_MSU/2019042714/postprd/*

# echo "Linking HRR-SMOKE VTABLE...."
# ln -sf ungrib/Variable_Tables/Vtable.hrrr_smoke.rap Vtable

# echo -e "\tRunning ungrib..."
# ./ungrib.exe >> ungrib.out 

# ######### GEOGRID ############
# echo -e "\tRunning geogrid ..."
# ./geogrid.exe >>  geogrid.out          

# ######### METGRID ############
# echo -e "\tRunning metgrid ..."
# ./metgrid.exe >> metgrid.out

# ######### REAL ############
# echo -e "\tStarting python loop ..."
# echo "Starting loop." 

# hour0=14
# hourF=23
# DATE=2019-04-27

# for hour in $(seq $hour0 $hourF); do

#   # Add leading zero to number if needed (aka, need midnight as 00, not 0; 1 am as 01; etc)
#   hour=$(printf %02d $hour)
#   #datenum="${DATE}${hour}"
#   datenum="${DATE//-/}${hour}"
#   echo $hour 

#   date="${DATE}_${hour}:00:00"

#   met_fn=met_em.d01.${date}.nc
#   wrf_fn=wrfinput_d01
#   wrf_fn_out=wrfinput_d01_${datenum}.nc

#   ~/.conda/envs/smoke_env/bin/python -u metgrid2wrf.py $met_fn $wrf_fn_out & 
# done
# wait 
# echo "Done with python step!"

# ######### CLEAN UP! ############

# # Create stdout for this processing run
# stdout=WPS_2019042714.out
# cat ungrib.out   >  $stdout
# cat geogrid.out  >> $stdout
# cat metgrid.out  >> $stdout

# echo "Done processing grib file, wrfinput[s] created." 

# rm *.p000
# rm GRIBFILE.*
# rm FILE:*
# # rm blank_*
