import xarray as xr
import sys
import os 
import pandas as pd 

# Get arguments passed to the script
metgrid_file_name = sys.argv[1]
# output_file_name  = sys.argv[2]

# Open the metgrid file 
# Check in metgrid file exists
if not os.path.exists(metgrid_file_name):
  print('Metgrid file does not exist.')
  sys.exit(1)

# Open the blank wrfinput file 
template = xr.open_dataset("blank_wrfinput.nc")
blank_wrf = template.copy()

data = xr.open_dataset(metgrid_file_name)

# Update the time stamps 
blank_wrf = blank_wrf.assign_coords(Time=data.Time.values) 
blank_wrf.attrs['SIMULATION_START_DATE'] = data.attrs['SIMULATION_START_DATE']
blank_wrf.attrs['START_DATE'] = data.attrs['SIMULATION_START_DATE']

# Get forecast hour 
forecast_date = os.path.basename(os.getcwd()) 
file_date = data.attrs['SIMULATION_START_DATE']

forecast_date = pd.to_datetime(forecast_date, format='%Y%m%d%H')
file_date = pd.to_datetime(file_date, format='%Y-%m-%d_%H:00:00')

forecast_hour =  file_date - forecast_date
forecast_hour = forecast_hour.seconds//3600 

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
blank_wrf.attrs['FORECAST_HOUR'] = forecast_hour

output_file_name = "wrfinput_d01_%s" % file_date.strftime("%Y%m%0d%0H")
output_file_name = "%s_%0d.nc" % (output_file_name, forecast_hour)

blank_wrf.to_netcdf(output_file_name)
print("Saved %s" % output_file_name)