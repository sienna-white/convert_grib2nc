#!/bin/bash

# Add the current directory to the Python path
current_directory="$(dirname "$0")"

# Replace 'grib2wrf_directory' with the path of the directory containing the 'grib2wrf_folders'
grib2wrf_directory="path_to_grib2wrf_directory"

# Define the 'grib2wrf_folders' list
grib2wrf_folders=("1" "2")


for folder in "${grib2wrf_folders[@]}"; do
  echo -e "\nLooking for finished runs in $folder"

  # Create a folder for the finished netcdf
  netcdf_folder="dest_folder"

  # Strip the date of the data from the folder name, figure out start + end times
  start_time=$(python -c "import set_up_wps_util as util; print(util.folder_name_to_date('$folder')[0])")
  end_time=$(python -c "import set_up_wps_util as util; print(util.folder_name_to_date('$folder')[1])")

  grib2wrf_file_path="$grib2wrf_directory/$folder"

  if [ -d "$grib2wrf_file_path" ]; then
    # Copy over finished files

    for file in "$grib2wrf_file_path"/*.nc; do
      if [ -f "$file" ]; then
        cp "$file" "$netcdf_folder"
        echo "... Copying over $file ..."
        # To access 'start_time' in the Python script, you need to write it to a file or use it as needed.
        echo "$(date -d "$start_time" +"%B/%d/%Y")" >> output.txt
      fi
    done
  else
    echo "No finished files found in $grib2wrf_file_path!"
  fi
done
