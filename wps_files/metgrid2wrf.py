import xarray as xr
import sys

# Get arguments passed to the script
metgrid_file_name = sys.argv[1]
output_file_name = sys.argv[2]

# Open the blank wrfinput file 
blank_wrf = xr.open_dataset("blank_wrfinput.nc")

# Open the metgrid file 
data = xr.open_dataset(metgrid_file_name)

# Update the time stamps 
blank_wrf = blank_wrf.assign_coords(Time=data.Time.values) 
blank_wrf.attrs['SIMULATION_START_DATE'] = data.attrs['SIMULATION_START_DATE']
blank_wrf.attrs['START_DATE'] = data.attrs['SIMULATION_START_DATE']

# Substitute in the mass density data as PM2.5 data
smoke_var_name = 'PM2_5_DRY'
blank_wrf[smoke_var_name].attrs['units'] = 'ug/m3' # UNITS = ug/m3!  # Correct the units + description
blank_wrf[smoke_var_name].attrs['description'] = data['MASSDEN'].attrs['description']

# For now, we will just use the surface layer of the metgrid data
# vertical_layers = blank_wrf.bottom_top

for i in range(0,1):
  blank_wrf[smoke_var_name][dict(bottom_top=i)] = data['MASSDEN'][dict(num_metgrid_levels=i)] 
  # We need to index array of data rather than use isel / sel. found this out the hard way.

# Save the output 
blank_wrf.to_netcdf(output_file_name)
